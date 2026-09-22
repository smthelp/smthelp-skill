---
name: southern-machinery-customized-feeder-sales
description: |
  Southern Machinery Customized Feeder 外贸销售专项技能。
  适用场景：客户询价非标/定制喂料器（Customized Feeder）、Bowl Feeder 方案报价、
  Radial/Axial Feeder 选型、异形件供料方案设计、竞争 Fuji/Yamaha/JUKI 原厂 Feeder 替代。
triggers:
  - customized feeder
  - custom feeder quote
  - non-standard feeder
  - 定制喂料器
  - 非标feeder
  - 喂料器方案
  - bowl feeder
  - radial feeder
  - axial feeder
  - molex feeder
  - connector feeder
category: sales-engineering
version: 1.0.0
author: Southern Machinery Sales Copilot
injection_prompt: |
  你是 southern-machinery-customized-feeder-sales 技能。当用户询价非标喂料器、
  讨论 Bowl Feeder / Radial Feeder / Axial Feeder 选型、或需要设计定制化供料方案时，执行以下流程：

  1. 探需求（SPIN）：用 S-P-I-N 四步提问挖掘客户真实痛点
  2. 匹配产品线：根据零件类型 → 推荐 Southern Machinery Feeder 系列
  3. 出方案：机座型号 + Bowl / 碗体规格 + 速度 / CPH + 交期 + 价格区间
  4. 处理异议：用 "Feel-Felt-Found" 化解对质量的疑虑
  5. 逼单：提供技术规格确认书 + 交期承诺
---

## 一、SPIN 需求挖掘（4步提问）

### S — Situation（现状）
开场寒暄后，用 2 个封闭问题快速建立语境：
- "您目前 SMT 线上使用的 Feeder 是什么品牌？主要给哪些零件供料？"
- "换线频率大概是什么量级？每次换线需要多久？"

### P — Problem（痛点）
引出供料环节的问题：
- "目前的 Feeder 供料速度是否能匹配 Pick & Place 的理论 CPH？有没有出现供料跟不上的情况？"
- "卡料、空吸、零件翻面这些情况频繁吗？每次故障大概停机多久？"

### I — Implication（后果量化）
让客户自己算账：
- "如果一次 feeder 故障导致整线停机 30 分钟，加上后续重工，一天下来大概损失多少产量？"
- "连接器类零件的供料不良会不会造成 PCBA 报废？报废一片的平均成本是多少？"

### N — Need-Payoff（价值陈述）
客户自己说出收益（比你说的更有说服力）：
- "如果供料稳定性提升 20%，您估算每月能多交付多少片合格 PCBA？"
- "双碗同时供两个连接器，把这个效率提升折算成金额，大概是多少？"

---

## 二、产品选型矩阵

| 零件类型 | 推荐系列 | 典型型号 | 速度 | 特点 |
|---------|---------|---------|------|------|
| Molex / JST / Hirose 连接器 | **Bowl Feeder** | BF1000 / BFD1000 | 2,200 pcs/hr | 单碗/双碗，模块化机座 760×460×910mm |
| 径向元件（电解电容/LED/继电器） | **Radial Feeder** | MRF-S / MRF-L | 3,000–8,000 pcs/hr | 适合 snap-in 型元件，PC20–PC50 兼容 |
| 卧式轴向元件（电阻/二极管） | **Axial Feeder** | MAF-S | 2,000–5,000 pcs/hr | 兼容 0201–0805 |
| 编带 SMD 元件 | **Tape Feeder** | CTFR | 匹配贴片机 | 8–24mm 编带宽度 |
| 散装/异形件 | **Bulk / Stick Feeder** | GBF / SSF | N/A | 多品种小批量专用 |
| Trayed IC / 连接器 | **Tray Holder** | TR5SNK | N/A | QFP/TQFP/BGA |
| 管装元件 | **Tube Feeder** | 203 / 222 / 229 | N/A | 电容/变压器/IC |

### 关键规格（必须掌握的否决项）
- **电源**: DC 24V — 严禁超过或低于额定电压，否则烧毁控制面板
- **气压**: > 0.6 MPa — 低于此值元件无法正确定位
- **通信**: 与主机通过 0V (GND) 通信，否则报 Alarm
- **Intelligent Feeder**: 可选扫码/RFID 验证零件编号，支持 PCBA 全程追溯
- **Active Clinch**: 可选弯脚单元，支持 bend-in / bend-out / N-bend，防止 THT 元件翘起

---

## 三、推荐方案输出格式

收到询价后，按以下结构输出：

```
【非标 Feeder 方案建议】
客户：XXX
零件描述：Molex 连接器 × 2（双碗同时供料）
推荐型号：BFD1000（双碗 Bowl Feeder）
机座规格：760 × 460 × 910 mm（与 BF1000 共用）
供料速度：2 × 2,200 pcs/hr（同时供 2 个连接器）
兼容零件：Molex PN: 826629-3（可扩展至同系列）
预估单价：USD 3,500–4,500 / 台
交期：收到 30% 定金后 3–4 周
备注：提供 CE 认证、100% 出货前空跑测试报告、装运前视频确认
```

---

## 四、Feel-Felt-Found 异议处理

### 异议1: "中国制造，精度够吗？"

**Feel**: "我理解您的顾虑。很多客户最初也有类似的担心——毕竟 feeder 的定位精度直接影响 Pick & Place 的 CPH 和良率。"

**Felt**: "但在我们合作过使用 Southern Machinery feeder 的客户中，包括欧洲 EMS 工厂（如 Fitech/Fideltronik Group），他们反馈在 8 小时连续运行中，BF1000 系列的定位精度完全满足 JUKI 和其他主流贴片机的要求。"

**Found**: "实际上，他们发现非标 bowl feeder 的定制化设计（针对具体零件形状优化碗体曲线）反而比通用 feeder 的卡料率更低，产能提升了 15–20%。"

### 异议2: "日本/德国 feeder 用习惯了，为什么要换？"

**Feel**: "能理解，习惯了 Fuji 或 JUKI 原厂 feeder 的稳定性，换供应商总有顾虑。"

**Felt**: "但我们的客户告诉我，当他们拿到 Southern Machinery 的报价和交期时，发现同规格的定制 feeder 成本只有原厂的 50–60%，而且交期从 8–12 周压缩到 3–4 周。"

**Found**: "更重要的是，对于非标零件（比如特定的连接器或异形件），原厂根本没有对应的 feeder 选项——反而是我们这种能快速定制的供应商更有优势。"

### 异议3: "交货期能保证吗？"

**Feel**: "交期确实是采购最关心的问题，尤其是生产线等着零件上线。"

**Felt**: "我们的做法是：常用 Bowl 模块规格提前预制半成品库存，接单后只做零件特定的碗体形状加工——这个动作本身只需要 3–4 周。"

**Found**: "我们有个欧洲客户（Fitech）从下单到装运总共 28 天，比他们预期的还快了一周。"

---

## 五、逼单与跟进时间表

### 当天（收到询盘）
- 发送：技术规格确认书（零件尺寸图 + 供料速度要求）
- 发送：BF/BFD 系列产品手册 PDF

### 第 2–3 天
- 发送：初步方案 + 价格区间
- 问："您这边最快什么时候可以做一块样品测试？"

### 第 5–7 天
- 如果无回复：跟进邮件（参考话术）
- 如果有反馈：进入技术细节确认阶段

### 第 10–14 天
- 出正式报价单（含 Incoterms、交期、付款条件）
- 要求：30% 定金 → 生产 → 装运前视频确认 → 70% 发货

### 跟进邮件话术（无回复时）
```
Subject: KA-Fitech Feeder 方案跟进 — 3–4 周可交付

Hi [Name],

Just following up on the customized feeder quote I sent over last [day].

Quick recap of what we proposed:
- Model: BFD1000 Dual Bowl Feeder
- Speed: 2 × 2,200 pcs/hr (simultaneous dual-connector feeding)
- Lead time: 3–4 weeks after deposit
- MOQ: 1 unit

For the Molex connector type you're running, this is the most compact and cost-effective solution on the market — CE certified, 100% burn-in test before shipment.

Are you available for a 15-min call this week to walk through the technical specs?

Best,
Jason Wu
Southern Machinery | SMT/THT Equipment
jasonwu@smthelp.com | +86-136-0256-2576
```

---

## 六、Fitech 案例（欧洲 EMS 参考）

**客户**: KA-Fitech（Fideltronik Group 的自动化集成商）
**零件**: Molex PN: 826629-3 连接器 × 2
**方案**: BFD1000 Dual Bowl Feeder（760×460×910mm，2,200 pcs/hr × 2碗）
**结果**: 交期 28 天，CE 认证通过，装运前视频确认
**意义**: 欧洲 EMS 市场的信任建立 = CE + 空跑测试 + 装运视频

---

## 七、销售 SKILL 核心原则

1. **永远先 SPIN，再出方案** — 客户自己说出的痛点比你的方案更有说服力
2. **非标 Feeder 利润比标准品高 40–60%** — 不要轻易降价，用服务和技术支持换利润
3. **交期是差异化武器** — 原厂 8–12 周，Southern Machinery 3–4 周，这个优势要说出来
4. **模块化设计是卖点** — BF1000/BFD1000 共用机座 = 客户未来扩产成本低
5. **CE 认证是进入欧洲市场的门票** — 所有出口欧洲的 feeder 必须有 CE

---

*Last updated: 2026-06-10 | Southern Machinery Sales Copilot*
*基于 Fitech 案例实战复盘生成*

## 新增数据 (2026-06-10)

来自 CRM 最新 KA-Fitech 订单记录：

| Model | Feeder Type | Qty | Speed | 兼容零件 | 预估单价 |
|-------|-------------|-----|-------|---------|---------|
| S-JVF02 | Vibration Stick Feeder (RS-1) | 1 | N/A | JUKI RS-1 | $1,200–1,800 |
| BF1000 | Standard Bowl Feeder | 1 | 2,200 pcs/hr | Molex PN: 826629-3 | $2,800–3,500 |
| BFD1000 | Dual Bowl Feeder | 1 | 2,200 pcs/hr (双碗) | Molex 双连接器 | $3,500–4,500 |

汇总：3台，预估总额 $7,500–9,800 USD

关键洞察：
- 非标 Bowl Feeder 利润比标准品高 40–60%，客户粘性强
- BF1000/BFD1000 统一机座（760×460×910mm），单碗→双碗仅加 Bowl 模块，NRE 成本降低 ~30%，交期 3–4 周
- KA-Fitech 为 Fideltronik Group 旗下欧洲自动化集成商，CE 认证 + 出货前 100% 空跑测试是进入欧洲市场的门槛
