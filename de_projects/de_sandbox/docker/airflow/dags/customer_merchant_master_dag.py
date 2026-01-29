
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.task_group import TaskGroup
from monitoring import on_failure_callback

with DAG(
    dag_id="customer_merchant_master",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,
    tags=["fintech"],
    default_args={"on_failure_callback": on_failure_callback},
) as dag:
    with TaskGroup(group_id="master_data_group") as master_data_group:
        spark_task = SparkSubmitOperator(
            task_id="ingest_customer_merchant_master",
            conn_id="spark_default",
            application="/opt/spark/jobs/customer_merchant_master.py",
            application_args=[
                "--customer-input-path",
                "/opt/spark/data/customers.csv",
                "--merchant-input-path",
                "/opt/spark/data/merchants.csv",
                "--customer-output-table",
                "dim_customers",
                "--merchant-output-table",
                "dim_merchants",
            ],
        )
