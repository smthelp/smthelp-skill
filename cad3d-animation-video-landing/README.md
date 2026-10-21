# cad3d-animation-video-landing · v2.0.0

把产品 3D 图（SolidWorks eDrawings / HOOPS HTML）一次性转化为：

1. **交互式机构动画**，合并进现有产品落地页，输出一个全新的单文件 HTML（多语言、可旋转、自动导览）
2. **4K YouTube 营销视频**：16:9 主视频 + 9:16 Shorts，英文 AI 配音、逐词高亮烧录字幕、背景音乐
3. **YouTube 缩略图**（1280×720 JPG + 4K PNG）
4. **SEO 文案**：标题、描述、章节、标签、Shorts 标题；以及每个比例的 SRT 字幕

已用于：CN-SM-2713 JUKI 定制夹爪吸嘴（v1.0）、SBF1001 振动盘送料器（v1.1）。

## 目录结构

```
cad3d-animation-video-landing/
├── README.md            ← 本文件：快速上手
├── SKILL.md             ← 给 AI Agent 的完整操作手册（流程、质量门槛、坑点）
├── VERSION              ← 当前版本号（semver）
├── CHANGELOG.md         ← 版本记录
├── config/
│   ├── product.schema.json   ← 产品配置的 JSON Schema（参数说明、取值范围、默认值）
│   └── product.example.json  ← 配置示例（SBF1001）
├── docs/
│   ├── IO_SPEC.md       ← 输入输出规范、文件命名、技术规格
│   ├── CONFIG.md        ← 可配置参数一览与调参建议
│   ├── WORKFLOW.md      ← 8 个阶段的核心流程与每阶段产物
│   └── VERSIONING.md    ← 版本与迭代机制（如何升级、发布、同步）
├── scripts/             ← 通用流水线脚本（复制到 <PROJ>/build/）
│   ├── pipeline.sh      ← 一键分阶段驱动（setup/fetch/extract/pack/tts/preview/render/encode/audio/srt/thumb/landing）
│   ├── cfg.py           ← 读取 product.json → 环境变量
│   ├── setup_env.sh  extract_mesh.py  ana.py/ana.js  loader.js  mkpage.py  preview.py
│   ├── render.py  run_render.sh  encode.py  enc_all.sh  audio_mix.py  tts.py  make_srt.py  thumb.py
│   └── pack.py  engine.js  video.js  landing.js  build_landing.py   ← 通用模板（产品相关，需改写）
├── references/          ← 机构分析范例
└── examples/
    ├── cn-sm-2713/      ← 夹爪吸嘴：小零件、命名完整、运动学（柱塞+摆动夹爪）
    └── sbf1001/         ← 振动盘：大装配体、零件未命名、流程类动画（物料流+振动+吹气+光纤）
```

## 快速开始（新产品）

```bash
PROJ=/workspace/projects/<proj>/<code>; mkdir -p $PROJ/build
cp -r scripts/* $PROJ/build/                         # 通用脚本
cp examples/<最接近的产品>/* $PROJ/build/             # 产品相关模板，作为起点
cp config/product.example.json $PROJ/product.json    # 修改 code / 输入 URL / 参数
cd $PROJ/build
bash pipeline.sh setup && bash pipeline.sh fetch && bash pipeline.sh extract
# ▶ 机构分析（人工 + AI）：读 bbox、渲染分析图，改写 pack.py / engine.js（分组、运动、爆炸、锚点）
bash pipeline.sh pack
# ▶ 写 vo.json 配音脚本，改写 video.js 场景与镜头
bash pipeline.sh tts && bash pipeline.sh preview l && bash pipeline.sh preview p   # 看联系表，修正遮挡
bash pipeline.sh landing                         # 落地页（改写 landing.js + i18n json + build_landing.py 插入点）
bash pipeline.sh audio && bash pipeline.sh srt && bash pipeline.sh thumb
bash pipeline.sh render l   # 反复执行直到 "have N of N"（每次 ≤ 20 分钟）
bash pipeline.sh encode l   # 再对 p 做一遍 render/encode
```

产物全部在 `$PROJ/deliverables/`，规范见 `docs/IO_SPEC.md`。

## 哪些是通用的，哪些要按产品改

| 通用（只改配置） | 按产品改写（从 examples 起步） |
|---|---|
| 环境、网格提取、打包格式、渲染/分片/续跑、编码、混音、SRT、缩略图框架、SEO 结构 | 零件分组（pack.py）、材质/运动/爆炸/锚点（engine.js）、场景与镜头（video.js）、导览步骤（landing.js）、文案与 i18n、落地页插入点 |

下一版路线图（v2.x）：把 engine/video/landing 的产品参数也抽到 `product.json`，做到新产品只改配置。

## 维护
修改方法后：更新 `VERSION`、`CHANGELOG.md`、SKILL.md 头部 `version`，并同步 Agent skill、工作区副本、GitHub、Google Drive（见 `docs/VERSIONING.md`）。
