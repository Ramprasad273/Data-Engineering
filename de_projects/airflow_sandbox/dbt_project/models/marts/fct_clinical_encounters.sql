{{ config(materialized='table') }}

SELECT
    e.encounter_id,
    e.patient_id,
    e.department_id,
    e.admitted_at,
    e.chief_complaint
FROM {{ ref('stg_clinical_encounters') }} e
