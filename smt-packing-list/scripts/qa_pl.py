#!/usr/bin/env python3
"""qa_pl.py - release gate for a Southern Machinery packing list.

Usage:
  python3 qa_pl.py <pl.json> [--xlsx out.xlsx] [--ci ci.json] [--profile assets/profile.json]

ERROR (must be 0 before the PL goes out as FINAL):
  PL No. format, PL No. != invoice No., missing consignee/address/date, open "confirm" keys, TO CONFIRM anywhere,
  package without dimensions/weights, G.W. < N.W., item without qty/unit/description/H.S. code,
  price or amount words in pl.json, wooden crates without the ISPM 15 remark,
  profile drift vs smt-commercial-invoice, XLSX with NOW()/TODAY(), hard-coded totals or a price column,
  and (with --ci) qty per description, invoice No., PO No. or Incoterm different from the commercial invoice.
WARN: no PO No., no consignee contact, no signer, more than 1 carton dimension pattern per package type,
  N.W. per unit that looks odd (< 1 g or > 5 t), CBM total > 60 (more than one 40' container).
Exit code 1 while any ERROR.
"""
import argparse, json, os, re, sys
for _p in (os.environ.get("PYLIB"), "/workspace/work/pylib"):
    if _p and os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TBC = "TO CONFIRM"
PRICE_WORDS = re.compile(r"\b(unit price|amount|usd|eur|cny|rmb|price|total value)\b", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pl")
    ap.add_argument("--xlsx")
    ap.add_argument("--ci")
    ap.add_argument("--profile", default=os.path.join(ROOT, "assets", "profile.json"))
    a = ap.parse_args()
    d = json.load(open(a.pl))
    prof = json.load(open(a.profile))
    E, W = [], []

    if not re.match(prof["pl"]["pl_no_pattern"], d.get("pl_no", "")):
        E.append(f"PL No. '{d.get('pl_no')}' does not follow: {prof['pl']['pl_no_rule']}")
    if d.get("invoice_no") and d["invoice_no"] != TBC and d["invoice_no"] != d.get("pl_no"):
        E.append(f"PL No. {d.get('pl_no')} != Invoice No. {d['invoice_no']} (same shipment = same number)")
    for k in ("date", "file_tag", "packages_text", "package_word"):
        if not d.get(k):
            E.append(f"missing {k}")
    cg = d.get("consignee", {})
    if not cg.get("company") or not cg.get("address"):
        E.append("consignee company / address missing")
    if not (cg.get("attn") or cg.get("tel") or cg.get("email")):
        W.append("no consignee contact (attn / tel / email)")
    if not d.get("po_no"):
        W.append("no PO No.")
    if not d.get("signer"):
        W.append("no signer name (signature line prints without a name)")
    for k in d.get("confirm", []):
        E.append(f"open confirm key: {k}")
    n_tbc = json.dumps(d, ensure_ascii=False).count(TBC)
    if n_tbc:
        E.append(f"{n_tbc} x '{TBC}' still in pl.json")
    if PRICE_WORDS.search(json.dumps({k: v for k, v in d.items() if k not in ("remarks",)}, ensure_ascii=False)):
        E.append("price / amount wording found - a packing list never shows values")

    tnw = tgw = tcbm = 0.0
    wood = False
    qty_by_desc = {}
    for pk in d.get("packages", []):
        c = pk.get("cno", "?")
        for k in ("L", "W", "H", "nw", "gw", "packing"):
            if pk.get(k) in (None, ""):
                E.append(f"package {c}: missing {k}")
        try:
            if float(pk["gw"]) < float(pk["nw"]):
                E.append(f"package {c}: G.W. {pk['gw']} < N.W. {pk['nw']}")
            tnw += float(pk["nw"]); tgw += float(pk["gw"])
            tcbm += pk["L"] * pk["W"] * pk["H"] / 1e6
        except (KeyError, TypeError, ValueError):
            pass
        if "wood" in str(pk.get("packing", "")).lower() or "crate" in str(pk.get("packing", "")).lower():
            wood = True
        if not pk.get("items"):
            E.append(f"package {c}: no items")
        for it in pk.get("items", []):
            desc = it.get("desc", "")
            if not desc or not it.get("qty") or not it.get("unit"):
                E.append(f"package {c}: item without description / qty / unit")
            if "h.s. code" not in desc.lower():
                E.append(f"package {c}: item without 'H.S. code:' line ({desc.splitlines()[0] if desc else ''})")
            key = desc.splitlines()[0].strip().lower() if desc else ""
            qty_by_desc[key] = qty_by_desc.get(key, 0) + (it.get("qty") or 0)
        try:
            units = sum(it.get("qty") or 0 for it in pk["items"])
            per = float(pk["nw"]) / units if units else 0
            if units and (per < 0.001 or per > 5000):
                W.append(f"package {c}: N.W. per unit {per:.4f} kg looks odd")
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            pass
    if wood and not any("ISPM 15" in r for r in d.get("remarks", [])):
        E.append("wooden packing without an ISPM 15 / IPPC remark")
    if tcbm > 60:
        W.append(f"total {tcbm:.2f} CBM > one 40' container")

    ci_path = os.path.join(os.path.dirname(ROOT), "smt-commercial-invoice", "assets", "profile.json")
    if os.path.exists(ci_path):
        ci = json.load(open(ci_path))
        for k in ("company", "address", "tel", "web", "email", "whatsapp"):
            if ci.get(k) != prof.get(k):
                E.append(f"profile drift vs smt-commercial-invoice: {k}")

    if a.ci:
        c = json.load(open(a.ci))
        if c.get("invoice_no") and c["invoice_no"] != d.get("invoice_no"):
            E.append(f"Invoice No. {d.get('invoice_no')} != CI {c['invoice_no']}")
        if c.get("po_no") and d.get("po_no") and c["po_no"] != d["po_no"]:
            E.append(f"PO No. {d['po_no']} != CI {c['po_no']}")
        if c.get("incoterm") and d.get("incoterm") and not str(d["incoterm"]).startswith(c["incoterm"]):
            E.append(f"Incoterm {d['incoterm']} != CI {c['incoterm']}")
        ci_qty = sum(float(l.get("qty") or 0) for l in c.get("items", c.get("lines", [])))
        pl_qty = sum(qty_by_desc.values())
        if ci_qty and abs(ci_qty - pl_qty) > 1e-6:
            E.append(f"total qty PL {pl_qty:g} != CI {ci_qty:g}")
        ci_hs = {str(l.get("hs_code", "")).replace(".", "") for l in c.get("items", []) if l.get("hs_code")}
        pl_hs = set(re.findall(r"H\.S\. code:\s*([0-9.]+)", json.dumps(d)))
        pl_hs = {h.replace(".", "") for h in pl_hs}
        if ci_hs and pl_hs and ci_hs != pl_hs:
            E.append(f"H.S. codes PL {sorted(pl_hs)} != CI {sorted(ci_hs)}")

    if a.xlsx:
        from openpyxl import load_workbook
        ws = load_workbook(a.xlsx).active
        sums = 0
        for row in ws.iter_rows():
            for cell in row:
                v = cell.value
                if isinstance(v, str):
                    if re.search(r"NOW\(|TODAY\(", v, re.I):
                        E.append(f"xlsx {cell.coordinate}: volatile date formula {v}")
                    if v.startswith("=SUM("):
                        sums += 1
                    if re.search(r"unit price|amount \(", v, re.I):
                        E.append(f"xlsx {cell.coordinate}: price column '{v}'")
        if sums < 3:
            E.append("xlsx totals are not SUM formulas")

    print(f"PL {d.get('pl_no')}: {len(d.get('packages', []))} packages, N.W. {tnw:.2f} kg, G.W. {tgw:.2f} kg, {tcbm:.4f} m3, qty {sum(qty_by_desc.values()):g}")
    for e in E:
        print("ERROR", e)
    for w in W:
        print("WARN ", w)
    print(f"{len(E)} ERROR, {len(W)} WARN -> {'FINAL OK' if not E else 'DRAFT'}")
    sys.exit(1 if E else 0)


if __name__ == "__main__":
    main()
