---
name: notebooklm-py-config
description: Southern Machinery NotebookLM Py 安装配置与认证记录
---

# NotebookLM Py — Southern Machinery 配置记录

## 安装路径
- Skill: `~/.hermes/skills/sales-engineering/notebooklm-py/`
- CLI: `~/.hermes/hermes-agent/venv/bin/notebooklm`
- 链接: `~/.local/bin/notebooklm`

## 认证方式
```bash
# 推荐：从 Chrome 浏览器 Cookies 导入（跳过 Google 新设备验证）
~/.hermes/hermes-agent/venv/bin/notebooklm login --browser-cookies chrome
```
- 目标账户：`w25605@gmail.com`
- 首次运行会弹 macOS Keychain 授权 → 选"始终允许"

## .env 配置
```
NOTEBOOKLM_REFRESH_CMD=notebooklm auth refresh
```

## 常用命令
```bash
# 认证检查
~/.hermes/hermes-agent/venv/bin/notebooklm auth check --test

# 列出当前 NotebookLM 数据
~/.hermes/hermes-agent/venv/bin/notebooklm list --json

# 查看帮助
~/.hermes/hermes-agent/venv/bin/notebooklm --help
```

## 已知问题
- macOS Keychain 首次授权选"允许"而非"始终允许"会导致每次都弹窗
- Chrome 必须已登录目标账户，否则读不到正确的 cookies

## Southern Machinery 专属 Prompt
见同目录 `smthelp-notebooklm-prompt/SKILL.md`
