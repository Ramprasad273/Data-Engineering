FROM apache/airflow:2.9.3-python3.11

USER root

# Install Java for Spark
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

# Install Apache Airflow providers
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark==4.7.0 \
    kafka-python \
    dbt-core==1.7.0 \
    dbt-postgres==1.7.0 \
    dbt-snowflake==1.7.0 \
    psycopg2-binary

# Configure Airflow for running with dbt while app is operational
COPY config/airflow_local_settings.py /opt/airflow/config/airflow_local_settings.py

# Set permissions for DAGs folder
RUN chmod -R 755 /opt/airflow/dags \
    && chmod -R 755 /opt/airflow/logs \
    && chmod -R 755 /opt/airflow/plugins \
    && chmod -R 755 /opt/airflow/config

# Install Python dependencies for dbt compatibility
RUN pip install --no-cache-dir \
    python-dateutil \
    pytz \
    pendulum
