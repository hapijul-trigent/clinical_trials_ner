import pytest
from models.model_setup import load_ner_model

def test_load_ner_model():
    pipeline = load_ner_model()
    assert pipeline is not None
    assert hasattr(pipeline, 'fullAnnotate')
    assert hasattr(pipeline, 'stages')
    print('Test Case Passed!')