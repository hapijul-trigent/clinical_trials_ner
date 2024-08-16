import logging
from pyspark.ml import Pipeline
import streamlit as st

@st.cache_data(show_spinner=False)
def generate_medical_answer(entitty: str, pipeline: Pipeline) -> str:
    """
    Generate a medical description to a given Named Entity using a pre-trained GPT model.

    Args:
        entity (str): The medical Entity to description.

    Returns:
        str: The generated description.

    Raises:
        Exception: If there's an error during pipeline execution.
    """
    global spark
    logger = logging.getLogger(__name__)
    logger.info("Generating medical description...")
    try:
        data = spark.createDataFrame([[entitty]]).toDF("text")
        result = pipeline.fit(data).transform(data)
        description = result.select("description").collect()[0][0]
        logger.info("description generated successfully!")
        return description
    except Exception as e:
        logger.error("Error generating medical description:", exc_info=True)
        raise Exception("Error generating medical description") from e