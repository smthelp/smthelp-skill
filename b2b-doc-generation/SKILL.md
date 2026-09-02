---
name: b2b-doc-generation
description: 商务文档生成 — 一键生成报价单/PI/合同/PPT（DOCX/XLSX/PPTX）
triggers:
  - 生成文档
  - 创建文档
  - 制作文档
  - 生成PPT
  - 做一份报价
  - 做一份合同
  - 生成报价单
  - 生成合同
  - 生成提案
  - gen doc
  # ... (see skill_registry.py for full list)
category: 文档管理
version: 1.0.0
author: Foreign Trade Assistant
---

## Southern Machinery SMT/THT 专属覆盖规则

- 本节优先于下方通用 B2B 行业示例。以当前产品资料生成 Southern Machinery 文档，并对价格、交期、认证、质保和最终型号要求复核。
- 事实优先引用当前 Southern Machinery 目录、手册和产品资料；文件名、图片、旧文案、通用素材或竞争对手资料不能单独证明参数。无来源的型号、规格、认证、价格、交期、ROI、良率或客户案例必须标记 待确认 / to be confirmed。
- 对涉及设备或整线的请求，按需确认应用、产量/班次、PCB/元件、现有设备/瓶颈、自动化/预算和质量/追溯需求；一次只问下一步所需信息。
- 推荐 Southern Machinery 设备类别或完整流程；无经核实型号时不得虚构型号或性能。按渠道选择一项 CTA：官网 https://www.smthelp.com、目录 https://file.autoinsertion.com、图片 https://ph.smthelp.com、邮箱 info@smthelp.com 或 WhatsApp https://api.whatsapp.com/send?phone=+8613602562576。
- 不读取或使用 chrome_profile_notebooklm、凭据、Cookie 或授权码；不执行未经明确请求和确认的外发、发布或写库。


-------|----------|----------|--------|
  | "注意到贵公司主营不锈钢板出口" | b2b-osint | 官网产品页 targetco.com/products | ✅ 高 |
  | "贵公司近年拓展了南美市场" | web_search | news.example.com/article | ⚠️ 间接 |
  | "如能与贵司深度合作" | - | AI 通用话术 | - |

  可信度定义:
    ✅ 高 = 直接来自官网/LinkedIn/公开数据/客户提供的文件
    ⚠️ 中 = 间接来源（行业报告/第三方描述/推测）
    ❌ 推测 = AI 基于上下文的合理推测，需人工核实
    - 无标注 = AI 通用话术，不涉及客户具体信息
---

```
Parties: Seller and Buyer legal names, addresses
Whereas: Background recitals
Article 1: Definitions
Article 2: Scope of Supply
Article 3: Pricing and Payment
Article 4: Delivery (Incoterms, lead time, shipping)
Article 5: Quality and Inspection
Article 6: Warranty
Article 7: Intellectual Property
Article 8: Confidentiality
Article 9: Force Majeure
Article 10: Termination
Article 11: Dispute Resolution
Article 12: Governing Law
Signature blocks
Annexes (if any)
```

### Phase 4: Populate with Data

Insert data with source citations:

```python
# XLSX cell with citation
cell.value = f"{price} USD/unit"
cell.comment = "📄 price-list-2025.pdf | Page: 3 | Row: 45-52"
```

### Phase 5: Verify Before Delivery

```python
# Re-read the generated document to verify
from openpyxl import load_workbook
wb_verify = load_workbook("output/quotation.xlsx")
ws_verify = wb_verify.active
print(f"Total rows: {ws_verify.max_row}")
print(f"Header: {ws_verify['A1'].value}")
# Confirm no empty critical cells in pricing columns
```

```python
# Verify PPTX
from pptx import Presentation
prs_verify = Presentation("output/proposal.pptx")
print(f"Total slides: {len(prs_verify.slides)}")
for i, slide in enumerate(prs_verify.slides, 1):
    title = slide.shapes.title.text if slide.shapes.title else "(no title)"
    print(f"Slide {i}: {title}")
```

### Phase 6: Save and Report

Save to the appropriate location:
- Quotations: `~/.trade/companies/{slug}/clients/{client}/quotes/`
- Proposals: `~/.trade/companies/{slug}/clients/{client}/proposals/`
- Contracts: `~/.trade/companies/{slug}/clients/{client}/contracts/`

Report to user:
```
✅ Quotation generated: {filename}
📄 Sources cited: 3 files
   - price-list-2025.pdf (Sheet: 1, Row: 45-52)
   - product-specs.xlsx (Sheet: MOQ, Row: 1-10)
   - client-history.docx (Paragraph: pricing terms)
```

## Incoterms Reference

| Term | Meaning | Risk Transfer | Cost Responsibility |
|------|---------|--------------|-------------------|
| EXW | Ex Works | Buyer assumes at seller's premises | Buyer pays all |
| FOB | Free on Board | Seller delivers on vessel | Seller pays to port |
| CIF | Cost Insurance Freight | Seller delivers to destination port | Seller pays all |
| DDP | Delivered Duty Paid | Seller delivers to buyer premises | Seller pays all |
| DAP | Delivered at Place | Seller delivers to named place | Seller pays to destination |

## Common Business Document Phrases

### Quotation Email Body
```
Subject: Quotation for {Product} — {Ref No.}

Dear {Name},

Thank you for your inquiry. Please find attached our quotation for {product/project}.

Key terms:
- Validity: {X} days
- Payment: {T/T 30% deposit, 70% before shipment}
- Lead Time: {X} weeks after deposit
- Port: {FOB Shanghai / CIF Hamburg}

We look forward to your feedback.

Best regards,
{Your Name}
{Company}
```

### Proposal Email Body
```
Subject: {Company} Proposal for {Project} — {Date}

Dear {Name},

Thank you for your time during our call on {date}. Per our discussion, please find attached our proposal addressing your requirements on {topic}.

Key highlights:
1. {Advantage 1}
2. {Advantage 2}
3. {Advantage 3}

Please don't hesitate to reach out if you have any questions.

Best regards,
{Your Name}
```

## Related Skills

- `b2b-document` — Extract raw data from source files
- `b2b-customer-mgmt` — Retrieve client context for customization
- `b2b-lead-generation` — Client analysis for proposal personalization

