{{ config(materialized='table') }}

SELECT DISTINCT 
    department_id, 
    'HOSPITAL_ACUTE_CARE' AS facility_type 
FROM {{ ref('stg_clinical_encounters') }}
