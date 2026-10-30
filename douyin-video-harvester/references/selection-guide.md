# 相关性审核与命名

## 审核（阶段 7 闸门）
1. `python3 -m dyh list -c cfg.json` 看排名、互动、时长、描述。
2. 逐张看 `05_sheets/`。保留：画面实际展示主题物（吸嘴、夹式/异形吸嘴、贴片机吸嘴、吸嘴应用案例）。
3. 排除：老板/员工口播、创业故事、节日祝福、工厂泛宣传、展会、生活内容、静态图片海报、电影片段开头、同公司其它产品（顶针、花键、刮刀）。
4. 排除 `06_dupes.json` 中与以前批次重复的条目。
5. 候选不够 N 条：调大 `filter.candidate_limit`，`download --ids <rank...>` 补下，再 `frames`。
6. 按排名顺序填 N 条。

## 文件名
- 小写英文、连字符分隔、2–12 词、`.mp4`，无序号前缀。
- 关键词优先：`<brand/model>-<component/application>-<smt-nozzle|gripper-nozzle>`，例：`yamaha-ysm20-ys24-usb-custom-smt-nozzle.mp4`、`juki-custom-gripper-claw-nozzle-cases.mp4`。
- 只写画面/描述能证实的品牌型号；不确定就用通用词（custom、odd-form）。
- 不与目标文件夹已有文件重名（`select` 自动检查）。
