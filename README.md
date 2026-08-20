# Synthetic EHR to FHIR readmission workflow

[![CI](https://github.com/Alfredo-Martin-Gil/ehr-fhir-readmissions/actions/workflows/ci.yml/badge.svg)](https://github.com/Alfredo-Martin-Gil/ehr-fhir-readmissions/actions/workflows/ci.yml)

A small, deterministic interoperability demonstration that converts tabular,
fully synthetic encounter data into a FHIR R4-shaped transaction Bundle and a
30-day readmission feature table.

## What is implemented

- six fictional encounters for four fictional patients;
- five explicit data-quality checks before transformation;
- deterministic Patient, Encounter and Observation resources;
- a derived encounter-level table with a mechanically calculated
  `readmitted_within_30d` label;
- tests covering quality rules, references, temporal logic and reproducibility;
- dependency-light CI on Python 3.11 and 3.12.

## Reproduce locally

```bash
python scripts/build_artifacts.py --check
python -m unittest discover -s tests -v
```

`--check` rebuilds the artefacts in memory and fails if the committed files
differ. To intentionally regenerate them after changing source data:

```bash
python scripts/build_artifacts.py
```

## Repository map

- `data/source/synthetic_encounters.csv`: authoritative fictional source rows
- `src/ehr_fhir/`: quality, transformation and serialization logic
- `fhir/synthetic_bundle.json`: generated FHIR-shaped demonstration Bundle
- `data/derived/readmission_features.csv`: generated analytical table
- `docs/data_contract.md`: field definitions and transformation rules
- `tests/`: executable evidence

## Evidence and limits

This is a software and data-engineering demonstration, not a prediction model.
The readmission label is derived from the next synthetic encounter; no
performance metric is reported. All people, identifiers, dates and observations
are fictional.

The JSON follows the project’s documented FHIR R4 subset and passes repository
structural checks. It has not been validated by an external FHIR validator or
against a national implementation guide. The project is not clinically
validated, deployed, production-ready, or evidence of improved outcomes,
regulatory compliance or medical-device status.

The previous BigQuery notebook and Power BI image are retained as historical
artefacts only; they are not part of the reproducible path and do not evidence a
live cloud pipeline or dashboard.

## Resumen en español

Demostración reproducible de interoperabilidad con datos enteramente sintéticos.
Genera recursos con estructura FHIR y una etiqueta analítica de reingreso a 30
días. No es un modelo predictivo, protocolo clínico ni sistema validado.

## License

MIT. See [LICENSE](LICENSE).
