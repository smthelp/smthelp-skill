# douyin-video-harvester

把"从某个抖音账号精选 N 条与主题相关的视频，改英文 SEO 文件名，存进 Google Drive"做成可复用、可升级的流水线。2026-10 用于 Southern Machinery SMT 吸嘴视频库（6 个账号、110 条）。

## 快速开始
```bash
bash scripts/setup.sh
mkdir -p secrets && cp ~/Downloads/www.douyin.com_cookies.txt secrets/douyin.cookies.txt   # 浏览器扩展 "Get cookies.txt LOCALLY" 导出
cp config/config.example.json my.json   # 编辑 run_name / profile / 关键词 / sink
scripts/run_batch.sh A my.json          # 抓取→排序→初筛→下载→联系表→去重→生成选择模板
# 查看 runs/<run_name>/05_sheets/*.jpg，编辑 runs/<run_name>/07_selection.json 填文件名
scripts/run_batch.sh B my.json          # 校验文件名→重命名→完整解码校验→上传→清单
```
完整示例：`examples/smt-nozzle/`（真实配置、已交付排除清单、20 条选择结果）。

## 架构
```
dyh/
  cli.py        命令入口（每个阶段一个子命令；auto = 阶段 A）
  config.py     默认值 ← JSON 配置 ← --set 覆盖
  io.py         运行目录文件布局（阶段之间只通过文件通信 → 可断点续跑）
  log.py        stderr 文本日志 + run.log.jsonl 结构化事件
  errors.py     错误码 → 退出码
  cookies.py    Netscape 解析，只保留抖音域名
  scrape.py     阶段1  Playwright+系统 Chromium 拦截 /aweme/v1/web/aweme/post/
  rank.py       阶段2  互动分排序
  filter.py     阶段3  关键词初筛 / 图片帖 / 已交付排除
  download.py   阶段4  yt-dlp 逐个 CDN 地址重试，并发，可缓存
  frames.py     阶段5  抽帧 + 联系表
  dedupe.py     阶段6  16x16 灰度指纹近重复检测（可跨批次目录）
  select.py     阶段7  审核结果校验（命名规则、重名、数量）+ 重命名
  verify.py     阶段8  时长对比 + 完整解码
  deliver.py    阶段9  上传 + 远端大小比对 + manifest.csv
  sinks/        交付后端插件：local、gdrive_gws（扩展点）
```
依赖关系：scrape → rank → filter → download → {frames, dedupe} → select(人工闸门) → verify → upload。

## 文档
- `SKILL.md` Agent 使用说明
- `references/io-spec.md` 输入输出与文件格式
- `references/selection-guide.md` 相关性审核与命名规则
- `references/error-handling.md` 错误码与排障
- `references/extending.md` 扩展点（新 sink、新排序、新筛选、自动视觉分类）
- `references/versioning.md` / `changelog.md` / `feedback-log.md` 版本与反馈

## 测试
`python3 -m unittest discover -s tests`（离线单元测试）。

## 安全
cookies 文件含登录会话，`.gitignore` 已排除 `secrets/`、`*.cookies.txt`、`runs/`。不要把原始浏览器导出的全量 cookies（含 Google/GitHub 会话）放进仓库或共享目录。
