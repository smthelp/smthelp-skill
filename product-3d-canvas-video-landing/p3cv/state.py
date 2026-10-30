"""Stage state in PROJ/state.json: status, timestamps, outputs, error. Lets runs resume."""
import json, time
from pathlib import Path


class State:
    def __init__(self, proj: Path):
        self.file = proj / "state.json"
        self.d = json.loads(self.file.read_text()) if self.file.exists() else {}

    def save(self):
        self.file.write_text(json.dumps(self.d, indent=1, ensure_ascii=False))

    def mark(self, stage, status, **kw):
        rec = self.d.setdefault(stage, {})
        rec.update(status=status, at=time.strftime("%Y-%m-%d %H:%M:%S"), **kw)
        if status == "done":
            rec.pop("error", None)
        self.save()

    def status(self, stage):
        return self.d.get(stage, {}).get("status", "pending")

    def done(self, stage):
        return self.status(stage) == "done"
