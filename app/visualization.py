import streamlit as st
from sparknlp_display import NerVisualizer
import logging


def visualize_ner(light_result):
    """
    Visualize Named Entity Recognition (NER) results using the NerVisualizer.

    Parameters:
    light_result (list): A list containing the NER results from a Spark NLP pipeline.

    Returns:
    HTML: HTML to displays the NER visualization in the Streamlit app.
    """
    logger = logging.getLogger(__name__)
    try:
        visualizer = NerVisualizer()
        html = visualizer.display(light_result, label_col='ner_chunk', document_col='document', return_html=True)
        logger.info(f"NER visualization rendered successfully: {html}")
        return html
    except Exception as e:
        st.error("An error occurred while visualizing NER results.")
        logger.error(f"Error in visualize_ner: {e}")

