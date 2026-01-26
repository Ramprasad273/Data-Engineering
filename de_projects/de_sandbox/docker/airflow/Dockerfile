FROM apache/airflow:latest-python3.12

USER root

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python packages
RUN pip install --no-cache-dir \
    apache-airflow-providers-postgres \
    dbt-postgres \
    dbt-duckdb \
    great-expectations \
    "psycopg2-binary" \
    "boto3" \
    "s3fs"