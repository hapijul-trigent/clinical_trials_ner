import sparknlp
from sparknlp.pretrained import PretrainedPipeline
from johnsnowlabs import nlp
nlp.start()
medical_text = ''' The patient is a 5-month-old infant who presented initially on Monday with
a cold, cough, and runny nose for 2 days'''
resp = nlp.load('med_ner.jsl.wip.clinical').predict(medical_text)
print(resp)

# def load_ner_model():
#     """
#     Load a pre-trained Named Entity Recognition (NER) model for clinical text.

#     This function initializes the Spark NLP library and loads the 
#     'ner_clinical' pre-trained pipeline, which is designed to identify 
#     named entities in clinical texts.

#     Returns:
#         PretrainedPipeline: A Spark NLP pipeline object that can be used 
#         for processing clinical text and extracting named entities.
#     """
#     sparknlp.start()
#     pipeline = PretrainedPipeline("ner_clinical", "en", "clinical/models")
#     return pipeline

# pipe = load_ner_model()
# print(pipe)