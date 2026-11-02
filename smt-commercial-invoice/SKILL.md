---
name: smt-commercial-invoice
description: Make or review Southern Machinery commercial invoices (CI / 商业发票 / 报关发票) in the branded Excel + PDF format, issued by the Hong Kong company Southern Machinery Sales and Service Co., Limited with the JPMorgan HK bank block. Use when Jason asks to 做/开 Commercial Invoice、出报关发票、把旧发票改成品牌版、统一发票格式、审核发给客户的 Invoice（条款、金额、银行信息、HS 编码、品牌）. Never guesses: payment terms, HS codes, specs, contract refs or prices without a source are marked to confirm and keep the invoice in DRAFT until Jason answers.
metadata:
  version: 1.0.0
  updated: 2026-11-02
  depends_on: smt-proforma-invoice (renderer pi_base.py vendored, profile.json kept identical), smt-brand-kit (logo, colours), smt-quotation (seller/bank profile)
  samples: JA26031701, JA26033001, JA26050401, JA26062601 (Jabil Hungary / Ukraine, 2026); reference DG25042301 (Thai DGT, 2025)
---

# SMT Commercial Invoice - order data -> one branded commercial invoice (XLSX + PDF)

```
old invoice / PO / shipment data --transcribe--> cis/<NO>/ci.json ──make_ci.py──> out/CI-<NO>-<buyer>[-DRAFT].xlsx + .pdf
Jason's answers --------------------------> issues[].resolved / field values      └─qa_ci.py─> 0 ERROR = final
```

## 1. Trigger (when to load)
- 中文：做 Commercial Invoice、开商业发票、出报关发票、发票改成品牌版、统一发票模板、审核 Invoice、核对发票条款/金额/银行信息、HS 编码核对。
- English: commercial invoice, customs invoice, re-issue invoice in our format, check our invoices.

## 2. Scope
| Use for | Not for |
|---|---|
| Commercial invoices to customers for export / customs (goods already ordered) | Proforma invoices for payment -> `smt-proforma-invoice` |
| Re-issuing old WPS/Excel invoices in the brand format | Quotations -> `smt-quotation` |
| Auditing invoices someone else made (brand, terms, amounts, bank, HS) | Packing lists (no template yet), courier waybills |
| Free-sample invoices (value for customs) | Sending anything to a customer - Jason sends |

## 3. Inputs (checklist)
Required
1. Buyer legal name, full address, country (from PO) + contact (attn, email, tel).
2. PO No. (exact), invoice date, invoice number (rule in field-spec.md).
3. Every line: SM model, English description, qty, unit, unit price, H.S. code.
4. Incoterm + place (default EXW Shenzhen, China), currency (default USD).
5. Terms of payment (from contract/PO/Jason - never assumed; samples: free of charge).
Optional: ship-to if different, buyer tax ID (VAT/EORI), PO date, frame contract ref., charges/discount, shipment mode/AWB, weights/cartons (as `lines` or `notes`), signatory (default Leo Liao).
Fixed (never typed per invoice): seller, address, contact, tax ID, bank -> `assets/profile.json`.

## 4. Outputs
- `cis/<NO>/out/CI-<NO>-<buyer>.xlsx` - A4 portrait, live formulas (Qty × Unit price, TOTAL), amount in words, brand header/footer.
- `cis/<NO>/out/CI-<NO>-<buyer>.pdf` - same, via LibreOffice; one page for up to ~6 lines.
- While issues are open: file name ends `-DRAFT`, red banner "DRAFT - n item(s) to confirm", amber cells, red TO_CONFIRM.
- For audits: `reviews/<date>-<subject>.md` (per-invoice table: severity 必改/待确认, location, current text, fix) + Chinese summary to Jason.

## 5. Steps
1. **Setup** (once per environment): `pip install --target <pylib> openpyxl`; LibreOffice for PDF (`SOFFICE=/path/to/soffice` if not on PATH). Run with `PYTHONPATH=<pylib>`.
2. **Transcribe**: `mkdir -p cis/<NO>`; copy `templates/ci.template.json` to `cis/<NO>/ci.json`; fill from the PO / old invoice literally (pdftotext -layout; check the rendered page too). Fix wording per `references/glossary-cn-en.md`.
3. **Flag, don't guess**: every gap or doubt becomes an `issues[]` entry (`level: CONFIRM`, `resolved: false`) - payment terms, HS code, open specs (voltage), supplier model names, contract ref. for another entity, sample price vs. regular price, odd addresses. Use the issue ids in field-spec.md so the right cell turns amber.
4. **Render**: `python3 scripts/make_ci.py cis/<NO>/ci.json --pdf`.
5. **Check**: `python3 scripts/qa_ci.py cis/<NO>/ci.json --xlsx cis/<NO>/out/*.xlsx`; open the PDF image (pdftoppm) - one page, no overlapping text, no cut-off lines.
6. **Deliver to Jason** in Chinese: PDF + XLSX, one short line per open issue as a question. Never to the customer.
7. **Answers**: write them into ci.json (value + `resolved: true`), repeat 4-5 until `0 ERROR -> FINAL OK`, deliver the final files.
8. **Learn**: a new rule goes where it lives (profile `ci`, qa_ci.py check, glossary, checklist), bump version, add a history line, push.
Audit only: walk `references/review-checklist.md` per invoice, write the reviews/ report, then offer steps 2-7 to re-issue.

## 6. Rules and cautions
- Seller = Hong Kong company **Southern Machinery Sales and Service Co., Limited** (Jason, 2026-11-02), letterhead with the Shenzhen Rm 1806 office address and Tel +86 755 8320 3237, as in the 2025 reference invoice DG25042301. No fax. No "Co.,Limited,China", no "Shenzhen" prefix.
- Bank block only from profile (JPMorgan Chase Bank N.A., Hong Kong Branch, USD a/c 63007917455, SWIFT CHASHKHH, bank code 007). If an old invoice shows other bank data: **report the difference, never change it silently**.
- Brand-kit's "no prices/terms in marketing material" does **not** apply to invoices: terms must be complete.
- Terms: `<Incoterm> <place> (Incoterms® 2020)`; payment adds to 100 %; insurance consistent with the Incoterm.
- Nothing invented: no payment term, HS code, voltage, price, weight or contract number without a source.
- HS codes are confirmed with the forwarder/customs broker; the skill only flags mismatches (e.g. adhesive kraft tape under 4810).
- Specs on a commercial invoice are final - no "to be confirmed before shipment".
- SM model names only; supplier model names (e.g. FYJ-D58 if it is the supplier's) must be confirmed/replaced.
- Free samples: say so in notes; the customs value must have a basis (same goods invoiced at USD 4.00 and 9.75 = under-valuation risk).
- A frame contract ref. prints only for the buyer entity it belongs to.
- Dates as `26 Jun 2026`; numbers 2 decimals; units always named.
- Old invoice PDFs modified after shipment (PDF ModDate) -> ask whether it is the final version.

## 7. Files
- `scripts/make_ci.py` - renderer (CI layout on top of `pi_base.py`).
- `scripts/pi_base.py` - vendored copy of smt-proforma-invoice `make_pi.py` v1.0.0 (do not edit; re-copy when that skill upgrades).
- `scripts/qa_ci.py` - release gate: numbering, parties, seller/bank/brand, profile drift vs smt-proforma-invoice, Incoterms, payment, arithmetic, units, HS, open issues, TO_CONFIRM, xlsx content. Exit 1 while any ERROR.
- `assets/profile.json` (+ `ci` block), `assets/sm-logo.png`.
- `templates/ci.template.json` - blank invoice data.
- `references/field-spec.md` - every ci.json field, source, print rule, issue ids.
- `references/glossary-cn-en.md` - 中英术语对照 + common wrong wording.
- `references/review-checklist.md` - audit / release checklist.
- `examples/jabil-JA26031701/` (free samples, Hungary) and `examples/jabil-JA26062601/` (machine, Ukraine): ci.json + DRAFT outputs.

## 8. Upgrading
- Version: major = ci.json format change; minor = new field/rule/output; patch = fixes and wording.
- Seller/bank change: smt-quotation profile -> smt-proforma-invoice profile -> this profile (qa_ci.py fails while they differ).
- Renderer change in smt-proforma-invoice: re-copy `make_pi.py` to `scripts/pi_base.py`, re-run both examples, check the PDFs.

## Version history
- 1.0.0 (2026-11-02) - first release from the Jabil invoice audit (4 invoices, 2026) and Jason's decision to issue from the Hong Kong company: branded CI renderer, release gate, field spec, CN-EN glossary, review checklist, template, 2 examples.
