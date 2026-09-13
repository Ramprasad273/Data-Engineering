{{ config(materialized='view') }}

SELECT
    patient_id,
    COUNT(*) AS abnormal_lab_count,
    MAX(resulted_at) AS last_abnormal_at
FROM {{ ref('stg_lab_results') }}
WHERE is_abnormal = TRUE
GROUP BY patient_id
