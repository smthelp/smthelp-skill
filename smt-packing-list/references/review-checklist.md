# Packing List review / release checklist

Use for auditing a PL someone else made (write `reviews/<date>-pl-review.md`: per PL a table 级别 高/中/低 | 位置 | 现文 | 建议) and before releasing one made with make_pl.py. Flag differences from the invoice; never change data silently.

## 1. Brand (smt-brand-kit + invoice family)
- [ ] Logo = `assets/sm-logo.png` (green #93AC3E / teal #0097B2), not the old olive / dark-teal version; not stretched.
- [ ] Company `Southern Machinery Sales and Service Co., Limited`, Shenzhen Rm 1806 address, Tel +86 755 8320 3237, smthelp.com · info@smthelp.com · WhatsApp +86 136 0256 2576. No fax, no "Co.,Limited,China", no "SHENZHEN … CO.,LTD.".
- [ ] Arial throughout (no SimSun/宋体, Times); title and table header Navy #003142; green rule under the letterhead.
- [ ] A4 portrait, fits the page width, nothing cut at the border, no columns spilling to page 2.

## 2. Document data
- [ ] PL No. = CI No. of the same shipment; rule 2 letters + YYMMDD + 2-digit seq.
- [ ] Date fixed (no `=NOW()` / `TODAY()`), format `04 May 2026`.
- [ ] Invoice No., PO No. printed; PO equals the CI.
- [ ] Consignee legal name and full address as on the PO; city not doubled; contact if known.
- [ ] Incoterm, port of loading, destination printed and equal to the CI.

## 3. Goods
- [ ] Each line: model + English name, Qty and Unit in their own columns, H.S. code = CI.
- [ ] Machines: S/N per unit. Branded third-party goods: origin checked (default China, Jason 2026-11-02).
- [ ] Total qty per item = CI qty. No unit price / amount anywhere.

## 4. Packages and arithmetic
- [ ] Each package: C/No., packing type, L × W × H cm, N.W., G.W. (G.W. ≥ N.W.).
- [ ] CBM = L×W×H/1,000,000 per package; totals of N.W., G.W., CBM, Qty recomputed (SUM formulas in the XLSX).
- [ ] Units consistent: kg, cm, m³; N.W. 2 decimals; CBM 4 decimals; half-width characters.
- [ ] Wooden crates: ISPM 15 / IPPC statement.

## 5. Marks, remarks, signature
- [ ] Shipping marks: buyer, city/country, PO No., PL/INV No., C/No., MADE IN CHINA.
- [ ] Remarks: packing, origin, non-dangerous, "values on the CI".
- [ ] Signature block with name; stamp on print does not cover text.

## 6. Gate
`python3 scripts/qa_pl.py pl.json --xlsx out/*.xlsx [--ci ci.json]` -> `0 ERROR -> FINAL OK`, then look at the PDF page.

## Findings that came up in the 2026-11 audit (watch for them)
Missing shipping marks / invoice ref / Incoterm on all three; `=NOW()` date; "Banan District"; HK vs Shenzhen entity mixed; qty hidden in the description ("* 20"); full-width brackets; 4 empty table rows; volume column printing on page 2; MANUFACTURER = Southern Machinery for third-party goods; HS codes to check with the broker (cables 8544 / connectors 8536 / conveyors 8428.90).
