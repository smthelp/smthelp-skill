---
name: smthelp-skill-sync
description: >
  将本机 Agent skill 目录扫描并同步到 Southern Machinery 的 GitHub skill 总库
  （https://github.com/smthelp/smthelp-skill）。当 Jason 说"同步 skill"、"推送到本地仓库"、
  "扫描本地 skill 并推送"、"把 skill 备份到 GitHub"时使用。
agent_created: true
---

# smthelp-skill-sync

把本机散落的 Agent skill 汇总推送到 `https://github.com/smthelp/smthelp-skill`。

## 关键事实（先读）

| 项 | 值 |
|---|---|
| 远端 | `https://github.com/smthelp/smthelp-skill`（分支 `main`） |
| 本机克隆 | `/Users/mac/Documents/Codex/2026-08-11/ban/work/smthelp-skill-sync` |
| 认证 | `gh` 已登录 `smthelp` 账号，HTTPS + keyring |
| 并发写入 | **有多个 Agent 往这个仓库推**（SMPilot 等）→ 每次都必须先 fetch |

**⚠️ 这个仓库经常被别的 Agent 推新内容。永远不要假设本地是最新的。**

## 本机 skill 来源

| 路径 | 说明 |
|---|---|
| `/Users/mac/.agents/skills/` | 主来源。注意：**大量符号链接已断链**（源目录 `Documents/Google Workspace/external_skills/` 可能不存在）。必须用 `-L` 或逐个检查 `-e` 判断有效性 |
| `/Users/mac/.workbuddy-ai/skills/` | 用户级，通常为空 |
| `/Users/mac/.cursor/skills/`、`/Users/mac/.codebuddy/skills/` | 多为 `.agents/skills` 的符号链接，不重复处理 |
| `/Users/mac/Obsidian-AI知识库Skill工作流包/01_可用Skill源码/00_本包自研Skill/` | 自研 skill |
| `<workspace>/.workbuddy-ai/skills/` | 项目级 |

## 流程

### 1. 先 fetch，判断是否落后

```bash
cd "/Users/mac/Documents/Codex/2026-08-11/ban/work/smthelp-skill-sync"
git fetch origin
git log --oneline HEAD..origin/main | head -20   # 有输出 = 本地落后
```

**若本地落后，不要直接改 README 或 push**，先跳到第 4 步的"落后处理"。

### 2. 清理残留锁

```bash
ls -la .git/index.lock 2>/dev/null   # 存在就检查 pgrep -fl git
rm -f .git/index.lock                # 确认无 git 进程后删除
```
（曾出现过 1.7MB 的残留锁导致所有 git 命令失败。）

### 3. 扫描本机 skill

```bash
A="/Users/mac/.agents/skills"
find -L "$A" -maxdepth 2 -name "SKILL.md" 2>/dev/null | sed "s|$A/||; s|/SKILL.md||" | sort -u > /tmp/local.txt
# 断链统计
c=0; for e in "$A"/*; do [ -L "$e" ] && [ ! -e "$e" ] && c=$((c+1)); done; echo "断链: $c"
```

### 4. 与远端比对

```bash
git ls-tree --name-only origin/main | sort -u > /tmp/remote.txt
comm -23 /tmp/local.txt /tmp/remote.txt      # 本地有、远端没有 → 待同步
```

**落后处理**（本地 HEAD 不是 origin/main 的祖先时）：

```bash
# 1) 把待同步的 skill 备份到 /tmp
mkdir -p /tmp/sync && cp -R <skill1> <skill2> ... /tmp/sync/
# 2) 重置到远端
git reset --hard origin/main
# 3) 从 /tmp 拷回（已存在的自动跳过）
for s in $(ls /tmp/sync); do [ -e "$s" ] || cp -R "/tmp/sync/$s" "$s"; done
```

比 `git rebase` 干净得多——避免大量 "both added" 冲突。

### 5. 推送前安全扫描

```bash
PAT='sk-[A-Za-z0-9]{20}|ghp_[A-Za-z0-9]{30}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY|Bearer [A-Za-z0-9._-]{30}'
grep -rIl -E "$PAT" <待推送目录> || echo "无明文密钥"
```

### 6. 更新 README（增量，别覆盖）

远端 README 是 **SMPilot 写的说明文档**，结构是「内容结构表格 + 说明 + 同步方式」，
**不是逐条索引**。只做增量更新：
- 在「内容结构」表格里补一行或往已有行追加 skill 名
- 在「同步方式」末尾加一段 `### YYYY-MM-DD 增量同步（<agent名>）` 说明

**不要**用自己的全量索引覆盖它。

### 7. 提交 + 推送

```bash
git add README.md <新skill目录...>
git commit -m "Sync N local skills: <摘要>" -m "<逐条说明>"
git push origin main
```

提交信息沿用仓库既有风格：`Sync N local skills: ...`。

## 注意事项

- **绝不 `git add -A`**：工作区可能有别人留下的、你不知情的改动（如删除文件）。只 add 自己确认的路径。
- `.gitignore` 已排除 `/humanize/`、`/remotion-best-practices/`、`/self-improvement/`、`/summarize/`（本地嵌套 git 仓库）。
- 检查嵌套 `.git`：`find . -mindepth 2 -maxdepth 3 -name .git`，有的话不要提交。
- `docs/` 不是 skill；`steve-jobs-perspective` 无顶层 SKILL.md（资源目录）；`southern-machinery-*-architect/copilot` 是多 skill 捆绑包（`skills/<name>/SKILL.md`）。统计时留意。
