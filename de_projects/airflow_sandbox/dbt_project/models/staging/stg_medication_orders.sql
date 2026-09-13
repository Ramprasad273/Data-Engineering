{{ config(materialized='view') }}

SELECT
    order_id,
    encounter_id,
    patient_id,
    medication_name,
    dose_mg AS prescribed_dosage_amount,
    status AS order_status,
    ordered_at
FROM raw.medication_orders
WHERE status NOT IN ('cancelled', 'entered_in_error')
