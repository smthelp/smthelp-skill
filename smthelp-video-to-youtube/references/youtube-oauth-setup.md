# YouTube OAuth 首次配置（一次性）

## 1. Google Cloud Console 前置条件

1. 打开 https://console.cloud.google.com/apis/credentials ，选中 YouTube Data API v3 已启用的项目。
2. **OAuth 客户端**：新建/选择 “Web 应用” 类型客户端（或已有客户端），记下 Client ID / Client Secret。
3. **已获授权的重定向 URI**：必须**一字不差**添加：
   ```
   http://127.0.0.1:8788/callback
   ```
   （无末尾斜杠、不是 https、端口 8788。若添加的是 localhost 写法，授权 URL 的 redirect_uri 也要相应改成 localhost。）
4. **OAuth 同意屏幕**：应用处于“测试中”时，必须把 YouTube 频道所属账号邮箱加入 **Test users**；否则授权页报
   `Error 403: access_denied (app not verified / testing mode)`。

## 2. 凭证存放（不入库）

```bash
mkdir -p ~/.config/smthelp-yt && chmod 700 ~/.config/smthelp-yt
cat > ~/.config/smthelp-yt/credentials.json <<'EOF'
{"client_id": "....apps.googleusercontent.com", "client_secret": "GOCSPX-...."}
EOF
chmod 600 ~/.config/smthelp-yt/credentials.json
```

> 不要把 client_secret 写进 smthelp-skill 仓库或任何 git 仓库。对话中暴露过密钥时应提醒用户到 Console 重置。

## 3. 授权流程（一次，之后自动刷新）

```bash
python3 scripts/yt_oauth.py
# 打印 AUTH_URL → 浏览器打开 → 选【拥有 Smthelping 频道的账号】→ Allow
# 页面跳回本地显示 “Authorization received”，令牌存 ~/.config/smthelp-yt/tokens.json
```

- scope 必须同时含 `youtube.upload` 与 `youtube.force-ssl`，否则无法核验频道/删除/回读。
- 上传目标是**授权账号的默认频道**。授权时选错账号 = 传到别的频道（历史上曾误传到 “SMT pcb assembly LED”）。
  上传前一律用 `channels.list(mine=true)` 核对 `UClX0iEG2bvJq8yUBEDamgDw`（SMT solution provider / Smthelping）。

## 4. 常见报错对照

| 报错 | 原因 | 处理 |
|---|---|---|
| `Error 400: redirect_uri_mismatch` | 重定向 URI 未登记/不一致 | 核对 Console 里登记的 URI 与授权 URL 完全一致 |
| `Error 403: access_denied`（测试模式） | 账号不在 Test users | 把频道账号邮箱加入测试用户后重试 |
| 上传成功但频道不对 | 授权账号默认频道不是 Smthelping | 用 Smthelping 所属账号重新授权，再上传 |
| `insufficient scopes` | 令牌缺少 force-ssl | 重新授权（yt_oauth.py 已含双 scope） |

## 5. 令牌维护

- access_token 约 1 小时过期：`yt_upload.py` 每次用 refresh_token 刷新后再上传。
- 令牌文件 `tokens.json` 权限 600；refresh_token 长期有效，除非用户在 Google 侧撤销。
