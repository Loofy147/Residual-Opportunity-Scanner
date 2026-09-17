import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from residual_opportunity_scanner.corpus_validator import validate_case
from residual_opportunity_scanner.scoring_v2 import SignalsV2, score_v2


ROOT = Path(__file__).resolve().parents[1]


def valid_case() -> dict:
    signals = SignalsV2(
        current_pressure=4,
        dependency=4,
        demand_signal=3,
        substitution_gap=3,
        intervention_specificity=3,
        reuse_leverage=4,
        differentiation=3,
        legal_friction=0,
        verification_cost=1,
        delivery_complexity=1,
    )
    scores = score_v2(signals)
    return {
        "case_id": "API-TEST-001",
        "subject": "Test API",
        "subject_type": "deprecated_api",
        "status": "verified",
        "as_of": "2026-09-17",
        "description": "Synthetic validator case.",
        "evidence": [
            {
                "evidence_id": "E1",
                "claim": "A documented migration exists.",
                "source": "https://example.com/migration",
                "status": "ESTABLISHED",
                "source_role": "PRIMARY_OFFICIAL",
            },
            {
                "evidence_id": "E2",
                "claim": "A current affected user population is documented.",
                "source": "https://example.com/users",
                "status": "ESTABLISHED",
                "source_role": "MEASUREMENT",
            },
        ],
        "signals": {
            "current_pressure": 4,
            "dependency": 4,
            "demand_signal": 3,
            "substitution_gap": 3,
            "intervention_specificity": 3,
            "reuse_leverage": 4,
            "differentiation": 3,
            "legal_friction": 0,
            "verification_cost": 1,
            "delivery_complexity": 1,
        },
        "assessment": {
            "target_user": "Maintainers of affected integrations",
            "pain_statement": "The migration requires non-trivial request changes.",
            "intervention": "Compatibility and migration diagnostics.",
            "buyer_evidence_ids": ["E2"],
            "ownership_status": "THIRD_PARTY",
            "authorization_status": "AUTHORIZED",
            "license_status": "CLEAR",
            "lawful_reuse_status": "CLEAR",
            "historical_control": False,
            "negative_control": False,
        },
        "scores": {**scores, "confidence": 0.9},
        "reuse_modes": ["migration", "automation"],
        "decision": {
            "label": "PURSUE",
            "reason": "Synthetic case with explicit current pressure and buyer/pain evidence.",
        },
    }


def test_valid_pursue_case_passes():
    schema = json.loads((ROOT / "schema/opportunity-case.v2.schema.json").read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    assert validate_case(valid_case(), validator) == []


def test_pursue_without_demand_evidence_fails():
    case = valid_case()
    case["signals"]["demand_signal"] = None
    case["scores"]["current_opportunity"] = None
    case["assessment"]["buyer_evidence_ids"] = []

    schema = json.loads((ROOT / "schema/opportunity-case.v2.schema.json").read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    messages = [issue.message for issue in validate_case(case, validator)]

    assert any("positive demand signal" in message for message in messages)
    assert any("buyer/pain evidence" in message for message in messages)


def test_unknown_is_not_zero_in_score_reproducibility():
    case = valid_case()
    case["signals"]["current_pressure"] = None
    case["scores"]["current_opportunity"] = 0.0

    schema = json.loads((ROOT / "schema/opportunity-case.v2.schema.json").read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    messages = [issue.message for issue in validate_case(case, validator)]

    assert any("unknown current_pressure" in message for message in messages)


def test_validate_corpus_reports_duplicate_ids_and_count_mismatch(tmp_path):
    case = valid_case()
    corpus_dir = tmp_path / "corpus"
    corpus_dir.mkdir()
    payload = json.dumps(case)
    (corpus_dir / "batch.jsonl").write_text(payload + "\n" + payload + "\n")

    schema = ROOT / "schema/opportunity-case.v2.schema.json"
    from residual_opportunity_scanner.corpus_validator import validate_corpus

    report = validate_corpus(
        corpus_dir,
        schema,
        target_counts={"api_dataset": 2, "namespace": 0, "web_infrastructure": 0},
        min_controls=0,
    )

    assert not report["valid"]
    assert any(error["kind"] == "identity" for error in report["errors"])


def test_validate_corpus_reports_invalid_json(tmp_path):
    corpus_dir = tmp_path / "corpus"
    corpus_dir.mkdir()
    (corpus_dir / "broken.jsonl").write_text("{not-json}\n")

    schema = ROOT / "schema/opportunity-case.v2.schema.json"
    from residual_opportunity_scanner.corpus_validator import validate_corpus

    report = validate_corpus(
        corpus_dir,
        schema,
        target_counts={"api_dataset": 0, "namespace": 0, "web_infrastructure": 0},
        min_controls=0,
    )

    assert not report["valid"]
    assert any(error["kind"] == "json" for error in report["errors"])
