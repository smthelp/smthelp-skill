---
name: smthelp-video-to-youtube
description: >
  为 Southern Machinery 产品创作营销/讲解视频（英文旁白 + 烧录英文字幕，素材来自本地产品视频），并发布到 Smthelping
  YouTube 频道。适用于产品宣传片、30 秒短视频、2-3 分钟全流程讲解视频（如散装/编带 Terminal 从供料到自动插件），
  以及任何需要本地渲染 + YouTube 上传的 B2B 设备视频任务。
whenToUse: >
  产品宣传视频，产品过程讲解视频，英文配音英文字幕视频，Bulk/编带 Terminal 供料自动插件流程视频，
  YouTube 上传发布，YouTube SEO 标题描述优化
metadata:
  source: hermes
  origin: "smthelp-video-to-youtube"
---

# smthelp-video-to-youtube

把本地产品素材做成可直接发布的 YouTube 视频：本地 html-video 工具链渲染（真实产品视频 + CSS 烧录字幕），
macOS `say` 合成英文旁白，最后通过 YouTube Data API v3 发布到 Smthelping 频道（UClX0iEG2bvJq8yUBEDamgDw）。

## 何时使用 / 路由

| 需求 | 走哪条路 |
|---|---|
| ≤30 秒单段宣传片 | 方式 A：单文件 HTML 模板渲染 |
| 2-3 分钟过程/讲解视频 | 方式 B：6×30s 分段渲染 + ffmpeg 拼接 |
| 发布到 YouTube | 方式 C：OAuth 授权 + 分块上传 + SEO 元数据 |

## 环境前提（本机已具备）

- html-video 工具链：`~/.workbuddy/tools/html-video`（已构建）。CLI：`node ~/.workbuddy/tools/html-video/packages/cli/dist/bin.js`。
- node 二进制路径会随版本目录变化（曾出现 `versions/22.22.2` → `22.22.2-2`）；**不要硬编码**，用 `node`（`~/.local/bin/node`）即可。
- ffmpeg/ffprobe、macOS `say`（Samantha 音色）、Playwright Chromium。
- 素材：SRT7001 产品目录文件夹中的产品视频/PDF（规格数字以项目 AGENTS.md 第 4 节为准）。
- YouTube 令牌：`~/.config/smthelp-yt/tokens.json`（含 refresh_token）；客户端凭证：`~/.config/smthelp-yt/credentials.json`（`{"client_id": "...", "client_secret": "..."}`，**不得入库**）。

## 关键约束（违反会导致返工）

1. **html-video 单段渲染硬上限 30 秒**（adapter 探测动画时长后 `Math.min(30, ...)`）。超过 30 秒必须拆成 30s 段分别渲染再拼接。
2. **本机 ffmpeg 无 libass/drawtext**：不能靠 ffmpeg 烧字幕。字幕必须在 HTML 模板里用 CSS opacity 动画烧录。
3. 竖屏素材（720×1280）必须裁成 16:9 背景：`scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080`。
4. 品牌色：teal `#00b3b0`（项目规范 teal `#009fa5` 系）与 lime `#82bf32`；字体 Archivo Black + Inter（Google Fonts）。
5. 型号事实：SRT7001 ≠ SRT7101；规格数字必须能在目录 PDF 中找到（0.8s/件、±0.5mm、10kg、连续 3 次缺料报警等）。
6. **发布边界**：YouTube 上传为公开外部变更，必须先获用户明确确认；频道归属以 `channels.list(mine=true)` 核验为准。

## 方式 A：≤30 秒宣传片

参考模板：`~/.workbuddy/tools/html-video/templates/srt7001-feeder-promo/`（六幕：Hook/痛点/框架/产品/循环/CTA）。

1. 写英文旁白（约 80 词/30s），按句分段合成并测量：
   `say -v Samantha -r 195 -o seg.aiff -f seg.txt` → 转 wav → `ffprobe` 测时长。
2. 生成单文件 index.html：CSS 场景窗口 + 字幕窗口（百分比按 30s 主时间轴换算），视频背景 `<video autoplay muted loop>`。
3. `project-create` → `project-set-template` → `project-render` 得到无声 MP4。
4. 混音：`ffmpeg -i silent.mp4 -i narration.wav -filter_complex "[1:a]apad=whole_dur=30[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k final.mp4`。
5. 质检：`ffprobe` 流信息 + 抽帧 `signalstats` YAVG（避免黑屏）+ 生成 contact sheet 给用户确认。

## 方式 B：2-3 分钟过程/讲解视频

以「散装/编带 Terminal 供料到自动插件全流程」为范例（6 段 × 30s）：

1. **选段**：按主题从素材视频均匀截取 4 段/段（如散装→震动盘、编带→卷盘裁切、供料器对接、自动插件+铆压、结果 CTA）。
2. **旁白**：每段 ~70-80 词，`say -r 160` 合成；再逐句合成以获得精确字幕时间戳（约 24 句）。
3. **生成 6 个模板**：`python3 scripts/gen_segment_templates.py spec.json`（spec 里含每段场景标题/标签/字幕时间/镜头文件；脚本会复制素材并生成 index.html + template.yaml 到模板库）。
4. **渲染+混音+拼接**：`bash scripts/render_and_assemble.sh`（逐段 project-create/set-template/render → 每段混入旁白 adelay=800,apad=30 → concat → 可选 BGM 低音量混入）。
5. **字幕文件**：输出完整 24 条 SRT（段偏移 = (段号-1)×30s）。
6. 质检同方式 A，另抽查每段起始帧亮度。

## 方式 C：上传 YouTube（Smthelping 频道）

1. **首次授权**（见 [references/youtube-oauth-setup.md](references/youtube-oauth-setup.md)）：
   - 先确认 `~/.config/smthelp-yt/credentials.json` 存在（用户提供 client_id/secret，不入库）。
   - `python3 scripts/yt_oauth.py` → 输出授权 URL → 浏览器打开 → 用户允许 → 令牌自动保存。
   - scope 必须同时含 `youtube.upload` + `youtube.force-ssl`（否则无法核验频道）。
2. **核验频道**：上传前必须 `channels.list(mine=true)` 且 id == `UClX0iEG2bvJq8yUBEDamgDw`；不符则停下，提示用户用 Smthelping 所属账号重新授权（OAuth 上传到账号默认频道）。
3. **上传**：`python3 scripts/yt_upload.py --video <mp4> --title "..." --description "..." --tags "a,b,c" --privacy public`。脚本会刷新令牌（access_token 会过期，**每次都刷新**）、分块上传、回读核验。
4. SEO 元数据：标题含主关键词（型号 + 品类），**必须 ≤100 字符**（YouTube 标题硬上限，超出报 invalidTitle 400）；描述含章节时间轴 + 规格要点 + 联系方式（info@smthelp.com / smthelp.com / WhatsApp）+ hashtags；categoryId 28，madeForKids false。

## 验证清单（交付前）

- [ ] `ffprobe`：h264 + aac、目标时长、1920×1080
- [ ] 抽帧亮度非黑、字幕可见（contact sheet）
- [ ] 上传后回读：channelId、title、privacy 与预期一致
- [ ] 未发布前先给用户确认成片；上传公开视频前再次确认
