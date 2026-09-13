{{ config(materialized='view') }}

SELECT
    patient_id,
    DATE_TRUNC('hour', recorded_at) AS telemetry_hour,
    AVG(heart_rate) AS avg_heart_rate,
    MAX(heart_rate) AS max_heart_rate,
    MIN(systolic_bp) AS min_systolic_bp,
    AVG(systolic_bp) AS avg_systolic_bp,
    MAX(temperature_c) AS max_temperature,
    MIN(spo2_pct) AS min_spo2
FROM {{ ref('stg_patient_vitals') }}
GROUP BY patient_id, DATE_TRUNC('hour', recorded_at)
