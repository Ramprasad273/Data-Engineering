"""
DAG 04: Intermediate Clinical Entity Aggregation & Feature Engineering.

Characteristics:
- Triggered by upstream staging completion or master coordinator.
- Builds longitudinal feature aggregates and window calculations:
  - int_vitals_hourly_aggregated
  - int_abnormal_lab_events
  - int_medication_active_cycles
  - int_icu_stay_timeline
- Triggers DAG 05 (Enterprise Marts) via TriggerDagRunOperator.
"""

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    "owner": "clinical_analytics_engineering",
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
    dag_id="dag_04_transform_intermediate_clinical",
    default_args=default_args,
    description="Intermediate clinical entity aggregation and longitudinal feature engineering",
    schedule_interval=None,  # Triggered via TriggerDagRunOperator
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["intermediate", "features", "windowing", "clinical", "cascade"],
) as dag:

    # 1. Transform Hourly Vital Sign Aggregates
    dbt_int_vitals = BashOperator(
        task_id="dbt_int_vitals_hourly",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select int_vitals_hourly_aggregated --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 2. Transform Abnormal Lab Events
    dbt_int_labs = BashOperator(
        task_id="dbt_int_abnormal_labs",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select int_abnormal_lab_events --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 3. Transform Active Medication Cycles
    dbt_int_meds = BashOperator(
        task_id="dbt_int_medication_cycles",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select int_medication_active_cycles --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 4. Transform ICU Stay Timeline
    dbt_int_icu = BashOperator(
        task_id="dbt_int_icu_timeline",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select int_icu_stay_timeline --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 5. Trigger Core Enterprise Marts Layer
    trigger_marts = TriggerDagRunOperator(
        task_id="trigger_enterprise_marts",
        trigger_dag_id="dag_05_build_enterprise_clinical_marts",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    [dbt_int_vitals, dbt_int_labs, dbt_int_meds, dbt_int_icu] >> trigger_marts
