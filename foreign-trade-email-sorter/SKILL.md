---
version: "1.0.0"
name: foreign-trade-email-sorter
description: "Gmail-based email classifier for foreign trade businesses. Auto-categorizes emails into Spam, Marketing, and Inquiries. Generates daily inquiry summary reports."
author: Morment
homepage: https://github.com/morment/foreign-trade-email-sorter
source: local
---

# Foreign Trade Email Sorter

专为外贸企业设计的 Gmail 邮件自动分类器。自动识别并分类邮件，重点提取询盘咨询邮件生成每日简报。

## 核心功能

- **自动分类 Gmail 邮件**
  - 🗑️ **Spam/Junk** - 垃圾邮件、钓鱼邮件
  - 📧 **Marketing** - 营销邮件、新闻订阅、促销
  - 💼 **Inquiry** - 客户询盘、咨询回复、报价请求 ← **重点**

- **询盘邮件智能处理**
  - 提取客户信息（姓名、公司、邮箱）
  - 识别产品意向和采购需求
  - 提取关键信息（数量、目标价、交期）
  - 生成结构化询盘摘要

- **每日简报输出**
  - 汇总当日所有询盘
  - 按优先级排序（高意向→低意向）
  - 输出到飞书/本地文件

## 分类规则

### 🗑️ Spam/Junk
- 明显的垃圾邮件特征
- 钓鱼邮件（伪装成银行、PayPal等）
- 无关的推销邮件
- 发件人在黑名单中

### 📧 Marketing
- 行业新闻订阅
- 供应商促销邮件
- 展会邀请
- 平台通知（Alibaba, Made-in-China等）
- 物流/货代推广

### 💼 Inquiry（询盘）- 重点识别
**询盘特征关键词：**
- "interested in", "quote", "quotation", "price", "pricing"
- "inquiry", "enquiry", "RFQ", "request for quote"
- "order", "purchase", "buy", "looking for"
- "sample", "catalog", "catalogue", "brochure"
- "MOQ", "lead time", "delivery time", "payment terms"

**询盘邮件特征：**
- 来自潜在客户（首次联系）
- 询问产品信息、价格、交期
- 有具体的采购意向
- 包含公司信息或签名

## 询盘信息提取

### 提取字段
| 字段 | 说明 | 示例 |
|------|------|------|
| **Sender** | 发件人姓名 | John Smith |
| **Email** | 发件人邮箱 | john@abccompany.com |
| **Company** | 客户公司 | ABC Trading Ltd |
| **Country** | 国家/地区 | USA, Germany |
| **Product** | 意向产品 | LED Strip Lights |
| **Quantity** | 采购数量 | 5000 pcs |
| **Target Price** | 目标价格 | $2.50/pc |
| **Lead Time** | 期望交期 | 30 days |
| **Priority** | 优先级 | High/Medium/Low |
| **Content Summary** | 内容摘要 | 询问LED灯带价格... |

### 优先级判断
- **High**: 明确采购意向，有具体数量/价格/交期要求
- **Medium**: 询问产品信息，有潜在采购可能
- **Low**: 仅索取目录/样品，意向不明确

## 每日简报格式

```
📊 外贸询盘日报 - 2026-03-18
=====================================

📈 今日统计
• 总邮件: 45 封
• 询盘邮件: 8 封 ⭐
• 营销邮件: 28 封
• 垃圾邮件: 9 封

=====================================
🔥 高优先级询盘 (3)
=====================================

【询盘 #1】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
客户: John Smith (ABC Trading Ltd)
邮箱: john@abctrading.com
国家: USA
产品: LED Strip Lights - 5050 SMD
数量: 5000 pcs
目标价: $2.50/pc
交期要求: 30 days
优先级: 🔴 HIGH
内容摘要: 客户明确需要5000条LED灯带，目标价$2.50，要求30天交期。已提供具体规格要求。
建议回复: 确认报价和交期可行性

【询盘 #2】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
客户: Maria Garcia
邮箱: maria@euroimport.es
国家: Spain
产品: Bluetooth Speakers
数量: 1000 pcs
目标价: 未提供
交期要求: 45 days
优先级: 🔴 HIGH
内容摘要: 西班牙进口商，需要1000个蓝牙音箱，要求45天交货。询问OEM可能性。
建议回复: 提供报价和OEM选项

【询盘 #3】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...

=====================================
🟡 中优先级询盘 (3)
=====================================
...

=====================================
🟢 低优先级询盘 (2)
=====================================
...

=====================================
📧 待回复清单
=====================================
1. john@abctrading.com - LED Strip Lights (HIGH)
2. maria@euroimport.es - Bluetooth Speakers (HIGH)
3. ...

=====================================
💡 今日建议
=====================================
• 优先处理美国客户的LED询盘，数量大且意向明确
• 西班牙客户有OEM需求，可推荐定制服务
• 建议今日内回复所有高优先级询盘

---
生成时间: 2026-03-18 18:00
来源邮箱: yourname@gmail.com
