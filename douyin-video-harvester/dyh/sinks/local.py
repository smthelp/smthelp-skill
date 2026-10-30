import os, shutil
from .base import Sink

class LocalSink(Sink):
    """Copy into a local folder (options: {"dir": "..."})."""
    def __init__(self, cfg, dir="delivered", **kw):
        super().__init__(cfg, **kw); self.dir = dir; os.makedirs(dir, exist_ok=True)
    def existing_names(self):
        return set(os.listdir(self.dir))
    def upload(self, path):
        dst = os.path.join(self.dir, os.path.basename(path)); shutil.copy2(path, dst)
        return {"name": os.path.basename(path), "id": dst, "size": os.path.getsize(dst), "url": "file://" + os.path.abspath(dst)}
