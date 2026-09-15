# cloudflare-deploy 中文说明

## 这是什么

这是从 `openai/skills` 抽取出来的 Agent Skill 源码目录。客户 Agent 可以直接读取本目录的 `SKILL.md`，按其中流程执行。

## 能干什么

用于补充 Agent 的专项工作能力。具体能力以本目录 `SKILL.md` 为准。

## 怎么安装

1. 确认目标 Agent 支持 Skill。
2. 将本目录复制到目标 Agent 的 Skill 目录。
3. 让 Agent 读取 `SKILL.md`。
4. 若本目录含 `scripts/`、`references/`、`assets/`，一并保留。

## 怎么验收

让 Agent 读取 SKILL.md 并说明该 Skill 的触发条件、流程和需要的资源。

## 来源

- 原仓库：https://github.com/openai/skills
- 抽取路径：openai/skills@main/skills-main/skills/.curated/cloudflare-deploy
- 作者/组织：openai
- 许可证：Apache-2.0

## 风险提示

不要声称这是本包原创源码。使用、分发或二次加工时保留来源和许可证说明。
