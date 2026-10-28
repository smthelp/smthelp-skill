#!/usr/bin/env python3
"""make_quote.py - render a Southern Machinery quotation (XLSX) from quote.json.

Usage:
  python3 make_quote.py <quote.json> [-o OUT.xlsx] [--profile assets/profile.json] [--pdf]

quote.json (paths relative to the json file; see examples/levven-CA26101201/quote.json):
{
  "quote_no": "CA26101201",            # 2 letters + YYMMDD + 2-digit seq (profile.quote_no_pattern)
  "date": "2026-10-12",                # ISO date, written as a fixed value (never =NOW())
  "valid_days": 30,                    # or "valid_until": "2026-11-11"
  "project": "PCB Insertion Solution", # optional subtitle under QUOTATION
  "prepared_by": "Leon Hong",          # key in profile.sales -> title/email/whatsapp
  "buyer": {"company": "", "address": "", "country": "", "attn": "", "email": "", "tel": ""},
  "currency": "USD", "incoterm": "EXW", "place": "Shenzhen, China",
  "layout": "auto",                    # auto | single | detail ; auto = detail sheets when any item has "sheet"
  "items": [{
     "model": "S7900VI", "name": "Odd-form Insertion Machine", "qty": 1, "unit": "set",
     "price": 73000,                   # base unit price
     "photo": "photos/s7900vi.png",    # optional
     "specs": ["Insertion heads: 6", ...],
     "options": [{"name": "Radial tape feeder", "qty": 5, "unit": "pc", "price": 3800, "included": true}],
     "sheet": "S7900VI"                # optional: put specs/options on this detail sheet (items may share one)
  }],
  "charges": [{"name": "Export packing ...", "qty": 10, "unit": "case", "price": 500}],
  "discount": 0,                       # positive number, shown as a negative line
  "terms": {"payment": "...", "delivery": "...", ...},  # overrides profile.defaults.terms
  "notes": ["Photos for reference only."]
}
Item amount = qty x price + sum(included option qty x price). Options with "included": false are listed
with their price but not added. All arithmetic is live Excel formulas; amount in words is written as text.
"""
import argparse, datetime as dt, json, math, os, re, subprocess, sys
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

COLS = [("A", 5.5), ("B", 17), ("C", 12), ("D", 44), ("E", 6), ("F", 6), ("G", 13), ("H", 15)]
NCOL = 8
MONEY = '#,##0.00'

INCOTERMS_2020 = {"EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"}


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def fmt_date(d):
    return d.strftime("%d %b %Y")


def amount_in_words(x, currency="USD"):
    names = {"USD": ("US dollars", "cents"), "EUR": ("euros", "cents"), "CNY": ("Chinese yuan", "fen"),
             "GBP": ("pounds sterling", "pence")}
    big, small = names.get(currency, (currency, "cents"))
    ones = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen " \
           "sixteen seventeen eighteen nineteen".split()
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


class Q:
    def __init__(self, quote, profile, base):
        self.q, self.p, self.base = quote, profile, base
        st = profile["style"]
        self.font = st["font"]
        self.c = st
        self.thin = Side(style="thin", color=st["muted"])
        self.navy_side = Side(style="medium", color=st["navy"])

    # ---------- style helpers ----------
    def f(self, size=10, bold=False, color=None, italic=False):
        return Font(name=self.font, size=size, bold=bold, italic=italic, color=color or self.c["grey"])

    def fill(self, color):
        return PatternFill("solid", fgColor=color)

    def put(self, ws, ref, value, size=10, bold=False, color=None, h="left", v="center", wrap=False,
            fill=None, fmt=None, italic=False, indent=0):
        cell = ws[ref]
        cell.value = value
        cell.font = self.f(size, bold, color, italic)
        cell.alignment = Alignment(horizontal=h, vertical=v, wrap_text=wrap, indent=indent)
        if fill:
            cell.fill = self.fill(fill)
        if fmt:
            cell.number_format = fmt
        return cell

    def merge(self, ws, r, c1, c2, r2=None):
        if c2 > c1 or (r2 and r2 > r):
            ws.merge_cells(start_row=r, start_column=c1, end_row=r2 or r, end_column=c2)

    def lines_needed(self, text, width_units, size=10):
        """Wrapped line count for text in a cell `width_units` wide (Excel column units) at font `size`."""
        per_unit = 1.15 * 10.0 / size  # Arial: ~1.15 chars per column unit at 10 pt
        cap = max(1, int(width_units * per_unit) - 2)
        n = 0
        for para in str(text).split("\n"):
            n += max(1, math.ceil(len(para) / cap))
        return n

    def width(self, c1, c2):
        return sum(w for _, w in COLS[c1 - 1:c2])

    def setup(self, ws, title):
        ws.title = title[:31]
        for col, w in COLS:
            ws.column_dimensions[col].width = w
        ws.sheet_view.showGridLines = False
        ps = ws.page_setup
        ps.paperSize = ws.PAPERSIZE_A4
        ps.orientation = "portrait"
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ps.fitToWidth, ps.fitToHeight = 1, 0
        ws.page_margins = PageMargins(left=0.4, right=0.4, top=0.45, bottom=0.6, header=0.2, footer=0.25)
        ws.print_options.horizontalCentered = True
        p = self.p
        contact = f"{p['web']}  ·  {p['email']}  ·  WhatsApp {p['whatsapp']}"
        ws.oddFooter.left.text = f"Quotation {self.q['quote_no']}"
        ws.oddFooter.center.text = contact
        ws.oddFooter.right.text = "Page &P of &N"
        for part in (ws.oddFooter.left, ws.oddFooter.center, ws.oddFooter.right):
            part.size, part.font, part.color = 8, f"{self.font},Regular", self.c["grey"]

    # ---------- blocks ----------
    def header(self, ws, compact=False):
        p = self.p
        logo = os.path.join(ROOT, "assets", p["logo"])
        ws.row_dimensions[1].height = 24
        ws.row_dimensions[2].height = 15
        ws.row_dimensions[3].height = 15
        if os.path.exists(logo):
            img = XLImage(logo)
            ratio = img.height / img.width
            img.width = 170
            img.height = int(170 * ratio)
            ws.add_image(img, "A1")
        self.put(ws, "D1", p["company"], 15, True, self.c["navy"], h="right")
        self.merge(ws, 1, 4, 8)
        self.put(ws, "D2", p["address"], 8, h="right")
        self.merge(ws, 2, 4, 8)
        tel = f"Tel {p['tel']}  ·  " if p.get("tel") else ""
        self.put(ws, "D3", f"{tel}{p['web']}  ·  {p['email']}  ·  WhatsApp {p['whatsapp']}", 8, h="right")
        self.merge(ws, 3, 4, 8)
        ws.row_dimensions[4].height = 4
        for c in range(1, NCOL + 1):
            ws.cell(4, c).fill = self.fill(self.c["green"])
        r = 6
        title = "QUOTATION" if not compact else "QUOTATION - DETAIL"
        self.put(ws, f"A{r}", title, 18 if not compact else 14, True, self.c["navy"])
        self.merge(ws, r, 1, 4)
        ws.row_dimensions[r].height = 26
        if self.q.get("project"):
            self.put(ws, f"E{r}", self.q["project"], 11, True, self.c["teal"], h="right")
            self.merge(ws, r, 5, 8)
        return r + 2

    def info_block(self, ws, r, compact=False):
        q, p = self.q, self.p
        b = q["buyer"]
        rep = p["sales"].get(q.get("prepared_by", ""), {})
        date = dt.date.fromisoformat(q["date"])
        valid = dt.date.fromisoformat(q["valid_until"]) if q.get("valid_until") else date + dt.timedelta(
            days=int(q.get("valid_days", p["defaults"]["valid_days"])))
        self.valid_until = valid
        addr = ", ".join(x for x in [b.get("address", ""), b.get("country", "")] if x)
        left = [("To", b.get("company", "")), ("Address", addr), ("Attn", b.get("attn", "")),
                ("Email", b.get("email", "")), ("Tel", b.get("tel", ""))]
        inco = f"{q.get('incoterm', 'EXW')} {q.get('place', '')} (Incoterms® 2020)".strip()
        right = [("Quotation No.", q["quote_no"]), ("Date", fmt_date(date)), ("Valid until", fmt_date(valid)),
                 ("Prepared by", q.get("prepared_by", "")), ("Email", rep.get("email", p["email"])),
                 ("Price basis", inco), ("Currency", q.get("currency", "USD"))]
        if compact:
            left = left[:1]
            right = right[:2]
        n = max(len(left), len(right))
        for i in range(n):
            rr = r + i
            lines = 1
            if i < len(left):
                k, v = left[i]
                self.put(ws, f"A{rr}", k, 9, True, self.c["navy"], v="top")
                self.merge(ws, rr, 1, 2)
                self.put(ws, f"C{rr}", v, 9, wrap=True, v="top")
                self.merge(ws, rr, 3, 4)
                lines = max(lines, self.lines_needed(v, self.width(3, 4), 9))
            if i < len(right):
                k, v = right[i]
                self.put(ws, f"E{rr}", k, 9, True, self.c["navy"], v="top")
                self.merge(ws, rr, 5, 6)
                self.put(ws, f"G{rr}", v, 9, bold=(k == "Quotation No."), wrap=True, v="top")
                self.merge(ws, rr, 7, 8)
                lines = max(lines, self.lines_needed(v, self.width(7, 8), 9))
            ws.row_dimensions[rr].height = 14 * lines + 1
            for c in range(1, NCOL + 1):
                ws.cell(rr, c).fill = self.fill(self.c["light"])
        return r + n + 1

    def table_header(self, ws, r):
        cur = self.q.get("currency", "USD")
        heads = ["Item", "Photo", "Model", "Description", "Qty", "Unit", f"Unit Price\n({cur})", f"Amount\n({cur})"]
        for i, h in enumerate(heads, 1):
            self.put(ws, f"{get_column_letter(i)}{r}", h, 9, True, "FFFFFF", h="center", wrap=True,
                     fill=self.c["navy"])
        ws.row_dimensions[r].height = 28
        return r + 1

    def box(self, ws, r1, r2):
        for rr in range(r1, r2 + 1):
            for c in range(1, NCOL + 1):
                cell = ws.cell(rr, c)
                cell.border = Border(left=self.thin if c == 1 else None, right=self.thin,
                                     top=self.thin if rr == r1 else None, bottom=self.thin if rr == r2 else None)

    def photo(self, ws, path, row, rows_h_pt):
        full = os.path.join(self.base, path)
        if not os.path.exists(full):
            print(f"WARN photo missing: {path}", file=sys.stderr)
            return 0
        img = XLImage(full)
        maxw = int(COLS[1][1] * 7.0) - 8  # px inside column B
        target_h = max(60, min(130, rows_h_pt * 1.33 - 6))
        ratio = img.height / img.width
        w = maxw
        h = int(w * ratio)
        if h > target_h:
            h = int(target_h)
            w = int(h / ratio)
        img.width, img.height = w, h
        ws.add_image(img, f"B{row}")
        return h / 1.33 + 6  # points needed

    def item_block(self, ws, r, idx, it, inline=True):
        """Write an item with specs/options. Returns (next_row, amount_cell_ref)."""
        start = r
        self.put(ws, f"A{r}", idx, 10, True, self.c["navy"], h="center", v="top")
        self.put(ws, f"C{r}", it.get("model", ""), 10, True, self.c["navy"], v="top")
        self.put(ws, f"D{r}", it.get("name", ""), 10, True, self.c["navy"], v="top", wrap=True)
        self.put(ws, f"E{r}", it.get("qty", 1), 10, h="center", v="top")
        self.put(ws, f"F{r}", it.get("unit", "set"), 10, h="center", v="top")
        self.put(ws, f"G{r}", it.get("price", 0), 10, h="right", v="top", fmt=MONEY)
        self.put(ws, f"H{r}", f"=E{r}*G{r}", 10, h="right", v="top", fmt=MONEY)
        ws.row_dimensions[r].height = 14 * self.lines_needed(it.get("name", ""), self.width(4, 4), 10) + 1
        base_row = r
        r += 1
        if inline:
            for s in it.get("specs", []):
                self.put(ws, f"D{r}", "•  " + s, 8, wrap=True, v="top")
                ws.row_dimensions[r].height = 11 * self.lines_needed("•  " + s, self.width(4, 4), 8) + 1
                r += 1
        opt_rows = []
        if it.get("options"):
            self.put(ws, f"D{r}", "Options", 9, True, self.c["teal"])
            ws.row_dimensions[r].height = 14
            r += 1
            for o in it["options"]:
                self.put(ws, f"D{r}", o["name"], 9, wrap=True, indent=1, v="top")
                self.put(ws, f"E{r}", o.get("qty", 1), 9, h="center", v="top")
                self.put(ws, f"F{r}", o.get("unit", "pc"), 9, h="center", v="top")
                self.put(ws, f"G{r}", o.get("price", 0), 9, h="right", v="top", fmt=MONEY)
                if o.get("included", True):
                    self.put(ws, f"H{r}", f"=E{r}*G{r}", 9, h="right", v="top", fmt=MONEY)
                    opt_rows.append(r)
                else:
                    self.put(ws, f"H{r}", "optional", 8, h="right", v="top", italic=True)
                ws.row_dimensions[r].height = 12.5 * self.lines_needed(o["name"], self.width(4, 4) - 2, 9) + 1
                r += 1
        # photo sizing
        total_h = sum((ws.row_dimensions[x].height or 15) for x in range(start, r))
        if it.get("photo"):
            need = self.photo(ws, it["photo"], start, total_h)
            if need > total_h:
                ws.row_dimensions[r - 1].height = (ws.row_dimensions[r - 1].height or 15) + (need - total_h)
        amount_ref = f"H{base_row}"
        if opt_rows:
            self.put(ws, f"D{r}", f"Subtotal {it.get('model', '')} incl. options", 9, True, self.c["navy"], h="right")
            self.merge(ws, r, 4, 7)
            refs = ",".join([f"H{base_row}"] + [f"H{x}" for x in opt_rows])
            self.put(ws, f"H{r}", f"=SUM({refs})", 10, True, self.c["navy"], h="right", fmt=MONEY)
            ws.row_dimensions[r].height = 16
            amount_ref = f"H{r}"
            r += 1
        self.box(ws, start, r - 1)
        return r, amount_ref

    def amount(self, it):
        a = it.get("qty", 1) * it.get("price", 0)
        for o in it.get("options", []):
            if o.get("included", True):
                a += o.get("qty", 1) * o.get("price", 0)
        return a

    def totals(self, ws, r, item_refs):
        q = self.q
        first = r
        cur = q.get("currency", "USD")
        has_extra = bool(q.get("charges") or q.get("discount"))
        sub_formula = "+".join(item_refs) if item_refs else "0"
        sub = None
        if has_extra:
            self.put(ws, f"D{r}", "Subtotal (equipment)", 10, True, self.c["navy"], h="right")
            self.merge(ws, r, 4, 7)
            self.put(ws, f"H{r}", "=" + sub_formula, 10, True, h="right", fmt=MONEY)
            sub = r
            r += 1
        charge_rows = []
        for ch in q.get("charges", []):
            label = ch["name"]
            self.put(ws, f"D{r}", label, 9, wrap=True)
            self.put(ws, f"E{r}", ch.get("qty", 1), 9, h="center")
            self.put(ws, f"F{r}", ch.get("unit", ""), 9, h="center")
            self.put(ws, f"G{r}", ch.get("price", 0), 9, h="right", fmt=MONEY)
            self.put(ws, f"H{r}", f"=E{r}*G{r}", 9, h="right", fmt=MONEY)
            ws.row_dimensions[r].height = 12.5 * self.lines_needed(label, self.width(4, 4), 9) + 1
            charge_rows.append(r)
            r += 1
        if q.get("discount"):
            self.put(ws, f"D{r}", q.get("discount_label", "Discount"), 9, h="right")
            self.merge(ws, r, 4, 7)
            self.put(ws, f"H{r}", -abs(q["discount"]), 9, h="right", fmt=MONEY)
            charge_rows.append(r)
            r += 1
        if r > first:
            self.box(ws, first, r - 1)
        inco = f"{q.get('incoterm', 'EXW')} {q.get('place', '')}".strip()
        self.put(ws, f"A{r}", f"TOTAL  {inco}  ({cur})", 11, True, "FFFFFF", fill=self.c["navy"], h="right")
        self.merge(ws, r, 1, 7)
        refs = "+".join(([f"H{sub}"] if sub else [sub_formula]) + [f"H{x}" for x in charge_rows])
        self.put(ws, f"H{r}", f"={refs}", 12, True, "FFFFFF", h="right", fill=self.c["navy"], fmt=MONEY)
        ws.row_dimensions[r].height = 22
        total_row = r
        r += 1
        total_val = sum(self.amount(i) for i in q["items"]) + sum(
            c.get("qty", 1) * c.get("price", 0) for c in q.get("charges", [])) - abs(q.get("discount", 0))
        self.total_value = total_val
        self.put(ws, f"A{r}", amount_in_words(total_val, cur), 9, True, self.c["teal"], italic=True)
        self.merge(ws, r, 1, 8)
        ws.row_dimensions[r].height = 16
        return r + 2, total_row

    def terms_block(self, ws, r):
        q, p = self.q, self.p
        terms = dict(p["defaults"]["terms"])
        terms.update(q.get("terms", {}))
        inco = f"{q.get('incoterm', 'EXW')} {q.get('place', '')} (Incoterms® 2020), in {q.get('currency', 'USD')}"
        terms.setdefault("price_basis", inco)
        if "price_basis" not in q.get("terms", {}):
            terms["price_basis"] = inco
        terms.setdefault("validity", "")
        if not q.get("terms", {}).get("validity"):
            terms["validity"] = f"This quotation is valid until {fmt_date(self.valid_until)}"
        self.put(ws, f"A{r}", "TERMS & CONDITIONS", 11, True, self.c["navy"])
        self.merge(ws, r, 1, 8)
        for c in range(1, NCOL + 1):
            ws.cell(r, c).border = Border(bottom=Side(style="thin", color=self.c["green"]))
        r += 1
        n = 0
        for key in p["terms_order"]:
            val = terms.get(key)
            if not val:
                continue
            vals = val if isinstance(val, list) else [val]
            n += 1
            self.put(ws, f"A{r}", f"{n}.", 9, True, self.c["navy"], h="right", v="top")
            self.put(ws, f"B{r}", p["terms_labels"].get(key, key.title()), 9, True, self.c["navy"], v="top")
            text = "\n".join(vals)
            self.put(ws, f"C{r}", text, 9, wrap=True, v="top")
            self.merge(ws, r, 3, 8)
            ws.row_dimensions[r].height = 12.5 * self.lines_needed(text, self.width(3, 8), 9) + 3
            r += 1
        for note in q.get("notes", []):
            n += 1
            self.put(ws, f"A{r}", f"{n}.", 9, True, self.c["navy"], h="right", v="top")
            self.put(ws, f"B{r}", note, 9, wrap=True, v="top")
            self.merge(ws, r, 2, 8)
            ws.row_dimensions[r].height = 12.5 * self.lines_needed(note, self.width(2, 8), 9) + 3
            r += 1
        return r + 1

    def bank_block(self, ws, r):
        b = self.p["bank"]
        if not b.get("show", True):
            return r
        self.put(ws, f"A{r}", "BANK INFORMATION", 11, True, self.c["navy"])
        self.merge(ws, r, 1, 8)
        for c in range(1, NCOL + 1):
            ws.cell(r, c).border = Border(bottom=Side(style="thin", color=self.c["green"]))
        r += 1
        for k, lab in (("beneficiary", "Beneficiary"), ("bank_name", "Bank"), ("bank_address", "Bank address"),
                       ("account_no", "Account No."), ("swift", "SWIFT")):
            self.put(ws, f"A{r}", lab, 9, True, self.c["navy"])
            self.merge(ws, r, 1, 2)
            red = "C0392B" if "TO_CONFIRM" in str(b.get(k, "")) else None
            self.put(ws, f"C{r}", b.get(k, ""), 9, color=red, bold=bool(red))
            self.merge(ws, r, 3, 8)
            r += 1
        self.put(ws, f"A{r}", self.p["bank_change_notice"], 8, italic=True, color=self.c["teal"])
        self.merge(ws, r, 1, 8)
        return r + 2

    def signature(self, ws, r):
        q, p = self.q, self.p
        rep = p["sales"].get(q.get("prepared_by", ""), {})
        self.put(ws, f"A{r}", f"For and on behalf of\n{p['company']}", 9, True, self.c["navy"], wrap=True, v="top")
        self.merge(ws, r, 1, 4)
        self.put(ws, f"E{r}", "Accepted and confirmed by the buyer\n" + q["buyer"].get("company", ""), 9, True,
                 self.c["navy"], wrap=True, v="top")
        self.merge(ws, r, 5, 8)
        ws.row_dimensions[r].height = 28
        r += 3
        line = Side(style="thin", color=self.c["grey"])
        for c in list(range(1, 4)) + list(range(5, 9)):
            ws.cell(r, c).border = Border(top=line)
        r += 0
        self.put(ws, f"A{r}", f"{q.get('prepared_by', '')}, {rep.get('title', '')}".strip(", ") +
                 "    Signature & company stamp", 8)
        self.merge(ws, r, 1, 4)
        self.put(ws, f"E{r}", "Name, title, signature & company stamp    Date", 8)
        self.merge(ws, r, 5, 8)
        return r + 1

    def page_breaks(self, ws, blocks, last_row):
        """Insert manual row breaks so no block (item, totals, terms, bank+signature) straddles a page."""
        from openpyxl.worksheet.pagebreak import Break, RowBreak
        total_w_pt = sum(w for _, w in COLS) * 7.8 * 0.75  # calibrated on LibreOffice PDF export
        printable_w = (8.27 - 0.8) * 72
        printable_h = (11.69 - 1.05) * 72 - 20
        scale = min(1.0, printable_w / total_w_pt)
        page_h = printable_h / scale
        h = lambda r: ws.row_dimensions[r].height or 15
        ws.row_breaks = RowBreak()
        used, row = 0.0, 1
        starts = {a: b for a, b in blocks}
        while row <= last_row:
            if row in starts:
                bh = sum(h(x) for x in range(row, starts[row] + 1))
                if used + bh > page_h and used > 0 and bh <= page_h:
                    ws.row_breaks.append(Break(id=row - 1))
                    used = 0.0
            used += h(row)
            if used > page_h:
                used = h(row)
            row += 1

    # ---------- sheets ----------
    def build(self, out):
        q = self.q
        layout = q.get("layout", "auto")
        use_detail = layout == "detail" or (layout == "auto" and any(i.get("sheet") for i in q["items"]))
        wb = Workbook()
        ws = wb.active
        self.setup(ws, "Quotation")
        r = self.header(ws)
        r = self.info_block(ws, r)
        hdr = r
        r = self.table_header(ws, r)
        item_refs = []
        self.blocks = []
        detail_items = {}
        for idx, it in enumerate(q["items"], 1):
            if use_detail and it.get("sheet"):
                detail_items.setdefault(it["sheet"], []).append((idx, it, r))
                start = r
                self.put(ws, f"A{r}", idx, 10, True, self.c["navy"], h="center", v="top")
                self.put(ws, f"C{r}", it.get("model", ""), 10, True, self.c["navy"], v="top")
                extra = f"\nSee sheet \"{it['sheet']}\" for specifications" + (" and options" if it.get("options") else "")
                self.put(ws, f"D{r}", it.get("name", "") + extra, 10, True, self.c["navy"], v="top", wrap=True)
                ws.cell(r, 4).font = self.f(10, True, self.c["navy"])
                self.put(ws, f"E{r}", it.get("qty", 1), 10, h="center", v="top")
                self.put(ws, f"F{r}", it.get("unit", "set"), 10, h="center", v="top")
                # G/H filled after detail sheet is written
                ws.row_dimensions[r].height = 30
                if it.get("photo"):
                    need = self.photo(ws, it["photo"], r, 60)
                    ws.row_dimensions[r].height = max(30, need)
                self.box(ws, start, r)
                item_refs.append(f"H{r}")
                r += 1
            else:
                s0 = r
                r, ref = self.item_block(ws, r, idx, it, inline=True)
                item_refs.append(ref)
                self.blocks.append((s0, r - 1))
        s0 = r
        r, total_row = self.totals(ws, r, item_refs)
        self.blocks.append((s0, r - 1))
        s0 = r
        r = self.terms_block(ws, r)
        self.blocks.append((s0, r - 1))
        s0 = r
        r = self.bank_block(ws, r)
        r = self.signature(ws, r)
        self.blocks.append((s0, r))
        ws.print_area = f"A1:H{r}"
        self.page_breaks(ws, self.blocks, r)
        # detail sheets
        for sheet, lst in detail_items.items():
            ds = wb.create_sheet()
            self.setup(ds, sheet)
            dr = self.header(ds, compact=True)
            dr = self.info_block(ds, dr, compact=True)
            dh = dr
            dr = self.table_header(ds, dr)
            ds.print_title_rows = f"{dh}:{dh}"
            dblocks = []
            for idx, it, srow in lst:
                s0 = dr
                dr, ref = self.item_block(ds, dr, idx, it, inline=True)
                dblocks.append((s0, dr - 1))
                sname = ds.title.replace("'", "''")
                ws[f"H{srow}"] = f"='{sname}'!{ref}"
                ws[f"H{srow}"].font = self.f(10)
                ws[f"H{srow}"].number_format = MONEY
                ws[f"H{srow}"].alignment = Alignment(horizontal="right", vertical="top")
                ws[f"G{srow}"] = f"=H{srow}/E{srow}"
                ws[f"G{srow}"].font = self.f(10)
                ws[f"G{srow}"].number_format = MONEY
                ws[f"G{srow}"].alignment = Alignment(horizontal="right", vertical="top")
            self.put(ds, f"A{dr}", "Prices on this sheet are carried to the Quotation sheet. Terms & conditions: see Quotation sheet.",
                     8, italic=True)
            self.merge(ds, dr, 1, 8)
            ds.print_area = f"A1:H{dr}"
            self.page_breaks(ds, dblocks, dr)
        wb.properties.creator = self.p["short"]
        wb.properties.company = self.p["company"]
        wb.properties.title = f"Quotation {q['quote_no']}"
        wb.properties.lastModifiedBy = self.p["short"]
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
    subprocess.run([s, "--headless", "--invisible", "--norestore", "-env:UserInstallation=file:///tmp/lo_smq",
                    "--convert-to", "pdf", "--outdir", outdir, xlsx], env=env, capture_output=True, timeout=180)
    pdf = os.path.splitext(os.path.abspath(xlsx))[0] + ".pdf"
    return pdf if os.path.exists(pdf) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("quote")
    ap.add_argument("-o", "--out")
    ap.add_argument("--profile", default=os.path.join(ROOT, "assets", "profile.json"))
    ap.add_argument("--pdf", action="store_true", help="also export PDF with LibreOffice")
    a = ap.parse_args()
    quote = load(a.quote)
    profile = load(a.profile)
    base = os.path.dirname(os.path.abspath(a.quote))
    name = f"Quotation-{quote['quote_no']}-{re.sub(r'[^A-Za-z0-9]+', '-', (quote['buyer'].get('short') or quote['buyer'].get('company', ''))).strip('-')}"
    out = a.out or os.path.join(base, "out", name + ".xlsx")
    q = Q(quote, profile, base)
    q.build(out)
    print(f"OK {out}  total {quote.get('currency', 'USD')} {q.total_value:,.2f}")
    if a.pdf:
        pdf = to_pdf(out)
        print(f"PDF {pdf}" if pdf else "PDF failed")


if __name__ == "__main__":
    main()
