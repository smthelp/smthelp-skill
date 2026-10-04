---
name: open-webui-remote-diagnosis
description: 远程诊断 Open WebUI 实例（Browserbase + Cloudflare 场景）的标准流程
archived: 2026-06-14
absorbed_into: devops/open-webui (as §2)
---

# Open WebUI 远程诊断与故障排查

## 触发条件
当用户要求你登录或诊断 Open WebUI 实例时使用。

## 诊断流程（已验证有效）

### 第一阶段：区分网络层 vs 应用层

```
步骤1: browser_navigate 到目标 URL
  - 成功加载 → 说明域名可达，CDN/代理可能正常
  - 超时 → 可能是网络隔离（如 198.18.x.x RFC 2544 测试地址）

步骤2: browser_console 检查页面状态
  - document.title 获取标题
  - document.body.innerHTML.length 检查内容是否加载
  - SvelteKit SPA: 等待 __sveltekit_ 动态加载完成

步骤3: 识别 Cloudflare 代理
  - 出现 "502 Bad Gateway" + cloudflare.com 链接 → Cloudflare CDN 正常，但源站服务挂了
  - Ray ID 存在 → 确认经过 Cloudflare
```

### 第二阶段：502 Bad Gateway 排查

**核心原则：** Cloudflare 可以访问，但源站（Open WebUI 后端）不响应。

```
用户需在服务器端执行：
1. 检查容器状态：
   docker ps | grep open-webui
   docker logs open-webui --tail 50

2. 检查端口监听：
   netstat -tlnp | grep -E '3000|8080|8000'

3. 重启服务：
   docker restart open-webui

4. 如果用 Cloudflare Tunnel：
   cloudflared tunnel list
   cloudflared tunnel run <tunnel-name>
```

### 第三阶段：网络隔离识别

```
特殊 IP 段警告：
- 198.18.x.x: RFC 2544 网络基准测试地址
  → 说明服务部署在 VPN / 虚拟机 / 内网环境
  → 需要先连入对应网络，或配置 Cloudflare Tunnel / ngrok 公网暴露
```

## 关键经验

1. **Browserbase 浏览器和 curl 不走同一路由** — Browserbase 能访问（成功返回 title），curl 超时，说明是出口路由问题，不是服务真的 down

2. **SvelteKit SPA 需要等待** — `__sveltekit_` 动态 import 后 splash screen 消失需要 5-10 秒

3. **502 是 Cloudflare 的缓存响应** — 不代表当前状态，可能源站已恢复但 CDN 还在缓存

4. **首次 browser_navigate 超时不代表失败** — SvelteKit 懒加载 JS 可能需要多次重试

## 快速检测命令

```bash
# 检测是否是 Cloudflare 代理
curl -sI "https://sui.3dsmt.com" | grep -i "cf-ray\|cloudflare"

# 检测源站是否有响应（绕过 Cloudflare 缓存）
curl -s -H "Cache-Control: no-cache" "https://sui.3dsmt.com"
```

## 常见部署场景

| 场景 | 特征 | 解决方案 |
|------|------|----------|
| Docker 本地 | `198.18.x.x` IP | 配置 Cloudflare Tunnel 或 ngrok |
| 云服务器 | 公网 IP 可直接访问 | 检查容器是否在运行 |
| VPN 内网 | ping 不通 | 先连 VPN 或配置隧道 |
| Cloudflare Tunnel | 502 源站错误 | `cloudflared tunnel run` 重连 |

## 作者备注
2026-04-30 验证于 sui.3dsmt.com (Cloudflare + Open WebUI SvelteKit SPA)
