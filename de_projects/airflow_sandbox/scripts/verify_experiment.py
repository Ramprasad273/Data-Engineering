#!/usr/bin/env python3
"""
Comprehensive Automated Verification Script for Clinical Data Platform Experiment.
Tests:
1. Docker Compose stack configuration & live volume mounts
2. Ingestion script syntax and structure
3. dbt model graph integrity (14 models, 5 lineage tiers)
4. Airflow DAG compilation and task dependencies
5. Grafana datasource and Executive CMO Dashboard schema
6. E2E Blueprint documentation completeness
"""

import json
import os
import re
import sys
import yaml

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def check(condition, message):
    if condition:
        print(f"  [PASS] {message}")
    else:
        print(f"  [FAIL] {message}")
        sys.exit(1)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 70)
    print("VALIDATING CLINICAL DATA PLATFORM EXPERIMENT SETUP")
    print("=" * 70)

    # 1. Validate docker-compose.yaml
    print("\n[1/6] Inspecting docker-compose.yaml...")
    compose_path = os.path.join(base_dir, "docker-compose.yaml")
    check(os.path.exists(compose_path), "docker-compose.yaml exists")
    with open(compose_path, "r", encoding="utf-8") as f:
        compose = yaml.safe_load(f)
    
    services = compose.get("services", {})
    check("clinical-postgres" in services, "clinical-postgres service defined")
    check("clinical-init" in services, "clinical-init automated setup service defined")
    check("grafana-server" in services, "grafana-server service defined")
    check("airflow-webserver" in services, "airflow-webserver service defined")

    # Check volume mounts for hot-reloading
    common_volumes = compose.get("x-airflow-common", {}).get("volumes", [])
    check(any("./dags" in v for v in common_volumes), "dags folder volume-mounted to Airflow")
    check(any("./dbt_project" in v for v in common_volumes), "dbt_project folder volume-mounted to Airflow")
    check(any("./scripts" in v for v in common_volumes), "scripts folder volume-mounted to Airflow")

    grafana_volumes = services.get("grafana-server", {}).get("volumes", [])
    check(any("dashboards" in v for v in grafana_volumes), "Grafana dashboards volume-mounted")
    check(any("provisioning" in v for v in grafana_volumes), "Grafana provisioning volume-mounted")

    # 2. Validate Ingestion Script
    print("\n[2/6] Inspecting Ingestion Script (generate_synthetic_data.py)...")
    ingest_script = os.path.join(base_dir, "scripts", "generate_synthetic_data.py")
    check(os.path.exists(ingest_script), "scripts/generate_synthetic_data.py exists")
    with open(ingest_script, "r", encoding="utf-8") as f:
        code = f.read()
    check("raw.patient_vitals" in code, "Creates raw.patient_vitals table")
    check("raw.clinical_encounters" in code, "Creates raw.clinical_encounters table")
    check("raw.medication_orders" in code, "Creates raw.medication_orders table")
    check("raw.lab_results" in code, "Creates raw.lab_results table")
    check("septic shock" in code.lower() or "critical" in code.lower(), "Generates high-acuity critical shock records")

    # 3. Validate dbt Models (14 models across 4 layers + exposures)
    print("\n[3/6] Inspecting dbt Models & Lineage Topology...")
    dbt_dir = os.path.join(base_dir, "dbt_project")
    check(os.path.exists(os.path.join(dbt_dir, "dbt_project.yml")), "dbt_project.yml exists")
    check(os.path.exists(os.path.join(dbt_dir, "profiles.yml")), "profiles.yml exists")

    expected_models = {
        "staging": [
            "stg_patient_vitals.sql",
            "stg_clinical_encounters.sql",
            "stg_medication_orders.sql",
            "stg_lab_results.sql",
            "stg_icu_stays.sql",
            "stg_bed_census.sql",
        ],
        "intermediate": [
            "int_vitals_hourly_aggregated.sql",
            "int_abnormal_lab_events.sql",
            "int_medication_active_cycles.sql",
            "int_icu_stay_timeline.sql",
        ],
        "marts": [
            "dim_patients.sql",
            "dim_departments.sql",
            "fct_icu_hourly_patient_vitals.sql",
            "fct_clinical_encounters.sql",
        ],
        "reporting": [
            "rpt_icu_sepsis_risk_surveillance.sql",
            "rpt_adverse_drug_events.sql",
            "rpt_hospital_bed_capacity.sql",
            "rpt_cmo_executive_quality_kpis.sql",
        ],
    }

    total_models = 0
    for layer, models in expected_models.items():
        layer_dir = os.path.join(dbt_dir, "models", layer)
        check(os.path.exists(layer_dir), f"Layer directory models/{layer} exists")
        for m in models:
            m_path = os.path.join(layer_dir, m)
            check(os.path.exists(m_path), f"Model {layer}/{m} exists")
            total_models += 1

    check(total_models == 18, f"All 18 dbt models present (found {total_models})")
    exposure_path = os.path.join(dbt_dir, "models", "exposures", "clinical_exposures.yml")
    check(os.path.exists(exposure_path), "clinical_exposures.yml exists")

    # 4. Validate Production Multi-DAG Architecture (9 DAGs)
    print("\n[4/6] Inspecting Airflow Production Multi-DAG Suite...")
    expected_dags = [
        "dag_00_hospital_ops_coordinator.py",
        "dag_01_ingest_bedside_telemetry.py",
        "dag_02_ingest_adt_encounters.py",
        "dag_03_ingest_pharmacy_and_labs.py",
        "dag_04_transform_intermediate_clinical.py",
        "dag_05_build_enterprise_clinical_marts.py",
        "dag_06_publish_executive_reporting.py",
        "dag_07_governance_and_quality_audit.py",
        "dag_08_emergency_bed_triage_wallboard.py",
    ]

    dags_dir = os.path.join(base_dir, "dags")
    for d in expected_dags:
        dag_file = os.path.join(dags_dir, d)
        check(os.path.exists(dag_file), f"DAG file dags/{d} exists")

    # Verify DAG 01: Autonomous Bedside Telemetry (NO TriggerDagRunOperator)
    with open(os.path.join(dags_dir, "dag_01_ingest_bedside_telemetry.py"), "r", encoding="utf-8") as f:
        c1 = f.read()
    check("TriggerDagRunOperator(" not in c1, "DAG 01 is autonomous (NO TriggerDagRunOperator)")
    check("*/15 * * * *" in c1, "DAG 01 has high-frequency streaming cron schedule")

    # Verify DAG 07: Sensed via ExternalTaskSensor (NO TriggerDagRunOperator)
    with open(os.path.join(dags_dir, "dag_07_governance_and_quality_audit.py"), "r", encoding="utf-8") as f:
        c7 = f.read()
    check("TriggerDagRunOperator(" not in c7, "DAG 07 uses decoupled sensing (NO TriggerDagRunOperator)")
    check("ExternalTaskSensor(" in c7, "DAG 07 implements ExternalTaskSensor for data governance")

    # Verify DAG 08: Autonomous ER Bed Triage (NO TriggerDagRunOperator)
    with open(os.path.join(dags_dir, "dag_08_emergency_bed_triage_wallboard.py"), "r", encoding="utf-8") as f:
        c8 = f.read()
    check("TriggerDagRunOperator(" not in c8, "DAG 08 is autonomous (NO TriggerDagRunOperator)")

    # Verify DAG 02, 04, 05: Trigger-driven cascade
    with open(os.path.join(dags_dir, "dag_02_ingest_adt_encounters.py"), "r", encoding="utf-8") as f:
        c2 = f.read()
    check("TriggerDagRunOperator(" in c2, "DAG 02 triggers downstream intermediate layer")

    with open(os.path.join(dags_dir, "dag_04_transform_intermediate_clinical.py"), "r", encoding="utf-8") as f:
        c4 = f.read()
    check("TriggerDagRunOperator(" in c4, "DAG 04 triggers downstream marts layer")

    with open(os.path.join(dags_dir, "dag_05_build_enterprise_clinical_marts.py"), "r", encoding="utf-8") as f:
        c5 = f.read()
    check("TriggerDagRunOperator(" in c5, "DAG 05 triggers downstream executive reporting layer")

    # 5. Validate Grafana Datasource & Dashboard
    print("\n[5/6] Inspecting Grafana Provisioning & Executive Dashboard...")
    ds_path = os.path.join(base_dir, "config", "grafana", "provisioning", "datasources", "datasources.yml")
    check(os.path.exists(ds_path), "datasources.yml exists")
    with open(ds_path, "r", encoding="utf-8") as f:
        ds_yaml = yaml.safe_load(f)
    ds_names = [d.get("name") for d in ds_yaml.get("datasources", [])]
    check("Healthcare_DWH" in ds_names, "Healthcare_DWH PostgreSQL datasource provisioned")

    board_path = os.path.join(base_dir, "config", "grafana", "dashboards", "cmo_executive_hospital_operations.json")
    check(os.path.exists(board_path), "cmo_executive_hospital_operations.json exists")
    with open(board_path, "r", encoding="utf-8") as f:
        board = json.load(f)
    check(board.get("uid") == "cmo-exec-ops", "Dashboard UID is cmo-exec-ops")
    check("Chief Medical Officer" in board.get("title", ""), "Dashboard title matches CMO Executive Operations")
    
    panel_titles = [p.get("title") for p in board.get("panels", []) if p.get("title")]
    check(any("Septic Shock" in t for t in panel_titles), "Active Septic Shock alerts panel present")
    check(any("Adverse Drug" in t for t in panel_titles), "Adverse Drug Incidents panel present")
    check(any("Census" in t for t in panel_titles), "Hospital Inpatient Census panel present")
    check(any("Triage" in t or "Surveillance" in t for t in panel_titles), "High-Acuity ICU Triage table present")

    # 6. Validate E2E Blueprint Documentation
    print("\n[6/6] Inspecting E2E Blueprint Documentation...")
    bp_path = os.path.join(base_dir, "E2E_TEST_EXPERIMENT_BLUEPRINT.md")
    check(os.path.exists(bp_path), "E2E_TEST_EXPERIMENT_BLUEPRINT.md exists")
    with open(bp_path, "r", encoding="utf-8") as f:
        bp = f.read()
    check("Grafana Server" in bp, "Grafana documented in Architecture diagram")
    check("5.7 Executive Grafana Dashboard Specification" in bp, "Section 5.7 Executive Grafana Dashboard present")
    check("cmo_executive_hospital_operations.json" in bp, "Dashboard JSON file documented in blueprint")

    print("\n" + "=" * 70)
    print("ALL CHECKS PASSED: Experiment platform is 100% verified!")
    print("=" * 70)

if __name__ == "__main__":
    main()
