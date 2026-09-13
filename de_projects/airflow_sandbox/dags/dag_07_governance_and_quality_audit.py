"""
DAG 07: Data Reliability Engineering, Schema Contracts & Quality Audit.

Characteristics:
- Runs on its own schedule (@hourly).
- NO TriggerDagRunOperator (Decoupled governance pipeline).
- Uses ExternalTaskSensor to sense upstream completion of dag_06_publish_executive_reporting.
- Executes full dbt test quality assertions, validating non-nullability, uniqueness, and metric integrity.
"""

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor

default_args = {
    "owner": "data_reliability_engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
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
    dag_id="dag_07_governance_and_quality_audit",
    default_args=default_args,
    description="Data reliability engineering, schema contracts & quality audit (ExternalTaskSensor - NO TriggerDagRunOperator)",
    schedule_interval="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["governance", "quality", "sensor", "dre", "contracts", "independent"],
) as dag:

    # 1. Sense upstream executive reporting completion (NO TriggerDagRunOperator used)
    sense_reporting_complete = ExternalTaskSensor(
        task_id="sense_executive_reporting_completion",
        external_dag_id="dag_06_publish_executive_reporting",
        external_task_id="dbt_rpt_cmo_kpis",
        mode="reschedule",
        poke_interval=60,
        timeout=1800,
        allowed_states=["success"],
        failed_states=["failed"],
    )

    # 2. Audit Staging Layer Contracts
    audit_staging = BashOperator(
        task_id="audit_staging_contracts",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} test --select staging --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 3. Audit Enterprise Marts & Dimension Integrity
    audit_marts = BashOperator(
        task_id="audit_marts_referential_integrity",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} test --select marts --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 4. Audit Executive Reporting Metrics & Risk Tiers
    audit_reporting = BashOperator(
        task_id="audit_reporting_risk_metrics",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} test --select reporting --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    sense_reporting_complete >> audit_staging >> audit_marts >> audit_reporting
