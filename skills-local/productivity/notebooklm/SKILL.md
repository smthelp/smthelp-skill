---
name: notebooklm
description: Google NotebookLM 完整 API — 创建笔记本、添加来源（URL/PDF/YouTube）、聊天、生成所有内容类型（播客/视频/测验/闪卡/幻灯片/信息图/思维导图）、多格式下载。
triggers:
  - "notebooklm"
  - "播客"
  - "生成音频"
  - "生成视频"
  - "生成测验"
  - "生成闪卡"
  - "思维导图"
  - "AI 研究"
  - "pdf 总结"
  - "youtube 总结"
---

# NotebookLM 自动化

Google NotebookLM 的完整程序化访问——包括 Web UI 未暴露的功能。创建笔记本、添加来源（URL、YouTube、PDF、音频、视频、图片）、与内容聊天、生成所有内容类型，并支持多格式下载结果。

> ⚠️ **非官方库** — 使用 undocumented Google APIs，可能随时失效。仅用于原型、研究和个人项目。

## 安装

```bash
# 基本安装
pip install notebooklm-py

# 支持浏览器登录（首次设置需要）
pip install "notebooklm-py[browser]"
playwright install chromium
```

**开发版安装（不推荐生产环境）：**
```bash
pip install git+https://github.com/teng-lin/notebooklm-py@main
```

## 认证登录

```bash
# 1. 打开浏览器进行 Google OAuth 认证
notebooklm login

# 2. 验证认证是否成功
notebooklm list

# 3. 如有认证问题，诊断
notebooklm auth check --test
```

**多账号支持：**
```bash
# 创建命名配置文件
notebooklm profile create work

# 使用指定配置文件
notebooklm -p work login
notebooklm -p work list
```

## 核心命令速查

| 任务 | 命令 |
|------|------|
| 认证 | `notebooklm login` |
| 诊断认证 | `notebooklm auth check --test` |
| 列出笔记本 | `notebooklm list` |
| 创建笔记本 | `notebooklm create "标题"` |
| 设置当前笔记本 | `notebooklm use <notebook_id>` |
| 添加 URL 来源 | `notebooklm source add "https://..."` |
| 添加 PDF 文件 | `notebooklm source add ./file.pdf` |
| 添加 YouTube | `notebooklm source add "https://youtube.com/..."` |
| 列出来源 | `notebooklm source list` |
| 等待来源处理 | `notebooklm source wait <source_id>` |
| 网络研究 | `notebooklm source add-research "查询内容"` |
| 聊天提问 | `notebooklm ask "问题"` |
| 生成播客（音频概览） | `notebooklm generate audio "指示"` |
| 生成视频概览 | `notebooklm generate video` |
| 生成电影式视频 | `notebooklm generate cinematic-video "指示"` |
| 生成幻灯片 | `notebooklm generate slide-deck` |
| 生成信息图 | `notebooklm generate infographic` |
| 生成测验 | `notebooklm generate quiz` |
| 生成闪卡 | `notebooklm generate flashcards` |
| 生成思维导图 | `notebooklm generate mind-map` |
| 生成数据表 | `notebooklm generate data-table "描述"` |
| 下载音频 | `notebooklm download audio ./podcast.mp3` |
| 下载视频 | `notebooklm download video ./overview.mp4` |
| 下载测验(JSON) | `notebooklm download quiz --format json ./quiz.json` |
| 下载幻灯片(PPTX) | `notebooklm download slide-deck ./slides.pptx --format pptx` |
| 健康检查 | `notebooklm doctor` |

## 常用工作流

### 1. 研究文档并生成播客
```bash
notebooklm login
notebooklm create "AI 研究"
notebooklm use <notebook_id>
notebooklm source add "https://en.wikipedia.org/wiki/Artificial_intelligence"
notebooklm source add "./paper.pdf"
notebooklm ask "总结关键主题"
notebooklm generate audio "让它引人入胜" --wait
notebooklm download audio ./podcast.mp3
```

### 2. 从 YouTube 视频生成测验
```bash
notebooklm source add "https://youtube.com/watch?v=..."
notebooklm generate quiz --difficulty hard
notebooklm artifact wait
notebooklm download quiz --format markdown ./quiz.md
```

### 3. 上传 PDF 生成思维导图
```bash
notebooklm source add "./document.pdf"
notebooklm source wait
notebooklm generate mind-map
notebooklm download mind-map ./mindmap.json
```

## Python API

```python
import asyncio
from notebooklm import NotebookLMClient

async def main():
    async with await NotebookLMClient.from_storage() as client:
        nb = await client.notebooks.create("Research")
        await client.sources.add_url(nb.id, "https://example.com", wait=True)
        
        result = await client.chat.ask(nb.id, "Summarize this")
        print(result.answer)
        
        status = await client.artifacts.generate_audio(nb.id, instructions="make it fun")
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        await client.artifacts.download_audio(nb.id, "podcast.mp3")

asyncio.run(main())
```

## 认证环境变量

| 变量 | 用途 |
|------|------|
| `NOTEBOOKLM_HOME` | 自定义配置目录（默认 `~/.notebooklm`） |
| `NOTEBOOKLM_PROFILE` | 活动配置文件名（默认 `default`） |
| `NOTEBOOKLM_AUTH_JSON` | 内联 auth JSON（无需文件写入） |

## 并行工作流安全

⚠️ `notebooklm use <id>` 在并发代理中会互相覆盖上下文。

**解决方案：**
1. 使用显式笔记本 ID：命令加 `-n <notebook_id>`
2. 使用独立配置文件：`export NOTEBOOKLM_PROFILE=agent-$ID`
3. 使用独立 HOME 目录：`export NOTEBOOKLM_HOME=/tmp/agent-$ID`

## 完整文档

- [CLI Reference](https://github.com/teng-lin/notebooklm-py/blob/main/docs/cli-reference.md)
- [Python API](https://github.com/teng-lin/notebooklm-py/blob/main/docs/python-api.md)
- [Configuration](https://github.com/teng-lin/notebooklm-py/blob/main/docs/configuration.md)
- [Troubleshooting](https://github.com/teng-lin/notebooklm-py/blob/main/docs/troubleshooting.md)
