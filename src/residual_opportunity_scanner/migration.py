"""Deterministic migration from the committed OpportunityCase v1 corpus to v2.

The migration is intentionally conservative: fields whose v1 semantics do not
match v2 are preserved in migration metadata and become UNKNOWN in v2.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from .scoring_v2 import SignalsV2, score_v2

DIRECT_SIGNAL_FIELDS = (
    "dependency",
    "substitution_gap",
    "reuse_leverage",
    "differentiation",
    "legal_friction",
    "verification_cost",
)
UNKNOWN_SIGNAL_FIELDS = (
    "current_pressure",
    "demand_signal",
    "intervention_specificity",
    "delivery_complexity",
)


def _migrate_signals(legacy: dict) -> tuple[dict, dict]:
    source = legacy.get("signals", {})
    signals = {name: source.get(name) for name in DIRECT_SIGNAL_FIELDS}
    signals.update({name: None for name in UNKNOWN_SIGNAL_FIELDS})

    legacy_signals = deepcopy(source)
    legacy_signals.setdefault("migration_pressure", None)
    return {**signals}, legacy_signals


def migrate_case_v1_to_v2(
    case: dict,
    *,
    source_file: str,
    source_line: int,
    migration_date: str,
) -> dict:
    """Convert one v1 case without inventing current-opportunity evidence."""

    if not case.get("case_id"):
        raise ValueError("v1 case is missing case_id")
    if not case.get("signals"):
        raise ValueError(f"{case['case_id']}: v1 case is missing signals")
    if not case.get("scores"):
        raise ValueError(f"{case['case_id']}: v1 case is missing scores")

    signals, legacy_signals = _migrate_signals(case)
    typed_signals = SignalsV2(**signals)
    scores = score_v2(typed_signals)

    legacy_scores = {
        key: case["scores"].get(key)
        for key in ("opportunity", "confidence")
        if key in case["scores"]
    }

    migrated = {
        "case_id": case["case_id"],
        "subject": case["subject"],
        "subject_type": case["subject_type"],
        "status": case.get("status", "candidate"),
        "as_of": case["as_of"],
        "description": case.get("description"),
        "evidence": deepcopy(case.get("evidence", [])),
        "signals": signals,
        "assessment": {
            "target_user": None,
            "pain_statement": None,
            "intervention": None,
            "buyer_evidence_ids": [],
            "ownership_status": "UNKNOWN",
            "authorization_status": "UNKNOWN",
            "license_status": "UNKNOWN",
            "lawful_reuse_status": "UNKNOWN",
            "historical_control": False,
            "negative_control": False,
        },
        "scores": {
            "current_opportunity": scores["current_opportunity"],
            "structural_value": scores["structural_value"],
            "friction": scores["friction"],
            "confidence": float(case["scores"].get("confidence", 0.0)),
        },
        "reuse_modes": deepcopy(case.get("reuse_modes", [])),
        "decision": {
            "label": "RESEARCH",
            "reason": "Provisional v2 migration; legacy decision is preserved only as migration metadata and requires explicit v2 reassessment.",
        },
        "migration": {
            "source_format": "opportunity-case.v1",
            "source_file": source_file,
            "source_line": source_line,
            "migration_date": migration_date,
            "legacy_status": case.get("status", "candidate"),
            "legacy_decision_label": case.get("decision", {}).get("label"),
            "legacy_decision_reason": case.get("decision", {}).get("reason"),
            "legacy_scores": legacy_scores,
            "legacy_signals": legacy_signals,
            "unknown_signal_reason": {
                "current_pressure": "v1 migration_pressure is not semantically identical to the v2 current_pressure construct; explicit reassessment required.",
                "demand_signal": "No v1 field establishes current buyer/user demand on the v2 scale.",
                "intervention_specificity": "v1 reuse_modes do not establish a concrete v2 intervention score.",
                "delivery_complexity": "No v1 field establishes v2 delivery complexity.",
            },
        },
    }

    return migrated


def migrate_jsonl_file(
    source: Path,
    destination: Path,
    *,
    source_label: str,
    migration_date: str,
) -> int:
    """Migrate one JSONL file and return the number of cases written."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    cases = []
    seen_ids: set[str] = set()

    with source.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            if not raw.strip():
                continue
            case = json.loads(raw)
            case_id = case.get("case_id")
            if case_id in seen_ids:
                raise ValueError(f"duplicate case_id {case_id!r} within {source}")
            seen_ids.add(case_id)
            cases.append(
                migrate_case_v1_to_v2(
                    case,
                    source_file=source_label,
                    source_line=line_no,
                    migration_date=migration_date,
                )
            )

    with destination.open("x", encoding="utf-8", newline="\n") as handle:
        for case in cases:
            handle.write(json.dumps(case, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    return len(cases)
