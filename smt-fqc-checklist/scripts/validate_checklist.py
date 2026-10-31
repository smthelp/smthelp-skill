#!/usr/bin/env python3
"""Quality gate for checklist.json before rendering.

Usage: python3 scripts/validate_checklist.py <checklist.json> [--glossary references/glossary.csv]
Exit 1 on any ERROR. Checks:
 - meta fields present; ids unique and ordered by section code
 - every item has zh + en item/criterion/method/source/sampling, grade in CR/MA/MI, status in C/S/T
 - S and T items carry a bilingual question; T items carry no numeric spec (no invented values)
 - C items with numbers in spec cite a document source (not only a general-practice code)
 - glossary: if a zh term appears, its fixed en term appears in the en text (飞达->Feeder ...)
 - protected tokens (model, compatible machine, brand names) are identical in zh and en
 - never-publish words (price, lead time, warranty ...) absent
"""
import argparse, csv, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEVER = ["price", "价格", "报价", "lead time", "交期", "warranty", "质保", "payment", "付款"]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("checklist")
    ap.add_argument("--glossary", default=os.path.join(HERE, "references", "glossary.csv"))
    a = ap.parse_args()
    d = json.load(open(a.checklist)); err, warn = [], []
    m = d.get("meta", {})
    for k in ("model", "product_name", "product_line", "doc_no", "doc_rev", "template_version", "sources"):
        if k not in m: err.append(f"meta.{k} missing")
    gl = list(csv.DictReader(open(a.glossary, encoding="utf-8")))
    seen = set()
    for sec in d["sections"]:
        for it in sec["items"]:
            i = it.get("id", "?")
            if i in seen: err.append(f"{i}: duplicate id")
            seen.add(i)
            if not i.startswith(sec["code"]): err.append(f"{i}: id not in section {sec['code']}")
            if it.get("grade") not in ("CR", "MA", "MI"): err.append(f"{i}: grade must be CR/MA/MI")
            st = it.get("status")
            if st not in ("C", "S", "T"): err.append(f"{i}: status must be C/S/T")
            for lang in ("zh", "en"):
                for f in ("item", "criterion", "method", "source", "sampling"):
                    if not it.get(lang, {}).get(f): err.append(f"{i}: {lang}.{f} empty")
            if st in ("S", "T") and not (it.get("question", {}).get("zh") and it.get("question", {}).get("en")):
                err.append(f"{i}: status {st} needs question.zh + question.en")
            spec = it.get("spec", {}) or {}
            nums = any(re.search(r"\d", str(spec.get(k, ""))) for k in ("nominal", "lsl", "usl"))
            if st == "T" and nums: err.append(f"{i}: TBD item must not carry numeric spec values")
            src = it.get("zh", {}).get("source", "")
            if st == "C" and nums and re.fullmatch(r"通用标准.*", src): err.append(f"{i}: confirmed numbers need a document source, not only a general-practice code")
            zh = " ".join(str(it.get("zh", {}).get(f, "")) for f in ("item", "criterion", "method"))
            en = " ".join(str(it.get("en", {}).get(f, "")) for f in ("item", "criterion", "method")).lower()
            for g in gl:
                if g.get("check") == "yes" and g["zh"] in zh and g["en"].lower() not in en:
                    warn.append(f"{i}: zh uses '{g['zh']}' but en lacks '{g['en']}'")
            for tok in [m.get("model", ""), m.get("compatible", "")] + ["JUKI", "Southern Machinery"]:
                for part in tok.split():
                    if part and (part in zh) != (part in " ".join(str(it.get('en', {}).get(f, '')) for f in ('item', 'criterion', 'method'))):
                        warn.append(f"{i}: protected token '{part}' not in both languages")
            blob = (zh + " " + en).lower()
            for w in NEVER:
                if w in blob: err.append(f"{i}: never-publish word '{w}'")
    n = len(seen); o = sum(1 for s in d["sections"] for it in s["items"] if it.get("status") in ("S", "T"))
    for w in warn: print("WARN ", w)
    for e in err: print("ERROR", e)
    print(f"{n} items, {o} open S/T, {len(err)} errors, {len(warn)} warnings")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
