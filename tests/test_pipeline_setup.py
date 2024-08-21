import pytest
from jsl_backend.pipeline_setup import buildNerPipeline, getEntityTypes

def test_build_ner_pipeline():
    pipeline = buildNerPipeline(selectedModel='ner_jsl')

    assert pipeline is not None
    assert hasattr(pipeline, 'fullAnnotate')

def test_get_entity_types():
    entity_types = getEntityTypes(nerModelType='ner_jsl')

    assert isinstance(entity_types, list)
    assert len(entity_types) > 0
    assert all(isinstance(entity, str) for entity in entity_types)
