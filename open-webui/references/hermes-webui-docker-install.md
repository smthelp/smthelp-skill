---
name: hermes-webui-docker-install
description: hermes-webui Docker macOS 安装配置 — 预构建镜像 + LaunchAgent 开机自启 + 远程 IP 访问
archived: 2026-06-14
absorbed_into: devops/open-webui (as §3)
tags:
  - docker
  - hermes-webui
  - macos
  - launchagent
  - homelab
created: 2026-04-25
updated: 2026-04-25
type: workflow
---

# hermes-webui Docker macOS 安装配置

## 关键经验

- **不要本地 build** — 超时，改用 `ghcr.io/nesquena/hermes-webui:latest` 预构建镜像
- **macOS UID/GID** — 非 1000，需在 `.env` 显式设置（`UID=501`, `GID=20` 或用 `id -u`/`id -g` 获取）
- **远程访问** — docker-compose.yml 端口映射改为 `8787:8787`（不写 `127.0.0.1:` 前缀则默认绑定 `0.0.0.0`）
- **安全警告** — 未设密码时默认绑定 `0.0.0.0` 有风险，容器日志会提示 `WARNING: Binding to 0.0.0.0 with NO PASSWORD SET`

## 标准安装流程

### 1. 拉取预构建镜像（不做本地 build）

```bash
docker pull ghcr.io/nesquena/hermes-webui:latest
```

### 2. 准备目录和 .env

```bash
mkdir -p ~/hermes-webui
cd ~/hermes-webui

cat > .env << 'EOF'
UID=$(id -u)
GID=$(id -g)
HERMES_WEBUI_HOST=0.0.0.0
HERMES_WEBUI_PORT=8787
HERMES_WEBUI_STATE_DIR=~/.hermes/webui-mvp
HERMES_HOME=~/.hermes
EOF
```

### 3. 准备 docker-compose.yml（使用预构建镜像 + 远程访问）

```yaml
version: "3.8"

services:
  hermes-webui:
    image: ghcr.io/nesquena/hermes-webui:latest
    ports:
      - "8787:8787"        # 0.0.0.0 暴露，支持远程 IP 访问
    volumes:
      - ${HERMES_HOME:-${HOME}/.hermes}:/home/hermeswebui/.hermes
      - ${HERMES_WORKSPACE:-${HOME}/workspace}:/workspace
    environment:
      - WANTED_UID=${UID:-1000}
      - WANTED_GID=${GID:-1000}
      - HERMES_WEBUI_HOST=0.0.0.0
      - HERMES_WEBUI_PORT=8787
      - HERMES_WEBUI_STATE_DIR=/home/hermeswebui/.hermes/webui
    restart: unless-stopped
```

### 4. 启动并验证

```bash
docker compose up -d
sleep 8
curl -s -o /dev/null -w "%{http_code}" http://localhost:8787/health
# 期望: 200
docker logs hermes-webui-hermes-webui-1 --tail 20
```

### 5. 注册 LaunchAgent 开机自启

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.hermes.webui</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/env</string>
        <string>bash</string>
        <string>-l</string>
        <string>-c</string>
        <string>cd /Users/jasonwu/hermes-webui && /usr/local/bin/docker compose up -d</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/Users/jasonwu/hermes-webui</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>

    <key>StandardOutPath</key>
    <string>/Users/jasonwu/.hermes/logs/webui.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/jasonwu/.hermes/logs/webui.error.log</string>
</dict>
</plist>
```

```bash
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.hermes.webui.plist
```

### 6. 远程访问

```bash
# 同一局域网直接浏览器访问
http://<本机IP>:8787

# 或 SSH Tunnel（更安全）：
ssh -N -L 8787:127.0.0.1:8787 jasonwu@<本机IP>
# 然后浏览器打开 http://localhost:8787
```

## 安全配置（强烈建议）

设置访问密码：
- 方式A：环境变量 `HERMES_WEBUI_PASSWORD=your_secure_password` 加入 `.env` + 重启
- 方式B：在 Web UI 的 Settings 界面设置

## 常用维护命令

```bash
# 查看状态
docker ps | grep hermes-webui

# 查看日志
docker logs -f hermes-webui-hermes-webui-1

# 重启
cd ~/hermes-webui && docker compose restart

# 停止
cd ~/hermes-webui && docker compose down

# 卸载（清除容器 + LaunchAgent）
cd ~/hermes-webui && docker compose down
launchctl bootout gui/501/ai.hermes.webui
rm ~/Library/LaunchAgents/ai.hermes.webui.plist
```
