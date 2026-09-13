{{ config(materialized=''view'') }}

SELECT
    telemetry_id,
    patient_id,
    recorded_at,
    heart_rate,
    systolic_bp,
    diastolic_bp,
    temperature_c,
    spo2_pct,
    vital_status
FROM raw.patient_vitals
WHERE vital_status = 'confirmed'
