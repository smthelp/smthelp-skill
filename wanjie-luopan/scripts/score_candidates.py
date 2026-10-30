#!/usr/bin/env python3
"""Deterministically gate and rank open-source project candidates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


WEIGHTS = {
    "relevance": 30,
    "novelty": 15,
    "substance": 15,
    "activity": 10,
    "documentation": 10,
    "usage_evidence": 10,
    "legal_safety": 10,
}

REQUIRED = ("name", "url")
BLOCKING_LICENSES = {"incompatible", "proprietary", "forbidden"}


def bounded_rating(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a number from 0 to 5")
    rating = float(value)
    if not 0 <= rating <= 5:
        raise ValueError(f"{field} must be between 0 and 5")
    return rating


def gate(candidate: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if candidate.get("repo_exists") is False:
        reasons.append("repository does not exist")
    if candidate.get("has_code") is False:
        reasons.append("no substantive code")
    if bounded_rating(candidate.get("relevance", 0), "relevance") < 2:
        reasons.append("insufficient relevance")
    license_status = str(candidate.get("license_status", "unknown")).lower()
    if license_status in BLOCKING_LICENSES:
        reasons.append(f"license status is {license_status}")
    if candidate.get("core_dependency_available") is False:
        reasons.append("core dependency is unavailable")
    return reasons


def score(candidate: dict[str, Any]) -> float:
    total = 0.0
    for field, weight in WEIGHTS.items():
        total += bounded_rating(candidate.get(field, 0), field) / 5 * weight
    return round(total, 1)


def tier(total: float, excluded: bool) -> str:
    if excluded:
        return "excluded"
    if total >= 80:
        return "look-now"
    if total >= 65:
        return "alternative"
    if total >= 50:
        return "ideas-only"
    return "excluded"


def evaluate(candidate: dict[str, Any], index: int) -> dict[str, Any]:
    missing = [field for field in REQUIRED if not candidate.get(field)]
    if missing:
        raise ValueError(f"candidate {index} missing required fields: {', '.join(missing)}")
    reasons = gate(candidate)
    total = score(candidate)
    result = dict(candidate)
    result["score"] = total
    result["tier"] = tier(total, bool(reasons))
    result["gate_reasons"] = reasons
    return result


def load_candidates(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    candidates = payload.get("candidates") if isinstance(payload, dict) else payload
    if not isinstance(candidates, list):
        raise ValueError("input must be a JSON array or an object with a candidates array")
    if not all(isinstance(item, dict) for item in candidates):
        raise ValueError("every candidate must be a JSON object")
    return candidates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON candidate file")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args()
    try:
        evaluated = [evaluate(item, index) for index, item in enumerate(load_candidates(args.input), 1)]
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    evaluated.sort(key=lambda item: (item["tier"] == "excluded", -item["score"], item["name"].lower()))
    indent = 2 if args.pretty else None
    print(json.dumps({"candidates": evaluated}, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
