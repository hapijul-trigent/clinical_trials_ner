import pandas as pd
import logging
from typing import List
from sparknlp.annotation import Annotation
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import streamlit as st
import random, json
from jsl_backend.entity_description_generation import get_description_refrences

def ner_chunks_to_dataframe(ner_chunks: List[Annotation]) -> pd.DataFrame:
    """
    Converts a list of NER chunk annotations into a Pandas DataFrame.
    
    Args:
        ner_chunks (List[Annotation]): A list of NER chunk annotations.
        
    Returns:
        pd.DataFrame: A DataFrame containing the NER chunk data.
        
    Example:
        ner_chunks = [
            Annotation(chunk, 17, 27, '40-year-old', {'chunk': '0', 'confidence': '0.999', 'ner_source': 'ner_chunk', 'entity': 'Age', 'sentence': '0'}, []),
            Annotation(chunk, 29, 33, 'white', {'chunk': '1', 'confidence': '0.9983', 'ner_source': 'ner_chunk', 'entity': 'Race_Ethnicity', 'sentence': '0'}, []),
            ...
        ]
        df = ner_chunks_to_dataframe(ner_chunks)
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info("Converting NER chunks to DataFrame")
        
        # Extract data from NER chunks
        data = []
        for chunk in ner_chunks:
            data.append({
                "chunk": chunk.result,
                "start": chunk.begin,
                "end": chunk.end,
                "confidence": float(chunk.metadata.get('confidence', 0.0)),
                "ner_source": chunk.metadata.get('ner_source', ''),
                "entity": chunk.metadata.get('entity', ''),
                "sentence": chunk.metadata.get('sentence', ''),
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        logger.info("Conversion successful. DataFrame created with %d records.", len(df))
        
        return df
    
    except Exception as e:
        logger.error("Failed to convert NER chunks to DataFrame: %s", str(e))
        return pd.DataFrame()  # Return an empty DataFrame on failure


def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    """
    Converts a DataFrame to CSV format.
    
    Args:
        df (pd.DataFrame): The DataFrame to convert.
    
    Returns:
        bytes: The CSV data in bytes.
    """
    logger = logging.getLogger(__name__)
    try:
        csv_data = df.to_csv(index=False).encode('utf-8')
        logger.info("DataFrame successfully converted to CSV format.")
        return csv_data
    except Exception as e:
        logger.error("Failed to convert DataFrame to CSV: %s", str(e))
        return b""


def dataframe_to_json(df: pd.DataFrame) -> bytes:
    """
    Converts a DataFrame to JSON format.
    
    Args:
        df (pd.DataFrame): The DataFrame to convert.
    
    Returns:
        bytes: The JSON data in bytes.
    """
    logger = logging.getLogger(__name__)
    try:
        json_data = df.to_json(orient='records').encode('utf-8')
        logger.info("DataFrame successfully converted to JSON format.")
        return json_data
    except Exception as e:
        logger.error("Failed to convert DataFrame to JSON: %s", str(e))
        return b""

def dataframe_to_pdf(df: pd.DataFrame) -> bytes:
    """
    Converts a DataFrame to PDF format.
    
    Args:
        df (pd.DataFrame): The DataFrame to convert.
    
    Returns:
        bytes: The PDF data in bytes.
    """
    logger = logging.getLogger(__name__)
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements = [table]
        doc.build(elements)
        buffer.seek(0)
        logger.info("DataFrame successfully converted to PDF format.")
        return buffer.getvalue()
    except Exception as e:
        logger.error("Failed to convert DataFrame to PDF: %s", str(e))
        return b""

def categorize_entities(df, chain):
    """
    Categorize entities from a DataFrame into a dictionary.

    Args:
    df (pandas.DataFrame): A DataFrame containing entity information with columns:
                           'entity', 'chunk', 'start', 'end', 'confidence', 'sentence'.

    Returns:
    dict: A dictionary where keys are entity types and values are lists of entity information.

    Raises:
    KeyError: If any required column is missing from the DataFrame.
    Exception: For any other unexpected errors during processing.
    """
    logging.info("Starting entity categorization")
    categorized = {}

    try:
        for _, row in df.iterrows():
            entity_type = row['entity']
            if entity_type not in categorized:
                categorized[entity_type] = []
                    
            # input_data = {"entity": row['chunk'], "type": row['entity'], 'context': 'Clinincal Trials'}
            # description, references = get_description_refrences(input_data, llm_chain=chain)
            
            entity_info = {
                'chunk': row['chunk'],
                'start': row['start'],
                'end': row['end'],
                'confidence': row['confidence'],
                'entity': row['entity'],
                'sentence': row['sentence'],
                'description': 'Clinical Entity Description',
                'references': 'references'
            }
            categorized[entity_type].append(entity_info)
            logging.debug(f"Processed entity: {entity_type}")

        logging.info(f"Categorization complete. Found {len(categorized)} entity types.")
        return categorized

    except KeyError as e:
        logging.error(f"Missing required column in DataFrame: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during categorization: {str(e)}")
        raise


def create_streamlit_buttons(categoryEntities: list, widget) -> None:
    """
    Create Streamlit buttons from a list of dictionaries.

    Args:
    categoryEntities (list): A list of dictionaries containing button information.
                 Each dictionary should have a "chunk" key with the button value.

    Returns:
    None
    """
    logger = logging.getLogger(__name__)
    try:
        # Create 3 columns (adjust this number to your liking)
        cols = st.columns(3)

        # Iterate over data and create buttons in columns
        for i, item in enumerate(categoryEntities):
            button_value = item["chunk"]
            button_key = f"{item['entity']}_{i}"
            with cols[i % 3]:  # Use the modulo operator to wrap around to the next column
                
                curr = st.button(str(button_value), key=button_key, use_container_width=True)
                if curr:
                    # Creating markdown to show the detailed information
                    with widget:
                        st.markdown(f"""
                                <div style="padding: 10px; background-color: #F5F9F4; border-radius: 5px;">
                                    <p><strong>Chunk:</strong> <code>{button_value}</code></p>
                                    <p><strong>Entity:</strong> <code>{item['entity']}</code></p>
                                    <p><strong>Description:</strong> <code>{item['description']}</code></p>
                                    <p><strong>References:</strong> <code>{item['references']}</code></p>
                                </div>
                                """, unsafe_allow_html=True)


    except Exception as e:
        logger.error(f"Error creating Streamlit buttons: {e}")


def get_or_create_session_state_variable(key, default_value=None):
    """
    Retrieves the value of a variable from Streamlit's session state.
    If the variable doesn't exist, it creates it with the provided default value.

    Args:
        key (str): The key of the variable in session state.
        default_value (Any): The default value to assign if the variable doesn't exist.

    Returns:
        Any: The value of the session state variable.
    """
    if key not in st.session_state:
        st.session_state[key] = default_value
    return st.session_state[key]
