---
name: smt-packing-list
description: Make or review Southern Machinery packing lists (PL / 装箱单) in the branded Excel + PDF format, issued by Southern Machinery Sales and Service Co., Limited (Hong Kong company name, Shenzhen office address) to match the commercial invoice of the same shipment. Use when Jason asks to 做/开 Packing List、出装箱单、把旧装箱单改成品牌版、统一 PL 模板、审核发给客户的 PL（品名、件数、尺寸重量、CBM、唛头、与发票一致性）. Never guesses: PO No., Incoterm, serial numbers, ISPM 15 status or anything without a source is marked TO CONFIRM and keeps the PL in DRAFT until Jason answers.
metadata:
  version: 1.0.0
  updated: 2026-11-02
  depends_on: smt-commercial-invoice (seller profile, numbering, CI data), smt-brand-kit (logo, colours), smt-proforma-invoice (document style)
  samples: JA26050401 (Jabil Hungary, final), JA26030401 (Jabil Ukraine, draft), DG24050801 (Thai DGT S3020A, draft)
---

# SMT Packing List - shipment data -> one branded packing list (XLSX + PDF)

```
CI (smt-commercial-invoice) + warehouse packing data --transcribe--> pls/<NO>/pl.json
                                                      make_pl.py ──> out/PL-<NO>-<tag>[-DRAFT].xlsx + .pdf
Jason's answers -> pl.json (values, confirm[] emptied) └─ qa_pl.py [--ci ci.json] ─> 0 ERROR = FINAL OK
```

## 1. Trigger (when to load)
- 中文：做 Packing List、开装箱单、出 PL、装箱单改品牌版、统一装箱单模板、审核/核对装箱单、唛头、毛净重/体积核对、PL 与发票对不上。
- English: packing list, PL, re-issue packing list in our format, check our packing lists, shipping marks.

## 2. Scope
| Use for | Not for |
|---|---|
| Export packing lists to customers (goods ordered, packed) | Commercial invoice -> `smt-commercial-invoice` |
| Re-issuing old WPS / Excel PLs in the brand format | Proforma invoice -> `smt-proforma-invoice`; quotation -> `smt-quotation` |
| Auditing PLs someone else made (brand, data, arithmetic, CI match) | Courier waybills, booking notes, certificates of origin |
| Samples, spare parts, machines in cartons / crates / pallets | Sending anything to a customer - Jason sends |

## 3. Inputs (checklist)
Required
1. CI of the same shipment: invoice No. (= PL No.), date, PO No., Incoterm, item descriptions, qty, units, H.S. codes.
2. Consignee legal name and full address (PO / CI); contact if on the CI.
3. Per package: C/No., packing type (carton / wooden crate / pallet), L × W × H in cm, N.W. and G.W. in kg, which items and how many are inside.
4. Machines: serial number per unit. Wooden packing: ISPM 15 / IPPC status.
Optional: notify party, shipping-mark wording from the buyer, signer (default Leo Liao), destination city.
Fixed (never typed per PL): seller, address, contacts, logo, style, origin default China, port of loading Shenzhen -> `assets/profile.json`.

## 4. Outputs
- `out/PL-<NO>-<tag>.xlsx` - A4 portrait, one page, live formulas (CBM per package, SUM totals for qty, N.W., G.W., CBM), brand letterhead and footer, dimensions kept in hidden columns K:M.
- `out/PL-<NO>-<tag>.pdf` - same via LibreOffice.
- While anything is open: name ends `-DRAFT`, red "DRAFT" banner, amber cells for `confirm[]` keys, red `TO CONFIRM`.
- Audits: `reviews/<date>-pl-review.md` (per PL: 级别 高/中/低, 位置, 现文, 建议; cross-file differences; recommended standard) + Chinese summary to Jason.

## 5. Steps
1. **Setup** (once per environment): `pip install --target <pylib> openpyxl` (and `xlrd` to read old .xls); LibreOffice for PDF (`SOFFICE=/path/to/soffice` if not on PATH). Run with `PYLIB=<pylib>` or `PYTHONPATH=<pylib>`.
2. **Read the sources**: old PL PDF -> `pdftotext -layout` + look at the page image (logo, layout, stamp); old .xls -> xlrd with `formatting_info=True` (all sheets, merged cells), then LibreOffice -> xlsx -> openpyxl to see formulas (`=NOW()`, hard-coded volumes). Recompute every total.
3. **Transcribe**: copy `templates/pl.template.json` to `pls/<NO>/pl.json`; fill from CI + packing data literally. Wording per `references/glossary-cn-en.md`; fields per `references/field-spec.md`. PL No. = CI No.
4. **Flag, don't guess**: unknown value -> `"TO CONFIRM"`; value you took from a weaker source (e.g. Incoterm from other invoices of the same buyer) -> add its key to `confirm[]`.
5. **Render**: `python3 scripts/make_pl.py pls/<NO>/pl.json --pdf`.
6. **Check**: `python3 scripts/qa_pl.py pls/<NO>/pl.json --xlsx pls/<NO>/out/*.xlsx [--ci <ci.json>]`; open the PDF image - one page, no clipped text, no overlap.
7. **Deliver to Jason** in Chinese: PDF + XLSX, one short question per open item. Never to the customer.
8. **Answers**: write them into pl.json, empty `confirm[]`, repeat 5-6 until `0 ERROR -> FINAL OK`, deliver the final files.
9. **Learn**: new rule -> profile `pl`, qa_pl.py, glossary or checklist; bump version, add a history line, push.
Audit only: walk `references/review-checklist.md` for each PL, write the reviews/ report, then offer steps 3-8 to re-issue.

## 6. Rules and cautions
- Seller = **Southern Machinery Sales and Service Co., Limited** with the Shenzhen Rm 1806 address and Tel +86 755 8320 3237 (Jason, 2026-11-02) - identical to the CI. Label it "Seller / Exporter", never "MANUFACTURER". No fax.
- **PL No. = CI No.** of the same shipment (Jason: new PL numbers, 2026-11-02). Same entity, PO, Incoterm, qty and H.S. codes as the CI - qa_pl.py `--ci` checks it.
- **No prices, amounts, bank or payment data** on a PL. Last remark: "Values are shown on the Commercial Invoice of the same number."
- Country of origin defaults to China (Jason, 2026-11-02); branded third-party goods keep China unless Jason says otherwise.
- Nothing invented: no PO No., Incoterm, S/N, weight, dimension or ISPM 15 status without a source. Reformatting (units, spacing, capitals) is fine; changing a number is not.
- H.S. codes are copied from the CI and confirmed with the forwarder / customs broker; the skill only flags doubts.
- Units: kg (2 decimals), cm, m³ (4 decimals so the total equals the sum of lines). Qty in its own column. Half-width characters only.
- Wooden crates need the ISPM 15 / IPPC line; machines need S/N (Thai BOI and most customs require it).
- Never `=NOW()` / `TODAY()`; dates `04 May 2026`.
- Shipping marks: buyer, city/country, PO No., PL/INV No., C/No. 1-n, MADE IN CHINA.
- Signature: "For and on behalf of <seller>", signer name under the line; stamp by hand on the printed copy.

## 7. Files
- `scripts/make_pl.py` - renderer (pl.json -> XLSX + PDF), profile-driven.
- `scripts/qa_pl.py` - release gate: numbering, PL = CI No., parties, open items, TO CONFIRM, arithmetic sanity, G.W. ≥ N.W., H.S. line per item, ISPM 15 for wood, no price wording, profile drift vs smt-commercial-invoice, XLSX formulas (no NOW, SUM totals), CI match (No., PO, Incoterm, qty, H.S.). Exit 1 while any ERROR.
- `assets/profile.json` (+ `pl` block), `assets/sm-logo.png`.
- `templates/pl.template.json` - blank PL data.
- `references/field-spec.md` - every pl.json field: type, source, print rule, confirm key.
- `references/glossary-cn-en.md` - 中英术语对照 + common wrong wording.
- `references/review-checklist.md` - audit / release checklist and the findings of the 2026-11 audit.
- `examples/jabil-hungary-JA26050401/` (4 cartons, final, matches CI), `examples/jabil-ukraine-JA26030401/` (6 items in one carton, draft), `examples/thai-dgt-DG24050801/` (machine in 4 wooden crates, draft with S/N and ISPM 15 open): pl.json + out/.

## 8. Upgrading
- Version: major = pl.json format change; minor = new field / rule / output; patch = fixes and wording.
- Seller change: smt-quotation -> smt-proforma-invoice -> smt-commercial-invoice -> this profile (qa_pl.py fails while they differ).
- After any renderer change: re-render all three examples, run qa_pl.py, look at the PDFs.

## Version history
- 1.0.0 (2026-11-02) - first release from the audit of 3 PLs (JA26030402, JA26050402, DGT S3020A) and Jason's decisions (HK company name + Shenzhen address, PL No. = CI No., origin China): branded PL renderer, release gate with CI cross-check, field spec, CN-EN glossary, review checklist, template, 3 examples.
