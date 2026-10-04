#!/usr/bin/env python3
"""Validate a Southern Machinery marketing brief JSON before content writing.

Usage:
    python3 scripts/validate_brief.py /path/to/marketing-brief.json

Exits 0 when the brief is complete; exits 1 and lists gaps otherwise.
"""

import json
import sys

REQUIRED_TOP = ["project", "target_customer", "platform", "content_format",
                "pain_point", "core_claim", "evidence", "style",
                "conversion_goal", "language"]

REQUIRED_CUSTOMER = ["region", "industry", "decision_role", "buying_stage"]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_brief.py <brief.json>")
        return 2

    try:
        with open(sys.argv[1], "r", encoding="utf-8") as fh:
            brief = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read brief: {exc}")
        return 1

    problems = []

    for key in REQUIRED_TOP:
        value = brief.get(key)
        if value in (None, "", []):
            problems.append(f"missing top-level field: {key}")

    customer = brief.get("target_customer") or {}
    for key in REQUIRED_CUSTOMER:
        value = customer.get(key)
        if value in (None, "", []):
            problems.append(f"missing target_customer.{key}")

    evidence = brief.get("evidence") or []
    if not evidence:
        problems.append("no evidence items: every claim needs a verified source")
    for idx, item in enumerate(evidence):
        if not item.get("source"):
            problems.append(f"evidence[{idx}] has no source")
        if not item.get("verified"):
            problems.append(f"evidence[{idx}] is not marked verified (check note / mark 待确认)")

    unverified = brief.get("unverified_items") or []
    if unverified:
        print("WARNING: unverified items must stay labeled 待确认 / to be confirmed in the final copy:")
        for item in unverified:
            print(f"  - {item}")

    if problems:
        print("BRIEF INCOMPLETE:")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print("BRIEF OK: all required fields present and evidence verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
