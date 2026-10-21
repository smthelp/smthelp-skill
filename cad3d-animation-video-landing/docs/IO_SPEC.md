# 输入 / 输出规范（v2.0.0）

## 1. 输入

| # | 输入 | 必需 | 格式 | 说明 |
|---|---|---|---|---|
| 1 | 3D 图 | 是 | eDrawings / HOOPS Communicator 单文件 HTML（URL 或本地） | 模型以 base64 SCS 内嵌；通过无头 Chromium 驱动 viewer 提取网格，不直接解析。STEP/GLB 在路线图中 |
| 2 | 现有落地页 | 是 | 单文件 HTML（URL 或本地） | 支持 Tailwind 页（CN-SM-2713）和自定义 CSS 变量页（SBF1001）；需有 i18n 对象 |
| 3 | 插入锚点 | 否 | HTML 片段字符串 | 3D 区块插入位置，默认 hero 之后 |
| 4 | 卖点依据 | 是 | 落地页文字 / 用户确认 | **只用**落地页已写明、CAD 可见或用户确认的参数，禁止编造 |
| 5 | 配音语言、频道、站点 | 否 | product.json | 默认英文、youtube.com/c/Smthelping、www.smthelp.com |
| 6 | 交付位置 | 否 | Google Drive 文件夹 ID | 自动建产品子文件夹上传 |

## 2. 输出（`$PROJ/deliverables/`）

| 文件 | 规格 |
|---|---|
| `<landing-slug>-3d.html` | 单文件，内嵌 Three.js + 量化网格（base64 gzip），约 1–3 MB；原页全部内容保留；新增 3D 区块（自动导览、标签页、拖拽旋转、速度/开合滑块、功能卡片、参数表、CTA）；页面全部语言同步；懒加载，DPR ≤ 1.75 |
| `<CODE>_4K_16x9.mp4` | 3840×2160，24 fps，H.264 High CRF17，AAC 320k，faststart，时长 1–3 min |
| `<CODE>_4K_9x16_Shorts.mp4` | 2160×3840，其余同上 |
| `<CODE>_thumbnail_4K.png` / `<CODE>_YouTube_thumbnail_1280x720.jpg` | 16:9；JPG < 2 MB；大字 + 产品 + Logo，文字不压产品 |
| `<CODE>_16x9_EN.srt` / `<CODE>_9x16_EN.srt` | UTF-8 SRT，与烧录字幕同一分句与时间 |
| `<CODE>_YouTube_SEO.txt` | 标题 ≤ 70 字符；描述（痛点→方案→要点→章节→链接→话题标签）；章节首条 0:00、每段 ≥ 10 s；标签 ≤ 500 字符；Shorts 标题 ≤ 60 字符含 #shorts |

## 3. 中间产物（`$PROJ/`）

`src/mesh.json`（世界矩阵+顶点+法线）、`src/tree.json`（装配树）、`build/model.b64`、`build/audio/vo_timing.json`（逐词时间）、
`build/timeline_l|p.json`（场景与字幕分句）、`frames_l|p/NNNNN.jpg`（可续跑）、`enc/*.mp4`（分段）。

## 4. 验收标准
- 机构运动方向、分组经剖视图验证；爆炸无悬浮/穿插。
- 每条参数可追溯；示意性元素（CAD 中没有的部件、强调色）在页面上注明。
- 两种比例联系表无文字/产品/字幕互相遮挡。
- ffprobe 分辨率、音轨、时长正确；落地页可加载、导览运行、切换语言正常、控制台无错误（被墙 CDN 除外）。
