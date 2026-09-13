{{ config(materialized='view') }}

SELECT
    department_id,
    COUNT(DISTINCT encounter_id) AS current_occupied_beds,
    CURRENT_TIMESTAMP AS snapshot_time
FROM {{ ref('stg_clinical_encounters') }}
WHERE discharged_at IS NULL
GROUP BY department_id
