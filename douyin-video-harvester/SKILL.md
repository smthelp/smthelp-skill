---
name: douyin-video-harvester
description: 从指定抖音主页抓取全部作品，按互动分数排序，关键词初筛 + 画面人工/Agent 审核选出 N 条主题相关视频（如 SMT 吸嘴），下载、去重、校验，用英文 SEO 文件名交付到 Google Drive 或本地，并生成清单 CSV。Use when the user gives a Douyin profile URL and wants the top / on-topic videos downloaded and delivered.
version: 1.0.0
---

# douyin-video-harvester

抖音主页 → 精选 N 条主题视频 → 英文 SEO 文件名 → Drive/本地交付 + 清单。

## 输入
| 项 | 必填 | 说明 |
|---|---|---|
| 主页 URL 或 sec_uid | 是 | `https://www.douyin.com/user/<sec_uid>` |
| cookies.txt | 是 | 登录 douyin.com 后导出的 Netscape 格式；程序只读取抖音域名的 cookie |
| 主题关键词 | 否 | `filter.include_keywords` / `exclude_keywords`（文本初筛） |
| 已交付清单 | 否 | 以前批次的 CSV（`aweme_id` 列），避免重复 |
| 数量 N | 否 | `select.count`，默认 20 |
| 交付目标 | 否 | `sink`: `local` 或 `gdrive_gws`（folder_id） |

## 输出（`runs/<run_name>/`）
`01_awemes.json` 原始作品 → `02_ranked.json` 排序 → `03_candidates.json` 候选 → `04_videos/` 原片 → `05_sheets/` 联系表 → `06_dupes.json` → `07_selection.json`（审核闸门）→ `08_final/` 重命名成片 → `09_verify.json` → `10_upload.json` + `manifest.csv` + `run.log.jsonl`。详见 `references/io-spec.md`。

## 流程（每步独立、可重跑）
1. `bash scripts/setup.sh` 安装依赖（chromium、ffmpeg、imagemagick、playwright、yt-dlp）。
2. 复制 `config/config.example.json`，填 `run_name`、`profile`、`cookies`、关键词、`exclude_id_files`、`sink`。
3. 阶段 A：`scripts/run_batch.sh A cfg.json`（scrape→rank→filter→download→frames→dedupe→select-template）。
4. **审核闸门**：逐张看 `05_sheets/sheet_*.jpg`，结合 `dyh list` 的描述，按 `references/selection-guide.md` 排除无关内容，填写 `07_selection.json` 的 `filename`。
5. 阶段 B：`scripts/run_batch.sh B cfg.json [archive.csv]`（select→verify→upload）。
6. 向用户回报：数量、排除了什么、目标文件夹总数、每个文件的链接；把 manifest 存档到项目 data/。

单步命令：`python3 -m dyh <scrape|rank|filter|list|download|frames|dedupe|select-template|select|verify|upload|auto|version> -c cfg.json [--set a.b=v]`。

## 关键规则
- 非作者看不到播放量 → 排序用 log 归一化互动分：点赞 .45、评论 .35、转发 .12、收藏 .08（可配置）。
- 描述/标签不可信（满屏 #吸嘴 的口播），**最终相关性以画面为准**。
- 文件名：小写英文、连字符、关键词在前（品牌/型号 + 部件 + smt-nozzle），无序号，在目标文件夹内唯一（`select` 会对比目标已有文件名）。
- cookies 是用户会话：不提交到 git、不打印、不上传；只取抖音域名。
- 失败处理与错误码见 `references/error-handling.md`；扩展点见 `references/extending.md`；升级见 `references/versioning.md`。
