"""Google Drive via the `gws` CLI (Google Workspace CLI). options: {"folder_id": "...", "gws": "gws"}.
Auth is whatever gws is configured with (in Hark: shell credentials provider=google)."""
import json, os, subprocess
from .base import Sink
from ..errors import DyhError

class GwsDriveSink(Sink):
    def __init__(self, cfg, folder_id=None, gws="gws", **kw):
        super().__init__(cfg, **kw)
        if not folder_id: raise DyhError("E_CONFIG", "sink.options.folder_id required for gdrive_gws")
        self.folder, self.gws = folder_id, gws
    def _list(self):
        q = f'"{self.folder}" in parents and trashed=false'
        out, token = [], None
        while True:
            params = {"q": q, "fields": "nextPageToken,files(id,name,size,webViewLink)", "pageSize": 1000}
            if token: params["pageToken"] = token
            r = subprocess.run([self.gws, "drive", "files", "list", "--params", json.dumps(params)], capture_output=True, text=True)
            if r.returncode: raise DyhError("E_UPLOAD", "list failed: " + r.stderr[-200:])
            d = json.loads(r.stdout); out += d.get("files", []); token = d.get("nextPageToken")
            if not token: return out
    def existing_names(self):
        return {f["name"] for f in self._list()}
    def upload(self, path):
        r = subprocess.run([self.gws, "drive", "+upload", path, "--parent", self.folder], capture_output=True, text=True)
        if r.returncode: raise DyhError("E_UPLOAD", f"{path}: {r.stderr[-200:]}")
        return {"name": os.path.basename(path)}
    def resolve(self, names):
        """After uploads, fetch id/size/url for the given names (one list call)."""
        m = {f["name"]: f for f in self._list()}
        return {n: {"name": n, "id": m[n]["id"], "size": int(m[n].get("size", 0)), "url": m[n].get("webViewLink", "")}
                for n in names if n in m}, len(m)
