import logging
from pyspark.ml import Pipeline
from sparknlp_jsl.annotator import MedicalNerModel
from sparknlp.base import LightPipeline
from pyspark.sql import SparkSession
import streamlit as st

from pipeline_stages import (
    documentAssembler,
    sentenceDetector,
    tokenizer,
    embeddings,
    jsl_ner_converter,
    spark
) 


@st.cache_resource
def buildNerPipeline(selectedModel, selectedEntities, spark: SparkSession = spark):
    """
    Creates a Spark NLP pipeline for Named Entity Recognition (NER) with specified entity types.
    
    Parameters:
        selectedModel str: The Model Name from ['ner_jsl','ner_jsl_slim','ner_jsl_enriched', 'ner_jsl_greedy']
        selectedEntities (list of str): A list of entity types to recognize.
        spark: SparkSession
    
    Returns:
        light_model_pipeline: A Spark ML pipeline configured for NER.
    """
    logger = logging.getLogger(__name__)
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
        
        # Build LightPipeline
        light_model_pipeline = LightPipeline(
            pipelineModel=pipeline.fit(spark.createDataFrame([['']]).toDF("text"))
        )
        logger.info("NER Pipeline created successfully.")
        return light_model_pipeline

    except Exception as e:
        logger.error(f"Error creating NER Pipeline: {e}")
        raise


def getEntityTypes(nerModelType: str):
    """
    Load a specified NER model and return a list of unique entity types.

    Args:
        nerModelType (str): The path or identifier for the NER model.

    Returns:
        list: A list of unique entity types used by the model.

    Raises:
        Exception: If there is an issue loading the model or extracting the classes.
    """
    logger = logging.getLogger(__name__)
    try:
        # Load the NER model
        logger.info(f"Loading NER model from {nerModelType}")
        ner_model = MedicalNerModel.pretrained(nerModelType, "en", "clinical/models") \
                .setInputCols(["sentence", "token", "embeddings"]) \
                    .setOutputCol("jsl_ner")
        
        # Extract and return the unique entity types
        entity_types = list(set([str(x)[2:] for x in ner_model.getClasses() if len(x) > 1]))
        logger.info(f"Successfully extracted {len(entity_types)} entity types.")
        return entity_types
    
    except Exception as e:
        logger.error(f"An error occurred while loading the NER model or extracting entity types: {e}")
        raise




# from model_setup import setup_config, initSparkSession
# # license_keys = setup_config()
# # spark = initSparkSession(secret=license_keys['SECRET'])
# pipe = buildNerPipeline(selectedModel='ner_jsl', selectedEntities=["Procedure", "Symptom", "Treatments", "Diabetes", "Drug", "Dosage",])
# print(pipe)
# spark.sparkContext.stop()