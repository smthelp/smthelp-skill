# pl.json field spec

Source order: commercial invoice of the same shipment (CI) -> PO -> packing data from the warehouse (cartons, weights, dimensions) -> profile. Copy as printed; never invent.

| Field | Type / example | Source | Print rule | confirm key |
|---|---|---|---|---|
| `pl_no` | `JA26050401` | = CI invoice No. | 2 letters + YYMMDD + 2-digit seq; same number as the CI | - |
| `date` | `2026-05-04` | CI date / shipping date | `04 May 2026`; fixed value, never `=NOW()` | - |
| `file_tag` | `Jabil-Hungary` | buyer short name + country/machine | file name `PL-<no>-<tag>[-DRAFT]` | - |
| `invoice_no` | `JA26050401` | CI | right block | `invoice_no` |
| `po_no` | `C-10003587880` | PO / CI | right block + shipping marks; unknown -> `TO CONFIRM` | `po_no` |
| `incoterm` | `EXW Shenzhen, China (Incoterms® 2020)` | CI | Shipment block; must equal CI | `incoterm` |
| `port_of_loading` | `Shenzhen, China` | profile default | Shipment block | `port_of_loading` |
| `destination` | `Tiszaújváros, Hungary` | consignee address | Shipment block | `destination` |
| `consignee.company` | legal name | PO / CI | as printed by the buyer | - |
| `consignee.address` | street, postcode city, country | PO / CI | city once, country last | - |
| `consignee.attn / tel / email` | | CI of the same shipment | optional; blank lines stay blank | - |
| `packages_text` | `4 cartons` | count of packages | right block "Packages" | - |
| `package_word` | `cartons` | | TOTAL row | - |
| `origin` | `China` | profile default (Jason 2026-11-02) | right block; branded third-party goods: still China unless Jason says otherwise | - |
| `packages[].cno` | `"1"` | carton number | C/No. column; one package = one block | - |
| `packages[].packing` | `Carton` / `Wooden crate` / `Pallet` | warehouse | Packing column | `packing` |
| `packages[].L/W/H` | cm, numbers | warehouse | `60 × 40 × 40`; CBM = L×W×H/1,000,000 (formula, 4 decimals) | - |
| `packages[].nw / gw` | kg per package | warehouse | 2 decimals; G.W. ≥ N.W.; totals = SUM | - |
| `packages[].items[].desc` | multi-line text | CI description | line 1 = SM model + plain English name; then Function / Material / S/N; last line `H.S. code: <code>` = CI | `items` |
| `packages[].items[].qty / unit` | `50`, `pcs` | CI / warehouse | Qty column; totals summed when all units are the same | `items` |
| `marks` | multi-line | composed | Buyer, city/country, PO No., PL/INV No., C/No. 1-n, MADE IN CHINA | `marks` |
| `remarks` | list | profile `standard_remarks` + packing line | numbered; wooden packing needs the ISPM 15 line | `remarks` |
| `signer` | `Leo Liao` | profile default | under the signature line; stamp on print | - |
| `confirm` | list of keys | reviewer | amber cells + DRAFT banner until emptied | - |
| `one_page` | `true` (default) | | fit to one A4 page | - |

## Never on a packing list
Unit price, amount, currency totals, bank details, payment terms. The last remark points to the CI for values.

## Units and number formats
- Weight `kg`, 2 decimals (`9.70`). Dimensions `cm`, integers, `L × W × H`. Volume `m³`, 4 decimals so the total equals the sum exactly.
- Qty integers; units `pcs`, `set`, `sets`, `rolls`, `pairs`.
- Dates `dd Mon yyyy`. Half-width characters only (no `（` `：`).
