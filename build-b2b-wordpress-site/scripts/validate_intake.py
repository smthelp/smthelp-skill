#!/usr/bin/env python3
"""Validate a sanitized B2B WordPress project intake JSON file."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_PATHS = {
    "project.primary_goal": "Define the business outcome.",
    "brand.name": "Provide the public brand name.",
    "brand.positioning": "Provide a one-sentence market position.",
    "company.legal_name": "Provide the legal company name.",
    "market.primary_language": "Choose the launch language.",
    "market.target_regions": "Identify priority markets.",
    "market.buyer_types": "Identify target buyer types.",
    "products.priority_categories": "List launch product categories.",
    "products.estimated_count": "Estimate the number of products.",
    "technical.domain": "Provide the domain or mark it pending.",
    "scope.required_routes": "Define the launch route map.",
}

PLACEHOLDERS = {
    "",
    "pending",
    "todo",
    "tbd",
    "unknown",
    "yyyy-mm-dd",
    "examplelighting.com",
    "example lighting",
    "example manufacturing co., ltd.",
}

SECRET_TERMS = {
    "password",
    "passwd",
    "secret",
    "api_key",
    "apikey",
    "private_key",
    "application_password",
    "root_password",
    "token",
}


def get_path(data: dict[str, Any], dotted: str) -> Any:
    value: Any = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def is_missing(value: Any) -> bool:
    if value is None or value is False:
        return True
    if isinstance(value, str):
        return value.strip().lower() in PLACEHOLDERS
    if isinstance(value, (list, dict)):
        return not value
    if isinstance(value, (int, float)):
        return value <= 0
    return False


def find_secret_keys(value: Any, prefix: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            normalized = key.lower().replace("-", "_")
            if normalized in SECRET_TERMS or any(term in normalized for term in SECRET_TERMS):
                hits.append(path)
            hits.extend(find_secret_keys(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(find_secret_keys(child, f"{prefix}[{index}]"))
    return hits


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_intake.py PROJECT_INTAKE.json", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}", file=sys.stderr)
        return 2

    secret_keys = sorted(set(find_secret_keys(data)))
    if secret_keys:
        print("BLOCKED: remove credential-like fields from the intake file:")
        for key in secret_keys:
            print(f"  - {key}")
        return 2

    missing = []
    for dotted, guidance in REQUIRED_PATHS.items():
        if is_missing(get_path(data, dotted)):
            missing.append((dotted, guidance))

    print(f"Intake file: {path}")
    print(f"Required checks: {len(REQUIRED_PATHS)}")
    print(f"Ready: {len(REQUIRED_PATHS) - len(missing)}")
    print(f"Needs input: {len(missing)}")

    if missing:
        print("\nMissing or placeholder values:")
        for dotted, guidance in missing:
            print(f"  - {dotted}: {guidance}")
        return 1

    print("\nPASS: the core intake is ready for planning. Confirm access separately through a secure channel.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
