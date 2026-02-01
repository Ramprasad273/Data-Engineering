from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

with DAG(
    dag_id="spark_data_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["spark", "pyspark", "demo"],
) as dag:
    
    # Task 1: BashOperator with Local Spark Mode (Most Reliable)
    # This directly calls spark-submit with all parameters
    task_bash_local = BashOperator(
        task_id="spark_bash_local_mode",
        bash_command=(
            "spark-submit "
            "--master local[*] "
            "--driver-memory 512m "
            "--executor-memory 512m "
            "/opt/spark-jobs/jobs/pyspark_sample.py"
        ),
    )
    
    # Task 2: SparkSubmitOperator with Local Mode
    # Uses Airflow's SparkSubmitOperator with a local connection
    # This is the "proper" Airflow way to run Spark jobs locally
    task_spark_local = SparkSubmitOperator(
        task_id="spark_operator_local_mode",
        application="/opt/spark-jobs/jobs/pyspark_sample.py",
        conn_id="spark_local",  # Connection configured for local[*]
        verbose=True,
        application_args=[],
        conf={
            "spark.driver.memory": "512m",
            "spark.executor.memory": "512m",
        },
    )
    
    # Task 3: SparkSubmitOperator with Cluster Mode (COMMENTED OUT - Has connection issues)
    # The cluster mode fails due to Spark master connectivity issues
    # Keeping this commented for reference on how to configure cluster mode
    # 
    # task_spark_cluster = SparkSubmitOperator(
    #     task_id="spark_operator_cluster_mode",
    #     application="/opt/spark-jobs/jobs/pyspark_sample.py",
    #     conn_id="spark_default",  # spark://spark-master:7077
    #     deploy_mode="client",
    #     verbose=True,
    #     driver_memory="512m",
    #     executor_memory="512m",
    #     total_executor_cores=1,
    #     conf={
    #         "spark.driver.maxResultSize": "512m",
    #     },
    # )
    
    # Run both working tasks in parallel
    [task_bash_local, task_spark_local]

