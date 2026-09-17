"""Strict validation for the M0 OpportunityCase v2 corpus."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

from .scoring_v2 import SignalsV2, score_v2

STRATA = {
    "api_dataset": {"deprecated_api", "dataset"},
    "namespace": {"namespace"},
    "web_infrastructure": {
        "domain", "dns_record", "certificate", "host", "service",
        "repository", "registry_entry", "web_graph_node", "endpoint", "other",
    },
}

DEFAULT_TARGETS = {"api_dataset": 40, "namespace": 30, "web_infrastructure": 30}
DEFAULT_MIN_CONTROLS = 15


@dataclass(frozen=True)
class ValidationIssue:
    kind: str
    message: str
    path: str | None = None

    def as_dict(self) -> dict[str, str | None]:
        return {"kind": self.kind, "path": self.path, "message": self.message}


def classify_stratum(case: dict) -> str:
    subject_type = case["subject_type"]
    for stratum, values in STRATA.items():
        if subject_type in values:
            return stratum
    raise ValueError(f"unsupported subject_type: {subject_type}")


def _uri_syntax_ok(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme and (parsed.netloc or parsed.scheme in {"file", "urn"}))


def _same(a: float | None, b: float | None) -> bool:
    if a is None or b is None:
        return a is b
    return abs(a - b) <= 1e-9


def validate_case(case: dict, validator: Draft202012Validator) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for error in validator.iter_errors(case):
        path = ".".join(str(item) for item in error.absolute_path) or "$"
        issues.append(ValidationIssue("schema", error.message, path))

    if issues:
        return issues

    evidence_ids = [item["evidence_id"] for item in case["evidence"]]
    if len(evidence_ids) != len(set(evidence_ids)):
        issues.append(ValidationIssue("evidence", "duplicate evidence_id values", "evidence"))

    for index, evidence in enumerate(case["evidence"]):
        if not _uri_syntax_ok(evidence["source"]):
            issues.append(ValidationIssue("evidence", "source is not a valid URI", f"evidence[{index}].source"))

    signals = SignalsV2(**case["signals"])
    computed = score_v2(signals)
    recorded = case["scores"]

    for key in ("current_opportunity", "structural_value", "friction"):
        if not _same(computed[key], recorded[key]):
            issues.append(
                ValidationIssue(
                    "score_reproducibility",
                    f"{key}: recorded={recorded[key]!r}, computed={computed[key]!r}",
                    f"scores.{key}",
                )
            )

    current_pressure = signals.current_pressure
    current_score = recorded["current_opportunity"]
    if current_pressure == 0 and current_score != 0.0:
        issues.append(ValidationIssue("invariant", "current_pressure == 0 requires current_opportunity == 0", "scores.current_opportunity"))
    if current_pressure is None and current_score is not None:
        issues.append(ValidationIssue("unknown_propagation", "unknown current_pressure requires unknown current_opportunity", "scores.current_opportunity"))

    decision = case["decision"]["label"]
    assessment = case["assessment"]
    if decision == "PURSUE":
        if current_score is None or current_score <= 0:
            issues.append(ValidationIssue("decision", "PURSUE requires positive current_opportunity", "decision.label"))
        if signals.current_pressure is None or signals.current_pressure <= 0:
            issues.append(ValidationIssue("decision", "PURSUE requires established current pressure", "signals.current_pressure"))
        if signals.demand_signal is None or signals.demand_signal <= 0:
            issues.append(ValidationIssue("decision", "PURSUE requires a positive demand signal", "signals.demand_signal"))
        if not assessment["buyer_evidence_ids"]:
            issues.append(ValidationIssue("decision", "PURSUE requires at least one buyer/pain evidence reference", "assessment.buyer_evidence_ids"))
        for field in ("target_user", "pain_statement", "intervention"):
            if not assessment[field]:
                issues.append(ValidationIssue("decision", f"PURSUE requires {field} to be established", f"assessment.{field}"))
        if assessment["ownership_status"] == "UNKNOWN":
            issues.append(ValidationIssue("legal_gate", "PURSUE requires known ownership status", "assessment.ownership_status"))
        if assessment["authorization_status"] in {"UNKNOWN", "NOT_AUTHORIZED"}:
            issues.append(ValidationIssue("legal_gate", "PURSUE requires acceptable authorization state", "assessment.authorization_status"))
        if assessment["license_status"] == "UNKNOWN":
            issues.append(ValidationIssue("legal_gate", "PURSUE requires known license state", "assessment.license_status"))
        if assessment["lawful_reuse_status"] in {"UNKNOWN", "NOT_REUSABLE"}:
            issues.append(ValidationIssue("legal_gate", "PURSUE requires lawful reuse to be clear or conditional", "assessment.lawful_reuse_status"))

    return issues


def load_cases(corpus_dir: Path) -> tuple[list[tuple[Path, int, dict]], list[dict]]:
    loaded: list[tuple[Path, int, dict]] = []
    issues: list[dict] = []
    for path in sorted(corpus_dir.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for line_no, raw in enumerate(handle, start=1):
                if not raw.strip():
                    continue
                try:
                    loaded.append((path, line_no, json.loads(raw)))
                except json.JSONDecodeError as error:
                    issues.append({
                        "file": str(path),
                        "line": line_no,
                        "kind": "json",
                        "path": None,
                        "message": f"invalid JSON: {error.msg}",
                    })
    return loaded, issues


def validate_corpus(
    corpus_dir: Path,
    schema_path: Path,
    *,
    target_counts: dict[str, int] | None = None,
    min_controls: int = DEFAULT_MIN_CONTROLS,
) -> dict:
    target_counts = target_counts or DEFAULT_TARGETS
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    issues: list[dict] = []
    seen_ids: dict[str, str] = {}
    counts = {key: 0 for key in STRATA}
    controls = 0

    cases, parse_issues = load_cases(corpus_dir)
    issues.extend(parse_issues)

    for path, line_no, case in cases:
        location = f"{path}:{line_no}"
        for issue in validate_case(case, validator):
            issues.append({"file": str(path), "line": line_no, **issue.as_dict()})

        case_id = case.get("case_id")
        if case_id:
            previous = seen_ids.get(case_id)
            if previous:
                issues.append({
                    "file": str(path),
                    "line": line_no,
                    "kind": "identity",
                    "path": "case_id",
                    "message": f"duplicate case_id {case_id!r}; first seen at {previous}",
                })
            else:
                seen_ids[case_id] = location

        if "subject_type" in case:
            try:
                counts[classify_stratum(case)] += 1
            except ValueError:
                pass

        assessment = case.get("assessment")
        if isinstance(assessment, dict) and (assessment.get("historical_control") or assessment.get("negative_control")):
            controls += 1

    total = sum(counts.values())
    expected_total = sum(target_counts.values())

    if total != expected_total:
        issues.append({"file": None, "line": None, "kind": "stratum_counts", "path": None, "message": f"expected {expected_total} cases, found {total}"})

    for stratum, expected in target_counts.items():
        actual = counts[stratum]
        if actual != expected:
            issues.append({"file": None, "line": None, "kind": "stratum_counts", "path": stratum, "message": f"expected {expected}, found {actual}"})

    if controls < min_controls:
        issues.append({"file": None, "line": None, "kind": "controls", "path": None, "message": f"required at least {min_controls} controls, found {controls}"})

    return {
        "valid": not issues,
        "total": total,
        "counts": counts,
        "controls": controls,
        "expected_counts": target_counts,
        "min_controls": min_controls,
        "errors": issues,
    }
