{{ config(
    materialized='table',
    tags=['tier_1', 'executive', 'sepsis', 'p0']
) }}

SELECT
    f.patient_id,
    f.telemetry_hour,
    f.department_id,
    f.min_systolic_bp,
    f.max_heart_rate,
    COALESCE(l.abnormal_lab_count, 0) AS abnormal_labs,
    COALESCE(m.active_med_count, 0) AS active_medications,
    CASE
        WHEN f.min_systolic_bp < 90 AND f.max_heart_rate > 110 THEN 'IMMINENT_SEPTIC_SHOCK'
        WHEN f.min_systolic_bp < 100 OR f.max_heart_rate > 100 THEN 'MODERATE_SEPSIS_RISK'
        ELSE 'STABLE'
    END AS sepsis_clinical_tier
FROM {{ ref('fct_icu_hourly_patient_vitals') }} f
LEFT JOIN {{ ref('int_abnormal_lab_events') }} l
    ON f.patient_id = l.patient_id
LEFT JOIN {{ ref('int_medication_active_cycles') }} m
    ON f.patient_id = m.patient_id
