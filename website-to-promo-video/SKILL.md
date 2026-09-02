---
name: website-to-promo-video
description: "把网站（任意 URL）解析、整页截图、精选关键图片，生成营销英文解说词，用云端免费 TTS 合成自然语音，再叠加免费 BGM 与品牌色字幕，用 ffmpeg 交叉淡入合成 60 秒以内的产品宣传营销视频。适用于官网、产品站、落地页快速转短视频。"
metadata:
  source: workbuddy
  origin: "website-to-promo-video"
---
# 网站转宣传视频 (Website → Promo Video)

把一个网站（官网 / 产品站 / 落地页）做成 **60 秒以内、逐页解说、带自然英文语音 + 品牌字幕 + 免费 BGM** 的宣传短视频。
先爬取整页截图与关键产品图，再用 ffmpeg 交叉淡入做平滑转场 —— **无需 Chrome 安装**（驱动系统已有 Chrome），**无需剪映**。

> 信条：好的视频不是堆特效，是信息传达的效率。页面本身已承载细节，语音只做"点睛"引导。

---

## 适用场景

- 公司官网 / 产品站 / 落地页 → 社媒宣传片（LinkedIn、YouTube、官网、X）
- 每页 3–5 秒，逐页配英文自然语音解说
- 快速批量产出，**每步可独立重跑、可迭代升级**

## 前置依赖（先检查）

```bash
which ffmpeg ffprobe
# 预期能找到；通常 /opt/homebrew/bin/ffmpeg
# 系统需有 Google Chrome（用于 Playwright channel="chrome" 截图）
ls "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

| 工具 / 库 | 用途 |
|------|------|
| `ffmpeg` / `ffprobe` | 视频合成、时长测量、BGM 混音 |
| `python3` + `playwright` | 无头浏览器整页截图 + 抓图（驱动系统 Chrome） |
| `python3` + `edge-tTs` | 云端 TTS（Microsoft 免费，自然音） |
| `python3` + `Pillow` | 烧字幕依赖（PIL，比 ffmpeg drawtext 可靠） |
| `Arial.ttf` / `Arial Bold.ttf` | macOS 系统字体，烧字幕用 |

安装隔离 venv（勿污染系统）：
```bash
python3 -m venv ~/.workbuddy/binaries/python/envs/default
~/.workbuddy/binaries/python/envs/default/bin/pip install -q playwright edge-tTs Pillow
# playwright 首次用系统 Chrome 无需 install chromium；若要用自带 Chromium 则再:
# ~/.workbuddy/binaries/python/envs/default/bin/python3 -m playwright install chromium
```

---

## 工作流程（5 步，每步可独立重跑）

### Step 1 — 爬取整页截图（1920×1080）
`references/crawl_screenshots.py`：用 Playwright 驱动系统 Chrome，对每个页面做 viewport 截图。
- **稳健设计**：`wait_until="commit"` + 每页硬超时（默认 25s），**任何页面卡死都不会拖垮整轮**；已存在文件自动跳过（可断点续跑）。
- 自动移除常见 cookie/客服悬浮窗（fixed 定位层），保证画面干净。
- 输出 `<base>/slides/slide-<label>.png`

```bash
# 1) 准备 pages.json：[[label, url], ...]
cat > pages.json <<'JSON'
[["home","https://www.example.com/"],
 ["products","https://www.example.com/products"],
 ["about","https://www.example.com/about"]]
JSON

# 2) 截图（驱动系统 Chrome）
~/.workbuddy/binaries/python/envs/default/bin/python3 \
  references/crawl_screenshots.py --pages pages.json --base . --chrome

# 竖屏 9:16（抖音/TikTok）：
#   --w 1080 --h 1920
```

### Step 1.5 — 精选帧：关键产品图 + 归一化
两件事：
1. **抓站内关键产品/机器图**（可选，作点缀特写帧）：`references/crawl_images.py` 按 alt/cls 关键词打分、过滤 logo/banner、校验 JPEG。输出 `<base>/assets/<hash>.jpg`。
2. **归一化排序**：`references/normalize.py` 把"整页截图 + 关键图"按最终顺序拼成 `slides_sel/slide-01.png …`，统一 1920×1080 cover-crop（无变形）。

```bash
# 抓图（可选）
~/.workbuddy/binaries/python/envs/default/bin/python3 \
  references/crawl_images.py --pages pages.json --base .

# 排序归一化：frames.json 决定最终画面顺序
#   [{"label":"home","kind":"shot","file":"slide-home.png"},
#    {"label":"hero","kind":"img","file":"ab12cd-3f9a.jpg"}, ...]
~/.workbuddy/binaries/python/envs/default/bin/python3 \
  references/normalize.py --base . --manifest frames.json
```
> 精选配方：**先锁全部叙事/整页截图（kind:shot）排成主线，再用产品图（kind:img）填剩余 slot**。
> 站内产品图多为 450×450 缩略图，放大到 1920 会糊——只挑 ≥1280×720 的原图作点缀，主体用清晰整页截图。
> 最终通常 **13 帧左右（≤14）**，保证总时长 < 60s。

### Step 2 — 写解说词（AI 完成）
为 **每页写一句精炼营销英文**，朗读时长 **3–5 秒**，并**突出你想强调的卖点**（售前/售后、性价比、认证等）。
- 总时长必须 **< 60s**；单页 **3–5s**
- **TTS 计时陷阱**：把型号长数字逐字读出会严重超时（如 `"R F one zero zero zero"` ≈ 8s）。规则：**解说词里尽量不出现长型号**，用品类名代替（"axial inserter" 而非 "S3000"）；首版常跑出 5–7s/句、总时长 70s+，需二次收紧到 3–4s/句。
- 数字 / 网址读成可读形式（`smthelp.com` → `"smthelp dot com"`，`2011` → `"2011"` 可读）
- 输出 `narration.json`：JSON 字符串数组 `["sentence1","sentence2",...]`，**顺序与 frames.json 一致**

### Step 3 — 云端 TTS 合成 WAV
`references/gen_tts.py`：用 edge-tTs（默认 `en-US-AriaNeural` 自然女声）生成每页 44.1k 单声道 WAV，测出每页时长写入 `audio/durations.json`。

```bash
~/.workbuddy/binaries/python/envs/default/bin/python3 \
  references/gen_tts.py --narration narration.json --out audio
# 换男声:   --voice en-US-GuyNeural
# 换中文:   --voice zh-CN-XiaoxiaoNeural
```
> 若某页 > 5s：缩短那一句，只重跑 Step 3 即可（其余缓存不变）。
> 总时长若 > 60s：收紧句子或删到 ≤14 帧。

### Step 4 — ffmpeg 交叉淡入合成视频（含字幕 + BGM）
`references/build_video.py`：
- 每页尾部裁掉 xfade 时长（默认 0.4s）做无缝音频拼接
- 用 `xfade` 链做视频淡入淡出
- 支持 **PIL 烧字幕**：`--subtitles`（半透明黑底 + 居中自动换行白字）
  - `--bold` → 用 **Arial Bold**，小屏更清晰
  - `--subtitle-color R,G,B` → 字幕文字品牌色，如 `'10,165,165'` == **#0AA5A5**
  - `--accent-color R,G,B` → 字幕框左侧品牌色条（如 `'144,169,61'` 绿）
- 支持 **`--bgm PATH`** 叠加免费 BGM（低音量循环垫底，视频流 copy 不重编码，快）

```bash
# 推荐成品：粗体 + #0AA5A5 字幕 + 绿色色条 + 免费 BGM
~/.workbuddy/binaries/python/envs/default/bin/python3 \
  references/build_video.py --base . --out promo_final.mp4 \
  --subtitles --bold --subtitle-color 10,165,165 --accent-color 144,169,61 \
  --bgm audio/bgm.mp3

# 干净版（无字幕无 BGM）：
#   references/build_video.py --base . --out promo.mp4
```
最终视频时长 = `sum(每页时长) - (N-1) * xfade`，13 帧约 55s。

### Step 4.5 — 获取免费商用 BGM（CC BY，合规署名）
推荐 **ccMixter**（社区授权曲库，含 CC BY 商用安全轨）。筛选要点：**只要 `Attribution`（CC BY / BY-SA），排除 `NonCommercial` 与 `Sampling Plus`**（这两者不可商用）。

```bash
# 1) 搜候选（多标签扫，商用安全）
for tag in ambient instrumental electronic lofi chill; do
  curl -sL -A "Mozilla/5.0" "https://ccmixter.org/api/query?f=json&tags=$tag&limit=12&sort=score" -o /tmp/cc_$tag.json
done
# 2) 用 Python 过滤 license_name 含 'Attribution' 且不含 'NonCommercial'/'Sampling'，
#    取 files[0].file_name 结尾为 .mp3 的轨（见下方"踩坑"里的字段说明）
# 3) 下载直链格式： https://ccmixter.org/content/<user>/<file_name>.mp3
#    （带 -e "https://ccmixter.org/" referer；/content/media/files/<id>.mp3 会 404）
# 4) 存为 audio/bgm.mp3，并写 ATTRIBUTION.txt 保留 CC BY 署名（法律必需）
```
> 更省事：直接调用 `bgm-library` skill（`bgm search ...` / `bgm pick ...`），它自动处理 referer 与署名。注意它底层也是 ccMixter，曲库偏小，tech/corporate 标签多为 NonCommercial，多扫几个标签再挑 instrumental。

---

## 关键决策 / 踩坑记录（必读）

- **Chrome 非必需安装**：本环境未装 Chromium。Playwright 用 `launch(channel="chrome")` 驱动系统已有 Chrome，截图正常且无无头浏览器开销。
- **某页 `load` 事件不触发会挂死整轮** → 改用 `wait_until="commit"` + 每页硬超时（默认 25s）+ **已截图跳过**，并把"截图"与"抓图"解耦（两个脚本分开跑），互不阻塞。
- **xfade 输入标号**：多张图输入时，视频流是 `[t:v]`（t 为输入序号，从 0 起）；链首用 `0:v`。音频输入为 `{N}:a`（N = 图片输入数）。
- **edge-tTs 流式 API**：用 `async for chunk in comm.stream()` 收集 `chunk["type"]=="audio"` 的字节写 mp3，再 ffmpeg 转 wav（新版 `stream_to_file` 偶有兼容问题，流式更稳）。
- **字幕策略**：用 **PIL 烧字幕**（`--subtitles`），比 ffmpeg drawtext/libass 更可靠（homebrew ffmpeg 通常缺 libfreetype/libass）。**`--subtitles` 模式必须用 TTS venv 的 python3 跑**（该 venv 有 Pillow），否则 `ModuleNotFoundError: No module named 'PIL'`。
- **`--bold` 粗体**：默认字体 Arial.ttf，加 `--bold` 切到 Arial Bold.ttf（macOS 自带），小屏/手机端可读性明显更好。
- **品牌色字幕校验**：烧入 `#0AA5A5`(10,165,165) + 绿条(144,169,61) 后，用一行 PIL 统计 `slides_sub/` 里对应色像素数（teal>300px、green>150px 即 PASS）确认颜色真烧进去了，再交付。
- **BGM 混音正确性校验**：因人声与终混时长/裁切不同，直接比 RMS 会失真。正确做法——把纯人声 `voiceover.wav` 对齐裁到与终混同长，求差分信号 `final - voice`，再取**人声最安静的 1s 窗口**看差分 RMS：若明显 > 人声底噪，即证明 BGM 垫底成功。
- **ccMixter 字段坑**：API 返回的 `license` 顶层常为 None，真实许可在 `license_name`（如 `"Attribution (3.0)"` / `"Sampling Plus"`）。下载直链**不是** `/content/media/files/<id>.mp3`（404），而是 `https://ccmixter.org/content/<user>/<files[0].file_name>`；需带 `Referer: https://ccmixter.org/`。`lic=comm` 参数无效（报 "invalid license argument"），必须拉全量后自己按 `license_name` 过滤。
- **TTS 计时陷阱**：见 Step 2。把型号长数字逐字读会爆时长，首版常超 60s，需二次重跑 TTS（只重跑 Step 3，其余缓存不变）。
- **图片型页面无法肉眼预览**：用 `crawl_images.py` 按 alt/cls 关键词 + 尺寸打分筛选"视觉最丰富"的机器页填 slot。

---

## 可迭代升级点

| 需求 | 改法 |
|------|------|
| 换语言 / 音色 | Step 3 `--voice zh-CN-XiaoxiaoNeural` / `en-US-GuyNeural` 等 |
| 改文案 | 编辑 `narration.json` 后**只重跑 Step 3 + Step 4**，其余缓存不变 |
| 字幕粗体 + 品牌色 | Step 4 `--subtitles --bold --subtitle-color 10,165,165`（#0AA5A5） |
| 左侧品牌色条 | Step 4 `--accent-color 144,169,61` |
| 透明背景字幕 | Step 4 `--subtitles --bold --subtitle-color 46,204,113 --transparent-bg` |
| 加免费 BGM | Step 4 `--bgm audio/bgm.mp3`（CC BY 必需保留 ATTRIBUTION.txt） |
| 调 BGM 音量 | Step 4 `--bgm-volume 0.18`（默认 0.18，相对人声增益） |
| 竖屏 9:16 | Step 1 `--w 1080 --h 1920`，并重跑 Step 2/3/4 |
| 调时长 / 转场 | Step 4 `--xfade 0.5 --fps 25` |
| 换网站重做 | 改 `pages.json` + `frames.json` + `narration.json`，从头跑 Step 1–4 |
| 复杂动效（运动图形） | 装 Chromium 后切 HyperFrames 渲染；或数据驱动动画用 Remotion（`remotion-video-toolkit`） |

---

## 不适用

- 复杂转场 / 多轨精细混音 / 剪辑 → 剪映 / PR / 达芬奇
- 需要数据驱动的程序化动画 → Remotion（`remotion-video-toolkit` skill）

---

## 文件清单

```
website-to-promo-video/
├── SKILL.md
└── references/
    ├── crawl_screenshots.py  # Step 1: 网站整页截图 (Playwright+系统Chrome, 稳健超时)
    ├── crawl_images.py        # Step 1.5: 抓站内关键产品图 (关键词打分+校验)
    ├── normalize.py           # Step 1.5: 排序归一化 -> slides_sel/slide-NN.png
    ├── gen_tts.py            # Step 3: narration.json -> 每页 WAV + durations.json
    └── build_video.py       # Step 4: 图片+语音 -> 交叉淡入 MP4 (字幕/BGM)
```

## 一个完整 run 的项目目录结构（参考）

```
<project>/
├── pages.json            # [[label,url],...]
├── frames.json          # 最终画面顺序 [{label,kind,file}]
├── narration.json       # 解说词（与 frames 顺序一致）
├── slides/             # Step1 整页截图（原始）
├── assets/             # Step1.5 站内关键图
├── slides_sel/         # Step1.5 归一化帧
├── slides_sub/         # Step4 烧字幕后帧
├── audio/
│   ├── full/slide_NN.wav
│   ├── durations.json
│   └── bgm.mp3        # 免费 BGM（CC BY）
├── promo_final.mp4    # ★ 成品
└── ATTRIBUTION.txt    # BGM 署名（CC BY 必需）
```
