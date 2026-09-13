"""
DAG 03: Ancillary Clinical Systems Ingestion (Pharmacy Orders & Laboratory Chemistry).

Characteristics:
- Runs hourly or triggered via coordinator.
- Ingests medication orders from pharmacy dispensing and laboratory diagnostics from LIS.
- Materializes stg_medication_orders and stg_lab_results.
"""

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "pharmacy_and_pathology_team",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
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
    dag_id="dag_03_ingest_pharmacy_and_labs",
    default_args=default_args,
    description="Pharmacy medication orders & LIS laboratory results ingestion and staging",
    schedule_interval="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["pharmacy", "labs", "lis", "ancillary"],
) as dag:

    # 1. Ingest Medication Orders and Lab Chemistry
    ingest_meds_labs = BashOperator(
        task_id="ingest_meds_and_labs_feed",
        bash_command=f"python {SCRIPTS_DIR}/generate_synthetic_data.py --source meds_and_labs",
        env=ENV_VARS,
        append_env=True,
    )

    # 2. Materialize Pharmacy & Lab Staging Models
    dbt_stg_meds_labs = BashOperator(
        task_id="dbt_stg_medication_and_labs",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select stg_medication_orders stg_lab_results --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    ingest_meds_labs >> dbt_stg_meds_labs
