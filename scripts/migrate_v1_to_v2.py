#!/usr/bin/env python3
"""Migrate committed v1 JSONL batches into a separate v2 corpus."""

from __future__ import annotations

import argparse
from pathlib import Path

from residual_opportunity_scanner.migration import migrate_jsonl_file


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True, type=Path, help="v1 JSONL input; may be repeated")
    parser.add_argument("--output-dir", type=Path, default=Path("research/cases/v2"))
    parser.add_argument("--migration-date", required=True, help="ISO date recorded in migration provenance")
    args = parser.parse_args()

    if len(args.migration_date) != 10:
        raise SystemExit("--migration-date must be YYYY-MM-DD")

    total = 0
    for source in args.input:
        if not source.is_file():
            raise SystemExit(f"input does not exist: {source}")
        destination = args.output_dir / source.name
        try:
            count = migrate_jsonl_file(
                source,
                destination,
                source_label=source.as_posix(),
                migration_date=args.migration_date,
            )
        except FileExistsError:
            raise SystemExit(f"refusing to overwrite existing migration output: {destination}")
        total += count
        print(f"migrated {count}: {source} -> {destination}")

    print(f"total migrated: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
