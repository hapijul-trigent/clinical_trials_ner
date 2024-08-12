# clinical_trials_ner
Streamlit application that utilizes John Snow Labs NLP models to perform Named Entity Recognition on clinical trials texts
# Navigate
```
clinical_trials_ner/
│
├── app/
│   ├── __init__.py
│   ├── main.py                # Streamlit app entry point
│   ├── data_processing.py     # Module for handling data input and preprocessing
│   ├── ner.py                 # Module for NER model integration and entity extraction
│   ├── visualization.py       # Module for entity visualization
│   ├── utils.py               # Utility functions
│   ├── model_setup.py         # Module to setup and load John Snow Labs NER models
|   ├── pipeline_setup.py      # Module to setup pipeline stages
|   ├── pipeline_stages.py     # Module to setup model pipeline
|
├── models/                    # John Snow Labs NER models
│   ├── sentence_detector_dl_en.zip
│   ├── 
|   ├── 
|   ├── 
│
├── tests/
│   ├── __init__.py
│   ├── test_data_processing.py # Tests for data input and preprocessing
│   ├── test_ner.py             # Tests for NER model integration and entity extraction
│   ├── test_visualization.py   # Tests for entity visualization
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── requirements.txt           # Required Python packages
├── README.md                  # Project overview and setup instructions
└── .gitignore                 # Git ignore file
```
# Environment Setup
```
$ bash setup.sh
```