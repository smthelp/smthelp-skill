# 主模板（唯一真源 / Single Source of Truth）

> **不要直接改本文件来适配某个机型。** 改这里会影响所有机型。
> 机型内容一律写到 `../machines/<MODEL>.json`，再用 `scripts/build_prompt.py` 生成。
> 只有「版式 / 区块 / 动效 / 品牌规范」这类**全局改动**才改本文件，改完必须同步 `CHANGELOG.md` 并升版本号。

## 使用

```bash
# 列出所有可用机型
python3 scripts/build_prompt.py --list

# 生成 S-WS450 的 prompt（打印到 stdout）
python3 scripts/build_prompt.py --model S-WS450

# 生成并落盘
python3 scripts/build_prompt.py --model S-WS450 --out ~/Desktop/S-WS450-prompt.md

# 批量生成全部机型
python3 scripts/build_prompt.py --all --out-dir ~/Desktop/sm-lp-prompts
```

---

<!-- BEGIN PROMPT -->

Build a 3D industrial product landing page for "[MODEL]" using React, TypeScript, Tailwind CSS, Framer Motion, and Lucide React. The page is for Southern Machinery, a Shenzhen-based SMT/THT assembly equipment manufacturer selling to overseas EMS and ODM factories. Audience: production engineers and purchasing managers. Dark industrial theme, credibility-first — real machine imagery, no abstract 3D characters or decorative particles.

GLOBAL STYLES
Background: #0B0E0F on html, body, #root, and the main wrapper
Font family: 'Archivo', sans-serif (Google Fonts, weights 300-900)
Body text color: #D7E2EA
Accent teal: #0AA5A5 (links, spec values, focus states)
Accent green: #90C641 (numbers, hotspot dots, highlights)
Global reset: box-sizing border-box, margin 0, padding 0
CSS class .hero-heading: gradient text using background: linear-gradient(180deg, #5C6E73 0%, #D9E4EA 100%) with -webkit-background-clip: text and -webkit-text-fill-color: transparent
Main wrapper has overflowX: 'clip'
First-screen height uses 100svh (never 100vh)

SECTION ORDER
HeroSection
TrustMarquee
ProcessSection
SpecsSection
RoiSection
ApplicationStack
FaqSection
QuoteSection

1. HERO SECTION
min-h-[100svh], flex column layout with overflowX: clip.
Navbar: horizontal nav with 5 links -- "Overview", "Specs", "ROI", "Applications", "Quote" -- justify-between. Left side shows the "SMThelp" wordmark, right side shows a small "CE Certified" badge. Text color #D7E2EA, font-medium, uppercase, tracking-wider. Sizes: text-sm md:text-lg lg:text-[1.4rem]. Padding: px-6 md:px-10 pt-6 md:pt-8. Hover: opacity 70% with 200ms transition.
Eyebrow line above the heading: "[PROCESS] // [CATEGORY]" in #90C641, font-mono, uppercase, tracking-[0.3em], text-xs.
Hero Heading: massive h1 with the text "[MODEL]". Uses .hero-heading gradient. font-black, uppercase, tracking-tight, leading-none, whitespace-nowrap, w-full. Sizes: text-[13vw] sm:text-[14vw] md:text-[15vw] lg:text-[16vw]. Margin top: mt-6 sm:mt-4 md:-mt-5. Wrapped in overflow-hidden container.
Bottom bar: flex justify-between items-end with pb-7 sm:pb-8 md:pb-10.
  Left: paragraph "[ONE_LINER]", color #D7E2EA, font-light, uppercase, tracking-wide, leading-snug. Font size: clamp(0.75rem, 1.4vw, 1.5rem). Max-width: max-w-[220px] sm:max-w-[280px] md:max-w-[340px].
  Right: QuoteButton component (see REUSABLE COMPONENTS).
Hero Machine Visual: centered absolutely. Uses a Magnet component (mouse-following magnetic effect, padding 150, strength 3, activeTransition "transform 0.3s ease-out", inactiveTransition "transform 0.6s ease-in-out") wrapping the machine media ([HERO_MEDIA]: 3/4-view cut-out render, or muted looping MP4 with WebP poster, under 2MB). Positioning: absolute left-1/2 -translate-x-1/2 z-10. Width: w-[300px] sm:w-[420px] md:w-[560px] lg:w-[680px]. On mobile: top-1/2 -translate-y-1/2. On sm+: sm:top-auto sm:translate-y-0 sm:bottom-0.
Hotspots: 3 absolutely positioned dots on the machine visual in #90C641 with a 2s pulse animation. On hover each expands into a label: [HOTSPOT_1], [HOTSPOT_2], [HOTSPOT_3].
FadeIn animations: navbar delay 0 (y -20); eyebrow 0.1; heading 0.15 (y 40); left text 0.35 (y 20); Quote button 0.5 (y 20); machine visual 0.6 (y 30).

2. TRUST MARQUEE
Two rows of real machine media that scroll horizontally based on scroll position. Background #0B0E0F. Padding: pt-24 sm:pt-32 md:pt-40 pb-10.
Content: [MARQUEE_MEDIA] -- real production footage only (process close-ups, boards exiting, feeding action, HMI screens, operator loading). Never abstract 3D motion graphics.
Row 1: first half of the media, tripled for seamless scrolling. Moves RIGHT: translateX(offset - 200).
Row 2: second half, tripled. Moves LEFT: translateX(-(offset - 200)).
Scroll offset: (window.scrollY - sectionTop + window.innerHeight) * 0.25
Each tile: 420px x 270px, rounded-2xl, object-cover, lazy loaded. Gap between tiles: gap-3. Gap between rows: gap-3.
Below the rows: a single-line mono marquee repeated 3 times -- "CE CERTIFIED · SHENZHEN FACTORY SINCE 2011 · 24-48H REMOTE DIAGNOSTICS · GLOBAL FIELD SERVICE".
Uses willChange: 'transform'. Scroll listener is passive.

3. PROCESS SECTION
Full-height centered section, min-h-screen, padding px-5 sm:px-8 md:px-10 py-20.
Four technical callout cards positioned absolutely in corners. Style: 1px border rgba(217,228,234,0.15), rounded-xl, px-4 py-3, font-mono text-xs, label in #D7E2EA and value in #90C641.
  Top-left: [CORNER_1] -- FadeIn delay 0.1, x -80, duration 0.9
  Bottom-left: [CORNER_2] -- FadeIn delay 0.25, x -80, duration 0.9
  Top-right: [CORNER_3] -- FadeIn delay 0.15, x 80, duration 0.9
  Bottom-right: [CORNER_4] -- FadeIn delay 0.3, x 80, duration 0.9
Heading: "[PROCESS]" using .hero-heading, font-black, uppercase, centered. Font size: clamp(2.6rem, 9vw, 130px). FadeIn delay 0, y 40.
Animated paragraph: character-by-character scroll-driven opacity animation, opacity 0.2 to 1, useScroll offset ['start 0.8', 'end 0.2']. Text: "[NARRATIVE]" -- two short sentences, process story only, NO spec numbers. Color #D7E2EA, font-medium, centered, leading-relaxed, max-w-[620px], font size clamp(1rem, 2vw, 1.35rem).
Below the paragraph: 3 StatCards (cycle / accuracy / changeover). If a value is not confirmed, render "On request" instead of a number.
QuoteButton below. Gap heading-to-text: gap-10 sm:gap-14 md:gap-16. Gap text-to-button: gap-16 sm:gap-20 md:gap-24.

4. SPECS SECTION
White background (#FFFFFF), rounded-t-[40px] sm:rounded-t-[50px] md:rounded-t-[60px]. Padding: px-5 sm:px-8 md:px-10 py-20 sm:py-24 md:py-32.
Heading: "Specifications" in #0B0E0F, font-black, uppercase, centered, clamp(2.6rem, 9vw, 130px). Margin bottom: mb-16 sm:mb-20 md:mb-28.
Numbered spec rows, max-w-5xl, centered. Each row has three parts:
  Left: index number, font-black, clamp(3rem, 10vw, 140px), color #0B0E0F
  Middle: spec name, font-medium, uppercase, clamp(1rem, 2.2vw, 2.1rem); short description below in font-light, opacity 0.6, clamp(0.85rem, 1.6vw, 1.25rem)
  Right: value, font-mono, font-semibold, clamp(0.95rem, 1.8vw, 1.4rem), color #0AA5A5
Rows separated by 1px borders rgba(11,14,15,0.15). Padding: py-8 sm:py-10 md:py-12. Staggered FadeIn: delay i * 0.1.
Spec rows:
[SPEC_01]
[SPEC_02]
[SPEC_03]
[SPEC_04]
[SPEC_05]
[SPEC_06]
[SPEC_07]
Never invent a number. Any unconfirmed value MUST render as "On request".
Footnote under the list: "Final specifications per the official technical datasheet."
Bottom grey note bar: "Recommended pairing: [PAIRING]"

5. ROI SECTION
Dark background (#0B0E0F), rounded-t-[40px] sm:rounded-t-[50px] md:rounded-t-[60px], pulled up with -mt-10 sm:-mt-12 md:-mt-14, z-10.
Heading: "Why it pays back" using .hero-heading.
Three-card grid (sm:grid-cols-3). Card style: 1px border rgba(217,228,234,0.18), rounded-3xl, p-8, hover border-[#0AA5A5] with 300ms transition.
  Card A -- big number "30-50%" in #90C641, label "CapEx vs Japanese lines", note "Budget range versus Fuji / Yamaha / Panasonic equivalents. Final quote depends on process options."
  Card B -- big number "2-3 yrs", label "Typical payback", note "Based on replaced manual or legacy stations at your local labour cost."
  Card C -- big number "24-48 h", label "Service response", note "Remote diagnostics plus global on-site support."
Below the cards, a bordered "quote qualification" strip asking three questions:
  1. PCB size range, double-sided or not, minimum component (0201 / 01005 / 0.4 mm pitch BGA)
  2. Target throughput (CPH or monthly board volume)
  3. Existing line brand (Yamaha / JUKI / Panasonic) and feeder models to interface with
NEVER display a final price anywhere on the page. Budget ranges only.

6. APPLICATION STACK
Dark background (#0B0E0F). 3 sticky-stacking cards that scale down as you scroll past them (Framer Motion useScroll and useTransform).
Scale: targetScale = 1 - (totalCards - 1 - index) * 0.03. Each card offset by top: ${index * 28}px. Each card is sticky top-24 md:top-32 inside an h-[85vh] container.
Card style: rounded-[40px] sm:rounded-[50px] md:rounded-[60px], border-2 border-[#D7E2EA] (hover: #90C641), background #0B0E0F, padding p-4 sm:p-6 md:p-8.
Card layout:
  Top row: index number (huge, same style as specs), industry label, scenario name, and a "View Case" ghost button.
  Bottom row: two-column image grid -- left column (40% width) has 2 stacked images, right column (60%) has 1 tall image. All rounded-[40px] sm:rounded-[50px] md:rounded-[60px]. Left top image height: clamp(130px, 16vw, 230px). Left bottom image height: clamp(160px, 22vw, 340px).
  Images must be real production or board photos. No stock abstract technology imagery.
Applications:
  01 - [APP_01]
  02 - [APP_02]
  03 - [APP_03]

7. FAQ SECTION
White background (#FFFFFF), rounded-t-[40px] sm:rounded-t-[50px] md:rounded-t-[60px]. Accordion with 6 items:
  1. Can it interface with our existing Yamaha / JUKI / Panasonic line?
  2. What is the lead time, and what does installation include?
  3. Do you provide CE documentation?
  4. How are spare parts supplied, and what do they cost?
  5. Is on-site commissioning and operator training included?
  6. What do you need from us to prepare a quote?
Answers must stay factual and bounded. Do not promise anything unconfirmed. Item 6 answer contains the mandatory CTA text (see below) verbatim.

8. QUOTE SECTION
Dark background. Left column: inquiry form with fields Name / Company / Country / PCB size range / Target throughput / Existing line brand / Message. Right column: contact block.
Mandatory CTA block, rendered verbatim, never rewritten:
"Note: This configuration is a draft and must be finalized and reviewed by our senior Sales Engineer (Jason Wu)."
"Action Required: Please provide your Gerber file or PCB drawings to info@smthelp.com for an accurate capacity simulation and nozzle engineering validation."
Footer: www.SMThelp.com | info@smthelp.com | WhatsApp +86 13602562576 | Shenzhen, China · Since 2011 | CE
Mobile: sticky bottom bar, background #0AA5A5, text "WhatsApp +86 13602562576".

REUSABLE COMPONENTS
QuoteButton: rounded-full pill button, gradient background linear-gradient(123deg, #06282A 7%, #0AA5A5 37%, #6FA832 72%, #90C641 100%), inner box-shadow 0px 4px 4px rgba(10,165,165,0.25), 4px 4px 12px #0AA5A5 inset, white 2px outline with -3px offset. Text: white, font-medium, uppercase, tracking-widest. Sizes: px-8 py-3 sm:px-10 sm:py-3.5 md:px-12 md:py-4, text text-xs sm:text-sm md:text-base. Label: "Request a Quote".
ViewCaseButton: ghost pill. rounded-full, border-2 border-[#D7E2EA], text #D7E2EA, font-medium, uppercase, tracking-widest. px-8 py-3 sm:px-10 sm:py-3.5, text-sm sm:text-base. Hover: bg-[#D7E2EA]/10. Label: "View Case".
Magnet: mouse-following magnetic hover effect. Tracks mouse position relative to element center, applies translate3d divided by strength. Activates within padding distance. Transitions 0.3s ease-out in / 0.6s ease-in-out out. willChange: 'transform'.
FadeIn: Framer Motion wrapper using whileInView with viewport={{ once: true, margin: "50px", amount: 0 }}. Accepts delay, duration (default 0.7), x (default 0), y (default 30). Easing [0.25, 0.1, 0.25, 1]. Uses motion.create() for dynamic element types.
AnimatedText: character-by-character scroll-reveal, opacity 0.2 to 1, useScroll offset ['start 0.8', 'end 0.2']. For narrative sentences only -- never for spec numbers.
Hotspot: absolutely positioned dot on the machine visual, #90C641, 2s pulse, expands to a label on hover.
Marquee: scroll-driven bidirectional row, passive listener, willChange: 'transform'.

KEY DEPENDENCIES
react, react-dom (^18.3.1); framer-motion (^12.38.0); lucide-react (^0.344.0); tailwindcss (^3.4.1); vite; typescript.

RESPONSIVE BREAKPOINTS
Tailwind default breakpoints (sm 640px, md 768px, lg 1024px), mobile-first. Heavy use of clamp() for fluid typography. First-screen height uses 100svh.

PERFORMANCE AND FALLBACKS
Hero video: MP4 (H.264) with WebP poster, muted loop playsInline, under 2MB. GIFs only in the marquee, each under 400KB.
All scroll listeners passive. willChange: 'transform' on animated elements.
prefers-reduced-motion: disable Magnet, marquee translation, and character animation (render text at full opacity).
Lazy-load every non-first-screen image. Target LCP under 2.5s.
No-JS fallback: Specs and FAQ must remain readable (use native details elements or render expanded by default).

COPY RULES
Keep SMT/THT terms in English, never translate: Wave Soldering, Preheat, Solder Pot, Flux, Dross, Conveyor, PCB, THT, SMD, CPH, UPH, Odd-form, Magazine, Feeder, Nozzle, Pitch.
Never mix CPH (components per hour) with UPH (boards per hour).
Money in USD only.
Banned filler words: efficient, intelligent, excellent, leading, world-class, perfect, revolutionary, game-changing, cutting-edge. Replace every adjective with a number, a condition, or a result.
No emoji stacks, no exclamation marks, no consumer-hype tone. The reader is a process engineer.

<!-- END PROMPT -->

---

## 占位符契约

`scripts/build_prompt.py` 会把 `[KEY]` 替换成 `machines/<MODEL>.json` 里 `fields.KEY` 的值。

| 占位符 | 必填 | 为空时的行为 |
|---|---|---|
| `MODEL` / `PROCESS` / `CATEGORY` / `ONE_LINER` / `NARRATIVE` | ✅ | 报错，停止生成 |
| `HOTSPOT_1..3` / `CORNER_1..4` / `APP_01..03` | ✅ | 报错，停止生成 |
| `SPEC_01..07` | ✅ | 报错，停止生成（不足 7 条就写 `On request` 占位行） |
| `HERO_MEDIA` / `MARQUEE_MEDIA` | ✅ | 报错，停止生成 |
| `PAIRING` | ➖ | 留空 → 脚本自动删除整行 `Bottom grey note bar` |
