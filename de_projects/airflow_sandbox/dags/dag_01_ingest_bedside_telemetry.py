"""
DAG 01: Bedside Telemetry Stream Ingestion (High-Frequency Streaming Simulation).

Characteristics:
- Runs independently on a frequent cron schedule (*/15 * * * *).
- NO TriggerDagRunOperator (Decoupled IoT monitor stream).
- Ingests raw bedside telemetry and materializes the stg_patient_vitals staging view.
"""

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "clinical_telemetry_team",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 2,
    "retry_delay": timedelta(seconds=30),
    "append_env": True,
}

DBT_DIR = os.getenv("AIRFLOW_DBT_DIR", "/opt/airflow/dbt_project")
SCRIPTS_DIR = os.getenv("AIRFLOW_SCRIPTS_DIR", "/opt/airflow/scripts")
DBT_BIN = os.getenv("DBT_BIN", "/home/airflow/.local/bin/dbt" if os.path.exists("/home/airflow/.local/bin/dbt") else "dbt")
ENV_VARS = {
    "PATH": f"/home/airflow/.local/bin:{os.environ.get('PATH', '/usr/local/bin:/usr/bin:/bin')}",
    "DB_HOST": os.getenv("DB_HOST", "clinical-postgres"),
    "DB_PORT": os.getenv("DB_PORT", "5432"),
    "DB_NAME": os.getenv("DB_NAME", "healthcare_dwh"),
    "DB_USER": os.getenv("DB_USER", "clinical_admin"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD", "clinical_secure_password"),
}

with DAG(
    dag_id="dag_01_ingest_bedside_telemetry",
    default_args=default_args,
    description="High-frequency bedside vital telemetry stream ingestion & staging (Independent Cron)",
    schedule_interval="*/15 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["streaming", "telemetry", "vitals", "iot", "independent"],
) as dag:

    # 1. Ingest Bedside Telemetry IoT Feed
    ingest_telemetry = BashOperator(
        task_id="ingest_bedside_telemetry_feed",
        bash_command=f"python {SCRIPTS_DIR}/generate_synthetic_data.py --source vitals",
        env=ENV_VARS,
        append_env=True,
    )

    # 2. Materialize Staging Vitals View
    dbt_stg_vitals = BashOperator(
        task_id="dbt_stg_patient_vitals",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select stg_patient_vitals --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    ingest_telemetry >> dbt_stg_vitals
