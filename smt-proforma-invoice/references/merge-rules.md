# Merge, override and confirmation rules

## Precedence
| Group | Fields | Draft value | When PO and quotation differ |
|---|---|---|---|
| Identity | buyer company, address, attn, email, tel, tax ID | PO | company/country -> CONFIRM; others INFO |
| Logistics | ship-to, destination, ship via, requested date, PO No./date | PO | requested date vs lead time -> CONFIRM |
| Quantity | qty per line | PO | always CONFIRM (price breaks, packing, lead time) |
| Commercial | unit price, payment, lead time, warranty, installation, packing, currency, Incoterm, place | quotation | CONFIRM, PO value shown beside it |
| Charges | freight, packing, service, tooling, other | quotation | different amount or one-sided -> CONFIRM |
| Discount | discount | quotation | different or PO-only -> CONFIRM |
| Tax | VAT / duties | none | any tax in the PO -> CONFIRM; DDP duties -> CONFIRM |
| Seller data | company, bank, origin, port of loading, tax ID | profile | never from PO |

When only one source has a value it is used (row "PO only" / "quotation only" in the mapping).
When neither has it: profile default = ASSUMED; no default = MISSING (TO_CONFIRM, red).

## Levels
- CONFIRM - Jason decides. Blocks release (qa_pi.py ERROR) until `decisions.resolve[id]` is "accept" or {"value": ...}.
- MISSING - no value anywhere. Blocks release.
- ASSUMED - default or fixed rule used. Listed for Jason; does not block.
- INFO - harmless (our model spelling kept, quoted item not ordered, address wording).

## Issue IDs (use them in decisions.json)
`pi_no`, `po_no`, `quote_ref`, `quote_validity`, `quote_missing`, `buyer.<field>`, `ship_to`, `currency`, `incoterm`, `place`,
`terms.payment|delivery|warranty|packing|installation|insurance|taxes`, `delivery_date`, `destination`,
`item<n>.match|model|name|qty|price|amount|options`, `quote_item<n>.not_ordered`, `charge.<freight|packing|service|tooling|other>`,
`charge.packing.qty`, `charge.freight.needed`, `mention.<freight|tax|discount>`, `discount`, `tax`, `total`.

## Never
- Pick the lower price, convert currency, add tax, add or drop freight, change Incoterm, or extend a lead time on our own.
- Copy a PO value into po.json that the PO does not print.
- Release a PI (to Jason as final, or anyone else) with qa_pi.py errors.
