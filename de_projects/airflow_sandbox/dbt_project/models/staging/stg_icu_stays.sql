{{ config(materialized='view') }}

SELECT
    encounter_id AS icu_stay_id,
    patient_id,
    department_id,
    admitted_at AS icu_admit_time,
    discharged_at AS icu_discharge_time
FROM {{ ref('stg_clinical_encounters') }}
WHERE department_id LIKE 'ICU%'
