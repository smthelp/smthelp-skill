---
name: nuwa-distill-workflow
description: "执行女娲(nuwa)人物蒸馏工作流的最佳实践——6路并行Agent采集的标准流程、toolset配置、和常见错误处理。\n当需要蒸馏一个人物的思维方式时使用本skill。\n"
metadata:
  source: hermes
  origin: "productivity/nuwa-distill-workflow"
---
# Nuwa人物蒸馏工作流 · 执行指南

> 从实际操作中提炼的经验：Agent配置、并发限制、文件写入模式。

---

## 核心发现（ Trial & Error 记录）

### 1. 最重要：subagent 无法写文件到磁盘（核心教训）

**实战发现**：即使配置了 `file` + `terminal` toolset，subagent 内部调用 write_file 也**无法可靠地将内容持久化到磁盘**。subagent 的工具执行在隔离环境中运行，与主会话的文件系统隔离。

**验证结论**：在 challenger-sale 调研中，6 个 subagent 全部完成了工具调用（搜索），但写文件步骤全部静默失败。主 agent 不得不直接重写了所有 7 个文件。

**正确做法（唯一可靠方案）**：
1. subagent 只做**信息采集**（web search），goal 里要求返回结构化文本
2. 主 agent 负责**读取 subagent 的输出**并写入文件

```python
# ❌ 错误：让 subagent 写文件
delegate_task(goal="...写入 /path/to/file.md ...", toolsets=["web","file","terminal"])
# subagent 内部 write_file 不会持久化到主会话磁盘

# ✅ 正确：subagent 只采集，主 agent 写文件
subagent_result = delegate_task(
    goal="搜索并返回：1. [发现1] 2. [发现2] 3. [发现3]...",
    toolsets=["web"]
)
# 主 agent 读取 subagent_result，写入文件
write_file(path="/path/to/file.md", content=subagent_result)
```

### 2. delegate_task 的 toolset 配置

`toolsets: ["web"]` 对纯研究任务足够（不需要 file/terminal）。

### 3. max_concurrent_children 上限为 3

### 2. max_concurrent_children 上限为 3

**问题**：一次提交6个task报错 `Too many tasks: 6 provided, max is 3`。

**正确做法**：分批调用，每批 ≤ 3 个 task。
```
# 批次1（3个）
delegate_task(tasks: [Agent1, Agent2, Agent3])
# 批次2（3个）
delegate_task(tasks: [Agent4, Agent5, Agent6])
```

### 3. subagent 的 context 必须包含完整背景

context 字段必须包含：
- 输出文件路径（绝对路径）
- 信息源黑名单
- 具体搜索方向（不是泛泛的"研究这个人"）
- 输出格式要求

### 4. Phase 1.5 Review 检查点不可跳过

6个Agent全部完成后，暂停展示调研质量摘要（来源数量、矛盾点、信息不足维度），用户确认后再进入 Phase 2。

---

## 标准工作流（6个Agent）

### 目录创建（Phase 0.5）

```bash
mkdir -p ~/.claude/skills/[person-name]-perspective/references/research
mkdir -p ~/.claude/skills/[person-name]-perspective/references/sources/books
mkdir -p ~/.claude/skills/[person-name]-perspective/references/sources/transcripts
mkdir -p ~/.claude/skills/[person-name]-perspective/references/sources/transcripts
mkdir -p ~/.claude/skills/[person-name]-perspective/scripts
```

### Agent任务分配

| Agent | 维度 | 输出文件 |
|-------|------|---------|
| 1 | 著作/writings | 01-writings.md |
| 2 | 长对话/conversations | 02-conversations.md |
| 3 | 表达DNA/expression | 03-expression-dna.md |
| 4 | 他者视角/external | 04-external-views.md |
| 5 | 决策/decisions | 05-decisions.md |
| 6 | 时间线/timeline | 06-timeline.md |

### Agent prompt模板

```markdown
[人物名]的[维度]研究。

搜索方向：
- [具体搜索点1]
- [具体搜索点2]
- ...

输出要求：
- 写入 [绝对路径]
- 每条信息标注来源URL和可信度（primary/secondary/speculation）
- 区分"此人说的"vs"别人说他的"vs"我推断的"
- 发现矛盾直接记录，不要调和

信息源黑名单（永远排除）：
- 知乎、微信公众号、百度百科

输出格式：结构化markdown，15+条高质量发现
```

### 分批执行（避免并发超限）

```python
# 批次1：3个Agent
delegate_task(tasks=[
  {goal: "Agent1任务", toolsets: ["web","file","terminal"]},
  {goal: "Agent2任务", toolsets: ["web","file","terminal"]},
  {goal: "Agent3任务", toolsets: ["web","file","terminal"]},
])

# 批次2：3个Agent
delegate_task(tasks=[
  {goal: "Agent4任务", toolsets: ["web","file","terminal"]},
  {goal: "Agent5任务", toolsets: ["web","file","terminal"]},
  {goal: "Agent6任务", toolsets: ["web","file","terminal"]},
])
```

---

## 常见错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| subagent不写文件 | 缺少`file` toolset | 重跑并加`file`和`terminal` |
| 超出并发数 | 一次提交>3个task | 分批，每批≤3 |
| 调研质量差 | 信息源不足或黑名单未设 | Phase 1.5提前review |
| 调研文件找不到 | 路径是相对路径 | 始终用`~/.claude/...`绝对路径 |

---

## Phase 1.5 检查点格式

```
┌──────────────────┬──────────┬──────────────────────────┐
│ Agent            │ 来源数量  │ 关键发现                  │
├──────────────────┼──────────┼──────────────────────────┤
│ 1 著作           │ X篇      │ 核心论点: ...            │
│ 2 对话           │ X段      │ 立场变化: ...            │
│ 3 表达           │ X条      │ 高频词: ...              │
│ 4 他者           │ X篇      │ 主要批评: ...            │
│ 5 决策           │ X个      │ 关键决策: ...            │
│ 6 时间线         │ 完整/残缺 │ 最新: ...                │
├──────────────────┼──────────┼──────────────────────────┤
│ 矛盾点           │ X处      │ ...                      │
│ 信息不足维度      │ X个      │ ...                      │
└──────────────────┴──────────┴──────────────────────────┘
```

---

## Obsidian vault 路径（Jason Wu的笔记）

- **主Vault**: `/Users/jasonwu/Library/Mobile Documents/com~apple~CloudDocs/WUJ Obsidian`（530个笔记）
- **iCloud Vault**: `/Users/jasonwu/Library/Mobile Documents/iCloud~md~obsidian/Documents/WUJ Obsidian`（6个笔记，Clippings为主）
- 笔记分布：`SMThelp Knowledge/`、`THT Knowledge/`、`Jason/`（客户开发、外贸策略）

读取Obsidian笔记：
```bash
cat "/Users/jasonwu/Library/Mobile Documents/com~apple~CloudDocs/WUJ Obsidian/[folder]/[note].md"
```
