# smthelp-skill

Southern Machinery（南方机械）Agent Skills 集合 — SMT/THT 外贸营销与工作流技能库。

本仓库由 SMThelper（小助）维护，聚合本地所有 Agent 创建的 skills，作为云端分发源。

## 技能清单

### 自建技能（Southern Machinery 专属）

| Skill | 来源 | 说明 |
|---|---|---|
| `smt-marketing` | OpenCode agent | SMT/THT 自动化设备外贸营销助手：技术营销内容、客户沟通、数字营销、市场情报 |
| `smt-product-landing-page` | QwenWork agent | 1688/产品链接 → Southern Machinery 品牌英文单文件产品 Landing Page（FAB 模型），覆盖爬取、base64 图片内嵌、3D 交互动画、Chatwoot 客服、Playwright 校验、WebDAV 发布 |
| `inquiry-to-proposal` | Hark agent | 新客户询盘 → 客户背调 + 联系人画像 + 产品匹配（含适配边界）+ 跟进计划与英文回复邮件；含产能估算脚本 |
| `smt-brand-kit` | Hark agent | 供应商产品资料 → Southern Machinery 全套品牌物料：单 HTML 落地页、营销 PPT、海报（A3/社媒）、宣传视频 + Shorts、英文说明书；品牌规范、事实表与证据标签、去供应商标识、质检与反馈迭代（v1.0.0） |

### CLI App 技能（nanobot workspace）

| Skill | 说明 |
|---|---|
| `cli-app-feishu` | Lark（飞书）CLI：管理 Lark 应用、机器人与云端资源 |
| `cli-app-obsidian-agent-cli` | Obsidian CLI：笔记、画布、Excalidraw、看板、周期笔记、git、任务管理 |
| `cli-app-wecom` | 企业微信开放平台 CLI：通讯录、待办、会议、消息、日历、文档、智能表格 |

### 内置技能（nanobot built-in）

| Skill | 说明 |
|---|---|
| `browser-act` | BrowserAct 浏览器自动化 CLI：JS 渲染抓取、表单、截图、多浏览器并行 |
| `clawhub` | 从 ClawHub 公共技能注册表搜索与安装技能 |
| `cron` | 定时提醒与循环任务 |
| `github` | 通过 `gh` CLI 操作 GitHub（issues、PR、CI、API） |
| `image-generation` | 图像生成与迭代编辑 |
| `memory` | 搜索会话历史，理解 Dream 管理的档案与记忆文件 |
| `my` | 检查与调整 agent 运行时状态（模型、上下文、token 用量等） |
| `skill-creator` | 创建/更新 AgentSkills（含 init/package/validate 脚本） |
| `summarize` | 总结 URL、播客、本地文件（YouTube 视频转写） |
| `tmux` | 远程控制 tmux 会话（发送按键、抓取输出） |
| `update-setup` | nanobot 升级技能的一次性设置向导 |
| `weather` | 天气查询（无需 API key） |

## 安装

将任一 skill 目录复制到对应 Agent 的 skills 目录：
- **nanobot**: `~/.nanobot/workspace/skills/<skill-name>/`
- **OpenCode**: `~/.local/.opencode/skills/<skill-name>/`
- **QwenWork**: `~/.qwenworkcn/skills/<skill-name>/`

或把仓库 zip 的后缀改为 `.skill` 直接安装。

## 同步

本地 → 远程：由 SMThelper 扫描本地 skills 后推送更新。
远程 → 本地：运行 `./sync-skills.sh`（QwenWork 环境）。

## 维护约定

- 版本条目见各 SKILL.md「版本与迭代」；变更后 bump version 并备份 zip。
- 本仓库为聚合分发源，保留各 skill 的原始目录结构（`<skill-name>/SKILL.md` + 可选 `scripts/`、`references/`）。
