# 核心流程（8 阶段）

| 阶段 | 命令 | 产物 | 时间（2 vCPU） | 关键点 |
|---|---|---|---|---|
| 0 环境 | `pipeline.sh setup` | env/、node_modules | 5 min | playwright 1.47.0（arm64）；所有依赖放 PROJ 下防沙箱清空 |
| 1 获取+提取 | `fetch`、`extract` | src/mesh.json、tree.json | 5 min | Hook WebViewer 原型拿到 viewer，getNodeMeshData |
| 2 机构理解 | 人工+AI（ana.py） | 机构说明、卖点表 | 20–40 min | bbox、剖视、分析图；写出驱动→传动→输出链；FAB 卖点 |
| 3 3D 引擎 | `pack` + 改 engine.js | model.b64 | 30–60 min | 分组、材质、运动、爆炸、锚点；缺失结构做示意并注明 |
| 4 配音 | 写 vo.json、`tts` | vo_timing.json | 5 min | 8–9 场景、约 230 词、95–130 s；数字写成可读形式 |
| 5 时间线 | 改 video.js、`preview l/p` | 联系表 | 30–60 min | 动作卡在关键词上；镜头连续；两种比例分别排版 |
| 6 渲染编码 | `render l`×N、`encode l`，p 同理 | 两个 MP4 | 每比例 1–2 h | 可续跑；先交付 HTML/缩略图/SEO |
| 7 周边 | `audio`、`srt`、`thumb`、SEO | 音频、SRT、缩略图、SEO | 15 min | −16 LUFS、闪避音乐；缩略图文字不压产品 |
| 8 落地页 | 改 landing.js、i18n、`landing` | 单 HTML | 30–60 min | 固定高度画布、懒加载、全语言、截图自测 |

交付：一次性给出全部文件（或上传 Drive），并提出可选修订项（重渲染成本）。
详细做法与坑点见 `SKILL.md`。
