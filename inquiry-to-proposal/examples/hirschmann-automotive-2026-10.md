# Hirschmann Automotive｜连接器插针机（Stitching）询盘分析

> 询盘：2026-09-25 首发（Jörg Eckert，总部采购）→ 10-07、10-14 两次催复（Cornel Vasile，罗马尼亚）。**我方已约 3 周未回复，需今天回。**
> 性质：群发 RFI（"Dear Sir or Madam"）+ 市场技术摸底，不是 RFQ。目标是选出"标准化、成熟"的插针平台，降低定制带来的投资、交期和风险。

---

## 1. 客户背调

| 项目 | 内容 | 来源 | 可信度 |
|---|---|---|---|
| 公司 | Hirschmann Automotive GmbH，奥地利 Rankweil，成立 1959 | 官网 | 高 |
| 股权 | 100% 私有，最终由 Rauch 私人基金会持有（Rauch 果汁家族），不缺钱、决策稳 | 2024/2025 GRI 可持续报告 | 高 |
| 行业 | 汽车一级/二级供应商：连接器、线束组件、传感器、高压连接器（HPS 系列）、注塑包封；拓展微出行 | 官网 | 高 |
| 规模 | 全球约 7,100 人；生产基地：奥地利、德国 Freyung、捷克 Vsetín、罗马尼亚、摩洛哥 Kenitra、墨西哥 San Miguel、中国南通 | 官网/GRI | 高 |
| 集团营收 | 2022 €531M → 2023 €617M → 2024 €589M（下滑） | GRI 2024 | 高 |
| 母公司（奥地利法人） | 2025 营收约 €515.9M，净利约 €49.4M | firmenakte.at（第三方摘录） | 中 |
| 罗马尼亚工厂（发件方） | Hirschmann Automotive TM SRL，2007 成立，集团最大工厂（Chirileu + Sânpaul 两厂）；2025 营收 RON 659.8M（约 €132M，**-15.9%**），**净亏 RON 1.3M**，员工 1,698（-6.7%） | comercial.ro / atlasfirme / ZF | 中高 |
| 终端客户 | 德系 OEM（Daimler、BMW、VW 集团等） | ro.wikipedia；Nesensohn 头衔含"VW Group" | 中 |

**经营判断**：集团盈利但增长放缓，罗马尼亚厂 2025 年收入降、转亏 → 降本压力大。这正好解释了询盘的核心诉求："少定制、低投资、短交期、低风险"。

**可能采购规模（推测）**：
- 这是战略级平台评估，覆盖 8–270 pin、10 万到数百万/年四档产能 → 若选定，可能多台、多工厂复制（罗马尼亚优先，摩洛哥/墨西哥/中国待确认）。
- 单个项目首单更可能是 1–2 台试点（**待确认**）。
- 预算周期：Q4 正值 2027 年资本预算编制期，进入短名单的时间窗口就是现在（**推测**）。

**决策链**：
| 人物 | 职位 | 角色判断 |
|---|---|---|
| Christian Stroj | 全球间接材料与投资采购总监（总部） | 经济决策/商务把关人 |
| Stefan Nesensohn | VW 集团项目工艺开发负责人（总部） | 技术评估人/用户，**技术上的关键人** |
| Jörg Eckert | 采购（总部） | RFI 发起人 |
| Calin Guta | 罗马尼亚采购组长 | 本地采购管理 |
| Cornel Vasile | 罗马尼亚间接材料采购 | 执行人，负责收集供应商回复 |

**信息缺口（待确认）**：附件 PPT（产品/工艺谱系）我们是否收到；目标工厂和首个项目；具体连接器型号/图纸/pin 规格（线径、方针/圆针、长度、料带还是线材）；目前用的是哪家插针机；预算与评估时间表；是否需要 CE/机械安全 Directive、本地服务合同。

---

## 2. 联系人画像：Cornel Vasile

- **职位/职权**：罗马尼亚厂间接材料采购。负责收集信息、催进度、整理对比表；**没有技术否决权和最终拍板权**，但他的对比表决定我们能不能进短名单。
- **沟通风格**：正式、礼貌、模板化；两周内两次催复，且第一次说"本周内可联系我" → 有内部截止期，在被上级追进度。
- **痛点**：要按时交齐供应商对比（可能是 Excel 打分表），供应商回复不完整或太慢让他难做。
- **关注点**：回复完整度（逐条对应清单）、价格与交期、本地服务、制造地。
- **潜在异议**：中国供应商的售后与备件响应；机器是否真的"标准"；是否有汽车行业连接器插针案例；CE 合规；语言和时差。
- **性格推测**：流程型、规则导向，偏谨慎（**推测**）。
- **采购意向**：中等。目前在"市场调研/长名单"阶段，主动催了两次说明他需要我们的回复来完成名单，但不代表已有明确采购计划。
- **策略**：给他一份"可直接粘进对比表"的结构化回复；技术深度留给 Nesensohn。

---

## 3. 匹配方案

### 先说最关键的判断
客户明确写了：**是连接器插针（把 pin 插进塑料胶壳做排针/连接器），不是 PCB 插针**。我司 S7020 / S7020T / S7000P 是**按 PCB 设计**的标准 THT 插件平台。要用于胶壳插针，需要把 PCB 夹具换成**胶壳定位治具（quick-change nest）**，并验证 pin 供料（料带 vs 线材）。这一点必须如实讲，否则后续技术评估会被一票否决。

### 推荐清单（参数来自官网，价格/交期由 Jason 填写）
| 产品 | 已公开规格 | 适配点 | 局限 |
|---|---|---|---|
| **S7020T 双头端子插件机**（主推） | 12,000 CPH（0.55 s/点）；料盘/振动盘供料；视觉校正 0.015 mm；插入力检测（选配）；扫码防错；RS-232C/以太网/MES；夹持范围 80×80–380×280 mm；端子厚 0.5–1.2 mm | 高混合、换型靠程序 + 治具；中低产能 | 无标准折弯、清洁、托盘包装模块；插入力检测非完整力-位移曲线（待确认） |
| **S7000P 插针机**（备选） | 8,000 pcs/h；料带 pin，1.2–4.0 mm pin；1–3 个插头，可同时插不同 pin；工控机，多点 Mark 视觉校正 | 多种 pin 混插 | 官网注明需先评审治具与产品验证，即需要一定配置工作 |
| **S7020 双头 PIN/铆钉机** | 12,000 CPH，360° 插入角，内/外弯脚 | 同平台 | 同上 |

### 逐条需求对应
| 客户要求 | 我方 | 说明 |
|---|---|---|
| 8–270 pin、多种外形与节距 | 部分满足 | 程序可编；每个胶壳族需要专用治具（**待确认**治具成本与换型时间） |
| 直针/弯针 | 直针可以；**弯针不满足** | 无标准折弯模块 |
| Press-fit pin 和焊针 | 待确认 | 取决于 pin 截面与料带形式，需要样品验证 |
| 周期/产能 | 满足 10 万–100 万档 | 见下方产能估算 |
| 换型时间 | 待确认 | 程序切换快，治具快换方案需确认 |
| 供料（pin + 胶壳） | pin：料盘/振动盘 ✓；胶壳：**需要人工或另配上料** | 自动上下料需定制 |
| 视觉 / pin 有无 / 位置朝向 | 部分满足 | 有视觉校正与漏插检测；插后 100% pin 检测待确认 |
| 力-位移监控 | 部分（插入力检测选配） | 是否能输出每针 F-D 曲线（**待确认**） |
| 清洁、折弯、打标追溯、托盘包装 | 标准机不含 | 有扫码 + MES 数据，打标/包装需外配 |
| 投资、交期、培训、服务、制造地 | 价格/交期待 Jason 填写；深圳制造；远程在线支持 | 欧洲本地服务（**待确认**是否有罗马尼亚/东欧服务伙伴） |

### 按产能分档的建议（假设 3,000 有效小时/年，即两班约 75% OEE，**估算**）
| 年产能 | 建议 | 说明 |
|---|---|---|
| 10 万/年 | 1 台 S7020T + 快换治具 | 270 pin 的产品约 13 万/年·台，可覆盖 |
| 50 万/年 | 1–2 台 | 50 pin 的产品约 72 万/年·台 |
| 100 万/年 | 2–3 台（视平均 pin 数） | 100 pin 的产品约 36 万/年·台 |
| 数百万/年 | **不推荐我司标准机** | 该档需要连续式/多工位专用插针机，诚实告知可赢得信任 |

### 差异化卖点
1. 标准机型、程序换型，投资远低于欧洲定制插针机（价格待填）。
2. **用客户样品做免费在线演示**，提交一页评估报告 + ROI（我司惯用打法）。
3. 30 年 THT 自动插件经验；服务过 Signify、Flex、Schneider 等全球工厂。
4. 数据接口（MES/扫码防错）满足汽车追溯基础要求。

### 风险提示
- **核心风险：PCB 平台 ≠ 胶壳插针平台**。如果客户要的是"线材下料 + 切断 + 插入 + 折弯"的经典 stitching 机，我们不是对口产品。
- 欧洲本地服务、CE 合规文件、汽车行业连接器案例都是短板，回答要实事求是。
- 不要给出无法兑现的周期/CPK 承诺；未经样品验证不承诺 press-fit 质量。
- 2027 预算窗口内可能已有欧洲供应商在跟进，速度和清晰度是我们的机会。

---

## 4. 跟进计划
| 阶段 | 时间（北京时间） | 目标 | 待确认事项 |
|---|---|---|---|
| ① 首次回复 | **10-15（今天）21:00 前**（罗马尼亚 16:00 前） | 致歉延误；给出标准平台概览与诚实定位；索取附件和样品 | 价格区间、交期、CE |
| ② 资料包 | 10-22 前 | 发 S7020T/S7000P 规格书、按产能分档配置表、预算价区间、视频案例；邀请 30 分钟技术通话（Nesensohn） | pin 规格、胶壳图纸、目标工厂 |
| ③ 样品验证/在线演示 | 10-29 至 11-06 | 收样品后用实机在线演示，出一页评估报告 + ROI | 治具方案、换型时间、F-D 能力 |
| ④ 正式报价与促单 | 11-13 至 11-30 | 正式报价（含治具、备件包、培训、远程服务）；争取进 2027 预算短名单；提出试点 1 台 | 决策时间表、付款与验收条款 |

> 如果第②步后 7 天无回音：给 Cornel 发一封简短跟进，并抄送 Nesensohn，内容只提一个价值点（如免费样品演示）。

---

## 英文回复邮件（v1）

To: Cornel.Vasile@hirschmann-automotive.com
Cc: Joerg.Eckert@hirschmann-automotive.com; Stefan.Nesensohn@hirschmann-automotive.com; Calin.Guta@hirschmann-automotive.com; Christian.Stroj@hirschmann-automotive.com

Subject: RE: Request for Standard Connector Stitching Machine Solutions – Southern Machinery Standard Platform Overview

Dear Mr. Vasile,

Thank you for your follow-up, and please accept our apologies for the delayed response to Mr. Eckert's request of September 25.

We have reviewed your requirements carefully and want to give you a clear, honest picture of where our standard platforms fit.

1. Our standard platform
Our S7020T dual-head insertion machine is a series-built, servo-driven platform (12,000 insertions/hour theoretical, reel or bowl feeding, vision correction 0.015 mm, optional insertion force detection, barcode verification and MES interface). The platform was originally designed for PCB-based insertion. For connector stitching into housings, the machine stays standard, while housing nests and pin feeding are configured per connector family. We will state these configuration points openly in our proposal.

2. Recommended scope by annual volume (preliminary, to be confirmed with your samples)
- 100,000 to 500,000 connectors/year: 1 to 2 S7020T cells with quick-change housing nests
- 1,000,000 connectors/year: 2 to 3 cells, depending on average pin count
- Several million connectors/year: in our view a dedicated continuous stitching concept is more suitable, and we would not recommend our standard platform for this range.

3. Standard features vs. options
- Standard: vision correction, missing-insertion detection, barcode/QR verification, data export to MES
- Optional: insertion force detection
- Not standard (would require customization): pin bending, cleaning, marking, automated housing loading/unloading, tray packaging

4. Commercial overview
- Budget price per standard cell: [EUR price range]
- Standard lead time: [X weeks]
- Manufacturing location: Shenzhen, China
- Training: [on-site / remote training concept]
- Service and spare parts: remote online support, [spare parts stock and delivery time], [local service partner in Europe, if any]

Proposed next step
We would be glad to run a free online demonstration with your actual connector samples on our machine, followed by a one-page evaluation report covering cycle time, quality results and ROI. To prepare this, could you kindly share:
- The presentation attached to the original request
- Drawings or samples of 2 to 3 representative connectors
- Your preferred timeline for the evaluation

We will send the technical datasheets and a configuration matrix by [date].

Best regards,
Jason Wu
