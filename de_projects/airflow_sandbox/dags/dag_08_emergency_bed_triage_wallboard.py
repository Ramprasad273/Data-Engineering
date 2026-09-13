"""
DAG 08: Emergency Bed Triage & Operational Wallboard Feed.

Characteristics:
- Completely autonomous operational DAG running on its own independent cron (@hourly).
- NO TriggerDagRunOperator (Decoupled operational service).
- Periodically aggregates acute hospital bed occupancy and surge capacity directly for ER nursing wallboards.
"""

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "emergency_operations_director",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    "append_env": True,
}

DBT_DIR = os.getenv("AIRFLOW_DBT_DIR", "/opt/airflow/dbt_project")
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
    dag_id="dag_08_emergency_bed_triage_wallboard",
    default_args=default_args,
    description="Live emergency triage bed capacity & acute unit census refresh (Autonomous Cron - NO TriggerDagRunOperator)",
    schedule_interval="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["emergency", "triage", "beds", "wallboard", "operations", "independent"],
) as dag:

    # Refresh bed census and hospital capacity models for the live wallboard
    refresh_triage_beds = BashOperator(
        task_id="refresh_bed_triage_feed",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select stg_bed_census rpt_hospital_bed_capacity --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )
