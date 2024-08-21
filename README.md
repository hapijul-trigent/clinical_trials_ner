# clinical_trials_ner
Streamlit application that utilizes John Snow Labs NLP models to perform Named Entity Recognition on clinical trials texts
# Navigate
```
clinical_trials_ner/
│
├── README.md                         # Project overview and setup instructions
├── requirements.txt                  # Required Python packages
├── setup.sh                          # Setup script for environment configuration
│
├── app/                              # Main application code
│   ├── __init__.py                   # Package initializer
│   ├── clinical_ner_app_with_session_states.py # Main Streamlit app with session state management
│   ├── data_processing.py            # File handling and text extraction functions
│   ├── utils.py                      # Utility functions for data processing and visualization
│   ├── .streamlit/
│   │   └── config.toml               # Streamlit configuration file
│   └── clinical_NER_app.py           # Main Streamlit app (this file was missing)
│
├── jsl_backend/                      # Backend processing modules
│   ├── __init__.py                   # Package initializer
│   ├── ner.py                        # NER model integration and entity extraction
│   ├── ner_display.py                # NER results visualization
│   ├── pipeline_setup.py             # Setup for NLP pipeline
│   ├── pipeline_stages.py            # Stages of the NLP pipeline
│   ├── entity_description_generation.py # Generate entity descriptions using LLM
│   ├── entityDescCache.py            # Cache for entity descriptions
│   ├── fonts/
│   │   └── Lucida_Console.ttf        # Font used for visualization
│   ├── label_colors/
│   │   ├── ner.json                  # Colors for NER labels
│   │   └── relations.json            # Colors for relation labels
│   ├── models/
│   │   └── sentence_detector_dl_en.zip # Pre-trained model for sentence detection
│   └── style.css                     # Stylesheet for visualizations
│
├── static/                           # Static resources (images, CSS)
│   └── images/
│       ├── Trigent_Logo.png          # Trigent logo used in the app
│       └── Trigent_Logo_full.png     # Full version of the Trigent logo
│
├── tests/                            # Unit tests for the project
│   ├── __init__.py                   # Package initializer
│   ├── test_data_processing.py       # Tests for data processing functions
│   ├── test_ner.py                   # Tests for NER model integration
│   └── test_visualization.py         # Tests for visualization functions
│
└── hadop_spark_setup.sh              # Script for setting up Hadoop and Spark

```
# Environment Setup
```
$ bash setup.sh
```
