# Data Engineering Sandbox

# Data Engineering Sandbox

[![Build Status](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/ci.yml)
[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](tests)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](tests)

This project provides a local, production-grade data platform simulation environment using Docker Compose. It is designed to be a self-contained platform for developing and testing data pipelines.

## Project Installation and Execution

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

### How to run the Fintech Pipelines

1.  **Access the Airflow UI:**
    Open your web browser and navigate to `http://localhost:8080`.
    Use the following credentials to log in:
    -   **Username:** `admin`
    -   **Password:** `admin`

2.  **Trigger the Fintech DAGs:**
    -   In the Airflow UI, you will see the following DAGs:
        - `transaction_ingestion`
        - `customer_merchant_master`
        - `settlement_reconciliation`
        - `fraud_feature_engineering`
        - `risk_scoring`
    -   Enable the DAGs by clicking the toggle button on the left.
    -   Trigger the DAGs by clicking the "play" button on the right.

3.  **Monitor the pipelines:**
    You can monitor the progress of the pipelines in the Airflow UI. Once the pipelines are complete, you can check the tables in the `postgres` database.

## Dashboards

The project includes a monitoring stack with Grafana dashboards. To access the Grafana dashboards, go to `http://localhost:3000` in your browser. The default username and password are `admin` and `admin`.

The following dashboards are available:

-   **Infrastructure Monitoring**: To monitor the health of the Docker containers.
-   **Log Analytics**: To analyze the logs from the different services.
-   **Database Monitoring**: To monitor the health of the PostgreSQL database.
-   **Pipeline Monitoring**: To monitor the status of the Airflow DAGs.
-   **Data Quality Monitoring**: To monitor the quality of the data in the tables.

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
