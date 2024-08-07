import streamlit as st
from data_processing import upload_file, extract_text
from PIL import Image

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

#
st.image('static/images/Trigent_Logo_full.png')
st.title("Clinical Trials NER Application")
uploaded_file = upload_file()
if uploaded_file:
    text = extract_text(uploaded_file)
 