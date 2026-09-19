#!/usr/bin/env python3
"""
Synthetic Clinical Telemetry & EHR Data Generator.
Populates PostgreSQL warehouse (healthcare_dwh) with high-acuity ICU and hospital operations data.
Supports modular sourcing: vitals, encounters, meds_and_labs, or all.
"""

import argparse
import os
import random
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import execute_batch

def get_connection():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "healthcare_dwh")
    user = os.getenv("DB_USER", "clinical_admin")
    password = os.getenv("DB_PASSWORD", "clinical_secure_password")
    
    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )

def seed_encounters(cur, patients, departments, now):
    print("  -> Seeding raw.clinical_encounters (500 records)...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.clinical_encounters (
            encounter_id VARCHAR(50) PRIMARY KEY,
            patient_id VARCHAR(50) NOT NULL,
            department_id VARCHAR(50) NOT NULL,
            admitted_at TIMESTAMP NOT NULL,
            discharged_at TIMESTAMP,
            encounter_type VARCHAR(30),
            chief_complaint VARCHAR(100)
        );
    """)
    cur.execute("TRUNCATE TABLE raw.clinical_encounters;")
    
    encounters = []
    for i in range(1, 501):
        enc_id = f"ENC_{i:05d}"
        pat_id = random.choice(patients)
        dept = random.choice(departments)
        admit = now - timedelta(days=random.randint(1, 30), hours=random.randint(0, 23))
        discharge = None if random.random() < 0.30 else (admit + timedelta(days=random.randint(1, 5)))
        encounters.append((enc_id, pat_id, dept, admit, discharge, "INPATIENT", "Telemetry Monitoring"))

    execute_batch(cur, """
        INSERT INTO raw.clinical_encounters 
        (encounter_id, patient_id, department_id, admitted_at, discharged_at, encounter_type, chief_complaint)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, encounters, page_size=1000)

def seed_vitals(cur, patients, now):
    print("  -> Seeding raw.patient_vitals (10,000 telemetry readings with critical sepsis cases)...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.patient_vitals (
            telemetry_id VARCHAR(50) PRIMARY KEY,
            patient_id VARCHAR(50) NOT NULL,
            recorded_at TIMESTAMP NOT NULL,
            heart_rate NUMERIC(5, 2),
            systolic_bp NUMERIC(5, 2),
            diastolic_bp NUMERIC(5, 2),
            temperature_c NUMERIC(4, 2),
            spo2_pct NUMERIC(5, 2),
            vital_status VARCHAR(20)
        );
    """)
    cur.execute("TRUNCATE TABLE raw.patient_vitals;")

    vitals = []
    for i in range(1, 10001):
        tel_id = f"TEL_{i:06d}"
        pat_id = random.choice(patients)
        t_time = now - timedelta(hours=random.randint(0, 120), minutes=random.randint(0, 59))
        
        # 10% septic shock cases (BP < 90, HR > 110, vital_status = 'critical')
        if random.random() < 0.10:
            hr = round(random.uniform(115.0, 160.0), 2)
            sbp = round(random.uniform(65.0, 88.0), 2)
            dbp = round(random.uniform(40.0, 60.0), 2)
            status = "critical"
        else:
            hr = round(random.uniform(62.0, 98.0), 2)
            sbp = round(random.uniform(110.0, 135.0), 2)
            dbp = round(random.uniform(70.0, 85.0), 2)
            status = "confirmed"

        temp = round(random.uniform(36.5, 39.2), 2)
        spo2 = round(random.uniform(92.0, 99.0), 2)
        vitals.append((tel_id, pat_id, t_time, hr, sbp, dbp, temp, spo2, status))

    execute_batch(cur, """
        INSERT INTO raw.patient_vitals 
        (telemetry_id, patient_id, recorded_at, heart_rate, systolic_bp, diastolic_bp, temperature_c, spo2_pct, vital_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, vitals, page_size=1000)

def seed_meds_and_labs(cur, patients, meds, med_statuses, lab_tests, now):
    print("  -> Seeding raw.medication_orders (2,000 records)...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.medication_orders (
            order_id VARCHAR(50) PRIMARY KEY,
            encounter_id VARCHAR(50),
            patient_id VARCHAR(50) NOT NULL,
            medication_name VARCHAR(100) NOT NULL,
            dose_mg NUMERIC(8, 2),
            status VARCHAR(30),
            ordered_at TIMESTAMP NOT NULL
        );
    """)
    cur.execute("TRUNCATE TABLE raw.medication_orders;")

    med_orders = []
    for i in range(1, 2001):
        order_id = f"MED_{i:05d}"
        enc_id = f"ENC_{random.randint(1, 500):05d}"
        pat_id = random.choice(patients)
        med_name = random.choice(meds)
        dosage = round(random.choice([250.0, 500.0, 750.0, 1200.0, 1500.0]), 2)
        status = random.choice(med_statuses)
        ordered_at = now - timedelta(days=random.randint(0, 14), hours=random.randint(0, 23))
        med_orders.append((order_id, enc_id, pat_id, med_name, dosage, status, ordered_at))

    execute_batch(cur, """
        INSERT INTO raw.medication_orders 
        (order_id, encounter_id, patient_id, medication_name, dose_mg, status, ordered_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, med_orders, page_size=1000)

    print("  -> Seeding raw.lab_results (1,500 records)...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.lab_results (
            lab_id VARCHAR(50) PRIMARY KEY,
            patient_id VARCHAR(50) NOT NULL,
            test_name VARCHAR(100) NOT NULL,
            result_value NUMERIC(8, 2),
            reference_high NUMERIC(8, 2),
            is_abnormal BOOLEAN,
            resulted_at TIMESTAMP NOT NULL
        );
    """)
    cur.execute("TRUNCATE TABLE raw.lab_results;")

    labs = []
    for i in range(1, 1501):
        lab_id = f"LAB_{i:05d}"
        pat_id = random.choice(patients)
        test_name, ref_high, elevated_val = random.choice(lab_tests)
        is_abnormal = (random.random() < 0.25)
        res_val = round(elevated_val if is_abnormal else random.uniform(ref_high * 0.4, ref_high * 0.95), 2)
        res_at = now - timedelta(days=random.randint(0, 10), hours=random.randint(0, 23))
        labs.append((lab_id, pat_id, test_name, res_val, ref_high, is_abnormal, res_at))

    execute_batch(cur, """
        INSERT INTO raw.lab_results 
        (lab_id, patient_id, test_name, result_value, reference_high, is_abnormal, resulted_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, labs, page_size=1000)

def main() -> None:
    parser = argparse.ArgumentParser(description="Clinical EHR & Telemetry Generator")
    parser.add_argument("--source", choices=["vitals", "encounters", "meds_and_labs", "all"], default="all",
                        help="Select clinical source domain to generate")
    args = parser.parse_args()

    print(f"[INFO] Connecting to Clinical Data Warehouse (target: {args.source})...")
    conn = get_connection()
    conn.autocommit = False
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    patients = [f"PAT_{i:04d}" for i in range(1, 101)]
    departments = ["ICU-NORTH", "ICU-SOUTH", "EMERGENCY", "CARDIAC-SURGERY", "ONCOLOGY"]
    meds = ["Vancomycin", "Norepinephrine", "Piperacillin", "Furosemide", "Heparin", "Meropenem", "Vasopressin"]
    med_statuses = ["administered", "dispensed", "pending", "administered"]
    lab_tests = [
        ("Serum Lactate", 2.0, 4.5),
        ("WBC Count", 11.0, 18.5),
        ("Serum Creatinine", 1.2, 3.4),
        ("Platelets", 150.0, 95.0),
        ("Troponin I", 0.04, 1.25)
    ]

    now = datetime.utcnow()
    random.seed(42)

    if args.source in ("all", "encounters"):
        seed_encounters(cur, patients, departments, now)

    if args.source in ("all", "vitals"):
        seed_vitals(cur, patients, now)

    if args.source in ("all", "meds_and_labs"):
        seed_meds_and_labs(cur, patients, meds, med_statuses, lab_tests, now)

    conn.commit()
    cur.close()
    conn.close()
    print(f"[SUCCESS] Seeding complete for domain: {args.source}")

if __name__ == "__main__":
    main()
