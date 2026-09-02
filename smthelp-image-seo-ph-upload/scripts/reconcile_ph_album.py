from __future__ import annotations

import csv
import json
import os
import re
import urllib.parse
import html
from pathlib import Path
from typing import Any

import requests


ROOT = Path(os.environ.get("SMTHELP_IMAGE_WORKSPACE", os.getcwd())).resolve()
PACKAGE_NAME = os.environ.get("SMTHELP_IMAGE_PACKAGE_DIR", f"seo-webp-upload-{__import__('datetime').datetime.now():%Y-%m-%d}")
PACKAGE_DIR = Path(PACKAGE_NAME)
if not PACKAGE_DIR.is_absolute():
    PACKAGE_DIR = ROOT / PACKAGE_DIR
MANIFEST_JSON = PACKAGE_DIR / "seo-webp-manifest.json"
MANIFEST_CSV = PACKAGE_DIR / "seo-webp-manifest.csv"
RECONCILE_JSON = PACKAGE_DIR / "album-reconcile.json"


def read_rows() -> list[dict[str, Any]]:
    return json.loads(MANIFEST_JSON.read_text(encoding="utf-8-sig"))


def write_rows(rows: list[dict[str, Any]]) -> None:
    MANIFEST_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    fields: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fields:
                fields.append(key)
    with MANIFEST_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def decode_data_object(raw: str) -> dict[str, Any] | None:
    try:
        text = urllib.parse.unquote(raw)
        return json.loads(text)
    except Exception:
        return None


def extract_images(html: str) -> list[dict[str, str]]:
    images: list[dict[str, str]] = []
    for item_match in re.finditer(r'<div class="list-item[^>]+data-type="image"[^>]*>', html):
        attrs = item_match.group(0)
        attrs_double = dict(
            (key, html_unescape(value))
            for key, value in re.findall(r'([\w-]+)="([^"]*)"', attrs)
        )
        object_match = re.search(r"data-object='([^']+)'", attrs)
        obj = decode_data_object(object_match.group(1)) if object_match else None
        if not obj:
            continue
        image = obj.get("image") or {}
        title = attrs_double.get("data-title") or urllib.parse.unquote(str(image.get("title") or ""))
        images.append(
            {
                "image_id": str(attrs_double.get("data-id") or obj.get("id_encoded") or image.get("id_encoded") or ""),
                "title": title,
                "viewer_url": str(image.get("url_viewer") or image.get("url_short") or ""),
                "direct_url": str(image.get("url") or ""),
                "filename": str(image.get("filename") or ""),
                "display_url": str(image.get("display_url") or ""),
            }
        )
    return images


def html_unescape(value: str) -> str:
    return html.unescape(value)


def main() -> None:
    album_url = os.environ.get("SMTHELP_PH_ALBUM_URL", "").strip()
    album_id = os.environ.get("SMTHELP_PH_ALBUM_ID", "").strip()
    if not album_url and album_id:
        album_url = f"https://ph.smthelp.com/album/{album_id}"
    if not album_url:
        raise SystemExit("Set SMTHELP_PH_ALBUM_URL or SMTHELP_PH_ALBUM_ID.")

    response = requests.get(album_url, timeout=(10, 60))
    response.raise_for_status()
    images = extract_images(response.text)

    rows = read_rows()
    buckets: dict[str, list[dict[str, str]]] = {}
    for image in images:
        buckets.setdefault(image["title"], []).append(image)

    matched = 0
    for row in rows:
        if row.get("upload_status") == "uploaded" and row.get("uploaded_url"):
            continue
        candidates = buckets.get(str(row.get("title", "")), [])
        if not candidates:
            continue
        image = candidates.pop(0)
        row["upload_status"] = "uploaded"
        row["uploaded_url"] = image["viewer_url"] or image["direct_url"]
        row["direct_url"] = image["direct_url"]
        row["image_id"] = image["image_id"]
        row["uploaded_album_id"] = album_id
        row["uploaded_album_url"] = album_url
        row["upload_error"] = ""
        matched += 1

    write_rows(rows)
    result = {
        "album_url": album_url,
        "album_id": album_id,
        "images_found": len(images),
        "matched_to_manifest": matched,
        "remaining_not_uploaded": sum(1 for row in rows if row.get("upload_status") != "uploaded"),
        "images": images,
    }
    RECONCILE_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
