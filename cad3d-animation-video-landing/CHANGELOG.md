# CHANGELOG

## v2.0.0 — 2026-10-21 · 标准化模块
- Added: `README.md` 快速上手；`docs/IO_SPEC.md`、`docs/CONFIG.md`、`docs/WORKFLOW.md`、`docs/VERSIONING.md`。
- Added: `config/product.schema.json` + `product.example.json` 统一产品配置；`scripts/cfg.py` 配置→环境变量；
  `scripts/pipeline.sh` 分阶段一键驱动（setup → landing），全部可续跑。
- Added: `examples/sbf1001/`（大装配体、流程动画）与 `examples/cn-sm-2713/` 完整产品代码，作为新产品起点。
- Changed: `tts.py` 支持 VOICE / VOICE_RATE；`run_render.sh` 支持 FPS；`VERSION` 文件。
- 兼容性：v1.x 项目可继续用原脚本；新项目建议放 `product.json` 并用 `pipeline.sh`。

## v1.1.0 — 2026-10-20 · SBF1001 振动盘送料器
- Added: 未命名零件的 bbox + 编号分析图分类法（ana.py / ana.js）；CAD 缺失结构的示意画法并在页面注明。
- Added: 3D 渲染目标 R3D≈0.67 放大 + 4K 原生文字层；`SHARD=k/n` 分片并行渲染；`enc_all.sh` 续跑编码；输出名取 CODE。
- Added: 非 Tailwind 落地页合并（页面 CSS 变量 + 合并 I18N + 包装 applyLang）。
- Lessons: 10 万三角面在 SwiftShader 下需 MeshStandard；只引用落地页已有参数，不引用 CAD 机架尺寸。

## v1.0.0 — 2026-10-19 · CN-SM-2713 JUKI 夹爪吸嘴
- 首版：eDrawings 网格提取、共享 Three.js 引擎（运动学、爆炸、剖切、高亮）、逐词同步 4K 时间线（16:9 + 9:16）、
  edge-tts 配音、音乐、SRT、缩略图、SEO、7 语言落地页合并。
