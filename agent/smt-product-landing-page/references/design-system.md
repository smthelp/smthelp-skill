# Design System — Southern Machinery Landing Pages

从 `file.autoinsertion.com/public/Southern Machinery Product/Southern-Machinery-1200mm-LED-SMT-Line-Solution.html` 提取的品牌设计系统。所有产品页必须沿用，保证系列感。

## Tokens

```css
:root {
  --teal: #009fa5;        /* 主色：按钮、tab 选中、hero 边线 */
  --teal-dark: #087d86;   /* 主色 hover、eyebrow、CTA band 底 */
  --lime: #82bf32;        /* 辅色：challenge 边线、service 偶数步、CTA 顶边 */
  --lime-soft: #f0f7df;
  --ink: #292d30;         /* 正文/暗 band 底 */
  --muted: #66727a;       /* 次级文字 */
  --line: #cbdfe2;        /* 分隔线 */
  --soft: #eef7f8;        /* soft band 底 */
  --paper: #ffffff;
  --warm: #f4b740;        /* 警示/qualification、focus outline */
  --max: 1180px;
  --header-height: 76px;
}
font-family: Arial, "Helvetica Neue", sans-serif;  /* 仅此一族，离线友好 */
```

暗 band 高亮数字用 `#b8e563`；暗 band eyebrow 用 `#9ed9d8`。

## 版式节奏

- `.band` 88px 垂直 padding（compact 58px）；soft / dark 交替制造节奏
- `.eyebrow` 13px/800/uppercase/teal-dark，置于每个 h2 之上
- h1 54px（hero 内 46px）/ h2 38px / h3 20px；section-head max-width 780px
- `.container` = min(calc(100% - 40px), 1180px) 居中

## 组件库（类名即契约）

| 组件 | 类 | 用途 |
|---|---|---|
| 顶栏 | `.utility-bar` | 暗色条：公司+电话+邮箱 |
| 吸顶头 | `.site-header .brand/.site-nav/.header-cta/.nav-toggle` | Logo 左上；移动端汉堡 |
| Hero | `.hero .hero-media(absolute,cover) .hero-copy` | 图绝对定位铺满；teal 半透明文案板贴底左 |
| 数据条 | `.signal-strip .signals .signal` | 3 格大数字+注释 |
| 痛点 | `.challenge-grid .challenge` | 3 列，lime/teal 交替左边线 |
| FAB 卡 | `.system-shell .system-tabs .system-tab .system-detail .fab-row .fab-label` | tab 切换；F/A/B 三行，Benefit 标签用 #5f8f1f |
| 影响条 | `.impact-grid .impact` | 暗底 4 格大数字 |
| 规格 | `.spec-group .spec-title .spec-table` + `.qualification` + `.interface-chips` | 4px teal 标题线；斑马行；暖色免责块 |
| 画廊 | `.gallery-grid .gallery-item` + `<dialog id="lightbox">` | 16:9 cover；点击放大 |
| 视频 | `.video-grid .video-card .video-stage .video-load .play-icon` | click-to-load iframe，离线不崩 |
| 服务流 | `.service-flow .service-step` | 5 步，teal/lime 交替顶线 |
| FAQ | `.faq-list details summary` | +/− 手风琴 |
| CTA | `.cta-band .cta-grid .cta-actions` | teal-dark 底 + lime 顶边；右列按钮栈 |
| 页脚 | `footer .footer-grid .footer-brand .social-links .footer-bottom` | 4 列暗脚 |
| 浮动 | `.whatsapp-fab`(右下绿) `.back-to-top` `.chat-fab/.chat-panel`(左下) | 48px 圆钮，z-index 900/950 |

## 响应式断点

1020px（2 列化）→ 860px（汉堡导航、system-detail 单列、video 单列）→ 620px（全单列、spec 表 th/td 块级化）。`prefers-reduced-motion` 与 `@media print` 必备。

## 无障碍

`:focus-visible` 3px warm outline；skip-link；aria-label 全覆盖；touch target ≥44px；summary 不用 hover-only 信息。
