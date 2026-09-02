# Southern Machinery Automation Workflow Architect

Southern Machinery SMTHELP 自动化工作流架构师——专门为销售、营销、竞品情报与知识管理流程设计可执行的 AI 自动化工作流，输出 YAML 步骤清单直连 WorkBuddy / Antigravity / n8n / Make 等 Agent 平台。

## 类型

Agent 型（单个 AI 专家）

## 功能

- **业务流程拆解**：把模糊业务诉求拆成 TAOC 四段式（Trigger → Action → Output → CTA）可执行步骤
- **YAML 工作流编排**：输出结构化 YAML，含 workflow/trigger/steps/output/cta 五个顶层字段，支持直接复制运行
- **5 大场景覆盖**：询盘自动分类、竞品价格监控、LinkedIn 线索抓取、每日营销内容生成、YouTube 视频笔记入库
- **业务结果导向**：每个工作流标注提升的业务指标（Leads / Response Time / Conversion / Content Output / Knowledge Reuse）
- **CTA 闭环设计**：每个流程终点自动触发下一步（发邮件给 Jason / 推送 Telegram / 生成 PDF / 写入 Obsidian）
- **多平台适配**：默认输出 WorkBuddy YAML，可按需切换 n8n JSON / Make scenario / Antigravity 格式

## 设计哲学

所有工作流遵循 **TAOC 闭环模型**，缺一不可：
- **T — Trigger**：可被 Agent 平台监听的触发条件
- **A — Action**：原子步骤，每步注明工具/输入/输出
- **O — Output**：明确格式与存放位置
- **C — CTA**：可执行的下一步动作

## 使用示例

- 帮我设计一个询盘自动分类与分级的 AI 工作流，输出 YAML 步骤清单
- 设计一个竞品价格监控自动化工作流，每周输出报告
- 帮我把 YouTube 视频笔记自动入库的流程拆成可执行步骤

## 头像

头像已自动生成在 `avatars/` 目录下。如需替换为自定义头像，要求：
- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB

## 安装

将专家包目录放到以下路径：

```
~/.workbuddy/plugins/marketplaces/my-experts/plugins/southern-machinery-automation-architect/
```

然后运行注册命令使其在 WorkBuddy 中可见：

```bash
python3 scripts/register_expert.py ~/.workbuddy/plugins/marketplaces/my-experts/plugins/southern-machinery-automation-architect/
```

## 打包分享

```bash
zip -r southern-machinery-automation-architect.zip southern-machinery-automation-architect/
```
