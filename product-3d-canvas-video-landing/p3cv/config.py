"""Load product.json, merge defaults, validate, and expose project paths.

The project directory (PROJ) is the folder that holds product.json. Every stage reads and writes
only inside PROJ (plus the render scratch dir), so one product = one folder, resumable at any time.
"""
import copy, json
from pathlib import Path
from .errors import P3VError

SKILL_ROOT = Path(__file__).resolve().parent.parent

DEFAULTS = {
    "brand": {
        "name": "Southern Machinery",
        "logo_url": "https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png",
        "primary": "#0056b3", "primary_dark": "#003d80", "dark_bg": "#0B132B", "accent": "#38BDF8",
        "email": "info@smthelp.com", "whatsapp": "8613602562576", "website": "https://www.smthelp.com",
        "bar_label": "",
    },
    "sources": {"drawings": [], "landing": [], "docs": []},
    "download": {"timeout": 120, "retries": 3, "max_mb": 80, "extract_base64_images": True,
                 "user_agent": "Mozilla/5.0 (p3cv)"},
    "capture": {"enabled": True, "frames": 24, "viewport": [1000, 1000], "settle_s": 30, "zoom_steps": 5,
                "zoom_delta": -200, "drag_px": 40, "click_buttons": ["Pause", "Grid"], "hide_ui": True,
                "crop": [80, 60, 920, 1000], "whiten": {"min_bright": 212, "max_chroma": 28}, "aspect": "4:3"},
    "anim": {"module": None, "global": None, "cycle_param": "CYCLE"},
    "voice": {"provider": "edge", "voice": "en-US-AndrewNeural", "rate": "-2%", "lead_in": 1.2, "gap": 0.9,
              "tail": 2.6, "lufs": -14, "true_peak": -1.5, "replacements": {}, "max_cue_chars": 42},
    "segments": [],
    "landing": {"base": None, "insert_before": None, "nav_after_href": None, "nav_after_text": None, "nav_label": "How It Works",
                "output": None, "section": {}},
    "video": {"fps": 30, "formats": ["169", "916"], "scale": 2, "jpeg_quality": 92, "crf": 19,
              "chunks": 2, "tmp_dir": None, "scenes": [], "basename": None},
    "thumbnail": {"headline_html": "", "badges": [], "subline": "", "anim_t": 0, "anim_focus": None,
                  "output": None},
    "seo": {},
    "upload": {"sink": "local", "folder_name": "{product_name} ({date})"},
    "hooks": {},
    "plugins": [],
}

REQUIRED = ["slug", "product_name", "segments", "anim.module", "anim.global"]


def _merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        out[k] = _merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def _get(d, dotted):
    for p in dotted.split("."):
        if not isinstance(d, dict) or d.get(p) in (None, "", []):
            return None
        d = d[p]
    return d


class Config:
    def __init__(self, path):
        self.path = Path(path).resolve()
        if not self.path.exists():
            raise P3VError("E_CONFIG", f"{self.path} not found", "copy config/product.example.json to your project folder")
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise P3VError("E_CONFIG", f"product.json is not valid JSON: {e}")
        self.data = _merge(DEFAULTS, raw)
        self.proj = self.path.parent
        self.validate()

    # ---- validation -------------------------------------------------------
    def validate(self):
        missing = [k for k in REQUIRED if _get(self.data, k) is None]
        if missing:
            raise P3VError("E_CONFIG", "missing required keys: " + ", ".join(missing))
        for i, s in enumerate(self.data["segments"]):
            if isinstance(s, str):
                self.data["segments"][i] = {"text": s}
            elif not isinstance(s, dict) or not s.get("text"):
                raise P3VError("E_CONFIG", f"segments[{i}] needs a 'text'")
        n = len(self.data["segments"])
        for j, sc in enumerate(self.data["video"]["scenes"]):
            if "type" not in sc or "from_segment" not in sc:
                raise P3VError("E_CONFIG", f"video.scenes[{j}] needs 'type' and 'from_segment'")
            if not 0 <= sc["from_segment"] < n:
                raise P3VError("E_CONFIG", f"video.scenes[{j}].from_segment out of range 0..{n-1}")
        for f in self.data["video"]["formats"]:
            if f not in ("169", "916"):
                raise P3VError("E_CONFIG", f"video.formats: unknown format {f} (use 169 / 916)")

    # ---- access -----------------------------------------------------------
    def __getitem__(self, k):
        return self.data[k]

    def get(self, dotted, default=None):
        v = _get(self.data, dotted)
        return default if v is None else v

    def p(self, *parts):
        """Path inside the project; parent folders are created."""
        q = self.proj.joinpath(*parts)
        q.parent.mkdir(parents=True, exist_ok=True)
        return q

    def resolve(self, rel):
        """Resolve a path from config: absolute, relative to PROJ, or relative to the skill root."""
        if rel is None:
            return None
        q = Path(rel)
        if q.is_absolute():
            return q
        for base in (self.proj, SKILL_ROOT):
            if (base / q).exists():
                return base / q
        return self.proj / q

    @property
    def slug(self):
        return self.data["slug"]

    @property
    def video_basename(self):
        return self.data["video"]["basename"] or self.slug.replace("-", "_")

    @property
    def tmp_dir(self):
        d = Path(self.data["video"]["tmp_dir"] or f"/tmp/p3cv-{self.slug}")
        d.mkdir(parents=True, exist_ok=True)
        return d
