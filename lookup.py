#!/usr/bin/env python3
"""Zero-dependency CLI to search official US data center filing portals and validate filing-backed records.

Usage:
  python3 lookup.py list
  python3 lookup.py list --jurisdiction Texas
  python3 lookup.py list --category environmental-permit --json
  python3 lookup.py validate-record record.json
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any

SOURCES_PATH = Path(__file__).with_name("sources.json")
VALID_STAGES = {"announced", "zoning", "permitted", "under_construction"}
REQUIRED_RECORD_FIELDS = ("project_name", "state", "stage", "source_id", "filing_url", "observed_date")


def load_sources(path: Path = SOURCES_PATH) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def filter_sources(
    sources: list[dict[str, Any]],
    jurisdiction: str | None = None,
    category: str | None = None,
    query: str | None = None,
) -> list[dict[str, Any]]:
    out = sources
    if jurisdiction:
        needle = jurisdiction.lower()
        out = [s for s in out if needle in s["jurisdiction"].lower()]
    if category:
        needle = category.lower()
        out = [s for s in out if needle == s["category"].lower()]
    if query:
        needle = query.lower()
        out = [
            s
            for s in out
            if needle in s["name"].lower()
            or needle in s["proves"].lower()
            or needle in s["jurisdiction"].lower()
            or needle in s["id"].lower()
        ]
    return out


def validate_record(record: dict[str, Any], valid_source_ids: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_RECORD_FIELDS:
        val = record.get(field)
        if not isinstance(val, str) or not val.strip():
            errors.append(f"Missing or empty required field: {field}")

    stage = record.get("stage")
    if isinstance(stage, str) and stage not in VALID_STAGES:
        errors.append(f"Invalid stage '{stage}'; expected one of: {', '.join(sorted(VALID_STAGES))}")

    url = record.get("filing_url")
    if isinstance(url, str) and url.strip():
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"Invalid filing_url: {url}")

    if valid_source_ids is not None:
        sid = record.get("source_id")
        if isinstance(sid, str) and sid and sid not in valid_source_ids:
            errors.append(f"Unknown source_id '{sid}' (not in sources.json)")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search official US data center filing portals and validate records.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List or filter official public sources.")
    p_list.add_argument("--jurisdiction", help="Filter by state or jurisdiction substring (e.g. Texas, Federal).")
    p_list.add_argument("--category", help="Filter by exact category (power, utility, grid, environmental-permit, etc.).")
    p_list.add_argument("--query", "-q", help="Free-text search across name and scope.")
    p_list.add_argument("--json", action="store_true")

    p_val = sub.add_parser("validate-record", help="Validate that a JSON record links to an official filing.")
    p_val.add_argument("file", type=Path, help="Path to JSON object or JSON list of records.")
    p_val.add_argument("--strict-source", action="store_true", help="Require source_id to exist in sources.json.")

    args = parser.parse_args(argv)
    sources = load_sources()

    if args.cmd == "list":
        rows = filter_sources(sources, args.jurisdiction, args.category, args.query)
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            for r in rows:
                print(f"- [{r['id']}] {r['name']} ({r['jurisdiction']} · {r['category']})")
                print(f"  URL: {r['url']}")
                print(f"  Proves: {r['proves']}")
                print(f"  Limit:  {r['does_not_prove']}")
        return 0

    raw = json.loads(args.file.read_text(encoding="utf-8"))
    records = raw if isinstance(raw, list) else [raw]
    known_ids = {s["id"] for s in sources} if args.strict_source else None
    any_err = False
    for idx, rec in enumerate(records):
        errs = validate_record(rec, known_ids)
        if errs:
            any_err = True
            print(f"[FAIL] record #{idx}:")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"[PASS] record #{idx}: {rec['project_name']} ({rec['stage']})")
    return 1 if any_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
