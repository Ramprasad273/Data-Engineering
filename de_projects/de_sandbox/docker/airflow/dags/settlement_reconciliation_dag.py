
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.task_group import TaskGroup
from monitoring import on_failure_callback

with DAG(
    dag_id="settlement_reconciliation",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["fintech"],
    default_args={"on_failure_callback": on_failure_callback},
) as dag:
    with TaskGroup(group_id="reconciliation_group") as reconciliation_group:
        spark_task = SparkSubmitOperator(
            task_id="reconcile_settlements",
            conn_id="spark_default",
            application="/opt/spark/jobs/settlement_reconciliation.py",
            application_args=[
                "--transactions-table",
                "raw_transactions",
                "--settlement-files-path",
                "/opt/spark/data/settlements.csv",
                "--output-table",
                "fact_settlements",
            ],
        )
