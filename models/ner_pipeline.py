import logging
from pyspark.ml import Pipeline
from sparknlp.annotator import (
    DocumentAssembler, 
    SentenceDetectorDLModel, 
    Tokenizer, 
    WordEmbeddingsModel, 
    MedicalNerModel, 
    NerConverter
)
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.cache_resource
def getNerPipeline(selectedModel, selectedEntities):
    """
    Creates a Spark NLP pipeline for Named Entity Recognition (NER) with specified entity types.
    
    Parameters:
        selectedModel str: The Model Name from ['ner_jsl','ner_jsl_slim','ner_jsl_enriched', 'ner_jsl_greedy']
        selectedEntities (list of str): A list of entity types to recognize.
    
    Returns:
        Pipeline: A Spark ML pipeline configured for NER.
    """
    try:
        # Initialize the document assembler
        documentAssembler = DocumentAssembler().setInputCol("text").setOutputCol("document")

        # Load and set up the sentence detector
        sentenceDetector = SentenceDetectorDLModel.pretrained("sentence_detector_dl_healthcare","en","clinical/models") \
                .setInputCols(["document"]) \
                .setOutputCol("sentence") 

        # Initialize the tokenizer
        tokenizer = Tokenizer().setInputCols(["sentence"]).setOutputCol("token")

        # Load and set up the word embeddings
        embeddings = WordEmbeddingsModel.pretrained("embeddings_clinical", "en", "clinical/models")\
                .setInputCols(["sentence", "token"])\
                .setOutputCol("embeddings")

        # Load and set up the NER model
        ner_model = MedicalNerModel.pretrained(selectedModel, "en", "clinical/models")\
            .setInputCols(["sentence", "token", "embeddings"])\
                .setOutputCol("ner")

        # Initialize the NER converter
        ner_converter = NerConverter()\
            .setInputCols(["sentence", "token", "ner"])\
                .setOutputCol("ner_chunk")\
                    .setWhiteList(selectedEntities)

        # Create the pipeline
        pipeline = Pipeline(stages=[
                      documentAssembler,
                      sentenceDetector,
                      tokenizer,
                      embeddings,
                      ner_model,
                      ner_converter
                    ])
        
        logger.info("NER Pipeline created successfully.")
        return pipeline

    except Exception as e:
        logger.error(f"Error creating NER Pipeline: {e}")
        raise

