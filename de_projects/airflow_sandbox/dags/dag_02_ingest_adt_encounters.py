"""
DAG 02: Hospital ADT Patient Encounters & Admissions Ingestion.

Characteristics:
- Runs hourly or triggered via coordinator.
- Ingests EHR patient encounters, discharges, and department transfers.
- Materializes stg_clinical_encounters, stg_icu_stays, and stg_bed_census.
- Cascades into DAG 04 (Intermediate Features) via TriggerDagRunOperator.
"""

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    "owner": "hospital_adt_team",
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
    dag_id="dag_02_ingest_adt_encounters",
    default_args=default_args,
    description="Hospital ADT encounter ingestion, staging & intermediate cascade trigger",
    schedule_interval="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ehr", "adt", "encounters", "admissions", "cascade"],
) as dag:

    # 1. Ingest ADT Encounters from EHR
    ingest_adt = BashOperator(
        task_id="ingest_adt_encounters_feed",
        bash_command=f"python {SCRIPTS_DIR}/generate_synthetic_data.py --source encounters",
        env=ENV_VARS,
        append_env=True,
    )

    # 2. Materialize ADT Staging Models
    dbt_stg_adt = BashOperator(
        task_id="dbt_stg_encounters_and_census",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select stg_clinical_encounters stg_icu_stays stg_bed_census --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 3. Trigger Intermediate Entity Layer
    trigger_intermediate = TriggerDagRunOperator(
        task_id="trigger_intermediate_transformation",
        trigger_dag_id="dag_04_transform_intermediate_clinical",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    ingest_adt >> dbt_stg_adt >> trigger_intermediate
