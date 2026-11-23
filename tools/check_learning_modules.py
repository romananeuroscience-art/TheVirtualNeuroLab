#!/usr/bin/env python3
"""Validate curriculum and lesson specification metadata; no third-party dependencies."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
curriculum = json.loads((ROOT / "learning/curriculum.json").read_text())
assert curriculum["modules"], "Curriculum must contain modules"
ids = [m["id"] for m in curriculum["modules"]]
assert len(ids) == len(set(ids)), "Duplicate module IDs"
for item in curriculum["modules"]:
    assert item["objectives"], f"Missing objectives: {item['id']}"
for path in sorted((ROOT / "learning/modules").glob("*.json")):
    lesson = json.loads(path.read_text())
    assert lesson["id"] in ids, f"Unmapped lesson: {path}"
    for key in ("objective", "prerequisites", "visual", "interaction", "assessment",
                "model_disclaimer", "references", "license_status", "standards_mapping_status"):
        assert key in lesson, f"{path}: missing {key}"
    assert lesson["visual"].get("text_alternative"), f"{path}: missing accessible alternative"
    assert lesson["interaction"].get("controls"), f"{path}: missing controls"
    assert lesson["assessment"].get("feedback"), f"{path}: missing feedback"
    assert lesson["license_status"] in ("pending-review", "approved", "blocked")
print(f"Validated {len(ids)} curriculum entries and lesson specifications.")
