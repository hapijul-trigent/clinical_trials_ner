import logging
import sys, os

sys.path.append('/workspaces/clinical_trials_ner')
sys.path.append('/workspaces/clinical_trials_ner/app')
sys.path.append('/workspaces/clinical_trials_ner/models')

import streamlit as st
from data_processing import upload_file, extract_text
from ner import model_and_entity_selection
from models.model_setup import setup_config, initSparkSession
from models.pipeline_stages import spark, license_keys
from models.pipeline_setup import buildNerPipeline
from visualization import visualize_ner
from PIL import Image


# Configure logging
logging.basicConfig(level=logging.INFO)
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
uploaded_file = upload_file(location=st.sidebar)

# Body
st.image('static/images/Trigent_Logo_full.png')
st.title("Clinical Trials NER Application")
generateButton = None
if uploaded_file:
    text = extract_text(uploaded_file)
    if text.strip():
        # Your text area widget
        st.text_area(label='Editor', value=text, height=200)
        generateButton = st.button('Extract Entities', type='primary')
    else:
        st.info('Empty File!')
if generateButton and text:
    logger.info(f'{selected_model}: {selected_entities}')
    light_model_pipeline = buildNerPipeline(selectedModel=selected_model, selectedEntities=selected_entities)
    results = light_model_pipeline.fullAnnotate(text)

    # Visualize NER
    html = visualize_ner(results)
    st.title('Recognize Entities')
    st.write(html, unsafe_allow_html=True)


 