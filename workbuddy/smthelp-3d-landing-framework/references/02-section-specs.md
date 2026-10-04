# 02 · 8 段区块详细规格

> 这些规格已经固化在 `templates/prompt-master-EN.md` 里。
> 本文件是**可读的说明版**，用于理解每个数值为什么这么定。改版式时先读这里，再改模板。

## 全局

```
背景 #0B0E0F → html, body, #root, main wrapper
字体 'Archivo' 300–900（Google Fonts）
正文色 #D7E2EA
全局 reset: box-sizing border-box, margin 0, padding 0
main wrapper: overflowX: 'clip'

.hero-heading:
  background: linear-gradient(180deg, #5C6E73 0%, #D9E4EA 100%)
  -webkit-background-clip: text
  -webkit-text-fill-color: transparent
```

首屏高度一律 `100svh`，**不用 `100vh`**——移动端 LinkedIn / 微信内置浏览器地址栏收起时会跳。

---

## 1 · HERO SECTION

`min-h-[100svh]`，flex column，`overflowX: clip`。

- **Navbar**：5 链接 `Overview / Specs / ROI / Applications / Quote`，`justify-between`。
  左 `SMThelp` 字标，右 `CE Certified` 小标。
  文字 `#D7E2EA` / font-medium / uppercase / tracking-wider / `text-sm md:text-lg lg:text-[1.4rem]` / `px-6 md:px-10 pt-6 md:pt-8` / hover opacity 70% 200ms。
- **Eyebrow**：`[PROCESS] // [CATEGORY]`。`#90C641` / font-mono / uppercase / `tracking-[0.3em]` / `text-xs`。
- **Hero Heading**：`[MODEL]`，`.hero-heading`，font-black / uppercase / tracking-tight / leading-none / whitespace-nowrap / w-full。
  字号 `text-[13vw] sm:text-[14vw] md:text-[15vw] lg:text-[16vw]`
  → **比原框架的 17.5vw 小**：人名是短的，机型号是长的（`S-WS450` 7 字符 vs `azou` 4 字符）。
  `mt-6 sm:mt-4 md:-mt-5`，外层 overflow-hidden（让渐显从下方"浮起"）。
- **Bottom bar**：`flex justify-between items-end pb-7 sm:pb-8 md:pb-10`
  - 左：`[ONE_LINER]`，`#D7E2EA` / font-light / uppercase / tracking-wide / leading-snug / `clamp(0.75rem, 1.4vw, 1.5rem)` / `max-w-[220px] sm:max-w-[280px] md:max-w-[340px]`
  - 右：`QuoteButton`
- **Hero 设备主视觉**：`Magnet` 包裹（padding 150 / strength 3 / in `0.3s ease-out` / out `0.6s ease-in-out`）
  `absolute left-1/2 -translate-x-1/2 z-10`，`w-[300px] sm:w-[420px] md:w-[560px] lg:w-[680px]`
  移动端 `top-1/2 -translate-y-1/2`；`sm+` → `sm:top-auto sm:translate-y-0 sm:bottom-0`
  - 素材优先级：① 3/4 视角去背 PNG/WebP ② 运行 MP4（muted/loop/playsInline，≤2 MB）+ WebP poster ③ SolidWorks / KeyShot 渲染
  - **禁止**抽象 3D 卡通形象、发光粒子等装饰素材
- **Hotspot**：3 个绝对定位圆点，`#90C641`，2s 脉冲，hover 展开标签
- **FadeIn 时序**：navbar 0 (y -20) / eyebrow 0.1 / heading 0.15 (y 40) / 左文字 0.35 (y 20) / 按钮 0.5 (y 20) / 设备 0.6 (y 30)
  → 设备最后出场，形成"字先立住，机器再浮起"的层级

## 2 · TRUST MARQUEE

背景 `#0B0E0F`，`pt-24 sm:pt-32 md:pt-40 pb-10`。

- Row 1 向右 `translateX(offset - 200)`；Row 2 向左 `translateX(-(offset - 200))`
- `offset = (window.scrollY - sectionTop + window.innerHeight) * 0.25`
- 素材三倍复制实现无缝循环
- Tile `420 × 270`，`rounded-2xl`，`object-cover`，lazy load，gap-3
- 下方 mono 小字跑马灯（重复 3 次）：
  `CE CERTIFIED · SHENZHEN FACTORY SINCE 2011 · 24-48H REMOTE DIAGNOSTICS · GLOBAL FIELD SERVICE`
- `willChange: 'transform'`，listener `{ passive: true }`

## 3 · PROCESS SECTION

`min-h-screen`，`px-5 sm:px-8 md:px-10 py-20`，居中。

- **四角技术标注卡**（不是 3D 装饰图标）：
  1px border `rgba(217,228,234,0.15)` / `rounded-xl` / `px-4 py-3` / font-mono `text-xs` / 标签 `#D7E2EA`、数值 `#90C641`

  | 位置 | FadeIn |
  |---|---|
  | Top-left `[CORNER_1]` | delay 0.1, x -80, duration 0.9 |
  | Bottom-left `[CORNER_2]` | delay 0.25, x -80, duration 0.9 |
  | Top-right `[CORNER_3]` | delay 0.15, x 80, duration 0.9 |
  | Bottom-right `[CORNER_4]` | delay 0.3, x 80, duration 0.9 |

- **标题**：`[PROCESS]`，`.hero-heading`，font-black / uppercase / centered / `clamp(2.6rem, 9vw, 130px)`
  → 比原框架 12vw 小，工业工艺名（`Wave Soldering`）比人名长
- **字符渐显段落**：`[NARRATIVE]`，两句，**不放参数**
  `#D7E2EA` / font-medium / centered / leading-relaxed / `max-w-[620px]` / `clamp(1rem, 2vw, 1.35rem)`
  逐字符 opacity `0.2 → 1`，`useScroll` offset `['start 0.8', 'end 0.2']`
- **3 个 StatCard**（cycle / accuracy / changeover）。未确认的值写 `On request`
- **QuoteButton**。间距：标题→文字 `gap-10 sm:gap-14 md:gap-16`，文字→按钮 `gap-16 sm:gap-20 md:gap-24`

## 4 · SPECS SECTION（浅色）

背景 `#FFFFFF`，`rounded-t-[40px] sm:rounded-t-[50px] md:rounded-t-[60px]`，`px-5 sm:px-8 md:px-10 py-20 sm:py-24 md:py-32`。

- 标题 `Specifications`，`#0B0E0F`，font-black / uppercase / centered / `clamp(2.6rem, 9vw, 130px)`，`mb-16 sm:mb-20 md:mb-28`
- 行布局（`max-w-5xl` 居中）：
  - 左编号：`font-black clamp(3rem, 10vw, 140px)`，`#0B0E0F`
  - 中参数名：`font-medium uppercase clamp(1rem, 2.2vw, 2.1rem)`；下方描述 `font-light opacity 0.6 clamp(0.85rem, 1.6vw, 1.25rem)`
  - 右数值：`font-mono font-semibold clamp(0.95rem, 1.8vw, 1.4rem)`，`#0AA5A5`
  - 分隔线 1px `rgba(11,14,15,0.15)`，`py-8 sm:py-10 md:py-12`
  - Stagger FadeIn：`delay = i * 0.1`
- **溯源规则**：数值只取已确认锚点；表外写 `On request`
- 脚注：`Final specifications per the official technical datasheet.`
- 底部灰底条：`Recommended pairing: [PAIRING]`（PAIRING 为空时脚本自动删整行）

## 5 · ROI SECTION

背景 `#0B0E0F`，`rounded-t-[40/50/60px]`，`-mt-10 sm:-mt-12 md:-mt-14 z-10`。

- 标题 `Why it pays back`
- 三卡 `sm:grid-cols-3`，卡样式 1px border `rgba(217,228,234,0.18)` / `rounded-3xl` / `p-8` / hover `border-[#0AA5A5]` 300ms

  | 卡 | 大字 | 标签 | 说明 |
  |---|---|---|---|
  | A | `30-50%` `#90C641` | CapEx vs Japanese lines | Budget range versus Fuji / Yamaha / Panasonic equivalents. Final quote depends on process options. |
  | B | `2-3 yrs` | Typical payback | Based on replaced manual or legacy stations at your local labour cost. |
  | C | `24-48 h` | Service response | Remote diagnostics plus global on-site support. |

- **报价熔断条**：三问（PCB 尺寸范围 / 目标产能 / 现有线体品牌与 feeder 型号）
- ⚠️ **全页禁止最终价格**

## 6 · APPLICATION STACK

背景 `#0B0E0F`。3 张 sticky 叠卡。

- `targetScale = 1 - (totalCards - 1 - index) * 0.03`，每张 `top: ${index * 28}px`
- 容器 `h-[85vh]`，卡 `sticky top-24 md:top-32`
- 卡：`rounded-[40/50/60px]` / `border-2 #D7E2EA`（hover `#90C641`）/ bg `#0B0E0F` / `p-4 sm:p-6 md:p-8`
- 顶行：编号（同 Specs 大字）+ 行业标签 + 场景名 + `View Case` ghost 按钮
- 底行：左列 40%（两图，`clamp(130px,16vw,230px)` / `clamp(160px,22vw,340px)`），右列 60%（一高图）
- **图片必须是真实产线/焊点/板卡照片**，禁 Unsplash 抽象科技图

## 7 · FAQ SECTION（浅色）

背景 `#FFFFFF`，`rounded-t-[40/50/60px]`，6 问手风琴：

1. Can it interface with our existing Yamaha / JUKI / Panasonic line?
2. What is the lead time, and what does installation include?
3. Do you provide CE documentation?
4. How are spare parts supplied, and what do they cost?
5. Is on-site commissioning and operator training included?
6. What do you need from us to prepare a quote?

第 6 问的答案直接放**强制 CTA 两行原文**。

## 8 · QUOTE SECTION + FOOTER

深色。左：询盘表单（Name / Company / Country / PCB size range / Target throughput / Existing line brand / Message）。右：联系块。

强制 CTA 两行原文 + Footer：

```
www.SMThelp.com | info@smthelp.com | WhatsApp +86 13602562576
Shenzhen, China · Since 2011 | CE
```

移动端：`position: sticky; bottom: 0` 底栏，bg `#0AA5A5`，`WhatsApp +86 13602562576`。
