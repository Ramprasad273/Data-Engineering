{{ config(materialized='view') }}

SELECT
    patient_id,
    encounter_id,
    COUNT(*) AS active_med_count,
    SUM(dose_mg) AS total_administered_dosage
FROM {{ ref('stg_medication_orders') }}
WHERE order_status IN ('administered', 'dispensed')
GROUP BY patient_id, encounter_id
