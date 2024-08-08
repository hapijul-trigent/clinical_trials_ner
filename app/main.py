import streamlit as st
from data_processing import upload_file, extract_text
from utils import model_and_entity_selection
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

# Application
# SideBar
st.sidebar.image("static/images/Trigent_Logo.png")
st.sidebar.title('Trigent Clinical NER')
model_and_entity_selection(location=st.sidebar)
uploaded_file = upload_file(location=st.sidebar)

# Body
st.image('static/images/Trigent_Logo_full.png')
st.title("Clinical Trials NER Application")
if uploaded_file:
    text = extract_text(uploaded_file)
    if text.strip():
        # Your text area widget
        st.text_area(label='Editor', value=text, height=200)
        generateButton = st.button('Generate', type='primary')
    else:
        st.info('Empty File!')
 