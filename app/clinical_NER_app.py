import logging
import sys, os

sys.path.append('/workspaces/clinical_trials_ner')
sys.path.append('/workspaces/clinical_trials_ner/app')
sys.path.append('/workspaces/clinical_trials_ner/models')

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
from utils import ner_chunks_to_dataframe, dataframe_to_pdf, dataframe_to_csv

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
st.sidebar.title('Trigent Clinical NER')
selected_model, selected_entities = model_and_entity_selection(location=st.sidebar)
# FIle Uploader
uploaded_file = upload_file(location=st.sidebar)

# Body
st.image('static/images/Trigent_Logo_full.png')
st.title("Clinical Trials NER Application")
generateButton = None
st.sidebar.divider()
sessionExit = st.sidebar.button(label='Stop Session', type='primary')
if uploaded_file:
    # Process File
    text = extract_text(uploaded_file)
    if text.strip():
        # Your text area widget
        st.text_area(label='Editor', value=text, height=200)
        generateButton = st.button(label='Extract Entities', type='primary')
    else:
        st.info('Empty File!')
if generateButton and text:
    # build pipeline
    extracted_entities, results = extractNamedEntities(
        text=text, 
        selected_model=selected_model, 
        selected_entities=selected_entities
    )
    
    # # Visualize NER
    html = visualize_ner(results)
    
    # # Display the output in Streamlit
    st.title('Recognize Entities')
    st.markdown(
    f'<div class="scroll entities" style="overflow-x: auto;border: 1px solid rgb(230, 233, 239);border-radius: 0.25rem;padding: 1rem;margin-bottom: 2.5rem;white-space: pre-wrap;">{html}</div>'
    , unsafe_allow_html=True)

    # Convert to Downloadable Document format
    df = ner_chunks_to_dataframe(ner_chunks=extracted_entities)
    
    if not df.empty:
        st.write(df)
        
        # CSV download
        csv_data = dataframe_to_csv(df)
        if csv_data:
            st.download_button(label="Download as CSV", data=csv_data, file_name='ner_chunks.csv', mime='text/csv')
        
        # PDF download
        pdf_data = dataframe_to_pdf(df)
        if pdf_data:
            st.download_button(label="Download as PDF", data=pdf_data, file_name='ner_chunks.pdf', mime='application/pdf')
    else:
        st.warning("No data available to display or download.")
if sessionExit:
    spark.stop()
    st.success('Session Terminated')
    st.stop()