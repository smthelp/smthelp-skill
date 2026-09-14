---
name: viwolf-cms-publish
description: "viwolf 建站 CMS（admin888 类后台）自动发布与整改 skill——无 API 表单式 CMS 的发布契约逆向五法、产品页/博客 addsave 发布、腾讯云 COS 图片三步上载、YouTube/目录看板素材集成、全站 301 归一（WordPress 片段法）、发布验证与回滚、QoderWork 定时流水线四件套模板。触发词：viwolf、admin888 后台、smthelp.com 发布、产品页发布、博客发布、addsave、shop_imgs、静态页重建、无API的CMS、301归一、发布流水线、pending.csv、secrets.env。用于 Southern Machinery 站点发布/GEO 整改落地；不要用于：有官方 REST API 的 WordPress 常规站（直接走 wp/v2）。"
version: 1.0.0
metadata:
  source: qoderwork-session-260914
  origin: "smthelp.com viwolf publish pipeline（SME-6300/SAGV0601 试点逆向实录）"
  upgradeable: true
  instance_doc: references/viwolf-endpoints.md
---

# viwolf 类 CMS 自动发布 Skill

给「没有 API、只有表单后台」的建站系统（典型：viwolf/威拓 admin888）建立可靠的机器发布通道。核心思想：**先用一次人肉试点把发布契约逆向成文档，之后一切按契约跑，改动只进文档不改流程。**

## 适用 / 不适用
- 适用：SaaS 建站后台（form + session cookie + 静态页生成）、需要批量发布产品页/博客、GEO 整改后的内容供给流水线。
- 不适用：原生 WordPress（有 wp/v2 REST，直接用内容 API）、需要复杂工作流的 CMS（先评估官方 API）。

## 发布契约逆向五法（新站点首次接入必做，全程只读→试点各一发）
1. **摸入口**：登录后抓菜单树（GET index.php），按 `modelid`/`listid` 归类内容模型（产品/文章/单页）；列表页行内链接暴露真实动作名（edt/delete/copy/def）。
2. **抄表单**：GET 编辑页（?action=edt 或 ?action=add），dump 全部 `name="…"`，从 `<form action>` 拿保存端点；用「label→字段」邻接解析语义（名称/SEO三件套/富文本/参数槽）。
3. **试探写入**：urlencode POST 保存端点。**看响应体里的 SQL echo / PHP notice 判断真实结果**（display_errors 类站点会打印 UPDATE 语句），并 GET 编辑页回读确认入库。
4. **定位重建触发点**：改库≠改线上。对静态生成型 CMS，逐一验证 保存端点/发布开关(如 action=def)/清缓存端点(redis.php 类)/URL 管理器 是否触发静态重建；找不到就走「**delete+add 重建**」保底路径（addsave 必然生成静态文件）。
5. **字段禁忌二分**：整体 FAIL、分组 OK 时，按字段组二分（空字符串常触发 SQL 错——**可选字段宁可不传，不要传空**）。

## 快速开始（实例端点见 references/viwolf-endpoints.md）
```bash
# 1) 登录拿 cookie（凭据一律读 secrets.env，不硬编码、不回显）
curl -s -c jar -X POST "$ADMIN/login.php?action=check" \
  --data-urlencode "adminname=$USER" --data-urlencode "adminpass=$PASS"   # 期望 302
# 2) 发布产品/文章：POST addsave（更新=先 delete 再 addsave；字段带真实来源）
# 3) 清缓存 → 双域名验证：200 + title 正确 + 内容特征串（表/视频/附件计数）
```

## 图片上载三步（COS 直传型）
```
a) POST {site}//tengxun/server/auth.php  body={"method":"put","pathname":"/<bucket-prefix>/<file>","query":{},"headers":{"content-type":"image/jpeg"}} → q-sign-* 签名串
b) PUT https://<bucket>.cos.<region>.myqcloud.com/<key>?<签名串>  --data-binary @file  → 200
c) POST {site}/ajax/ajax.php?action=uploadimgs  form: kkey=<key去头斜杠> kurl=<完整COS URL> tid=<产品ID或0> ktype=shop_imgs → media_id
本地图先 sips 限宽1600/jpeg q82；只用真实产品图，禁 AI 图。
```

## 素材集成（产品页富化标准件）
- 图：本机资料库渲染图/PDF 页截图 → 上载 COS → `<img alt="型号+品类关键词">`。
- 视频：产品目录看板（HTML 卡片含 data-title/data-url）按型号关键词过滤 → youtube-nocookie embed。
- 文档：目录看板按型号过滤 PDF → Downloads 清单。
- 参数：`<table>` 参数表是 GEO 引用主力，数字必须有来源文件（PDF/看板），无来源 → 标 needs_input 停发，**宁缺勿编**。

## 整站 301 归一（多域名家族整改）
- 服务器层不可改（SaaS/面板无权限）时，用 WordPress「Code Snippets 片段 + template_redirect」等效实现：**只挂前端、GET/HEAD only、登录编辑者豁免、wp-json/wp-admin 天然不受影响**。
- 宝塔 WAF 会拦含 `$_SERVER`/`preg_match`/`file(` 等特征的 POST——**改合规写法（$wp->request/strspn/explode），不做编码绕过**；Code Snippets 的 REST PUT 间歇不持久 → 改码走 DELETE+POST+回读三连。
- 跨域跳转必须 wp_redirect（wp_safe_redirect 白名单回退会把 Location 变成 wp-admin）；发布后必须清 nginx 页缓存，验证用带随机参数的 URL 穿透缓存判定「新逻辑对不对」，再用裸 URL 判定「缓存追没追上」。
- 镜像检测会把「301 后同标题」误判为 mirror——评估复扫时人工注明假阳性。

## 定时流水线四件套（QoderWork cron 模板）
文件四件套（放项目 publishing-queue/）：`pipeline-sop.md`（唯一操作契约，任务只引用它）、`pending.csv`（type,model,title,slug,category,keywords,source,status,published_url,notes）、`log.md`（台账+周报）、`secrets.env`(600)。
节奏模板：周二产品发布 / 周三博客发布 / 周四选题生成（只写队列）/ 周五只读周检（URL巡检+孤儿页清单+队列健康）。任务纪律：**失败标 failed 不自动重试发布**；结果写台账+任务报告；无来源数据转 needs_input。

## 已知坑速查
- 表单 enctype=multipart 与 urlencode 服务端可能不同分支——保存失败时换 multipart 复测。
- slug 冲突自动加 `---<id>` 后缀：旧文件未删时会占用干净 slug，产生孤儿页 → 记 stale-urls 清单，走平台工单删文件。
- 类目页/列表页常多一层 CDN TTL：详情页 200 即算发布成功，列表可见性次日复核。
- 后台路径写进 payload/仓库前脱敏（占位符 + secrets 文件）。

## 验证与回滚
- 验证三断言：HTTP 200（源站+生产域名）、`<title>` 含目标串、正文特征计数（图/视频/附件/表）符合预期。
- 回滚：内容级=删后按台账旧内容重建；站点级（301 片段）=停片段+清缓存；队列级=改 status 不回滚线上。

## 升级回流协议（每次使用后必做）
1. 新逆向出的端点/字段/类目表 → 追加 `references/viwolf-endpoints.md`
2. 新坑 → 本文件「已知坑速查」补一行；改配置不动流程时**不 bump 版本**
3. 流程变化才升 `version`，并在 skill 目录 `CHANGELOG.md` 记为什么改
4. 通用化边界：实例专属值（域名/listid/bucket/栏目）只准出现在 references，SKILL.md 保持可移植

## 文件索引
| 路径 | 作用 | 更新频率 |
|---|---|---|
| SKILL.md | 方法论与流程 | 低 |
| references/viwolf-endpoints.md | smthelp 实例端点/字段/类目/看板配置 | 高 |
| CHANGELOG.md | 版本记录 | 每次改动 |
