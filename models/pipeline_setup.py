import logging
from pyspark.ml import Pipeline
from sparknlp_jsl.annotator import MedicalNerModel
import streamlit as st
from pipeline_stages import (
    documentAssembler,
    sentenceDetector,
    tokenizer,
    embeddings,
    jsl_ner_converter
) 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# @st.cache_resource
def buildNerPipeline(selectedModel, selectedEntities):
    """
    Creates a Spark NLP pipeline for Named Entity Recognition (NER) with specified entity types.
    
    Parameters:
        selectedModel str: The Model Name from ['ner_jsl','ner_jsl_slim','ner_jsl_enriched', 'ner_jsl_greedy']
        selectedEntities (list of str): A list of entity types to recognize.
    
    Returns:
        Pipeline: A Spark ML pipeline configured for NER.
    """
    try:
        # Load and set up the NER model
        ner_model = MedicalNerModel.pretrained(selectedModel, "en", "clinical/models")\
            .setInputCols(["sentence", "token", "embeddings"])\
                .setOutputCol("ner")

        # Create the pipeline
        pipeline = Pipeline(
            stages=[
                documentAssembler,
                sentenceDetector,
                tokenizer,
                embeddings,
                ner_model,
                jsl_ner_converter
            ]
        )
        
        logger.info("NER Pipeline created successfully.")
        return pipeline

    except Exception as e:
        logger.error(f"Error creating NER Pipeline: {e}")
        raise

from model_setup import setup_config, initSparkSession
license_keys = setup_config()
spark = initSparkSession(secret=license_keys['SECRET'])
pipe = buildNerPipeline(selectedModel='ner_jsl', selectedEntities=["Procedure", "Symptom", "Treatments", "Diabetes", "Drug", "Dosage",])
pipe