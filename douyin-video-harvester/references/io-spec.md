# 输入输出规范

## 配置 (JSON, schema: config/config.schema.json)
必填 `run_name`；`profile` 抓取时必填。其余有默认值（dyh/config.py `DEFAULTS`）。命令行 `--set filter.candidate_limit=50` 可覆盖任意键（值按 JSON 解析）。

## 运行目录 runs/<run_name>/
| 文件 | 阶段 | 格式 |
|---|---|---|
| 01_awemes.json | scrape | 抖音原始 aweme 对象数组（重跑时按 aweme_id 合并） |
| 02_ranked.json | rank | 同上 + `_score` `_rank` `_is_image` |
| 03_candidates.json | filter | 候选子集 + `_filter`（keyword_hit / no_keyword） |
| 04_videos/{rank:03d}_{aweme_id}.mp4 | download | 原片 |
| 05_sheets/sheet_NN.jpg | frames | 每条 3 帧（25/50/80%），左上角黄色数字 = 排名 |
| 06_dupes.json | dedupe | `[{"a","b","diff"}]`，diff<阈值即视为同一视频 |
| 07_selection.json | **人工/Agent** | `[{"aweme_id","filename"}]`，顺序即交付顺序，数量 = select.count |
| 08_final/<filename> | select | 重命名后的成片 |
| 09_verify.json | verify | 每个文件 bytes/duration/api_duration/decode_error/ok |
| 10_upload.json | upload | 远端 id/size/url、目标文件夹总数、mismatch/missing |
| manifest.csv | upload | order,orig_rank,aweme_id,filename,likes,comments,shares,favorites,desc,url |
| run.log.jsonl | 全部 | 每行一个事件 `{"t","stage","event",...}` |

## 交付给用户
manifest.csv（另存一份到项目 data/<account>-douyin-<topic>N.csv，作为以后批次的 `exclude_id_files`）+ 文件链接列表 + 目标文件夹总数。
