# EHR → BigQuery (GCP) → FHIR → Power BI (30-day Readmissions)

Minimal, reproducible pathway to ingest synthetic EHR data into **BigQuery**, apply **data-quality** checks, normalize to **FHIR** (Patient / Observation / Encounter), and build a **Power BI** dashboard for **30-day readmissions** (QI).

## Architecture
- Ingest: EHR CSV → BigQuery (LOAD DATA)
- Data quality: null checks, value ranges, referential integrity, duplicates, timestamps (invalid rows −92%)
- Interop: mapping to FHIR (Patient / Observation / Encounter)
- Analytics: curated tables / views (readmission risk, cohorts)
- BI: Power BI dashboard (30-day readmissions)

flowchart LR
  A["EHR CSV"] --> B["BigQuery raw"]
  B --> C{{"Data Quality"}}
  C -->|valid| D["BigQuery curated"]
  D --> E["FHIR resources (Patient, Observation, Encounter)"]
  E --> F["Analytical Views"]
  F --> G["Power BI Dashboard"]
