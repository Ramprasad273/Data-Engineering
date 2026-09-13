"""
DAG 00: Hospital Operations Master Coordinator.

Characteristics:
- Master orchestration coordinator for manual execution, integration testing, and full-stack CI runs.
- Triggers upstream decoupled ingestion feeds in parallel and initiates the end-to-end clinical platform run.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    "owner": "principal_data_architect",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 0,
}

with DAG(
    dag_id="dag_00_hospital_ops_coordinator",
    default_args=default_args,
    description="Master coordinator triggering full clinical platform batch flows on demand",
    schedule_interval=None,  # Manual / On-Demand trigger
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["master", "coordinator", "e2e", "orchestration"],
) as dag:

    trigger_vitals = TriggerDagRunOperator(
        task_id="trigger_dag_01_telemetry",
        trigger_dag_id="dag_01_ingest_bedside_telemetry",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    trigger_encounters = TriggerDagRunOperator(
        task_id="trigger_dag_02_adt_encounters",
        trigger_dag_id="dag_02_ingest_adt_encounters",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    trigger_pharmacy = TriggerDagRunOperator(
        task_id="trigger_dag_03_pharmacy_and_labs",
        trigger_dag_id="dag_03_ingest_pharmacy_and_labs",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    trigger_triage = TriggerDagRunOperator(
        task_id="trigger_dag_08_bed_triage",
        trigger_dag_id="dag_08_emergency_bed_triage_wallboard",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    [trigger_vitals, trigger_encounters, trigger_pharmacy, trigger_triage]
