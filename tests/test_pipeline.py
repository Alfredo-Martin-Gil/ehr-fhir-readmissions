import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ehr_fhir import build_artifacts, load_rows
from ehr_fhir.quality import validate_rows


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_rows(ROOT / "data/source/synthetic_encounters.csv")
        cls.bundle_text, cls.features = build_artifacts(cls.rows)
        cls.bundle = json.loads(cls.bundle_text)

    def test_source_passes_quality_rules(self):
        self.assertEqual(validate_rows(self.rows), [])

    def test_expected_resource_counts(self):
        kinds = [entry["resource"]["resourceType"] for entry in self.bundle["entry"]]
        self.assertEqual(kinds.count("Patient"), 4)
        self.assertEqual(kinds.count("Encounter"), 6)
        self.assertEqual(kinds.count("Observation"), 6)

    def test_references_resolve(self):
        resources = {
            f"{entry['resource']['resourceType']}/{entry['resource']['id']}"
            for entry in self.bundle["entry"]
        }
        for entry in self.bundle["entry"]:
            resource = entry["resource"]
            for field in ("subject", "encounter"):
                if field in resource:
                    self.assertIn(resource[field]["reference"], resources)

    def test_only_one_synthetic_30_day_readmission(self):
        self.assertEqual(self.features.count(",1\n"), 1)

    def test_build_is_deterministic(self):
        self.assertEqual(build_artifacts(self.rows), (self.bundle_text, self.features))

    def test_bad_temporal_order_is_rejected(self):
        invalid = [dict(row) for row in self.rows]
        invalid[0]["discharge_time"] = "2026-01-01T00:00:00Z"
        self.assertTrue(any("discharge precedes admission" in error
                            for error in validate_rows(invalid)))

    def test_duplicate_encounter_is_rejected(self):
        invalid = [dict(row) for row in self.rows]
        invalid[1]["encounter_id"] = invalid[0]["encounter_id"]
        self.assertTrue(any("duplicate encounter_id" in error
                            for error in validate_rows(invalid)))

    def test_artefacts_match_committed_files(self):
        self.assertEqual(
            (ROOT / "fhir/synthetic_bundle.json").read_text(encoding="utf-8"),
            self.bundle_text,
        )
        self.assertEqual(
            (ROOT / "data/derived/readmission_features.csv").read_text(encoding="utf-8"),
            self.features,
        )


if __name__ == "__main__":
    unittest.main()
