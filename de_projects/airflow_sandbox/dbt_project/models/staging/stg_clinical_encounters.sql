{{ config(materialized='view') }}

SELECT
    encounter_id,
    patient_id,
    department_id,
    admitted_at,
    discharged_at,
    encounter_type,
    chief_complaint
FROM raw.clinical_encounters
