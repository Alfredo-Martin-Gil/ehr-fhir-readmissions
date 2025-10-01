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
## Snapshot (KPI)

<p align="left">
  <img src="https://github.com/Alfredo-Martin-Gil/ehr-fhir-readmissions/blob/main/powerbi/kpi_readmissions.png?raw=true" alt="KPI 30-day readmissions" width="520">
</p>


## Cómo reproducir (rápido)

1) Abre el notebook en Colab: [notebooks/etl_ehr_to_bigquery.ipynb](notebooks/etl_ehr_to_bigquery.ipynb)
2) En la primera celda, verifica:
   - `PROJECT_ID = "apt-philosophy-473810-k9"`
   - `LOCATION = "US"`
3) Ejecuta las celdas en orden:
   - Setup BigQuery → Crear dataset `ehr` → Crear tablas y cargar muestras
   - Data Quality (5 reglas) → Crear vista `ehr.vw_readmissions` → KPI de readmisiones
4) (Opcional) Ejecuta las reglas SQL desde `sql/dq_rules.sql` en BigQuery.
5) (Opcional) Conecta Power BI a BigQuery y usa la vista `ehr.vw_readmissions` para el KPI.
