# Airflow Sandbox with Spark

## Objective

This project provides a self-contained development environment for running Apache Airflow with a distributed Apache Spark cluster. It is designed to be an easy-to-use sandbox for developing, testing, and running data pipelines that leverage the power of Spark for distributed data processing, orchestrated by Airflow.

The key goals of this project are:
- To provide a one-command setup for a complete Airflow and Spark environment.
- To demonstrate how to integrate Airflow with Spark for running PySpark jobs.
- To offer a starting point for building more complex data engineering projects.

## Architecture

The environment is orchestrated using `docker-compose` and consists of the following services:

```
+--------------------------+      +-------------------------+
|      Airflow Services    |      |      Spark Cluster      |
|                          |      |                         |
|  +-------------------+   |      |  +------------------+   |
|  |  Webserver (UI)   |   |      |  |   Spark Master   |   |
|  +-------------------+   |      |  +------------------+   |
|                          |      |                         |
|  +-------------------+   |      |  +------------------+   |
|  |    Scheduler      |   |      |  |   Spark Worker   |   |
|  +-------------------+   |      |  +------------------+   |
|                          |      +-----------+-------------+
|  +-------------------+   |                  |
|  |   Celery Worker   |---+------------------+ (Submit Jobs)
|  +-------------------+   |
|                          |
+------------+-------------+
             |
+------------+-------------+
|    Supporting Services   |
|                          |
|  +-------------------+   |
|  |    PostgreSQL     |   | (Metadata DB)
|  +-------------------+   |
|                          |
|  +-------------------+   |
|  |       Redis       |   | (Celery Broker)
|  +-------------------+   |
|                          |
+--------------------------+
```

### Components

-   **Airflow**:
    -   `airflow-webserver`: The Airflow UI, accessible at `http://localhost:8080`.
    -   `airflow-scheduler`: Responsible for scheduling and triggering DAGs.
    -   `airflow-worker`: A Celery worker that executes the tasks defined in the DAGs.
-   **Spark**:
    -   `spark-master`: The master node of the Spark cluster. Its UI is available at `http://localhost:8081`.
    -   `spark-worker`: A worker node that performs the actual data processing.
-   **Supporting Services**:
    -   `postgres`: A PostgreSQL database used by Airflow to store its metadata.
    -   `redis`: A Redis instance that acts as a message broker for the CeleryExecutor.

## How to Run

### Prerequisites

-   Docker
-   Docker Compose

### 1. Start the Environment

To start all the services in detached mode, run the following command from the `airflow_sandbox` directory:

```bash
docker-compose up -d
```

### 2. Access the Services

-   **Airflow UI**: Open your web browser and navigate to `http://localhost:8080`.
    -   **Username**: `admin`
    -   **Password**: `admin`
-   **Spark Master UI**: Open your web browser and navigate to `http://localhost:8081`.

### 3. Running the Example DAG

The project comes with an example DAG called `spark_data_pipeline`. This DAG demonstrates how to run a PySpark job from Airflow.

1.  In the Airflow UI, you should see the `spark_data_pipeline` DAG.
2.  Enable the DAG by clicking the toggle switch next to its name.
3.  The DAG will run based on its schedule (`@daily`), or you can trigger it manually by clicking the "play" button.

The DAG has two tasks that run the same Spark job (`pyspark_sample.py`) in two different ways:
-   `spark_bash_local_mode`: Uses a `BashOperator` to execute `spark-submit`.
-   `spark_operator_local_mode`: Uses the `SparkSubmitOperator`.

### 4. Stop the Environment

To stop all the services, run:

```bash
docker-compose down
```

To stop the services and remove all volumes (this will delete the Airflow metadata and logs), run:

```bash
docker-compose down -v
```

## Common Issues and Fixes

-   **Issue**: Airflow UI is not accessible at `http://localhost:8080`.
    -   **Fix**: Check the logs of the `airflow-webserver` container for errors: `docker-compose logs -f airflow-webserver`. It might take a few minutes for the webserver to start up, especially on the first run.

-   **Issue**: The `spark_data_pipeline` DAG is not visible in the Airflow UI.
    -   **Fix**: Check the logs of the `airflow-scheduler` container: `docker-compose logs -f airflow-scheduler`. Ensure there are no errors in the DAG file (`dags/spark_pipeline.py`).

-   **Issue**: The Spark job fails with a connection error.
    -   **Fix**:
        1.  Verify that the Spark master and worker are running correctly by checking their logs: `docker-compose logs -f spark-master` and `docker-compose logs -f spark-worker`.
        2.  Check the Spark Master UI at `http://localhost:8081` to see if the worker is registered.
        3.  The example DAG includes a commented-out task for running Spark in cluster mode (`spark_operator_cluster_mode`). This task is known to have connection issues in some environments. For local development, using the local mode tasks is recommended.

-   **Issue**: "Cannot create container for service airflow-worker: invalid mount config for type "bind": bind source path does not exist".
    -   **Fix**: This can happen if the directory structure on your host machine does not match what's expected in the `docker-compose.yaml`. Make sure all the mapped volumes like `./dags`, `./logs`, etc., exist in the `airflow_sandbox` directory.