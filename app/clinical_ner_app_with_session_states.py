import logging
import sys, os
sys.path.append('/workspaces/clinical_trials_ner')
import pandas as pd
import streamlit as st
from data_processing import upload_file, extract_text, process_dataframe
from jsl_backend.ner import model_and_entity_selection, extractNamedEntities
from jsl_backend.model_setup import setup_config, initSparkSession
from jsl_backend.pipeline_stages import spark, license_keys
from jsl_backend.pipeline_setup import buildNerPipeline, getEntityTypes
from jsl_backend.visualization import visualize_ner, create_multiindex_dataframe_of_groupedEntity, get_label_color
from PIL import Image
from utils import ner_chunks_to_dataframe , categorize_entities, get_or_create_session_state_variable, dataframe_to_csv, dataframe_to_json, dataframe_to_pdf, create_streamlit_buttons
import multiprocessing
from jsl_backend.entity_description_generation import loadChain, get_description_refrences
from jsl_backend.entityDescCache import entities

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
st.divider()
# Main Page Title and Caption
st.title("Entities in Clinical Trial Abstracts")  # Placeholder for title
# Placeholder for caption
st.caption("This model extracts to trial design, diseases, drugs, population,Heart_Disease, Hyperlipidemia, Diabetes, Age, Test, Test_Result, Birth_Entity, Drug_BrandName, Date, etc. relevant entities from clinical trial abstracts.")


# Input and Session Setup
# Custom CSS for styling
st.markdown("""
    <style>
       /* change the select box properties */
        div[data-baseweb="select"]>div {
        background-color:#fff;
        border-color:rgb(194, 189, 189);
        width: 100%;
    }

    /* change the tag font properties */
        span[data-baseweb="tag"]>span {
        color: black;
        font-size: 17px;
    }
    span.st-ae{
        background-color:  #FCF1C9 ;
    }
    
    .e1q9reml2 {
        color: #F4FAF3;
    }
    
    .st-f2 p{
        padding: 0.3rem 0.4rem;
        border-radius: 5px;
        background-color: #6699cc;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Groq
description_llm_chain = loadChain()

selected_model, selected_entities, light_model_pipeline, modelColumn, editorColumns = model_and_entity_selection(location=st)
get_or_create_session_state_variable(key='selected_model', default_value=selected_model)
get_or_create_session_state_variable(key='selected_entities', default_value=selected_entities)
st.session_state['selected_entities'] = selected_entities
with modelColumn:
    uploaded_file = upload_file(location=st)
get_or_create_session_state_variable(key='uploaded_file', default_value=uploaded_file)
get_or_create_session_state_variable(key='ner_html', default_value=None)
get_or_create_session_state_variable(key='df', default_value=pd.DataFrame())
get_or_create_session_state_variable(key='results', default_value=None)
get_or_create_session_state_variable(key='entity_descriptions', default_value=None)

# Process FIle Data
if uploaded_file or 'trialText' in st.session_state.keys():
    # Process File
    if uploaded_file:
        st.session_state['trialText'] = extract_text(uploaded_file)
        # st.session_state['ner_html'] = None
    
    if st.session_state['trialText'].strip():
        with modelColumn:
            st.session_state['trialText'] = st.text_area(label='Editor', value=st.session_state['trialText'], height=200, label_visibility='hidden')
            st.session_state['generateButton'] = st.button(label='Extract Entities', type='primary')
    else:
        st.info('Empty File!')
else:
    with modelColumn:
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
        st.session_state['categorizedEntities'] = categorize_entities(df=st.session_state['df'], chain=None)
        
        # Generate Description
        filtered_entities = [(chunk, entity) for chunk, entity in st.session_state['df'][['chunk', 'entity']].itertuples(index=False, name=None) if entities.get(entity.lower(), False)]
        st.session_state['entity_descriptions'] = get_description_refrences(entities=filtered_entities, llm_chain=description_llm_chain)
        
    if not st.session_state['df'].empty:
        with editorColumns:
            # On Edit Entity Label Update Vizualization
            st.session_state['ner_html'] = visualize_ner(st.session_state['results'], selected_labels=st.session_state['selected_entities'])
            
            # Columns
            titleCol, csvDownloadCol, jsonDownloadCol, pdfDownloadCol = st.columns([5.8, 1.4, 1.4, 1.4], vertical_alignment='bottom')
            # # Display the output in Streamlit
            with titleCol:
                st.markdown(
                    """
                    <h1 style="font-family: Vistol; text-align: center; font-size: 32px; margin-top: 6px; background-color:#B0CFA6; padding: 10px; border-radius: 5px; padding-left:10px; color:white;">
                        Identified Named Entities
                    </h1>
                    """
                , unsafe_allow_html=True)
            st.markdown(
            f'''
                <div class="scroll entities" style="overflow-x: auto;border: 1px solid rgb(230, 233, 239);border-radius: 0.25rem;padding: 1rem;margin-bottom: 2.5rem;white-space: pre-wrap; margin-top:10px">
                    {st.session_state['ner_html']}
                </div>
            ''',unsafe_allow_html=True)

            # st.table(st.session_state['categorizedEntities'])

            filtered_df: pd.DataFrame = st.session_state['df'][st.session_state['df']['entity'].isin(st.session_state['selected_entities'])].reset_index(drop=True).sort_values(by='entity')
            
            # Multiprocessing to speed  up download data processing
            output_queue = multiprocessing.Queue()
        
            # Create and start the process
            p = multiprocessing.Process(target=process_dataframe, args=(filtered_df, output_queue))
            p.start()

            # Wait for the process to finish
            p.join()
            
            # Get the results
            results = output_queue.get()
            csv_data = results['csv']
            json_data = results['json']
            pdf_data = results['pdf']
            
            with csvDownloadCol:
                if csv_data:
                    st.download_button(label="CSV ⤓", data=csv_data, file_name='ner_chunks.csv', mime='text/csv', use_container_width=True)
            # JSON download
            with jsonDownloadCol:
                if csv_data:
                    st.download_button(label="JSON ⤓", data=json_data, file_name='ner_chunks.json', mime='text/json', use_container_width=True)
            
            # PDF download
            with pdfDownloadCol:
                if pdf_data:
                    st.download_button(label="PDF ⤓", data=pdf_data, file_name='ner_chunks.pdf', mime='application/pdf', use_container_width=True)
            
            
            # Check Minimum One Entity Selection
            # Visualize Streamlit tabs dynamically
            keysForTabs = [key for key in st.session_state['categorizedEntities'].keys() if key in st.session_state['selected_entities']]
            if len(keysForTabs) > 0:
                # st.dataframe(st.session_state['entity_descriptions'], use_container_width=True)
                # st.write(st.session_state['entity_descriptions'].set_index('EntityName').T.to_dict('list')['chest pain'])
                tabs = st.tabs(keysForTabs)

                for i, key in enumerate(keysForTabs):
                    with tabs[i]:
                        st.header(key)
                        
                        create_streamlit_buttons(
                            list({v['chunk']:v for v in st.session_state['categorizedEntities'][key]}.values()),    # Removes duplicate entity before sending to create buttons
                            widget=editorColumns,   # PLace to Inject
                            descriptions=st.session_state['entity_descriptions'].set_index('EntityName').T.to_dict('list'),     # COnverting df into processable dicts
                        )
            else:
                st.info('No Entity Labels is Selected')
        st.divider()
        if len(st.session_state['selected_entities']) > 0: st.table(filtered_df.drop(columns=['ner_source', 'sentence']).style.apply(get_label_color, axis=1))  
    else:
        st.warning("No data available to display or download.")

# Footer with Font Awesome icons
footer_html = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<div style="text-align: center; margin-right: 10%;">
    <p>
        &copy; 2024, Trigent Software Inc. All rights reserved. |
        <a href="https://www.linkedin.com/company/trigent-software" target="_blank" aria-label="LinkedIn"><i class="fab fa-linkedin"></i></a> |
        <a href="https://www.twitter.com/trigent-software" target="_blank" aria-label="Twitter"><i class="fab fa-twitter"></i></a> |
        <a href="https://www.youtube.com/trigent-software" target="_blank" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
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