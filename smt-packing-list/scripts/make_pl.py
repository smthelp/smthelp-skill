#!/usr/bin/env python3
"""make_pl.py - Southern Machinery branded Packing List: pl.json -> XLSX (A4 portrait, live formulas) [+ PDF].

Usage:
  python3 make_pl.py <pl.json> [--out DIR] [--pdf] [--profile assets/profile.json]
  Output: DIR/PL-<pl_no>-<file_tag>[-DRAFT].xlsx (+ .pdf). DIR defaults to <pl.json dir>/out.

pl.json fields: see references/field-spec.md and templates/pl.template.json.
- Any value equal to "TO CONFIRM" prints red bold; a value that contains it gets an amber cell.
- Keys listed in "confirm" (invoice_no, po_no, incoterm, destination, port_of_loading, packing, items, marks, remarks)
  print amber. While anything is open the sheet shows a DRAFT banner and the file name ends -DRAFT.
- Never prints prices or amounts.
"""
import argparse, json, os, subprocess, sys, datetime, math
for _p in (os.environ.get("PYLIB"), "/workspace/work/pylib"):
    if _p and os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.page import PageMargins

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELLER = {}
NAVY = GREEN = TEAL = GREY = LIGHT = MUTED = None
RED, AMBER = "C00000", "FFE699"
TBC = "TO CONFIRM"
FONT = "Arial"


def load_profile(path):
    global SELLER, NAVY, GREEN, TEAL, GREY, LIGHT, MUTED, FONT, thin, BOX
    SELLER = json.load(open(path))
    st = SELLER["style"]
    NAVY, GREEN, TEAL, GREY, LIGHT, MUTED = st["navy"], st["green"], st["teal"], st["grey"], st["light"], st["muted"]
    FONT = st.get("font", "Arial")
    thin = Side(style="thin", color=MUTED)
    BOX = Border(left=thin, right=thin, top=thin, bottom=thin)


def open_items(d):
    return len(d.get("confirm", [])) + json.dumps(d, ensure_ascii=False).count(TBC)

# A C/No | B Packing | C Description | D Qty | E Unit | F N.W. | G G.W. | H LxWxH | I CBM | K L | L W | M H (hidden)
COLS = [("A", 6.5), ("B", 10), ("C", 42), ("D", 6.5), ("E", 6), ("F", 9), ("G", 9), ("H", 13), ("I", 9)]
NCOL = 9
thin = BOX = None


def font(size=9, bold=False, color=GREY, italic=False):
    return Font(name=FONT, size=size, bold=bold, color=color, italic=italic)


def fill(c):
    return PatternFill("solid", fgColor=c)


def put(ws, ref, v, size=9, bold=False, color=GREY, h="left", va="center", wrap=False, bg=None, fmt=None, italic=False):
    c = ws[ref]
    if isinstance(v, str) and v.strip() == TBC:
        color, bold = RED, True
    elif isinstance(v, str) and TBC in v:
        bg = AMBER
    c.value = v
    c.font = font(size, bold, color, italic)
    c.alignment = Alignment(horizontal=h, vertical=va, wrap_text=wrap)
    if bg:
        c.fill = fill(bg)
    if fmt:
        c.number_format = fmt
    return c


def merge(ws, r1, c1, r2, c2):
    if r2 > r1 or c2 > c1:
        ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)


def nlines(text, width, size=9):
    cap = max(1, int(width * 1.15 * 10.0 / size) - 2)
    return sum(max(1, math.ceil(len(p) / cap)) for p in str(text).split("\n"))


def fmt_date(s):
    return datetime.date.fromisoformat(s).strftime("%d %b %Y")


def build(d, out):
    conf = set(d.get("confirm", []))
    amb = lambda k: AMBER if k in conf else None
    wb = Workbook(); ws = wb.active; ws.title = "Packing List"
    for col, w in COLS:
        ws.column_dimensions[col].width = w
    for col in "KLM":
        ws.column_dimensions[col].hidden = True
    ws.sheet_view.showGridLines = False
    ps = ws.page_setup
    ps.paperSize, ps.orientation = ws.PAPERSIZE_A4, "portrait"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ps.fitToWidth, ps.fitToHeight = 1, (1 if d.get("one_page", True) else 0)
    ws.page_margins = PageMargins(left=0.4, right=0.4, top=0.45, bottom=0.6, header=0.2, footer=0.25)
    ws.print_options.horizontalCentered = True
    ws.oddFooter.left.text = f"Packing List {d['pl_no']}"
    ws.oddFooter.center.text = f"{SELLER['web']}  ·  {SELLER['email']}  ·  WhatsApp {SELLER['whatsapp']}"
    ws.oddFooter.right.text = "Page &P of &N"
    for p in (ws.oddFooter.left, ws.oddFooter.center, ws.oddFooter.right):
        p.size, p.font, p.color = 8, f"{FONT},Regular", GREY

    # letterhead
    for r, h in ((1, 26), (2, 15), (3, 15)):
        ws.row_dimensions[r].height = h
    img = XLImage(os.path.join(ROOT, "assets", SELLER.get("logo", "sm-logo.png")))
    ratio = img.height / img.width
    img.width, img.height = 165, int(165 * ratio)
    ws.add_image(img, "A1")
    put(ws, "C1", SELLER["company"], 15, True, NAVY, h="right"); merge(ws, 1, 3, 1, 9)
    put(ws, "C2", SELLER["address"], 8, h="right"); merge(ws, 2, 3, 2, 9)
    put(ws, "C3", f"Tel {SELLER['tel']}  ·  {SELLER['web']}  ·  {SELLER['email']}  ·  WhatsApp {SELLER['whatsapp']}",
        8, h="right"); merge(ws, 3, 3, 3, 9)
    ws.row_dimensions[4].height = 4
    for c in range(1, NCOL + 1):
        ws.cell(4, c).fill = fill(GREEN)
    put(ws, "A6", "PACKING LIST", 18, True, NAVY); merge(ws, 6, 1, 6, 3); ws.row_dimensions[6].height = 26
    n_open = open_items(d)
    if n_open:
        put(ws, "D6", "DRAFT - fields marked amber / red to confirm", 9, True, RED, h="right"); merge(ws, 6, 4, 6, 9)

    # parties | document data
    cg = d["consignee"]
    left = [("Seller / Exporter", SELLER["company"]), ("Consignee", cg["company"]), ("Address", cg["address"]),
            ("Attn", cg.get("attn", "")), ("Tel", cg.get("tel", "")), ("Email", cg.get("email", ""))]
    right = [("PL No.", d["pl_no"], None), ("Date", fmt_date(d["date"]), None),
             ("Invoice No.", d["invoice_no"], amb("invoice_no")), ("PO No.", d["po_no"], amb("po_no")),
             ("Packages", d["packages_text"], None), ("Country of origin", d.get("origin", SELLER["pl"]["country_of_origin"]), None)]
    r = 8
    for (lk, lv), (rk, rv, rb) in zip(left, right):
        put(ws, f"A{r}", lk, 9, True, NAVY, bg=LIGHT); merge(ws, r, 1, r, 2)
        put(ws, f"C{r}", lv, 9, wrap=True, bg=LIGHT); merge(ws, r, 3, r, 5)
        put(ws, f"F{r}", rk, 9, True, NAVY, bg=LIGHT); merge(ws, r, 6, r, 7)
        put(ws, f"H{r}", rv, 9, bg=rb or LIGHT, wrap=True); merge(ws, r, 8, r, 9)
        for c in (1, 2, 3, 4, 5, 6, 7):
            ws.cell(r, c).fill = fill(LIGHT)
        ws.row_dimensions[r].height = 14 * max(nlines(lv, 54), nlines(rv, 22)) + 2
        r += 1
    r += 1

    # shipment
    put(ws, f"A{r}", "SHIPMENT", 10, True, NAVY); merge(ws, r, 1, r, 9)
    for c in range(1, NCOL + 1):
        ws.cell(r, c).border = Border(bottom=Side(style="thin", color=GREEN))
    r += 1
    for k, label in (("port_of_loading", "Port of loading"), ("destination", "Destination"),
                     ("incoterm", "Delivery terms")):
        put(ws, f"A{r}", label, 9, True, NAVY); merge(ws, r, 1, r, 2)
        put(ws, f"C{r}", d.get(k) or SELLER["pl"].get(k, TBC), 9, bg=amb(k)); merge(ws, r, 3, r, 9)
        r += 1
    r += 1

    # table
    hdr = ["C/No.", "Packing", "Description of goods", "Qty", "Unit", "N.W. (kg)", "G.W. (kg)", "L × W × H (cm)", "CBM (m³)"]
    for i, t in enumerate(hdr, 1):
        c = ws.cell(r, i); c.value = t; c.font = font(9, True, "FFFFFF")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.fill = fill(NAVY); c.border = BOX
    ws.row_dimensions[r].height = 28
    hdr_row = r
    r += 1
    first = r
    units = {}
    for pk in d["packages"]:
        r1 = r
        for it in pk["items"]:
            put(ws, f"C{r}", it["desc"], 9, wrap=True, va="top", bg=amb("items"))
            q = put(ws, f"D{r}", it["qty"], 9, h="center", va="top", fmt="0")
            put(ws, f"E{r}", it["unit"], 9, h="center", va="top")
            units.setdefault(it["unit"], []).append(f"D{r}")
            first_line_bold = ws[f"C{r}"]
            ws.row_dimensions[r].height = 11.6 * nlines(it["desc"], 48) + 4
            r += 1
        r2 = r - 1
        put(ws, f"A{r1}", pk["cno"], 9, True, h="center")
        put(ws, f"B{r1}", pk["packing"], 9, h="center", wrap=True, bg=amb("packing"))
        put(ws, f"F{r1}", pk["nw"], 9, h="right", fmt="0.00")
        put(ws, f"G{r1}", pk["gw"], 9, h="right", fmt="0.00")
        ws[f"K{r1}"], ws[f"L{r1}"], ws[f"M{r1}"] = pk["L"], pk["W"], pk["H"]
        put(ws, f"H{r1}", f'=K{r1}&" × "&L{r1}&" × "&M{r1}', 9, h="center")
        put(ws, f"I{r1}", f"=K{r1}*L{r1}*M{r1}/1000000", 9, h="right", fmt="0.0000")
        for col in (1, 2, 6, 7, 8, 9):
            merge(ws, r1, col, r2, col)
            ws.cell(r1, col).alignment = Alignment(horizontal=ws.cell(r1, col).alignment.horizontal,
                                                   vertical="center", wrap_text=True)
        for rr in range(r1, r2 + 1):
            for c in range(1, NCOL + 1):
                ws.cell(rr, c).border = BOX
    last = r - 1
    # totals
    npk = len(d["packages"])
    put(ws, f"A{r}", "TOTAL", 9, True, "FFFFFF", bg=NAVY); merge(ws, r, 1, r, 2)
    put(ws, f"C{r}", f"{npk} {d['package_word']}", 9, True, "FFFFFF", bg=NAVY)
    if len(units) == 1:
        u = next(iter(units))
        put(ws, f"D{r}", f"=SUM(D{first}:D{last})", 9, True, "FFFFFF", h="center", bg=NAVY, fmt="0")
        put(ws, f"E{r}", u, 9, True, "FFFFFF", h="center", bg=NAVY)
    else:
        for c in "DE":
            ws[f"{c}{r}"].fill = fill(NAVY)
    put(ws, f"F{r}", f"=SUM(F{first}:F{last})", 9, True, "FFFFFF", h="right", bg=NAVY, fmt="0.00")
    put(ws, f"G{r}", f"=SUM(G{first}:G{last})", 9, True, "FFFFFF", h="right", bg=NAVY, fmt="0.00")
    ws[f"H{r}"].fill = fill(NAVY)
    put(ws, f"I{r}", f"=SUM(I{first}:I{last})", 9, True, "FFFFFF", h="right", bg=NAVY, fmt="0.0000")
    for c in range(1, NCOL + 1):
        ws.cell(r, c).border = BOX
    ws.row_dimensions[r].height = 18
    tot = r
    r += 2

    # shipping marks + remarks
    put(ws, f"A{r}", "SHIPPING MARKS", 10, True, NAVY); merge(ws, r, 1, r, 3)
    put(ws, f"D{r}", "REMARKS", 10, True, NAVY); merge(ws, r, 4, r, 9)
    for c in range(1, NCOL + 1):
        ws.cell(r, c).border = Border(bottom=Side(style="thin", color=GREEN))
    r += 1
    rem = "\n".join(f"{i}. {t}" for i, t in enumerate(d["remarks"], 1))
    put(ws, f"A{r}", d["marks"], 9, True, NAVY, wrap=True, va="top", bg=amb("marks") or LIGHT); merge(ws, r, 1, r, 3)
    put(ws, f"D{r}", rem, 9, wrap=True, va="top", bg=amb("remarks")); merge(ws, r, 4, r, 9)
    ws.row_dimensions[r].height = 11.6 * max(nlines(d["marks"], 58), nlines(rem, 52)) + 4
    r += 2

    # signature
    put(ws, f"F{r}", f"For and on behalf of\n{SELLER['company']}", 9, True, NAVY, wrap=True, va="top")
    merge(ws, r, 6, r, 9); ws.row_dimensions[r].height = 28
    r += 3
    for c in range(6, 10):
        ws.cell(r, c).border = Border(top=Side(style="thin", color=GREY))
    put(ws, f"F{r}", (d.get("signer") + "    " if d.get("signer") else "") + "Authorized signature & company stamp", 8)
    merge(ws, r, 6, r, 9)
    ws.print_area = f"A1:I{r}"
    ws.print_title_rows = f"{hdr_row}:{hdr_row}"
    wb.save(out)
    return out


def soffice():
    for c in (os.environ.get("SOFFICE"), "soffice", "libreoffice",
              "/workspace/work/lo/root/opt/libreoffice26.8/program/soffice.bin"):
        if c and (os.path.exists(c) or subprocess.run(["which", c], capture_output=True).returncode == 0):
            return c


def to_pdf(xlsx):
    s = soffice()
    if not s:
        print("WARN no LibreOffice found; skip PDF (set SOFFICE=/path/to/soffice)", file=sys.stderr)
        return None
    outdir = os.path.dirname(os.path.abspath(xlsx))
    env = dict(os.environ, SAL_USE_VCLPLUGIN="svp")
    pdf = os.path.splitext(os.path.abspath(xlsx))[0] + ".pdf"
    for _ in range(2):
        subprocess.run([s, "--headless", "--invisible", "--norestore", "-env:UserInstallation=file:///tmp/lo_smpl",
                        "--convert-to", "pdf", "--outdir", outdir, xlsx], env=env, capture_output=True, timeout=180)
        if os.path.exists(pdf):
            return pdf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pl")
    ap.add_argument("--out")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--profile", default=os.path.join(ROOT, "assets", "profile.json"))
    a = ap.parse_args()
    load_profile(a.profile)
    d = json.load(open(a.pl))
    outdir = a.out or os.path.join(os.path.dirname(os.path.abspath(a.pl)), "out")
    os.makedirs(outdir, exist_ok=True)
    suffix = "-DRAFT" if open_items(d) else ""
    x = build(d, os.path.join(outdir, f"PL-{d['pl_no']}-{d['file_tag']}{suffix}.xlsx"))
    print(x)
    if a.pdf:
        print(to_pdf(x))


if __name__ == "__main__":
    main()
