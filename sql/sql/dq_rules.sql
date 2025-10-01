-- Null checks
SELECT COUNT(*) AS null_patient_ids FROM ehr.encounters WHERE patient_id IS NULL;

-- Value ranges (example)
SELECT COUNT(*) AS out_of_range_hr
FROM ehr.vitals
WHERE heart_rate NOT BETWEEN 20 AND 220;

-- Duplicates
SELECT patient_id, encounter_id, COUNT(*) AS c
FROM ehr.encounters
GROUP BY 1,2
HAVING c > 1;

-- Referential integrity
SELECT COUNT(*) AS missing_patient_ref
FROM ehr.encounters e
LEFT JOIN ehr.patients p ON e.patient_id = p.patient_id
WHERE p.patient_id IS NULL;

-- Timestamp consistency
SELECT COUNT(*) AS wrong_time_order
FROM ehr.encounters
WHERE discharge_time < admit_time;
