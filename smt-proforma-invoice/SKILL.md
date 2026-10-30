---
name: smt-proforma-invoice
description: Make Southern Machinery proforma invoices (PI / 形式发票) in the branded Excel + PDF format from a customer PO and our quotation. Use when Jason asks to 做PI, 开形式发票, 出PI, 根据客户PO做PI, 把报价单转成PI, convert/re-issue an old PI, or check a PI against the PO. Merges PO + quotation field by field, never guesses: conflicts, quantity changes, missing fields, discount/freight/tax that are not stated are marked "to confirm" and block release until Jason answers. Outputs PI XLSX/PDF plus a field-mapping and check summary (conflicts, missing items, assumptions).
metadata:
  version: 1.0.0
  updated: 2026-10-30
  depends_on: smt-quotation (quote.json format, seller profile, brand), smt-brand-kit (logo, colours)
  samples: TUK25093001, SA25102501, AR25120201, JP25121601/JP25122201 (CNY), PC26011401, IS2026032001
---

# SMT Proforma Invoice - customer PO + our quotation -> one branded PI

```
customer PO (pdf/xlsx/email) --transcribe--> po.json ─┐
our quotation (smt-quotation) ------------> quote.json ┼─build_pi.py─> pi.json + PI-<no>-mapping.md/-check.xlsx
Jason's answers ------------------------> decisions.json┘        │
                                             make_pi.py ─> out/PI-<no>-<buyer>.xlsx (+PDF) ─> qa_pi.py ─> Jason
```
One PI = one folder `pis/<PI_NO>/` with `po.json`, `quote.json`, `decisions.json`, `pi.json`, `out/`.
Seller, bank and style come from `assets/profile.json` (kept identical to smt-quotation; qa_pi.py checks it).

## When to use
- Customer sends a PO after our quotation -> PI for payment.  - Customer asks for a PI without a formal PO (PO No. "Verbal order <date>", Jason must say so).
- Re-issue an old PI in the new format (rebuild po.json from the old PI, see `examples/prosser-PC26011401`).
- Check a PI someone made against the PO (run build_pi.py, read the CONFIRM list).
Not for: quotations (smt-quotation), commercial invoices / packing lists for customs (different document).

## Files
- `assets/profile.json` - company, address, contact, sales people, bank (+ country, account type, bank code 007), style, and `pi`: number rule, seller tax ID (61178505-000-03-20-0, printed only when `show_tax_id`), country of origin, port of loading, CNY WeChat/Alipay line, export-control line, PI defaults.
- `scripts/build_pi.py` - merge PO + quotation + decisions -> `pi.json` and the mapping/check summary (`.md` for chat, `-check.xlsx` with Check + Mapping sheets).
- `scripts/make_pi.py` - pi.json -> XLSX (A4, live formulas, amber cells for open issues, "DRAFT - n item(s) to confirm" banner) and `--pdf` via LibreOffice.
- `scripts/qa_pi.py` - release gate; exit code 1 while any ERROR.
- `references/field-mapping.md` - every PI field: where it comes from (PO / quotation / profile) and how it prints.
- `references/merge-rules.md` - precedence, conflict levels and the confirmation list. `references/checklist.md` - human check before release.
- `examples/_template/` (po.json, decisions.json), `examples/demo-creationtech/` (quote CT26102801 + DEMO PO with 6 conflicts: `draft/` before answers, `out/` after), `examples/prosser-PC26011401/` (real 2026-01 PI rebuilt, PO-only, DDP + DHL freight).

## Inputs
1. **po.json** - transcribe the customer PO literally (pdf: pdftotext / pdf-tools; xlsx: openpyxl; scan: read the image). Copy numbers and words as printed; leave a field out when the PO is silent. Never fill PO fields from the quotation - that is build_pi.py's job and it records the source.
2. **quote.json** - the smt-quotation file that the PO refers to (`reviews/<QUOTE_NO>/quote.json` or `quotes/<NO>/`). Optional; without it every price is CONFIRM.
3. **decisions.json** (optional, grows with Jason's answers) - `pi_no`, `date`, `prepared_by`, `show_tax_id`, `export_control_line`, `resolve` {issue id: "accept" | {"value": x}}, `lines` {item no: ["H.S. code: ..."]}, `notes`.

## Workflow
1. `mkdir pis/<PI_NO>`; write po.json from the PO; copy the quotation's quote.json.
2. `python3 scripts/build_pi.py --po po.json --quote quote.json [--decisions decisions.json] --pi-no <NO> --date <YYYY-MM-DD> -o .`
3. `python3 scripts/make_pi.py pi.json --pdf` -> look at every PDF page.
4. `python3 scripts/qa_pi.py pi.json --xlsx out/*.xlsx`.
5. **Deliver to Jason** (never to the customer), in Chinese: PI XLSX + PDF (draft while issues are open) + the summary: open CONFIRM / MISSING items as short questions, ASSUMED values in one line.
6. Jason answers -> write them into decisions.json -> repeat 2-4 until qa_pi.py shows 0 ERROR -> deliver the final PI.
7. **Learn**: a new rule from Jason goes where it lives (profile `pi`, merge rule in build_pi.py + merge-rules.md, check in qa_pi.py), re-run both examples, bump version, add a history line, push.

## Merge rules (short; full table in references/merge-rules.md)
- PO wins for identity and logistics: buyer, ship-to, PO No./date, ordered quantity, requested date, customer part numbers, HS codes.
- Quotation wins for the draft of commercial terms: unit price, payment, lead time, warranty, packing, installation, charges, discount, currency, Incoterm. A different PO value is never adopted silently.
- Levels: **CONFIRM** (conflict or decision) and **MISSING** (no source; prints red TO_CONFIRM) block release; **ASSUMED** (profile default or fixed rule) is listed; **INFO** is harmless.
- Always CONFIRM: any PO vs quotation difference in price, qty, payment, lead time, currency, Incoterm, warranty, charges, discount, total; PO line not in the quotation or matched only by description; quotation expired at PO date; PO quotes another quotation No.; PO mentions freight / tax / discount without an amount; C- or D-terms without a freight amount; DAP/DPU/DDP insurance; DDP duties; packing count when quantity changed; any tax line.
- Quoted items not in the PO are left off and listed (INFO). Model spelling: ours is printed, the PO's is kept in the mapping.
- Nothing is invented: no tax, discount, freight, price, warranty or date that no source states.

## Fixed rules (brand + document)
- Same letterhead, colours, Arial, contact block and bank block as smt-quotation: `Southern Machinery Sales and Service Co., Limited` everywhere (= bank beneficiary); no fax line; no 'Shenzhen' prefix.
- PI No. = 2 letters (same as the quotation / customer) + YYMMDD (PI date) + 2-digit sequence, e.g. KA26103001. Dates print as `30 Oct 2026`; never =NOW().
- Header block: To / Address / Attn / Email / Tel / [Tax ID] / Ship to  |  PI No. / Date / PO No. / PO date / Quotation ref. / Currency.
- Shipment & payment block: port of loading, destination, delivery terms `<Incoterm> <place> (Incoterms® 2020)`, delivery time with a start point, terms of payment (adds to 100 %), insurance consistent with the Incoterm, [shipment by], [requested date], country of origin, [seller tax ID].
- Table: Item | Model / P/N | Description of goods (+ "Your P/N", "H.S. code" lines) | Qty | Unit | Unit price (CUR) | Amount (CUR); charges and discount below the subtotal; TOTAL line names Incoterm, place and currency; amount in words.
- CNY PIs print the WeChat / Alipay line under the bank details; USD/EUR use the JPMorgan HK account only.
- Remarks: warranty, packing, installation, taxes & duties, notes, optional export-control line, "quote the PI number with your payment".

## Upgrading
- Seller/bank change: change smt-quotation profile first, copy to this profile (qa_pi.py fails until both match).
- Version: major = po.json/pi.json format change; minor = new field/rule/output; patch = fixes.

## Version history
- 1.0.0 (2026-10-30) - first release from 7 PIs (2025-09 to 2026-03): PO + quotation merge with CONFIRM / MISSING / ASSUMED / INFO issues and decisions loop, branded PI renderer (draft banner, amber open cells), mapping/check summary (.md + .xlsx), release gate, demo + real examples.
