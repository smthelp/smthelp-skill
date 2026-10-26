# 错误码与排障
退出码 = 错误码编号；所有错误同时写入 run.log.jsonl。

| 码 | 退出 | 含义 | 处理 |
|---|---|---|---|
| E_CONFIG | 2 | 配置缺失/无效 | 检查 JSON、run_name、sink.options |
| E_DEP | 3 | 缺依赖 | `bash scripts/setup.sh`；沙箱重置后需重装 |
| E_COOKIES | 4 | cookies 缺失或无抖音域 | 登录 douyin.com 后重新导出 |
| E_SCRAPE_EMPTY | 5 | 抓到 0 条 | cookies 过期 / 验证码 / sec_uid 错；看 scrape_last.png |
| E_SCRAPE_PARTIAL | 警告 | has_more 仍为 true 就停了 | 再跑 scrape，自动按 aweme_id 合并；或调大 stall_limit |
| E_DOWNLOAD | 日志 | 某条所有 CDN 地址都失败 | 重跑 download（已下的跳过）；CDN 链接数小时后过期 → 重新 scrape |
| E_VERIFY | 8 | 时长不符或解码错误 | 删除 04_videos 中该文件，download --ids 重下，再 select/verify |
| E_SELECTION | 9 | 文件名不合规/重名/数量不对/ID 不在候选 | 按提示修改 07_selection.json |
| E_UPLOAD | 10 | 上传失败或远端大小不一致 | 重跑 upload（已存在的同名文件跳过）；不一致的先在目标删除再重传 |
| E_STAGE_INPUT | 11 | 上一阶段输出缺失 | 先跑上一阶段 |

已知现象：yt-dlp 自带 Douyin 提取器因 a_bogus 签名失败 → 本工具不用它，只用 yt-dlp 下载 CDN 直链；Playwright 自带浏览器在 arm64 下载 403 → 用系统 chromium；沙箱需代理时自动读取 HTTPS_PROXY。
