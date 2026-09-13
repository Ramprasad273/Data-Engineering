{{ config(
    materialized='table',
    tags=['executive', 'board', 'tier_1']
) }}

SELECT
    CURRENT_DATE AS report_date,
    COUNT(DISTINCT s.patient_id) FILTER (WHERE s.sepsis_clinical_tier = 'IMMINENT_SEPTIC_SHOCK') AS active_septic_shock_alerts,
    COUNT(DISTINCT a.patient_id) AS adverse_drug_incidents,
    SUM(b.total_admissions) AS aggregate_patient_census
FROM {{ ref('rpt_icu_sepsis_risk_surveillance') }} s
FULL OUTER JOIN {{ ref('rpt_adverse_drug_events') }} a
    ON s.patient_id = a.patient_id
FULL OUTER JOIN {{ ref('rpt_hospital_bed_capacity') }} b
    ON s.department_id = b.department_id
