from sparknlp.base import DocumentAssembler
from sparknlp.annotator import SentenceDetectorDLModel
from sparknlp_jsl.annotator import Tokenizer, WordEmbeddingsModel, NerConverterInternal


# Converts the input text into a format that the Spark NLP pipeline can process. 
# It creates a document column, which is the first required step in the NLP pipeline.

documentAssembler = DocumentAssembler()\
                .setInputCol("text")\
                .setOutputCol("document")

# Splits the document into sentences, which are easier to process individually
sentenceDetector = SentenceDetectorDLModel.pretrained("sentence_detector_dl_healthcare","en","clinical/models") \
                .setInputCols(["document"]) \
                .setOutputCol("sentence") 


# Breaks down the sentences into individual tokens (usually words), which are the basic units for processing in NLP.
tokenizer = Tokenizer()\
                .setInputCols(["sentence"])\
                .setOutputCol("token")


# Converts tokens into dense vectors (embeddings) that capture semantic meaning.
# These embeddings are necessary for the NER model to understand the context.
embeddings = WordEmbeddingsModel.pretrained("embeddings_clinical", "en", "clinical/models")\
                .setInputCols(["sentence", "token"])\
                .setOutputCol("embeddings")

# Converts the NER results into a readable format (chunks of text) by combining the tokens back into the original entities.
jsl_ner_converter = NerConverterInternal() \
                .setInputCols(["sentence", "token", "jsl_ner"]) \
                .setOutputCol("ner_chunk")


