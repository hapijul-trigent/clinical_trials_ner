import pytest
from jsl_backend.pipeline_stages import (
    load_document_assembler,
    load_sentence_detector,
    load_tokenizer,
    load_embeddings_model,
    load_ner_converter
)

def test_load_document_assembler():
    document_assembler = load_document_assembler()
    
    assert document_assembler is not None
    assert document_assembler.getOutputCol() == "document"

def test_load_sentence_detector():
    sentence_detector = load_sentence_detector()
    
    assert sentence_detector is not None
    assert sentence_detector.getOutputCol() == "sentence"

def test_load_tokenizer():
    tokenizer = load_tokenizer()
    
    assert tokenizer is not None
    assert tokenizer.getOutputCol() == "token"

def test_load_embeddings_model():
    embeddings_model = load_embeddings_model()
    
    assert embeddings_model is not None
    assert embeddings_model.getOutputCol() == "embeddings"

def test_load_ner_converter():
    ner_converter = load_ner_converter()
    
    assert ner_converter is not None
    assert ner_converter.getOutputCol() == "ner_chunk"
