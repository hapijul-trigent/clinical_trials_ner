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
│
├── models/
│   ├── __init__.py
│   ├── model_setup.py         # Module to setup and load John Snow Labs NER models
|   ├── pipeline_setup.py      # Module to setup pipeline stages
|   ├── pipeline_stages.py     # Module to setup model pipeline
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

```
# Installing pyspark and spark-nlp
! pip install --upgrade -q pyspark==3.1.2 spark-nlp==$PUBLIC_VERSION

# Installing Spark NLP Healthcare
! pip install --upgrade -q spark-nlp-jsl==$JSL_VERSION  --extra-index-url https://pypi.johnsnowlabs.com/$SECRET

# Installing Spark NLP Display Library for visualization
! pip install -q spark-nlp-display
```

To install Java 8 on Ubuntu, you can use the following steps:

1. **Update the package index:**
   ```bash
   sudo apt update
   ```

2. **Install Java 8:**
   ```bash
   sudo apt install openjdk-8-jdk
   ```

3. **Verify the installation:**
   ```bash
   java -version
   ```

   This should output something like:
   ```
   openjdk version "1.8.0_xxx"
   OpenJDK Runtime Environment (build 1.8.0_xxx-xxx)
   OpenJDK 64-Bit Server VM (build 25.71-b00, mixed mode)
   ```

4. **Set Java 8 as the default Java version (if you have multiple versions installed):**
   ```bash
   sudo update-alternatives --config java
   ```

   This command will list all installed Java versions. Select the appropriate number for Java 8.

5. **Set the `JAVA_HOME` environment variable (optional but recommended):**

   Open the `/etc/environment` file in an editor:
   ```bash
   sudo nano /etc/environment
   ```

   Add the following line:
   ```bash
   JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
   ```

   Save and close the file, then reload it:
   ```bash
   source /etc/environment
   ```

   You can verify it by:
   ```bash
   echo $JAVA_HOME
   ```
** Alternative:
```
sudo apt install openjdk-8-jdk openjdk-8-jre

# Add to - /etc/environment
JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
JRE_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre


```
6. **Set SPARK_LOCAL_IP** on Ubuntu, if get gateway error.
```
JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
SPARK_LOCAL_IP=10.0.3.240 / IP ADDRESS
```

7. **PySpark** on Ubuntu
```
https://medium.com/@GalarnykMichael/install-spark-on-ubuntu-pyspark-231c45677de0
```
