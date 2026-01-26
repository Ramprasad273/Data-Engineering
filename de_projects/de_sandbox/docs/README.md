# Data Engineering Sandbox Documentation

## 1. System Architecture

### 1.1. Overview

This project provides a local, production-grade data platform simulation environment using Docker Compose. It is designed to be a self-contained platform for developing and testing data pipelines.

### 1.2. Components

- **Storage & Databases:**
  - **MinIO:** S3-compatible object storage for raw data and artifacts.
  - **PostgreSQL:** OLTP database for metadata, and as a data warehouse.
  - **DuckDB:** Embedded OLAP database for analytics and testing (via dbt).

- **Orchestration & Transformation:**
  - **Apache Airflow:** Workflow orchestration.
  - **dbt:** Data transformation.
  - **Great Expectations:** Data quality and validation.

- **Observability & Ops:**
  - **Prometheus:** Metrics collection.
  - **Grafana:** Dashboards and visualization.
  - **Loki:** Log aggregation.
  - **Promtail:** Log shipping.

### 1.3. Data Flow

A sample data flow is provided in the example DAG:

1.  **Data Ingestion:** A CSV file is placed in the `dbt/seeds` directory.
2.  **dbt seed:** The CSV data is loaded into the `raw_customers` table in Postgres.
3.  **dbt run:** A dbt model transforms the raw data and creates a `stg_customers` view.
4.  **Great Expectations:** A checkpoint validates the data in the `raw_customers` table.

## 2. Getting Started

### 2.1. Prerequisites

-   Docker
-   Docker Compose
-   A `git` client to clone the repository.

### 2.2. Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd Data-Engineering/de_projects/de_sandbox
    ```
3.  **Create the environment file:**
    Create a `.env` file by copying the example file. This file contains all the credentials and configurations for the services.
    ```bash
    cp .env.example .env
    ```
    _Note: You can customize the values in the `.env` file if needed. If you are updating the project, make sure to check if the `.env.example` file has changed and update your `.env` file accordingly. It is crucial that the `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` variable is set correctly for Airflow to connect to the PostgreSQL database._

4.  **Start the platform:**
    This command will build the Docker images and start all the services in the background.
    ```bash
    make up
    ```
    _**Note:** If you do not have `make` installed, you can use the following command instead:_
    ```bash
    docker compose up -d --build
    ```
    You can check the status of the services by running `docker compose ps`.

### 2.3. How to run the example pipeline

1.  **Access the Airflow UI:**
    Open your web browser and navigate to `http://localhost:8080`.
    Use the following credentials to log in:
    -   **Username:** `airflow`
    -   **Password:** `airflow`

2.  **Trigger the example DAG:**
    -   In the Airflow UI, you will see a DAG named `example_dag`.
    -   Enable the DAG by clicking the toggle button on the left.
    -   Trigger the DAG by clicking the "play" button on the right.

3.  **Monitor the pipeline:**
    You can monitor the progress of the pipeline in the Airflow UI. Once the pipeline is complete, you can check the following:
    -   **dbt:** The `stg_customers` view will be created in the `public` schema of the `airflow` database.
    -   **Great Expectations:** The validation results will be available in the `great_expectations/uncommitted/validations` directory.
    -   **MinIO:** You can access the MinIO UI at `http://localhost:9001` to see the created bucket.

### 2.4. Accessing Services

- **Airflow:** `http://localhost:8080` (user: airflow, pass: airflow)
- **MinIO:** `http://localhost:9001` (user: minioadmin, pass: minioadmin)
- **Grafana:** `http://localhost:3000` (user: admin, pass: admin)
- **Prometheus:** `http://localhost:9090`
- **Loki:** `http://localhost:3100`

## 3. How to...

### 3.1. Add a new Airflow pipeline

1.  Create a new Python file in the `docker/airflow/dags` directory.
2.  Define your DAG and tasks in the file.
3.  The new DAG will automatically be loaded by Airflow.

### 3.2. Add a new dbt model

1.  Create a new SQL file in the `dbt/models` directory.
2.  Write your dbt transformation logic.
3.  Reference the new model in your Airflow DAGs.

### 3.3. Add a Great Expectations check

1.  Create a new expectation suite using the Great Expectations CLI or by manually creating a JSON file in the `great_expectations/expectations` directory.
2.  Create a new checkpoint in the `great_expectations/checkpoints` directory.
3.  Run the checkpoint from your Airflow DAG.

## 4. Monitoring

The platform includes a basic monitoring stack using Prometheus and Grafana.

- **Prometheus:** Scrapes metrics from the services.
- **Grafana:** Provides a default dashboard to visualize the metrics.

## 5. Future Roadmap

### 5.1. Scaling

The platform is designed to be extensible. To scale the platform, you can:

-   Switch to the Airflow CeleryExecutor for distributed task execution.
-   Increase the number of dbt threads for parallel model execution.
-   Move to a cloud-based environment with more resources.

### 6. Troubleshooting

### 6.1. `alembic.util.exc.CommandError: Can't locate revision identified by ...`

This error occurs when the Airflow database is in a bad state due to a version mismatch or a failed migration. To resolve this, you need to reset the database.

**Warning:** This will delete all your Airflow data, including DAGs, connections, and history.

1.  **Stop and remove all services and volumes:**
    ```bash
    make clean
    ```
    _**Note:** If you do not have `make` installed, you can use the following command instead:_
    ```bash
    docker compose down -v
    ```

2.  **Start the platform again:**
    ```bash
    make up
    ```
