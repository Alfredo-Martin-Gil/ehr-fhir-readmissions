"""Data-quality rules for the synthetic source table."""

from datetime import datetime


def parse_instant(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_rows(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    encounter_ids: set[str] = set()
    patient_demographics: dict[str, tuple[str, str]] = {}

    for index, row in enumerate(rows, start=2):
        required = (
            "patient_id", "birth_date", "sex", "encounter_id",
            "admit_time", "discharge_time", "heart_rate",
        )
        missing = [field for field in required if not row.get(field)]
        if missing:
            errors.append(f"row {index}: missing {', '.join(missing)}")
            continue

        if row["encounter_id"] in encounter_ids:
            errors.append(f"row {index}: duplicate encounter_id")
        encounter_ids.add(row["encounter_id"])

        demographics = (row["birth_date"], row["sex"])
        previous = patient_demographics.setdefault(row["patient_id"], demographics)
        if previous != demographics:
            errors.append(f"row {index}: inconsistent patient demographics")

        try:
            admitted = parse_instant(row["admit_time"])
            discharged = parse_instant(row["discharge_time"])
            if discharged < admitted:
                errors.append(f"row {index}: discharge precedes admission")
        except ValueError:
            errors.append(f"row {index}: invalid encounter timestamp")

        try:
            heart_rate = int(row["heart_rate"])
            if not 20 <= heart_rate <= 220:
                errors.append(f"row {index}: heart_rate outside 20..220")
        except ValueError:
            errors.append(f"row {index}: heart_rate is not an integer")

    return errors
