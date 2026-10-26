"""Copy deliverables into upload.local_dir/<folder_name>."""
import shutil
from pathlib import Path


def upload(files, folder_name, u, lg):
    dest = Path(u.get("local_dir", "deliveries")).expanduser() / folder_name
    dest.mkdir(parents=True, exist_ok=True)
    res = []
    for f in files:
        shutil.copy(f, dest / f.name); res.append({"name": f.name, "bytes": f.stat().st_size})
    return {"location": str(dest), "files": res}
