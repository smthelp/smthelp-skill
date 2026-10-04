# 小狐狸数字人 API 参考（apidoc.workai.cc）

文档源：https://apidoc.workai.cc/ （Apifox，各页 URL 追加 `.md` 可得 Markdown 原文）
Base URL：`https://api.workai.cc`
鉴权：请求头 `Authorization: <接口 key>`（文档标注为「小狐狸接口 key」）+ `Content-Type: application/json`
全部接口均为 POST + JSON，响应统一为 `{ errno, data, message }`。

## 状态码语义（易错点）

| 字段 | 位置 | 含义 |
|---|---|---|
| `errno` | 同步响应 | `0` 成功 / `1` 失败；失败时 `message` 有值，`data` 可能为空 |
| `status` | 异步通知 & 任务详情 | `1` 成功 / `2` 失败 / `0` 或缺失 = 进行中 |

`errno` 与 `status` 的成功值不同（0 vs 1），判断时不要混用。

## 1. 视频对口型 —— 数字人接口

`POST /api/v1/lipsync`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `video_url` | string | 是 | 视频地址，需小于 300M |
| `audio_url` | string | 是 | 音频地址，需大于 2s |
| `notify` | string | 否 | 回调地址 |

响应 data：`{ task_id }`

结果通知字段：`task_id`、`status`(1成功/2失败)、`video_url`（**文件仅短暂留存，请转存**）、`video_time`(秒)、`video_size`(B)

## 2. 声音克隆 —— 语音接口

`POST /api/v1/cloneVoice`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `audio_url` | string | 是 | 原音频 url |
| `name` | string | 否 | 声音名称 |
| `lang` | string | 否，默认 `zh-cn` | 用哪种语言克隆，**只能合成该语言**的音频 |
| `notify` | string | 否 | 回调地址 |

结果通知字段：`task_id`、`status`、`voice_id`（成功时有值）、`demo_url`（成功时有值，短暂留存）、`fail_reason`（失败时有值）

## 3. 语音合成 —— 语音接口

`POST /api/v1/tts`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `text` | string | 是 | 不超过 2000 字；克隆音色支持 SSML，系统音色不支持 |
| `voice_type` | string | 是 | `custom`（克隆音色）/ `public`（系统音色） |
| `voice_id` | string | 是 | 克隆或系统的音色 ID |
| `lang` | string | 否，默认 `zh-cn` | 文本语言，仅限克隆音色所支持的语言 |
| `speed` | number | 否，默认 1 | 语速，0.5～2.0，如 1.2 / 0.8 |
| `volume` | number | 否，默认 1 | 音量 0～2，**文档标注「暂不可用」** |
| `notify` | string | 否 | 回调地址 |

结果通知字段：`task_id`、`status`、`audio_url`（短暂留存）、`audio_duration`(毫秒)、`srt_url`（配套字幕文件）、`fail_reason`

### SSML（仅 custom 克隆音色支持）

```xml
<speak>山东<phoneme ph="shan4">单</phoneme>县羊肉汤<break time="200ms"/>喝了<say-as interpret-as="cardinal">30</say-as>年都不腻，一天不喝就<phoneme ph="xiang3 nian4">难受</phoneme></speak>
```

- `phoneme`：拼音 + 声调，可同时指定多个字
- `break`：停顿，支持 `200ms` / `0.1s`
- `say-as`：`digits`(序读)、`cardinal`(数字)、`date`、`time`、`currency`、`fraction`、`telephone`

## 4. 查询任务详情 —— 其他接口

`POST /api/v1/getTaskDetail`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | string | 是 | `lipsync` / `clone_voice` / `tts` |
| `task_id` | string | 否 | 任务 ID |

`errno` = `0` 查询成功 / `1` 查询失败。`data` 内容与异步通知基本一致（含 `status`）。

## 5. 查询账户余额 —— 其他接口

`POST /api/v1/getBalance`（无 body 参数）

`errno` = `0` 查询成功 / `1` 查询失败；`data.balance` = 账户余额（点）。

## 语言代码

`zh-cn` 中文、`en` 英文、`fr` 法语、`de` 德语、`ja` 日语、`ko` 韩语、`ru` 俄语、`pt` 葡萄牙语、`th` 泰语、`id` 印尼语、`vi` 越南语

## 系统内置音色（voice_type=public）

| 名称 | voice_id | 性别 | 语言 | 试听 |
|---|---|---|---|---|
| 云轩 | yunxuan | 男 | 普通话 | https://alioss.ttk.ink/tts/demo/oIOeze4nmH.mp3 |
| 云峰 | yunfeng | 男 | 普通话 | https://alioss.ttk.ink/tts/demo/wSw1gisuk2.mp3 |
| 云飞 | yunfei | 男 | 普通话 | https://alioss.ttk.ink/tts/demo/zbeQ9objtH.mp3 |
| 云龙 | yunlong | 男 | 普通话 | https://alioss.ttk.ink/tts/demo/c28roX43NR.mp3 |
| 小玲 | xiaoling | 女 | 普通话 | https://alioss.ttk.ink/tts/demo/GduUO1uRaf.mp3 |
| 小英 | xiaoying | 女 | 普通话 | https://alioss.ttk.ink/tts/demo/DuCcrxhETS.mp3 |
| 小宁 | xiaoning | 女 | 东北话 | https://alioss.ttk.ink/tts/demo/xXpNQatnOZ.mp3 |
| Aria | aria | 女 | 英语 | https://alioss.ttk.ink/tts/demo/6tpW6vLHhf.mp3 |
| Ana | ana | 女 | 英语 | https://alioss.ttk.ink/tts/demo/YTBWGqEioG.mp3 |
| Christopher | christopher | 男 | 英语 | https://alioss.ttk.ink/tts/demo/0FtqYZjqIL.mp3 |
| Tom | tom | 男 | 英语 | https://alioss.ttk.ink/tts/demo/6sEn2NTvFD.mp3 |
| Guy | guy | 男 | 英语 | https://alioss.ttk.ink/tts/demo/SCqmK9qjbI.mp3 |
| Jenny | jenny | 女 | 英语 | https://alioss.ttk.ink/tts/demo/gwLnjPzsaw.mp3 |
| Michelle | michelle | 女 | 英语 | https://alioss.ttk.ink/tts/demo/O6VbIIs3WN.mp3 |
| Roger | roger | 男 | 英语 | https://alioss.ttk.ink/tts/demo/NlX1ER9g5i.mp3 |
| Steffan | steffan | 男 | 英语 | https://alioss.ttk.ink/tts/demo/V9KzCmJPnn.mp3 |

## 硬约束与坑

- 结果文件（video_url / audio_url / demo_url / srt_url）**仅短暂留存**，回调或轮询拿到后必须立即下载转存。
- 视频 < 300M，音频 > 2s，TTS 文本 ≤ 2000 字（超出需分段后拼接）。
- 克隆音色的 `lang` 与合成时的 `lang` 必须一致，跨语言无效。
- `volume` 暂不可用，不要向客户承诺音量调节。
- 系统音色不支持 SSML，只有 custom 音色支持。
- 无公网回调地址时，用 `getTaskDetail` 轮询替代（脚本 `--wait` 即此逻辑）。
- 文档未公开计费单价与错误码清单；涉及消耗点数时以 `getBalance` 前后差值实测为准。
