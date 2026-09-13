{{ config(materialized='table') }}

SELECT DISTINCT 
    patient_id, 
    'ADULT_INPATIENT' AS patient_cohort 
FROM {{ ref('stg_clinical_encounters') }}
