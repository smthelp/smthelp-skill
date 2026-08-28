---
name: smthelp-inquiry-followup
description: "SMT 设备询盘跟进：判断询盘真伪与阶段、补齐资格审查数据、生成分层跟进话术与下一步动作。收到海外询盘、要跟进客户、判断是真买家还是竞品探价、写跟进邮件时触发。"
---

# 询盘跟进（SMT 设备外贸）

## 核心定位

询盘跟进的失败通常不是回复慢，而是**没有把客户状态、缺口数据、下一步动作分清楚**，导致每次跟进都在重复问同样的东西，或者被竞品用一句"how much"牵着走。

本 skill 的输出不是一封邮件，是一份**跟进决策**：这个询盘现在处于哪一层、还缺什么数据、这次联系要拿到什么。

## 触发场景

- 收到新的海外询盘（网站表单、Alibaba、展会名片、LinkedIn 私信）
- 客户问"how much" / "send me quotation" / "price list"
- 客户读完报价后失联，需要重新激活
- 每周/每月盘一遍在手询盘，排跟进优先级

---

## SM 硬约束

- **报价熔断**：客户直索价格时禁止给最终价，先反问三项契约数据（PCB 尺寸与最小元件、目标 CPH、现有线体兼容性）
- **术语保留**：Pick-and-place、Reflow、Wave Soldering、CPH、Gerber、BGA、Pitch、Feeder、Nozzle 等保留英文
- **整线连带**：涉及 S-70LD 必配 STF1003；涉及 S-WS450 必配 SUL460
- **强制 CTA**：方案/报价类输出结尾必带 Jason Wu 复核声明 + Gerber 提交要求（见 `smthelp-brand-voice`）

---

## 工作流

### Step 1：询盘分层

先判定客户在哪个阶段，不同阶段的动作完全不同：

| 层 | 特征 | 本次目标 |
|---|---|---|
| **L0 探价** | 只问价格、无工况、邮箱是免费邮箱、公司名模糊 | 拿到三项契约数据，拿不到就降级处理 |
| **L1 有需求未定型** | 说了产品方向（如 wave soldering），没给工况 | 补齐工艺参数，锁定机型 |
| **L2 技术方案中** | 给了 PCB / 产能 / 兼容性信息 | 出配置清单 + 预算区间，推视频验厂 |
| **L3 商务谈判** | 在比价、谈付款与交期 | 价值锚定（源头 + 售后 + ROI），不降价换单 |
| **L4 失联** | 报价后无回应 ≥ 14 天 | 用新信息重启，不问"考虑得怎么样" |

**判不出来的，按低一层处理。** 宁可多问一次，不要在 L0 就发报价单。

### Step 2：缺口数据盘点

对照下表，列出还缺什么：

**必填（没有就不能报价）**
- PCB 尺寸范围、是否双面贴装、最小元件（0201 / 0.4mm pitch BGA）
- 目标产能（CPH 或月产量）
- 现有线体品牌（Yamaha / JUKI / Panasonic）与 Feeder 型号

**加分（有则方案更准）**
- 产品类型（汽车电子 / 医疗 / 消费 / 工控）
- 当前是人工线还是半自动，瓶颈在哪一段
- 目标市场与认证要求（CE / UL）
- 采购时间窗与预算区间
- 谁是决策人（采购 / 工艺 / 老板）

### Step 3：判断询盘真伪

红旗信号（出现 2 条以上，按 L0 处理）：

- 用免费邮箱（Gmail / Outlook）却自称大型工厂
- 只问价格，对工况一问三不知，或回答前后矛盾
- 同时索要全线所有型号报价
- 要"最详细的技术图纸 + BOM"但拒绝提供自己产线信息
- 域名刚注册、LinkedIn 无员工、地址是虚拟办公室

**不要直接质疑客户。** 用反问自然筛：真买家答得上来，探价的会消失。

### Step 4：生成跟进动作

每条询盘输出且仅输出一个**下一步动作**，附话术骨架：

- 缺数据 → 发反问邮件（按 Step 5 模板）
- 数据齐 → 出配置清单 + 预算区间 + 强制 CTA
- 已报价 → 给新信息跟进（新案例 / 交期窗口 / 视频验厂邀请）
- 失联 → 重启序列（第 1 次给新信息，第 2 次给行业信息，第 3 次礼貌结案）

### Step 5：反问话术（熔断期用）

不要罗列问题清单，要解释**为什么需要**，否则客户觉得在被审问：

```
Thanks for your interest in [机型]. To size the line correctly, I need three
things — each one changes the configuration:

1. PCB size range and smallest component (e.g. 0201, 0.4 mm pitch BGA)
   → this decides the nozzle set and vision system.
2. Target throughput (CPH or monthly output)
   → this decides whether one [机型] is enough or you need two in sequence.
3. Your existing line (Yamaha / JUKI / Panasonic) and feeder models
   → this decides the interface and whether we reuse your feeders.

If you'd rather not go back and forth, send the Gerber file and I'll run a
capacity simulation and come back with a full configuration.
```

客户嫌麻烦时的降级话术（不要省略，直接用）：

*"Understood — we can skip the details. Based on a standard configuration, the budgetary range is USD [区间]. Final pricing depends on the process options; I'll confirm once we see your PCB."*

---

## 输出格式

```text
【询盘跟进单】

客户：[公司] / [国家] / [联系人与职位]
来源：[网站表单 / Alibaba / 展会 / LinkedIn]
当前分层：L[0-4] —— [一句判定依据]

已有数据：
  - PCB / 最小元件：[有/无] …
  - 目标产能：[有/无] …
  - 线体兼容性：[有/无] …
  - 时间窗与预算：[有/无] …

缺口：[列出本次必须拿到的 1–3 项]
真伪信号：[红旗 N 条，或无]

本次动作：[一个动作]
话术：[可直接发送的邮件正文]

下次时间点：[X 天后] / 触发条件：[客户回复 / 无回复]

风险与待确认：
  - [交期/认证/付款方式等未决事项]
```

盘一批询盘时，先输出优先级表（`客户 | 分层 | 缺口 | 动作 | 时间点`），再逐个展开。

---

## Gotchas

1. **不要在 L0 阶段发报价单**
   解释：给了价格就等于把谈判筹码交出去，且配置必然不准，后续改价极难解释。L0 的目标永远是拿数据。

2. **不要用 "Just following up" 开头**
   解释：无信息量，海外采购每天收到几十封，会直接归档。每次跟进必须带一个新信息：新案例、交期窗口、参数补充、行业变化。

3. **不要为了显得专业而承诺具体交期或认证**
   解释：交期取决于配置与排产，认证取决于目标市场。写"配置确认后提供确切 lead time"，不要估数字。

4. **不要把竞品探价当成失败线索直接丢掉**
   解释：探价方也可能是分销商或未来渠道。保持专业回复，但只给公开参数与预算区间，不给配置逻辑与成本结构。

5. **不要在邮件里贴完整价目表**
   解释：价目表会被直接用于压同行，且不同市场应有差异。只给当前需求对应的配置与区间。

6. **不要跳过强制 CTA**
   解释：Jason Wu 复核声明与 Gerber 提交要求是公司的合规动作，同时是把对话从"比价"拉回"工艺"的唯一抓手。
