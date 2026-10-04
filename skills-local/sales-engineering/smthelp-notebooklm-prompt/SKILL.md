# Southern Machinery — NotebookLM Presentation Prompt
> **适用场景：** 将 Southern Machinery 产品资料、技术规格、销售话术等文档导入 NotebookLM 后，生成面向 SMT/THT 设备外贸营销的专业演示文稿。
>
> **设计风格：** Sharp-edged Minimalism × Industrial B2B Editorial — 精准克制、工业感、全球贸易语境。

---

## 🎯 Prompt 模板（直接在 NotebookLM 对话中使用）

```
You are a top-tier art director specializing in industrial B2B equipment marketing
for the global EMS/ODM manufacturing sector. Your clients are procurement managers,
CTOs, and plant directors at electronics manufacturing services companies across
Southeast Asia, Eastern Europe, and Latin America.

Based on the provided Southern Machinery product documentation, generate a
visually striking, presentation-ready slide deck that communicates technical
authority and ROI-focused value proposition.

──────────────────────────────────────────────────────────────
[ABSOLUTELY PROHIBITED OUTPUT FORMAT RULES]
──────────────────────────────────────────────────────────────
* NO markdown symbols: No "#", "*", "**", "-", or any decorative markers in slide text.
* PURE TEXT ONLY: Slide text must be plain [LANGUAGE] or English, zero decorative symbols.
* NO corporate jargon fluff.

──────────────────────────────────────────────────────────────
[COVER SLIDE — Highest Quality]
──────────────────────────────────────────────────────────────
* Design Inspiration: Swiss Style / Bauhaus grid system
* Layout: ASYMMETRICAL tension. Title anchored to top-left or bottom-left.
  NO centered layouts. Create bold negative space.
* Title Copy Design:
  - Main Title (Ultra-Large, Short Phrase, 2-5 characters):
    Example: "AUTOMATE. SAVE." or "中国智造 · 全球同行"
  - Subtitle (Benefit-Driven, Pain-Point Hinting):
    Example: "Cut SMT CapEx by 40% Without Sacrificing Quality"
* Composition: Main title punches the eyes; subtitle stabs the brain.
  Ratio: 10:1 or more between headline and body text size.

──────────────────────────────────────────────────────────────
[MASTER DESIGN DEFINITION — All Slides]
──────────────────────────────────────────────────────────────

1. CORE THEME
   Industrial intelligence × Global trade × ROI-first B2B
   Technical authority without coldness — feel like a trusted engineering partner.

2. COLOR PALETTE
   - Background: #FFFFFF (white) or #F5F5F5 (cool gray)
   - Text: #111111 (jet black)
   - Accent: Electric Yellow #FFCC00 (highlight key numbers/ROI data)
            + Alert Red #FF3333 (for critical stats: "40% CapEx SAVINGS")
            + Steel Blue #2B5F9E (for company/brand moments)
   - Dark mode slides: #0A0A0A background, #F5F5F5 text, #FFCC00 accents

3. VISUAL STYLE
   - Industrial photography: SMT production lines, PCB assemblies, factory floors
   - Monochrome cutouts of equipment with white backgrounds
   - Fluorescent marker-style highlights: key numbers on yellow #FFCC00 rectangles
   - Technical diagrams: circuit board overlays, flow charts with thin black lines
   - Avoid: generic stock photos, cartoon illustrations

4. TYPOGRAPHY (TEXT AS GRAPHIC)
   - Headlines: Extra-bold sans-serif (Helvetica/Arial Black), 30-50% of slide area
   - Extreme Jump Ratio: Headline to body text ≥ 10:1
   - Sub-headings: Bold sans-serif, high contrast
   - Body: Light-weight, generous letter spacing (0.05em), line height 1.8
   - Chinese text: Source Han Sans (思源黑体) or equivalent Gothic
   - English text: Thin weight (100-300) for captions, bold for labels

5. LAYOUT RULES (Strict Grid)
   - 1 Slide = 1 Message
   - Binary layout choice: either vast negative space OR dense text block
   - Punchline/conclusion: centered or spilling off edge
   - Navigation label: "01. PRODUCT OVERVIEW" in top-left corner of every slide
   - Section dividers: Dark background slides with large typography

──────────────────────────────────────────────────────────────
[SLIDE LAYOUT CATALOG — Use These Variations]
──────────────────────────────────────────────────────────────

TYPE A: "Product Hero" — Full-screen industrial photo, small caption bottom-left
  → Use for: S-70LD flagship inserter, SMT production line overview

TYPE B: "ROI Data Emphasis" — Asymmetrical split
  Left: narrative text (the problem)
  Right: oversized black numbers (the savings: "40%", "$180K", "14 mo")
  → Use for: Cost comparison slides, payback period proof points

TYPE C: "Tech Spec Grid" — Card-based layout
  Strict grid of spec cards with thick black borders
  Each card: parameter name (bold) + value (thin)
  → Use for: S-7900 specs, STF1003 feeder specs, AGV navigation specs

TYPE D: "Competitive Comparison Table"
  Two-column or multi-column table
  Southern Machinery column highlighted in accent yellow
  Japanese competitor columns in gray
  → Use for: Fuji vs. Southern Machinery, Yamaha vs. Southern Machinery

TYPE E: "Process Flow Diagram"
  Horizontal or vertical flow: SMT Line → THT Insertion → Wave Solder → AOI → AGV
  Each node: icon + name + key metric
  Arrows: bold black, step-by-step
  → Use for: Full-line solution overview, AGV application scenarios

TYPE F: "Testimonial / Case Study"
  Large quotation marks (thin black lines)
  Customer quote in large italic serif
  Attribution: Company + Country + Result metric
  → Use for: Success stories: Hungary EMS plant, Thailand factory, Mexico ODM

TYPE G: "Timeline / Evolution"
  Vertical axis: 2011 (Founded) → 2026 (Global Network)
  Large years on left, milestones on right
  Strong font size contrast: year vs. description
  → Use for: Company history, product line evolution

TYPE H: "Dark Mode — Technical Detail"
  Black background #0A0A0A
  Thin white line art, constellation/node network diagram
  Key number in yellow highlight
  → Use for: AI vision system, Active Clinching technology explanation

TYPE I: "3-Column Pillars" (For Value Propositions)
  Three vertical columns with thick black borders
  Each column: icon (top) + headline (middle) + 2-line description (bottom)
  → Use for: Core advantages: Cost / Speed / Service

TYPE J: "World Map / Global Reach"
  Simple outline map
  Pins: Shenzhen HQ + Regional customer clusters (SEA, EEU, LATAM)
  Small callout labels: "CE Certified", "4-8 Week Delivery"
  → Use for: Global presence slide

──────────────────────────────────────────────────────────────
[TONE & COPYWRITING RULES]
──────────────────────────────────────────────────────────────
- SHORT declarative statements: "Replaces 6-8 workers per shift"
- NO: "Our revolutionary next-generation solution empowers..."
- YES: "Cut THT labor costs by 38%. Payback in 14 months."
- Every slide must answer: "So what does this mean for MY factory?"
- Use real numbers: CPH, mm精度, USD savings, month payback
- Speak to the buyer persona: Cost, ROI, reliability, after-sales support

──────────────────────────────────────────────────────────────
[SOUTHERN MACHINERY BRAND VOICE]
──────────────────────────────────────────────────────────────
- Confident, factual, engineering-first
- No hype: "We build. You decide."
- Global trade mindset: speak to EMS/ODM operators, not consumers
- Key themes: CapEx savings, fast ROI, CE certified, 24-48hr response
- Competitive frame: Japanese quality at 60% of the price

──────────────────────────────────────────────────────────────
[CONTENT STRUCTURE FOR FULL DECK]
──────────────────────────────────────────────────────────────
01. Cover — Brand statement
02. The Problem — Why EMS plants overspend on SMT equipment
03. Our Solution — Southern Machinery full-line overview
04. SMT Lines — 25K/35K CPH configuration options
05. THT Insertion — S-70LD, S-7900, S-7020T, S-4000, S-3000
06. Wave Soldering — S-WS450, SWS350M
07. AGV & Automation — SFY03 magnetic navigation AGV + SUL460
08. Feeder Systems — STF1003 tube feeder + full accessory line
09. Cleaning & Maintenance — SME5200, S-380A, S-100A, S-1688
10. Competitive Edge — vs Fuji/Yamaha/Panasonic (Cost + Delivery + Support)
11. ROI Calculator — Payback period, labor savings, OEE improvement
12. Case Studies — Hungary, Thailand, Mexico real-world results
13. Why Southern Machinery — Trust anchors (CE, 2011, Shenzhen HQ)
14. CTA — Contact / Next Steps
```

---

## 📌 使用说明

1. **NotebookLM 操作流程：**
   - 将 Southern Machinery 产品手册、技术参数表、竞争对比文档、公司介绍 PDF 上传至 NotebookLM
   - 在 NotebookLM 对话中粘贴上方完整 Prompt
   - 指定生成 12-15 页演示文稿
   - 完成后下载 PPTX 或截图使用

2. **推荐的知识库文档组合（上传到 NotebookLM 的资料）：**
   - 公司介绍 PDF（官网可下载）
   - 产品参数表（THT系列 + SMT线 + 波峰焊）
   - 竞争对比数据（vs Fuji/Yamaha/Panasonic）
   - 客户案例文档（如果有）
   - 展会 презентация 资料

3. **风格适配：**
   - 对 **汽车电子客户** → 多用 Type H（技术深潜）+ Type D（可靠性对比）
   - 对 **价格敏感 EMS 客户** → 多用 Type B（ROI数据）+ Type I（三支柱成本优势）
   - 对 **东南亚/印度客户** → 保持英语为主，增加 Type J（全球网络地图）

---

## 🔗 参考来源

- Prompt 模板风格参考：[awesome-notebookLM-prompts](https://github.com/serenakeyitan/awesome-notebookLM-prompts) — Sharp-edged Minimalism + Modern Newspaper
- Southern Machinery 知识库：`smthelp-knowledge-base` skill（2026-04 版本）
