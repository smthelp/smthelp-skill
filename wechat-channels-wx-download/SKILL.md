---
name: wechat-channels-wx-download
description: 在 macOS 上安装并使用 ltaoo/wx_channels_download（微信视频号下载器）：一键安装、首次 sudo 运行装证书和系统代理、在 Mac 微信视频号页面出现的下载按钮下载（可选画质）、config.yaml 设置下载目录与命名、MCP 接入、卸载证书。Use when Jason wants 视频号 videos saved locally with the in-page download button, or wants an agent to list/download a 视频号 account's videos via MCP.
version: 1.0.0
---

# wechat-channels-wx-download

Mac 微信视频号 → 页面内「下载」按钮 → 本地 MP4（自动解密，可选画质）。

## 红线
- 只下载 Southern Machinery 自有、供应商授权或允许转载的内容；他人视频只做内部参考。
- 对外发布前由 Jason 审核。
- 许可证是 MIT + Commons Clause：可以自用，**不得把该软件本身拿去售卖或做收费服务**。
- 它会安装根证书 `SunnyNet` 并设置系统代理（默认 127.0.0.1:2023）。只在 Jason 自己的 Mac 上用；不用时可以卸载证书。

## 与 res-downloader 的分工
| | wx_channels_download | res-downloader |
|---|---|---|
| 范围 | 只做视频号，页面内下载按钮、画质可选 | 多平台抓包（含抖音） |
| 自动化 | MCP：按账号列视频、查详情、直接下载 | CLI/MCP：列出已抓资源再下载 |
| 代理端口 | 2023 | 8899 |
**两者不要同时开**，都会改系统代理。

## 1. 安装（一次）
```bash
bash scripts/install_macos.sh
cd ~/Applications/wx_channels_download && sudo ./wx_video_download
```
- 脚本：按芯片下载最新 darwin 包 → 解压到 `~/Applications/wx_channels_download` → 去隔离属性 → 写 `config.yaml`（下载到 `~/Movies/SMT-WeChat-Channels`）。
- 首次必须 `sudo` 运行：自动装证书、设系统代理；终端出现「代理服务启动成功」即可。
- 被拦截时：系统设置 → 隐私与安全性 → 仍要打开。
- 自动装证书失败：双击 `SunnyNet.cer` → 加入「系统」钥匙串 → 信任设为「始终信任」。

## 2. 下载（每次）
1. 运行 `wx_video_download`（首次之后可双击）。
2. 打开 Mac 微信 → 视频号 → 打开视频；操作栏会多一个「下载」按钮（没有就看页面侧边/底部悬浮按钮）。
3. 视频开始播放后暂停，点下载；下拉菜单可选更高画质。文件名末尾带画质标记。
4. 用完关掉下载器。若断网：系统设置 → 网络 → 代理，关掉 HTTP/HTTPS 代理。

## 3. 命名与归档
- `config.yaml` 的 `download.filenameTemplate` 可用 `{{author}} {{title}} {{id}} {{spec}} {{created_at}}`；带 `/` 会按目录分（仅后台下载生效）。
- 归档用于营销时再按规范改名：`<YYYYMMDD>_<主题英文>_<设备型号>_wx-channels.mp4`，并记 `manifest.csv`（日期、原标题、作者、文件名、用途、授权）。

## 4. MCP（可选）
下载器运行时，设置 → MCP 打开 Streamable HTTP，默认 `http://127.0.0.1:2022/mcp`。常用工具：
`get_wxchannels_status`、`search_wxchannels_accounts`、`get_wxchannels_account_videos`、`get_wxchannels_video_profile`、`download_content`、`get_download_tasks`、`decrypt_wxchannels_video`、`get_certificate_status`。
`deploy_sph_worker`、`update_config` 会改远端或配置，调用前要先问 Jason。不要把 `api.hostname` 开到公网。

## 5. 卸载
```bash
bash scripts/uninstall_macos.sh   # 先 sudo wx_video_download uninstall 卸证书，再可选删目录
```

## 故障排查
| 现象 | 处理 |
|---|---|
| 没有下载按钮 | 确认终端提示代理启动成功、证书已信任；重启微信再开视频号 |
| 断网 / 和 Clash 冲突 | 关系统代理；或 `proxy.system: false`，Clash 转发到 127.0.0.1:2023 |
| 新版视频号白屏 | 更新到最新版：重新跑 install_macos.sh（不覆盖已有 config.yaml） |

## 参考
- https://github.com/ltaoo/wx_channels_download （README、docs/guide/start.md、docs/config、docs/cli/mcp.md）
