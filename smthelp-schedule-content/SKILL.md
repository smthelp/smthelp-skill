---
name: smthelp-schedule-content
description: "Southern Machinery SMT 营销内容永动机调度器：协调调度四个营销内容 skills 的主控 skill。当用户需要系统化地做 SMT 设备外贸营销内容、想建立内容生产飞轮、不知道当前该拆解还是该写作、或想按'拆解→想清楚→写一次→用到极致'的流程产出产品营销内容时使用此 skill。负责评估用户所处阶段并调用 smthelp-content-judge / smthelp-content-clarify / smthelp-content-architect / smthelp-content-build。"
---

# Southern Machinery SMT 营销内容永动机调度器 (smthelp-schedule-content)

## 系统概述

这不是一篇"讲道理"的文章，而是一份可以直接上手练习的技能手册。

如果一套方法只能看懂，那它是知识；如果一套方法可以照着做，那它才是技能。

本系统把「AI 内容永动机」方法论改编为 Southern Machinery SMT 设备外贸营销专用版，拆解为 4 个可复用 Skills：

1. **smthelp-content-judge** —— 竞品/同行营销内容拆解
2. **smthelp-content-clarify** —— 营销内容写作前澄清
3. **smthelp-content-architect** —— 产品母内容构建
4. **smthelp-content-build** —— 营销内容裂变

## 核心理念

AI 不会自动帮你做好外贸营销，除非你已经在用"系统"的方式做内容。

当你真正掌握这 4 个 Skills，你做的就不再是零散文案，而是——"一套可以不断产出 SMT 产品营销内容的能力。"

## 四个 Skill 概览

### Skill 1｜smthelp-content-judge
- **作用**：把模糊的"感觉"，训练成稳定可复用的判断力
- **目标**：判断同行营销内容是否值得借鉴
- **触发场景**：刷到竞品产品页/帖子/EDM，想知道为什么有效

### Skill 2｜smthelp-content-clarify
- **作用**：解决「知道要写产品内容，但写不出来/写偏了」
- **目标**：写作前澄清卖给谁、凭什么信、看完做什么
- **触发场景**：产品页/文章/邮件不知道从哪写，或逻辑混乱

### Skill 3｜smthelp-content-architect
- **作用**：一个好卖点，只消耗一次脑力
- **目标**：把已验证卖点升级为可长期复用的产品母内容
- **触发场景**：某产品询盘转化不错、新机型上线、卖点被反复问起

### Skill 4｜smthelp-content-build
- **作用**：不是多写，而是「把写过的用到极致」
- **目标**：一份母内容 → 多平台多次分发
- **触发场景**：已有产品长文/视频/EDM，要裂变到 LinkedIn、SEO、YouTube、WhatsApp

## 正确使用顺序（必须牢记）

⚠️ **顺序一旦错，系统就会失效**

唯一正确顺序是："拆解 → 想清楚 → 写一次 → 用到极致"

### 调度流程

当用户提出营销内容相关请求时：

1. **评估阶段**：判断用户当前处于内容生产流程的哪个阶段
2. **调度决策**：根据阶段调用相应的 skill
3. **执行引导**：按正确顺序引导用户完成流程；事实类表述以 `smthelp-knowledge-base` 或用户提供的已验证资料为准

### 阶段判断标准

**阶段 1 - 拆解阶段**
- 用户提到：分析竞品/同行内容、某篇为什么有效、学习对手打法
- 调用：`smthelp-content-judge`

**阶段 2 - 澄清阶段**
- 用户提到：不知道写什么、逻辑混乱、写作卡壳、新品要出内容
- 调用：`smthelp-content-clarify`

**阶段 3 - 构建阶段**
- 用户提到：已验证卖点、主推产品、要写母内容/核心文案
- 调用：`smthelp-content-architect`

**阶段 4 - 裂变阶段**
- 用户提到：已完成内容、要复用、多平台分发、展会物料
- 调用：`smthelp-content-build`

## 业务场景路由示例

| 用户需求 | 实际阶段 | 调用 |
|----------|----------|------|
| "帮我拆一下竞品这台贴片机的页面" | 拆解 | smthelp-content-judge |
| "新机型 SME-XXX 上线，要写产品介绍" | 澄清 → 构建 | clarify → architect |
| "展会后要跟进的物料" | 裂变 | smthelp-content-build |
| "这篇文章改成 LinkedIn 帖子和邮件" | 裂变 | smthelp-content-build |
| "想系统建立内容生产流程" | 全流程 | 按 1→2→3→4 引导 |

## 成熟标志

✅ 你不再依赖灵感，而是拥有一套可重复的 SMT 营销内容生产系统。

✅ 你清楚地知道每个创作阶段该用什么工具，不再混乱和低效。

✅ 你建立的不再是内容库，而是"一套可以不断产出内容的能力。"

## 使用建议

- 你不需要一次全用，哪怕只练一个，都会立刻改善你的创作状态
- 每个 Skill 都是独立能力模块
- 始终按正确顺序训练：拆解 → 想清楚 → 写一次 → 用到极致
- 始终遵守事实合规：任何平台上的任何说法，都要经得起"来源在哪"的追问
