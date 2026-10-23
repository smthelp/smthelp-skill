# 文案标准（copy-standards）：FAB + 六步博客 + GEO

## 1. 总则

- 英文母版，句子短，技术词首次出现顺手解释（"feed-hole pitch (the distance between sprocket holes)"）
- 每段先给数字再给形容词；不写 "best / No.1 / world-class" 这类不可核对的话
- 不写价格；CTA 只有三类：发图/型号要报价、WhatsApp、邮件
- 冲突数字不在正文里"选一个"，正文写范围或"see disclosure"，细节进 disclosure 表
- 来源只有一份、无法核实的参数 → `To be confirmed`
- 领域知识参考 `smthelp/smthelp-skill/learn-SMT-in-3-hours`（工艺流程、故障与维护、视觉语言），保证术语和工艺描述专业

## 2. FAB（Feature → Advantage → Benefit）

6 组，每组三行（key：`fab{N}n/f/a/b`）：

- **Feature**：真实参数或结构（"Die-cut on both faces with locating dots"）
- **Advantage**：技术上意味着什么（"The splice seats at the original pitch, so the sprocket drives straight through"）
- **Benefit**：对客户的结果（省人、防错、提效、过审）（"No re-threading, no mis-pick at the joint"）

配套：痛点 6 卡（`w{N}t/d`）先共鸣，再进 FAB；summary/metrics 放最硬的 4-6 个数字。

## 3. 八篇博客：Dan Koe 六步内容法

每篇内部按六步写，**但任何标题（文章标题、小标题、页面任何 h1-h4/summary）都不得出现这六步的名字**：

| 步 | 内部作用 | 小标题写法示例（可用） |
|---|---|---|
| Hook | 前三秒让人停下 | "Look at what actually stopped the line" |
| Diagnosis | 说出真正的痛 | "The stop that hides in plain sight" |
| Framework | 可复用的方法 | "Move the work off the machine" |
| Vehicle | 把方法装进产品 | "A splice built for the sprocket" |
| Loop | 让老客户反复回来 | "Why this gets cheaper every month" |
| CTA | 明确下一步 | "Your next step" |

### 禁用词（标题中，全部语言；build.py `BANNED` 与 verify.py 同源）

- en：hook, diagnosis/diagnose, framework, vehicle, loop, CTA, call to action, Dan Koe（1.1.0 起；方法论作者名不出现在页面任何标题，正文也不写）
- es：gancho, diagnóstico, marco de trabajo, vehículo, bucle, llamada a la acción
- pt：gancho, diagnóstico, estrutura de trabalho, veículo, loop, chamada para/à ação
- fr：accroche, hameçon, diagnostic, framework, véhicule, boucle, appel à l'action
- ar：خطاف، تشخيص، إطار عمل، مركبة، حلقة، دعوة إلى/لاتخاذ إجراء
- ru：крючок, хук, диагноз, диагностика, фреймворк, носитель, петля, призыв к действию
- zh：钩子、诊断、框架、载体、循环、行动号召

### 八篇选题（按买家旅程排，避免重复）

1. 停线的真正原因（认知）
2. 隐性成本怎么算（量化）
3. 选型：参数怎么对应你的机器
4. 操作方法/步骤（how-to）
5. 常见错误与排查
6. 材料/版本对比（如美纹纸 vs 牛皮纸）
7. 采购与库存节奏（Loop）
8. 从样品到批量：询盘清单

每篇 350-600 词，4-6 个小标题；正文英文，其他语言可提供译文（`blogs.json` 中加 `"es": [...]`），没有译文时页面显示英文并提示 `blog_note`。

## 4. GEO（生成式引擎优化）

让 AI 搜索/答案引擎能直接引用：

- **summary 框**：一段 50-80 词、可独立引用的产品总结（`.sump`，被 speakable 选中）+ 6 条实体事实 `dl`（品类、制造商、规格、适配、包装、交期）
- **Q&A**：10 条 FAQ，问题用买家原话，答案第一句直接给结论 + 数字（FAQPage 同源）
- **实体事实**：公司全称、成立年份（2011）、城市（Shenzhen）、型号代码、单位统一（mm、pcs/roll）
- **可引用句**：每个 section 的 lead 一句话能脱离上下文成立
- **DefinedTermSet**：4-6 个术语定义（如 "Feed-hole pitch"、"3-hole / 5-hole splice"）
- **HowTo**：操作步骤与 how 区同源
- 不发明数据：视频 uploadDate、销量、认证号拿不到就不写
