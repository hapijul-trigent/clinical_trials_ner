# Clinical Trials Named Entity Recognition (NER)

**Clinical Trials NER** is a Streamlit-based application that leverages John Snow Labs NLP models to perform Named Entity Recognition (NER) on clinical trial texts. This project is designed to extract and visualize critical entities such as diseases, drugs, population demographics, and trial design elements from clinical trial abstracts.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **NER Model Integration:** Utilizes pre-trained NER models from John Snow Labs to extract entities from clinical trial texts.
- **Streamlit Interface:** User-friendly web application built with Streamlit, allowing easy file uploads, entity selection, and results visualization.
- **Multi-format Output:** Export extracted entities to CSV, JSON, and PDF formats.
- **Advanced Visualization:** Visualize NER results directly in the browser with dynamic, color-coded entity displays.
- **Clinical Entity Description and Reference generation:** Utilizes ChatGroq[Mixtral7b] for generation.
- **Session Management:** Maintains session state across different user interactions to enhance the user experience.

## Installation

### Prerequisites

- Python 3.7 or later
- [pip](https://pip.pypa.io/en/stable/) for package management

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/hapijul-trigent/clinical_trials_ner.git
   cd clinical_trials_ner
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the environment:**

   Run the setup script to configure the necessary environment:

   ```bash
   bash setup.sh
   ```

## Usage

1. **Launch the Streamlit app:**

   ```bash
   streamlit run app/clinical_ner_app_with_session_states.py
   ```

2. **Upload a clinical trial document:**

   The application supports PDF, DOCX, and TXT file formats.

3. **Select NER Model and Entities:**

   Choose from various pre-trained NER models and specify the entities you wish to extract.

4. **Visualize and Export Results:**

   View the extracted entities in the browser and export the results to CSV, JSON, or PDF.

## Project Structure

```
clinical_trials_ner/
│
├── app/                            # Main application code
├── jsl_backend/                    # Backend processing modules
├── static/                         # Static resources (images, CSS)
├── tests/                          # Unit tests for the project
├── README.md                       # Project overview and setup instructions
├── requirements.txt                # Required Python packages
└── setup.sh                        # Setup script for environment configuration
```

## Technologies Used

- **Python:** The core language for application logic.
- **Streamlit:** Framework for building the web application.
- **John Snow Labs NLP:** Pre-trained models for Named Entity Recognition (NER).
- **PySpark:** Used for NLP pipeline setup.
- **LangChain, Langchain-Groq:** For generating entity descriptions.

## Contributing

We welcome contributions! If you have suggestions for improvements or have found bugs, please feel free to submit a pull request or create an issue in the repository.

### Steps to Contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit and push your changes (`git push origin feature-branch`).
5. Submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please contact the project maintainers at [hapijul_h@trigent.com](mailto:hapijul_h@trigent.com).
