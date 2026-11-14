---
name: wechat-channels-res-downloader
description: 用开源工具 res-downloader（putyy/res-downloader，Apache-2.0）在 macOS 上把微信视频号视频下载到本地：安装、装证书、开启抓取、在微信桌面端播放视频号、下载并解密，再按 Southern Machinery 规则重命名归档。也覆盖 CLI / MCP 让 Agent 查询资源和创建下载。Use when Jason wants WeChat Channels (视频号) videos saved locally.
version: 1.0.0
---

# wechat-channels-res-downloader

微信视频号 → res-downloader 抓取 → 本地 MP4（已解密）→ 重命名归档。

## 适用范围与红线
- 只下载 Southern Machinery 自有、供应商授权或明确允许转载的内容。他人视频仅作内部参考，不得二次发布。
- 对外发布前一律由 Jason 审核。
- 工具原理是本机代理抓包（同 Charles/Fiddler），需要安装并信任一张本机根证书；只在 Jason 自己的 Mac 上使用，不要把证书或 `control/session.json` 提交到任何仓库。

## 环境
| 项 | 说明 |
|---|---|
| 系统 | macOS（Jason 的 Mac mini）；Win/Linux 安装包同样存在 |
| 微信 | Mac 版微信，已登录，可打开视频号 |
| 版本 | 默认 4.0 beta（含视频号插件、CLI、MCP）；求稳可装 3.1.3 稳定版（无 CLI/MCP） |
| 代理 | 127.0.0.1:8899（软件自动设置系统代理） |

## 1. 安装（一次）
```bash
bash scripts/install_macos.sh            # 最新 4.0 beta，自动识别 Apple 芯片 / Intel
STABLE=1 bash scripts/install_macos.sh   # 改装 3.1.3 稳定版
```
脚本：从 GitHub Releases 下载对应 dmg → 挂载 → 复制 `res-downloader.app` 到 /Applications → 去掉隔离属性。
若首次打开被拦截：系统设置 → 隐私与安全性 → 仍要打开。

## 2. 证书与网络（一次）
1. 打开 res-downloader，按引导**安装证书**并输入 Mac 登录密码授权（之后可在“系统设置 → 证书”重装）。
2. 允许网络访问。

## 3. 下载视频号（每次）
1. res-downloader →“获取资源”→ 点 **开启抓取**；类型选“视频”或全部。
2. 打开 Mac 微信 → 视频号 → 播放目标视频（播放几秒即可被抓到）。
3. 回到 res-downloader 资源列表，找到域名含 `finder` / `channels` 的视频条目 → 下载。
4. 视频号文件是加密的：下载后在操作项点 **视频解密（视频号）**（4.0 预装视频号插件时会自动处理）。
5. 用完点 **关闭抓取**。若关闭软件后无法上网：系统设置 → 网络 → 代理，手动关掉 HTTP/HTTPS 代理。

## 4. 命名与归档
- 文件名：`<YYYYMMDD>_<主题英文>_<设备型号>_<来源>.mp4`，例 `20261114_radial-insertion-demo_S3010A_wx-channels.mp4`。
- 存放：`~/Movies/SMT-WeChat-Channels/<YYYY-MM>/`；需要时再上传 Google Drive 对应文件夹。
- 每批记录 `manifest.csv`：日期、原标题、作者、视频号链接或描述、文件名、用途（内部参考/可发布）、授权情况。

## 5. Agent 自动化（可选，需 4.0 且软件在运行）
```bash
bash scripts/rd.sh resources list --limit 50          # 列出已抓到的资源（JSON）
bash scripts/rd.sh downloads create --resource-id ID  # 用资源 ID 建下载任务
bash scripts/rd.sh downloads list                     # 看进度
```
MCP 配置（Claude/Codex/Hermes 等支持 mcpServers 的客户端）：
```json
{"mcpServers":{"res-downloader":{"command":"/Applications/res-downloader.app/Contents/MacOS/res-downloader","args":["mcp","--stdio"]}}}
```
CLI/MCP 不会自动打开视频号或登录微信，仍需先在微信里播放视频。退出码 3 = 桌面应用没开或会话失效，重启应用即可。

## 故障排查
| 现象 | 处理 |
|---|---|
| 列表空白 | 确认已“开启抓取”、证书已信任、系统代理为 127.0.0.1:8899；重新播放视频 |
| 下载的视频打不开 | 未解密，点“视频解密（视频号）” |
| 大文件失败 | 复制链接用 Motrix 下载后再解密 |
| 关掉后断网 | 手动关闭系统代理 |

## 参考
- 项目：https://github.com/putyy/res-downloader
- 文档：https://res.putyy.com/ （安装 / 快速开始 / CLI 与 MCP）
