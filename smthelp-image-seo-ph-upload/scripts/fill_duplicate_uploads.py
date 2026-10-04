from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(os.environ.get("SMTHELP_IMAGE_WORKSPACE", os.getcwd())).resolve()
PACKAGE_NAME = os.environ.get("SMTHELP_IMAGE_PACKAGE_DIR", f"seo-webp-upload-{__import__('datetime').datetime.now():%Y-%m-%d}")
PACKAGE_DIR = Path(PACKAGE_NAME)
if not PACKAGE_DIR.is_absolute():
    PACKAGE_DIR = ROOT / PACKAGE_DIR
MANIFEST_JSON = PACKAGE_DIR / "seo-webp-manifest.json"
MANIFEST_CSV = PACKAGE_DIR / "seo-webp-manifest.csv"


def read_rows() -> list[dict[str, Any]]:
    return json.loads(MANIFEST_JSON.read_text(encoding="utf-8-sig"))


def write_rows(rows: list[dict[str, Any]]) -> None:
    MANIFEST_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with MANIFEST_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = read_rows()
    uploaded_by_sha: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.get("upload_status") == "uploaded" and (row.get("uploaded_url") or row.get("direct_url")):
            uploaded_by_sha.setdefault(str(row.get("sha256")), row)

    filled = 0
    for row in rows:
        if row.get("upload_status") == "uploaded":
            continue
        source = uploaded_by_sha.get(str(row.get("sha256")))
        if not source:
            continue
        row["upload_status"] = "uploaded"
        row["uploaded_url"] = source.get("uploaded_url") or source.get("direct_url") or ""
        row["direct_url"] = source.get("direct_url") or source.get("uploaded_url") or ""
        row["image_id"] = source.get("image_id", "")
        row["uploaded_album_id"] = source.get("uploaded_album_id", "")
        row["uploaded_album_url"] = source.get("uploaded_album_url", "")
        row["upload_error"] = ""
        row["duplicate_of"] = source.get("seo_filename", "")
        filled += 1

    write_rows(rows)
    print(json.dumps({
        "filled_duplicates": filled,
        "uploaded": sum(1 for row in rows if row.get("upload_status") == "uploaded"),
        "remaining": sum(1 for row in rows if row.get("upload_status") != "uploaded"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
