# 可配置参数（product.json）

完整约束见 `config/product.schema.json`，示例见 `config/product.example.json`。`scripts/cfg.py` 把配置转成环境变量供 `pipeline.sh` 使用。

| 路径 | 环境变量 | 默认 | 作用 / 调参建议 |
|---|---|---|---|
| product.code | CODE | PRODUCT | 所有输出文件名前缀 |
| inputs.drawing / landing | DRAWING_URL / LANDING_URL | — | fetch 阶段下载到 src/ |
| inputs.landing_insert_before | — | hero 之后 | build_landing.py 中的插入锚点 |
| voice.voice | VOICE | en-US-AndrewMultilingualNeural | 任意 edge-tts 声音（如 en-GB-RyanNeural） |
| voice.rate | VOICE_RATE | +2% | 语速；改动后需重跑 tts → preview → render |
| video.fps | FPS | 24 | 24 足够；30 会增加 25% 渲染时间 |
| video.render_scale_3d | R3D | 0.67 | 3D 层内部分辨率比例；1.0 最清晰但慢约 2×；文字层始终 4K 原生 |
| video.shards | SHARDS | 2 | 并行渲染进程数（2 vCPU 下 2 最优），相差 15 s 启动 |
| video.chunk_seconds | CHUNK | 1150 | 单次渲染预算，须 < 后台 1200 s 上限 |
| video.segments | NSEG | 8 | 编码分段数，每段需 < 20 分钟 |
| video.crf | — | 17 | 画质；YouTube 4K 建议 16–20 |
| landing.languages / i18n_file | — | 页面全部语言 | 新增文案必须覆盖页面已有的每种语言 |
| landing.dpr_max | — | 1.75 | 移动端性能 |
| brand.* | — | 南方机械品牌色 | teal #00A896/#00C2AD、navy #0B132B、amber #F5B13D |
| thumbnail.camera | — | 见示例 | 缩略图机位（target/dist/az/el/sx） |
| delivery.drive_folder_id / subfolder | DRIVE_FOLDER / DRIVE_SUBFOLDER | — | 交付上传位置 |

## 产品相关参数（目前在代码中，v2.x 将并入配置）
- `pack.py`：零件 id → 组名映射、坐标原点、量化范围 S。
- `engine.js`：材质映射、运动组与轴（枢轴/行程或振动/物料流路径）、EXPLODE 偏移表、ANCHORS 标注点、道具。
- `video.js`：场景 id 与 vo.json 对应、镜头关键帧（target, dist, az, el, fov, sx, sy）、标注与文案。
- `landing.js`：STEPS（导览步骤、机位、标签）、stepState。
