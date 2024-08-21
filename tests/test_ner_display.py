import pytest
from jsl_backend.ner_display import NerVisualizer
import json
from jsl_backend.ner import model_and_entity_selection, extractNamedEntities
import streamlit as st
from unittest.mock import MagicMock

def test_display_ner():
    visualizer = NerVisualizer()
    st.selectbox = MagicMock(return_value='ner_jsl')
    st.multiselect = MagicMock(return_value=['Gender', 'Drug'])
    text = "A 45-year-old male patient was diagnosed with type 2 diabetes and prescribed Metformin."
    selected_model, selected_entities, light_model_pipeline, _, _ = model_and_entity_selection(st)
    _, results = extractNamedEntities(text, selected_model=selected_model, selected_entities=selected_entities, light_model_pipeline=light_model_pipeline)
    html_output = visualizer.display(results, label_col='ner_chunk', document_col='document', return_html=True, labels=selected_entities)
    
    assert isinstance(html_output, str)
    assert '<span class="spark-nlp-display-entity-name" >' in html_output
