import logging
import sys, os
import pandas as pd
import streamlit as st
from data_processing import upload_file, extract_text
from ner import model_and_entity_selection, extractNamedEntities
from model_setup import setup_config, initSparkSession
from pipeline_stages import spark, license_keys
from pipeline_setup import buildNerPipeline, getEntityTypes
from visualization import visualize_ner
from PIL import Image
from sparknlp.annotator import *
from sparknlp_jsl.annotator import *
from sparknlp.base import *
from utils import ner_chunks_to_dataframe, dataframe_to_pdf, dataframe_to_csv, dataframe_to_json, categorize_entities, create_streamlit_buttons, get_or_create_session_state_variable


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Set main panel
favicon = Image.open("/workspaces/clinical_trials_ner/static/images/Trigent_Logo.png")
st.set_page_config(
    page_title="Entities in Clinical Trial | Trigent AXLR8 Labs",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Add logo and title
logo_path = "https://trigent.com/wp-content/uploads/Trigent_Axlr8_Labs.png"
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="{logo_path}" alt="Trigent Logo" style="max-width:100%;">
    </div>
    """,
    unsafe_allow_html=True
)

# Main Page Title and Caption
st.title("Entities in Clinical Trial Abstracts")  # Placeholder for title
# Placeholder for caption
st.caption("This model extracts to trial design, diseases, drugs, population, statistics, publication etc. relevant entities from clinical trial abstracts.")


# Input and Session Setup
selected_model, selected_entities, light_model_pipeline = model_and_entity_selection(location=st)
get_or_create_session_state_variable(key='selected_model', default_value=selected_model)
get_or_create_session_state_variable(key='selected_entities', default_value=selected_entities)
st.session_state['selected_entities'] = selected_entities
uploaded_file = upload_file(location=st)
get_or_create_session_state_variable(key='uploaded_file', default_value=uploaded_file)
get_or_create_session_state_variable(key='ner_html', default_value=None)
get_or_create_session_state_variable(key='df', default_value=pd.DataFrame())
get_or_create_session_state_variable(key='results', default_value=None)

# Process FIle Data
if uploaded_file or 'trialText' in st.session_state.keys():
    # Process File
    if uploaded_file:
        st.session_state['trialText'] = extract_text(uploaded_file)
        # st.session_state['ner_html'] = None
    
    if st.session_state['trialText'].strip():
        # Your text area widget
        st.markdown("""
            <h1 style="font-family: Times New Roman; color: black; text-align: left; font-size: 36px; margin-top: 20px;">
                Editor 
            </h1>
            """, unsafe_allow_html=True)
        st.session_state['trialText'] = st.text_area(label='Editor', value=st.session_state['trialText'], height=200, label_visibility='hidden')
        st.session_state['generateButton'] = st.button(label='Extract Entities', type='primary')
    else:
        st.info('Empty File!')
else:
            # Your text area widget
    st.markdown("""
            <h1 style="font-family: Times New Roman; color: black; text-align: left; font-size: 36px; margin-top: 20px;">
                Editor ✎
            </h1>
            """, unsafe_allow_html=True)
    text = st.text_area(label='Editor', value='', height=200, label_visibility='hidden', placeholder='Upload Trials data....')
    st.session_state['generateButton'] = st.button(label='Extract Entities', type='primary', disabled=True)


if st.session_state['generateButton'] and st.session_state['trialText'] or st.session_state['ner_html'] is not None:
    # build pipeline
    if  st.session_state['generateButton'] and st.session_state['trialText']:
        st.session_state['extracted_entities'], st.session_state['results'] = extractNamedEntities(
            text=st.session_state['trialText'], 
            selected_model=st.session_state['selected_model'], 
            selected_entities=st.session_state['selected_entities'],
            light_model_pipeline=light_model_pipeline
        )
    
        # # Visualize NER
        st.session_state['ner_html'] = visualize_ner(st.session_state['results'], selected_labels=st.session_state['selected_entities'])
        
                # Convert to Downloadable Document format
        st.session_state['df'] = ner_chunks_to_dataframe(ner_chunks=st.session_state['extracted_entities'])
        # Create Streamlit tabs dynamically
        st.session_state['categorizedEntities'] = categorize_entities(df=st.session_state['df'])
        
    if not st.session_state['df'].empty:
        # On Edit Entity Label Update Vizualization
        st.session_state['ner_html'] = visualize_ner(st.session_state['results'], selected_labels=st.session_state['selected_entities'])
        
        # Columns
        titleCol, csvDownloadCol, jsonDownloadCol, pdfDownloadCol = st.columns([5.8, 1.4, 1.4, 1.4], vertical_alignment='bottom')
        # # Display the output in Streamlit
        with titleCol:
            st.markdown(
                """
                <h1 style="font-family: Times New Roman: #27ae60; text-align: left; font-size: 32px; margin-top: 10px; background-color: #eafaf1; padding: 10px; border-radius: 5px;">
                    Clinical Entities
                </h1>
                """
            , unsafe_allow_html=True)
        st.markdown(
        f'''
            <div class="scroll entities" style="overflow-x: auto;border: 1px solid rgb(230, 233, 239);border-radius: 0.25rem;padding: 1rem;margin-bottom: 2.5rem;white-space: pre-wrap; margin-top:10px">
                {st.session_state['ner_html']}
            </div>
        ''',unsafe_allow_html=True)

        # st.json(st.session_state['categorizedEntities'])
    
        filtered_df = st.session_state['df'][st.session_state['df']['entity'].isin(st.session_state['selected_entities'])]
        # CSV download
        with csvDownloadCol:
            csv_data = dataframe_to_csv(filtered_df)
            if csv_data:
                st.download_button(label="CSV ⤓", data=csv_data, file_name='ner_chunks.csv', mime='text/csv', use_container_width=True)
        # JSON download
        with jsonDownloadCol:
            json_data = dataframe_to_json(filtered_df)
            if csv_data:
                st.download_button(label="JSON ⤓", data=json_data, file_name='ner_chunks.json', mime='text/json', use_container_width=True)
        
        # PDF download
        with pdfDownloadCol:
            pdf_data = dataframe_to_pdf(filtered_df)
            if pdf_data:
                st.download_button(label="PDF ⤓", data=pdf_data, file_name='ner_chunks.pdf', mime='application/pdf', use_container_width=True)
        st.table(st.session_state['df'][st.session_state['df']['entity'].isin(st.session_state['selected_entities'])])
    else:
        st.warning("No data available to display or download.")


# Footer with Font Awesome icons
footer_html = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<div style="text-align: center; margin-right: 10%;">
    <p>
        &copy; 2024, Your Company Name. All rights reserved. |
        <a href="https://www.linkedin.com/your-company" target="_blank" aria-label="LinkedIn"><i class="fab fa-linkedin"></i></a> |
        <a href="https://www.twitter.com/your-company" target="_blank" aria-label="Twitter"><i class="fab fa-twitter"></i></a> |
        <a href="https://www.youtube.com/your-company" target="_blank" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
    </p>
</div>
"""

# Custom CSS to make the footer sticky
footer_css = """
<style>
.footer {
    position: fixed;
    z-index: 1000;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
[data-testid="stSidebarNavItems"] {
    max-height: 100%!important;
}
</style>
"""

# Combining the HTML and CSS
footer = f"{footer_css}<div class='footer'>{footer_html}</div>"

# Rendering the footer
st.markdown(footer, unsafe_allow_html=True)