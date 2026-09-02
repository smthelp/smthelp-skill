---
name: html-video-product-promo
description: "把公司产品落地页快速转成 30 秒英文产品宣传视频（画面 + 字幕 + 旁白）。 依赖本地已安装的 html-video 工具链（nexu-io/html-video）和 macOS say 离线 TTS。"
whenToUse: "生成产品宣传视频，产品页转视频，产品展示视频，产品落地页视频，生成带字幕和语音的视频，product promo video，product showcase video，landing page to video"
metadata:
  source: workbuddy
  origin: "html-video-product-promo"
---
# html-video-product-promo

把公司产品落地页转成 30 秒英文产品宣传视频。

## 何时使用

- 用户给出某个公司产品落地页 URL，要求生成带英文语音/字幕的展示视频。
- 没有 MiniMax/OpenAI/ElevenLabs TTS key，需要可立即交付的离线英文配音。
- 想复用 html-video 的 Hyperframes 渲染链路 + 纯 CSS 动画模板。

## 前置依赖（本机必须已装好）

- `~/.workbuddy/tools/html-video`：已 clone / pnpm install / pnpm -r build。
- Playwright Chromium（build 需与 adapter 实际解析版本一致，通常是 1234）。
- `ffmpeg` + `ffprobe`。
- macOS `say`（英文 TTS，默认用 `Samantha` 音色）。
- `claude` CLI 已登录（用于 `html-video studio` 的 AI 链路；本纯模板渲染流程可不用，但建议就绪）。

## 完整工作流

### 1. 提取产品信息

用 WebFetch 读取落地页，提取：

- 产品名 / 型号
- 核心卖点 / 关键规格
- 目标行业 / 应用
- 品牌定位语 / CTA

### 2. 写英文旁白脚本

约 80 词、30 秒、B2B 营销口吻。结构：

1. Hook：点出目标客户的痛点
2. Solution：产品名 + 定位
3. Proof：3 个核心卖点/规格
4. Range：产品组合（如有）
5. CTA：官网 / 邮箱

### 3. 合成旁白并测时长

```bash
WDIR=/Users/jasonwu/WorkBuddy/<date>/sme_video
say -v Samantha -r 200 -o "$WDIR/narration.aiff" -f "$WDIR/narration.txt"
ffmpeg -y -i "$WDIR/narration.aiff" "$WDIR/narration.wav"
D=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$WDIR/narration.wav")
```

### 4. 创建 html-video 单文件模板

目录：`~/.workbuddy/tools/html-video/templates/<name>/`

文件：

- `template.html-video.yaml`：

```yaml
id: <name>
name: <Product> Promo
description: <short desc>
engine: hyperframes
composition:
  type: single-file
  src: index.html
inputs:
  schema: {}
```

- `index.html`：1920×1080 单页，用 CSS keyframes 控制 6 场景时间线：

```css
/* scene1: 0-5s, scene2: 5-11s, scene3: 11-18s, scene4: 18-24s, scene5: 24-29s, cta: 29-30s */
.scn1 { opacity: 0; animation: show 30s linear 0s forwards; }
.scn2 { opacity: 0; animation: show 30s linear 5s forwards; }
...
```

字幕也作为场景元素之一，用 `opacity` 切换（不能用 `display:none`，CSS 动画对其无效）。

### 5. 渲染无声视频

```bash
cd ~/.workbuddy/tools/html-video
NODE=/Users/jasonwu/.workbuddy/binaries/node/versions/22.22.2/bin/node
BIN=packages/cli/dist/bin.js
$NODE $BIN project-create --name "<project>"
$NODE $BIN project-set-template <project_id> --template <template_name>
$NODE $BIN project-render <project_id> --output <WDIR>/silent.mp4
```

### 6. 混音得到最终 MP4

```bash
cd <WDIR>
ffmpeg -y -i silent.mp4 -i narration.wav \
  -filter_complex "[1:a]apad=whole_dur=<D>[a]" \
  -map 0:v -map "[a]" \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart \
  final.mp4
```

### 7. 验证

```bash
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name -of default=noprint_wrappers=1 final.mp4
ffmpeg -ss <t> -i final.mp4 -frames:v 1 frame.png
```

确认含 h264 视频 + aac 音频，字幕已烧入画面。

## 已知坑与解法

1. **pnpm/corepack 卡死**：html-video 仓库写死 `packageManager: pnpm@9.15.0`，若系统 corepack 没缓存该版本且代理没传过去，会无限卡死。解决：`corepack prepare pnpm@9.15.0 --activate`，并确保 `HTTPS_PROXY`/`HTTP_PROXY` 在构建/下载命令环境里。
2. **Playwright 浏览器版本错位**：`pnpm exec playwright install` 可能按根目录 playwright 1.61.0 装 1228 构建；但 adapter-hyperframes 运行时解析到 1.62.1，期望 1234 构建。解决：给 `node_modules/.pnpm/playwright@1.62.1/.../cli.js install chromium chromium-headless-shell`。
3. **ffmpeg 无 libass**：macOS 自带 ffmpeg 通常未编译 `subtitles`/`ass` 滤镜。解法：把字幕直接做到 html-video 模板里 CSS 动画烧入，不依赖 ffmpeg 字幕滤镜。
4. **CSS `display:none` 不响应动画**：字幕元素默认态用 `opacity:0`，动画切 `opacity:1`。
5. **长任务别用 `nohup &` + `sleep` 轮询**：会被后续命令/超时误杀。用工具托管的 `run_in_background`。

## 交付物

- `final.mp4`：1920×1080，~30 秒，h264+aac，字幕烧入画面。
- `narration.txt`：英文旁白脚本。
- `subtitles.srt`：备用字幕文件。

## 注意事项

- 对外发布前必须经 Jason 确认，机仔不会擅自上传到社媒/官网。
- 配音为 macOS 离线合成音；若有 MiniMax/OpenAI/ElevenLabs key，可替换为更自然的人声 TTS。
- 本工作流仅渲染画面，不调用 html-video 的 AI agent 生成链路；如需 AI 生成动画脚本，需确保 `claude` 已登录或设 `ANTHROPIC_API_KEY`。
