"""Job file (job.json) loading, defaults and validation. The job file is the ONLY input contract.
Schema id: smt-3d-product-media/job@1  (see references/job-spec.md). Paths in a job are relative to the job file."""
import copy, json, os

SCHEMA = "smt-3d-product-media/job@1"
SKILL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

def _deep(a, b):
    out = copy.deepcopy(a)
    for k, v in b.items():
        out[k] = _deep(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else copy.deepcopy(v)
    return out

def skill_version():
    return open(os.path.join(SKILL, "VERSION")).read().strip()

class Job(dict):
    """dict with .path(rel) resolving against the job dir and .out(rel) against output.dir"""
    def path(self, p):
        if p is None: return None
        p = os.path.expanduser(str(p).replace("{skill}", SKILL))
        return p if os.path.isabs(p) else os.path.normpath(os.path.join(self["_dir"], p))
    def out(self, *p):
        d = self.path(self["output"]["dir"]); os.makedirs(d, exist_ok=True)
        return os.path.join(d, *p)
    def work(self, *p):
        d = self.out("work", *p[:-1]) if len(p) > 1 else self.out("work")
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, p[-1]) if p else d
    def wdir(self, *p):
        d = self.out("work", *p); os.makedirs(d, exist_ok=True); return d
    def name(self, variant, lang, ext):
        o = self["output"]; pr = self["product"]
        return o["name_pattern"].format(model=pr["model"], slug=pr.get("seo_slug", pr["model"]), variant=variant, LANG=lang.upper(), lang=lang) + ext

def _set(d, dotted, value):
    ks = dotted.split("."); 
    for k in ks[:-1]: d = d.setdefault(k, {})
    try: d[ks[-1]] = json.loads(value)
    except json.JSONDecodeError: d[ks[-1]] = value

def load(job_path, sets=()):
    raw = json.load(open(job_path, encoding="utf-8"))
    for s in sets: _set(raw, *s.split("=", 1))
    defaults = json.load(open(os.path.join(SKILL, "config", "defaults.json"), encoding="utf-8"))
    j = Job(_deep(defaults, raw)); j["_dir"] = os.path.dirname(os.path.abspath(job_path)); j["_file"] = os.path.abspath(job_path)
    errs, warns = validate(j)
    return j, errs, warns

def validate(j):
    E, W = [], []
    if j.get("schema") != SCHEMA:
        E.append(f"J01 schema must be '{SCHEMA}' (got {j.get('schema')!r}); see references/versioning.md for migration")
    for k in ("model",):
        if not j.get("product", {}).get(k): E.append(f"J02 product.{k} missing")
    langs = j["output"]["langs"]
    if not langs: E.append("J03 output.langs empty")
    cad = j.get("model", {}).get("cad")
    if not cad: E.append("J04 model.cad missing (STEP/STP/GLB/GLTF/OBJ/STL)")
    elif not os.path.exists(j.path(cad)): E.append(f"J05 model.cad not found: {j.path(cad)}")
    else:
        ext = os.path.splitext(cad)[1].lower()
        if ext in (".x_t", ".x_b", ".sldprt", ".sldasm", ".prt", ".asm", ".catpart"):
            E.append(f"J06 {ext} cannot be read here: export STEP AP214 (with colours) from the CAD tool")
    an = j.get("animation", {})
    for i, sc in enumerate(an.get("scenes", [])):
        if "id" not in sc or "dur" not in sc: E.append(f"J10 animation.scenes[{i}] needs id and dur")
        if sc.get("action", "idle") not in ("idle", "board_in", "feed", "insert", "board_out"):
            E.append(f"J11 scene {sc.get('id')}: unknown action {sc.get('action')}")
        for L in langs:
            if sc.get("caption") and L not in sc["caption"]: W.append(f"J12 scene {sc.get('id')}: no caption for {L}")
    for i, c in enumerate(j.get("real_clips", [])):
        if not os.path.exists(j.path(c["src"])): E.append(f"J20 real_clips[{i}] not found: {c['src']}")
        for L in langs:
            if L not in c.get("caption", {}): W.append(f"J21 real_clips[{i}] no caption for {L}")
    v = j.get("voice", {})
    if v.get("enabled"):
        for L in langs:
            if L not in v.get("voices", {}): E.append(f"J30 voice.voices.{L} missing")
            for k, ln in enumerate(v.get("lines", [])):
                if L not in ln: E.append(f"J31 voice.lines[{k}] missing {L}")
    d = j.get("deck", {})
    if d.get("enabled"):
        for L in langs:
            if not d.get("spec", {}).get(L): E.append(f"J40 deck.spec.{L} missing")
            elif not os.path.exists(j.path(d["spec"][L])): E.append(f"J41 deck spec not found: {d['spec'][L]}")
    if not j.get("disclosure"): W.append("J50 no disclosure text: add one when the 3D differs from the real machine")
    return E, W
