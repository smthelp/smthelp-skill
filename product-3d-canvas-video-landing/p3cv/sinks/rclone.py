"""Any rclone remote (Drive, S3, WebDAV, OneDrive...): upload.remote = 'gdrive:Marketing'."""
import subprocess
from ..errors import P3VError


def upload(files, folder_name, u, lg):
    remote = u.get("remote")
    if not remote:
        raise P3VError("E_CONFIG", "upload.remote is required for sink rclone")
    dest = f"{remote.rstrip('/')}/{folder_name}"
    for f in files:
        r = subprocess.run(["rclone", "copy", str(f), dest], capture_output=True, text=True)
        if r.returncode:
            raise P3VError("E_UPLOAD", r.stderr[-400:])
        lg.info("uploaded %s", f.name)
    return {"location": dest, "files": [{"name": f.name, "bytes": f.stat().st_size} for f in files]}
