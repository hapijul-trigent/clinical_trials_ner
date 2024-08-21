import pytest
from jsl_backend.ner import model_and_entity_selection, extractNamedEntities
import streamlit as st
from unittest.mock import MagicMock

def test_model_and_entity_selection():
    st.selectbox = MagicMock(return_value='ner_jsl')
    st.multiselect = MagicMock(return_value=['Gender', 'Drug'])

    selected_model, selected_entities, light_model_pipeline, modelColumn, editorColumns = model_and_entity_selection(st)

    assert selected_model == 'ner_jsl'
    assert selected_entities == ['Gender', 'Drug']
    assert light_model_pipeline is not None
    assert modelColumn is not None
    assert editorColumns is not None

def test_extract_named_entities():
    mock_pipeline = MagicMock()
    mock_pipeline.fullAnnotate = MagicMock(return_value=[{'ner_chunk': [], 'text': 'example text'}])
    selected_model, selected_entities, light_model_pipeline, modelColumn, editorColumns = model_and_entity_selection(st)
    entities, results = extractNamedEntities("Aspirin drug use daily", "ner_jsl", ['Drug',], light_model_pipeline=light_model_pipeline)
    
    
    assert isinstance(entities, list)
    assert isinstance(results, dict)

    assert 'ner_chunk' in results
