
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.task_group import TaskGroup
from monitoring import on_failure_callback

with DAG(
    dag_id="risk_scoring",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["fintech"],
    default_args={"on_failure_callback": on_failure_callback},
) as dag:
    with TaskGroup(group_id="risk_scoring_group") as risk_scoring_group:
        spark_task = SparkSubmitOperator(
            task_id="generate_risk_scores",
            conn_id="spark_default",
            application="/opt/spark/jobs/risk_scoring.py",
            application_args=[
                "--fraud-features-table",
                "fraud_features",
                "--output-table",
                "risk_scores",
            ],
        )
