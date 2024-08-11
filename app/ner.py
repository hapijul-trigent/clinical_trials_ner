import streamlit as st
from typing import Tuple
import logging
from app.pipeline_setup import buildNerPipeline
from pprint import pprint
from pipeline_setup import getEntityTypes


def model_and_entity_selection(location: st) -> Tuple:
    """Defines Model & Entity Selection"""
    # Models
    models = [
        'ner_jsl','ner_jsl_slim',
        'ner_jsl_enriched',
        'ner_jsl_greedy',
    ]
    # Model selection
    selected_model = location.selectbox("Choose the pretrained model", options=models, index=0)
    
    # Entitties
    EntityTypes = getEntityTypes(nerModelType=selected_model)
    selected_entities = location.multiselect('Detect Clinical Entities', options=EntityTypes, default=EntityTypes[:5])
    return selected_model, selected_entities


def extractNamedEntities(text, selected_model, selected_entities):
    """
    Extract named entities from the provided text using a specified NLP model and entities.

    Args:
        text (str): The input text to extract entities from.
        selected_model (str): The name of the model to use for entity extraction.
        selected_entities (list): A list of entities to extract.

    Returns:
        list: A list of dictionaries containing the extracted entities and their corresponding information.
        results: output of fullAnnote
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f'{selected_model}: {selected_entities}')
        
        # Build the NLP pipeline using the selected model and entities
        light_model_pipeline = buildNerPipeline(selectedModel=selected_model, selectedEntities=selected_entities)
        
        # Run the pipeline on the provided text
        results = light_model_pipeline.fullAnnotate(text)
        logger.info(f'Extracted named entities successfully!')
        return results[0]['ner_chunk'], results[0]

    except Exception as e:
        logger.error(f"An error occurred while extracting named entities: {str(e)}")
        return [], None