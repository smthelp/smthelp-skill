# PI field mapping (old PI samples -> new PI -> source)

| New PI field | Old PI wording (2025-26 samples) | Source order | Notes |
|---|---|---|---|
| Letterhead company | "Southern Machinery Sales and Service Co.,Limited" (spacing varied) | profile.company | Exactly `Southern Machinery Sales and Service Co., Limited` |
| Address / contact | "Add: Rm 1806 ... P/C 518102", "TEL ... FAX ... website" | profile | Fax dropped; web · email · WhatsApp |
| Title | PROFORMA INVOICE | fixed | Draft banner while issues are open |
| To | To / Customer | PO buyer.company -> quotation | Company name differs -> CONFIRM |
| Address | Add / ADD | PO -> quotation | Differences INFO (PO kept) |
| Attn / Email / Tel | Attn, Buyer, Contact, Office, Mail | PO -> quotation | Optional; empty -> WARN |
| Tax ID (buyer) | (Turkey PO) | PO | Printed when given |
| Ship to | Ship to / Goods to be delivered to / DELIVERY AT | PO ship_to -> buyer (ASSUMED) | |
| PI No. | No. / Invoice # / Invoice No. (SA25102501, JP25121601, IS2026032001, Tuk25093001) | decisions / --pi-no -> quotation letters + date + 01 (ASSUMED) | 2 letters + YYMMDD + 2 digits |
| Date | 25-Oct-25, 2026/1/14, =NOW() | --date / decisions | Fixed value, `30 Oct 2026` |
| PO No. / PO date | PO / PO# | PO | Missing PO No. -> MISSING |
| Quotation ref. | (new) | quote.quote_no | PO quote_ref different -> CONFIRM |
| Currency | (USD/UNIT), CNY/UNIT, US$ | quotation -> PO -> profile | Differ -> CONFIRM, nothing converted |
| Port of loading | 1. PORT OF LOADING: SHENZHEN | PO -> profile.pi.port_of_loading | |
| Destination | PORT OF DESTINATION / DELIVERY AT | PO destination -> ship-to country | Missing -> MISSING |
| Delivery terms | DELIVERY TERMS: EXW SHENZHEN / Trade terms: Ex-work / DDP / CWO | quotation -> PO -> profile | Printed `EXW Shenzhen, China (Incoterms® 2020)` |
| Delivery time | 3 days, TWO WEEK, 10 working days, 1 week | quotation -> PO -> profile | Requested date earlier than lead time -> CONFIRM |
| Terms of payment | 100% pay advance / T/T 100% before shipment | quotation -> PO -> profile | Compared by % and trigger words |
| Insurance | To be cover by the Buyer | rule by Incoterm | CIF/CIP and D-terms -> CONFIRM |
| Shipment by | MODE OF SHIPMENT: BY AIR | PO ship_via | Optional |
| Country of origin | COUNTERY OF ORIGIN: CHINA | profile | Always |
| Seller tax ID | VAT number / Tax-Id 61178505-000(-03-20-0) | profile.pi.tax_id | Only when decisions.show_tax_id |
| Item / Model / Description | ITEM NO., Model, P/N, DESCRIPTION OF GOODS | match PO line to quotation item (model, then description) | Our model spelling printed; PO "Your P/N" line |
| HS code / extra lines | "H.S. code: 7616999000", "Raw material", "Function" | PO hs_code / lines, decisions.lines | One line each under the description |
| Qty / Unit | QTY (UNIT) | PO qty; unit PO -> quotation | Qty differs from quote -> CONFIRM |
| Unit price | UNIT PRICE (USD/UNIT) | quotation (incl. included options) | PO differs -> CONFIRM |
| Amount | AMOUNT | formula qty x price | |
| Charges | Shipping Cost / Air transport DHL / mould / packing lines | quotation charges + PO charges, matched by kind | One-sided or different -> CONFIRM |
| Discount | (none in samples) | quotation / PO | Differ or PO-only -> CONFIRM |
| Tax | (none) | never auto | PO tax line -> CONFIRM |
| Total | Total / TOTAL AMOUNT | formula | PO total differs -> CONFIRM |
| Amount in words | (new) | generated | |
| Remarks | Remark lines, "THESE COMMODITIES ARE LICENSED FOR THE ULTIMATE DESTINATION" | quotation terms, profile, decisions | Export line only when decisions.export_control_line |
| Bank details | BANK DETAIL block (name, bank, address, account, SWIFT, country, account type, bank code 007) | profile.bank | Must equal smt-quotation bank |
| CNY payment | "Please pay to WeChat or Alipay account +8613602562576" | profile.pi.alt_payment_cny | CNY PIs only |
| Signature | (none in samples) | profile + buyer | Seller and buyer countersign boxes |
