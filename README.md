# EHR → BigQuery (GCP) → FHIR → Power BI (30-day Readmissions)

Demo **mínima y reproducible** para:
1) Ingerir datos EHR sintéticos a **BigQuery** con `pandas`.
2) Aplicar **5 reglas** de *data quality*.
3) Exponer una **vista analítica** con KPI de **readmisiones a 30 días**.
4) Mantener referencias a **FHIR** (Patient / Encounter / Observation) con ejemplos JSON.

## Arquitectura (resumen)
EHR CSV (synthetic) → BigQuery (raw) → Data Quality (5) → BigQuery (curated) → FHIR refs → Vista `vw_readmissions` → Power BI (KPI 30d)

**Tablas**: `patients`, `encounters`, `vitals`  
**Vista**: `ehr.vw_readmissions` (incluye `length_of_stay_min` y `readmitted_30d`)

## Estructura
