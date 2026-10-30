#!/usr/bin/env python3
"""extract_quote.py - turn an old Southern Machinery quotation (.xlsx / .xls, legacy layout) into a quote.json draft.

Usage:
  python3 extract_quote.py <old.xlsx|old.xls> [-o kit_dir]     # writes kit_dir/quote.json + kit_dir/photos/

Legacy layout handled (all quotations 2025-2026): header labels T0:/TO:, Add:, Attn:, Mail:, Tel:, Quotation No.,
Date, Prepared by, Time of Delivery, Validity, Terms of Payment; item table with Item / Model / Description / Qty /
Unit Price / Total; spec lines under each item; "Packing cost" line; "Remark" block with numbered terms; optional
detail sheets (one per machine) whose items match summary models. Photos (xlsx only) are saved and linked to the
item whose rows they sit on.

The draft keeps the source wording; rewrite specs/terms in clean English (references/terms-library.md) before
rendering, then run qa_quote.py. Anything not found is left empty for qa_quote.py to flag.
"""
import argparse, datetime as dt, json, os, re, sys


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def nmodel(m):
    return re.sub(r"[^A-Z0-9]", "", str(m).upper())


def num(v):
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(",", "").strip())
    except Exception:
        return None


class Sheet:
    """Uniform grid: cells[(r, c)] -> value (1-based); formulas kept as text; images [(row, col, bytes, ext)]."""

    def __init__(self, title, cells, images, datemode=None):
        self.title, self.cells, self.images, self.datemode = title, cells, images, datemode
        self.maxr = max([r for r, _ in cells] or [0])
        self.maxc = max([c for _, c in cells] or [0])

    def get(self, r, c):
        return self.cells.get((r, c))

    def row(self, r):
        return [(c, self.cells[(r, c)]) for c in range(1, self.maxc + 1) if (r, c) in self.cells]


def load_sheets(path):
    sheets = []
    if path.lower().endswith(".xls"):
        import xlrd
        b = xlrd.open_workbook(path)
        for s in b.sheets():
            cells = {}
            for r in range(s.nrows):
                for c in range(s.ncols):
                    cell = s.cell(r, c)
                    v = cell.value
                    if v in ("", None):
                        continue
                    if cell.ctype == xlrd.XL_CELL_DATE:
                        v = xlrd.xldate_as_datetime(v, b.datemode)
                    cells[(r + 1, c + 1)] = v
            sheets.append(Sheet(s.name, cells, [], b.datemode))
    else:
        import openpyxl
        wb = openpyxl.load_workbook(path)
        for ws in wb.worksheets:
            if ws.title.startswith("WpsReserved"):
                continue
            cells = {}
            for row in ws.iter_rows():
                for c in row:
                    if c.value not in (None, ""):
                        cells[(c.row, c.column)] = c.value
            imgs = []
            for im in ws._images:
                try:
                    a = im.anchor._from
                    imgs.append((a.row + 1, a.col + 1, im._data(), getattr(im, "format", "png") or "png"))
                except Exception:
                    pass
            sheets.append(Sheet(ws.title, cells, imgs))
    return sheets


LABELS = [
    ("company", r"^(T0|TO)\s*:?$"), ("address", r"^Add(ress)?\s*:?$"), ("attn", r"^Attn\s*:?$"),
    ("email", r"^(E-?)?Mail\s*:?$"), ("tel", r"^Tel\s*:?$"), ("quote_no", r"^Quotation No\.?\s*:?$"),
    ("date", r"^Date\s*:?$"), ("prepared_by", r"^Prepared by\s*:?$"), ("delivery_short", r"^Time of Delivery\s*:?$"),
    ("validity", r"^Validity\s*:?$"), ("payment_short", r"^Terms of Payment\s*:?$"),
]


def header_fields(sh, raw):
    out = {}
    for (r, c), v in sorted(sh.cells.items()):
        if r < 4 or not isinstance(v, str):
            continue
        t = norm(v)
        for key, pat in LABELS:
            if key in out or not re.match(pat, t, re.I):
                continue
            val = None
            for cc in range(c + 1, c + 4):
                if sh.get(r, cc) not in (None, ""):
                    val = sh.get(r, cc)
                    break
            out[key] = val
            if val is not None:
                raw.append((f"{sh.title}!R{r} {key}", val))
    return out


def find_table(sh):
    for r in range(1, sh.maxr + 1):
        vals = {norm(v).lower(): c for c, v in sh.row(r) if isinstance(v, str)}
        if "item" in vals and "description" in vals:
            col = {"item": vals["item"]}
            for k, names in (("model", ["model"]), ("qty", ["qty", "quantity"]), ("price", ["unit price"]),
                             ("total", ["total", "amount"])):
                for n in names:
                    if n in vals:
                        col[k] = vals[n]
            return r, col
    return None, None


def parse_items(sh, raw):
    hr, col = find_table(sh)
    if not hr:
        return [], [], None
    items, charges = [], []
    cur = None
    remark_row = None
    qc, pc = col.get("qty"), col.get("price")
    model_c = col.get("model", col["item"] + 1)
    for r in range(hr + 1, sh.maxr + 1):
        row = sh.row(r)
        if not row:
            continue
        texts = [norm(v) for c, v in row if isinstance(v, str)]
        if any(re.match(r"^Remark", t, re.I) for t in texts):
            remark_row = r
            break
        if any(re.match(r"^Total\s*[:：]?$", t, re.I) for t in texts):
            continue
        itemv = num(sh.get(r, col["item"]))
        qty = num(sh.get(r, qc)) if qc else None
        price = num(sh.get(r, pc)) if pc else None
        desc_cells = [(c, v) for c, v in row if model_c < c < (qc or 99) and isinstance(v, str)
                      and not re.match(r"^(USD|EUR|CNY|Ex-?work.*)$", norm(v), re.I)]
        desc = " ".join(norm(v) for _, v in desc_cells)
        unit = None
        if qc:
            for cc in range(qc + 1, (pc or qc + 3)):
                if isinstance(sh.get(r, cc), str):
                    unit = norm(sh.get(r, cc))
        for c, v in row:
            if isinstance(v, str):
                raw.append((f"{sh.title}!R{r}C{c}", v))
        if re.search(r"packing", desc, re.I) and price:
            charges.append({"name": desc, "qty": qty or 1, "unit": (unit or "case").lower(), "price": price, "_row": r})
            continue
        model = sh.get(r, model_c)
        if itemv is not None and (model or desc):
            lines = [norm(x) for x in str(desc_cells[0][1]).split("\n") if norm(x)] if desc_cells else [""]
            cur = {"model": norm(model or ""), "name": lines[0], "qty": qty or 1, "unit": (unit or "set").lower(),
                   "price": price, "specs": lines[1:], "options": [], "_row": r}
            items.append(cur)
            continue
        if cur is None:
            continue
        if re.match(r"^Optional\s*:?$", desc, re.I):
            continue
        if price is not None and desc:
            cur["options"].append({"name": desc, "qty": qty or 1, "unit": (unit or "pc").lower(), "price": price})
        elif desc:
            cur["specs"].append(desc)
    return items, charges, remark_row


TERM_KEYS = [("delivery", r"deliver"), ("payment", r"payment"), ("warranty", r"warrant"),
             ("insurance", r"insurance"), ("packing", r"packing|package|shipment cost"),
             ("installation", r"service|install|training|engineer"), ("other", r"other terms")]


def parse_remarks(sh, r0, raw):
    if not r0:
        return {}
    lines = []
    for r in range(r0, sh.maxr + 1):
        for c, v in sh.row(r):
            if isinstance(v, str):
                raw.append((f"{sh.title}!R{r}C{c} remark", v))
                lines += [norm(x) for x in v.split("\n") if norm(x)]
    terms = {}
    last = None
    for ln in lines:
        if re.match(r"^Remark\s*:?$", ln, re.I):
            continue
        body = re.sub(r"^(\d+[\.、)]|[A-Z]\))\s*", "", ln)
        body = re.sub(r"^(Delivery time|Payment terms|Warranty|Service( Term)?|INSURANCE|Insurance)\s*[:：]\s*", "", body,
                      flags=re.I)
        body = re.sub(r"^Payment terms\s*[:：]\s*", "", body, flags=re.I)
        key = None
        for k, pat in TERM_KEYS:
            if re.search(pat, ln, re.I):
                key = k
                break
        if re.match(r"^[A-Z]\)", ln) and last:
            key = last if not re.search(r"ex-?work|package|shipment cost", ln, re.I) else "packing"
            if re.search(r"engineer|install|training", ln, re.I):
                key = "installation"
        if not key or not body:
            continue
        if key in terms:
            terms[key] = (terms[key] if isinstance(terms[key], list) else [terms[key]]) + [body]
        else:
            terms[key] = body
        last = key if key != "packing" else last
    return terms


def extract(path, outdir):
    raw = []
    sheets = load_sheets(path)
    main = sheets[0]
    for sh in sheets:  # letterhead rows (company name, address, phone) for wording checks
        for (r, c), v in sh.cells.items():
            if r <= 3 and isinstance(v, str):
                raw.append((f"{sh.title}!R{r} header", v))
    h = header_fields(main, raw)
    items, charges, rr = parse_items(main, raw)
    terms = parse_remarks(main, rr, raw)
    # detail sheets
    for sh in sheets[1:]:
        ditems, _, _ = parse_items(sh, raw)
        for d in ditems:
            for it in items:
                if nmodel(it["model"]) == nmodel(d["model"]):
                    if it["model"] != d["model"]:
                        raw.append((f"{sh.title} model", f"MODEL_MISMATCH {it['model']} vs {d['model']}"))
                    it["specs"] = d["specs"] or it["specs"]
                    it["options"] = d["options"] or it["options"]
                    it["price"] = d["price"] if d["price"] is not None else it["price"]
                    it["sheet"] = sh.title
                    it["_drow"], it["_dsheet"] = d["_row"], sh
    # photos
    photos = []
    if outdir:
        os.makedirs(os.path.join(outdir, "photos"), exist_ok=True)

    def attach(sh, lst, rowkey):
        from io import BytesIO
        from PIL import Image
        for (r, c, data, ext) in sorted(sh.images, key=lambda x: -len(x[2])):  # biggest picture first
            if r <= 3:
                continue  # header logo
            try:
                w, hgt = Image.open(BytesIO(data)).size
                if w > 2.5 * hgt:
                    continue  # wide line-overview picture, not one item
            except Exception:
                pass
            cand = [it for it in lst if it.get(rowkey) and it.get(rowkey) <= r]
            if not cand or not outdir:
                continue
            it = max(cand, key=lambda x: x[rowkey])
            if it.get("photo"):
                continue
            fn = f"photos/{re.sub(r'[^a-z0-9]+', '-', it['model'].lower()).strip('-') or 'item'}.{ext}"
            with open(os.path.join(outdir, fn), "wb") as f:
                f.write(data)
            it["photo"] = fn
            photos.append(fn)

    attach(main, items, "_row")
    for sh in sheets[1:]:
        attach(sh, [it for it in items if it.get("_dsheet") is sh], "_drow")
    for it in items:
        for k in ("_row", "_drow", "_dsheet"):
            it.pop(k, None)
        if not it["options"]:
            it.pop("options")
        if it["price"] is None:
            it["price"] = 0
    for c in charges:
        c.pop("_row", None)
    qn = norm(h.get("quote_no") or "")
    date = h.get("date")
    if isinstance(date, dt.datetime):
        date = date.date().isoformat()
    elif isinstance(date, (int, float)):
        date = (dt.date(1899, 12, 30) + dt.timedelta(days=int(date))).isoformat()
    elif not date or "NOW" in str(date).upper():
        m = re.match(r"^[A-Z]{2}(\d{2})(\d{2})(\d{2})\d{2}$", qn)
        date = f"20{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""
    vd = re.search(r"(\d+)", str(h.get("validity") or ""))
    attn = norm(h.get("attn") or "")
    email = norm(h.get("email") or "")
    m = re.search(r"<([^>]+@[^>]+)>", attn)
    if m:
        email = email or m.group(1)
        attn = norm(attn.replace(m.group(0), ""))
    inco = "EXW"
    place = "Shenzhen, China"
    q = {
        "quote_no": qn, "date": date, "valid_days": int(vd.group(1)) if vd else 30, "project": "",
        "prepared_by": norm(h.get("prepared_by") or ""),
        "buyer": {"company": norm(h.get("company") or ""), "address": norm(h.get("address") or ""), "country": "",
                  "attn": attn, "email": email, "tel": norm(h.get("tel") or "")},
        "currency": "USD", "incoterm": inco, "place": place,
        "layout": "detail" if any(it.get("sheet") for it in items) else "single",
        "items": items, "charges": charges, "terms": terms,
        "_source": os.path.basename(path),
    }
    if outdir:
        with open(os.path.join(outdir, "quote.json"), "w", encoding="utf-8") as f:
            json.dump(q, f, ensure_ascii=False, indent=1)
    return q, raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    out = a.out or os.path.splitext(os.path.basename(a.src))[0].replace(" ", "-")
    q, _ = extract(a.src, out)
    print(f"OK {out}/quote.json  items {len(q['items'])}  charges {len(q['charges'])}  terms {list(q['terms'])}")


if __name__ == "__main__":
    main()
