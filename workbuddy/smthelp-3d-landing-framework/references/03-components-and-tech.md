# 03 · 组件、性能、降级与 SEO

## 可复用组件

| 组件 | 改造自 | 规格 |
|---|---|---|
| **QuoteButton** | 原 `JoinButton` | `rounded-full`；背景 `linear-gradient(123deg, #06282A 7%, #0AA5A5 37%, #6FA832 72%, #90C641 100%)`；内阴影 `0px 4px 4px rgba(10,165,165,0.25)` + `4px 4px 12px #0AA5A5 inset`；白色 2px outline（offset -3px）。文字 white / font-medium / uppercase / tracking-widest。`px-8 py-3 sm:px-10 sm:py-3.5 md:px-12 md:py-4`，`text-xs sm:text-sm md:text-base`。Label `Request a Quote` |
| **ViewCaseButton** | 原 `LiveProjectButton` | Ghost 胶囊，`border-2 #D7E2EA`，文字 `#D7E2EA`，uppercase / tracking-widest，`px-8 py-3 sm:px-10 sm:py-3.5`，hover `bg-[#D7E2EA]/10` |
| **Magnet** | 原 `Magnet` | 鼠标跟随磁吸，`translate3d` 除以 strength（3），进入 padding 150 内激活，in `0.3s ease-out` / out `0.6s ease-in-out`，`willChange: transform`。**作用对象改为设备主视觉** |
| **FadeIn** | 原 `FadeIn` | `whileInView`，`viewport={{ once: true, margin: "50px", amount: 0 }}`，duration 默认 0.7，easing `[0.25, 0.1, 0.25, 1]`，接受 delay / x / y，用 `motion.create()` 支持动态元素类型 |
| **AnimatedText** | 原 `AnimatedText` | 逐字符 opacity `0.2 → 1`，`useScroll` offset `['start 0.8','end 0.2']`。**仅用于工艺叙事短句，参数禁用** |
| **Marquee** | 原滚动逻辑 | 双向滚动驱动，passive listener，`willChange: transform` |
| **Hotspot** | 新增 | 设备图上绝对定位标注点，`#90C641`，2s 脉冲，hover 展开参数标签 |
| **SpecRow / StatCard / AccordionItem** | 新增 | 参数行 / 数据卡 / FAQ 折叠项 |

## 依赖

```
react, react-dom ^18.3.1
framer-motion ^12.38.0
lucide-react ^0.344.0
tailwindcss ^3.4.1
vite, typescript
```

## 响应式

Tailwind 默认断点（sm 640 / md 768 / lg 1024），mobile-first。
字号大量使用 `clamp()`，从手机到超宽屏连续缩放。
首屏高度 `100svh`。

## 性能（原框架完全没写，B2B 必须补）

| 项 | 要求 |
|---|---|
| Hero 视频 | MP4 (H.264) + WebP poster，`muted loop playsInline`，**≤ 2 MB** |
| GIF | 只允许出现在 Marquee，单张 **≤ 400 KB** |
| 滚动监听 | 全部 `{ passive: true }` |
| 变换元素 | `willChange: 'transform'` |
| 图片 | 非首屏全部 `loading="lazy"` |
| LCP 目标 | **< 2.5 s** |

## 降级

- **`prefers-reduced-motion: reduce`** → 关闭 Magnet、Marquee 位移、AnimatedText 逐字动画；文字直接 opacity 1。
- **无 JS 降级** → Specs 与 FAQ 必须可读：用原生 `<details>`，或默认展开。
  ⚠️ 这一条在 B2B 场景尤其重要：采购常在**企业邮件网关 / 内网代理**后面打开落地页，JS 可能被拦。参数是唯一不能丢的内容。

## SEO 与分享

- `<title>`：`[MODEL] [PROCESS] Machine | Southern Machinery`
- meta description：机型 + 两个关键参数 + 一句话应用
- OG image 1200×630：设备图 + 机型号 + 品牌绿条
- JSON-LD `Product` schema：`brand: Southern Machinery`、`sku: [MODEL]`

## 已知坑

1. **`h-screen` 在移动端会跳** —— LinkedIn / 微信内置浏览器地址栏收起时视口高度变化。一律用 `100svh`。
2. **`whitespace-nowrap` 的超大标题在窄屏会溢出** —— 必须配外层 `overflow-hidden` + `overflowX: 'clip'` 的 wrapper，否则会出现横向滚动条。
3. **Marquee 的 `willChange` 不要长期挂着** —— 只在进入视口时启用，否则移动端内存压力明显。
4. **sticky 叠卡的容器高度必须是 `h-[85vh]` 的倍数关系** —— 容器太短会让最后一张卡还没展开就被推走。
5. **`prefers-reduced-motion` 下 AnimatedText 要渲染成普通文本** —— 不能只关动画，否则字符会是 opacity 0.2 的残影。
