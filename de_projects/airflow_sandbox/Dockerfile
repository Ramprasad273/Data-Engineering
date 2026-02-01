FROM apache/airflow:2.9.3-python3.11

USER root

# Install Java
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Copy Spark from official image
COPY --from=apache/spark:3.5.0 /opt/spark /opt/spark

ENV SPARK_HOME=/opt/spark

# IMPORTANT: Keep Airflow path + add Spark
ENV PATH="/home/airflow/.local/bin:/opt/spark/bin:${PATH}"

USER airflow

# Install provider in airflow venv
RUN pip install --no-cache-dir apache-airflow-providers-apache-spark==4.7.0
