# 落地页发布到 GitHub + GitHub Pages

把生成好的单文件 HTML 推到公司仓库并开 Pages 的标准流程。所有坑都来自 2026-09-06 的实测。

---

## 1. 授权：先确认能不能推

```bash
gh auth status                                    # 看当前登录账号
gh api repos/<OWNER>/<REPO> --jq '{perm:.permissions}'
```

**坑 1**：`gh` 默认登录的是 `smthelp`，对 `smthelp111/*` 只有 `pull`，**没有 push**。
跨账号仓库必须用目标账号自己的 PAT。

**坑 2**：本机通常没有 SSH 密钥（`~/.ssh` 无 `.pub`），SSH 路线不可行。

**坑 3（必做）**：拿到 PAT 先数长度。GitHub 经典 PAT 是 **40 位**（`ghp_` + 36）。
短了就是粘贴被截断，直接让用户重贴——先验证再动手，别浪费一轮推送。

```bash
curl -s -H "Authorization: Bearer $TOKEN" https://api.github.com/user
# 返回 login 即有效；返回 "Bad credentials" 即无效
```

**坑 4**：克隆时把 token 写进 remote URL，之后所有 `git push` 都不用再输凭据、不再触发审批：

```bash
git clone https://<OWNER>:${TOKEN}@github.com/<OWNER>/<REPO>.git /tmp/repo
```

---

## 2. 文件结构

```
index.html                                        ← Pages 入口（根目录）
machines/<seo-filename>.html                      ← 保留 SEO 原文件名
prompts/<MODEL>-landing-prompt.md                 ← 生成该页的 Prompt
README.md                                         ← 仓库索引（规格表 + 维护说明）
.gitignore                                        ← ._* / .DS_Store / Thumbs.db
```

**坑 5**：百度网盘同步卷写文件会生成 AppleDouble `._*` 垃圾文件。
`cp -R` 之后再 `find . -name '._*' -delete`，并且 `.gitignore` 里加 `._*` 兜底。

**坑 6**：HTML 落盘后 Notion 会注入 `data-page-node-id`（~695 处 / +30 KB）。推送前必须清：

```python
s = re.sub(r'\s*data-page-node-id="[^"]+"', '', s)
```

---

## 3. Pages 源分支：默认不是 main

**坑 7**：这个仓库的 Pages 源是 **`master`**，不是 `main`。
仓库同时存在 `main` / `master` / `gh-pages` 三个分支，`master` 和 `gh-pages` 上已有
`s100b-southern-machinery-3d-landing.html`（另一机型）——**不要覆盖**。

```bash
# 查当前配置
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/<OWNER>/<REPO>/pages

# 改源到 main（返回 204，body 为空，别用 json.load 解析）
curl -s -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/<OWNER>/<REPO>/pages \
  -d '{"source":{"branch":"main","path":"/"}}'
```

**坑 8（关键）**：改完源**不会自动重建**，页面继续 404。必须推一个空提交触发：

```bash
git commit --allow-empty -m "chore: trigger GitHub Pages rebuild"
git push origin main
```

空提交后约 **25 秒**生效。轮询验证：

```bash
for i in $(seq 1 10); do
  code=$(curl -s -o /tmp/pg.html -w "%{http_code}" "$PAGES_URL")
  [ "$code" = "200" ] && echo OK && break
  sleep 12
done
```

---

## 4. 上线后核验清单

```
title / canonical / meta description
Logo、Chatwoot、5 条社媒、file.autoinsertion.com、ph.smthelp.com、wa.me
Schema.org Product、强制 CTA ×2（逐字）、配套机型
YouTube 视频数、Catalog PDF 数、Blog 篇数
data-page-node-id 残留 = 0
禁用词 = 0，最终价格 = 0
```

---

## 5. 已知待办

**canonical 冲突**：页面里的 canonical 指向 `https://www.SMThelp.com/products/...`（品牌官网），
但 Pages 实际地址是 `https://<USER>.github.io/<REPO>/`。
若该页只发在 Pages，canonical 应改成 Pages 地址；若官网同名页面存在，保持现状。
**每次部署前确认一次，不要默认。**

**Chatwoot 混合内容**：SDK 的 `baseUrl` 是 `http://chat.smthelp.com`，而 Pages 是 HTTPS，
浏览器会拦截。需要 `chat.smthelp.com` 支持 HTTPS，否则客服组件在线上不显示。
