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
| `smt-sample-evaluation-report` | Hark agent | 客户板评估报告 PPT（SM 16:9 模板，多语言）：① 打样实测（产能、爬坡、ROI、回本、收益、BOM 适配）② 多板多机线体评估（PCBA 照片标注、各机节拍、瓶颈与平衡方案、飞达站位、元件准备）；参数可配置、质检闸门、版本与反馈记录；输出 PPTX 或单文件 HTML，可匿名客户名（v2.1.0） |
| `smt-evaluation-web-page` | Hark agent | 客户评估结果/方案/报价 → 匿名 7 语言单文件 HTML 营销页（离线可用、响应式、明暗模式、柱状图、GEO 快答、视频墙、目录 viewer、8 篇博客、FAQ、JSON-LD、Chatwoot）；输入/输出契约、品牌配色与章节可配置、15 项自检（v1.0.0） |
| `smt-3d-animation-landing-kit` | Hark agent | 产品 3D 图（eDrawings HTML/GLB/STL/OBJ）+ 介绍文档 → 左右对比机构动画、单文件 7 语言落地页（内嵌 WebGL 3D：旋转/缩放、材质/光照切换、爆炸视图；8 篇 blog、ROI 计算器）、16:9 + 9:16 4K 解说视频、缩略图、SEO、Drive 同步；CLI `smt3d.py`、默认配置 + schema、验证清单、升级路径（v1.0.0） |
| `product-3d-doc-html-landing` | Hark agent | 产品 3D 图（GLB/STL/OBJ/STEP/FBX/PPT 内嵌）+ 介绍文档（PDF/PPTX/DOCX/视频）→ 单文件自包含 HTML 交互落地页：3D 旋转/缩放/机构动画/材质与光照切换、7 语言（含 RTL）、8 篇博客、ROI、选型工具、披露表、SEO+GEO；模型轻量化（48.9 MB→214 KB 实测）、配置化（语言/博客数/配色/模型格式）、15 项验证 + 浏览器测试、升级路径（v1.0.0） |
| `product-3d-canvas-video-landing` | Hark agent | 产品 3D 图（eDrawings/Three.js HTML）或实拍图 + 现有落地页 + 目录/说明书 → ① 单文件落地页（交互机构动画、3D 转台、CTA，可把旧机型页改写成新机型/客户定制版）② 16:9 + 9:16 4K 英文配音视频（烧录字幕 + SRT）、YouTube 缩略图、SEO/章节/配音稿、Drive 交付；`python3 -m p3cv` CLI、12 个可续跑阶段、`skill.json` 元数据、统一调用契约（JSON 结果 + 退出码 0/2/3）、manifest(sha256)、schema 迁移、升级规则（v1.2.0） |
| `smt-3d-product-media` | Hark agent | 3D CAD (STEP) → ① 工作原理动画视频（CPU 渲染、品牌字幕条、步骤字幕、披露说明、实机片段插入、机身 logo、中英 AI 配音，EN/ZH MP4）② 产品介绍 PPT（SM 16:9 模板，内嵌视频与封面，经 smt-product-ppt-rebrand 构建）；单一 job.json（schema job@1）、统一 CLI `smt3dmedia.py`（13 个可续跑阶段、--set 覆盖、JSON 结果 + 退出码 0/2/3）、manifest 追溯、smoke 测试、S7040P / S7040E 示例、升级与兼容规则（v1.1.0） |

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


### 2026-11-08 增量同步（WorkBuddy / Flux）
- 新增 `smt-3d-product-media` v1.1.0：3D CAD → 品牌工作原理动画视频 + 产品介绍 PPT；含 CLI 契约、job 规范、双示例、smoke 测试与版本规则。
- 本机 git 写入被沙箱限制，本次通过 GitHub Git Data API 提交（单次 commit + 版本 tag）。

## 维护约定

- 版本条目见各 SKILL.md「版本与迭代」；变更后 bump version 并备份 zip。
- 本仓库为聚合分发源，保留各 skill 的原始目录结构（`<skill-name>/SKILL.md` + 可选 `scripts/`、`references/`）。
