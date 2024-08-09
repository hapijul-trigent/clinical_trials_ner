import streamlit as st
from typing import Tuple

def model_and_entity_selection(location: st) -> Tuple:
    """Defines Model & Entity Selection"""
    # Models
    models = [
        'ner_jsl','ner_jsl_slim',
        'ner_jsl_enriched',
        'ner_jsl_greedy',
    ]
    
    # Entitties
    entities = [
        "Test", "Oncological", "Procedure", "Symptom", "Treatments", "Diabetes", "Drug", "Dosage", "Date",
        "Imagine_Finding", "Anatomical_Site", "Behavioral_Observation", "Biological_Process", "Blood_Pressure",
        "Body_Measurement", "Cancer", "Cardiovascular_Disease", "Cell", "Chemotherapy_Regimen", "Clinical_Procedure",
        "Cognitive_Observation", "Comorbidity", "Complication", "Condition", "Congenital_Disorder", "Dermatological",
        "Diagnosis", "Diet", "Disability", "Disease", "Disease_Symptom", "Drug_Administration_Route", "Drug_Brand_Name",
        "Drug_Class", "Drug_Compound", "Drug_Dosage_Form", "Drug_Indication", "Drug_Interaction", "Drug_Metabolism",
        "Drug_Overdose", "Drug_Precaution", "Drug_Side_Effect", "Drug_Trade_Name", "Endocrine_Disorder",
        "Environmental_Exposure", "Family_History", "Genetic_Disorder", "Genetic_Variation", "Health_Indicator",
        "Hematological_Disorder", "Immunological_Disorder", "Infectious_Disease", "Inflammatory_Disorder",
        "Laboratory_Finding", "Laboratory_Test", "Lipid_Disorder", "Medical_Device", "Medical_Encounter",
        "Medical_History", "Mental_Disorder", "Metabolic_Disorder", "Microbiological_Finding", "Musculoskeletal_Disorder",
        "Neonatal_Disorder", "Neurological_Disorder", "Nutritional_Observation", "Oncological_Procedure", "Organism",
        "Pain", "Physical_Activity", "Physical_Exam_Finding", "Physical_Measurement", "Psychiatric_Disorder",
        "Pulmonary_Disorder", "Renal_Disorder", "Respiratory_Disorder", "Social_History", "Substance_Abuse", "Surgical_Procedure"
    ]

    
    # Model selection
    selected_model = location.selectbox("Choose the pretrained model", options=models, index=0)
    selected_entities = location.multiselect('Detect Clinical Entities', options=entities, default=["Treatments", "Diabetes", "Drug", "Dosage",])

    return selected_model, selected_entities

