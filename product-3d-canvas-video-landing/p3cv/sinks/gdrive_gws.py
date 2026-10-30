"""Google Drive through the `gws` CLI (Google Workspace CLI; in Hark the OAuth token is injected
on the wire). Creates (or reuses) a sub-folder under upload.parent_id, uploads every file, then
verifies names + sizes by listing the folder. Re-running skips files already present with the
same size, so a failed upload can simply be retried."""
import json, subprocess
from ..errors import P3VError


def gws(args):
    r = subprocess.run(["gws", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise P3VError("E_UPLOAD", f"gws {' '.join(args[:3])}: {r.stderr.strip()[-400:]}",
                       "is the Google account connected / gws installed?")
    return json.loads(r.stdout) if r.stdout.strip().startswith(("{", "[")) else r.stdout


def upload(files, folder_name, u, lg):
    parent = u.get("parent_id")
    if not parent:
        raise P3VError("E_CONFIG", "upload.parent_id (Drive folder id) is required for sink gdrive")
    q = f"'{parent}' in parents and name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    found = gws(["drive", "files", "list", "--params", json.dumps({"q": q, "fields": "files(id,webViewLink)"})]).get("files", [])
    if found:
        fid, link = found[0]["id"], found[0].get("webViewLink")
    else:
        d = gws(["drive", "files", "create", "--json", json.dumps({"name": folder_name, "mimeType": "application/vnd.google-apps.folder",
                                                                     "parents": [parent]}), "--params", json.dumps({"fields": "id,webViewLink"})])
        fid, link = d["id"], d.get("webViewLink")
    def listing():
        return {f["name"]: int(f.get("size", 0)) for f in gws(["drive", "files", "list", "--params", json.dumps(
            {"q": f"'{fid}' in parents and trashed=false", "fields": "files(name,size)", "pageSize": 200})]).get("files", [])}
    have = listing()
    for f in files:
        if have.get(f.name) == f.stat().st_size:
            lg.info("skip %s (already uploaded)", f.name); continue
        gws(["drive", "+upload", str(f), "--parent", fid]); lg.info("uploaded %s", f.name)
    have = listing()
    missing = [f.name for f in files if have.get(f.name) != f.stat().st_size]
    if missing:
        raise P3VError("E_UPLOAD", "verification failed for: " + ", ".join(missing), "re-run upload")
    return {"location": link or fid, "folder_id": fid, "files": [{"name": f.name, "bytes": have[f.name]} for f in files]}
