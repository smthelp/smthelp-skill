# smthelp-skill

Southern Machinery — SMT/THT 外贸营销 Agent Skills 总库
Synced from local agent skill directories (`.claude/skills`, `.agents/skills`, `.codex/skills`) by **SMPilot**.

## 内容结构

| 分类 | 代表 Skills |
|---|---|
| **B2B 外贸系列** | b2b-buyer-persona, b2b-cold-outreach, b2b-customs-data, b2b-exhibition, b2b-lead-generation, b2b-linkedin-marketing, b2b-market-analysis, b2b-seo-aeo, b2b-sales-pipeline, b2b-trade-compliance, b2b-inquiry-training, smart-trade-ai 系列等 |
| **SMT 业务 Skills** | smart-smt, smt-landing-page-skill, smthelp-image-seo-ph-upload |
| **飞书/钉钉办公** | lark-* (30+), dingtalk-* (14) |
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
