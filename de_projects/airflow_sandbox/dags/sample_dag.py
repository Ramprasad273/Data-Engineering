from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="sandbox_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    start = BashOperator(
        task_id="start",
        bash_command="echo 'Pipeline Started'"
    )

    end = BashOperator(
        task_id="end",
        bash_command="echo 'Pipeline Finished'"
    )

    start >> end
