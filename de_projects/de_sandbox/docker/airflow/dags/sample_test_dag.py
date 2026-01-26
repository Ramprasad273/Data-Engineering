from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="sample_test_dag",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    # dbt tasks
    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command="dbt seed --profiles-dir /opt/dbt --project-dir /opt/dbt",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run --profiles-dir /opt/dbt --project-dir /opt/dbt",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="dbt test --profiles-dir /opt/dbt --project-dir /opt/dbt",
    )

    # Great Expectations task
    ge_checkpoint = BashOperator(
        task_id="ge_checkpoint",
        bash_command="great_expectations checkpoint run raw_customers_checkpoint --config-dir /opt/great_expectations",
    )

    dbt_seed >> dbt_run >> dbt_test >> ge_checkpoint
