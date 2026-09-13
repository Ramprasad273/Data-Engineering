{{ config(materialized='view') }}

SELECT
    lab_id,
    patient_id,
    test_name,
    result_value,
    reference_high,
    is_abnormal,
    resulted_at
FROM raw.lab_results
