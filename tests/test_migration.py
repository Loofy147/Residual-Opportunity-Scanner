import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from residual_opportunity_scanner.migration import migrate_case_v1_to_v2
from residual_opportunity_scanner.scoring_v2 import SignalsV2, score_v2

ROOT = Path(__file__).resolve().parents[1]


def legacy_case() -> dict:
    return {
        "case_id": "API-MIGRATION-001",
        "subject": "Legacy API",
        "subject_type": "deprecated_api",
        "status": "verified",
        "as_of": "2026-09-17",
        "description": "Legacy test case.",
        "evidence": [
            {
                "evidence_id": "E1",
                "claim": "The API is deprecated.",
                "source": "https://example.com/deprecation",
                "status": "ESTABLISHED",
                "source_role": "PRIMARY_OFFICIAL",
            }
        ],
        "signals": {
            "dependency": 4,
            "migration_pressure": 5,
            "substitution_gap": 3,
            "reuse_leverage": 4,
            "differentiation": 4,
            "legal_friction": 0,
            "verification_cost": 1,
        },
        "scores": {"opportunity": 70, "confidence": 0.93},
        "reuse_modes": ["migration"],
        "decision": {"label": "PURSUE", "reason": "Legacy reason."},
    }


def test_migration_preserves_unknowns_and_legacy_metadata():
    migrated = migrate_case_v1_to_v2(
        legacy_case(),
        source_file="research/cases/m0-corpus-001.jsonl",
        source_line=1,
        migration_date="2026-09-17",
    )

    assert migrated["signals"]["current_pressure"] is None
    assert migrated["signals"]["demand_signal"] is None
    assert migrated["signals"]["intervention_specificity"] is None
    assert migrated["signals"]["delivery_complexity"] is None
    assert migrated["signals"]["dependency"] == 4
    assert migrated["migration"]["legacy_signals"]["migration_pressure"] == 5
    assert migrated["migration"]["legacy_decision_label"] == "PURSUE"
    assert migrated["decision"]["label"] == "RESEARCH"
    assert migrated["scores"]["current_opportunity"] is None

    expected = score_v2(SignalsV2(**migrated["signals"]))
    assert migrated["scores"]["structural_value"] == expected["structural_value"]
    assert migrated["scores"]["friction"] == expected["friction"]


def test_migration_does_not_mark_controls_from_legacy_labels():
    migrated = migrate_case_v1_to_v2(
        legacy_case(),
        source_file="batch.jsonl",
        source_line=3,
        migration_date="2026-09-17",
    )
    assert migrated["assessment"]["historical_control"] is False
    assert migrated["assessment"]["negative_control"] is False
    assert migrated["assessment"]["ownership_status"] == "UNKNOWN"
    assert migrated["assessment"]["lawful_reuse_status"] == "UNKNOWN"


def test_migrated_case_is_v2_schema_valid():
    schema = json.loads((ROOT / "schema/opportunity-case.v2.schema.json").read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = list(validator.iter_errors(
        migrate_case_v1_to_v2(
            legacy_case(),
            source_file="batch.jsonl",
            source_line=1,
            migration_date="2026-09-17",
        )
    ))
    assert errors == []
