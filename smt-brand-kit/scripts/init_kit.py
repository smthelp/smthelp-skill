#!/usr/bin/env python3
"""Create a product kit folder.

usage: init_kit.py <kit_dir> --model X3100 --name "X-ray Counter with Inspection" [--supplier-terms "RMI,瑞茂,Sxray"]

<kit_dir>/
  sources/            supplier material as received (pdf, pptx, xlsx, jpg, mp4) - never published
  extracted/          text + images pulled by extract_sources.py
  photos/             cleaned, rebranded photos used by all outputs
  videos/             rebranded clips (logo covered, end cards trimmed, audio dropped)
  facts.json          the fact table: every value with source + evidence label  (single source of truth)
  copy.json           master marketing copy in the Southern Machinery voice (feeds every output)
  deck.json manual.json poster.json video-promo.json video-short.json   output specs
  landing/            product dir for smt-product-landing-page (product.json, blogs.json, i18n/)
  out/                generated deliverables
  kit.json            model, names, supplier terms to scrub, version log
"""
import argparse, json, os

ap = argparse.ArgumentParser()
ap.add_argument("kit"); ap.add_argument("--model", required=True); ap.add_argument("--name", required=True)
ap.add_argument("--supplier-terms", default="", help="comma list of supplier names, brands, domains, phone numbers to scrub")
ap.add_argument("--supplier-model", default="", help="supplier's own model code if it differs from the SM model")
a = ap.parse_args()
k = a.kit
for d in ["sources", "extracted", "photos", "videos", "landing/i18n", "out"]:
    os.makedirs(os.path.join(k, d), exist_ok=True)


def put(name, obj):
    p = os.path.join(k, name)
    if os.path.exists(p): print("keep", p); return
    json.dump(obj, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("new ", p)


full = f"Smart EMS {a.model} {a.name}"
put("kit.json", {"model": a.model, "product_name": full, "short_name": f"{a.model} {a.name}",
                 "supplier_model": a.supplier_model,
                 "supplier_terms": [t.strip() for t in a.supplier_terms.split(",") if t.strip()],
                 "languages": ["en", "es", "pt", "fr", "ar", "ru", "zh"],
                 "skill_version": "1.0.0", "log": []})
put("facts.json", {"_how": "One row per fact. evidence: v = Verified source (current SM/supplier doc), c = To be confirmed (conflict, old or single source), t = Concept view. Conflicting values: put both in 'values' and mark c. Never add price, lead time, warranty, payment terms, certificates, customer names.",
                   "product": {"model": a.model, "name": full, "category": "", "one_line": ""},
                   "facts": [{"key": "example_speed", "label": "Counting speed", "value": "", "unit": "", "source": "brochure p.2", "evidence": "v"}],
                   "versions": [], "conflicts": [], "photos": [], "videos": []})
put("copy.json", {"_how": "Master copy in the SM voice. Every output takes its words from here so the kit stays consistent.",
                  "tagline": "", "headline": "", "subhead": "", "one_paragraph_answer": "",
                  "pains": [{"h": "", "b": ""}], "steps": [{"h": "", "b": ""}], "benefits": [""],
                  "metrics": [{"v": "", "l": ""}], "fit": "", "before_you_order": [{"h": "", "b": ""}],
                  "faq": [{"q": "", "a": ""}], "cta": "", "evidence_note": ""})
print("kit ready:", k)
