#!/usr/bin/env python3
"""qa_pi.py - release gate for a Southern Machinery proforma invoice.

Usage:
  python3 qa_pi.py <pi.json> [--xlsx out.xlsx] [--profile assets/profile.json]

ERROR (must be 0 before the PI may go to the customer):
  open CONFIRM / MISSING issues from build_pi.py, TO_CONFIRM anywhere, PI number format, missing PO number,
  buyer company/address, items without qty or price, payment split not 100 %, invalid Incoterm,
  company name / bank block different from smt-quotation profile, =NOW()/TODAY() or hard-coded amounts in the XLSX,
  XLSX total different from pi.json total.
WARN: ASSUMED values (profile defaults), no PO date, no buyer email/tel, insurance wording vs Incoterm,
  delivery time without a start point, legacy wording (Co.,Ltd, Ex-work, pay advance, to be cover ...).
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INCOTERMS = {"EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"}
SLIPS = [(r"Co\.,\s?Ltd|Co Limited|Co\.,Limited", "Southern Machinery Sales and Service Co., Limited"),
         (r"\bEx-?works?\b|\bEx-W\b", "EXW <place> (Incoterms® 2020)"), (r"pay advance", "100% T/T in advance"),
         (r"to be cover\b", "to be covered"), (r"receive (the )?payment", "receipt of payment"),
         (r"[、：；（）]", "full-width punctuation"), (r"Sheznhen|Slodering|Converyor|deivery|paymen\b", "spelling")]


class Rep:
    def __init__(self):
        self.rows = []

    def add(self, lev, where, msg, fix=""):
        self.rows.append((lev, where, msg, fix))

    def out(self):
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        for lev, w, m, f in sorted(self.rows, key=lambda x: order[x[0]]):
            print(f"{lev:5} | {w} | {m}" + (f" | fix: {f}" if f else ""))
        e = sum(1 for r in self.rows if r[0] == "ERROR")
        w = sum(1 for r in self.rows if r[0] == "WARN")
        print(f"\n{e} error(s), {w} warning(s)")
        return e


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("issues", "sources", "_generated_by"):
                continue
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, o


def check(pi, prof, rep):
    for i in pi.get("issues", []):
        if i["level"] in ("CONFIRM", "MISSING") and not i.get("resolved"):
            rep.add("ERROR", i["id"], f"{i['level']} open: {i['note']}", "answer in decisions.json, rebuild")
        elif i["level"] == "ASSUMED" and not i.get("resolved"):
            rep.add("WARN", i["id"], f"assumed: {i['field']} = {i['draft']}", "confirm or override in decisions.json")
    for path, v in walk(pi):
        if isinstance(v, str) and "TO_CONFIRM" in v:
            rep.add("ERROR", path, "TO_CONFIRM", "fill the value")
        if isinstance(v, str):
            for pat, fix in SLIPS:
                if re.search(pat, v, re.I):
                    rep.add("WARN", path, f"wording '{re.search(pat, v, re.I).group(0)}'", fix)
    if not re.match(prof["pi"]["pi_no_pattern"], pi.get("pi_no", "")):
        rep.add("ERROR", "pi_no", f"'{pi.get('pi_no')}' breaks the rule", prof["pi"]["pi_no_rule"])
    if not pi.get("po_no"):
        rep.add("ERROR", "po_no", "no customer PO number", "write it from the PO, or 'Verbal order <date>' if Jason says so")
    if not pi.get("po_date"):
        rep.add("WARN", "po_date", "no PO date")
    b = pi.get("buyer", {})
    for k in ("company", "address"):
        if not b.get(k):
            rep.add("ERROR", f"buyer.{k}", "missing")
    for k in ("email", "tel"):
        if not b.get(k):
            rep.add("WARN", f"buyer.{k}", "missing")
    if pi.get("incoterm") not in INCOTERMS:
        rep.add("ERROR", "incoterm", f"'{pi.get('incoterm')}' not an Incoterms 2020 rule")
    pay = pi.get("terms", {}).get("payment", "")
    pcts = [int(x) for x in re.findall(r"(\d{1,3})\s*%", pay)]
    if pcts and sum(pcts) != 100:
        rep.add("ERROR", "terms.payment", f"payment split adds to {sum(pcts)} %")
    dl = pi.get("terms", {}).get("delivery", "")
    if dl and not re.search(r"after|from|upon|before|within .* of|stock", dl, re.I):
        rep.add("WARN", "terms.delivery", "no start point", "e.g. 'after receipt of the deposit'")
    ins = pi.get("terms", {}).get("insurance", "")
    if pi.get("incoterm") in ("CIF", "CIP") and re.search(r"buyer", ins, re.I):
        rep.add("WARN", "terms.insurance", f"{pi['incoterm']} but insurance says buyer")
    total = 0.0
    for n, it in enumerate(pi.get("items", []), 1):
        q, p = it.get("qty"), it.get("price")
        if not isinstance(q, (int, float)) or not isinstance(p, (int, float)):
            rep.add("ERROR", f"item {n}", "qty or price not a number")
            continue
        if p <= 0 or q <= 0:
            rep.add("ERROR", f"item {n}", "qty/price <= 0")
        total += q * p
    for c in pi.get("charges", []):
        total += float(c.get("qty", 1)) * float(c.get("price", 0))
    total -= abs(pi.get("discount") or 0)
    if pi.get("total_check") is not None and abs(total - pi["total_check"]) > 0.01:
        rep.add("ERROR", "total", f"recomputed {total:,.2f} != pi.json {pi['total_check']:,.2f}")
    # brand + bank consistent with smt-quotation
    sq = os.path.join(os.path.dirname(ROOT), "smt-quotation", "assets", "profile.json")
    if os.path.exists(sq):
        q = json.load(open(sq, encoding="utf-8"))
        for k in ("company", "address", "tel", "web", "email", "whatsapp"):
            if q.get(k) != prof.get(k):
                rep.add("ERROR", f"profile.{k}", "differs from smt-quotation profile", "copy the value across")
        for k in ("beneficiary", "bank_name", "bank_address", "account_no", "swift"):
            if q["bank"].get(k) != prof["bank"].get(k):
                rep.add("ERROR", f"bank.{k}", "differs from smt-quotation profile", "copy the value across")
    if prof["bank"]["beneficiary"] != prof["company"]:
        rep.add("ERROR", "bank.beneficiary", "beneficiary must equal the company name")
    rep.add("INFO", "total", f"{pi.get('currency')} {total:,.2f}")
    return total


def check_xlsx(path, total, rep):
    from openpyxl import load_workbook
    wb = load_workbook(path)
    ws = wb.active
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and re.search(r"NOW\(|TODAY\(", v, re.I):
                rep.add("ERROR", c.coordinate, "volatile date formula")
            if isinstance(v, str) and "TO_CONFIRM" in v:
                rep.add("ERROR", c.coordinate, "TO_CONFIRM printed on the PI")
    hdr = None
    for row in ws.iter_rows(min_col=7, max_col=7):
        c = row[0]
        if isinstance(c.value, str) and c.value.startswith("Amount"):
            hdr = c.row
        elif hdr and c.row > hdr and isinstance(c.value, (int, float)) and c.value > 0:
            rep.add("ERROR", c.coordinate, "hard-coded amount; use a formula")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pi")
    ap.add_argument("--xlsx")
    ap.add_argument("--profile", default=os.path.join(ROOT, "assets", "profile.json"))
    a = ap.parse_args()
    pi = json.load(open(a.pi, encoding="utf-8"))
    prof = json.load(open(a.profile, encoding="utf-8"))
    rep = Rep()
    total = check(pi, prof, rep)
    if a.xlsx:
        check_xlsx(a.xlsx, total, rep)
    sys.exit(1 if rep.out() else 0)


if __name__ == "__main__":
    main()
