# Required Blocks — 每页必含元素（逐字核对清单）

Jason 的固定要求，生成后逐项核对，链接必须逐字一致。

## Header
- 左上角 Logo：`https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png`（alt="Southern Machinery"，width 218px 显示）

## Footer CTA（社交五件套 + 资源 + 联系）
- [LinkedIn Company Page](https://www.linkedin.com/company/smtmachine)
- [LinkedIn Profile](https://cn.linkedin.com/in/smtsupplier)
- [Twitter](https://twitter.com/smtspecialist)
- [Facebook](https://www.facebook.com/autoinsertion)
- [YouTube Channel](https://www.youtube.com/c/Smthelping)
- Browse our machine catalog at [file.autoinsertion.com](https://file.autoinsertion.com) and find machine photos at [ph.smthelp.com](https://ph.smthelp.com).（footer-bottom 固定句）
- Contact us: info@smthelp.com（mailto）
- 附加惯例：tel:+8613602562576、www.smthelp.com、Shenzhen 地址行、© 2026 Southern Machinery Co., Ltd.

## WhatsApp
- 浮动 FAB + CTA 按钮：`https://wa.me/8613602562576`（CTA 可带 ?text= 预填，FAB 用裸链）

## Puter.js 产品聊天窗
- 位置：左下 `.chat-fab` + `.chat-panel`（右下留给 WhatsApp FAB）
- **禁止**静态 `<script src="https://js.puter.com/v2/">`——file:// 会弹阻断式 "Unsupported Protocol" 框
- 正确姿势：`location.protocol` 为 http/https 时首次开窗动态注入；file:// 显示兜底文案（邮箱+WhatsApp+“host this page to enable AI chat”）
- system prompt 内置该产品事实表（规格/兼容/操作/维护/报价引导），限答本产品，<120 词
- 90s 超时降级为联系兜底；首次提问弹 puter.com 登录窗属正常（visitor-pays）

## 媒体
- YouTube：click-to-load（poster + play 按钮 → 点击才插 iframe），oEmbed 校验存活后收录
- 图片：品牌图用 ph.smthelp.com；供应商图（alicdn）必须 WebDAV 自托管后引用自有 URL（防盗链 403）
- lightbox 占位 `<img class="dialog-image" alt="">` 不写 src 属性

## 技术底线
- 单文件、原生 HTML/CSS/JS、无 CDN 依赖（双击 file:// 可用；字体用系统 Arial）
- 无障碍与 print/reduced-motion 样式齐备（见 design-system.md）
