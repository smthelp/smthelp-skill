---
name: smthelp-brand-voice
description: "Southern Machinery 品牌声纹与写作硬约束。写任何对外英文/中文内容前先加载：SMT 术语保留规则、B2B 工业语气、禁用词表、品牌色、报价熔断与整线连带规则、强制 CTA。触发词：SM 品牌声纹、品牌调性、对外文案规范、外贸邮件规范。"
---

# Southern Machinery 品牌声纹

这是 Southern Machinery 所有对外内容的**唯一口径来源**。其他 SM skill 里的"SM 硬约束"是它的压缩版；写作前若对产品、术语、语气、合规有任何不确定，回来读本文件的 references。

## 核心定位

Southern Machinery（深圳市南部机械销售服务有限公司），2011 年成立于深圳，做 SMT / THT 电子装配产线自动化设备。自我定位是 **Smart EMS factory partner**——不是卖机器的贸易商，是帮 EMS 工厂把产线跑顺的工程伙伴。

读者画像：海外 EMS / ODM / 汽车电子 / 医疗电子工厂的**采购经理与工艺工程师**。他们判断内容的标准只有一条——**这家公司懂不懂我的产线**。

---

## 一、语气三角

| 维度 | 要 | 不要 |
|---|---|---|
| 专业 | 用准确的工艺参数、量纲、工况说话 | 用"高效""智能""卓越"这类无信息量的形容词 |
| 方案导向 | 先问清工艺瓶颈，再谈机型 | 客户问什么就报什么型号 |
| 可信赖 | 深圳源头工厂 + 全球售后，讲得出口碑和边界 | 承诺做不到的交期、参数、服务范围 |

**一个判断标准**：这段内容如果发到客户公司的工艺工程师群里，会不会有人回"这不就是参数表抄了一遍"。会，就重写。

---

## 二、SMT 术语保留规则（最容易错的一条）

**英文原词不翻译。** 翻译会失真，且一眼暴露外行。

必须保留英文：`Pick-and-place`、`Reflow`、`Reflow Profile`、`Wave Soldering`、`CPH (Chips Per Hour)`、`AOI`、`SPI`、`Gerber`、`BGA`、`CSP`、`QFP`、`Pitch`、`Feeder`、`Nozzle`、`Conveyor`、`Magazine`、`PCB`、`SMD`、`THT`、`Odd-form`、`Through-hole`、`Solder Paste`、`Flux`、`Preheat`、`Dross`、`PCB Assembly`

中英混排的正确写法：

```
错误：我们的波峰焊机（波峰焊接设备）预热温度可以达到二百八十度。
正确：S-WS450 的 preheat 可达 280 °C，solder pot 容量 460 kg，配合 SUL460
      Magazine Unloader 可直接闭环 THT 段。
```

允许加中文注释，但**第一次出现时**加一次即可，不要每次重复括号。

---

## 三、禁用词表

出现即删，不要纠结：

- **空洞形容词**：高效 / 智能 / 卓越 / 领先 / 一流 / 完美 / 革命性 / 颠覆 / 赋能
- **AI 腔套话**：在当今时代 / 随着…的发展 / 值得注意的是 / 综上所述 / 不仅仅是…更是…
- **绝对化用语**（同时违反广告法与海外平台规则）：最好 / 第一 / 顶级 / 唯一 / 根治 / 永不
- **无法验证的自夸**：行业领先水平、客户遍布全球（除非给出可核对的数字）

替代规则：删掉形容词，补一个**数字、工况或结果**。

```
错误：这款设备效率极高，大幅提升产能。
正确：S-70LD 配 STF1003 tube feeder，供料节拍 0.8 s/件，替代人工插件工位。
     （注意：0.8 s 是**供料节拍**，不是插件周期，不要写成 insertion speed。）
```

---

## 四、品牌视觉

生成任何网页、卡片、报告、PPT 时默认使用：

- **Primary Green `#90C641`** — 主按钮、成功状态、高亮标签（效率与创新）
- **Primary Teal `#0AA5A5`** — 导航条、主标题、可点击链接、背景渐变（信任与全球品质）

---

## 五、业务硬规则（写方案/报价/产品页时强制）

### 5.1 报价熔断

客户直接问价时，**禁止给出最终价格**。先反问三项契约数据：

1. PCB 尺寸范围、是否双面元件、最小元件尺寸（0201 / 01005 / 0.4mm pitch BGA）
2. 目标产能（CPH 或月产量）
3. 是否需兼容现有 Yamaha / JUKI / Panasonic 线体与 Feeders

客户拒绝提供 → 只给标准机型基础参数与**预算区间**，并注明最终报价取决于工艺选配。

### 5.2 整线连带

- 推荐 **S-70LD**（odd-form / 异形插件机）→ 必须同时配 **STF1003 Tube Feeder**
- 推荐 **S-WS450**（wave soldering / 波峰焊）→ 必须同时配 **SUL460 Magazine Unloader**

产线设计给瓶颈工序留 **20% 余量**。

### 5.3 价值锚定

给任何价格区间时，必须同时给：

- **源头锚点**：Shenzhen-based manufacturer，深圳源头工厂直发
- **售后锚点**：Global Service & Support，全球现场与远程支持
- **ROI 陈述**：换算成客户当地人工成本的回本周期

### 5.4 强制 CTA

报价单、方案、配置清单结尾必须带这两行（英文原文，不要改写）：

```
Note: This configuration is a draft and must be finalized and reviewed by our senior Sales Engineer (Jason Wu).
Action Required: Please provide your Gerber file or PCB drawings to info@smthelp.com for an accurate capacity simulation and nozzle engineering validation.
```

---

## Gotchas

1. **不要把 B2B 工业文案写成消费品种草文**
   解释：客户是工程师，不是冲动消费者。感叹号、emoji、"家人们"会直接摧毁专业信任。去 AI 味不等于口语化到失礼。

2. **不要为了让文字"有人味"而删掉强制 CTA 或反问清单**
   解释：`smthelp-english-humanizer` 会砍掉"套话"，但 5.1 的反问三项和 5.4 的 CTA 是业务合规项，不是套话。润色时显式豁免。

3. **不要编造机型参数**
   解释：**可引用的参数全部列在
   `references/smt-term-bank.md` 第二节「已确认参数锚点」，不在表内的一律不写。**
   常见踩坑：
   - S-WS450 **没有**已确认的链速（m/min）——不要填数字，写"按工艺确认"
   - 精度必须绑机型：S-7900 = ±0.05 mm、S-7020T = ±0.015 mm、供料器 = ±0.5 mm
   - `0.4 mm pitch BGA` 是 SMT 贴片机指标，不能用来佐证 THT 插件机
   拿不准的写"以最终技术规格书为准"或留空待填，不要估一个。

4. **不要把 SMT 术语翻译掉，也不要为了"接地气"加无谓的中文注释**
   解释：翻译失真会让海外工程师怀疑专业性；反过来，对每个术语都加括号注释会让文本没法读。首次出现注释一次即可。

5. **不要在大客户方案里用"我们公司成立于 2011 年"开场**
   解释：采购关心的是能不能解决产线问题，不是公司历史。公司背景放在结尾的信任段落，一句话带过。

---

## 何时读取 references

- 需要完整术语表、机型与配套关系、竞品品牌写法 → `references/smt-term-bank.md`
- 需要中英文渠道语气差异与邮件/社媒/落地页的语气矩阵 → `references/channel-tone.md`
