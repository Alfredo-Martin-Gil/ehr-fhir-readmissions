-- Data Quality rules (reference SQL) — ehr-fhir-readmissions
-- Proyecto: apt-philosophy-473810-k9

-- 1) Nulls en claves (encounters.patient_id)
SELECT COUNT(*) AS null_patient_ids
FROM `apt-philosophy-473810-k9.ehr.encounters`
WHERE patient_id IS NULL;

-- 2) Ranges en vitals (HR 20–220)
SELECT COUNT(*) AS out_of_range_hr
FROM `apt-philosophy-473810-k9.ehr.vitals`
WHERE heart_rate NOT BETWEEN 20 AND 220;

-- 3) Duplicates por (patient_id, encounter_id)
SELECT COUNT(*) AS dup_pairs
FROM (
  SELECT patient_id, encounter_id, COUNT(*) c
  FROM `apt-philosophy-473810-k9.ehr.encounters`
  GROUP BY 1,2
  HAVING c > 1
);

-- 4) Integridad referencial (encounters vs patients)
SELECT COUNT(*) AS missing_patient_ref
FROM `apt-philosophy-473810-k9.ehr.encounters` e
LEFT JOIN `apt-philosophy-473810-k9.ehr.patients` p
ON e.patient_id = p.patient_id
WHERE p.patient_id IS NULL;

-- 5) Orden temporal (discharge_time >= admit_time)
SELECT COUNT(*) AS wrong_time_order
FROM `apt-philosophy-473810-k9.ehr.encounters`
WHERE discharge_time < admit_time;
