
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.task_group import TaskGroup
from monitoring import on_failure_callback

with DAG(
    dag_id="fraud_feature_engineering",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["fintech"],
    default_args={"on_failure_callback": on_failure_callback},
) as dag:
    with TaskGroup(group_id="feature_engineering_group") as feature_engineering_group:
        spark_task = SparkSubmitOperator(
            task_id="generate_fraud_features",
            conn_id="spark_default",
            application="/opt/spark/jobs/fraud_feature_engineering.py",
            application_args=[
                "--transactions-table",
                "raw_transactions",
                "--output-table",
                "fraud_features",
            ],
        )
