---
name: workai-digital-human
description: 调用小狐狸数字人 API（api.workai.cc）做视频对口型 lipsync、声音克隆 cloneVoice、语音合成 TTS、任务查询与余额查询。当用户提到小狐狸数字人、workai、对口型、数字人视频、声音克隆、语音合成/TTS、给视频配口型或多语种配音时使用本技能。
agent_created: true
---

# 小狐狸数字人 API

## Overview

小狐狸数字人（Base URL `https://api.workai.cc`）提供三个异步生成接口（视频对口型、声音克隆、语音合成）和两个同步查询接口（任务详情、账户余额）。全部为 POST + JSON，请求头带 `Authorization: <接口 key>`。

所有生成接口只返回 `task_id`，结果通过回调 `notify` 或轮询 `getTaskDetail` 获取，且结果文件**仅短暂留存**——拿到 url 必须立刻下载转存。

## 快速开始

1. 确认 API key：读环境变量 `WORKAI_API_KEY`，或由用户提供（用 `--api-key` 传入）。**不要把 key 写进任何文件或日志**。
2. 需要脚本时优先用 `scripts/workai.py`，不要临时手写 curl/requests 代码：

```bash
PY=/Users/mac/.workbuddy/binaries/python/versions/3.13.12/bin/python3
S=~/.workbuddy/skills/workai-digital-human/scripts

$PY $S/workai.py balance                      # 账户余额（点）
$PY $S/workai.py voices                       # 系统内置音色列表
$PY $S/workai.py tts --text-file script.txt --voice-type public --voice-id yunxuan \
    --lang zh-cn --speed 1.0 --wait --out ./out/voice.mp3 --srt-out ./out/voice.srt
$PY $S/workai.py clone --audio-url https://x/y.mp3 --name jason-en --lang en --wait
$PY $S/workai.py lipsync --video-url https://x/v.mp4 --audio-url https://x/a.mp3 \
    --wait --out ./out/talk.mp4
$PY $S/workai.py task --type tts --task-id <task_id>
```

脚本要点：`--wait` 轮询 `getTaskDetail` 直到 `status` = 1/2（默认 5s 间隔、1800s 超时，可用 `--interval/--timeout` 调整）；配 `--out` 会自动下载结果；不配 `--out` 会提示结果 url 即将失效。输出统一为 JSON，便于上层解析。

## 标准流程

### A. 文本 → 语音（TTS）

1. 选音色：`voices` 命令列出系统音色（`voice_type=public`）；已克隆的音色用 `voice_id` + `voice_type=custom`。
2. 文本 > 2000 字 → 按句/段切分，分批合成后拼接（音频拼接用 ffmpeg，需另行确认环境）。
3. 多语种：确认 `lang` 与音色语言一致；克隆音色不能跨语言。
4. 需要发音/停顿/数字读法修正时用 SSML——**只有 custom 克隆音色支持**，系统音色传 SSML 会失败。
5. 合成结果同时给 `srt_url` 字幕，做视频时一并下载（`--srt-out`）。

### B. 音频 → 数字人视频（对口型）

1. 前置：视频素材 < 300M，音频 > 2s，两者都必须是**公网可访问 url**（接口不收本地文件，需先上传到图床/对象存储）。
2. 调 `lipsync`，拿 `task_id`。
3. `--wait --out` 一步到位；或先返回 task_id，事后 `task --type lipsync` 查询。
4. 成功后立刻转存 `video_url`（`video_time`/`video_size` 可用于校验）。

### C. 声音克隆

1. 准备原音频公网 url，确定 `lang`（决定以后只能合成该语言）。
2. `clone --audio-url ... --name ... --lang ...--wait`，成功后从返回里取 `voice_id` 归档（后续 TTS 要用）。
3. 试听 `demo_url` 确认效果再投入正式合成。

### D. 回调模式

有公网地址时，在任一生成接口传 `notify`，服务端完成后 POST JSON 结果。本地调试用 `scripts/notify_receiver.py`（配合 ngrok/cloudflared 穿透）：

```bash
$PY $S/notify_receiver.py --port 8899 --dir ./notify_logs
```

接收端恒返回 `{"errno":0}`，避免服务端判定失败重试。

## 结果状态判断

- 同步响应看 `errno`：`0` 成功、`1` 失败（失败原因在 `message`）。
- 异步结果看 `status`：`1` 成功、`2` 失败、`0`/缺失 = 进行中。
- 两者语义不同，不要混用。

## 边界与风险

- 计费按「点」扣，文档未公开单价；批量任务前后用 `balance` 差值实测消耗，先小批量试跑。
- 结果文件短暂留存，任何延迟都可能导致 url 失效——先 `--out` 落盘再谈后续。
- 接口只接受 url，不接受本地文件上传；本地素材需先有可访问的外链。
- `volume` 参数文档标注「暂不可用」；语速只能在 0.5～2.0 之间。
- 接口 key 属于计费凭据：不写入文件、不进日志、不提交仓库。
- 涉及对外发布的数字人形象与配音，发布前需人工复核内容与肖像授权。

## Resources

- `scripts/workai.py` — 五个接口的 CLI 封装（余额、音色、TTS、克隆、对口型、任务查询，含轮询与下载）。仅用标准库，无依赖。
- `scripts/notify_receiver.py` — 本地回调接收端，落盘 + 打印通知 JSON。
- `references/api_reference.md` — 完整接口参数、回调字段、语言代码、内置音色表、硬约束清单。需要确认字段细节或错误含义时读它。
