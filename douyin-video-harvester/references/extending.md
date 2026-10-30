# 扩展点（不改核心逻辑即可升级）

| 想做的事 | 改哪里 | 核心是否需改 |
|---|---|---|
| 新交付目标（S3、WebDAV、YouTube、NAS） | `dyh/sinks/<name>.py` 继承 `Sink`，实现 `existing_names()`、`upload()`，可选 `resolve()`；在 `sinks/__init__.py` REGISTRY 注册；config `sink.type` | 否 |
| 换排序权重 | config `rank.weights` | 否 |
| 新主题（如 feeder、AOI） | 新 config：关键词、命名规则写进 selection-guide 的附录 | 否 |
| 自动视觉分类（CLIP/多模态模型给候选打分） | 新模块读 `05_sheets/_frames/*.jpg`，输出 `07_selection.json` 草稿；挂到 cli 新子命令 | 只加子命令 |
| 其它平台（快手、B 站、TikTok） | 新 `scrape_<platform>.py` 输出同格式 01_awemes.json（aweme_id/desc/statistics/video.duration/video.bit_rate） | 否，后续阶段通用 |
| 后处理（转码、裁 Shorts、加水印） | 在 select 与 verify 之间加阶段，读写 08_final | 只加子命令 |

约定：新阶段只通过 `io.FILES` 中登记的文件读写；错误抛 `DyhError`（新码加到 errors.py）；日志用 `log.event(stage, event, **data)`；新增配置键要写默认值并更新 schema。
