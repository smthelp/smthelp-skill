# PI PC26011401 字段映射与核对摘要

- PO: PR-260113-91  ·  报价单: 无  ·  PI 日期: 2026-01-14
- PI 合计: USD 2,250.00
- 未解决待确认/缺失: **0**（为 0 才可放行给客户）

## 待确认 (CONFIRM)

| ID | 字段 | PO | 报价单 | PI 草稿取值 | 说明 | 状态 |
|---|---|---|---|---|---|---|
| quote_missing | Quotation |  |  |  | no quotation given: every price and term comes from the PO only | 已处理: accepted draft |
| terms.insurance | Insurance |  |  | Transport risk is borne by the seller until delivery at the named place (DDP) | DDP: we carry the transport risk - confirm whether we insure the shipment | 已处理: accepted draft |
| terms.taxes | Taxes & duties |  |  | Import duties and taxes in the destination country are included (DDP) | DDP: we pay import duty and VAT - confirm the amount is inside the freight/price | 已处理: accepted draft |
| item1.match | Item 1 | BLHC800 |  |  | PO line not found in the quotation: price, description and spec need approval | 已处理: accepted draft |
| item1.price | Item 1 unit price | 150.0 |  | 150.0 | price only in the PO (not quoted) | 已处理: accepted draft |
| charge.freight | Charge: Shipping cost via DHL air to USA, duties paid (DDP) | 450.00 |  | included | charge only in the PO (not quoted) - confirm amount | 已处理: accepted draft |

## 假设取值 (ASSUMED)

| ID | 字段 | PO | 报价单 | PI 草稿取值 | 说明 | 状态 |
|---|---|---|---|---|---|---|
| ship_to | Ship to |  |  | same as buyer | PO gives no separate delivery address; buyer address used | 已处理: accepted draft |
| terms.warranty | Warranty |  |  | 12 months from the date of shipment, excluding consumable and wear parts and damage caused by misuse | neither PO nor quotation states it; profile default | 已处理: omitted |
| terms.packing | Packing |  |  | Export packing included | neither PO nor quotation states it; profile default | 已处理: accepted draft |

## 字段映射

| 字段 | PO | 报价单 | PI 取值 | 规则 | 状态 |
|---|---|---|---|---|---|
| PI date |  |  | 2026-01-14 | --date / decisions / build day | OK |
| PI No. |  |  | PC26011401 | given by Jason | OK |
| PO No. | PR-260113-91 |  | PR-260113-91 | PO only | OK |
| PO date |  |  |  | not stated (optional) | OK |
| Quotation ref. |  |  |  | quotation file used | OK |
| Prepared by |  |  | Jason Wu | decisions / quotation / Jason Wu | OK |
| Buyer company | PROSSER LLC |  | PROSSER LLC | PO only | OK |
| Buyer address | 319 E. Coma Ave. Suite 245, Hidalgo, TX 78557 |  | 319 E. Coma Ave. Suite 245, Hidalgo, TX 78557 | PO only | OK |
| Buyer country | USA |  | USA | PO only | OK |
| Attn | Javier Lopez |  | Javier Lopez | PO only | OK |
| Email | info@us-prosser.com |  | info@us-prosser.com | PO only | OK |
| Tel | 956 843 1100 |  | 956 843 1100 | PO only | OK |
| Buyer tax ID |  |  |  | not stated (optional) | OK |
| Ship to |  |  | same as buyer | PO silent -> buyer address | ASSUMED |
| Currency | USD |  | USD | PO only | OK |
| Delivery terms (Incoterm) | DDP |  | DDP | PO only | OK |
| Named place | Hidalgo, TX, USA |  | Hidalgo, TX, USA | PO only | OK |
| Terms of payment | 100% T/T in advance |  | 100% T/T in advance | PO only | OK |
| Delivery time | 1 week after receipt of payment |  | 1 week after receipt of payment | PO only | OK |
| Warranty |  |  | 12 months from the date of shipment, excluding consumable and wear parts and damage caused by misuse | profile default | ASSUMED |
| Packing |  |  | Export packing included | profile default | ASSUMED |
| Insurance |  |  | Transport risk is borne by the seller until delivery at the named place (DDP) | DDP: seller's risk | CONFIRM |
| Port of loading |  |  | Shenzhen, China | PO / profile (Shenzhen) | OK |
| Destination | USA |  | USA | PO / ship-to country | OK |
| Item 1 | BLHC800 Lower heating core 800 W x12 @ 150 |  | BLHC800 x12.0 @ 150.00 | not in quotation | CONFIRM |
| Charge freight | 450.00 |  | Shipping cost via DHL air to USA, duties paid (DDP) | PO only | CONFIRM |
| Total | 2,250.00 |  | 2,250.00 | computed | OK |
