#!/usr/bin/env python3
"""make_ci.py - render a Southern Machinery COMMERCIAL INVOICE (XLSX, optional PDF) from ci.json.

Usage:
  PYTHONPATH=<dir with openpyxl> python3 make_ci.py <ci.json> [-o OUT.xlsx] [--profile assets/profile.json] [--pdf]

Layout (A4 portrait, one page for up to ~6 lines) - same letterhead/colours/bank block as smt-quotation and
smt-proforma-invoice:
  letterhead (logo, company, Shenzhen address, Tel, web, email, WhatsApp)  ->  COMMERCIAL INVOICE (+ DRAFT banner)
  Buyer / Address / Attn / Email / Tel / [Tax ID] / Ship to  |  Invoice No. / Date / PO No. / [PO date] / [Contract ref.] / Currency
  SHIPMENT & PAYMENT TERMS: port of loading, destination, delivery terms (Incoterms® 2020), shipment, payment,
                            insurance, [requested date], country of origin, [seller tax ID]
  items: Item | Model / P/N | Description (+ Your P/N, H.S. code) | Qty | Unit | Unit price | Amount  (live formulas)
  TOTAL <Incoterm place> (<currency>) + amount in words
  REMARKS: notes (non-dangerous, sample line, ...), [export-control line], certification line
  BANK DETAILS (JPMorgan HK) + bank-change notice, seller signature block
Open issues (level CONFIRM/MISSING, resolved false) shade their cells amber; TO_CONFIRM prints red; file name gets -DRAFT.
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import pi_base as M  # vendored smt-proforma-invoice renderer
from openpyxl.styles import Border, Side


class CI(M.PI):
    def setup(self, ws):
        super().setup(ws)
        ws.title = "Commercial Invoice"
        ws.oddFooter.left.text = f"Commercial Invoice {self.d['pi_no']}"

    def header(self, ws):
        r = super().header(ws)
        ws["A6"].value = "COMMERCIAL INVOICE"
        return r

    def parties(self, ws, r):
        d = self.d
        d["quote_ref"] = d.get("contract_ref", "")
        r2 = super().parties(ws, r)
        ren = {"PI No.": "Invoice No.", "Quotation ref.": "Contract ref.", "To": "Buyer"}
        for row in ws.iter_rows(min_row=r, max_row=r2):
            for c in row:
                if c.value in ren:
                    c.value = ren[c.value]
        if self.flagged("contract_ref"):
            for row in ws.iter_rows(min_row=r, max_row=r2):
                if row[3].value == "Contract ref.":
                    row[5].fill = self.fill(M.AMBER)
        return r2

    def shipment(self, ws, r):
        r2 = super().shipment(ws, r)
        ren = {"Delivery time": "Shipment", "SHIPMENT & PAYMENT": "SHIPMENT & PAYMENT TERMS"}
        for row in ws.iter_rows(min_row=r, max_row=r2):
            for c in row:
                if c.value in ren:
                    c.value = ren[c.value]
        return r2

    def remarks(self, ws, r):
        d, p = self.d, self.p
        ci = p.get("ci", {})
        notes = list(d.get("notes", []))
        if d.get("export_control_line"):
            notes.append(p["pi"]["export_control_line"])
        notes.append(ci.get("certify_line", "We certify that this invoice is true and correct and that the goods are of Chinese origin."))
        self.put(ws, f"A{r}", "REMARKS", 11, True, self.c["navy"])
        self.merge(ws, r, 1, M.NCOL)
        self.rule(ws, r)
        r += 1
        for n, note in enumerate(notes, 1):
            self.put(ws, f"A{r}", f"{n}.", 9, True, self.c["navy"], h="right", v="top")
            self.put(ws, f"B{r}", note, 9, wrap=True, v="top", flag=d.get("note_flags", {}).get(str(n)))
            self.merge(ws, r, 2, M.NCOL)
            ws.row_dimensions[r].height = self.k * (12.5 * self.lines(note, self.width(2, 7), 9) + 3)
            r += 1
        return r + 1

    def signature(self, ws, r):
        d, p = self.d, self.p
        self.put(ws, f"D{r}", f"For and on behalf of\n{p['company']}", 9, True, self.c["navy"], wrap=True, v="top")
        self.merge(ws, r, 4, 7)
        ws.row_dimensions[r].height = self.k * 14 * 3
        r += 4
        line = Side(style="thin", color=self.c["grey"])
        for c in range(4, 8):
            ws.cell(r, c).border = Border(top=line)
        sig = d.get("signatory") or p.get("ci", {}).get("default_signatory", "")
        self.put(ws, f"D{r}", f"{sig}    Authorized signature & company stamp".strip(), 8)
        self.merge(ws, r, 4, 7)
        return r + 1


def is_draft(d):
    return any(i.get("level") in ("CONFIRM", "MISSING") and not i.get("resolved") for i in d.get("issues", []))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ci")
    ap.add_argument("-o", "--out")
    ap.add_argument("--profile", default=os.path.join(ROOT, "assets", "profile.json"))
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    d = M.load(a.ci)
    d["pi_no"] = d["invoice_no"]
    prof = M.load(a.profile)
    prof["pi"]["tax_id_label"] = prof.get("ci", {}).get("tax_id_label", "Seller Tax ID")
    base = os.path.dirname(os.path.abspath(a.ci))
    short = re.sub(r"[^A-Za-z0-9]+", "-", d["buyer"].get("short") or d["buyer"].get("company", "")).strip("-")
    out = a.out or os.path.join(base, "out", f"CI-{d['invoice_no']}-{short}{'-DRAFT' if is_draft(d) else ''}.xlsx")
    CI(d, prof, base).build(out)
    tot = d.get("total_check")
    print(f"OK {out}  total {d.get('currency')} {tot:,.2f}" if tot is not None else f"OK {out}  total TO_CONFIRM")
    if a.pdf:
        pdf = M.to_pdf(out)
        print(f"PDF {pdf}" if pdf else "PDF failed")


if __name__ == "__main__":
    main()
