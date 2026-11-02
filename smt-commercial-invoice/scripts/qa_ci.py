#!/usr/bin/env python3
"""qa_ci.py - release gate for a Southern Machinery commercial invoice.

Usage: python3 qa_ci.py <ci.json> [--xlsx out/CI-*.xlsx] [--profile assets/profile.json]
Prints ERROR / WARN lines; exit code 1 while any ERROR (= not final, deliver only as DRAFT).
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INCOTERMS = {"EXW", "FCA", "FAS", "FOB", "CFR", "CIF", "CPT", "CIP", "DAP", "DPU", "DDP"}


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def walk(x):
    if isinstance(x, dict):
        for v in x.values():
            yield from walk(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk(v)
    else:
        yield x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ci")
    ap.add_argument("--xlsx")
    ap.add_argument("--profile", default=os.path.join(ROOT, "assets", "profile.json"))
    a = ap.parse_args()
    d, p = load(a.ci), load(a.profile)
    ci = p.get("ci", {})
    E, W = [], []

    # numbering and dates
    no = d.get("invoice_no", "")
    if not re.match(ci.get("invoice_no_pattern", r"^[A-Z]{2}\d{8}$"), no):
        E.append(f"invoice_no '{no}' does not follow {ci.get('invoice_no_rule')}")
    elif d.get("date") and no[2:8] != d["date"][2:4] + d["date"][5:7] + d["date"][8:10]:
        W.append(f"invoice_no {no} YYMMDD differs from date {d['date']}")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", d.get("date", "")):
        E.append("date must be ISO YYYY-MM-DD")
    if not d.get("po_no"):
        E.append("PO No. missing")

    # parties
    b = d.get("buyer", {})
    for k in ("company", "address", "country"):
        if not b.get(k):
            E.append(f"buyer.{k} missing")
    if not d.get("ship_to"):
        W.append("ship_to missing (prints buyer as ship-to?)")

    # seller / bank / brand
    if p["company"] != "Southern Machinery Sales and Service Co., Limited":
        E.append(f"seller name '{p['company']}' is not the standard name")
    if p["bank"].get("beneficiary") != p["company"]:
        E.append("bank beneficiary differs from seller company")
    for k in ("bank_name", "account_no", "swift", "bank_address"):
        if not p["bank"].get(k):
            E.append(f"bank.{k} missing in profile")
    if re.search(r"fax", json.dumps(p), re.I):
        E.append("profile contains a fax line (brand rule: no fax)")
    sib = os.path.join(os.path.dirname(ROOT), "smt-proforma-invoice", "assets", "profile.json")
    if os.path.exists(sib):
        q = load(sib)
        for k in ("company", "address", "tel", "web", "email", "whatsapp", "bank", "style"):
            if q.get(k) != p.get(k):
                E.append(f"profile.{k} differs from smt-proforma-invoice profile - sync them")

    # terms
    if d.get("incoterm") not in INCOTERMS:
        E.append(f"incoterm '{d.get('incoterm')}' is not an Incoterms 2020 rule")
    if not d.get("place"):
        E.append("Incoterm place missing")
    t = d.get("terms", {})
    if not t.get("payment"):
        E.append("terms.payment missing")
    if d.get("incoterm") in ("CIF", "CIP") and "buyer" in t.get("insurance", "").lower():
        E.append("CIF/CIP but insurance says buyer")

    # items and arithmetic
    tot = 0.0
    sample = any("no commercial value" in n.lower() for n in d.get("notes", []))
    for n, it in enumerate(d.get("items", []), 1):
        q, pr = it.get("qty"), it.get("price")
        if not isinstance(q, (int, float)) or not isinstance(pr, (int, float)):
            E.append(f"item {n}: qty/price not numeric")
            continue
        tot += q * pr
        if not it.get("unit"):
            E.append(f"item {n}: unit missing")
        elif it["unit"] not in ci.get("allowed_units", [it["unit"]]):
            W.append(f"item {n}: unit '{it['unit']}' not in allowed list")
        if not it.get("hs_code"):
            W.append(f"item {n}: H.S. code missing (customs needs it)")
        if not it.get("model"):
            W.append(f"item {n}: model missing")
        if pr == 0 and not sample:
            E.append(f"item {n}: zero price without the sample line")
    for ch in d.get("charges", []):
        tot += ch.get("qty", 1) * ch.get("price", 0)
    tot -= abs(d.get("discount", 0) or 0)
    if d.get("total_check") is None or abs(round(tot, 2) - d["total_check"]) > 0.005:
        E.append(f"total_check {d.get('total_check')} != computed {tot:,.2f}")
    if not d.get("items"):
        E.append("no items")

    # open items
    for i in d.get("issues", []):
        if i.get("level") in ("CONFIRM", "MISSING") and not i.get("resolved"):
            E.append(f"open {i['level']}: {i.get('field', i['id'])} - {i.get('note', '')}")
    if any(isinstance(v, str) and "TO_CONFIRM" in v for v in walk(d)):
        E.append("TO_CONFIRM still printed")
    if not any("dangerous" in n.lower() for n in d.get("notes", [])):
        W.append("no dangerous-goods statement in notes")

    # xlsx content
    if a.xlsx:
        try:
            from openpyxl import load_workbook
            ws = load_workbook(a.xlsx).active
            text = " ".join(str(c.value) for row in ws.iter_rows() for c in row if c.value is not None)
            if p["company"] not in text:
                E.append("xlsx: seller company not printed")
            if p["bank"]["account_no"] not in text:
                E.append("xlsx: bank account not printed")
            if "Incoterms® 2020" not in text:
                E.append("xlsx: Incoterms® 2020 not printed")
            if re.search(r"\bfax\b", text, re.I):
                E.append("xlsx: fax printed")
        except Exception as ex:  # noqa
            W.append(f"xlsx not checked: {ex}")

    for x in E:
        print("ERROR", x)
    for x in W:
        print("WARN ", x)
    print(f"{len(E)} ERROR, {len(W)} WARN -> {'FINAL OK' if not E else 'DRAFT ONLY'}")
    sys.exit(1 if E else 0)


if __name__ == "__main__":
    main()
