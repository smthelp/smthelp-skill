from __future__ import annotations

import csv
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from requests import RequestException


ROOT = Path(os.environ.get("SMTHELP_IMAGE_WORKSPACE", os.getcwd())).resolve()
PACKAGE_NAME = os.environ.get("SMTHELP_IMAGE_PACKAGE_DIR", f"seo-webp-upload-{datetime.now():%Y-%m-%d}")
PACKAGE_DIR = Path(PACKAGE_NAME)
if not PACKAGE_DIR.is_absolute():
    PACKAGE_DIR = ROOT / PACKAGE_DIR
MANIFEST_JSON = PACKAGE_DIR / "seo-webp-manifest.json"
MANIFEST_CSV = PACKAGE_DIR / "seo-webp-manifest.csv"
RESULTS_JSON = PACKAGE_DIR / "upload-results.json"
SUMMARY_MD = PACKAGE_DIR / "upload-summary.md"

BASE_URL = os.environ.get("SMTHELP_PH_BASE_URL", "https://ph.smthelp.com").rstrip("/")
JSON_URL = f"{BASE_URL}/json"
API_UPLOAD_URL = f"{BASE_URL}/api/1/upload"
ALBUM_NAME = os.environ.get(
    "SMTHELP_PH_ALBUM_NAME",
    f"southern-machinery-image-seo-webp-{datetime.now():%Y-%m-%d}",
)
ALBUM_DESCRIPTION = (
    "Southern Machinery CE, MD, ISO and RoHS certification images converted to SEO-friendly WebP files "
    "for SMT, THT, board handling and PCB assembly equipment references. Confirm the latest certificate "
    "status before customer-facing compliance claims."
)
GET_TIMEOUT = (10, 30)
POST_TIMEOUT = (10, 60)
UPLOAD_TIMEOUT = (10, 90)


def require_env(name: str, *, required: bool = True) -> str:
    value = os.environ.get(name, "")
    if required and not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def extract_auth_token(html: str) -> str | None:
    match = re.search(r"PF\.obj\.config\.auth_token\s*=\s*\"([^\"]+)\"", html)
    return match.group(1) if match else None


def read_manifest() -> list[dict[str, Any]]:
    with MANIFEST_JSON.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_manifest(rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fields:
                fields.append(key)
    with MANIFEST_JSON.open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, ensure_ascii=False, indent=2)
    with MANIFEST_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def request_json(response: requests.Response) -> dict[str, Any]:
    try:
        return response.json()
    except ValueError:
        return {
            "status_code": response.status_code,
            "status_txt": response.reason,
            "error": {
                "message": response.text[:500],
                "context": "non-json-response",
            },
        }


def logged_in(session: requests.Session) -> tuple[bool, str | None, str]:
    try:
        response = session.get(f"{BASE_URL}/upload", timeout=GET_TIMEOUT)
        token = extract_auth_token(response.text)
        is_login_page = '<body id="login"' in response.text or "Username or Email address" in response.text
        return (response.ok and not is_login_page), token, response.url
    except RequestException:
        return False, None, ""


def login(session: requests.Session, username: str, password: str) -> str | None:
    headers = {
        "Accept": "application/json, text/html",
        "Referer": f"{BASE_URL}/login",
        "X-Requested-With": "XMLHttpRequest",
    }
    for _attempt in range(3):
        try:
            login_page = session.get(f"{BASE_URL}/login", timeout=GET_TIMEOUT)
            login_page.raise_for_status()
            token = extract_auth_token(login_page.text)
            response = session.post(
                f"{BASE_URL}/login",
                data={
                    "login-subject": username,
                    "password": password,
                    "auth_token": token or "",
                },
                headers=headers,
                allow_redirects=False,
                timeout=POST_TIMEOUT,
            )
            ok, upload_token, _ = logged_in(session)
            if ok:
                return upload_token
            if response.status_code in (301, 302, 303):
                time.sleep(1)
                ok, upload_token, _ = logged_in(session)
                if ok:
                    return upload_token
        except RequestException:
            time.sleep(2)
    return None


def create_album(session: requests.Session, token: str) -> dict[str, Any] | None:
    data = {
        "action": "create-album",
        "type": "album",
        "auth_token": token,
        "album[name]": ALBUM_NAME,
        "album[description]": ALBUM_DESCRIPTION,
        "album[privacy]": "public",
        "album[password]": "",
        "album[new]": "true",
    }
    headers = {
        "Accept": "application/json",
        "Referer": f"{BASE_URL}/upload",
        "X-Requested-With": "XMLHttpRequest",
    }
    try:
        response = session.post(JSON_URL, data=data, headers=headers, timeout=POST_TIMEOUT)
        payload = request_json(response)
        if response.ok and "album" in payload:
            return payload["album"]
        return {
            "error": payload.get("error", payload),
            "status_code": response.status_code,
        }
    except RequestException as exc:
        return {
            "error": {"message": str(exc), "context": "create-album-request"},
            "status_code": 0,
        }


def upload_json(
    session: requests.Session,
    row: dict[str, Any],
    token: str,
    album_id: str | None,
    timestamp: int,
) -> dict[str, Any]:
    source = ROOT / row["webp_relative_path"]
    data = {
        "action": "upload",
        "type": "file",
        "privacy": "public",
        "timestamp": str(timestamp),
        "auth_token": token,
        "title": row["title"],
        "description": row["description"],
        "tags": row["tags"],
        "category_id": "",
        "nsfw": "0",
    }
    if album_id:
        data["album_id"] = album_id
    headers = {
        "Accept": "application/json",
        "Referer": f"{BASE_URL}/upload",
        "X-Requested-With": "XMLHttpRequest",
    }
    try:
        with source.open("rb") as handle:
            files = {"source": (row["seo_filename"], handle, "image/webp")}
            response = session.post(JSON_URL, data=data, files=files, headers=headers, timeout=UPLOAD_TIMEOUT)
        payload = request_json(response)
        payload["_http_status"] = response.status_code
        payload["_method"] = "json"
        return payload
    except RequestException as exc:
        return {
            "_http_status": 0,
            "_method": "json",
            "error": {"message": str(exc), "context": "json-upload-request"},
        }


def upload_api_v1(api_key: str, row: dict[str, Any], album_id: str | None) -> dict[str, Any]:
    source = ROOT / row["webp_relative_path"]
    data = {
        "key": api_key,
        "title": row["title"],
        "description": row["description"],
        "tags": row["tags"],
        "format": "json",
    }
    if album_id:
        data["album_id"] = album_id
    headers = {
        "Accept": "application/json",
        "X-API-Key": api_key,
    }
    try:
        with source.open("rb") as handle:
            files = {"source": (row["seo_filename"], handle, "image/webp")}
            response = requests.post(API_UPLOAD_URL, data=data, files=files, headers=headers, timeout=UPLOAD_TIMEOUT)
        payload = request_json(response)
        payload["_http_status"] = response.status_code
        payload["_method"] = "api-v1"
        return payload
    except RequestException as exc:
        return {
            "_http_status": 0,
            "_method": "api-v1",
            "error": {"message": str(exc), "context": "api-v1-upload-request"},
        }


def image_result(payload: dict[str, Any]) -> dict[str, str]:
    image = payload.get("image") or payload.get("success", {}).get("image") or {}
    album = image.get("album") or {}
    return {
        "image_id": str(image.get("id_encoded") or image.get("id") or ""),
        "viewer_url": str(image.get("url_viewer") or image.get("url_short") or image.get("url") or ""),
        "direct_url": str(image.get("url") or ""),
        "album_id": str(album.get("id_encoded") or album.get("id") or ""),
        "album_url": str(album.get("url") or ""),
        "album_name": str(album.get("name") or ""),
    }


def main() -> None:
    api_key = require_env("SMTHELP_PH_API_KEY", required=False)
    username = require_env("SMTHELP_PH_USERNAME", required=False)
    password = require_env("SMTHELP_PH_PASSWORD", required=False)
    if not api_key and not (username and password):
        raise SystemExit("Set either SMTHELP_PH_API_KEY or SMTHELP_PH_USERNAME + SMTHELP_PH_PASSWORD.")

    rows = read_manifest()
    session = requests.Session()
    session.headers.update({"User-Agent": "Southern-Machinery-SEO-WebP-Uploader/1.0"})

    auth_token: str | None = None
    preset_album_id = os.environ.get("SMTHELP_PH_ALBUM_ID", "").strip()
    preset_album_url = os.environ.get("SMTHELP_PH_ALBUM_URL", "").strip()
    album: dict[str, Any] | None = (
        {"id_encoded": preset_album_id, "url": preset_album_url, "name": ALBUM_NAME}
        if preset_album_id or preset_album_url
        else None
    )
    album_id: str | None = preset_album_id or None
    login_status = "not-attempted"
    max_uploads = int(os.environ.get("SMTHELP_PH_MAX_UPLOADS", "0") or "0")

    if username and password and not album_id:
        auth_token = login(session, username, password)
        login_status = "ok" if auth_token else "failed"
        if auth_token:
            created = create_album(session, auth_token)
            if created and "error" not in created:
                album = created
                album_id = str(album.get("id_encoded") or album.get("id") or "")
            else:
                album = created

    timestamp = int(time.time() * 1000)
    results: list[dict[str, Any]] = []
    success_count = 0
    failure_count = 0
    api_key_invalid = False
    attempted_uploads = 0

    for index, row in enumerate(rows, start=1):
        if row.get("upload_status") == "uploaded" and row.get("uploaded_url"):
            results.append({
                "index": index,
                "seo_filename": row["seo_filename"],
                "status": "skipped-existing",
                "url": row["uploaded_url"],
            })
            success_count += 1
            continue
        if max_uploads and attempted_uploads >= max_uploads:
            continue

        payload: dict[str, Any] | None = None
        attempted_uploads += 1
        if auth_token:
            payload = upload_json(session, row, auth_token, album_id, timestamp)
        if (not payload or payload.get("_http_status") != 200) and api_key and not api_key_invalid:
            payload = upload_api_v1(api_key, row, album_id)
            error = payload.get("error") if payload else None
            if isinstance(error, dict) and error.get("code") == 100 and "Invalid API v1 key" in str(error.get("message", "")):
                api_key_invalid = True

        extracted = image_result(payload or {})
        ok = bool(payload and payload.get("_http_status") == 200 and (extracted["direct_url"] or extracted["viewer_url"]))
        if ok:
            success_count += 1
            row["upload_status"] = "uploaded"
            row["uploaded_url"] = extracted["viewer_url"] or extracted["direct_url"]
            row["direct_url"] = extracted["direct_url"]
            row["image_id"] = extracted["image_id"]
            row["uploaded_album_id"] = extracted["album_id"] or album_id or ""
            row["uploaded_album_url"] = extracted["album_url"] or (str(album.get("url")) if album else "")
        else:
            failure_count += 1
            row["upload_status"] = "failed"
            row["upload_error"] = json.dumps((payload or {}).get("error", payload), ensure_ascii=False)[:1000]
            if api_key_invalid and not auth_token:
                row["upload_error"] = "Login failed and API v1 key was rejected by the server."

        results.append({
            "index": index,
            "seo_filename": row["seo_filename"],
            "status": row["upload_status"],
            "uploaded_url": row.get("uploaded_url", ""),
            "direct_url": row.get("direct_url", ""),
            "method": (payload or {}).get("_method", ""),
            "http_status": (payload or {}).get("_http_status", ""),
            "error": row.get("upload_error", ""),
        })
        write_manifest(rows)
        RESULTS_JSON.write_text(json.dumps({
            "generated": datetime.now().isoformat(timespec="seconds"),
            "base_url": BASE_URL,
            "album_name": ALBUM_NAME,
            "album": album,
            "login_status": login_status,
            "success_count": success_count,
            "failure_count": failure_count,
            "results": results,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{index}/{len(rows)}] {row['upload_status']}: {row['seo_filename']}", flush=True)
        if api_key_invalid and not auth_token:
            for remaining in rows[index:]:
                remaining["upload_status"] = "failed"
                remaining["upload_error"] = "Skipped after server rejected API v1 key and login was unavailable."
                failure_count += 1
                results.append({
                    "index": len(results) + 1,
                    "seo_filename": remaining["seo_filename"],
                    "status": "failed",
                    "uploaded_url": "",
                    "direct_url": "",
                    "method": "api-v1",
                    "http_status": 400,
                    "error": remaining["upload_error"],
                })
            break
        time.sleep(0.2)

    write_manifest(rows)
    output = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "base_url": BASE_URL,
        "album_name": ALBUM_NAME,
        "album": album,
        "login_status": login_status,
        "success_count": success_count,
        "failure_count": failure_count,
        "results": results,
    }
    RESULTS_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    album_line = ""
    if album and "error" not in album:
        album_line = f"- Album URL: {album.get('url', '')}"
    elif album:
        album_line = f"- Album creation: failed or unsupported (`{json.dumps(album.get('error', album), ensure_ascii=False)[:300]}`)"
    lines = [
        "# Upload Summary",
        "",
        f"- Generated: {output['generated']}",
        f"- Site: `{BASE_URL}`",
        f"- Album name requested: `{ALBUM_NAME}`",
        f"- Login status: `{login_status}`",
        album_line,
        f"- Uploaded: {success_count}",
        f"- Failed: {failure_count}",
        f"- Results JSON: `{RESULTS_JSON}`",
        f"- Updated manifest JSON: `{MANIFEST_JSON}`",
        f"- Updated manifest CSV: `{MANIFEST_CSV}`",
    ]
    SUMMARY_MD.write_text("\n".join(line for line in lines if line) + "\n", encoding="utf-8")
    print(json.dumps({
        "login_status": login_status,
        "album_name": ALBUM_NAME,
        "album_id": album_id,
        "album_url": album.get("url") if album and "error" not in album else "",
        "success_count": success_count,
        "failure_count": failure_count,
        "results_json": str(RESULTS_JSON),
        "summary": str(SUMMARY_MD),
    }, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
