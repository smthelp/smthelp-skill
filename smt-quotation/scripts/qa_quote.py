#!/usr/bin/env python3
"""qa_quote.py - quality gate for a Southern Machinery quotation.

Usage:
  python3 qa_quote.py <quote.json> [--xlsx OUT.xlsx] [--profile assets/profile.json] [--today YYYY-MM-DD]
  python3 qa_quote.py --legacy <old quotation .xlsx/.xls>   # review an existing file (no json needed)

Prints ERROR / WARN / INFO lines (severity, location, text, fix). Exit 1 if any ERROR.
Checks: required fields, quote-number rule, dates and validity, Incoterms 2020 + named place, currency,
payment split = 100 %, warranty/delivery anchors, arithmetic, model spelling consistency, supplier terms,
English slips seen in past quotations, bank fields, photos, and in the XLSX: no volatile =NOW()/TODAY(),
company name, contact block.
"""
import argparse, datetime as dt, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INCOTERMS = {"EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"}

# phrase -> suggested fix (learned from Jason's quotations; extend in references/checklist.md + here)
SLIPS = {
    r"\bT0:": "TO: / To (letter O, not zero)",
    r"responsibled": "borne by / paid by",
    r"to be cover\b": "to be covered",
    r"receipt deposit|receipt payment|receipt 50%": "receipt of the deposit / payment",
    r"no mentioned": "not stated",
    r"\b1 years\b": "12 months / 1 year",
    r"Ex-?work SZ|Ex-work Shenzhen": "EXW Shenzhen, China (Incoterms® 2020)",
    r"Payment terms\s*[:：]\s*Payment terms": "duplicated label",
    r"Ralay": "Relay",
    r"Signa\b|Plugl": "Signal / Plug",
    r"Parament": "Parameter",
    r"outerdimension": "outer dimensions",
    r"Co Limited|Co\.,Ltd|Sales And Service|Sales and  Service": "Shenzhen Southern Machinery Sales and Service Co., Ltd.",
    r"FAX\s*:": "fax line - drop unless the number is still in use",
    r"[，：、（）]": "full-width Chinese punctuation in English text",
    r"KG/c ㎡|KG/c㎡": "kgf/cm²",
}


class Report:
    def __init__(self):
        self.rows = []

    def add(self, sev, where, text, fix=""):
        self.rows.append((sev, where, text, fix))

    def show(self):
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        groups = {}
        for sev, where, text, fix in self.rows:  # same finding in many cells -> one line
            groups.setdefault((sev, text, fix), []).append(where)
        for (sev, text, fix), wh in sorted(groups.items(), key=lambda g: order[g[0][0]]):
            loc = ", ".join(dict.fromkeys(wh))
            if len(wh) > 4:
                loc = ", ".join(list(dict.fromkeys(wh))[:4]) + f" (+{len(wh) - 4} more)"
            print(f"{sev:5} | {loc} | {text}" + (f" | fix: {fix}" if fix else ""))
        e = sum(1 for r in self.rows if r[0] == "ERROR")
        w = sum(1 for r in self.rows if r[0] == "WARN")
        print(f"\n{e} error(s), {w} warning(s)")
        return e


def norm_model(m):
    return re.sub(r"[^A-Z0-9]", "", str(m).upper())


def scan_text(rep, where, text, supplier_terms):
    for pat, fix in SLIPS.items():
        if re.search(pat, str(text)):
            rep.add("WARN", where, f"wording: '{re.search(pat, str(text)).group(0)}'", fix)
    for t in supplier_terms:
        if t and t.lower() in str(text).lower():
            rep.add("ERROR", where, f"supplier term '{t}'", "remove supplier name / model / contact")


def check_json(q, p, base, today, rep, scan=True):
    st = p.get("supplier_terms", [])
    _scan = scan_text if scan else (lambda *a, **k: None)
    for k in ("quote_no", "date", "buyer", "items", "currency", "incoterm", "place", "prepared_by"):
        if not q.get(k):
            rep.add("ERROR", k, "missing", "fill it")
    qn = q.get("quote_no", "")
    if qn and not re.match(p["quote_no_pattern"], qn):
        rep.add("WARN", "quote_no", f"'{qn}' does not follow rule", p["quote_no_rule"])
    try:
        d = dt.date.fromisoformat(q["date"])
        if qn and re.match(r"^[A-Z]{2}\d{8}$", qn) and qn[2:8] != d.strftime("%y%m%d"):
            rep.add("WARN", "quote_no/date", f"number date {qn[2:8]} != quote date {d:%y%m%d}", "align them")
        valid = dt.date.fromisoformat(q["valid_until"]) if q.get("valid_until") else d + dt.timedelta(
            days=int(q.get("valid_days", p["defaults"]["valid_days"])))
        if valid < today:
            rep.add("WARN", "validity", f"expired on {valid}", "re-issue with a new date / number")
    except Exception as e:
        rep.add("ERROR", "date", f"bad date: {e}", "use YYYY-MM-DD")
    b = q.get("buyer", {})
    for k in ("company", "attn", "email"):
        if not b.get(k):
            rep.add("ERROR", f"buyer.{k}", "missing", "fill from the inquiry")
    for k in ("address", "country", "tel"):
        if not b.get(k):
            rep.add("WARN", f"buyer.{k}", "missing", "fill from the inquiry / signature")
    if b.get("email") and not re.match(r"^[^@\s<>]+@[^@\s<>]+\.[a-z]{2,}$", b["email"], re.I):
        rep.add("ERROR", "buyer.email", f"'{b['email']}' not a clean address", "address only")
    if q.get("prepared_by") and q["prepared_by"] not in p["sales"]:
        rep.add("WARN", "prepared_by", f"'{q['prepared_by']}' not in profile.sales", "add to assets/profile.json")
    if q.get("incoterm", "").upper() not in INCOTERMS:
        rep.add("ERROR", "incoterm", f"'{q.get('incoterm')}' is not an Incoterms 2020 rule", ", ".join(sorted(INCOTERMS)))
    terms = dict(p["defaults"]["terms"]); terms.update(q.get("terms", {}))
    pay = str(terms.get("payment", ""))
    pcts = [int(x) for x in re.findall(r"(\d{1,3})\s*%", pay)]
    if pcts and sum(pcts) != 100:
        rep.add("ERROR", "terms.payment", f"split adds to {sum(pcts)} %", "make it 100 %")
    if re.search(r"after installation|after acceptance", pay, re.I) and q.get("incoterm", "").upper() in ("EXW", "FOB", "FCA"):
        rep.add("WARN", "terms.payment", "balance due after installation on an EXW/FOB sale - goods leave before you are paid",
                "balance before shipment, or L/C, or a cap on days after delivery")
    if not re.search(r"after|from|upon", str(terms.get("delivery", "")), re.I):
        rep.add("WARN", "terms.delivery", "no start point", "e.g. within 30 days after receipt of the deposit")
    if "warranty" not in q.get("terms", {}) and not scan:
        rep.add("WARN", "terms.warranty", "no warranty stated in the quotation", "add period, start point, exclusions")
    elif "warranty" not in q.get("terms", {}):
        rep.add("INFO", "terms.warranty", "profile default warranty used", "confirm it fits this product")
    elif not re.search(r"from|after", str(terms["warranty"]), re.I):
        rep.add("WARN", "terms.warranty", "no start point", "from the date of shipment / installation acceptance")
    inst = " ".join(terms["installation"]) if isinstance(terms.get("installation"), list) else str(terms.get("installation", ""))
    if re.search(r"free", inst, re.I) and not re.search(r"remote|video|on-site|air fare|travel|accommodation", inst, re.I):
        rep.add("WARN", "terms.installation", "'free installation' without saying remote or on-site / who pays travel",
                "state remote vs on-site and who covers air fare, hotel, local transport")
    for k, v in terms.items():
        _scan(rep, f"terms.{k}", " ".join(v) if isinstance(v, list) else v, st)
    # items
    seen = {}
    total = 0.0
    for i, it in enumerate(q.get("items", []), 1):
        w = f"item {i} {it.get('model', '')}"
        for k in ("model", "name", "qty", "price"):
            if it.get(k) in (None, ""):
                rep.add("ERROR", w, f"{k} missing", "fill it")
        if isinstance(it.get("price"), (int, float)) and it["price"] <= 0:
            rep.add("ERROR", w, "price <= 0", "check")
        n = norm_model(it.get("model", ""))
        if n in seen and seen[n] != it.get("model"):
            rep.add("WARN", w, f"model spelled '{it.get('model')}' and '{seen[n]}'", "use one spelling")
        seen.setdefault(n, it.get("model"))
        if it.get("photo") and not os.path.exists(os.path.join(base, it["photo"])):
            rep.add("ERROR", w, f"photo not found: {it['photo']}", "fix path")
        for s in [it.get("name", "")] + it.get("specs", []) + [o.get("name", "") for o in it.get("options", [])]:
            _scan(rep, w, s, st)
        a = it.get("qty", 1) * it.get("price", 0) + sum(o.get("qty", 1) * o.get("price", 0)
                                                         for o in it.get("options", []) if o.get("included", True))
        total += a
    for c in q.get("charges", []):
        total += c.get("qty", 1) * c.get("price", 0)
        _scan(rep, "charges", c.get("name", ""), st)
    total -= abs(q.get("discount", 0))
    if "expected_total" in q and abs(q["expected_total"] - total) > 0.005:
        rep.add("ERROR", "total", f"computed {total:,.2f} != expected {q['expected_total']:,.2f}", "find the line that differs")
    rep.add("INFO", "total", f"{q.get('currency', 'USD')} {total:,.2f}")
    for k, v in p["bank"].items():
        if "TO_CONFIRM" in str(v):
            rep.add("ERROR", f"profile.bank.{k}", "bank detail not confirmed", "Jason fills assets/profile.json once")
            break
    return total


def check_xlsx(path, p, rep):
    import openpyxl
    wb = openpyxl.load_workbook(path)
    blob = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str):
                    blob.append(v)
                    if re.search(r"(NOW|TODAY)\(\)", v, re.I):
                        rep.add("ERROR", f"{ws.title}!{c.coordinate}", f"volatile date formula {v}", "type a fixed date")
    text = "\n".join(blob)
    if p["company"] not in text:
        rep.add("ERROR", "xlsx", "registered company name not found", p["company"])
    for k in ("web", "email", "whatsapp"):
        if p[k] not in text and p[k] not in str(wb.active.oddFooter.center.text):
            rep.add("WARN", "xlsx", f"contact '{p[k]}' missing", "add the SM contact block")
    for pat, fix in SLIPS.items():
        m = re.search(pat, text)
        if m:
            rep.add("WARN", "xlsx", f"wording: '{m.group(0)}'", fix)
    for t in p.get("supplier_terms", []):
        if t and t.lower() in text.lower():
            rep.add("ERROR", "xlsx", f"supplier term '{t}'", "remove")
    pr = wb.properties
    if pr.creator and "Southern" not in pr.creator:
        rep.add("WARN", "xlsx properties", f"author '{pr.creator}'", "set to Southern Machinery")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("quote", nargs="?")
    ap.add_argument("--xlsx")
    ap.add_argument("--legacy", help="review an existing quotation file directly")
    ap.add_argument("--profile", default=os.path.join(ROOT, "assets", "profile.json"))
    ap.add_argument("--today", default=dt.date.today().isoformat())
    a = ap.parse_args()
    p = json.load(open(a.profile, encoding="utf-8"))
    rep = Report()
    today = dt.date.fromisoformat(a.today)
    if a.legacy:
        sys.path.insert(0, HERE)
        from extract_quote import extract
        q, raw = extract(a.legacy, None)
        rep.add("INFO", "legacy", f"converted {os.path.basename(a.legacy)} for review")
        for where, v in raw:
            if str(v).startswith("MODEL_MISMATCH"):
                rep.add("WARN", where, str(v).replace("MODEL_MISMATCH", "model spelled differently:"), "use one spelling")
                continue
            scan_text(rep, where, v, p.get("supplier_terms", []))
            if re.search(r"(NOW|TODAY)\(\)", str(v), re.I):
                rep.add("ERROR", where, "date is =NOW(): changes every time the file is opened", "type a fixed date")
        check_json(q, p, os.path.dirname(os.path.abspath(a.legacy)), today, rep, scan=False)
    else:
        q = json.load(open(a.quote, encoding="utf-8"))
        check_json(q, p, os.path.dirname(os.path.abspath(a.quote)), today, rep)
        if a.xlsx:
            check_xlsx(a.xlsx, p, rep)
    sys.exit(1 if rep.show() else 0)


if __name__ == "__main__":
    main()
