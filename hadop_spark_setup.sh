#!/bin/bash

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y curl wget vim openjdk-8-jdk scala git

# Set up environment variables for Java
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> ~/.bashrc
echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> ~/.bashrc
source ~/.bashrc

# Install Hadoop
HADOOP_VERSION="3.3.6"
wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz
tar -xzvf hadoop-$HADOOP_VERSION.tar.gz
sudo mv hadoop-$HADOOP_VERSION /usr/local/hadoop

# Set up Hadoop environment variables
echo "export HADOOP_HOME=/usr/local/hadoop" >> ~/.bashrc
echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" >> ~/.bashrc
echo "export HADOOP_CONF_DIR=\$HADOOP_HOME/etc/hadoop" >> ~/.bashrc
source ~/.bashrc

# Hadoop basic configuration
mkdir -p ~/hadoop_data/hdfs/namenode
mkdir -p ~/hadoop_data/hdfs/datanode

# Configure Hadoop core-site.xml
cat <<EOT >> $HADOOP_HOME/etc/hadoop/core-site.xml
<configuration>
   <property>
      <name>fs.defaultFS</name>
      <value>hdfs://localhost:9000</value>
   </property>
</configuration>
EOT

# Configure Hadoop hdfs-site.xml
cat <<EOT >> $HADOOP_HOME/etc/hadoop/hdfs-site.xml
<configuration>
   <property>
      <name>dfs.replication</name>
      <value>1</value>
   </property>
   <property>
      <name>dfs.namenode.name.dir</name>
      <value>file:///home/$USER/hadoop_data/hdfs/namenode</value>
   </property>
   <property>
      <name>dfs.datanode.data.dir</name>
      <value>file:///home/$USER/hadoop_data/hdfs/datanode</value>
   </property>
</configuration>
EOT

# Format Hadoop Namenode
hdfs namenode -format

# Start Hadoop
start-dfs.sh

# Install Spark
SPARK_VERSION="3.5.0"
wget https://downloads.apache.org/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz
tar -xzvf spark-$SPARK_VERSION-bin-hadoop3.tgz
sudo mv spark-$SPARK_VERSION-bin-hadoop3 /usr/local/spark

# Set up Spark environment variables
echo "export SPARK_HOME=/usr/local/spark" >> ~/.bashrc
echo "export PATH=\$PATH:\$SPARK_HOME/bin:\$SPARK_HOME/sbin" >> ~/.bashrc
source ~/.bashrc

# Start Spark
start-master.sh
start-worker.sh spark://localhost:7077

echo "Hadoop and Spark setup is complete!"
