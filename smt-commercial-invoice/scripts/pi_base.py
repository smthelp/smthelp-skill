#!/usr/bin/env python3
"""pi_base.py (vendored copy of smt-proforma-invoice/scripts/make_pi.py v1.0.0; do not edit here, re-copy on upgrade) - render a Southern Machinery proforma invoice (XLSX, optional PDF) from pi.json.

Usage:
  python3 make_pi.py <pi.json> [-o OUT.xlsx] [--profile assets/profile.json] [--pdf]

pi.json is written by build_pi.py (PO + quotation merge). Layout, top to bottom (A4 portrait):
  letterhead (logo, company, address, contact)  ->  PROFORMA INVOICE + draft banner while issues are open
  parties: To / Address / Attn / Email / Tel / Ship to   |   PI No. / Date / PO No. / PO date / Quotation ref. / Currency
  shipment & payment: port of loading, destination, delivery terms (Incoterms 2020), delivery time,
                      terms of payment, insurance, country of origin, [ship via], [seller tax ID]
  items: Item | Model / P/N | Description of goods (+ HS code / extra lines) | Qty | Unit | Unit price | Amount
  subtotal, charges (freight, packing ...), discount, TOTAL <Incoterm place> (<currency>), amount in words
  remarks: warranty, packing, installation, taxes, notes, [export-control line]
  bank details (+ country, account type, bank code), [CNY WeChat/Alipay line], signatures
Every amount is a live formula. Cells tied to an unresolved CONFIRM issue are shaded amber; TO_CONFIRM prints red.
"""
import argparse, datetime as dt, json, math, os, re, subprocess, sys
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
COLS = [("A", 5.5), ("B", 18), ("C", 56), ("D", 8), ("E", 8), ("F", 15), ("G", 18)]  # same total width as smt-quotation
NCOL = 7
MONEY = '#,##0.00'
QTY = '#,##0.##'
TBC = "TO_CONFIRM"
AMBER, RED = "FFE699", "C0392B"


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def fmt_date(s):
    try:
        return dt.date.fromisoformat(s).strftime("%d %b %Y")
    except (TypeError, ValueError):
        return s or ""


def amount_in_words(x, currency="USD"):
    names = {"USD": ("US dollars", "cents"), "EUR": ("euros", "cents"), "CNY": ("Chinese yuan", "fen"),
             "GBP": ("pounds sterling", "pence")}
    big, small = names.get(currency, (currency, "cents"))
    ones = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
            "sixteen seventeen eighteen nineteen").split()
    tens = "  twenty thirty forty fifty sixty seventy eighty ninety".split(" ")

    def lt1000(n):
        w = []
        if n >= 100:
            w.append(ones[n // 100] + " hundred")
            n %= 100
            if n:
                w.append("and")
        if n >= 20:
            w.append(tens[n // 10] + ("-" + ones[n % 10] if n % 10 else ""))
        elif n or not w:
            w.append(ones[n])
        return " ".join(w)

    def words(n):
        if n == 0:
            return "zero"
        parts = []
        for val, name in ((10**9, "billion"), (10**6, "million"), (1000, "thousand"), (1, "")):
            if n >= val:
                parts.append((lt1000(n // val) + " " + name).strip())
                n %= val
        return " ".join(parts)

    whole = int(math.floor(round(x, 2)))
    cents = int(round((round(x, 2) - whole) * 100))
    s = f"{big.upper()} {words(whole).upper()}"
    if cents:
        s += f" AND {small.upper()} {words(cents).upper()}"
    return "SAY " + s + " ONLY"


class PI:
    def __init__(self, pi, profile, base):
        self.d, self.p, self.base = pi, profile, base
        st = profile["style"]
        self.font, self.c = st["font"], st
        self.delta = st.get("body_size_delta", 0)
        self.k = 1 + 0.1 * self.delta
        self.thin = Side(style="thin", color=st["muted"])
        self.open = {i["id"] for i in pi.get("issues", [])
                     if i["level"] in ("CONFIRM", "MISSING") and not i.get("resolved")}

    # ---------- helpers ----------
    def f(self, size=10, bold=False, color=None, italic=False):
        if size <= 10:
            size += self.delta
        return Font(name=self.font, size=size, bold=bold, italic=italic, color=color or self.c["grey"])

    def fill(self, color):
        return PatternFill("solid", fgColor=color)

    def put(self, ws, ref, value, size=10, bold=False, color=None, h="left", v="center", wrap=False,
            fill=None, fmt=None, italic=False, flag=None):
        cell = ws[ref]
        if value == TBC or (isinstance(value, str) and TBC in value):
            color, bold = RED, True
        cell.value = value
        cell.font = self.f(size, bold, color, italic)
        cell.alignment = Alignment(horizontal=h, vertical=v, wrap_text=wrap)
        if flag and self.flagged(flag):
            fill = AMBER
        if fill:
            cell.fill = self.fill(fill)
        if fmt:
            cell.number_format = fmt
        return cell

    def flagged(self, prefix):
        return any(i == prefix or i.startswith(prefix + ".") for i in self.open)

    def merge(self, ws, r, c1, c2):
        if c2 > c1:
            ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)

    def lines(self, text, width_units, size=10):
        if size <= 10:
            size += self.delta
        cap = max(1, int(width_units * 1.15 * 10.0 / size) - 2)
        return sum(max(1, math.ceil(len(p) / cap)) for p in str(text).split("\n"))

    def width(self, c1, c2):
        return sum(w for _, w in COLS[c1 - 1:c2])

    def rule(self, ws, r):
        for c in range(1, NCOL + 1):
            ws.cell(r, c).border = Border(bottom=Side(style="thin", color=self.c["green"]))

    # ---------- blocks ----------
    def setup(self, ws):
        ws.title = "Proforma Invoice"
        for col, w in COLS:
            ws.column_dimensions[col].width = w
        ws.sheet_view.showGridLines = False
        ps = ws.page_setup
        ps.paperSize, ps.orientation = ws.PAPERSIZE_A4, "portrait"
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ps.fitToWidth, ps.fitToHeight = 1, 0
        ws.page_margins = PageMargins(left=0.4, right=0.4, top=0.45, bottom=0.6, header=0.2, footer=0.25)
        ws.print_options.horizontalCentered = True
        p = self.p
        ws.oddFooter.left.text = f"Proforma Invoice {self.d['pi_no']}"
        ws.oddFooter.center.text = f"{p['web']}  ·  {p['email']}  ·  WhatsApp {p['whatsapp']}"
        ws.oddFooter.right.text = "Page &P of &N"
        for part in (ws.oddFooter.left, ws.oddFooter.center, ws.oddFooter.right):
            part.size, part.font, part.color = 8, f"{self.font},Regular", self.c["grey"]

    def header(self, ws):
        p = self.p
        logo = os.path.join(ROOT, "assets", p["logo"])
        for r, h in ((1, 24), (2, 15), (3, 15)):
            ws.row_dimensions[r].height = self.k * h
        if os.path.exists(logo):
            img = XLImage(logo)
            ratio = img.height / img.width
            img.width, img.height = 170, int(170 * ratio)
            ws.add_image(img, "A1")
        self.put(ws, "C1", p["company"], 15, True, self.c["navy"], h="right")
        self.merge(ws, 1, 3, 7)
        self.put(ws, "C2", p["address"], 8, h="right")
        self.merge(ws, 2, 3, 7)
        tel = f"Tel {p['tel']}  ·  " if p.get("tel") else ""
        self.put(ws, "C3", f"{tel}{p['web']}  ·  {p['email']}  ·  WhatsApp {p['whatsapp']}", 8, h="right")
        self.merge(ws, 3, 3, 7)
        ws.row_dimensions[4].height = 4
        for c in range(1, NCOL + 1):
            ws.cell(4, c).fill = self.fill(self.c["green"])
        r = 6
        self.put(ws, f"A{r}", "PROFORMA INVOICE", 18, True, self.c["navy"])
        self.merge(ws, r, 1, 3)
        ws.row_dimensions[r].height = self.k * 26
        if self.open:
            self.put(ws, f"D{r}", f"DRAFT - {len(self.open)} item(s) to confirm", 10, True, RED, h="right")
            self.merge(ws, r, 4, 7)
        return r + 2

    def parties(self, ws, r):
        d = self.d
        b, st = d["buyer"], d.get("ship_to", {})
        addr = ", ".join(x for x in [b.get("address", ""), b.get("country", "")] if x and x != TBC) or b.get("address")
        ship = ", ".join(x for x in [st.get("company", ""), st.get("address", ""), st.get("country", "")] if x)
        same = st.get("address") == b.get("address") and st.get("company") == b.get("company")
        left = [("To", b.get("company", ""), "buyer.company"), ("Address", addr, "buyer.address"),
                ("Attn", b.get("attn", ""), "buyer.attn"), ("Email", b.get("email", ""), "buyer.email"),
                ("Tel", b.get("tel", ""), "buyer.tel")]
        if b.get("tax_id"):
            left.append(("Tax ID", b["tax_id"], "buyer.tax_id"))
        left.append(("Ship to", "Same as above" if same else ship, "ship_to"))
        right = [("PI No.", d["pi_no"], "pi_no"), ("Date", fmt_date(d["date"]), "date"),
                 ("PO No.", d.get("po_no", ""), "po_no"), ("PO date", fmt_date(d.get("po_date")), "po_date"),
                 ("Quotation ref.", d.get("quote_ref", ""), "quote_ref"), ("Currency", d.get("currency", ""), "currency")]
        right = [x for x in right if x[1] or x[0] in ("PO No.",)]
        n = max(len(left), len(right))
        for i in range(n):
            rr, ln = r + i, 1
            if i < len(left):
                k, v, fl = left[i]
                self.put(ws, f"A{rr}", k, 9, True, self.c["navy"], v="top")
                self.merge(ws, rr, 1, 2)
                self.put(ws, f"C{rr}", v, 9, wrap=True, v="top", flag=fl)
                ln = max(ln, self.lines(v, self.width(3, 3), 9))
            if i < len(right):
                k, v, fl = right[i]
                self.put(ws, f"D{rr}", k, 9, True, self.c["navy"], v="top")
                self.merge(ws, rr, 4, 5)
                self.put(ws, f"F{rr}", v or TBC if k == "PO No." else v, 9, bold=(k == "PI No."), wrap=True, v="top",
                         flag=fl)
                self.merge(ws, rr, 6, 7)
                ln = max(ln, self.lines(v, self.width(6, 7), 9))
            ws.row_dimensions[rr].height = self.k * (14 * ln + 1)
            for c in range(1, NCOL + 1):
                if not ws.cell(rr, c).fill or ws.cell(rr, c).fill.fgColor.rgb in (None, "00000000"):
                    ws.cell(rr, c).fill = self.fill(self.c["light"])
        return r + n + 1

    def shipment(self, ws, r):
        d, p = self.d, self.p
        sh, t = d.get("shipment", {}), d.get("terms", {})
        inco = f"{d.get('incoterm', '')} {d.get('place', '')} (Incoterms® 2020)".strip()
        rows = [("Port of loading", sh.get("port_of_loading", ""), "port_of_loading"),
                ("Destination", sh.get("destination", ""), "destination"),
                ("Delivery terms", inco, "incoterm"),
                ("Delivery time", t.get("delivery", ""), "terms.delivery"),
                ("Terms of payment", t.get("payment", ""), "terms.payment"),
                ("Insurance", t.get("insurance", ""), "terms.insurance")]
        if sh.get("ship_via"):
            rows.append(("Shipment by", sh["ship_via"], "ship_via"))
        if d.get("delivery_date"):
            rows.append(("Requested date", fmt_date(d["delivery_date"]), "delivery_date"))
        rows.append(("Country of origin", sh.get("country_of_origin", p["pi"]["country_of_origin"]), "origin"))
        if d.get("show_tax_id"):
            rows.append((p["pi"]["tax_id_label"], p["pi"]["tax_id"], "tax_id"))
        self.put(ws, f"A{r}", "SHIPMENT & PAYMENT", 11, True, self.c["navy"])
        self.merge(ws, r, 1, NCOL)
        self.rule(ws, r)
        r += 1
        for n, (k, v, fl) in enumerate(rows, 1):
            self.put(ws, f"A{r}", f"{n}.", 9, True, self.c["navy"], h="right", v="top")
            self.put(ws, f"B{r}", k, 9, True, self.c["navy"], v="top")
            self.put(ws, f"C{r}", v, 9, wrap=True, v="top", flag=fl)
            self.merge(ws, r, 3, NCOL)
            ws.row_dimensions[r].height = self.k * (12.5 * self.lines(v, self.width(3, 7), 9) + 3)
            r += 1
        return r + 1

    def table(self, ws, r):
        d = self.d
        cur = d.get("currency", "USD")
        heads = ["Item", "Model / P/N", "Description of goods", "Qty", "Unit", f"Unit price\n({cur})", f"Amount\n({cur})"]
        for i, h in enumerate(heads, 1):
            self.put(ws, f"{get_column_letter(i)}{r}", h, 9, True, "FFFFFF", h="center", wrap=True, fill=self.c["navy"])
        ws.row_dimensions[r].height = self.k * 28
        self.hdr_row = r
        r += 1
        first = r
        refs = []
        for n, it in enumerate(d["items"], 1):
            iid = f"item{n}"
            desc = it.get("name", "")
            extra = []
            if it.get("customer_ref"):
                extra.append(f"Your P/N: {it['customer_ref']}")
            if it.get("hs_code"):
                extra.append(f"H.S. code: {it['hs_code']}")
            extra += it.get("lines", [])
            text = desc + ("\n" + "\n".join(extra) if extra else "")
            self.put(ws, f"A{r}", n, 10, True, self.c["navy"], h="center", v="top")
            model = str(it.get("model", ""))
            self.put(ws, f"B{r}", model, 10 if len(model) <= 14 else 9, True, self.c["navy"], v="top", wrap=True,
                     flag=f"{iid}.match")
            self.put(ws, f"C{r}", text, 10, v="top", wrap=True, flag=f"{iid}.name")
            ws[f"C{r}"].font = self.f(10, True, self.c["navy"]) if not extra else self.f(10)
            self.put(ws, f"D{r}", it.get("qty"), 10, h="center", v="top", fmt=QTY, flag=f"{iid}.qty")
            self.put(ws, f"E{r}", it.get("unit", ""), 10, h="center", v="top")
            self.put(ws, f"F{r}", it.get("price"), 10, h="right", v="top", fmt=MONEY, flag=f"{iid}.price")
            ok = isinstance(it.get("qty"), (int, float)) and isinstance(it.get("price"), (int, float))
            self.put(ws, f"G{r}", f"=D{r}*F{r}" if ok else TBC, 10, h="right", v="top", fmt=MONEY)
            ln = max(self.lines(text, self.width(3, 3), 10), self.lines(model, self.width(2, 2) - 1, 10))
            ws.row_dimensions[r].height = self.k * (14 * ln + 2)
            refs.append(f"G{r}")
            r += 1
        self.box(ws, first, r - 1)
        return r, refs

    def box(self, ws, r1, r2):
        for rr in range(r1, r2 + 1):
            for c in range(1, NCOL + 1):
                ws.cell(rr, c).border = Border(left=self.thin if c == 1 else None, right=self.thin,
                                               top=self.thin if rr == r1 else None,
                                               bottom=self.thin)

    def totals(self, ws, r, refs):
        d = self.d
        cur = d.get("currency", "USD")
        first = r
        extra = bool(d.get("charges") or d.get("discount"))
        sub = None
        if extra:
            self.put(ws, f"C{r}", "Subtotal (goods)", 10, True, self.c["navy"], h="right")
            self.merge(ws, r, 3, 6)
            self.put(ws, f"G{r}", "=" + "+".join(refs) if refs else 0, 10, True, h="right", fmt=MONEY)
            sub = r
            r += 1
        crow = []
        for ch in d.get("charges", []):
            kind = ch["name"]
            self.put(ws, f"C{r}", kind, 9, wrap=True, flag=self.charge_flag(ch))
            self.put(ws, f"D{r}", ch.get("qty", 1), 9, h="center", fmt=QTY)
            self.put(ws, f"E{r}", ch.get("unit", ""), 9, h="center")
            self.put(ws, f"F{r}", ch.get("price", 0), 9, h="right", fmt=MONEY)
            self.put(ws, f"G{r}", f"=D{r}*F{r}", 9, h="right", fmt=MONEY)
            ws.row_dimensions[r].height = self.k * (12.5 * self.lines(kind, self.width(3, 3), 9) + 2)
            crow.append(r)
            r += 1
        if d.get("discount"):
            self.put(ws, f"C{r}", d.get("discount_label", "Discount"), 9, h="right", flag="discount")
            self.merge(ws, r, 3, 6)
            self.put(ws, f"G{r}", -abs(d["discount"]), 9, h="right", fmt=MONEY)
            crow.append(r)
            r += 1
        if r > first:
            self.box(ws, first, r - 1)
        inco = f"{d.get('incoterm', '')} {d.get('place', '')}".strip()
        self.put(ws, f"A{r}", f"TOTAL  {inco}  ({cur})", 11, True, "FFFFFF", fill=self.c["navy"], h="right")
        self.merge(ws, r, 1, 6)
        parts = ([f"G{sub}"] if sub else refs) + [f"G{x}" for x in crow]
        tot_ok = d.get("total_check") is not None
        self.put(ws, f"G{r}", ("=" + "+".join(parts)) if tot_ok and parts else TBC, 12, True, "FFFFFF", h="right",
                 fill=self.c["navy"], fmt=MONEY)
        ws.row_dimensions[r].height = self.k * 22
        r += 1
        words = amount_in_words(d["total_check"], cur) if tot_ok else "AMOUNT IN WORDS: TO_CONFIRM"
        self.put(ws, f"A{r}", words, 9, True, self.c["teal"], italic=True)
        self.merge(ws, r, 1, NCOL)
        ws.row_dimensions[r].height = self.k * 16
        return r + 2

    def charge_flag(self, ch):
        n = ch["name"].lower()
        if re.search(r"freight|shipping|courier|\bdhl\b|fedex|\bups\b|\btnt\b|air ?transport|sea ?transport", n):
            return "charge.freight"
        if re.search(r"pack|\bcase|crate|carton|pallet", n):
            return "charge.packing"
        if re.search(r"install|training|commission|travel", n):
            return "charge.service"
        if re.search(r"mold|mould|tooling", n):
            return "charge.tooling"
        return "charge.other"

    def remarks(self, ws, r):
        d, p = self.d, self.p
        t = d.get("terms", {})
        rows = []
        for k, lab in (("warranty", "Warranty"), ("packing", "Packing"), ("installation", "Installation"),
                       ("taxes", "Taxes & duties")):
            if t.get(k):
                rows.append((lab, t[k], f"terms.{k}"))
        notes = list(d.get("notes", []))
        if d.get("export_control_line"):
            notes.append(p["pi"]["export_control_line"])
        notes.append("Please quote the PI number with your payment. Goods are released after payment as per the terms above.")
        self.put(ws, f"A{r}", "REMARKS", 11, True, self.c["navy"])
        self.merge(ws, r, 1, NCOL)
        self.rule(ws, r)
        r += 1
        n = 0
        for lab, v, fl in rows:
            n += 1
            self.put(ws, f"A{r}", f"{n}.", 9, True, self.c["navy"], h="right", v="top")
            self.put(ws, f"B{r}", lab, 9, True, self.c["navy"], v="top")
            self.put(ws, f"C{r}", v, 9, wrap=True, v="top", flag=fl)
            self.merge(ws, r, 3, NCOL)
            ws.row_dimensions[r].height = self.k * (12.5 * self.lines(v, self.width(3, 7), 9) + 3)
            r += 1
        for note in notes:
            n += 1
            self.put(ws, f"A{r}", f"{n}.", 9, True, self.c["navy"], h="right", v="top")
            self.put(ws, f"B{r}", note, 9, wrap=True, v="top")
            self.merge(ws, r, 2, NCOL)
            ws.row_dimensions[r].height = self.k * (12.5 * self.lines(note, self.width(2, 7), 9) + 3)
            r += 1
        return r + 1

    def bank(self, ws, r):
        b, d = self.p["bank"], self.d
        self.put(ws, f"A{r}", "BANK DETAILS", 11, True, self.c["navy"])
        self.merge(ws, r, 1, NCOL)
        self.rule(ws, r)
        r += 1
        for k, lab in (("beneficiary", "Beneficiary"), ("bank_name", "Bank"), ("bank_address", "Bank address"),
                       ("account_no", b.get("account_label", "Account No.")), ("swift", "SWIFT"),
                       ("bank_code", "Bank code"), ("country", "Country / region"), ("account_type", "Account type")):
            if not b.get(k):
                continue
            self.put(ws, f"A{r}", lab, 9, True, self.c["navy"])
            self.merge(ws, r, 1, 2)
            self.put(ws, f"C{r}", b[k], 9)
            self.merge(ws, r, 3, NCOL)
            r += 1
        if d.get("currency") == "CNY" or d.get("alt_payment"):
            self.put(ws, f"A{r}", self.p["pi"]["alt_payment_cny"], 9, True, self.c["navy"])
            self.merge(ws, r, 1, NCOL)
            r += 1
        self.put(ws, f"A{r}", self.p["bank_change_notice"], 8, italic=True, color=self.c["teal"])
        self.merge(ws, r, 1, NCOL)
        return r + 2

    def signature(self, ws, r):
        d, p = self.d, self.p
        rep = p["sales"].get(d.get("prepared_by", ""), {})
        self.put(ws, f"A{r}", f"For and on behalf of\n{p['company']}", 9, True, self.c["navy"], wrap=True, v="top")
        self.merge(ws, r, 1, 3)
        self.put(ws, f"D{r}", "Accepted and confirmed by the buyer\n" + d["buyer"].get("company", ""), 9, True,
                 self.c["navy"], wrap=True, v="top")
        self.merge(ws, r, 4, 7)
        n = 1 + max(self.lines(p["company"], self.width(1, 3), 9), self.lines(d["buyer"].get("company", ""), self.width(4, 7), 9))
        ws.row_dimensions[r].height = self.k * 14 * n
        r += 3
        line = Side(style="thin", color=self.c["grey"])
        for c in (1, 2, 3, 4, 5, 6, 7):
            if c != 4 or True:
                ws.cell(r, c).border = Border(top=line)
        self.put(ws, f"A{r}", f"{d.get('prepared_by', '')}, {rep.get('title', '')}".strip(", ") +
                 "    Signature & company stamp", 8)
        self.merge(ws, r, 1, 3)
        self.put(ws, f"D{r}", "Name, title, signature & company stamp    Date", 8)
        self.merge(ws, r, 4, 7)
        return r + 1

    def page_breaks(self, ws, blocks, last):
        from openpyxl.worksheet.pagebreak import Break, RowBreak
        total_w = sum(w for _, w in COLS) * 7.8 * 0.75
        scale = min(1.0, (8.27 - 0.8) * 72 / total_w)
        page_h = ((11.69 - 1.05) * 72 - 20) / scale
        h = lambda x: ws.row_dimensions[x].height or 15
        ws.row_breaks = RowBreak()
        used, starts = 0.0, dict(blocks)
        for row in range(1, last + 1):
            if row in starts:
                bh = sum(h(x) for x in range(row, starts[row] + 1))
                if used + bh > page_h and used > 0 and bh <= page_h:
                    ws.row_breaks.append(Break(id=row - 1))
                    used = 0.0
            used += h(row)
            if used > page_h:
                used = h(row)

    def build(self, out):
        wb = Workbook()
        ws = wb.active
        self.setup(ws)
        blocks = []
        r = self.header(ws)
        r = self.parties(ws, r)
        s = r
        r = self.shipment(ws, r)
        blocks.append((s, r - 1))
        s = r
        r, refs = self.table(ws, r)
        if len(self.d["items"]) > 12:  # long item lists: repeat the table header on every page
            ws.print_title_rows = f"{self.hdr_row}:{self.hdr_row}"
        r = self.totals(ws, r, refs)
        blocks.append((r - 4, r - 1))
        s = r
        r = self.remarks(ws, r)
        blocks.append((s, r - 1))
        s = r
        r = self.bank(ws, r)
        r = self.signature(ws, r)
        blocks.append((s, r))
        ws.print_area = f"A1:G{r}"
        self.page_breaks(ws, blocks, r)
        wb.properties.creator = wb.properties.lastModifiedBy = self.p["short"]
        wb.properties.company = self.p["company"]
        wb.properties.title = f"Proforma Invoice {self.d['pi_no']}"
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        wb.save(out)
        return out


def soffice():
    for c in (os.environ.get("SOFFICE"), "soffice", "libreoffice",
              "/workspace/work/lo/root/opt/libreoffice26.8/program/soffice.bin"):
        if c and (os.path.exists(c) or subprocess.run(["which", c], capture_output=True).returncode == 0):
            return c
    return None


def to_pdf(xlsx):
    s = soffice()
    if not s:
        print("WARN no LibreOffice found; skip PDF (set SOFFICE=/path/to/soffice)", file=sys.stderr)
        return None
    outdir = os.path.dirname(os.path.abspath(xlsx))
    env = dict(os.environ, SAL_USE_VCLPLUGIN="svp")
    pdf = os.path.splitext(os.path.abspath(xlsx))[0] + ".pdf"
    for _ in range(2):
        subprocess.run([s, "--headless", "--invisible", "--norestore", "-env:UserInstallation=file:///tmp/lo_smq",
                        "--convert-to", "pdf", "--outdir", outdir, xlsx], env=env, capture_output=True, timeout=180)
        if os.path.exists(pdf):
            return pdf
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pi")
    ap.add_argument("-o", "--out")
    ap.add_argument("--profile", default=os.path.join(ROOT, "assets", "profile.json"))
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    d = load(a.pi)
    base = os.path.dirname(os.path.abspath(a.pi))
    short = re.sub(r"[^A-Za-z0-9]+", "-", d["buyer"].get("short") or d["buyer"].get("company", "")).strip("-")
    out = a.out or os.path.join(base, "out", f"PI-{d['pi_no']}-{short}.xlsx")
    PI(d, load(a.profile), base).build(out)
    tot = d.get("total_check")
    print(f"OK {out}  total {d.get('currency')} {tot:,.2f}" if tot is not None else f"OK {out}  total TO_CONFIRM")
    if a.pdf:
        pdf = to_pdf(out)
        print(f"PDF {pdf}" if pdf else "PDF failed")


if __name__ == "__main__":
    main()
