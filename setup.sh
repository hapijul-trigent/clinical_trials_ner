#!/bin/bash

# Step 1: Update the package index
echo "Updating package index..."
sudo apt update

# Step 2: Install Java 8
echo "Installing Java 8..."
sudo apt install -y openjdk-8-jdk openjdk-8-jre

# Step 3: Verify the Java installation
echo "Verifying Java installation..."
java -version

# Step 4: Set Java 8 as the default version (if needed)
echo "Setting Java 8 as the default version..."
sudo update-alternatives --config java

# Step 5: Set the JAVA_HOME environment variable
echo "Setting JAVA_HOME environment variable..."
JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
echo "JAVA_HOME=$JAVA_HOME" | sudo tee -a /etc/environment
source /etc/environment
echo "JAVA_HOME is set to $JAVA_HOME"

# Step 6: Set SPARK_LOCAL_IP (if needed)
echo "Setting SPARK_LOCAL_IP..."
SPARK_LOCAL_IP="<YOUR_IP_ADDRESS>"  # Replace with your actual IP address
echo "SPARK_LOCAL_IP=$SPARK_LOCAL_IP" | sudo tee -a /etc/environment
source /etc/environment
echo "SPARK_LOCAL_IP is set to $SPARK_LOCAL_IP"

# Step 7: Install pyspark and spark-nlp
echo "Installing PySpark and Spark NLP..."
pip install --upgrade -q pyspark==3.1.2 spark-nlp==$PUBLIC_VERSION

# Step 8: Install Spark NLP Healthcare
echo "Installing Spark NLP Healthcare..."
pip install --upgrade -q spark-nlp-jsl==$JSL_VERSION --extra-index-url https://pypi.johnsnowlabs.com/$SECRET

# Step 9: Install Spark NLP Display Library for visualization
echo "Installing Spark NLP Display Library..."
pip install -q spark-nlp-display

echo "Setup complete!"
