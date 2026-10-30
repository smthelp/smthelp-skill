---
name: foreign-trade-geo-audit
description: "外贸独立站 GEO（生成式引擎优化）评估与整改 skill — 按 E-E-A-T × 生成式引擎 RAG 逻辑的六维评分卡，对任意外贸官网做技术抓取、站外信源检索、问题定级与 30 天整改路线图，输出单文件 HTML 报告 + data.json。"
whenToUse: "用户要求「做 GEO 评估」「GEO 审计报告」「AI 搜索优化诊断」「生成式引擎优化」「网站 AI 友好度检测」「为什么 AI 不提我们品牌」；评估对象为外贸/B2B 独立站；不要用于：纯传统 SEO 关键词排名优化、竞价投放优化"
category: 分析报告
version: 1.0.0
author: user-generated
metadata:
  source: hermes
  origin: "sales-engineering/foreign-trade-geo-audit"
  upgradeable: true
  rubric_version: "1.0.1"
---

# 外贸独立站 GEO 评估 Skill

## 这是什么

把「官网在 AI 问答（豆包 / DeepSeek / 元宝 / 文心 / Kimi / ChatGPT）里会不会被提到、会不会被引用」这件模糊的事，变成一套**可抓取、可打分、可复现、可比对**的六维评估流程。

**与 SEO 的根本区别**：SEO 抢的是搜索结果页的十条链接；GEO 抢的是 AI 答案里的那一句话。SEO 看关键词排名，GEO 看**实体是否被 AI 正确识别 + 是否有 ≥3 个独立信源交叉印证**。

## Southern Machinery 覆盖规则（优先级最高）

- 事实优先引用被评估站点自身内容与官方资料；无来源的年份、规模、认证、客户数、ROI 必须标记 `待确认 / to be confirmed`。
- 评估结论可以尖锐，但**每一条扣分必须给出可复现的抓取证据**（URL、HTTP 状态码、HTML 片段、检索结果），不得凭印象打分。
- 报告页脚固定 Southern Machinery CTA：LinkedIn 公司页 / LinkedIn Profile / Twitter / Facebook / YouTube Channel + `file.autoinsertion.com` 与 `ph.smthelp.com` 那句原文。
- 交付物固定两份：`data.json`（结构化数据源）+ `output.html`（单文件、CSS/JS 全内联、无外链）。
- 不读取 Cookie / 凭据 / 授权码；不执行未经确认的外发、发布或写库操作。

---

## 快速开始

```bash
cd skills/foreign-trade-geo-audit

# Phase 2 — 技术抓取（客观事实，全自动）
python3 scripts/geo_scan.py --url https://www.smthelp.com --profile smt --out /tmp/scan.json

# Phase 3 — 评分（自动基线 + 硬上限规则，输出待 Agent 判断项）
python3 scripts/geo_score.py --scan /tmp/scan.json --profile smt --out /tmp/score.json

# Phase 5 — 生成报告
python3 scripts/geo_report.py --data data.json --out output.html
```

**Agent 负责**：Phase 1（确认范围）、Phase 4（站外信源检索，需联网判断）、以及 Phase 3 中脚本标记为 `needs_agent` 的评分项定分。脚本负责所有可自动化的部分。

---

## Phase 1 · 需求理解（Agent）

向用户确认最少 4 项，一次问清，不要挤牙膏：

| 项 | 说明 | 默认值 |
|---|---|---|
| `url` | 被评估站点（含协议） | 必填 |
| `entity` | 品牌 / 公司法定名 / 创始人（实体消歧用） | 从站点 title 提取 |
| `profile` | 行业画像：`smt` / `industrial` / `consumer` / `saas` | `industrial` |
| `markets` | 目标出口市场（决定场景词与语种） | 从站点 hreflang 推断 |

**先读配置再动手**：`config/industry-profiles.json` 决定场景词模板与权重微调，不要跳过。

## Phase 2 · 技术抓取（脚本，全自动）

`geo_scan.py` 抓取并输出客观事实，**不做任何主观判断**。覆盖：

- 传输层：HTTPS、HTTP/2、Server、CDN 节点、viewport
- 抓取层：robots.txt、sitemap（自动发现 + URL 数 + lastmod 分布 + soft-404 检测）
- 结构层：JSON-LD 块数与类型、OG、canonical、hreflang（**含协议缺失检测**）、H1/H2/H3 层级
- 内容层：正文词数、数字密度（可量化参数）、FAQ 痕迹、meta 覆盖率、图片 alt 缺失率
- 实体层：NAP 抽取（地址 / 电话 / 邮箱）、同族镜像域名探测、公司名变体

```bash
python3 scripts/geo_scan.py --url https://www.smthelp.com \
  --pages /,/about-us,/faq,/contact-us,/news.html \
  --probe-mirrors --profile smt --out /tmp/scan.json
```

> ⚠️ 脚本输出的是**事实**，不是结论。例如它报告 `jsonld_total: 0`，由 Agent 在 Phase 3 结合 rubric 判定这扣多少分。

## Phase 3 · 六维评分（脚本给基线，Agent 定终分）

读 `config/scoring-rubric.json`。六个维度：

| ID | 维度 | 核心问题 | 是否可自动 |
|---|---|---|---|
| A | 技术地基 | AI 的抓取器能不能顺畅拿到内容？ | 全自动 |
| B | 结构化数据 | AI 能不能**机器确认**你是谁、卖什么？ | 全自动 |
| C | 内容 AI 友好度 | 内容是不是 AI 愿意引用的形态？ | 半自动 |
| D | 站外信源生态 | 除了你自己，还有谁替你说话？ | `needs_agent` |
| E | 实体一致性 | AI 会不会把你认错成别家？ | 半自动 |
| F | AI 平台认知 | 五平台实测盲测 | `needs_agent`（待盲测） |

**脚本产出基线分 + 命中的硬上限规则**，`needs_agent` 项输出「待判断清单 + 建议区间」。Agent 在 ±10 分范围内调整并**写明理由**。

### 硬上限规则（cap rules，来自方法论，不可绕过）

这些是 GEO 的结构性约束，命中即封顶，不因其他项高分而抵消：

1. `independent_source_count < 3` → **D ≤ 35**
   （依据：2026 年可信度分层要求 ≥3 个独立信源交叉验证，单信源占比 ≤8%）
2. `nap_conflicts > 1` 或 `mirror_domains > 1` → **E ≤ 40**
   （依据：实体消歧失败时，AI 无证据判断哪个是权威主站）
3. `jsonld_total == 0` → **B ≤ 25**
   （依据：无机器可读实体档案，AI 只能靠正文猜测）
4. `content_freshness > 730 天` → **C ≤ 45**
   （依据：生成引擎对时间衰减的敏感度远高于传统搜索）

## Phase 4 · 站外信源检索（Agent，需联网）

**这一步不能省，也不能用官网内容替代。** 按 `references/source-playbook.md` 执行，至少跑三类词：

- **品牌词**：`"{品牌}"` / `"{公司法定名}"` — 看实体是否被归对、有无同名干扰
- **场景词**：`config/industry-profiles.json` 里该行业的 `scenario_queries` — 看谁在占位
- **人物词**：`"{创始人} {行业}"` — 看个人实体能否反哺公司实体

**核心动作：记录「AI / 搜索引用了哪些网址」—— 引用来源清单就是信源缺口地图。AI 引了谁，就去哪里布局。**

## Phase 5 · 输出（脚本 + Agent 文案）

`geo_report.py` 读 `data.json` 渲染 `templates/report.html`，产出单文件报告。必备模块：

1. 综合分 + 一句话诊断（金句形态，如「展厅很满，但每件展品都没有价签」）
2. 六维评分卡（环形图 + 进度条 + 正负证据双列）
3. 亮点清单（已存在但未被声明的资产）
4. 问题清单（P0 致命 / P1 重要 / P2 改进，每条带 🛠 修复动作）
5. 机会点（别家抢不走的牌）
6. 30 天四周行动清单（每周带 📦 产出物）
7. 盲测题表（T1–T6，品牌词 / 场景词 / 参数词 / 人物词）
8. 可直接粘贴的 JSON-LD 代码（带复制按钮）

写完必须跑冒烟测试（见「交付前自检」）。

## Phase 6 · 升级回流（每次评估后必做）

本 skill 设计为**可演进**的。每次评估结束，按 `references/issue-library.md` 顶部协议执行：

1. 本次发现的新问题类型 → 追加进 `references/issue-library.md`
2. 本次用到的新检测项 → 追加进 `config/scoring-rubric.json` 的 `checks`（并 bump `rubric_version`）
3. 新行业的场景词 → 追加进 `config/industry-profiles.json`
4. 在 `CHANGELOG.md` 记一行，说明改了什么、为什么

**原则：改配置不改 SKILL.md 逻辑。只有流程本身变化时才 bump SKILL.md 的 `version`。**

---

## 交付前自检（逐条确认，不可跳过）

```bash
# 1. 结构与语法
python3 -c "import re;h=open('output.html',encoding='utf-8').read();\
print('div',h.count('<div'),h.count('</div>'),'script',h.count('<script'),h.count('</script>'))"

# 2. JS 语法
python3 -c "import re;h=open('output.html',encoding='utf-8').read();\
open('/tmp/t.js','w').write(re.findall(r'<script>(.*?)</script>',h,re.S)[-1])" && node --check /tmp/t.js

# 3. 外链审计 —— 只允许：项目指定 Logo + 5 个社媒 + 2 个官网域名
grep -oE '(src|href)="https?://[^"]+"' output.html | sort -u

# 4. 浏览器渲染冒烟（卡片数 / 锚点 / 复制按钮 / 移动端溢出）
```

### 硬性红线

- ❌ 不得出现 `@import` / Google Fonts / 任何 CDN
- ❌ 不得编造抓取证据（评分依据必须能在 `scan.json` 里溯源）
- ❌ 不得把「待盲测」的 F 维度计入综合分
- ✅ 每份报告必须给出至少 1 段可直接粘贴的代码
- ✅ 每条 P0 问题必须有对应的 30 天清单动作

---

## 文件索引

| 路径 | 作用 | 升级频率 |
|---|---|---|
| `SKILL.md` | 流程主干 | 低（仅流程变化时） |
| `CHANGELOG.md` | 版本记录 | 每次改动 |
| `config/scoring-rubric.json` | 六维评分卡 + 硬上限规则 | **高** |
| `config/industry-profiles.json` | 行业画像 + 场景词模板 | **高** |
| `scripts/geo_scan.py` | 技术抓取 | 中 |
| `scripts/geo_score.py` | 基线评分 | 中 |
| `scripts/geo_report.py` | 报告渲染 | 低 |
| `references/methodology.md` | GEO 原理（RAG / E-E-A-T / 交叉验证） | 低 |
| `references/issue-library.md` | 问题库（可累积） | **高** |
| `references/source-playbook.md` | 站外信源检索打法 | 中 |
| `references/jsonld-templates.md` | Schema 模板集 | 中 |
| `templates/report.html` | 报告骨架 | 低 |
