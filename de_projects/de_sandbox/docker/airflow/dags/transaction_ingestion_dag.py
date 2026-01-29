
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.task_group import TaskGroup
from monitoring import on_failure_callback

with DAG(
    dag_id="transaction_ingestion",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["fintech"],
    default_args={"on_failure_callback": on_failure_callback},
) as dag:
    with TaskGroup(group_id="ingestion_group") as ingestion_group:
        spark_task = SparkSubmitOperator(
            task_id="ingest_transactions",
            conn_id="spark_default",
            application="/opt/spark/jobs/transaction_ingestion.py",
            application_args=[
                "--input-path",
                "/opt/spark/data/raw_transactions.json",
                "--output-table",
                "raw_transactions",
            ],
            packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0",
        )
