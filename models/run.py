from model_setup import setup_config, get_spark
from ner_pipeline import getNerPipeline

keys = setup_config()
spark = get_spark(secret=keys['SECRET'])
pipe = getNerPipeline(selectedModel='ner_jsl', 
                      selectedEntities=
                      ["Test", "Oncological", "Procedure", "Symptom", "Treatments", "Diabetes", "Drug", "Dosage",]
                    )
print(pipe)