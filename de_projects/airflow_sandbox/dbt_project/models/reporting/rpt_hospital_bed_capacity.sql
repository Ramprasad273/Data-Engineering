{{ config(materialized='table', tags=['operations']) }}

SELECT
    e.department_id,
    COUNT(DISTINCT e.encounter_id) AS total_admissions,
    d.facility_type
FROM {{ ref('fct_clinical_encounters') }} e
JOIN {{ ref('dim_departments') }} d
    ON e.department_id = d.department_id
GROUP BY e.department_id, d.facility_type
