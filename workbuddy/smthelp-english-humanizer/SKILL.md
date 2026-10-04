---
name: smthelp-english-humanizer
description: "外贸英文内容去 AI 味。润色开发信、LinkedIn 帖子、产品页、方案、报价说明时使用。基于 Wikipedia AI 写作特征库，但按 B2B 工业设备场景调整：保留 SMT 英文术语、按文体控制人格化程度、豁免强制 CTA 与资格审查反问。"
---

# 英文去 AI 味（B2B 工业版）

## 核心定位

原版 humanizer 的目标是把 AI 文本改得像真人写的博客。但 Southern Machinery 的对外英文是**B2B 工业技术沟通**，直接套用会出事：它会把报价单里的合规声明当成"套话"删掉，会把 Gerber、0.4 mm pitch BGA 这类术语当成"AI 词汇"改写，还会在正式方案里塞进 "I genuinely don't know how to feel about this" 这种句子。

所以本版加了一层**文体档位**控制：先判断这段英文属于哪一档，再决定人格化到什么程度。

---

## 触发场景

- "这段英文读起来太像 AI 了，改一下"
- "帮我润色这封开发信 / 这个产品页 / 这份方案"
- "检查有没有 AI 写作痕迹"
- 发出去之前对任何英文对外内容做最后一道检查

---

## Step 1：先定文体档位（这一步错了后面全错）

| 档位 | 典型文体 | 人格化上限 | 能否用第一人称 "I" | 能否表达个人情绪 |
|---|---|---|---|---|
| **A 正式** | 报价单、技术方案、配置清单、合同条款、验收标准 | 零。只做减法，不加风格 | 不建议，用 we / the configuration | 禁止 |
| **B 商务** | 开发信、询盘回复、跟进邮件、展会邀约 | 低。可以有温度，不能有个性 | 可以，"I checked your line…" | 禁止（可说期待，不说感受） |
| **C 观点** | LinkedIn 帖子、博客文章、行业评论 | 中。允许立场与判断 | 应该，观点需要有人承担 | 允许，但要专业范围内 |
| **D 口语** | 视频口播稿、社媒短文案、展会话术 | 高。按说话写 | 必须 | 允许 |

**判断原则**：客户会不会拿这份文件去做内部决策或采购审批？会 → A 档。

**A 档的正确目标不是"像人写的"，是"像工程师写的"**：短句、主动语态、参数精确、无修饰。

---

## Step 2：SM 内容豁免清单（先划出来，不许改）

润色前，先把以下内容从待改区里摘出来：

1. **SMT 英文术语** — Pick-and-place、Reflow、Wave Soldering、CPH、Gerber、BGA、Pitch、Feeder、Nozzle、Conveyor、Odd-form 等。它们看起来生硬，但改了就不专业。
2. **数字与量纲** — `0.8 s/件`、`±0.05 mm`、`4,000 CPH`、`280 °C`、`460 kg`、`50 × 50 mm`
   等。绝对不能模糊化成 `fast` / `high precision` / `large capacity`。
   **但前提是数字本身可溯源**：出处见
   `smthelp-brand-voice/references/smt-term-bank.md` 第二节。
   来源不明的数字不是"豁免项"，是"待删项"。
3. **强制 CTA 两行** — Jason Wu 复核声明与 Gerber 提交要求，原文保留，一个词都不要动。
4. **资格审查三项反问** — PCB 尺寸/最小元件、目标 CPH、线体兼容性。这是业务动作，不是套话。
5. **机型与配套关系** — S-70LD + STF1003、S-WS450 + SUL460。

---

## Step 3：扫描 AI 特征

按 `references/ai-patterns.md` 的 24 类特征逐项扫描。这个文件是主特征库，包含每类的识别词、问题说明和 Before/After 示例。

最高频的六类（外贸英文里最常见）：

1. **虚假深度的 -ing 尾巴** — "…，ensuring seamless integration and maximizing throughput."
2. **AI 高频词** — moreover、additionally、crucial、pivotal、landscape、showcase、testament、underscore、delve、robust、seamless、leverage
3. **破折号滥用** — 一段里出现两次以上
4. **三段式堆砌** — "efficiency, reliability, and cost-effectiveness"
5. **空洞归因** — "Industry experts believe"、"Studies show"（没有具体出处）
6. **无谓升华** — "This represents a major step toward the future of smart manufacturing."

**规则 4 的工业例外**：技术参数天然成组（PCB size、component range、throughput），这类并列不算"三段式堆砌"，不要改。只有**形容词**成三才算。

---

## Step 4：改写

通用原则：

- 删掉 AI 词后**不要留空**，补一个具体信息（数字、工况、结果、时间）
- 把 `-ing` 尾巴改成独立短句
- 破折号换成句号或逗号
- 空洞归因换成具体出处，或直接断言（我们有把握的事不需要假装引用）
- 无谓升华删掉，换成下一步动作

```
AI 腔：
Our wave soldering machine is a testament to our commitment to innovation,
delivering unparalleled performance and ensuring seamless integration into
your existing production line — maximizing throughput and minimizing downtime.

A 档改法（方案/报价）：
The S-WS450 handles boards up to 450 mm wide, with preheat to 280 °C and a
460 kg solder pot. It is lead-free compatible with a dual-wave system. It pairs
with the SUL460 Magazine Unloader (≈30 s magazine change) to close the THT loop.
Conveyor speed is confirmed per process.

C 档改法（LinkedIn）：
Most wave soldering bottlenecks aren't in the solder pot. They're at the
exit — boards stacking up because there's no unloader downstream.
```

同一个意思，A 档和 C 档的写法完全不同。**先定档，再改写。**

---

## Step 5：朗读与合规检查

- 逐句读一遍，卡住的地方重写
- A / B 档：确认无 emoji、无感叹号、无"I feel"、无幽默
- 确认 Step 2 的五项豁免内容完好无损
- 确认所有数字与原文一致

---

## 输出格式

```
【文体档位】A/B/C/D —— [一句判定依据]

【豁免保留】
- 术语：…（N 处，未改动）
- 数字：…（N 处，未改动）
- 强制 CTA / 资格审查反问：完好

【AI 特征诊断】
- [特征类] × [N 处]：[典型改法示例]
- [特征类] × [N 处]：[典型改法示例]

【修改稿】
[全文]

【改动说明】
主要改动方向：[一句话]
未改动的原因：[说明哪些看似 AI 腔但属于业务必需，故保留]
```

---

## Gotchas

1. **不要把 A 档文档润色成 C 档**
   解释：原版 humanizer 鼓励"加入第一人称、表达不确定、让一些混乱进来"。这在博客里有效，在报价单里是灾难——采购拿着有"我个人觉得"的方案去做审批，信任直接崩掉。

2. **不要把 SMT 术语当 AI 词汇改掉**
   解释：`leverage` 该删，`Feeder` 不能删。判断标准：删掉后是否影响技术准确性。影响的一律保留。

3. **不要删掉强制 CTA 和资格审查反问**
   解释：它们读起来确实像模板，但那是合规与业务动作。要改的是它们**周围**的文字，不是它们本身。

4. **不要把"参数并列"误判为"三段式堆砌"**
   解释：`50 × 50 mm, 0201 components, 0.4 mm pitch BGA` 是技术规格，不是修辞。只有形容词成组（efficient, reliable, cost-effective）才需要拆。

5. **不要为了让文字自然而模糊数字**
   解释：`0.8 s/件` 改成 `fast insertion speed` 会让工程师怀疑我们没有真实数据。宁可生硬，不可含糊。

6. **不要把精度数字在机型之间串用**
   解释：S-7900 = ±0.05 mm，S-7020T = ±0.015 mm，STF1003 供料器 = ±0.5 mm。
   三者差 10–30 倍。写到 S-70LD 文案里的精度只能用供料器的 ±0.5 mm，
   写成 ±0.05 mm 等于对客户做出设备做不到的承诺。

6. **不要给 B 档邮件加幽默**
   解释：跨文化商务邮件里，幽默的误解成本极高。温度靠具体（提到对方产线的细节）建立，不靠玩笑。

---

## 何时读取 references

- 需要 24 类 AI 特征的完整识别词表与 Before/After 示例 → `references/ai-patterns.md`
- 需要确认术语、机型、品牌色、强制 CTA 的准确写法 → 调 `smthelp-brand-voice`
