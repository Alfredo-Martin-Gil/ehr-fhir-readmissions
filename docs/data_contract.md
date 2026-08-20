# Data contract and transformation rules

## Authoritative input

`data/source/synthetic_encounters.csv` contains fictional demonstration rows.
Identifiers use the `SYN-` prefix and do not map to people or clinical systems.

| Field | Type | Rule |
|---|---|---|
| `patient_id` | string | required; stable across a fictional patient |
| `birth_date` | ISO date | required; consistent for each patient |
| `sex` | FHIR administrative gender code | required; consistent per patient |
| `encounter_id` | string | required and unique |
| `admit_time` | ISO 8601 instant | required |
| `discharge_time` | ISO 8601 instant | required; not before admission |
| `heart_rate` | integer | required; demonstration range 20–220/min |

## Five quality gates

1. required fields are non-empty;
2. encounter identifiers are unique;
3. patient demographics are internally consistent;
4. encounter timestamps parse and discharge is not before admission;
5. heart rate is an integer in the declared demonstration range.

The range is a data-engineering plausibility rule, not a clinical decision
threshold.

## Derived label

For each encounter, rows for the same patient are ordered by admission time.
`readmitted_within_30d = 1` when the next admission occurs from zero through
30 days after discharge, inclusive; otherwise it is `0`.

This is a deterministic analytical label for synthetic data. It is not a risk
prediction, outcome claim or clinically validated definition.

## FHIR subset

The generated transaction Bundle contains Patient, Encounter and heart-rate
Observation resources. Internal subject and encounter references must resolve.
Terminology URIs and codes are included for interoperability demonstration.
Repository tests check structure and references, not full profile conformance.
