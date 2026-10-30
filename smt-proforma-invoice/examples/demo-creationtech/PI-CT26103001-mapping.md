# PI CT26103001 字段映射与核对摘要

- PO: DEMO-4500012345  ·  报价单: CT26102801  ·  PI 日期: 2026-10-30
- PI 合计: USD 6,500.00
- 未解决待确认/缺失: **0**（为 0 才可放行给客户）

## 待确认 (CONFIRM)

| ID | 字段 | PO | 报价单 | PI 草稿取值 | 说明 | 状态 |
|---|---|---|---|---|---|---|
| terms.payment | Terms of payment | Net 30 days after delivery | 50% T/T deposit with order, 50% T/T before shipment | 50% T/T deposit with order, 50% T/T before shipment | PO and quotation differ; draft uses the quotation value | 已处理: accepted draft |
| delivery_date | Requested delivery date | 2026-11-20 | Within 30 days after receipt of the deposit | 2026-11-20 | PO wants 2026-11-20; the quoted lead time allows delivery only by 2026-11-29 | 已处理: accepted draft |
| item1.price | Item 1 unit price | 2900.0 | 2950.0 | 2950.0 | PO price differs from the quotation; draft keeps the quoted price | 已处理: accepted draft |
| charge.packing | Charge: Export packing: vacuum-sealed, fumigation-free wooden case |  | 600.00 | included | quoted charge not shown on the PO - confirm the buyer accepts it | 已处理: accepted draft |
| mention.freight | Freight | Freight: to be advised |  | not on PI | PO mentions it without an amount - nothing added until Jason gives the figure | 已处理: accepted draft |
| total | Total | 5,800.00 |  | 6,500.00 | PO total 5,800.00 differs from the PI total 6,500.00 | 已处理: accepted draft |

## 信息 (INFO)

| ID | 字段 | PO | 报价单 | PI 草稿取值 | 说明 | 状态 |
|---|---|---|---|---|---|---|
| item1.model | Item 1 model | SFY-04 | SFY04 | SFY04 | our spelling kept; PO spelling shown in the mapping | - |

## 字段映射

| 字段 | PO | 报价单 | PI 取值 | 规则 | 状态 |
|---|---|---|---|---|---|
| PI date |  |  | 2026-10-30 | --date / decisions / build day | OK |
| PI No. |  | CT26102801 | CT26103001 | given by Jason | OK |
| PO No. | DEMO-4500012345 |  | DEMO-4500012345 | PO only | OK |
| PO date | 2026-10-30 |  | 2026-10-30 | PO only | OK |
| Quotation ref. | CT26102801 | CT26102801 | CT26102801 | quotation file used | OK |
| Prepared by |  | Jason Wu | Jason Wu | decisions / quotation / Jason Wu | OK |
| Buyer company | Creation Technologies | Creation Technologies | Creation Technologies | PO = quotation | OK |
| Buyer address | Dallas, TX | Dallas, TX | Dallas, TX | PO = quotation | OK |
| Buyer country | USA | USA | USA | PO = quotation | OK |
| Attn | Benjamin Dendy | Benjamin Dendy | Benjamin Dendy | PO = quotation | OK |
| Email | benjamin.dendy@creationtech.com | benjamin.dendy@creationtech.com | benjamin.dendy@creationtech.com | PO = quotation | OK |
| Tel |  |  |  | not stated (optional) | OK |
| Buyer tax ID |  |  |  | not stated (optional) | OK |
| Ship to | DEMO receiving address, Dallas, TX |  | DEMO receiving address, Dallas, TX | PO ship-to | OK |
| Currency | USD | USD | USD | PO = quotation | OK |
| Delivery terms (Incoterm) | EXW | EXW | EXW | PO = quotation | OK |
| Named place | Shenzhen | Shenzhen, China | Shenzhen, China | PO = quotation | OK |
| Terms of payment | Net 30 days after delivery | 50% T/T deposit with order, 50% T/T before shipment | 50% T/T deposit with order, 50% T/T before shipment | conflict -> draft = quotation | CONFIRM |
| Delivery time |  | Within 30 days after receipt of the deposit | Within 30 days after receipt of the deposit | quotation only (PO silent) | OK |
| Requested delivery date | 2026-11-20 |  | 2026-11-20 | PO | OK |
| Warranty |  | 12 months from the date of shipment, excluding consumable and wear parts and damage caused by misuse | 12 months from the date of shipment, excluding consumable and wear parts and damage caused by misuse | quotation only (PO silent) | OK |
| Packing |  | Export packing as listed above. Freight from Shenzhen is arranged and paid by the buyer (EXW). | Export packing as listed above. Freight from Shenzhen is arranged and paid by the buyer (EXW). | quotation only (PO silent) | OK |
| Installation |  | Free remote installation guidance and operator training by video call | Free remote installation guidance and operator training by video call | quotation only (PO silent) | OK |
| Insurance |  | To be covered by the buyer | To be covered by the buyer | EXW: buyer insures | OK |
| Port of loading |  |  | Shenzhen, China | PO / profile (Shenzhen) | OK |
| Destination |  |  | USA | PO / ship-to country | OK |
| Item 1 | SFY-04 AGV soldering pallet transfer x2 @ 2900 | SFY04 AGV (automated guided vehicle) for soldering pallets, magnetic-strip navigation, each with 40 m magnetic strip and charger x2 @ 2,950.00 | SFY04 x2.0 @ 2,950.00 | matched by model | CONFIRM |
| Charge packing |  | 600.00 | Export packing: vacuum-sealed, fumigation-free wooden case | quotation only | CONFIRM |
| Total | 5,800.00 |  | 6,500.00 | computed | OK |
