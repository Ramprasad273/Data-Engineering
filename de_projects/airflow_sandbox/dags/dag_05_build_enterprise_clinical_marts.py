"""
DAG 05: Enterprise Clinical Marts Layer (Core Facts & Dimensions).

Characteristics:
- Triggered by DAG 04 completion or coordinator.
- Materializes core dimensional model in PostgreSQL warehouse:
  - dim_patients
  - dim_departments
  - fct_icu_hourly_patient_vitals
  - fct_clinical_encounters
- Triggers DAG 06 (Executive Reporting) via TriggerDagRunOperator.
"""

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    "owner": "data_warehouse_team",
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
    dag_id="dag_05_build_enterprise_clinical_marts",
    default_args=default_args,
    description="Enterprise dimensional clinical marts materialization (Facts & Dimensions)",
    schedule_interval=None,  # Triggered via TriggerDagRunOperator
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["marts", "facts", "dimensions", "warehouse", "cascade"],
) as dag:

    # 1. Materialize Dimensions
    dbt_dimensions = BashOperator(
        task_id="dbt_dim_patients_and_depts",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select dim_patients dim_departments --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 2. Materialize Core ICU Vitals Fact Table
    dbt_fct_vitals = BashOperator(
        task_id="dbt_fct_icu_hourly_vitals",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select fct_icu_hourly_patient_vitals --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 3. Materialize Clinical Encounters Fact Table
    dbt_fct_enc = BashOperator(
        task_id="dbt_fct_clinical_encounters",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} run --select fct_clinical_encounters --profiles-dir .",
        env=ENV_VARS,
        append_env=True,
    )

    # 4. Trigger Executive Reporting Layer
    trigger_reporting = TriggerDagRunOperator(
        task_id="trigger_executive_reporting",
        trigger_dag_id="dag_06_publish_executive_reporting",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    dbt_dimensions >> [dbt_fct_vitals, dbt_fct_enc] >> trigger_reporting
