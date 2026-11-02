#!/usr/bin/env python3
"""Validate a deck spec against config/deck-rules.json before building.

usage: validate_spec.py <spec.json> <assets_dir>
Exit 0 = OK (warnings allowed), 1 = errors. Error codes are listed in references/error-handling.md."""
import json, os, re, sys

SKILL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RULES = json.load(open(os.path.join(SKILL, "config", "deck-rules.json"), encoding="utf-8"))
L = RULES["limits"]
CJK = re.compile(r"[\u4e00-\u9fff]")

def walk_text(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ("image", "notes", "images", "before", "after", "video", "poster"): yield from walk_text(v)
    elif isinstance(o, (list, tuple)):
        for v in o: yield from walk_text(v)

def images_of(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("image", "before", "after", "poster", "video") and isinstance(v, str): yield v
            elif k in ("images", "side") and isinstance(v, list):
                for it in v:
                    if isinstance(it, list) and it and str(it[0]).lower().endswith((".jpg", ".jpeg", ".png")): yield it[0]
                    elif isinstance(it, str) and it.lower().endswith((".jpg", ".jpeg", ".png")): yield it
            else: yield from images_of(v)
    elif isinstance(o, list):
        for v in o: yield from images_of(v)

def rng(name, n, lim, errs, where):
    lo, hi = lim
    if not lo <= n <= hi: errs.append(f"E12 {where}: {name} has {n} items, allowed {lo}-{hi}")

def validate(spec, assets):
    errs, warns = [], []
    for k in ("meta", "title", "contents", "slides"):
        if k not in spec: errs.append(f"E10 missing top-level key '{k}'")
    if errs: return errs, warns
    for k in ("title", "subject", "keywords"):
        if not spec["meta"].get(k): errs.append(f"E10 meta.{k} empty")
    for k in ("eyebrow", "name", "subtitle", "tagline", "date", "image"):
        if not spec["title"].get(k): errs.append(f"E10 title.{k} empty")
    if len(spec["title"].get("name", "")) > L["deck_name_chars"]: warns.append("W20 title.name long; may wrap to 3 lines")
    c = spec["contents"]
    if not RULES["contents_items"]["min"] <= len(c) <= RULES["contents_items"]["max"]:
        errs.append(f"E12 contents has {len(c)} items")
    slides = spec["slides"]; types = [s.get("type") for s in slides]
    if not RULES["body_slides"]["min"] <= len(slides) <= RULES["body_slides"]["max"]:
        errs.append(f"E12 {len(slides)} body slides, allowed {RULES['body_slides']['min']}-{RULES['body_slides']['max']}")
    for t in RULES["required_types"]:
        if t not in types: errs.append(f"E11 required slide type '{t}' missing")
    for group in RULES["required_any_of"]:
        if not any(t in types for t in group): errs.append(f"E11 need one of {group}")
    if types and types[-1] != RULES["last_body_type"]: errs.append(f"E11 last body slide must be '{RULES['last_body_type']}'")
    for i, s in enumerate(slides, 3):
        t = s.get("type"); w = f"slide {i} ({t})"
        if t not in RULES["slide_types"]: errs.append(f"E11 {w}: unknown type"); continue
        if not s.get("title"): errs.append(f"E10 {w}: title empty")
        elif len(s["title"]) > L["title_chars"]: warns.append(f"W20 {w}: title > {L['title_chars']} chars")
        if len(s.get("lead", "")) > L["lead_chars"]: warns.append(f"W20 {w}: lead > {L['lead_chars']} chars")
        if t == "metrics":
            rng("items", len(s["items"]), L["metrics_items"], errs, w)
            for it in s["items"]:
                if len(it[0]) > L["metric_value_chars"]: warns.append(f"W21 {w}: metric value '{it[0]}' may wrap")
        if t == "pains": rng("items", len(s["items"]), L["pains_items"], errs, w)
        if t == "fab":
            rng("rows", len(s["rows"]), L["fab_rows"], errs, w)
            for r in s["rows"]:
                if len(r) != 3: errs.append(f"E13 {w}: each FAB row needs Feature, Advantage, Benefit")
        if t == "gallery": rng("items", len(s["items"]), L["gallery_items"], errs, w)
        if t == "summary": rng("items", len(s["items"]), L["summary_items"], errs, w)
        if t == "table":
            if len(s["rows"]) > L["table_rows_max"]: errs.append(f"E12 {w}: table rows > {L['table_rows_max']}, split the slide")
            for r in s["rows"]:
                if len(r) != len(s["columns"]): errs.append(f"E13 {w}: row width {len(r)} != {len(s['columns'])} columns")
        if t == "specs" and len(s["rows"]) > L["specs_rows_max"]: errs.append(f"E12 {w}: specs rows > {L['specs_rows_max']}")
        if t == "process": rng("steps", len(s["steps"]), L["process_steps"], errs, w)
    for txt in walk_text(spec):
        for bad in RULES["forbidden_text"]:
            if bad.lower() in txt.lower(): errs.append(f"E14 placeholder text '{bad}' in: {txt[:60]}")
        for bad in RULES["forbidden_brands_in_body"]:
            if bad.lower() in txt.lower(): errs.append(f"E15 third-party brand '{bad}' in: {txt[:60]}")
        if not RULES["chinese_allowed"] and CJK.search(txt): errs.append(f"E16 Chinese text in English deck: {txt[:60]}")
    for img in set(images_of(spec)):
        if not os.path.exists(os.path.join(assets, img)): errs.append(f"E17 image not found: {img}")
    return errs, warns

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    errs, warns = validate(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
    for w in warns: print("WARN ", w)
    for e in errs: print("ERROR", e)
    print("spec OK" if not errs else f"spec FAILED ({len(errs)} errors)")
    sys.exit(1 if errs else 0)
