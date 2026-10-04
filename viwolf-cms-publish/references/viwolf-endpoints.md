# viwolf 实例端点与配置（smthelp 生产站）
> 实例专属数据全部集中于此；SKILL.md 保持可移植。凭据一律只放 publishing-queue/secrets.env，严禁写入本文件。

## 站点
- 后台 base：`http://smthelp.v5.viwolf.cn/admin888`（session cookie `imb_admin`；登录 POST `login.php?action=check`，字段 adminname/adminpass）
- 生产域：`https://www.smthelp.com`（同一实例绑定域名）；备份站：smthelp.net（WP，整站 301→.com，Code Snippets 片段 #30）
- 清缓存：GET `redis.php?action=cache`

## 内容模型与端点
| 模型 | 列表 | 新增保存 | 编辑保存 | 删除 | 备注 |
|---|---|---|---|---|---|
| 产品 modelid=8 | `manage.shop.php?listid=<cat>&modelid=8` | `manage.shop.php?action=addsave&listid=<cat>&modelid=8&pid=1&lang=en` | `action=edtsave&listid=<cat>&lang=en&productid=<kid>`（**只写库不重建静态页**） | `action=delete&modelid=8&listid=<cat>&pid=1&kid=<kid>` | 更新页=delete+addsave |
| 文章 modelid=6 | `manage.article.php?listid=<col>&modelid=6` | `manage.article.php?action=addsave&listid=<col>&lang=en&modelid=6` | `action=edtsave…kid=` | `action=delete…kid=` | ndate=YYYY-MM-DD |
| 单页 modelid=2 / 超链接 50 / 自定义 53 | `index.php?action=add&modelid=…` | — | — | — | 栏目增删走 index.php |

产品字段：ksubtitle1 名称｜ktitle SEO标题(带 " \| Southern Machinery")｜kkeywords｜kdescription≤160 含数字｜kdesc1 卖点ul｜kcontent 正文HTML｜**para_01/02/03、kdesc2、shop_video_cover 可选字段一律不传空值**（空串触发 SQL 错；省略则 OK）。
文章字段：ksubtitle1/ktitle/kkeywords/kdescription/kdesc1(导语)/kcontent/ndate。

## 产品类目 listid（节选）
18401 PCB cleaning machine｜18407 THT machine｜18385 SMT machine｜19282 Wave Soldering Machines｜18403 Soldering machine｜18400 3D SPI AOI｜18406/18391 Separator-Router｜18601 Peripheral other｜18421 Board Handling｜18425 ESD｜18426 Feeders｜18427 PCB Assembly｜18398 PCB Bare Board｜18387 operation manual｜18390 X-ray。完整树：`index.php` 菜单或 `manage.shop.php?listid=<cat>&modelid=8` 页内。

## 文章栏目
18608 News and Events（博客默认）；其余：18603 Accessary、18604 Article、18605 Auto insertion、18606 General Information、18607 LED Marketing、18609 PCB、18610 PCBA cleaning machine、18611 Picture、18612 Reflow oven、18613 Reflow soldering、18614 SMT；19283 为无名新栏目（0 文，可改名启用）。

## 图片/文档上载（COS 三步）
- 签名：POST `http://smthelp.v5.viwolf.cn//tengxun/server/auth.php`（双斜杠原样）body `{"method":"put","pathname":"/smthelp.com/shop_imgs/<file>","query":{},"headers":{"content-type":"image/jpeg"}}` → 返回 `q-sign-*` 串
- 上传：PUT `https://hk03-1251009151.cos.ap-shanghai.myqcloud.com/smthelp.com/shop_imgs/<file>?<签名串>`
- 注册：POST `http://smthelp.v5.viwolf.cn//ajax/ajax.php?action=uploadimgs` form-data `kkey=smthelp.com/shop_imgs/<file>`（无首斜杠）`kurl=<完整COS地址> tid=<产品kid或0> ktype=shop_imgs` → media_id。pdf 用 kkey 前缀 `/smthelp.com/pdf/`、action one_file；视频 one_video。
- 富文本编辑器=UEditor（内容入库时 HTML 被转义存储，前台自行还原）；静态页 URL=`<slug>.html`，slug 冲突自动后缀 `---<kid>`。

## 素材看板
- 视频：`https://file.autoinsertion.com/public/Southern-Machinery-YouTube-Video-Board.html`（`<article class="doc-card video-card" data-title data-url>` 卡片可正则过滤；频道 youtube.com/c/Smthelping）
- 目录：`https://file.autoinsertion.com/public/Southern-Machinery-Product-Catalog-Board.html`（460+ PDF，href 直指 file.autoinsertion.com/public/<空间>/<文件>.pdf）
- 本地图源：ph.smthelp.com **文件级 404 未修**；实际图源=COS shop_imgs；素材库 `/Volumes/MOVESPEED/WUJ-doc/`（PCBA Cleaning Machine/、SMThelp Product PPT/、Southern Machinery Product PPT/.poster-work/、SMThelp Poster/）

## 发布流水线（QoderWork）
- 四件套目录：`smthelp-web/publishing-queue/`（pipeline-sop.md v260914.1 为运行时契约、pending.csv、log.md、secrets.env 600）
- cron（Asia/Shanghai 10:00，run_latest）：二=产品 fbce9c97-3071-4ac9-887d-f23501e5ac1e｜三=博客 8c34e6bb-51c9-4ae0-8909-c402c59dc045｜四=选题生成 a1ab3825-cdf7-47b4-a43d-69a96ae34f56｜五=周检 34f42291-6c3b-420c-928e-9d40fdfa0f7c
- ⚠️ 冲突预警：旧任务 14e67052（每6小时发 .net Blog）与 301 冲突，待处置
- 已发布样板：SME-6300 kid=137681（2图+2视频+4目录）｜SME-5600D kid=137682（3图 pdfimages 提取+1视频+目录PDF，slug 干净）｜SME-750II kid=137683（3图+3视频+1PDF，规格 750×750×40/480kg 等断言通过）｜博客 kid=2086。真实图来源优先级：本地渲染图→PDF pdfimages 提取→无图发布（禁 AI 图）。
- 待清理：孤儿静态页 `sme-6300-in-line-pcba-cleaning-machine.html`（旧内容，无入口）→ viwolf 工单删文件；`publishing-queue/stale-urls.md` 建议建立登记。

## 已知实例坑
- addsave 生成的静态页立即出现在源站；`.com` 类目页有 CDN TTL（分钟级）。
- 列表端 `action=def&kid=…&status=1` 是上下线开关，不触发重建。
- `url.php?action=p_url/a_url` 为链接编辑（modal 界面，curl 不可直写）。
- 后台 display_errors 开启：判断成败看 302 + 响应无 `ERROR!`，PHP notice 属噪音。
