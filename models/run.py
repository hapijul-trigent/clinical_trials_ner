import os 
import json

with open('.secret/spark_nlp_for_healthcare_8568.json') as f:
    license_keys = json.load(f)

# Defining license key-value pairs as local variables
locals().update(license_keys)
os.environ.update(license_keys)



# ------------------------------------------
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

params = {"spark.driver.memory":"10G", 
          "spark.kryoserializer.buffer.max":"2000M", 
          "spark.driver.maxResultSize":"2000M"} 

spark = sparknlp_jsl.start(license_keys['SECRET'],params=params)

print("Spark NLP Version :", sparknlp.version())
print("Spark NLP_JSL Version :", sparknlp_jsl.version())

print(spark)

#-------------------------------------
sample_text = """The patient is a 40-year-old white male who presents with a chief complaint of "chest pain". The patient is diabetic and has a prior history of coronary artery disease. The patient presents today stating that his chest pain started yesterday evening and has been somewhat intermittent. He has been advised Aspirin 81 milligrams QDay, insulin 50 units in a.m. HCTZ 50 mg QDay. Nitroglycerin 1/150 sublingually PRN chest pain."""



# ---------------------------------------------
jsl_model_list = ["ner_jsl",]


documentAssembler = DocumentAssembler()\
                .setInputCol("text")\
                .setOutputCol("document")

sentenceDetector = SentenceDetectorDLModel.pretrained("sentence_detector_dl_healthcare","en","clinical/models") \
                .setInputCols(["document"]) \
                .setOutputCol("sentence") 

tokenizer = Tokenizer()\
                .setInputCols(["sentence"])\
                .setOutputCol("token")

jsl_ner_converter = NerConverterInternal() \
                .setInputCols(["sentence", "token", "jsl_ner"]) \
                .setOutputCol("ner_chunk")

embeddings = WordEmbeddingsModel.pretrained("embeddings_clinical", "en", "clinical/models")\
                .setInputCols(["sentence", "token"])\
                .setOutputCol("embeddings")
  
for model_name in jsl_model_list:

  jsl_ner = MedicalNerModel.pretrained(model_name, "en", "clinical/models") \
                          .setInputCols(["sentence", "token", "embeddings"]) \
                          .setOutputCol("jsl_ner")


  jsl_ner_pipeline = Pipeline(stages=[documentAssembler, 
                                      sentenceDetector,
                                      tokenizer,
                                      embeddings,
                                      jsl_ner,
                                      jsl_ner_converter])


  jsl_ner_model = jsl_ner_pipeline.fit(spark.createDataFrame([['']]).toDF("text"))
  
  light_model = LightPipeline(jsl_ner_model)
  light_result = light_model.fullAnnotate(sample_text)

  print("\n\n\n")
  print(f"***************  The visualization results for {model_name} ***************")
  print("\n\n\n")

  from sparknlp_display import NerVisualizer
  visualiser = NerVisualizer()
  visualiser.display(light_result[0], label_col='ner_chunk', document_col='document')
  print("\n\n\n")