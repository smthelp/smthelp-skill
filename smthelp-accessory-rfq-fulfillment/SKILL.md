---
name: smthelp-accessory-rfq-fulfillment
description: "Southern Machinery SMTHELP 配件/耗材/ESD 类海外客户询盘的履约技能。当客户提供海外客户（EMS/ODM/贸易商/电商）发来的备件、SMT/ESD 附件、防静电周转、料盒料架、接驳台皮带等附件耗材询盘，并要求：①从淘宝/1688/Alibaba(含 Made-in-China)搜索汇总 3 家优质供应商并比价（价格/交期/保修/售后/联系方式）；和/或 ②结合 Southern Machinery 自有产品目录生成品牌化解决方案（HTML 客户版 + 英文报价邮件）时触发。输入为询盘原文（Excel/PDF/图片/粘贴文本），输出为供应商对比报告与/或品牌化 HTML 方案 + 英文报价邮件。"
agent_created: true
---

# SMTHELP 配件/耗材询盘履约技能

## 技能目的

把"收到海外客户附件/耗材/ESD 类询盘 → 三平台供应商比价 → 映射南方机械自有产品 → 输出品牌化方案"这一套我们已验证可复用的流程固化下来。覆盖两条互补支线，可单跑也可串跑：

- **Mode A 供应商比价**：从淘宝 / 1688 / Alibaba（及 Made-in-China）搜出 3 家优质供应商，对比价格、交期、保修、售后、联系方式，输出 Markdown 对比报告 + RFQ 邮件模板。
- **Mode B 品牌化方案**：读取 Southern Machinery 自有目录（本地 PDF / IMA 知识库），把客户每条需求映射到 SMTHELP® 型号，生成带 Logo 与社交 CTA 的品牌化 HTML 客户方案 + 英文报价邮件（含内部定价参考块）。

## 触发条件

以下任一即触发，并按指令判断跑 Mode A、Mode B 还是两者：
- "从淘宝/1688/alibaba 搜索 N 家供应商，比价 + 联系方式"
- "结合 Southern Machinery 产品给我出一份给客户的解决方案/提案"
- 提供 Excel/PDF/图片询盘，且品类为：备件、SMT 附件、ESD 周转车/料架/料盒、防尘罩、接驳台皮带、料盘存储等
- 明确"做供应商对比报告"或"出 HTML 客户版 + 英文报价邮件"

> 若是**整机/整线设备询盘**（贴片机、回流焊、波峰焊、AOI 等），改调 `smthelp-inquiry-processor` 技能，不要走本技能。

## 品牌资产（写死，所有交付物复用）

```
Logo (header 左上角):
  https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png
官网:        www.smthelp.com
销售邮箱:    sales@smthelp.com
社交/目录页脚 CTA:
  LinkedIn Company Page : https://www.linkedin.com/company/smtmachine
  LinkedIn Profile      : https://cn.linkedin.com/in/smtsupplier
  Twitter               : https://twitter.com/smtspecialist
  Facebook              : https://www.facebook.com/autoinsertion
  YouTube Channel       : https://www.youtube.com/c/Smthelping
  机器目录              : https://file.autoinsertion.com
  机器图片              : https://ph.smthelp.com
```

## 通用前置：解析询盘

先把客户清单结构化。支持三种来源：

**Excel（.xlsx）** — 用隔离 Python 环境（openpyxl）：
```bash
cd "<询盘所在目录>"
"C:/Users/Admin/.workbuddy/binaries/python/envs/default/Scripts/python.exe" -c "
import openpyxl
wb = openpyxl.load_workbook('Shop supply items.xlsx', data_only=True)
for ws in wb.worksheets:
    for row in ws.iter_rows(values_only=True):
        if any(c is not None for c in row):
            print([str(c).replace(chr(10),' / ')[:120] if c is not None else '' for c in row])
"
```
> 若 `envs/default` 不存在，先建：`"...\python\versions\3.13.12\python.exe" -m venv "...\python\envs\default"`，再 `venv\Scripts\pip install openpyxl pdfplumber`。

**PDF** — `pdfplumber` 提取文本（同上 venv）。

**图片/粘贴文本** — 用 Read 工具读图片，或直接解析粘贴文本。

提取字段：序号、品名、数量、规格备注（尺寸/材质/颜色/认证/配件要求）。

## Mode A — 三平台供应商比价（SOP）

1. **WebSearch 多平台并行**，每个物料用 `query_keyword_groups` 同时覆盖：
   - `淘宝 [型号/描述] 价格`
   - `1688 [型号/描述] 厂家`
   - `Alibaba/Made-in-China [英文描述] supplier`
   - 必要时 `site:1688.com ...` / `site:alibaba.com ...` 精确过滤
2. **筛 3 家优质供应商**，优先级：出口经验、经营年限、认证（ISO/BV）、响应快、报价/保修清晰、有真实联系方式。
3. **WebFetch 抓详情**：供应商联系页 / 产品页，提取 公司名、联系人、email、电话、WhatsApp、WeChat、地址、价格(币种)、MOQ、交期、保修、售后、付款方式。
4. **产出 Markdown 报告** `references/supplier-comparison-template.md` 为骨架，含：
   - 3 家供应商卡片（平台/联系人/核心优势）
   - 分物料报价对比表
   - 综合评分（价格/交期/保修/服务/库存 5 维）
   - 采购推荐（主供 + 议价筹码 + 谈判要点 + RFQ 邮件模板）
   - 风控提示（尺寸美标/公制差异、打样确认导电性能等）

## Mode B — 品牌化方案（SOP）

1. **读南方机械目录**：本地 PDF（如 `ESD PCB Rack Storage (Trolley).pdf`、`Southern Machinery ESD series 2022--Catalogue.pdf`、`SMThelp Smart EMS Factory Accessory Catalogue.pdf`）用 pdfplumber 提取；并按需检索 IMA 知识库 KB1 `7300441431899003`(Auto Insertion)、KB2 `0019c8357ac06861`(吴家兴)、KB3 `7399641549132739`(SMT设备)。注：ESD/耗材数据常不在 KB 中，以本地目录为准。
2. **逐条映射**：每条客户需求 → SMTHELP® 型号；诚实标注 近配 vs 需开模（尤其美标英寸尺寸 NDC/PB，标准料盒高度常偏矮，建议"标准近配 + 按图开模"双选项）。
3. **生成 HTML 客户版**：复制 `references/sm-solution-html-template.html`，填入型号/参数/报价占位 `[ ___ ]`，header 用上面 Logo，footer 用上面社交 CTA。自包含、可浏览器打开或"打印→存 PDF"。
4. **生成英文报价邮件**：复制 `references/quotation-email-template.md`，填 9 项报价表，末尾 INTERNAL 定价参考块（基于 Mode A 市场锚价，发送前删除）。

## 风格与风控（贯穿所有交付物）

- 简洁、专业、咨询式 solution-selling；以客户收益（产能/良率/省人/ROI）为主。
- 给最终方案前先问 2–4 个澄清问题（如走标准近配还是精确开模）。
- 价格来自网络仅为指示性锚价，必须标注 FOB 且内部留底，不可当作正式报价直接发给客户。
- 诚实标注尺寸/认证差距，不夸大标准件匹配度；NDC/PB 美标尺寸务必让供应商书面确认或明确开模费与交期。
- 引导客户访问 www.SMThelp.com、下载目录、WhatsApp/邮件索报价与 layout 设计。

## 交付物命名

```
[客户简称]-[品类]-Supplier-Comparison.md          # Mode A
[客户简称]-[品类]-SM-Solution.html                 # Mode B 客户版
[客户简称]-[品类]-Quotation-Email.md               # Mode B 英文邮件
```
