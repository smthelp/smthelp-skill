# SM stencil wiping paper roll price list (adapted from squeegee-kit/quote/make_quote.py, 2026-11-19).
# Reads ROWS (cny per SKU) from ../models.py; USD = round(CNY x 2 / 6.6) via models.usd().
# DO NOT RENDER until Jason has set the price basis and filled cny in models.py.
# usage: python3 quote/make_quote.py              -> refuses while any offered row has cny None
#        python3 quote/make_quote.py --skip-unpriced   -> renders only rows that have a cny (lists the skipped ones)
import sys, os, datetime
D = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(D); sys.path.insert(0, K)
from models import ROWS, GROUPS, usd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as XImg

QNO = "SM-Q-WP-" + datetime.date.today().strftime("%Y%m%d"); DATE = datetime.date.today().isoformat()
GREEN, TEAL, DARK = "90C641", "0AA5A5", "003141"
TITLE = "SMT Stencil Wiping Paper Rolls - sized for DEK, MPM, GKG, Desen, Panasonic, Yamaha and more"
TERMS = [
 "Unit price per roll. Size = core (tube) length x paper width x roll length, e.g. 410 x 300 mm x 10 m.",
 "Before ordering please confirm: printer brand and model, core length, paper width, core opening (cross slot / straight slot / 12 inner grooves / paper tube) and roll direction - a photo of the old roll is the fastest way.",
 "Material: natural wood pulp + polyester, hydroentangled two-layer web, low lint, absorbs water and oil, usable with stencil cleaning solvents. Composition and basis weight confirmed per batch.",
 "Custom widths, lengths, width-only rolls and 200 x 200 mm sheets on request. Rows marked 'size table' are confirmed per order.",
 "Printer brand names identify compatible printers only; Southern Machinery is not affiliated with them.",
 "Price basis: [to be confirmed by Southern Machinery]. Payment terms, lead time and validity: [to be confirmed by Southern Machinery].",
]
OPEN = ("listed", "single", "table")   # which model status rows are offered

def items(skip_unpriced):
    rows = [r for r in ROWS if r["status"] in OPEN]
    miss = [r["code"] for r in rows if r["cny"] is None]
    if miss and not skip_unpriced:
        sys.exit(f"STOP: {len(miss)} of {len(rows)} rows have no cny in models.py (price basis pending). "
                 "Fill cny first, or run with --skip-unpriced to render only priced rows.")
    if miss: print("skipped (no cny):", ", ".join(miss))
    out = []
    for r in rows:
        if r["cny"] is None: continue
        model = r["model"] + ("  (size table - confirm)" if r["status"] == "table" else "")
        out.append(dict(g=r["group"], code=r["code"], model=model, size=r["size"], opening=r["opening"], cny=r["cny"], usd=usd(r["cny"])))
    if not out: sys.exit("STOP: no priced rows.")
    return out

HDR = ["No.", "SM code", "Printer / fit", "Size (core x width x length)", "Core / opening", "USD / roll", "Qty", "Amount (USD)"]

def xlsx(path, it):
    wb = Workbook(); ws = wb.active; ws.title = "Price list"
    thin = Side(style="thin", color="BBBBBB"); B = Border(left=thin, right=thin, top=thin, bottom=thin)
    for i, w in enumerate([6, 24, 32, 28, 26, 12, 8, 14]): ws.column_dimensions[chr(65 + i)].width = w
    ws.row_dimensions[1].height = 48; ws.add_image(XImg(os.path.join(K, "sm-logo.png")), "A1")
    ws.merge_cells("D1:H1"); ws["D1"] = "PRICE LIST / QUOTATION"; ws["D1"].font = Font(bold=True, size=20, color=DARK); ws["D1"].alignment = Alignment(horizontal="right", vertical="center")
    r = 3
    for k, v in [("Product", TITLE), ("Quotation No.", QNO), ("Date", DATE), ("To", "[Customer name / company]"), ("Currency", "USD, unit price per roll"),
                 ("From", "Southern Machinery | info@smthelp.com | WhatsApp +86 136 0256 2576 | www.smthelp.com")]:
        ws.cell(r, 2, k).font = Font(bold=True, color=DARK); ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=8); ws.cell(r, 3, v); r += 1
    r += 1; first = None; n = 1
    for g in GROUPS:
        sub = [x for x in it if x["g"] == g]
        if not sub: continue
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
        c = ws.cell(r, 1, f"{g}. {GROUPS[g]}"); c.font = Font(bold=True, color="FFFFFF", size=12); c.fill = PatternFill("solid", fgColor=GREEN); r += 1
        for i, h in enumerate(HDR, 1):
            c = ws.cell(r, i, h); c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=TEAL); c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = B
        r += 1
        for x in sub:
            first = first or r
            for i, v in enumerate([n, x["code"], x["model"], x["size"], x["opening"], x["usd"], 0, f"=F{r}*G{r}"], 1):
                c = ws.cell(r, i, v); c.border = B; c.alignment = Alignment(vertical="center", wrap_text=True, horizontal="center" if i in (1, 6, 7, 8) else "left")
                if i in (6, 8): c.number_format = '"$"#,##0.00'
            ws.cell(r, 7).fill = PatternFill("solid", fgColor="FFF8DC"); r += 1; n += 1
    last = r - 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
    c = ws.cell(r, 1, "TOTAL (USD) - enter quantities in the yellow Qty column"); c.font = Font(bold=True); c.alignment = Alignment(horizontal="right")
    t = ws.cell(r, 8, f"=SUM(H{first}:H{last})"); t.font = Font(bold=True, color=DARK); t.number_format = '"$"#,##0.00'; t.border = B
    r += 2; ws.cell(r, 1, "Notes").font = Font(bold=True, color=DARK, size=12); r += 1
    for i, tx in enumerate(TERMS, 1):
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
        c = ws.cell(r, 1, f"{i}. {tx}"); c.alignment = Alignment(wrap_text=True, vertical="top"); ws.row_dimensions[r].height = 30; r += 1
    ws.page_setup.orientation = "landscape"; ws.sheet_properties.pageSetUpPr.fitToPage = True; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    wb.save(path)

def pdf(path, it):
    from weasyprint import HTML
    th = "<tr>" + "".join(f"<th>{h}</th>" for h in HDR[:6]) + "</tr>"
    body = ""; n = 1
    for g in GROUPS:
        sub = [x for x in it if x["g"] == g]
        if not sub: continue
        rows = ""
        for x in sub:
            rows += f"<tr><td>{n}</td><td><b>{x['code']}</b></td><td>{x['model']}</td><td>{x['size']}</td><td>{x['opening']}</td><td class=p>${x['usd']:,}</td></tr>"; n += 1
        body += f"<h2>{g}. {GROUPS[g]}</h2><table class=q>{th}{rows}</table>"
    html = f"""<html><head><style>
@page{{size:A4 landscape;margin:12mm 12mm 14mm;@bottom-center{{content:"Southern Machinery  |  www.smthelp.com  |  info@smthelp.com  |  WhatsApp +86 136 0256 2576   -   page " counter(page);font:8pt DejaVu Sans;color:#0AA5A5}}}}
body{{font-family:'DejaVu Sans';font-size:8.6pt;color:#222}}
.top{{display:flex;justify-content:space-between;align-items:center;border-bottom:4px solid #90C641;padding-bottom:6px}}
h1{{color:#003141;font-size:22pt;margin:0}} .meta td{{padding:1px 8px 1px 0}} .meta b{{color:#003141}}
table.q{{width:100%;border-collapse:collapse;margin-top:4px}} .q th{{background:#0AA5A5;color:#fff;padding:5px;font-size:8.4pt}}
.q td{{border:1px solid #ccc;padding:3.5px 5px}} .q tr:nth-child(even) td{{background:#f4f9ec}} td.p{{text-align:right;font-weight:bold;color:#003141;white-space:nowrap}}
h2{{background:#90C641;color:#fff;font-size:10.5pt;padding:4px 8px;margin:10px 0 0;page-break-after:avoid}}
.hero{{display:flex;gap:10px;align-items:center;margin:8px 0}} .hero img{{height:105px;border:1px solid #ddd}}
ol{{margin:4px 0 0 16px;padding:0}} li{{margin-bottom:3px}}
</style></head><body>
<div class=top><img src="file://{K}/sm-logo.png" style="height:44px"><h1>PRICE LIST / QUOTATION</h1></div>
<div class=hero><img src="file://{K}/assets/01-rolls-hero.jpg"><img src="file://{K}/assets/07-core-types.jpg">
<table class=meta><tr><td><b>Product</b></td><td>{TITLE}</td></tr><tr><td><b>Quotation No.</b></td><td>{QNO}</td></tr><tr><td><b>Date</b></td><td>{DATE}</td></tr>
<tr><td><b>To</b></td><td>[Customer name / company]</td></tr><tr><td><b>Currency</b></td><td>USD, unit price per roll</td></tr></table></div>
{body}<h2>Notes</h2><ol>{''.join(f'<li>{t}</li>' for t in TERMS)}</ol></body></html>"""
    HTML(string=html).write_pdf(path)

if __name__ == "__main__":
    it = items("--skip-unpriced" in sys.argv)
    o = os.path.join(K, "out", "quote"); os.makedirs(o, exist_ok=True)
    base = os.path.join(o, "Southern-Machinery-Price-List-SMT-Stencil-Wiping-Paper-Rolls-USD")
    xlsx(base + ".xlsx", it); pdf(base + ".pdf", it)
    for x in it: print(x["g"], x["code"], x["cny"], x["usd"])
