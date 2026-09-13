{{ config(materialized='view') }}

SELECT
    icu_stay_id,
    patient_id,
    department_id,
    icu_admit_time,
    COALESCE(icu_discharge_time, CURRENT_TIMESTAMP) AS active_end_time,
    EXTRACT(EPOCH FROM (COALESCE(icu_discharge_time, CURRENT_TIMESTAMP) - icu_admit_time)) / 3600.0 AS icu_hours
FROM {{ ref('stg_icu_stays') }}
