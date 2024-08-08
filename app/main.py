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

# Application
st.image('static/images/Trigent_Logo_full.png')
st.title("Clinical Trials NER Application")

# SideBar
uploaded_file = upload_file()
if uploaded_file:
    text = extract_text(uploaded_file)
    # Title and description
    # st.sidebar.image("https://path-to-john-snow-labs-logo.png", width=200)
    st.markdown('<p class="big-font">Detect Clinical Entities</p>', unsafe_allow_html=True)
    st.write("Choose the pretrained model to test")
    # Model selection
    model = st.selectbox("Choose Pretrainde Model",
        [
        'ner_jsl','ner_jsl_slim'
        'ner_jsl_enriched'
        'ner_jsl_greedy'
        ]
    )
    if text.strip():
        # Your text area widget
        st.text_area(label='Editor', value=text, height=int(len(text.strip())/2.3))
        generateButton = st.button('Generate', type='primary')
    else:
        st.info('Empty File!')
 