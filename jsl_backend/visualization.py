from jsl_backend.ner_display import NerVisualizer
import logging


def visualize_ner(light_result, selected_labels):
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
        html = visualizer.display(light_result, label_col='ner_chunk', document_col='document', return_html=True, labels=selected_labels)
        logger.info(f"NER visualization rendered successfully!")
        return html
    except Exception as e:
        st.error("An error occurred while visualizing NER results.")
        logger.error(f"Error in visualize_ner: {e}")

