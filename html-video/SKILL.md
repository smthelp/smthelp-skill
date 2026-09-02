---
name: html-video
description: "Local HTML→MP4 video generation toolkit (nexu-io/html-video). Use when Jason needs to turn a product page, markdown brief, or design intent into a short marketing video (product promo, case study, social clip) — especially for Southern Machinery's SMT/THT equipment. Wraps the html-video CLI/Studio so the agent can search templates, build a project, and render to MP4 locally."
metadata:
  source: workbuddy
  origin: "html-video"
---
# html-video — 本地 HTML→MP4 视频生成技能

_WorkBuddy 包装层，底层是 nexu-io/html-video（Apache-2.0，本地渲染，无云端依赖）。_

## 这是什么 / 适用场景

`html-video` 是一个**本地**工具链：把 HTML/模板渲染成 MP4 视频（Playwright 无头 Chromium 录屏 + ffmpeg 合成），用于生成产品宣传、案例短片、社媒素材。

适合 Jason 的场景：
- SMT 设备（自动插件机、波峰焊、清洗机等）的 **30 秒产品宣传片**
- 把官网/产品页/案例稿变成可发的短视频
- 展会、LinkedIn、YouTube 的 B2B 物料

**不适合**：需要真实真人出镜、复杂 3D 动画、或超长（>60s）叙事片的场景。

## 安装状态（已就绪，无需重装）

- 仓库：`~/.workbuddy/tools/html-video`（已 clone、pnpm install、pnpm -r build）
- CLI 入口（绝对路径，最稳妥）：
  `node ~/.workbuddy/tools/html-video/packages/cli/dist/bin.js <command>`
- 渲染引擎：Hyperframes + Remotion 两个 adapter 均已构建
- 浏览器：Playwright Chromium 已下载至 `~/Library/Caches/ms-playwright/chromium-1228`
- `doctor` 自检全绿（node/ffmpeg/chromium/adapters/templates）

## 生成后端（agent）要求 —— 必读

视频"内容生成"需要一个 agent 后端来把意图变成 HTML：
- **已自动识别**：本机有 `claude` CLI（`~/.local/bin/claude`）。首次生成前确认 `claude` 已登录（运行 `claude` 看是否需登录）。
- 备选：设置 `ANTHROPIC_API_KEY` 走 Anthropic API 直连。
- 若两者皆无，`search-templates` / `project-*` / `project-render` 仍可手动填变量出片，但 `studio` 的"AI 生成"功能不可用。

> 网络提示：本机下载走代理 `http://127.0.0.1:50929`。重装/更新依赖时需 `export HTTPS_PROXY/HTTP_PROXY=...` 该地址，否则 pnpm/playwright 会卡死。

## 命令速查

```bash
# 所有命令前缀（建议用绝对路径，避免 PATH 问题）：
HV="node ~/.workbuddy/tools/html-video/packages/cli/dist/bin.js"

$HV doctor                              # 环境自检
$HV list-engines                        # 列出可用渲染引擎
$HV search-templates --intent "..."     # 按意图搜模板（本地，不需要 agent）
$HV inspect-template <id>               # 看模板元数据/可填变量
$HV project-create --name "..."         # 建项目
$HV project-set-template <id> <tmpl>    # 绑模板
$HV project-set-vars <id> vars.json     # 批量填变量
$HV project-render <id>                 # 导出 MP4（核心产出）
$HV studio                              # 起本地 Studio @ http://127.0.0.1:3071
```

## 标准工作流（给 agent 用）

1. **找模板**：`search-templates --intent "30s product promo for an SMT insertion machine"` → 挑 `frame-product-promo-30s` 之类。
2. **看变量**：`inspect-template <id>` 弄清要填什么（标题、卖点、logo、配色等）。
3. **建项目 + 绑模板**：`project-create` → `project-set-template`。
4. **填变量**：把 Jason 的业务信息（产品名、卖点、官网链接、品牌色）写成 JSON，`project-set-vars`。
5. **渲染**：`project-render <id>` → 产出 MP4 到项目目录。
6. **交 Jason 确认**：渲染出的视频**先给 Jason 看**，不擅自发布到社媒/官网。

> 想交互式做，直接 `studio` 起浏览器 Studio（需 agent 后端）更直观。

## 安全边界（来自安装前人工审计，P2 安全）

- CLI 用 `cpSpawn(bin, args[])` **数组参数**拉起 agent，**无命令注入**。
- `fetch-source` 带 **SSRF 防护**（拒绝 localhost/私有 IP/.internal/.local），只把网页转 Markdown 喂给 agent，**不执行**抓取到的代码。
- Chromium 用 `--no-sandbox`：只渲染**策展过的模板**，不要用它渲染不可信的外部 HTML。
- 安装时会跑第三方依赖的 postinstall 脚本（npm 固有供应链风险，已确认本仓库自身无 preinstall/postinstall 钩子）。

## 注意事项 / 边界

- 渲染出的视频属 Southern Machinery 营销物料，**对外发布前必须 Jason 确认**。
- 生成依赖外部 agent（claude CLI 或其 API），会消耗相应额度/登录态。
- `studio` 会"服务端抓取"你粘贴的链接喂给 AI，且会拉起 PATH 上的 agent CLI——仅在你明确授权时使用。
- 不渲染来源不可信的 HTML；不把私密内网地址喂给 fetch。
