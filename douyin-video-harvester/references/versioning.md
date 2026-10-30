# 版本与发布
- 语义化版本：`VERSION` 与 `dyh/__init__.py` 同步。修 bug = patch；新增阶段/sink/配置键（向后兼容）= minor；改文件布局、配置键含义、CLI 参数 = major。
- 升级：`python3 scripts/bump_version.py minor "add webdav sink"` → 补全 changelog → 跑 `python3 -m unittest discover -s tests` → 提交 → 打 tag `douyin-video-harvester-vX.Y.Z`。
- 用户反馈写入 `feedback-log.md`（日期、反馈原话、改动、版本）。
