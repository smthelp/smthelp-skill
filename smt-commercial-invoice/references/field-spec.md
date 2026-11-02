# ci.json field specification

One commercial invoice = one folder `cis/<INVOICE_NO>/` with `ci.json` and `out/`.
Source column: **PO** = customer purchase order, **SHIP** = shipment/packing data, **PROFILE** = `assets/profile.json`, **JASON** = only Jason can decide.

| Key | Type | Source | Rule / how it prints |
|---|---|---|---|
| `invoice_no` | str | JASON / numbering rule | 2 letters (customer code, JA = Jabil) + YYMMDD (invoice date) + 2-digit sequence, e.g. `JA26062601`. File name must use the full number. |
| `date` | ISO date | JASON | Prints `26 Jun 2026`. Never `=NOW()`. |
| `po_no` | str | PO | Printed exactly as on the PO (`C-10003652009`). Required. |
| `po_date` | ISO date | PO | Optional; printed when given. |
| `contract_ref` | str | PO / JASON | Frame contract number, e.g. `UA-03978-2016 dated 10 Oct 2019`. Only when it applies to this buyer entity. Empty = row hidden. |
| `buyer.company` | str | PO | Buyer's legal name (`Jabil Circuit Ukraine LLC`). |
| `buyer.address`, `buyer.country` | str | PO | Full legal address, printed as `address, country`. |
| `buyer.attn`, `email`, `tel` | str | PO | Buyer contact. Phone numbers go in `tel` (never under a "Contract Number" label). |
| `buyer.tax_id` | str | PO | VAT / EORI / EDRPOU when the buyer supplies it. |
| `buyer.short` | str | - | Used in the file name (`Jabil-Ukraine`). |
| `ship_to` | obj | PO | `company/address/country`; identical to buyer prints "Same as above". |
| `currency` | str | PO | `USD` (default), `EUR`, `CNY`. Printed in column heads and TOTAL. |
| `incoterm`, `place` | str | PO / quotation | Prints `EXW Shenzhen, China (Incoterms® 2020)`. |
| `terms.payment` | str | PO / contract / JASON | Must add up to 100 %; samples: `Free of charge - no payment required`. Never invented. |
| `terms.delivery` | str | SHIP | Printed as "Shipment" (e.g. `By buyer's forwarder from Shenzhen (EXW)`, `DHL Express, AWB ...`). |
| `terms.insurance` | str | PROFILE | `To be covered by the buyer` unless CIF/CIP. |
| `shipment.port_of_loading`, `destination`, `country_of_origin` | str | PROFILE / PO | Defaults `Shenzhen, China` / buyer country / `China`. |
| `show_tax_id` | bool | PROFILE | `true` prints Seller Tax ID 61178505-000-03-20-0. |
| `export_control_line` | bool | - | `true` prints "These commodities are licensed for the ultimate destination shown above." |
| `signatory` | str | JASON | Name under the seller signature (default Leo Liao). Stamp: Hong Kong company stamp, applied on the printed/PDF copy. |
| `items[]` | list | PO + product data | `model` (SM model, never a supplier model), `name` (English, one fact per line), `customer_ref` (prints "Your P/N"), `qty` (number), `unit` (pcs / sets / rolls ...), `price` (number, 2 decimals), `hs_code` (8-10 digits, confirmed with forwarder), `lines` (extra lines). |
| `charges[]` | list | PO / quotation | Freight, packing ... `name/qty/unit/price`; printed under the subtotal. |
| `discount` | num | PO / quotation | Positive number, printed negative. |
| `total_check` | num | computed | Must equal Σ qty×price + charges − discount (qa_ci.py checks). Amount in words is generated from it. |
| `notes[]` | list | - | First line `Non-dangerous goods.`; samples add `Free samples, no commercial value. Value for customs purposes only.` |
| `note_flags` | obj | - | `{ "2": "issue_id" }` shades a note amber while that issue is open. |
| `issues[]` | list | review | `{id, level CONFIRM/MISSING/INFO, field, note, resolved}`. Any open CONFIRM/MISSING = DRAFT. |

## Issue ids that shade cells
`buyer.company|address|attn|email|tel|tax_id`, `ship_to`, `pi_no` (invoice no.), `date`, `po_no`, `po_date`, `contract_ref`, `currency`, `incoterm`, `port_of_loading`, `destination`, `origin`, `tax_id`, `terms.payment|delivery|insurance`, `item<N>.match` (model), `item<N>.name` (description), `item<N>.qty`, `item<N>.price`, `discount`, `charge.freight|packing|service|other`.

## Seller block (fixed, from profile - never typed per invoice)
- Company: **Southern Machinery Sales and Service Co., Limited** (Hong Kong company; = bank beneficiary)
- Address: Rm 1806, Block 3, Jinyun COFCO, Qianjin 2nd Road, Xixiang, Bao'an District, Shenzhen 518102, China
- Tel +86 755 8320 3237 · smthelp.com · info@smthelp.com · WhatsApp +86 136 0256 2576 - **no fax**
- Bank: JPMorgan Chase Bank N.A., Hong Kong Branch · USD a/c 63007917455 · SWIFT CHASHKHH · bank code 007
