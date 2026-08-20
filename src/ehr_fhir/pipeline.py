"""Deterministic transformation from synthetic CSV rows to FHIR-shaped JSON."""

import csv
import io
import json
from datetime import timedelta
from pathlib import Path

from .quality import parse_instant, validate_rows


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _resource_entry(resource: dict) -> dict:
    return {
        "fullUrl": f"urn:uuid:{resource['resourceType'].lower()}-{resource['id'].lower()}",
        "resource": resource,
        "request": {"method": "PUT", "url": f"{resource['resourceType']}/{resource['id']}"},
    }


def build_artifacts(rows: list[dict[str, str]]) -> tuple[str, str]:
    errors = validate_rows(rows)
    if errors:
        raise ValueError("\n".join(errors))

    entries: list[dict] = []
    patients: dict[str, dict] = {}
    by_patient: dict[str, list[dict[str, str]]] = {}

    for row in rows:
        patients.setdefault(
            row["patient_id"],
            {
                "resourceType": "Patient",
                "id": row["patient_id"],
                "identifier": [{
                    "system": "https://example.org/synthetic-patient-id",
                    "value": row["patient_id"],
                }],
                "gender": row["sex"],
                "birthDate": row["birth_date"],
            },
        )
        by_patient.setdefault(row["patient_id"], []).append(row)

    for patient_id in sorted(patients):
        entries.append(_resource_entry(patients[patient_id]))

    feature_rows: list[dict[str, str | int]] = []
    for patient_id in sorted(by_patient):
        patient_rows = sorted(by_patient[patient_id], key=lambda item: item["admit_time"])
        for position, row in enumerate(patient_rows):
            admitted = parse_instant(row["admit_time"])
            discharged = parse_instant(row["discharge_time"])
            next_admission = (
                parse_instant(patient_rows[position + 1]["admit_time"])
                if position + 1 < len(patient_rows)
                else None
            )
            readmitted = int(
                next_admission is not None
                and timedelta(0) <= next_admission - discharged <= timedelta(days=30)
            )

            encounter = {
                "resourceType": "Encounter",
                "id": row["encounter_id"],
                "status": "finished",
                "class": {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                    "code": "IMP",
                    "display": "inpatient encounter",
                },
                "subject": {"reference": f"Patient/{patient_id}"},
                "period": {"start": row["admit_time"], "end": row["discharge_time"]},
            }
            observation = {
                "resourceType": "Observation",
                "id": f"SYN-O-{row['encounter_id'].removeprefix('SYN-E')}",
                "status": "final",
                "category": [{"coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                }]}],
                "code": {"coding": [{
                    "system": "http://loinc.org",
                    "code": "8867-4",
                    "display": "Heart rate",
                }]},
                "subject": {"reference": f"Patient/{patient_id}"},
                "encounter": {"reference": f"Encounter/{row['encounter_id']}"},
                "effectiveDateTime": row["admit_time"],
                "valueQuantity": {
                    "value": int(row["heart_rate"]),
                    "unit": "beats/minute",
                    "system": "http://unitsofmeasure.org",
                    "code": "/min",
                },
            }
            entries.extend((_resource_entry(encounter), _resource_entry(observation)))
            feature_rows.append({
                "patient_id": patient_id,
                "encounter_id": row["encounter_id"],
                "admit_time": row["admit_time"],
                "discharge_time": row["discharge_time"],
                "length_of_stay_hours": int((discharged - admitted).total_seconds() // 3600),
                "readmitted_within_30d": readmitted,
            })

    bundle = {
        "resourceType": "Bundle",
        "id": "synthetic-readmissions-demo",
        "type": "transaction",
        "meta": {"tag": [{
            "system": "https://example.org/data-classification",
            "code": "synthetic",
            "display": "Fully synthetic demonstration data",
        }]},
        "entry": entries,
    }
    bundle_text = json.dumps(bundle, indent=2, sort_keys=True) + "\n"

    fieldnames = [
        "patient_id", "encounter_id", "admit_time", "discharge_time",
        "length_of_stay_hours", "readmitted_within_30d",
    ]
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(feature_rows)
    return bundle_text, buffer.getvalue()
