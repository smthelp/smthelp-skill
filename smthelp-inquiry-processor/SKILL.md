---
name: smthelp-inquiry-processor
description: "Southern Machinery SMTHELP 客户询盘全流程处理技能。当用户提供海外客户（EMS/ODM/LED显示屏/汽车电子/医疗电子等）通过邮件、WhatsApp 或 LinkedIn 发来的设备询盘原文时自动触发，执行：客户背调画像、5维询盘扫描、设备方向判定、产品匹配（结合 IMA 知识库）、销售内部分析（中文）、客户英文回复邮件、行动计划。输入为客户询盘原文（粘贴或转发），输出为一份结构化 Markdown 报告文件及可直接发送的英文跟进邮件。"
agent_created: true
---

# SMTHELP 询盘全流程处理技能

## 技能目的

本技能封装了处理 Southern Machinery SMTHELP 海外客户设备询盘的**完整 SOP**，覆盖从收到原始询盘到输出可执行的销售分析报告和英文回复邮件的全流程。适用于贴片机、插件机、回流焊、AOI/SPI、传送设备、料盘存储架、清洗设备及整线方案等所有设备品类。

## 触发条件

用户提供以下任一形式的客户询盘时立即触发：
- 粘贴邮件原文（含发件人、收件人、日期、主题、正文）
- 转发 WhatsApp/LinkedIn 询盘文本
- 提供 PDF/截图格式的询盘（先提取文字再处理）
- 明确说"分析这个询盘"、"帮我回复这个客户"、"做客户背调"

## 核心工作流（7步法，严格顺序执行）

### 第1步：客户背调 — 多源交叉验证

**目标**：5分钟内构建客户360°画像。

**信息来源（按优先级）**：

1. **公司官网** — WebFetch 抓取 About/Products/Manufacturing 页面
2. **LinkedIn** — WebSearch "[公司名] LinkedIn employees revenue"
3. **财务数据库** — WebFetch craft.co / getlatka.com / rocketreach.co / dnb.com 获取营收、员工数、融资
4. **行业新闻** — WebSearch "[公司名] manufacturing SMT factory"
5. **联系人定位** — WebSearch "[联系人姓名] [公司名] LinkedIn role"

**必须提取的维度**：

| 维度 | 数据点 |
|------|--------|
| 公司身份 | 全称、成立年份、总部、分支 |
| 财务规模 | 年营收（或估值/融资总额）、员工数 |
| 产品业务 | 核心产品线、服务行业、商业模式 |
| 制造能力 | 自有工厂/SMT产线/外包/新建、工厂面积、认证（ISO/AS9100/IATF） |
| 联系人 | 姓名、职位、决策权重判断、性格风格推断 |

**特殊场景识别**：
- EMS/CM → 关注设备品牌、产能、客户行业
- 自有品牌制造 → 关注产品复杂度、PCB工艺特点
- 新建项目 → 关注融资、选址、团队背景
- 活动/租赁公司建厂 → 关注垂直整合动机、成本敏感度

### 第2步：5维询盘扫描

从询盘原文提取以下5个维度，能提取的填入，提取不到的标「未知」：

| 维度 | 提取关键词 | 判断什么 |
|------|-----------|---------|
| **行业** | automotive / medical / consumer / industrial / telecom / LED display / EMS/CM | 合规要求、认证门槛、洁净度 |
| **产品类型** | PCB / PCBA / board / module / assembly / LED module / connector | 工艺路线（SMT为主 / THT为主 / 混装） |
| **产能信号** | monthly volume / CPH / shift / lines / sqm per month | 设备规模、ROI测算基准 |
| **现有产线** | existing line / current brand / Hanwha / Yamaha / Panasonic / serial number | 是新线、扩线、换线还是配件采购 |
| **痛点/需求** | yield / defect / labor / changeover / simple / no automation / budget | 核心诉求锚定 |

**特殊信号**：
- 客户指定具体型号 → 已做过市场调研，直接推该型号或对标替代
- 客户排除智能功能 → 推被动版/基础版，不要硬推智能版
- 仅需配件/备件 → 走 After-Sales 快速通道，重点是响应速度
- 客户列出竞争对手型号 → 做竞品对标分析

### 第3步：设备方向判定

根据第2步扫描结果，归入以下方向之一：

| 方向 | 触发信号 | 推荐设备组合方向 |
|------|---------|----------------|
| **SMT 新线** | 提到 SMT / pick & place / reflow / 整线 | 印刷机 → SPI → 贴片机(×2) → 回流焊 → AOI → 上下板机 |
| **THT 插件** | 提到 through-hole / axial / radial / DIP / 波峰焊 | S4000 → S3000 → S7900 → 波峰焊/选择波峰焊 |
| **odd-form 异形** | 提到 connector / transformer / relay / 大端子 | S7900 + S7020 + 散料供料器 |
| **PCB handling** | 提到 conveyor / buffer / loader / unloader | 接驳台、缓存机、翻板机、上下板机 |
| **清洗** | 提到 cleaning / flux residue / medical / aerospace | 水洗/溶剂清洗设备 |
| **改造升级** | 提到 upgrade / replace / bottleneck / OEE | 旧线评估 → 局部升级 |
| **🔧 After-Sales** | 提到 spare parts / belt / serial number / repair | 快速响应 → 原厂配件匹配 |
| **📦 仓储/物料** | 提到 storage rack / reel storage / magazine | 料盘存储架/物料管理设备 |

**产能验证（整线询盘时必做）**：
- 将客户目标产能换算为所需 CPH（贴装点/小时）
- 用目标产能 ÷ 单机 CPH ÷ 22天 ÷ 20小时 ≈ 所需贴片机数量
- 若客户配置严重不匹配目标，必须在分析中指出

### 第4步：产品匹配 — 知识库搜索

**搜索源（并行查询）**：

1. **smthelp.com 产品页面** — WebSearch `site:smthelp.com [关键词]` 或 WebFetch 分类页
2. **IMA 知识库 KB1**（kb_id: `7300441431899003`）— Auto Insertion Machine 产品手册、SMT教材
3. **IMA 知识库 KB2**（kb_id: `0019c8357ac06861`）— S-MVF01 散料供料器、THIM3-T 等

**搜索关键词示例**：
- 贴片机：`pick and place machine LED SMT CPH specifications`
- 料盘架：`reel rack storage 7inch 13inch SIS7000A SIS4000A`
- 传送带：`conveyor belt S-460C replacement spare parts`
- 回流焊：`reflow oven 10 zone specifications`

**竞品对标（客户指定竞品型号时）**：
- WebSearch `[竞品型号] specifications CPH price comparison`
- 提取竞品 CPH、价格区间、优势/劣势
- 匹配 Southern Machinery 对标型号

### 第5步：销售内部分析报告（中文）

按模板输出，写入文件：`[客户简称]-[询盘主题]-RFQ-Analysis.md`

**必须包含的章节**：
1. **客户背调画像** — 公司概览表 + 产品线 + 认证 + 制造能力 + 联系人分析 + 客户价值评级
2. **询盘分级内部分析** — 5维扫描表 + 方向判定 + 优先级 + 3-5条依据
3. **产品匹配与方案推荐** — 推荐产品 + 规格参数 + 方案差异化优势
4. **卖点锚定** — OEE/人工/良率/换线/ROI 中选择1主1辅
5. **英文回复邮件** — 可直接发送的完整邮件正文
6. **行动计划** — P0/P1/P2 优先级动作 + 索取资料清单 + 跟进时间表
7. **附录** — 联系人表、产品链接、竞品参考、信息缺口清单

**写作铁律**：
- **结论先行**：第一句就是方向+优先级+跟进建议
- **每条依据对应一个事实或推导**，不空话
- **不编造客户没说的信息**，未知就是未知
- **信息不足时先给框架**，标注【假设】，把索取信息列为最高优先级
- **不锁型号、不报价**（型号留给 sales-copilot 选型）

### 第6步：英文客户回复邮件

**风格要求**：
- 专业、克制、匹配客户身份和沟通风格
- 工程师型客户 → 简洁直接、给技术信息
- 采购型客户 → 结构化、给对比选项
- CEO/Founder → 视野高度、给ROI和战略价值
- 不吹嘘、不用感叹号、不堆形容词

**结构要素**：
1. 感谢 + 确认理解客户需求
2. 推荐方向说明（3-5句，聚焦工艺匹配度）
3. 差异化价值（1-2个卖点）
4. CTA（三选一，只能一条）：

| CTA | 适用场景 |
|-----|---------|
| **Book a line assessment** | 客户有现有产线，提了升级/瓶颈/OEE痛点 |
| **Send BOM and PCB files** | 客户给了产品描述但缺工艺细节 |
| **Request turnkey proposal** | 客户明确要整线方案，有产能目标 |

**落款格式**：统一用 `Best regards, [销售名] Southern Machinery SMTHELP`

### 第7步：行动计划

**P0 — 24小时内的动作**：
- 发送英文回复邮件
- 内部通知销售和产品团队

**P1 — 48小时内的动作**：
- 索取缺失信息（BOM / Gerber / 目标产能 / 现有设备 / 预算）
- 准备产品视频和规格书

**P2 — 7天内的动作**：
- 发送定制方案
- 安排视频会议或工厂参观

**特殊标注**：
- 长期价值评估（客户是否有后续整线需求）
- 竞品风险提示
- 物流/关税注意事项（跨境客户）

## 知识库参考

处理后两步必定调用的知识源：

- **IMA 知识库 #1**（kb_id: `7300441431899003`）：Auto Insertion Machine — S3000/S4000/S3820A/S7900/S7020 系列手册、SMT 教材、自动化方案图、THT PCB 设计指南
- **IMA 知识库 #2**（kb_id: `0019c8357ac06861`）：S-MVF01 散料供料器、THIM3-T 端子插件机手册、设备电气图纸、SMT 工艺教材
- **smthelp.com**：官方产品目录，通过 WebSearch + WebFetch 获取最新产品信息

## 输出文件规范

- 分析报告：保存到当前项目根目录，文件名格式 `[客户简称]-[询盘主题]-RFQ-Analysis.md`
- 文件编码：UTF-8
- 完成后调用 `present_files` 展示报告文件
- 同时追加到 `.workbuddy/memory/YYYY-MM-DD.md` 完成工作记录

## 常见场景速查

| 场景 | 关键动作 | CTA选择 |
|------|---------|---------|
| 配件/备件询盘 | 序列号匹配 + 原厂OE锁定 | Send serial number photo |
| 单一型号询价 | 直接推该型号 + 问数量 | Request quotation details |
| 整线RFQ | 产能验证 + 竞品对标 | Request turnkey proposal |
| 客户排除智能功能 | 推被动版/基础版 | Send BOM and PCB files |
| 海外建厂客户 | 物流分析 + 当地服务能力 | Book a line assessment |
| 融资中初创 | 突出ROI + 分阶段方案 | Send BOM and PCB files |
