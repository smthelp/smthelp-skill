#!/usr/bin/env python3
"""build_pi.py - merge a customer PO and our quotation into pi.json + a field-mapping / check summary.

Usage:
  python3 build_pi.py --po po.json [--quote quote.json] [--decisions decisions.json]
                      [--pi-no KA26103001] [--date 2026-10-30] [-o pis/<PI_NO>]

Inputs (all JSON, see examples/_template):
  po.json        the customer's purchase order, transcribed literally (never "corrected" by hand).
  quote.json     our quotation in smt-quotation format (optional; without it every price is CONFIRM).
  decisions.json Jason's answers: {"pi_no": "...", "date": "...", "prepared_by": "...",
                 "resolve": {"<issue id>": "accept" | {"value": <new value>}},
                 "lines": {"1": ["H.S. code: 8479899990"]}, "notes": ["..."], "show_tax_id": true}

Outputs in -o (default: pis/<pi_no>/ next to po.json):
  pi.json                         data for make_pi.py, each field with its source; issues[] with status
  PI-<no>-mapping.md / -check.xlsx  field mapping + check summary (conflicts, missing, assumptions)

Merge rules (references/merge-rules.md is the full table):
  identity & logistics (buyer, ship-to, PO no., qty, requested date)   -> PO wins
  commercial terms (unit price, payment, lead time, warranty, charges) -> quotation wins for the draft
  every PO <-> quotation difference, missing value or profile default is recorded as an issue:
    CONFIRM   conflict or something Jason must decide        (blocks release until resolved)
    MISSING   no source gives the value; printed as TO_CONFIRM (blocks release)
    ASSUMED   taken from a profile default or a fixed rule    (listed, does not block)
    INFO      harmless difference, e.g. our spelling of a model kept
Nothing is inferred: no tax, discount, freight or price is invented.
"""
import argparse, copy, datetime as dt, difflib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INCOTERMS = {"EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"}
TBC = "TO_CONFIRM"


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def norm(s):
    return re.sub(r"[^A-Z0-9]", "", str(s or "").upper())


def ntext(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9%/ ]", " ", str(s or "").lower())).strip()


def blank(v):
    return v is None or (isinstance(v, str) and not v.strip())


def num(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = re.sub(r"[^\d.,-]", "", str(v))
    if s.count(",") and s.count("."):
        s = s.replace(",", "")
    elif s.count(",") == 1 and len(s.split(",")[1]) != 3:
        s = s.replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def money(x):
    return "" if x is None else f"{x:,.2f}"


def charge_kind(name):
    n = str(name).lower()
    if re.search(r"freight|shipping|ship cost|courier|\bdhl\b|fedex|\bups\b|\btnt\b|air ?transport|sea ?transport|delivery cost", n):
        return "freight"
    if re.search(r"pack|\bcase|crate|carton|pallet", n):
        return "packing"
    if re.search(r"install|training|commission|travel", n):
        return "service"
    if re.search(r"mold|mould|tooling", n):
        return "tooling"
    return "other:" + norm(name)[:20]


def pay_sig(s):
    """Comparable signature of a payment term: the percentages and their trigger words."""
    t = ntext(s)
    pcts = re.findall(r"(\d{1,3})\s*%", t)
    trig = sorted(set(re.findall(r"advance|deposit|before shipment|after shipment|against|b/?l|delivery|"
                                 r"installation|acceptance|l/?c|net ?\d+|days", t)))
    return (tuple(pcts), tuple(trig))


def weeks_max(s):
    """Upper bound of a lead time text in days, or None."""
    t = ntext(s).replace("~", "-")
    m = re.search(r"(\d+)\s*(?:-|to)?\s*(\d+)?\s*(working days|days|day|weeks|week|months|month)", t)
    if not m:
        return None
    n = int(m.group(2) or m.group(1))
    unit = m.group(3)
    return n * (7 if "week" in unit else 30 if "month" in unit else 1)


class Builder:
    def __init__(self, po, quote, profile, decisions, args):
        self.po, self.q, self.p, self.d, self.a = po, quote or {}, profile, decisions or {}, args
        self.issues = []
        self.mapping = []   # rows: field, po, quote, value, rule, status, id

    # ------------------------------------------------------------ issues
    def issue(self, iid, level, field, po=None, qt=None, draft=None, note=""):
        self.issues.append({"id": iid, "level": level, "field": field, "po": po, "quote": qt,
                            "draft": draft, "note": note, "resolved": False, "resolution": None})
        return self.issues[-1]

    def row(self, field, po, qt, value, rule, status="OK", iid=""):
        self.mapping.append({"field": field, "po": po, "quote": qt, "value": value, "rule": rule,
                             "status": status, "id": iid})

    def pick(self, iid, field, po_v, qt_v, default=None, prefer="po", same=None, level_conflict="CONFIRM",
             default_label="profile default", required=True):
        """Choose a value from PO / quotation / default and record why."""
        same = same or (lambda a, b: ntext(a) == ntext(b))
        has_po, has_qt = not blank(po_v), not blank(qt_v)
        if has_po and has_qt:
            if same(po_v, qt_v):
                v = qt_v if prefer == "quote" else po_v
                self.row(field, po_v, qt_v, v, "PO = quotation")
                return v
            v = po_v if prefer == "po" else qt_v
            src = "PO" if prefer == "po" else "quotation"
            self.issue(iid, level_conflict, field, po_v, qt_v, v,
                       f"PO and quotation differ; draft uses the {src} value")
            self.row(field, po_v, qt_v, v, f"conflict -> draft = {src}", level_conflict, iid)
            return v
        if has_po:
            self.row(field, po_v, qt_v, po_v, "PO only")
            return po_v
        if has_qt:
            self.row(field, po_v, qt_v, qt_v, "quotation only (PO silent)")
            return qt_v
        if default not in (None, ""):
            self.issue(iid, "ASSUMED", field, None, None, default, f"neither PO nor quotation states it; {default_label}")
            self.row(field, None, None, default, default_label, "ASSUMED", iid)
            return default
        if required:
            self.issue(iid, "MISSING", field, None, None, TBC, "no source gives this value")
            self.row(field, None, None, TBC, "missing", "MISSING", iid)
            return TBC
        self.row(field, None, None, "", "not stated (optional)")
        return ""

    # ------------------------------------------------------------ parts
    def header(self, pi):
        po, q, d, p = self.po, self.q, self.d, self.p
        today = self.a.date or d.get("date") or dt.date.today().isoformat()
        pi["date"] = today
        self.row("PI date", None, None, today, "--date / decisions / build day")
        pino = self.a.pi_no or d.get("pi_no")
        if not pino:
            letters = (q.get("quote_no") or "")[:2] or "XX"
            pino = letters.upper() + dt.date.fromisoformat(today).strftime("%y%m%d") + "01"
            self.issue("pi_no", "ASSUMED", "PI No.", None, q.get("quote_no"), pino,
                       "built from the quotation letters + PI date + 01; check the day's sequence")
            self.row("PI No.", None, q.get("quote_no"), pino, p["pi"]["pi_no_rule"], "ASSUMED", "pi_no")
        else:
            self.row("PI No.", None, q.get("quote_no"), pino, "given by Jason")
        pi["pi_no"] = pino
        pi["po_no"] = self.pick("po_no", "PO No.", po.get("po_no"), None)
        pi["po_date"] = self.pick("po_date", "PO date", po.get("po_date"), None, required=False)
        pi["quote_ref"] = q.get("quote_no", "")
        if po.get("quote_ref") and q.get("quote_no") and norm(po["quote_ref"]) != norm(q["quote_no"]):
            self.issue("quote_ref", "CONFIRM", "Quotation ref.", po["quote_ref"], q["quote_no"], q["quote_no"],
                       "the PO quotes another quotation number - check it is the right quotation")
        self.row("Quotation ref.", po.get("quote_ref"), q.get("quote_no"), pi["quote_ref"], "quotation file used")
        if q.get("quote_no") and q.get("date"):
            vu = q.get("valid_until") or (dt.date.fromisoformat(q["date"]) +
                                          dt.timedelta(days=int(q.get("valid_days", 30)))).isoformat()
            ref = po.get("po_date") or today
            if ref > vu:
                self.issue("quote_validity", "CONFIRM", "Quotation validity", ref, vu, None,
                           f"PO dated {ref} after the quotation expired on {vu}; prices need re-approval")
        if not q:
            self.issue("quote_missing", "CONFIRM", "Quotation", None, None, None,
                       "no quotation given: every price and term comes from the PO only")
        pi["prepared_by"] = d.get("prepared_by") or q.get("prepared_by") or "Jason Wu"
        self.row("Prepared by", None, q.get("prepared_by"), pi["prepared_by"], "decisions / quotation / Jason Wu")

    def parties(self, pi):
        po, q = self.po, self.q
        pb, qb = po.get("buyer", {}), q.get("buyer", {})
        b = {}
        b["company"] = self.pick("buyer.company", "Buyer company", pb.get("company"), qb.get("company"),
                                 same=lambda x, y: norm(x).replace("LTDA", "LTD") == norm(y).replace("LTDA", "LTD"))
        b["address"] = self.pick("buyer.address", "Buyer address", pb.get("address"), qb.get("address"),
                                 level_conflict="INFO")
        b["country"] = self.pick("buyer.country", "Buyer country", pb.get("country"), qb.get("country"),
                                 level_conflict="CONFIRM")
        for k, lab in (("attn", "Attn"), ("email", "Email"), ("tel", "Tel")):
            b[k] = self.pick(f"buyer.{k}", lab, pb.get(k), qb.get(k), level_conflict="INFO", required=False)
        b["tax_id"] = self.pick("buyer.tax_id", "Buyer tax ID", pb.get("tax_id"), qb.get("tax_id"), required=False)
        b["short"] = qb.get("short") or pb.get("short") or ""
        pi["buyer"] = b
        st = po.get("ship_to") or {}
        if st.get("address"):
            pi["ship_to"] = {"company": st.get("company") or b["company"], "address": st["address"],
                             "country": st.get("country") or b["country"]}
            self.row("Ship to", st.get("address"), None, st["address"], "PO ship-to")
        else:
            pi["ship_to"] = {"company": b["company"], "address": b["address"], "country": b["country"]}
            self.issue("ship_to", "ASSUMED", "Ship to", None, None, "same as buyer",
                       "PO gives no separate delivery address; buyer address used")
            self.row("Ship to", None, None, "same as buyer", "PO silent -> buyer address", "ASSUMED", "ship_to")

    def commercial(self, pi):
        po, q, p = self.po, self.q, self.p
        dfl = p["pi"]["defaults"]
        cur_po, cur_q = po.get("currency"), q.get("currency")
        pi["currency"] = self.pick("currency", "Currency", cur_po, cur_q, dfl["currency"], prefer="quote")
        if not blank(cur_po) and not blank(cur_q) and norm(cur_po) != norm(cur_q):
            for i in self.issues:
                if i["id"] == "currency":
                    i["note"] = "currency differs: every price must be re-checked, nothing converted automatically"
        inco = self.pick("incoterm", "Delivery terms (Incoterm)", (po.get("incoterm") or "").upper() or None,
                         (q.get("incoterm") or "").upper() or None, dfl["incoterm"], prefer="quote")
        place = self.pick("place", "Named place", po.get("place"), q.get("place"), dfl["place"], prefer="quote",
                          same=lambda x, y: norm(x)[:6] == norm(y)[:6])
        pi["incoterm"], pi["place"] = inco, place
        if inco not in INCOTERMS and inco != TBC:
            self.issue("incoterm.invalid", "CONFIRM", "Delivery terms", po.get("incoterm"), q.get("incoterm"), inco,
                       "not an Incoterms 2020 rule")
        qt = q.get("terms", {})
        pi["terms"] = {}
        pi["terms"]["payment"] = self.pick("terms.payment", "Terms of payment", po.get("payment"), qt.get("payment"),
                                           dfl["payment"], prefer="quote",
                                           same=lambda x, y: pay_sig(x) == pay_sig(y))
        pi["terms"]["delivery"] = self.pick("terms.delivery", "Delivery time", po.get("delivery"),
                                            qt.get("delivery"), dfl["delivery"], prefer="quote",
                                            same=lambda x, y: weeks_max(x) == weeks_max(y))
        if po.get("delivery_date"):
            lead = weeks_max(pi["terms"]["delivery"])
            start = po.get("po_date") or pi["date"]
            if lead:
                earliest = (dt.date.fromisoformat(start) + dt.timedelta(days=lead)).isoformat()
                if po["delivery_date"] < earliest:
                    self.issue("delivery_date", "CONFIRM", "Requested delivery date", po["delivery_date"],
                               pi["terms"]["delivery"], po["delivery_date"],
                               f"PO wants {po['delivery_date']}; the quoted lead time allows delivery only by {earliest}")
            pi["delivery_date"] = po["delivery_date"]
            self.row("Requested delivery date", po["delivery_date"], None, po["delivery_date"], "PO")
        pi["terms"]["warranty"] = self.pick("terms.warranty", "Warranty", po.get("warranty"), qt.get("warranty"),
                                            dfl["warranty"], prefer="quote")
        pi["terms"]["packing"] = self.pick("terms.packing", "Packing", po.get("packing"), qt.get("packing"),
                                           dfl["packing"], prefer="quote", level_conflict="INFO")
        if qt.get("installation") or po.get("installation"):
            pi["terms"]["installation"] = self.pick("terms.installation", "Installation", po.get("installation"),
                                                    qt.get("installation"), prefer="quote")
        if inco in p["pi"]["seller_insures_incoterms"]:
            ins = self.pick("terms.insurance", "Insurance", po.get("insurance"), qt.get("insurance"), None,
                            prefer="quote")
            if blank(po.get("insurance")) and blank(qt.get("insurance")):
                pass
        elif inco in ("DAP", "DPU", "DDP"):
            ins = po.get("insurance") or qt.get("insurance") or \
                f"Transport risk is borne by the seller until delivery at the named place ({inco})"
            if not (po.get("insurance") or qt.get("insurance")):
                self.issue("terms.insurance", "CONFIRM", "Insurance", None, None, ins,
                           f"{inco}: we carry the transport risk - confirm whether we insure the shipment")
            self.row("Insurance", po.get("insurance"), qt.get("insurance"), ins, f"{inco}: seller's risk", "CONFIRM")
        else:
            ins = po.get("insurance") or qt.get("insurance") or p["pi"]["insurance_buyer"]
            self.row("Insurance", po.get("insurance"), qt.get("insurance"), ins, f"{inco}: buyer insures")
        pi["terms"]["insurance"] = ins
        if inco == "DDP":
            tx = po.get("taxes") or qt.get("taxes") or \
                "Import duties and taxes in the destination country are included (DDP)"
            if not (po.get("taxes") or qt.get("taxes")):
                self.issue("terms.taxes", "CONFIRM", "Taxes & duties", None, None, tx,
                           "DDP: we pay import duty and VAT - confirm the amount is inside the freight/price")
            pi["terms"]["taxes"] = tx
        else:
            pi["terms"]["taxes"] = qt.get("taxes") or dfl["taxes"]
        pi["shipment"] = {
            "port_of_loading": po.get("port_of_loading") or p["pi"]["port_of_loading"],
            "destination": po.get("destination") or ", ".join(x for x in [pi["ship_to"].get("country")] if x) or TBC,
            "ship_via": po.get("ship_via") or "",
            "country_of_origin": p["pi"]["country_of_origin"],
        }
        if pi["shipment"]["destination"] == TBC:
            self.issue("destination", "MISSING", "Port / place of destination", None, None, TBC, "PO gives no destination")
        self.row("Port of loading", po.get("port_of_loading"), None, pi["shipment"]["port_of_loading"],
                 "PO / profile (Shenzhen)")
        self.row("Destination", po.get("destination"), None, pi["shipment"]["destination"], "PO / ship-to country")

    def items(self, pi):
        po, q, p = self.po, self.q, self.p
        tol = p["pi"]["price_tolerance"]
        q_items = list(q.get("items", []))
        used = set()
        out = []

        def q_unit_price(it):
            a = it.get("qty", 1) * it.get("price", 0)
            for o in it.get("options", []):
                if o.get("included", True):
                    a += o.get("qty", 1) * o.get("price", 0)
            return a / (it.get("qty", 1) or 1)

        for n, pl in enumerate(po.get("items", []), 1):
            iid = f"item{n}"
            match, how = None, ""
            for j, qi in enumerate(q_items):
                if j not in used and pl.get("model") and norm(pl["model"]) == norm(qi.get("model")):
                    match, how = j, "model"
                    break
            if match is None:
                best, score = None, 0
                for j, qi in enumerate(q_items):
                    if j in used:
                        continue
                    s = difflib.SequenceMatcher(None, ntext(pl.get("name")), ntext(qi.get("name"))).ratio()
                    if s > score:
                        best, score = j, s
                if best is not None and score >= 0.6:
                    match, how = best, f"description ({score:.0%})"
            qi = q_items[match] if match is not None else None
            if match is not None:
                used.add(match)
            it = {"line": pl.get("line", n)}
            if qi is None:
                self.issue(f"{iid}.match", "CONFIRM", f"Item {n}", pl.get("model") or pl.get("name"), None, None,
                           "PO line not found in the quotation: price, description and spec need approval")
            elif how != "model":
                self.issue(f"{iid}.match", "CONFIRM", f"Item {n}", pl.get("model") or pl.get("name"),
                           qi.get("model") or qi.get("name"), qi.get("model"),
                           f"matched to the quotation by {how}, not by model - check it is the same product")
            # model / name
            if qi and qi.get("model"):
                it["model"] = qi["model"]
                if pl.get("model") and pl["model"] != qi["model"]:
                    self.issue(f"{iid}.model", "INFO", f"Item {n} model", pl["model"], qi["model"], qi["model"],
                               "our spelling kept; PO spelling shown in the mapping")
            else:
                it["model"] = pl.get("model", "")
            it["name"] = (qi or {}).get("name") or pl.get("name") or TBC
            if it["name"] == TBC:
                self.issue(f"{iid}.name", "MISSING", f"Item {n} description", None, None, TBC, "no description")
            it["customer_ref"] = pl.get("customer_part_no") or ""
            it["lines"] = list(pl.get("lines", []))
            # qty
            pq, qq = num(pl.get("qty")), (num(qi.get("qty")) if qi else None)
            if pq is None:
                it["qty"] = qq if qq is not None else TBC
                self.issue(f"{iid}.qty", "MISSING" if qq is None else "CONFIRM", f"Item {n} qty", None, qq, it["qty"],
                           "PO line has no quantity")
            else:
                it["qty"] = pq
                if qq is not None and abs(pq - qq) > 1e-9:
                    self.issue(f"{iid}.qty", "CONFIRM", f"Item {n} qty", pq, qq, pq,
                               "ordered quantity differs from the quoted quantity (price breaks, packing and lead "
                               "time may change); draft uses the PO quantity")
            it["unit"] = pl.get("unit") or (qi or {}).get("unit") or "pc"
            # price
            pp = num(pl.get("price"))
            qp = q_unit_price(qi) if qi else None
            if qi and qi.get("options"):
                self.issue(f"{iid}.options", "INFO", f"Item {n} options", None, len(qi["options"]), None,
                           "quotation unit price includes the included options")
            if pp is not None and qp is not None:
                if abs(pp - qp) > max(tol * qp, 0.005):
                    it["price"] = qp
                    self.issue(f"{iid}.price", "CONFIRM", f"Item {n} unit price", pp, qp, qp,
                               "PO price differs from the quotation; draft keeps the quoted price")
                else:
                    it["price"] = qp
            elif qp is not None:
                it["price"] = qp
                self.issue(f"{iid}.price", "ASSUMED", f"Item {n} unit price", None, qp, qp,
                           "PO shows no unit price; quoted price used")
            elif pp is not None:
                it["price"] = pp
                if qi is not None:
                    pass
                else:
                    self.issue(f"{iid}.price", "CONFIRM", f"Item {n} unit price", pp, None, pp,
                               "price only in the PO (not quoted)")
            else:
                it["price"] = TBC
                self.issue(f"{iid}.price", "MISSING", f"Item {n} unit price", None, None, TBC, "no price anywhere")
            # printed line amount
            pa = num(pl.get("amount"))
            if pa is not None and isinstance(it["qty"], float) and pp is not None and abs(pa - pp * it["qty"]) > 0.01:
                self.issue(f"{iid}.amount", "CONFIRM", f"Item {n} amount on PO", pa, None, money(pp * it["qty"]),
                           "PO line amount is not qty x unit price")
            it["hs_code"] = pl.get("hs_code") or (qi or {}).get("hs_code") or ""
            out.append(it)
            self.row(f"Item {n}", f"{pl.get('model', '')} {pl.get('name', '')} x{pl.get('qty')} @ {pl.get('price')}",
                     (f"{qi.get('model', '')} {qi.get('name', '')} x{qi.get('qty')} @ {money(qp)}" if qi else None),
                     f"{it['model']} x{it['qty']} @ {money(it['price']) if isinstance(it['price'], float) else it['price']}",
                     f"matched by {how}" if qi else "not in quotation",
                     "CONFIRM" if any(i['id'].startswith(iid + '.') and i['level'] in ('CONFIRM', 'MISSING')
                                      for i in self.issues) else "OK", iid)
        for j, qi in enumerate(q_items):
            if j not in used:
                self.issue(f"quote_item{j + 1}.not_ordered", "INFO", f"Quotation item {j + 1}", None,
                           f"{qi.get('model', '')} {qi.get('name', '')}", None, "quoted but not in the PO - left off the PI")
        pi["items"] = out

    def charges(self, pi):
        po, q = self.po, self.q
        po_c = {charge_kind(c["name"]): c for c in po.get("charges", [])}
        q_c = {charge_kind(c["name"]): c for c in q.get("charges", [])}
        out = []
        for k in list(dict.fromkeys(list(q_c) + list(po_c))):
            pc, qc = po_c.get(k), q_c.get(k)
            iid = f"charge.{k.split(':')[0]}"
            if pc and qc:
                pa = num(pc.get("qty", 1)) * num(pc.get("price"))
                qa = num(qc.get("qty", 1)) * num(qc.get("price"))
                if abs(pa - qa) > 0.01:
                    self.issue(iid, "CONFIRM", f"Charge: {qc['name']}", money(pa), money(qa), money(qa),
                               "PO and quotation amounts differ; draft keeps the quotation")
                out.append(dict(qc))
            elif qc:
                self.issue(iid, "CONFIRM", f"Charge: {qc['name']}", None, money(num(qc.get('qty', 1)) * num(qc['price'])),
                           "included", "quoted charge not shown on the PO - confirm the buyer accepts it")
                out.append(dict(qc))
            else:
                self.issue(iid, "CONFIRM", f"Charge: {pc['name']}", money(num(pc.get('qty', 1)) * num(pc['price'])),
                           None, "included", "charge only in the PO (not quoted) - confirm amount")
                out.append(dict(pc))
            self.row(f"Charge {k}", pc and money(num(pc.get('qty', 1)) * num(pc['price'])),
                     qc and money(num(qc.get('qty', 1)) * num(qc['price'])), out[-1]["name"],
                     "both" if pc and qc else "quotation only" if qc else "PO only", "CONFIRM" if not (pc and qc) else "OK", iid)
        # quantity-linked charges (packing per unit) when qty changed
        if any(i["id"].endswith(".qty") and i["level"] == "CONFIRM" for i in self.issues):
            for c in out:
                if charge_kind(c["name"]) == "packing":
                    self.issue("charge.packing.qty", "CONFIRM", f"Charge: {c['name']}", None, c.get("qty"), c.get("qty"),
                               "item quantity changed - check the number of cases / packing amount")
        m = po.get("mentions", {})
        for k, label in (("freight", "Freight"), ("tax", "Tax / VAT"), ("discount", "Discount")):
            if m.get(k):
                self.issue(f"mention.{k}", "CONFIRM", label, m[k], None, "not on PI",
                           "PO mentions it without an amount - nothing added until Jason gives the figure")
        # incoterm needs freight?
        inco = pi.get("incoterm")
        if inco in {"CPT", "CIP", "CFR", "CIF", "DAP", "DPU", "DDP"} and not any(charge_kind(c["name"]) == "freight" for c in out):
            self.issue("charge.freight.needed", "CONFIRM", "Freight", inco, None, "not on PI",
                       f"{inco} means we pay the freight, but no freight amount is given")
        pi["charges"] = out
        # discount
        pd, qd = num(po.get("discount")), num(q.get("discount"))
        if pd or qd:
            if pd and qd and abs(pd - qd) > 0.01:
                self.issue("discount", "CONFIRM", "Discount", money(pd), money(qd), money(qd), "discount differs")
                pi["discount"] = qd
            elif qd:
                pi["discount"] = qd
                if not pd:
                    self.issue("discount", "INFO", "Discount", None, money(qd), money(qd), "quoted discount carried")
            else:
                pi["discount"] = pd
                self.issue("discount", "CONFIRM", "Discount", money(pd), None, money(pd), "discount only in the PO")
        else:
            pi["discount"] = 0
        # tax
        pi["tax"] = []
        if po.get("tax"):
            self.issue("tax", "CONFIRM", "Tax / VAT", json.dumps(po["tax"]), None, "not on PI",
                       "the PO lists tax; export PIs carry no tax unless Jason says so")

    def totals(self, pi):
        items_ok = all(isinstance(i["qty"], float) or isinstance(i["qty"], int) for i in pi["items"]) and \
            all(isinstance(i["price"], (int, float)) for i in pi["items"])
        if not items_ok:
            pi["total_check"] = None
            return
        t = sum(i["qty"] * i["price"] for i in pi["items"])
        t += sum(num(c.get("qty", 1)) * num(c["price"]) for c in pi["charges"]) - abs(pi.get("discount") or 0)
        pi["total_check"] = round(t, 2)
        pt = num(self.po.get("total"))
        if pt is not None and abs(pt - t) > 0.01:
            self.issue("total", "CONFIRM", "Total", money(pt), None, money(t),
                       f"PO total {money(pt)} differs from the PI total {money(t)}")
        self.row("Total", money(pt), None, money(t), "computed")

    # ------------------------------------------------------------ decisions
    def apply_decisions(self, pi):
        res = self.d.get("resolve", {})
        for i in self.issues:
            r = res.get(i["id"])
            if r is None:
                continue
            i["resolved"] = True
            if r == "accept":
                i["resolution"] = "accepted draft"
            elif isinstance(r, dict) and "value" in r:
                i["resolution"] = f"set to {r['value']}" if r["value"] not in ("", None) else "omitted"
                self.set_path(pi, i["id"], r["value"])
        for k, v in self.d.get("lines", {}).items():
            idx = int(k) - 1
            if 0 <= idx < len(pi["items"]):
                pi["items"][idx]["lines"] = list(v)
        if "show_tax_id" in self.d:
            pi["show_tax_id"] = bool(self.d["show_tax_id"])
        pi["notes"] = list(self.po.get("pi_notes", [])) + list(self.d.get("notes", []))
        for k in ("export_control_line", "alt_payment"):
            if k in self.d:
                pi[k] = self.d[k]

    def set_path(self, pi, iid, value):
        m = re.match(r"item(\d+)\.(qty|price|name|model|unit)$", iid)
        if m:
            pi["items"][int(m.group(1)) - 1][m.group(2)] = num(value) if m.group(2) in ("qty", "price") else value
            return
        m = re.match(r"(terms|buyer)\.(\w+)$", iid)
        if m:
            pi.setdefault(m.group(1), {})[m.group(2)] = value
            return
        if iid in ("currency", "incoterm", "place", "po_no", "po_date", "pi_no", "discount"):
            pi[iid] = num(value) if iid == "discount" else value
            return
        if iid == "ship_to" and isinstance(value, dict):
            pi["ship_to"] = value
            return
        if iid == "destination":
            pi["shipment"]["destination"] = value
            return
        if iid.startswith("charge.") and isinstance(value, dict):
            k = iid.split(".")[1]
            pi["charges"] = [c for c in pi["charges"] if charge_kind(c["name"]).split(":")[0] != k]
            if value.get("price") is not None:
                pi["charges"].append(value)
            return
        if iid.startswith("charge.") and value in (None, "remove", 0):
            k = iid.split(".")[1]
            pi["charges"] = [c for c in pi["charges"] if charge_kind(c["name"]).split(":")[0] != k]

    # ------------------------------------------------------------ run
    def build(self):
        pi = {"_generated_by": "smt-proforma-invoice/build_pi.py", "show_tax_id": False}
        self.header(pi)
        self.parties(pi)
        self.commercial(pi)
        self.items(pi)
        self.charges(pi)
        self.apply_decisions(pi)
        self.totals(pi)
        # a decision may have closed issues that were re-raised by totals; re-apply resolution flags
        res = self.d.get("resolve", {})
        for i in self.issues:
            if i["id"] in res and not i["resolved"]:
                i["resolved"], i["resolution"] = True, "accepted draft"
        pi["issues"] = self.issues
        pi["sources"] = {"po": self.po.get("_source", ""), "quote": self.q.get("quote_no", "")}
        return pi


LEVEL_CN = {"CONFIRM": "待确认", "MISSING": "缺失", "ASSUMED": "假设取值", "INFO": "信息"}


def write_summary(pi, mapping, outdir):
    no = pi["pi_no"]
    iss = pi["issues"]
    open_block = [i for i in iss if i["level"] in ("CONFIRM", "MISSING") and not i["resolved"]]
    L = [f"# PI {no} 字段映射与核对摘要", "",
         f"- PO: {pi.get('po_no')}  ·  报价单: {pi.get('quote_ref') or '无'}  ·  PI 日期: {pi['date']}",
         f"- PI 合计: {pi.get('currency')} {money(pi.get('total_check')) if pi.get('total_check') is not None else 'TO_CONFIRM'}",
         f"- 未解决待确认/缺失: **{len(open_block)}**（为 0 才可放行给客户）", ""]
    for lev in ("CONFIRM", "MISSING", "ASSUMED", "INFO"):
        rows = [i for i in iss if i["level"] == lev]
        if not rows:
            continue
        L += [f"## {LEVEL_CN[lev]} ({lev})", "", "| ID | 字段 | PO | 报价单 | PI 草稿取值 | 说明 | 状态 |", "|---|---|---|---|---|---|---|"]
        for i in rows:
            st = ("已处理: " + i["resolution"]) if i["resolved"] else ("未处理" if lev in ("CONFIRM", "MISSING") else "-")
            L.append(f"| {i['id']} | {i['field']} | {i['po'] if i['po'] is not None else ''} | "
                     f"{i['quote'] if i['quote'] is not None else ''} | {i['draft'] if i['draft'] is not None else ''} | "
                     f"{i['note']} | {st} |")
        L.append("")
    L += ["## 字段映射", "", "| 字段 | PO | 报价单 | PI 取值 | 规则 | 状态 |", "|---|---|---|---|---|---|"]
    for m in mapping:
        L.append(f"| {m['field']} | {m['po'] if m['po'] is not None else ''} | {m['quote'] if m['quote'] is not None else ''} | "
                 f"{m['value']} | {m['rule']} | {m['status']} |")
    md = os.path.join(outdir, f"PI-{no}-mapping.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        wb = Workbook()
        ws = wb.active
        ws.title = "Check"
        ws.append(["ID", "Level", "Field", "PO", "Quotation", "PI draft", "Note", "Status"])
        fills = {"CONFIRM": "FFE699", "MISSING": "F4B6B6", "ASSUMED": "DDEBF7", "INFO": "EDEDED"}
        for i in iss:
            ws.append([i["id"], i["level"], i["field"], str(i["po"] or ""), str(i["quote"] or ""), str(i["draft"] or ""),
                       i["note"], ("resolved: " + i["resolution"]) if i["resolved"] else "open"])
            for c in ws[ws.max_row]:
                c.fill = PatternFill("solid", fgColor=fills[i["level"]])
                c.alignment = Alignment(wrap_text=True, vertical="top")
        ws2 = wb.create_sheet("Mapping")
        ws2.append(["Field", "PO", "Quotation", "PI value", "Rule", "Status"])
        for m in mapping:
            ws2.append([m["field"], str(m["po"] or ""), str(m["quote"] or ""), str(m["value"]), m["rule"], m["status"]])
        for w in (ws, ws2):
            for c in w[1]:
                c.font = Font(bold=True)
            for col, wd in zip("ABCDEFGH", (18, 10, 24, 28, 28, 24, 60, 18)):
                w.column_dimensions[col].width = wd
        wb.save(os.path.join(outdir, f"PI-{no}-check.xlsx"))
    except ImportError:
        pass
    return md, open_block


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--po", required=True)
    ap.add_argument("--quote")
    ap.add_argument("--decisions")
    ap.add_argument("--pi-no")
    ap.add_argument("--date")
    ap.add_argument("--profile", default=os.path.join(ROOT, "assets", "profile.json"))
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    po = load(a.po)
    po.setdefault("_source", os.path.basename(a.po))
    quote = load(a.quote) if a.quote else {}
    dec = load(a.decisions) if a.decisions and os.path.exists(a.decisions) else {}
    b = Builder(po, quote, load(a.profile), dec, a)
    pi = b.build()
    outdir = a.out or os.path.join(os.path.dirname(os.path.abspath(a.po)))
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "pi.json"), "w", encoding="utf-8") as f:
        json.dump(pi, f, ensure_ascii=False, indent=1)
    md, open_block = write_summary(pi, b.mapping, outdir)
    counts = {}
    for i in pi["issues"]:
        counts[i["level"]] = counts.get(i["level"], 0) + 1
    print(f"OK {os.path.join(outdir, 'pi.json')}  PI {pi['pi_no']}  total {pi.get('currency')} "
          f"{money(pi.get('total_check')) if pi.get('total_check') is not None else 'TO_CONFIRM'}")
    print("issues", counts, f"open blocking: {len(open_block)}")
    for i in open_block:
        print(f"  {i['level']:8} {i['id']:28} {i['note']}")
    print(f"summary {md}")


if __name__ == "__main__":
    main()
