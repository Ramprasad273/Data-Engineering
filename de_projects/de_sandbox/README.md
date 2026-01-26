# Data Engineering Sandbox

This project provides a local, production-grade data platform simulation environment using Docker Compose. It is designed to be a self-contained platform for developing and testing data pipelines.

## Project Setup and Execution

### Prerequisites

*   Docker
*   Docker Compose
*   A `git` client to clone the repository.

### Setup

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
    _Note: You can customize the values in the `.env` file if needed. If you are updating the project, make sure to check if the `.env.example` file has changed and update your `.env` file accordingly._

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

### How to run the example pipeline

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

## Services

- **Airflow:** `http://localhost:8080` (user: airflow, pass: airflow)
- **MinIO:** `http://localhost:9001` (user: minioadmin, pass: minioadmin)
- **Grafana:** `http://localhost:3000` (user: admin, pass: admin)
- **Prometheus:** `http://localhost:9090`
- **Loki:** `http://localhost:3100`

## Troubleshooting

### `alembic.util.exc.CommandError: Can't locate revision identified by ...`

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

## Documentation

For detailed documentation, please see the `docs/README.md` file.
