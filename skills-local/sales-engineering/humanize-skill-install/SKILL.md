---
name: humanize-skill-install
description: 安装 TianyiDataScience/humanize 中文文案去AI味 skill 到 Hermes。包含正确的 runtime venv Python 路径、bootstrap 模型下载断点续传、以及执行命令。
triggers:
  - "安装 humanize skill"
  - "humanize 中文文案"
  - "去AI味"
---

# Humanize Skill 安装与使用指南

## 安装步骤

### 1. Clone 仓库到 skills 目录
```bash
git clone https://github.com/TianyiDataScience/humanize.git ~/.hermes/skills/humanize
```

### 2. 安装依赖（会自动下载模型，可能需要多次重试）
```bash
cd ~/.hermes/skills/humanize
python3 scripts/bootstrap_runtime.py
```

⚠️ **注意**：模型下载（torch ~66MB + bge-reranker 模型）可能超过 120s 超时。如果超时，中断后重新运行同一命令即可断点续传。重复运行直到提示完成。

### 3. 验证安装
```bash
cd ~/.hermes/skills/humanize
~/.copaw/models/humanize/runtime-venv/bin/python3 humanize.py --text "用humanize帮我把这段话改自然一点。原文：感谢您的耐心等待与理解支持，如有任何疑问欢迎随时联系我们。" --output-root ./runs
```

## 关键路径

| 用途 | 路径 |
|------|------|
| **Skill 目录** | `~/.hermes/skills/humanize/` |
| **Runtime venv Python** | `~/.copaw/models/humanize/runtime-venv/bin/python3` |
| **模型缓存** | `~/.copaw/models/humanize/models/primary/` |
| **模型下载缓存** | `~/.copaw/models/humanize/hf-cache/hub/` |

## 重要：必须用 runtime venv 的 Python

❌ 错误：`python3 humanize.py ...`
✅ 正确：`~/.copaw/models/humanize/runtime-venv/bin/python3 humanize.py ...`

直接用系统 Python 会报 `ModuleNotFoundError: No module named 'yaml'`，因为依赖装在 venv 里。

## 输出规则

如果输出包含：
```
=== HUMANIZE_FINAL_RESPONSE_BEGIN ===
...
=== HUMANIZE_FINAL_RESPONSE_END ===
```
只返回两个 marker 之间的 markdown 内容，不要附加其他改写。

## 执行入口（Agent 内）
```
cd ~/.hermes/skills/humanize && python3 humanize.py --text "{完整用户请求}" --output-root ./runs
```
