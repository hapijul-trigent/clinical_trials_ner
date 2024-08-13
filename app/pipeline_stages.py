from sparknlp.base import DocumentAssembler
from sparknlp.annotator import SentenceDetectorDLModel
from sparknlp_jsl.annotator import Tokenizer, WordEmbeddingsModel, NerConverterInternal, MedicalTextGenerator
from model_setup import setup_config, initSparkSession
from pyspark.ml import Pipeline
import streamlit as st

# Init Spark
license_keys = setup_config()
spark = initSparkSession(secret=license_keys['SECRET'])

# Function to initialize SparkSession
@st.cache_resource(show_spinner=False)
def init_spark_session():
    license_keys = setup_config()
    return initSparkSession(secret=license_keys['SECRET'])

# Function to load Document Assembler
@st.cache_resource(show_spinner=False)
def load_document_assembler():
    return DocumentAssembler()\
                .setInputCol("text")\
                .setOutputCol("document")

# Function to load Sentence Detector
@st.cache_resource(show_spinner=False)
def load_sentence_detector():
    return SentenceDetectorDLModel.pretrained("sentence_detector_dl_healthcare","en","clinical/models") \
                .setInputCols(["document"]) \
                .setOutputCol("sentence")

# Function to load Tokenizer
@st.cache_resource(show_spinner=False)
def load_tokenizer():
    return Tokenizer()\
                .setInputCols(["sentence"])\
                .setOutputCol("token")

# Function to load Word Embeddings Model
@st.cache_resource(show_spinner=False)
def load_embeddings_model():
    return WordEmbeddingsModel.pretrained("embeddings_clinical", "en", "clinical/models")\
                .setInputCols(["sentence", "token"])\
                .setOutputCol("embeddings")

# Function to load NER Converter
@st.cache_resource(show_spinner=False)
def load_ner_converter():
    return NerConverterInternal() \
                .setInputCols(["sentence", "token", "ner"]) \
                .setOutputCol("ner_chunk")

# Initialize Spark
spark = init_spark_session()
# Load Components
documentAssembler = load_document_assembler()
sentenceDetector = load_sentence_detector()
tokenizer = load_tokenizer()
embeddings = load_embeddings_model()
jsl_ner_converter = load_ner_converter()



# document_assembler_enitity_description = DocumentAssembler() \
#     .setInputCol("text") \
#     .setOutputCol("documents")

# gpt_qa = MedicalTextGenerator.pretrained("biogpt_chat_jsl", "en", "clinical/models")\
#     .setInputCols("documents")\
#     .setOutputCol("description")

# pipeline_entity_description = Pipeline().setStages([document_assembler_enitity_description, gpt_qa])