---
name: pptx-to-promo-video
description: "把产品介绍 PPTX/PDF 逐页解析，生成专业英文解说词，用云端免费 TTS 合成自然语音，再用 ffmpeg 交叉淡入淡出合成 60 秒内的产品宣传视频。适用于产品手册、营销文档、培训材料快速转短视频。"
metadata:
  source: workbuddy
  origin: "pptx-to-promo-video"
---
# 文档转宣传视频 (Doc → Promo Video)

把一份产品介绍 PPTX / PDF，做成 **60 秒以内、逐页解说、带自然英文语音** 的宣传短视频。
保留原始页面与图片，用 ffmpeg 交叉淡入淡出做平滑转场 —— 无需 Chrome / 无需剪映。

> 信条：好的视频不是堆特效，是信息传达的效率。页面本身已承载细节，语音只做"点睛"引导。

---

## 适用场景

- 产品手册 / 公司介绍 PPTX / 方案 PDF → 社媒宣传片（LinkedIn、YouTube、官网）
- 每页 3–5 秒，逐页配英文自然语音解说
- 快速批量产出，可迭代（改文案只重跑 TTS，改转场只重跑合成）

## 前置依赖（先检查）

```bash
which soffice libreoffice pdftoppm ffmpeg ffprobe
# 预期都能找到；soffice 在 /opt/homebrew/bin/soffice 或 /Applications/LibreOffice.app/...
```

| 工具 | 用途 |
|------|------|
| `soffice` / `libreoffice` | PPTX → PDF |
| `pdftoppm` | PDF → 每页 PNG |
| `ffmpeg` / `ffprobe` | 视频合成、时长测量 |
| `python3` + `edge-tts` | 云端 TTS（Microsoft 免费，en-US-AriaNeural 自然音） |
| `Arial.ttf` | 烧字幕时使用（默认路径 macOS 系统字体） |
| `Pillow` (Python) | 烧字幕依赖（`pip install Pillow` 到 TTS venv） |

`edge-tts` 安装（隔离 venv，勿污染系统）：
```bash
python3 -m venv ~/.workbuddy/binaries/python/envs/default
~/.workbuddy/binaries/python/envs/default/bin/pip install -q edge-tts
```

---

## 工作流程（4 步，每步可独立重跑）

### Step 1 — 渲染页面为 1920×1080 PNG
`references/extract_slides.py` 完成三件事：
1. PPTX → `soffice --headless` 转 PDF（若输入已是 PDF 则跳过）
2. `pdftoppm -r 150` 导出每页 PNG
3. `ffmpeg scale+crop` 统一为 1920×1080，零填充命名为 `slide-01.png` … `slide-NN.png`

```bash
python3 references/extract_slides.py path/to/doc.pptx --out slides_1080
# 竖屏: --w 1080 --h 1920   (抖音 9:16)
```

### Step 1.5 — 分析与精选页面（PPTX / 图片型 PDF 必做）

源文档往往远多于 13 页，且分两类：

**A. 文本/叙事页**（必须保留）：承载产品故事主线。
- PDF：用 `pdftotext -f N -l N doc.pdf -` 逐页看字符数，定位有文字的页。
- **PPTX 特例**：渲染出的 PDF 文本层可能为空（文字在 PPTX XML 里，不在光栅化页面里）。用：
  ```bash
  python3 references/extract_pptx_text.py doc.pptx --slides slides_1080
  ```
  它会从 XML 抽每页真实文字，并**自动交叉校验渲染页数**：若 `Rendered PNGs >> PPTX text slides`（如 29 vs 10），说明 soffice 导出畸形——多出来的页是纯图片的机器/产线照片，不是新内容。
- **畸形导出必读**：`pdfinfo` 报的页数不可信，以 `pdftoppm` 实际渲染出的 PNG 数为准。保留全部真实叙事页即可，多余图片页交给下面的 profiling 挑。

**B. 图片/机器页**（填剩余 slot）：图片型文档（如自动化方案册）可能 6–29 页都是机器/产线图，模型无法肉眼预览。用 PIL 做数据化筛选：
```bash
~/.workbuddy/binaries/python/envs/default/bin/python3 references/profile_slides.py slides_1080 --keep 8
```
输出每张页的 `detail`（灰度标准差，照片/图纸高、空白低）、`color%`（饱和像素占比，挑真实照片）、`hue`（主色相，可识别品牌色）、`blank`、`dups`（感知哈希近重复），并给出"视觉最丰富"的机器照片候选列表。
> 精选配方：**先锁死全部叙事/文本页，再用 photo candidates 填剩余 slot**。复制到 `slides_sel/`：`cp slides_1080/slide-PP.png slides_sel/slide-NN.png`（NN 从 01 连续编号，对应 narration 顺序）。

精选后通常 **13 页左右**（≤14），保证总时长 < 60s。

### Step 2 — 写解说词（AI 完成）
读取页面文本（PPTX 内 `<a:t>` 提取，或看渲染图），为 **每页写一句精炼营销英文**，朗读时长控制在 **3–5 秒**。
- 总时长必须 **< 60s**；单页 **3–5s**
- **TTS 计时陷阱**：把型号数字逐字读出会严重超时（如 `"R F one zero zero zero"` ≈ 8s，`"E six four zero three"` 同理）。规则：**解说词里尽量不出现长型号**，用品类名代替（"axial inserter" 而非 "S3000"），或只保留极短代号；首版常跑出 5–7s/句、总时长 70s+，需二次收紧到 3–4s/句。
- 数字 / 网址读成可读形式（如 `smthelp.com` → `"smthelp dot com"`，`1.67` → `"one point six seven"`）
- 输出 `narration.json`：JSON 字符串数组 `["sentence1", "sentence2", ...]`

### Step 3 — 云端 TTS 合成 WAV
`references/gen_tts.py`：用 edge-tts（默认 `en-US-AriaNeural` 自然女声）生成每页 44.1k 单声道 WAV，测出每页时长写入 `audio/durations.json`。

```bash
python3 references/gen_tts.py --narration narration.json --out audio
# 换男声:   --voice en-US-GuyNeural
# 换中文:   --voice zh-CN-XiaoxiaoNeural
```

> 若某页 > 5s：缩短那一句，只重跑 Step 3 即可（其余缓存不变）。

### Step 4 — ffmpeg 交叉淡入合成视频
`references/build_video.py`：
- 每页尾部裁掉 xfade 时长（默认 0.3s）做无缝音频拼接
- 用 `xfade` 链做视频淡入淡出
- 输出 H.264 MP4（含 AAC 音轨）

```bash
# 基础模式（无字幕）
python3 references/build_video.py --base . --out promo.mp4

# 带英文字幕（PIL 烧入画面，需 venv python + Pillow）
~/.workbuddy/binaries/python/envs/default/bin/python3 references/build_video.py --base . --out promo_sub.mp4 --subtitles

# 字幕参数调优
--subtitle-size 48    # 字号（默认 52，长句可缩小）
--fontfile /path/to/Font.ttf   # 指定其他 TTF
```

最终视频时长 = `sum(每页时长) - (N-1) * xfade`，14 页约 52s。

---

## 关键决策 / 踩坑记录（必读）

- **Chrome 非必需**：HyperFrames 渲染依赖 Chrome，本环境未安装。改用 `ffmpeg xfade`，效果等价且更快，且无无头浏览器开销。
- **xfade 输入标号**：多张图输入时，视频流是 `[t:v]`（t 为输入序号，从 0 起）；链首用 `0:v`。音频输入为 `{N}:a`（N = 图片输入数）。
- **pdftoppm 命名非数字序**：`slide-10.png` 会排在 `slide-2.png` 前（字典序）。脚本必须按文件名数字提取再重命名为零填充 `slide-01.png`，否则顺序错乱。
- **edge-tts 流式 API**：用 `async for chunk in comm.stream()` 收集 `chunk["type"]=="audio"` 的字节写 mp3，再 ffmpeg 转 wav（新版 edge-tts 的 `stream_to_file` 偶有兼容问题，流式更稳）。
- **路径拼接**：脚本统一用 `base` + 相对目录拼接，避免音频写到意料外目录（曾踩过 cwd 相对路径把文件写到项目根而不是子目录的坑）。
- **字幕策略**：支持 **PIL 烧字幕**（`--subtitles`），用 Pillow 把英文解说文字合成到每张幻灯片底部（半透明黑底+白字，自动换行居中）。比 ffmpeg drawtext 更可靠（homebrew ffmpeg 通常缺 libfreetype/libass）。**注意**：`--subtitles` 模式必须用 **TTS venv 的 python3** 运行 build_video.py（该 venv 有 Pillow），否则报 `ModuleNotFoundError: No module named 'PIL'`。
- **PPTX 文本层为空 + 畸形导出**：PPTX 渲染成 PDF 后 `pdftotext` 可能读不到文字（文字在 XML）。用 `extract_pptx_text.py` 从 XML 抽真实文字；它还会交叉校验 `pdfinfo 页数 vs pdftoppm 渲染页数`，若后者远大于前者即畸形导出（多余页是纯图片）。一律以渲染出的 PNG 数为准选页。
- **图片型文档无法肉眼预览**：方案册/手册常 20–29 页全是机器照片。用 `profile_slides.py`（PIL：detail/color%/hue/blank/dups）选出"视觉最丰富"的机器页填 slot，先锁叙事页再填照片页。
- **TTS 计时陷阱**：把型号长数字逐字读会爆时长（如 "RF1000"≈8s）。解说词避开长型号、用类型名代替，收紧到 3–4s/句；首版常超 60s，需二次重跑 TTS（只重跑 Step 3，其余缓存不变）。
- **品牌色字幕校验**：烧入 teal(0,163,180)+green(144,169,61) 后，用一行 PIL 统计 `slides_sub/` 里 teal/green 像素数（teal>500px、green>200px 即 PASS）确认颜色真烧进去了，再打包交付。

---

## 可迭代升级点

| 需求 | 改法 |
|------|------|
| 换语言 / 音色 | Step 3 `--voice zh-CN-XiaoxiaoNeural` / `en-US-GuyNeural` 等 |
| 加英文字幕 | Step 4 `--subtitles`（需 venv python + Pillow）；字号 `--subtitle-size 48` |
| 字幕配品牌色 | Step 4 `--subtitles --subtitle-color 0,163,180 --accent-color 144,169,61`（teal 文字 + green 左侧色条，参考 Southern Machinery logo 配色；先用 PIL 分析 logo PNG 取主色） |
| 透明背景字幕 | Step 4 `--subtitles --transparent-bg --subtitle-color 46,204,113`（**不加**黑底框/色条，只画文字+细黑描边保可读性；用户要"透明背景字幕"时用此开关） |
| 加 BGM | `ffmpeg -i promo.mp4 -i bgm.mp3 -filter_complex "[0:a][1:a]amix=inputs=2[a]" -map 0:v -map "[a]" -shortest out.mp4`（BGM 用免费商用，如 Pixabay） |
| 竖屏 9:16 | Step 1 `--w 1080 --h 1920` |
| 调时长 / 转场 | Step 4 `--xfade 0.5 --fps 25` |
| 多文档批量 | 循环调用 4 步，输出按文档分目录 |
| 复杂动效（GSAP 运动图形） | 装 Chromium 后切换 HyperFrames 渲染管线；或可程序化数据动画用 Remotion |

---

## 不适用

- 复杂转场 / 多轨混音 / 精细剪辑 → 剪映 / PR / 达芬奇
- 需要数据驱动的程序化动画 → Remotion（见 `remotion-video-toolkit` skill）

---

## 文件清单

```
pptx-to-promo-video/
├── SKILL.md
└── references/
    ├── extract_slides.py   # Step1: PPTX/PDF -> 1920x1080 PNG
    ├── extract_pptx_text.py# Step1.5: 从 PPTX XML 抽每页文字 + 校验畸形导出
    ├── profile_slides.py   # Step1.5: PIL 分析渲染图，挑视觉最丰富的机器页
    ├── gen_tts.py          # Step3: narration.json -> 每页 WAV + durations.json
    └── build_video.py      # Step4: 图片 + 音频 -> 交叉淡入 MP4 (可选烧字幕)
```
