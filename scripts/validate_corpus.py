#!/usr/bin/env python3
"""Validate the M0 v2 corpus against the canonical schema and scoring model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from residual_opportunity_scanner.corpus_validator import DEFAULT_MIN_CONTROLS, validate_corpus


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-dir", type=Path, default=Path("research/cases/v2"))
    parser.add_argument("--schema", type=Path, default=Path("schema/opportunity-case.v2.schema.json"))
    parser.add_argument("--min-controls", type=int, default=DEFAULT_MIN_CONTROLS)
    parser.add_argument("--expected-api-dataset", type=int, default=40)
    parser.add_argument("--expected-namespace", type=int, default=30)
    parser.add_argument("--expected-web-infrastructure", type=int, default=30)
    args = parser.parse_args()

    targets = {
        "api_dataset": args.expected_api_dataset,
        "namespace": args.expected_namespace,
        "web_infrastructure": args.expected_web_infrastructure,
    }
    report = validate_corpus(args.corpus_dir, args.schema, target_counts=targets, min_controls=args.min_controls)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
