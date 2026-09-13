{{ config(materialized='table') }}

SELECT
    v.patient_id,
    v.telemetry_hour,
    v.avg_heart_rate,
    v.max_heart_rate,
    v.min_systolic_bp,
    v.avg_systolic_bp,
    i.department_id,
    i.icu_hours
FROM {{ ref('int_vitals_hourly_aggregated') }} v
JOIN {{ ref('int_icu_stay_timeline') }} i
    ON v.patient_id = i.patient_id
