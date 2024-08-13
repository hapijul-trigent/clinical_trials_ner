import logging
import sys, os

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
favicon = Image.open("./static/images/Trigent_Logo.png")
st.set_page_config(
    page_title="Clinical Trials NER Application",
    page_icon=favicon,
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Streamlit application that utilizes John Snow Labs NLP models to perform Named Entity Recognition on clinical trials texts"
    }
)


# Application
# SideBar
# st.sidebar.image("static/images/Trigent_Logo.png")
st.image('static/images/Trigent_Logo_full.png', use_column_width=True)
st.sidebar.markdown(
    """
    <h1 style="font-family: Times New Roman; color: black; text-align: left; font-size: 36px; margin-top: 10px;">
        Clinical Trials NER 
    </h1>
    """, unsafe_allow_html=True
)

# Input and Session Setup
selected_model, selected_entities = model_and_entity_selection(location=st.sidebar)
get_or_create_session_state_variable(key='selected_model', default_value=selected_model)
get_or_create_session_state_variable(key='selected_entities', default_value=selected_entities)
uploaded_file = upload_file(location=st.sidebar)
get_or_create_session_state_variable(key='uploaded_file', default_value=uploaded_file)
get_or_create_session_state_variable(key='ner_html', default_value=None)


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
        extracted_entities, results = extractNamedEntities(
            text=st.session_state['trialText'], 
            selected_model=st.session_state['selected_model'], 
            selected_entities=st.session_state['selected_entities']
        )
        st.session_state['extracted_entities'] = extracted_entities
        # # Visualize NER
        st.session_state['ner_html'] = visualize_ner(results)
        
                # Convert to Downloadable Document format
        df = ner_chunks_to_dataframe(ner_chunks=st.session_state['extracted_entities'])
        # Create Streamlit tabs dynamically
        st.session_state['categorizedEntities'] = categorize_entities(df=df)
        
    
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

    st.json(st.session_state['categorizedEntities'])
    if not df.empty:
        
        # CSV download
        with csvDownloadCol:
            csv_data = dataframe_to_csv(df)
            if csv_data:
                st.download_button(label="CSV ⤓", data=csv_data, file_name='ner_chunks.csv', mime='text/csv', use_container_width=True)
        # JSON download
        with jsonDownloadCol:
            json_data = dataframe_to_json(df)
            if csv_data:
                st.download_button(label="JSON ⤓", data=json_data, file_name='ner_chunks.json', mime='text/json', use_container_width=True)
        
        # PDF download
        with pdfDownloadCol:
            pdf_data = dataframe_to_pdf(df)
            if pdf_data:
                st.download_button(label="PDF ⤓", data=pdf_data, file_name='ner_chunks.pdf', mime='application/pdf', use_container_width=True)
        
    else:
        st.warning("No data available to display or download.")
