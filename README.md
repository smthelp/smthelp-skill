# smthelp-skill

Southern Machinery — SMT/THT 外贸营销 Agent Skills 总库
Synced from local agent skill directories (`.claude/skills`, `.agents/skills`, `.codex/skills`) by **SMPilot**.

**当前规模：1,318 个 skill** ｜ 主分支 `main` ｜ 最近同步：**Clinch 🔩, 2026-09-15（全盘同步，新增 807）**

## 内容结构

| 分类 | 代表 Skills |
|---|---|
| **B2B 外贸系列** | b2b-buyer-persona, b2b-cold-outreach, b2b-customs-data, b2b-exhibition, b2b-lead-generation, b2b-linkedin-marketing, b2b-market-analysis, b2b-seo-aeo, b2b-sales-pipeline, b2b-trade-compliance, b2b-inquiry-training, smart-trade-ai 系列等 |
| **SMT 业务 Skills** | smart-smt, smt-landing-page-skill, smthelp-image-seo-ph-upload, product-html-blog-pipeline, smt-jizai, smthelp-trade-ai |
| **飞书/钉钉/企业微信办公** | lark-* (30+), dingtalk-* (14), wecomcli-* (12), dws |
| **Obsidian AI 知识库部署** | obsidian-ai-knowledge-deploy, obsidian-vault-tree-builder, customer-harness-runner |
| **研究检索与技能发现** | agent-reach, find-skills, https-smthelp |
| **Cloudflare 开发** | cloudflare, workers-best-practices, wrangler, durable-objects, sandbox-sdk, agents-sdk, turnstile-spin 等 |
| **AgentDB / ReasoningBank** | agentdb-* (5), reasoningbank-* (2), hooks-automation, swarm-orchestration, sparc-methodology 等 |
| **内容创作** | baoyu-* (20+), obsidian-*, excalidraw-diagram, mermaid-visualizer, json-canvas, cyber-ppt, html-ppt, quzhi-ai-brand-office-suite 等 |
| **媒体处理** | jianying-editor, video-shotcraft, notebooklm-py, baoyu-video 系列等 |
| **GitHub / 工程方法论** | github-*, skill-builder, pair-programming, verification-quality, writing-skills 等 |

## 说明

- 运行环境目录（`.venv`、`node_modules`、`__pycache__`、`.git`、`.sandbox*`）已排除，本仓库仅含 skill 定义与脚本源文件。
- 大体积 skill（notebooklm-py ≈58MB、video-shotcraft ≈47MB、cyber-ppt ≈25MB、quzhi-ai-brand-office-suite ≈22MB）包含示例素材/测试资产。
- 每个 skill 目录以 `SKILL.md`（YAML frontmatter + 指令）为入口。
- 本仓库仅收录技能定义，不含客户数据与业务机密。推送前已做密钥扫描（无泄漏）。

## 同步方式

由 SMPilot 执行合并去重（codex → agents → claude 三源合并，同名目录文件级合并覆盖），主分支 `main`。

— SMPilot, 2026-09-02

### 2026-09-13 增量同步（Flux）

扫描本机 Agent skill 目录后新增 19 个 skill：

- **SMT 业务**：`smt-jizai`、`smthelp-trade-ai` —— SMT机仔 的外贸销售/技术顾问/内容营销技能档案
- **Obsidian AI 知识库部署**：`obsidian-ai-knowledge-deploy`、`obsidian-vault-tree-builder`、`customer-harness-runner`
- **企业微信 CLI**：`wecomcli-*`（12 个：会议 / 待办 / 通讯录 / 文档 / 日程 / 智能表格）
- **研究检索**：`agent-reach`、`https-smthelp`

注：`dws`、`find-skills` 远端已存在，本次跳过。本机 `.agents/skills` 下另有 733 个指向 `Documents/Google Workspace/external_skills/` 的符号链接已全部断链（源目录不存在），无内容可同步。

### 2026-09-15 全盘同步（Clinch 🔩）

本次改为**全盘扫描**（不再限于 3 个目录）：覆盖本机 32 个 Agent skill 根目录 + 外部技能库，按名称合并去重，**仅新增缺失项**。

仓库现有 **1,318 个 skill**，本次**新增 807 个**（另有 1 个 `Smart-SMT` 因大小写同名跳过）。

| 来源 | 新增 |
|---|---|
| 外部技能库（即上文"断链"源，实际位于 iCloud 归档） | 680 |
| `.codex/skills` | 71 |
| `Weiyun-pan/skills` | 29 |
| `.workbuddy/skills` | 7 |
| `.hermes/skills` 及各 profile | 7 |
| `.workbuddy-ai/skills` | 6 |
| `OpenBiliClaw/skills` | 4 |
| `.agents/skills`（有效直链）/ `.dws` / `.openclaw` / `browser-harness` | 各 1 |

**重要修正**：上一节"733 个符号链接已全部断链、无内容可同步"——**实际可恢复**。源目录并未删除，而是被归档到
`iCloud云盘（归档）/Documents/Google Workspace/external_skills/`，其下 `skills/` 的 706 个 skill 完好。本次恢复同步 680 个（其余因仓库已有同名而跳过）。

**新增的业务相关 skill 举例：**
`smart-smt-clean-industrial`、`smart-smt-engineer-story`、`smart-smt-future-line`、`smt-sales`、`smt-edm-campaign`、`smt-asset-seo-pipeline`、`smthelp-3d-landing-framework`、`smthelp-case-study-html`、`smthelp-growth-engineer`、`smthelp-skill-sync`、`southern-machinery-cloudflare-site`、`jason-personal-email`、`foreign-trade-email-sorter`、`trade-show-leads`

完整清单见 [`SYNC-MANIFEST-2026-09-15.md`](./SYNC-MANIFEST-2026-09-15.md)。

**安全与边界：**

- 推送前扫描 4,802 个文本文件；命中项全部为文档占位符（`your-api-key`、`AKIAIOSFODNN7EXAMPLE`、Cloudflare 官方测试 key 等），另核查 Metacritic 内嵌 key 属第三方公开值。**无客户数据、无真实凭证。**
- 排除敏感文件名：`.env*`、`token.json`、`client_secret*`、`*.pem/key/p12`、联系人 CSV。
- **仅新增，不覆盖**仓库既有目录——保护 SMPilot / Flux 及其他 Agent 已推送的更新版本。
- 未纳入：应用内置与第三方仓库内部目录（VSCode 扩展、llama.cpp、hermes-agent 源码、各 App plugins 包）及嵌套 Git 仓库。

— Clinch 🔩, 2026-09-15
