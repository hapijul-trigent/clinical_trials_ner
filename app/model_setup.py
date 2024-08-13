import json
import os
import logging

import sparknlp
import sparknlp_jsl
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml import Pipeline, PipelineModel
from pyspark.sql.types import StringType, IntegerType

from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp_jsl.annotator import *

import streamlit as st



@st.cache_resource(show_spinner=False)
def setup_config(config_path='.secret/spark_nlp_for_healthcare_8568.json'):
    """
    Loads Spark NLP for Healthcare license keys from a JSON file and sets them as environment variables.

    Args:
        config_path (str): Path to the JSON file containing the license keys. Defaults to '.secret/spark_nlp_for_healthcare_8568.json'.

    Returns:
        dict: A dictionary containing the license keys.

    Raises:
        FileNotFoundError: If the JSON file is not found.
        json.JSONDecodeError: If the JSON file cannot be decoded.
    """
    logger = logging.getLogger(__name__)
    try:
        with open(config_path) as f:
            license_keys = json.load(f)
        locals().update(license_keys)
        os.environ.update(license_keys)
        return license_keys
    except FileNotFoundError as e:
        logger.error("Error: The file was not found. %s", e)
        raise
    except json.JSONDecodeError as e:
        logger.error("Error: Failed to decode JSON. %s", e)
        raise

@st.cache_resource(show_spinner=False)
def initSparkSession(secret):
    """
    Initialize and return a Spark NLP session with specified configurations.

    Args:
        secret (str): The secret key for initializing Spark NLP JSL.

    Returns:
        SparkSession: An initialized Spark session with specified configurations.

    Raises:
        ValueError: If the secret is None or an empty string.
        Exception: For any other exceptions that occur during the initialization.
    """
    if not secret:
        raise ValueError("The secret key must be provided and cannot be empty.")

    params = {
        "spark.driver.memory": "4G",
        "spark.kryoserializer.buffer.max": "2000M",
        "spark.driver.maxResultSize": "2000M"
    }
    logger = logging.getLogger(__name__)
    try:
        spark = sparknlp_jsl.start(secret, params=params)
        logger.info("Spark NLP Version: %s", sparknlp.version())
        logger.info("Spark NLP_JSL Version: %s", sparknlp_jsl.version())
        return spark
    except Exception as e:
        logger.error("An error occurred while initializing Spark: %s", str(e))
        raise

# keys = setup_config()
# spark = initSparkSession(secret=keys['SECRET'])
# spark.stop()