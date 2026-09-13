{{ config(materialized='table', tags=['executive', 'tier_1']) }}

SELECT
    m.patient_id,
    m.encounter_id,
    m.active_med_count,
    m.total_administered_dosage,
    COALESCE(l.abnormal_lab_count, 0) AS abnormal_labs
FROM {{ ref('int_medication_active_cycles') }} m
LEFT JOIN {{ ref('int_abnormal_lab_events') }} l
    ON m.patient_id = l.patient_id
WHERE m.total_administered_dosage > 1000
