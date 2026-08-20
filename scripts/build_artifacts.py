#!/usr/bin/env python3
"""Build or verify committed artefacts from the authoritative synthetic CSV."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ehr_fhir import build_artifacts, load_rows  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    bundle, features = build_artifacts(
        load_rows(ROOT / "data/source/synthetic_encounters.csv")
    )
    outputs = {
        ROOT / "fhir/synthetic_bundle.json": bundle,
        ROOT / "data/derived/readmission_features.csv": features,
    }
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, expected in outputs.items()
                 if not path.exists() or path.read_text(encoding="utf-8") != expected]
        if stale:
            print("Stale or missing artefacts: " + ", ".join(stale), file=sys.stderr)
            return 1
        print("Committed artefacts are reproducible.")
        return 0

    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
