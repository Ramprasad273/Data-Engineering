"""
DAG 06: Executive Reporting Marts & Real-time Sepsis Alerting Feeds.

Characteristics:
- Triggered by DAG 05 completion or coordinator.
- Publishes critical executive reporting tables:
  - rpt_icu_sepsis_risk_surveillance (Feeds P0 ICU Paging System)
  - rpt_adverse_drug_events (Feeds Pharmacy Safety Monitor)
  - rpt_hospital_bed_capacity (Feeds Bed Census Displays)
  - rpt_cmo_executive_quality_kpis (Feeds Port 3000 Grafana CMO Board Dashboard)
- Monitored asynchronously by DAG 07 via ExternalTaskSensor.
"""

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "executive_bi_and_clinical_ops",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
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
    dag_id="dag_06_publish_executive_reporting",
    default_args=default_args,
    description="Executive CMO reporting marts & real-time sepsis surveillance publishing",
    schedule_interval=None,  # Triggered via TriggerDagRunOperator from DAG 05
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["reporting", "executive", "sepsis", "cmo", "grafana", "tier_1"],
) as dag:

    # 1. Publish Real-time ICU Sepsis Surveillance (P0 Clinical Alerting)
    dbt_rpt_sepsis = BashOperator(
        task_id="dbt_rpt_sepsis_surveillance",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select rpt_icu_sepsis_risk_surveillance --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 2. Publish Pharmacy Adverse Drug Event Incidents
    dbt_rpt_ade = BashOperator(
        task_id="dbt_rpt_adverse_drug_events",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select rpt_adverse_drug_events --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 3. Publish Hospital Bed Capacity & Inpatient Allocations
    dbt_rpt_beds = BashOperator(
        task_id="dbt_rpt_hospital_bed_capacity",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select rpt_hospital_bed_capacity --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 4. Publish CMO Executive Scorecard (Feeds Grafana Dashboard)
    dbt_rpt_cmo = BashOperator(
        task_id="dbt_rpt_cmo_kpis",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select rpt_cmo_executive_quality_kpis --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    [dbt_rpt_sepsis, dbt_rpt_ade, dbt_rpt_beds] >> dbt_rpt_cmo
