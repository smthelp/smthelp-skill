# 输出规范（output-spec）

## 1. 交付物

- 一个自包含 `.html`（CSS/JS 全内联，无构建依赖，双击 file:// 可用），文件名 = SEO 文件名
- 本地：`work/<slug>/dist/<filename>.html` + `shots/`（截图与 verify_report.json）
- GitHub：`smthelping/smt-product-landing-html/<product-line>/<filename>.html`，README 表格同步
- 可选：WebDAV `https://file.autoinsertion.com/public/Product%20landing%20Page/<filename>.html`

## 2. 单文件结构（section 顺序 = product.json `sections`）

```
<head>  meta / title / description / keywords / canonical / hreflang x7 + x-default /
        OG + Twitter / JSON-LD @graph / <style>base.css + components.css + product.css</style>
<body>
  skip-link · topbar · header(logo 左上, nav, 主题按钮, 语言菜单, 汉堡菜单)
  <main>
    hero        徽章 + H1(两段) + 副标题 + 2 CTA + 无价格说明 + 轮播图
    metrics     4 个数字（数字优先）
    trust       3 条信任信息
    summary     GEO 摘要框：一段可引用总结 + 6 条实体事实（dl）
    pain   #why 6 张痛点卡
    how         步骤 + 示意图（SVG/图片，标 Concept illustration）+ 安全提示
    fab         6 组 Feature / Advantage / Benefit tabs
    models      型号/规格卡 + 适配表（fit table）
    spec        规格表，每行带证据标签 Verified / Concept / To be confirmed
    disclosure  来源冲突披露表（数值、来源 A、来源 B、处理）
    calc        计算器（输入全由访客填，公式在 product.json）
    gallery     图库 + lightbox
    videos      YouTube 卡片，分类筛选，点击才加载 youtube-nocookie iframe
    blog        8 篇文章 <details>，id=article-N
    docs        目录 PDF 卡（打开/预览）+ Video Board / Catalog Board 卡
    service     服务流程 5 步
    faq         10 问（FAQPage JSON-LD 同源）
    family      同系列页面互链
    contact     WhatsApp + 邮件 CTA + 询盘表单（mailto，不收集数据）
  </main>
  footer  logo + 简介 + 社媒五件套 / 产品链接 / 目录·图片·视频墙·目录墙 / 邮箱·WhatsApp·电话·官网·地址
  lightbox · PDF modal · WhatsApp 浮钮 · 回到顶部
  <script> I18N + CFG + runtime.js </script>
  <script> Chatwoot（紧贴 </body> 前，最后一个元素） </script>
```

可删 section（如无视频、无计算器），verify 会自动跳过对应检查；不可删：hero、summary、spec、faq、contact。

## 3. 响应式与技术硬要求

- 390 px 宽无横向滚动（en 与 ar 都测）；断点 1240 / 1040 / 760 / 640 px
- RTL：ar 时 `<html dir="rtl">`，布局镜像，Logo 在右；数字/型号/邮箱用 `dir="ltr"` 或 isolate 防乱序
- `prefers-reduced-motion`：轮播与动画冻结；`@media print`：展开所有 details
- file:// 可用：不依赖服务器、无 fetch、无模块加载
- 禁 CDN 框架（Tailwind/Bootstrap/jQuery/字体 CDN）；唯一外部脚本是 Chatwoot sdk
- 图片：品牌图优先 ph.smthelp.com；必须内嵌的用 base64（≤800 px，q≈78）
- 偏好持久化：`localStorage` `<storage_prefix>_lang` / `_theme`；`?lang=xx` 可覆盖
- 切语言时同步：所有 `data-i18n` 文本、alt、aria-label、title、`document.title`、meta description、OG

## 4. 设计与文案标准

- 英文为主（en 为母版），面向海外 EMS 工程师/采购
- 数字优先：每个卖点给可核对的参数（孔数、mm、pcs/roll、交期）
- 不写价格；所有 CTA 引导询盘（发图/型号报价、WhatsApp、邮件）
- 无他牌水印、无供应商名；他牌机型只作"适配"出现
- 证据标签贯穿：Verified material / Concept illustration / To be confirmed
- 标题与小标题不得出现 hook / diagnosis / framework / vehicle / loop / CTA（任何语言）
- 设计系统沿用 base.css：品牌绿 `#0c665c`、金色强调、卡片圆角、暗色主题完整覆盖

## 5. 验收清单（verify.py 全部 PASS 才算完成）

- [ ] 无 JS pageerror、无坏图、无空 src
- [ ] 7 语言切换 + 刷新后保持；lang/dir 正确；无裸 key 泄漏
- [ ] 任何语言的标题里无六步法字样
- [ ] 主题切换双向持久
- [ ] Logo 左上（RTL 右上）；社媒五件套、目录站、图床、邮箱、WhatsApp 链接齐全
- [ ] Chatwoot 脚本在 `</body>` 前、https
- [ ] JSON-LD 可解析且含 Organization / WebPage / BreadcrumbList / Product / FAQPage / ItemList / DefinedTermSet
- [ ] canonical、OG、hreflang（语言数 + x-default）
- [ ] 390 px 无横滚（en、ar）
- [ ] FAB tab、视频筛选与点击加载、lightbox、PDF 预览、文章展开、计算器可用
- [ ] 博客数 = blog_count
- [ ] 人工目检截图：light_top、dark_middle、ar_middle、mobile_ar_top 至少 3 张


## 6. 可选组件的验收（1.1.0 起）

启用 `matcher` 时 verify 追加：`matcher_rows_rendered`、`matcher_filter_reduces`（逐个包装筛选，至少一个 0 < 行数 < 总数）、`matcher_filters_combine`（类别 + 脚距组合后行数不增且与计数文字一致）、`matcher_reset`、`matcher_search`、`matcher_empty_state`、`matcher_detail_inquiry`（wa.me?text= 与 mailto 链接）、`matcher_detail_close`（Esc）、`matcher_check_part`、`matcher_labels_translated`（6 种非英语表头 ≠ 英文，且无 `mx_` 原始 key）、`matcher_mobile_cards_en` / `_ar`（390 px：卡片、表头隐藏、无元素越界），并截 `*_matcher.png`、`mobile_*_matcher.png`。
启用 `npi` 时追加 `npi_stepper`（跳到最后一步、勾选改变进度、下一步按钮），JSON-LD 必须含 `HowTo`，截 `*_npi.png`。
