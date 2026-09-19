# Airflow Sandbox & Clinical Data Platform

Production-grade data engineering sandbox demonstrating multi-tier clinical data orchestration, distributed processing, dimensional modeling with dbt, and comprehensive infrastructure observability.

## Architectural Overview

The platform simulates a high-acuity healthcare informatics environment (EHR & ICU patient operations) featuring:
- Multi-DAG Orchestration: 9 coordinated Airflow DAGs implementing stream ingestion, event-driven cascades, and decoupled sensor auditing.
- Warehouse & Dimensional Modeling: PostgreSQL 16 warehouse running 18 dbt models across 5 lineage tiers (Staging -> Intermediate -> Marts -> Reporting -> Exposures).
- Distributed Compute: Apache Spark 3.5.0 cluster with Spark Master and Worker nodes configured for batch aggregation and analytical jobs.
- Full Observability Stack: Prometheus metric scraping, Grafana dashboards, Promtail and Loki log aggregation, and StatsD metric export.

### Service Endpoints

| Service | Container Name | Host Port | Internal Port | Configuration Key |
|---------|----------------|-----------|---------------|-------------------|
| Airflow Webserver | `metrics_airflow_webserver` | 8080 | 8080 | `_AIRFLOW_WWW_USER_PASSWORD` |
| Grafana Dashboard | `metrics_grafana_server` | 3001 | 3000 | `GF_SECURITY_ADMIN_PASSWORD` |
| Prometheus | `metrics_prometheus` | 9090 | 9090 | (no auth required) |
| Spark Master UI | `metrics_spark_master` | 8081 | 8080 | (no auth required) |
| Spark Master RPC | `metrics_spark_master` | 7077 | 7077 | - |
| Clinical PostgreSQL | `clinical_postgres` | 5433 | 5432 | `CLINICAL_DB_PASSWORD` |
| Airflow Metadata DB | `metrics_airflow_db` | - | 5432 | `POSTGRES_PASSWORD` |
| Loki | `metrics_loki` | 3100 | 3100 | - |
| Node Exporter | `metrics_node_exporter` | 9100 | 9100 | - |
| StatsD Exporter | `metrics_statsd_exporter` | 9102 | 9102 | - |

## Pipeline Lineage & DAG Architecture

### Airflow DAG Suite

1. `dag_00_hospital_ops_coordinator`: Master coordinator that triggers daily batch processing cascades.
2. `dag_01_ingest_bedside_telemetry`: High-frequency autonomous ingestion of streaming bedside vital monitors (`*/15 * * * *`).
3. `dag_02_ingest_adt_encounters`: Admission, Discharge, and Transfer (ADT) encounter staging.
4. `dag_03_ingest_pharmacy_and_labs`: Laboratory Information Systems (LIS) results and pharmacy medication orders ingestion.
5. `dag_04_transform_intermediate_clinical`: Entity stitching, active medication cycles, and hourly telemetry window aggregation.
6. `dag_05_build_enterprise_clinical_marts`: Materializes core clinical facts (`fct_clinical_encounters`, `fct_icu_hourly_patient_vitals`) and dimensions (`dim_patients`, `dim_departments`).
7. `dag_06_publish_executive_reporting`: Aggregates hospital bed capacity, adverse drug event surveillance, and ICU sepsis risk alerts.
8. `dag_07_governance_and_quality_audit`: Sensor-driven data governance pipeline using `ExternalTaskSensor` to audit upstream model completion without tight coupling.
9. `dag_08_emergency_bed_triage_wallboard`: Hourly autonomous wallboard reporting for emergency room bed allocation.

### dbt Modeling Tiers

The `dbt_project` defines 18 models structured across 5 hierarchical layers:
- Level 1: Staging (`models/staging/`): Cleans and standardizes raw telemetry, encounters, medication orders, labs, bed census, and ICU stays.
- Level 2: Intermediate (`models/intermediate/`): Performs entity stitching, active medication cycle calculations, and abnormal lab event windowing.
- Level 3: Marts (`models/marts/`): Core star-schema fact tables and conformed dimension models.
- Level 4: Reporting (`models/reporting/`): Business and clinical KPI aggregations including ICU sepsis risk surveillance and hospital capacity.
- Level 5: Exposures (`models/exposures/clinical_exposures.yml`): Formally registers downstream consumers including Grafana executive dashboards and clinical alerting engines.

## Observability & Dashboards

The stack auto-provisions a Chief Medical Officer (CMO) Executive Operations Dashboard in Grafana (`cmo-exec-ops`):
- Active Septic Shock Alerts: Real-time flags for acute hemodynamic collapse (SBP < 90 mmHg, HR > 110 bpm).
- Adverse Drug Incidents (ADE): Surveillance for high cumulative pharmaceutical toxicity (> 1,000 mg) combined with abnormal renal/cardiac lab values.
- Inpatient Bed Allocation & Unit Census: Live capacity tracking across ICU-North, ICU-South, Emergency, Cardiac Surgery, and Oncology.
- Airflow & Infrastructure Metrics: Executor task duration, scheduler heartbeat latency, container memory usage, and JVM memory pools.

## Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose v2.0+
- 8 GB RAM minimum (16 GB recommended)

### 1. Configure Environment
Copy the sample environment file to `.env` to override default credentials:
```bash
cp .env.example .env
```

### 2. Start the Stack
Start all services in detached mode:
```bash
docker-compose up -d
```

The `clinical-init` service automatically executes upon startup:
1. Verifies PostgreSQL connectivity.
2. Generates synthetic EHR records via `scripts/generate_synthetic_data.py`.
3. Compiles and materializes initial dbt models in the `healthcare_dwh` database.

### 3. Verify System Health
Run the automated verification suite to validate containers, DAG configurations, dbt models, and dashboard provisioning:
```bash
python scripts/verify_experiment.py
```

### 4. Access Platform UIs
- Airflow UI: [http://localhost:8080](http://localhost:8080)
- Grafana: [http://localhost:3001](http://localhost:3001)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Spark Master: [http://localhost:8081](http://localhost:8081)

*Note: Access credentials are authenticated against the environment variables defined in your local `.env` configuration file.*

## Teardown
To stop all containers and preserve volume data:
```bash
docker-compose down
```

To stop containers and wipe volume data (resets all databases and state):
```bash
docker-compose down -v
```
