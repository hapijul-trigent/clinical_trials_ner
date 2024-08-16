from jsl_backend.ner_display import NerVisualizer
import logging, random
import pandas as pd
import json, os
import streamlit as st

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


def create_multiindex_dataframe_of_groupedEntity(df):
    """
    Create a new DataFrame with a MultiIndex based on entity groups and chunks.

    This function takes a DataFrame containing 'entity', 'chunk', 'start', 'end', and 'confidence' columns.
    It creates a new DataFrame with a MultiIndex based on unique entity groups and their corresponding chunks.

    Args:
        df (pd.DataFrame): Input DataFrame containing the required columns.

    Returns:
        pd.DataFrame: A new DataFrame with MultiIndex and 'start', 'end', 'confidence' columns.

    Raises:
        KeyError: If the required columns are missing from the input DataFrame.
        ValueError: If the input DataFrame is empty.
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    try:
        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("Input DataFrame is empty")

        # Check for required columns
        required_columns = ['entity', 'chunk', 'start', 'end', 'confidence']
        if not all(col in df.columns for col in required_columns):
            raise KeyError(f"Input DataFrame is missing one or more required columns: {required_columns}")

        logger.info("Creating entity groups and chunks")
        entityGroups = df.entity.unique()
        entityGroupChunks = [df[df.entity==entity]['chunk'].values for entity in entityGroups]

        logger.info("Creating MultiIndex")
        index = pd.MultiIndex.from_tuples(
            [(l1, l2) for l1, l2_list in zip(entityGroups, entityGroupChunks) for l2 in l2_list], 
            names=['entityType', 'entityChunk']
        )

        logger.info("Generating data for new DataFrame")
        data = df[['start', 'end', 'confidence', 'entity']].values

        logger.info("Creating new DataFrame with MultiIndex")
        ndf = pd.DataFrame(data, index=index, columns=['start', 'end', 'confidence', 'entity'])

        logger.info("MultiIndex DataFrame created successfully")
        return ndf

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
    

@st.cache_data
def load_colors():
    here = os.path.abspath(os.path.dirname(__file__))
    return json.load(open(os.path.join(here, 'label_colors/ner.json'), 'r', encoding='utf-8'))


def get_label_color(row):
        """Internal function to generate random color codes for missing colors
        
        Input: dictionary of entity labels and corresponding colors
        Output: color code (Hex)
        """
        import json
        label = row['entity']
        label_colors = load_colors()
        if str(label).lower() in label_colors:
            return ['background-color: {}'.format(label_colors[label.lower()])] * len(row) # Return a list of color values for each cell in the row
        else:
            #update it to fetch from git new labels 
            r = lambda: random.randint(0,200)
            color = '#%02X%02X%02X' % (r(), r(), r())
            return ['background-color: {}'.format(color)] * len(row) # Return a list of color values for each cell in the row


