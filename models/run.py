from model_setup import setup_config, get_spark
# from ner_pipeline import getNerPipeline
import sparknlp
import sparknlp_jsl

from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp_jsl.annotator import *

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml import Pipeline,PipelineModel
from pyspark.sql.types import StringType, IntegerType

import pandas as pd
pd.set_option('display.max_colwidth', 200)

import warnings
warnings.filterwarnings('ignore')
keys = setup_config()
# spark = get_spark(secret=keys['SECRET'])
# pipe = getNerPipeline(selectedModel='ner_jsl', 
#                       selectedEntities=
#                       ["Test", "Oncological", "Procedure", "Symptom", "Treatments", "Diabetes", "Drug", "Dosage",]
#                     )
# print(pipe)
from sparknlp.pretrained import PretrainedPipeline
import sparknlp

# Start a Spark NLP session
spark = sparknlp.start()

# Load a pretrained medical NER pipeline
pipeline = PretrainedPipeline('ner_jsl', 'en', 'clinical/models')

# Sample text
text = "The patient was diagnosed with diabetes and prescribed metformin."

# Annotate the text
annotations = pipeline.fullAnnotate(text)

# Print annotations
for annotation in annotations[0]['ner_chunk']:
    print(f"Entity: {annotation.result}, Type: {annotation.metadata['entity']}")
