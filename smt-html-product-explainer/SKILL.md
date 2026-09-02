---
name: smt-html-product-explainer
description: "Generate animated self-contained HTML explainer pages (popular-science / line walkthrough / product showcase) for SMT + THT solutions. Two variants available. Standard 7-section product explainer (Hero, Challenge, Math, Line flow, Specs, Why-us, CTA) for B2B sales documents. Sci-pop anime storybook (multi-chapter narrative with character profiles, dialogue quips, AI art prompts) for viral popular-science content. Triggers when the user asks for an HTML animated explainer / shareable line configuration page / interactive product walkthrough / anime storybook / 动画科普介绍 / 动画科普绘本 in HTML format for a specific SMT/THT solution. Output is a single self-contained .html file (CSS + JS inlined, no build step, no external dependencies beyond an image URL or two). Uses PCB dark theme, SVG process flow / character scenes, scroll-reveal animations with html.js class gate, animated KPI counters with M/K suffix, and SPIN-selling questions at the end."
whenToUse: "生成 [产品/方案] 的HTML动画科普介绍，make me an animated explainer for [solution]，interactive line walkthrough for [machine family]，shareable HTML page showing [product] solution，popular science page for [SMT/THT topic]，生成 [产品/方案] 的动画科普绘本，anime storybook for [SMT/THT vertical]，sci-pop version of [explainer topic]，export to PDF，PDF version，发PDF版，PDF for LinkedIn / LinkedIn attachment，PDF attachment / 邮件附件 / 打印版，convert this HTML to PDF，Chrome headless print-to-pdf"
metadata:
  source: hermes
  origin: "marketing/smt-html-product-explainer"
---
## 技能指令（Skill Instructions）

When generating SMT/THT animated HTML explainers for Southern Machinery:
- Use the PCB dark theme (deep navy #050a13 / #07091a, panel #0e1d33, cyan accent #00e5ff, neon-green highlight #39ff7a, pink #ff4d8d, purple #a56bff)
- Keep all industry terms in UPPERCASE English: SMT, THT, PCB, PCBA, CPH, Feeder, Nozzle, Reflow Oven, Wave Soldering, Pick and Place, SPI, AOI, MES
- Choose variant based on user request. Standard 7-section (Hero, Challenge cards, Math, SVG line flow, Specs, Why-us, CTA) for B2B sales. Sci-pop anime storybook (8-chapter narrative with character profiles, AI art prompts, dialogue quips) for popular-science content.
- For storybook use 8-chapter structure (Prologue, 6 line-station chapters, Epilogue), each chapter has Character Profile + Visual Scene + Tech+AI-prompt panels
- Footer MUST include LinkedIn Company, LinkedIn Profile, Twitter, Facebook, YouTube Channel + catalog link (file.autoinsertion.com) + photo gallery link (ph.smthelp.com) + Southern Machinery logo at top-left
- ALWAYS use the html.js class gate pattern for reveal. Default `.reveal { opacity: 1 }`, JS adds `html.js` then `.reveal { opacity: 0 }`. Plus a 2.5s setTimeout safety net. Screenshot tools, prefers-reduced-motion, and IO-blocking extensions all break naive IO patterns.
- KPI counters should use M/K suffix formatter (1200000 -> 1.2M, 30000 -> 30K)
- End with 2-4 SPIN questions (Situation, Problem, Implication, Need-payoff)
- Save to /Users/jasonwu/Downloads/{Topic_Snake_Case}.html


# SMT/THT Animated HTML Product Explainer

## When to Use

Generate a single-file, self-contained HTML page that visually explains an SMT or THT solution to a non-expert decision-maker. Typical use cases:

- Industry-vertical solution showcases (LED tube, automotive, appliance, power supply, telecom)
- Line configuration walkthroughs ("here's what a 1.2M pcs/month LED tube line looks like")
- "Popular science" pieces for LinkedIn / email / smthelp.com blog
- Sales follow-up collateral after a discovery call

These pages are **marketing + education hybrids** — they walk a prospect through the problem → math → machine lineup → why-us → CTA, then drop SPIN questions to keep the conversation going.

## Standard Section Structure

Always build the page in this 7-section order. Skipping or reordering breaks the sales-engineer narrative flow.

1. **Hero** — gradient title, 1-line value prop, 4 animated KPI counters (e.g. target output, line capacity, yield, payback)
2. **The Challenge** — 3 cards covering the 3 specific pain points of the vertical (e.g. long-board handling, thermal-sensitive MCPCB, component mix)
3. **The Math** — back-calculated capacity formula with CPH_required, OEE assumptions, per-machine sizing. Engineers love seeing the work.
4. **The Line** — animated SVG process flow (Loader → Printer → Pick and Place → SPI → Reflow Oven → AOI → Unloader), with a dashed off-line branch for THT / Wave Soldering if relevant
5. **Equipment Specs** — 4–6 spec cards with bullet lists of hard numbers (CPH, zones, accuracy, supported components)
6. **Why Southern Machinery** — 4 stat tiles (CapEx saved %, response time, 1-stop scope, CE certification)
7. **CTA + SPIN** — clear CTA button + 2 open-ended SPIN questions (Q1 = current state pain, Q2 = growth/bottleneck)

Plus **header** (logo top-left, tagline top-right) and **footer** (5 social links + catalog + photo gallery + copyright).

## Design System (PCB Dark Theme)

Hard-code these tokens. Don't improvise colors per page.

```
--bg:      #050a13   (deep navy)
--bg-2:    #0a1626   (panel base)
--panel:   #0e1d33   (card surface)
--line:    #13283f   (borders, dividers)
--text:    #cfe6ff   (body)
--muted:   #7fa3c7   (sub-text)
--accent:  #00e5ff   (cyan — primary highlight)
--accent-2:#39ff7a   (neon green — second highlight, used for "core" machines in flow)
--warn:    #ffb84d   (orange — used only for the off-line THT/Wave branch)
```

Background trick that sells the PCB aesthetic:

```css
body::before {
  content: "";
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background-image:
    linear-gradient(rgba(0,229,255,.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,229,255,.06) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse at center, #000 30%, transparent 80%);
}
```

Plus two radial-gradient color washes (cyan top-left, neon-green bottom-right) for depth.

## Animation Patterns (use all 3 — they reinforce each other)

### 1. Scroll-reveal via IntersectionObserver

The default CSS state of `.reveal` MUST be visible. Only when JS has confirmed
the IntersectionObserver is set up do we hide them. This is the **html.js class
gate** pattern — it makes the page no-JS-safe and screenshot-tool-safe.

```css
/* Default (no-JS): always visible. */
.reveal { opacity: 1; }

/* Only when JS is active: hide, then animate in. */
html.js .reveal { opacity: 0; transform: translateY(24px); transition: all .8s cubic-bezier(.2,.7,.2,1); }
html.js .reveal.in { opacity: 1; transform: none; }
```

```js
// Mark JS enabled FIRST — that's what activates the hiding CSS
document.documentElement.classList.add('js');

// Aggressive IO: threshold 0, rootMargin 0, no negative bottom
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0, rootMargin: '0px 0px -10% 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Safety net: 2.5s fallback force-reveals anything still hidden
// (screenshot tools, prefers-reduced-motion, short pages, all of them)
setTimeout(() => {
  document.querySelectorAll('.reveal:not(.in)').forEach(el => el.classList.add('in'));
}, 2500);
```

**CRITICAL pitfall — the missing-class bug:** If you write `.reveal { opacity: 0 }`
unconditionally, content stays hidden when:
- Screenshot tools load the page without scroll events
- prefers-reduced-motion disables transitions and IO callbacks
- The page is shorter than the viewport (everything is "above the fold" but
  the threshold + rootMargin combo still hides some)
- Browser extension / privacy mode blocks IO

**The html.js gate pattern fixes ALL of these.** Default = visible, JS = animate.
Combined with a 2.5s `setTimeout` safety net, the page degrades gracefully.

### 2. Animated KPI counters

```html
<div class="num" data-target="1200000">0<span class="unit">pcs/mo</span></div>
```

```js
function animateNum(el) {
  const target = parseFloat(el.dataset.target);
  const dur = 1600;
  const start = performance.now();
  // Format big numbers compactly: 1200000 → 1.2M, 30000 → 30K
  const fmt = v => v >= 1e6   ? (v/1e6).toFixed(1).replace(/\.0$/,'') + 'M'
                  : v >= 1e4  ? Math.round(v/1e3) + 'K'
                  : v >= 1e3  ? Math.round(v).toLocaleString()
                  : Number.isInteger(target) ? Math.round(v).toString()
                  : v.toFixed(1);
  const tick = now => {
    const p = Math.min(1, (now - start) / dur);
    const ease = 1 - Math.pow(1 - p, 3);
    // Write into the text node BEFORE the <span class="unit"> so the unit stays put
    el.firstChild.nodeValue = fmt(target * ease);
    if (p < 1) requestAnimationFrame(tick);
    // Snap to clean final value when done (avoid 1.2M → 1.2M glitch)
    else el.firstChild.nodeValue = fmt(target);
  };
  requestAnimationFrame(tick);
}
```

NOTE: `el.firstChild.nodeValue` is the text node BEFORE the `<span class="unit">` — that's how the unit stays put while the number animates. The M/K suffix formatter avoids ugly 1,200,000 strings in tight 4-stat-card layouts.

### 3. SVG process flow with dashed pulse + machine float

The hero visual. Each machine is a `<g class="machine">` with `animation-delay` staggered to create a wave effect. The connecting line is a separate stroke with `stroke-dasharray` + animated `stroke-dashoffset`:

```css
.flow .pulse { animation: flowDash 2.2s linear infinite; }
@keyframes flowDash { to { stroke-dashoffset: -36; } }
.machine { transform-origin: center; transform-box: fill-box; animation: machineFloat 3.4s ease-in-out infinite; }
@keyframes machineFloat { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
```

## SVG Process Flow Recipe

For a 7-station SMT line in a 1100×360 viewBox, station width 100, gap 40:

```
x-positions: 60, 200, 340, 495, 635, 835, 975
y-center: 180
track: M 40 180 L 1060 180 (stroke #13283f, stroke-width 6)
pulse: same line, stroke #00e5ff, stroke-dasharray "8 28", opacity .7
arrows: small triangles at gaps (e.g. points="160,175 175,180 160,185")
```

Highlight the 2 "core" machines (Pick and Place + Reflow Oven) with the neon-green stroke and slightly larger boxes. Use the orange `var(--warn)` for the off-line THT/Wave branch — visually separates it from the main line.

## Required Footer Block (verbatim URL list)

Every explainer page must include these exact links in the footer:

- LinkedIn Company Page → https://www.linkedin.com/company/smtmachine
- LinkedIn Profile → https://cn.linkedin.com/in/smtsupplier
- Twitter → https://twitter.com/smtspecialist
- Facebook → https://www.facebook.com/autoinsertion
- YouTube Channel → https://www.youtube.com/c/Smthelping
- "Browse our machine catalog at file.autoinsertion.com and find machine photos at ph.smthelp.com."

Logo at top-left → https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png

## SPIN Question Pair (drop into CTA section)

Always end with exactly 2 SPIN questions. Q1 = current-state pain (yield / labor), Q2 = future pain (bottleneck / growth). Use the `.spin-q` style (left-border accent, monospace-eyebrow).

```html
<div class="spin-q">
  <b>Q1 — Current State:</b> What is your existing line's <b>first-pass yield</b> on [product], and how
  much of your throughput is currently lost to <b>manual insertion</b> or re-work?
</div>
<div class="spin-q">
  <b>Q2 — Growth &amp; Pain:</b> At your current run-rate, where is the <b>biggest bottleneck</b> —
  [Pick and Place / Reflow Oven / THT / labor]?
</div>
```

## Output Location & Naming

Save to `/Users/jasonwu/Downloads/{Topic_Snake_Case}.html`. Examples:
- `LED_Tube_1.2M_SMT_Solution.html`
- `Automotive_THT_Insertion_Line_Walkthrough.html`
- `Power_Supply_Wave_Soldering_Explainer.html`

If the page is a lead-magnet (has a 4-field form), also see the **Lead-Magnet Variant** section below for the form pattern + n8n activation steps.

If the user wants the page live on `ph.smthelp.com/<slug>`, also see **Deployment to ph.smthelp.com** below — the agent cannot push HTML to ph.smthelp.com directly in-session, so the file is delivered locally and a manual Hostinger/SFTP step is required.

## Sci-Pop Anime Storybook Variant

When the user asks for a "动画科普绘本" (popular-science picture book) — i.e. a
narrative anime-style page rather than a straight product explainer — replace
the 7-section structure with a **multi-chapter storybook**. Same PCB dark theme,
same footer, same SPIN-selling CTA at the end, but the body is organized as
hero → TOC → 6–8 narrative chapters → SPIN → footer.

### Chapter Structure (8 chapters is the sweet spot for one full vertical)

| Ch | Title Pattern | What's inside |
|----|---------------|---------------|
| 00 | Prologue / The Call | The market trigger (e.g. 1.2M pcs/mo order), the back-calculation, sets the stakes |
| 01 | Hero entry 1 | First machine on the line (Loader / Magazine), the "awakening" moment |
| 02 | Hero entry 2 | Second station (Stencil Printer) — the foundation metaphor |
| 03 | Battle / Choice | Two machines in contrast (Speed vs Precision) — the heart of the line |
| 04 | Transformation | The thermal/process step (Reflow Oven) — the "forge" or "alchemy" beat |
| 05 | Judgment | The quality step (AOI / SPI) — the "all-seeing eye" beat |
| 06 | Off-line branch | THT / Wave Soldering — separates from main flow visually |
| 07 | Epilogue | The delivered result, all heroes assembled, the final reveal |

### Per-chapter panel recipe (use this 3-panel structure inside each chapter)

1. **Character Profile panel** (col-4): SVG avatar of the machine as a robot
   character + role label (e.g. "THE SPEED DEMON") + persona name (e.g.
   "SM-800 · 极速忍者") + 1-paragraph voice + 3 stat pills (CPH / accuracy /
   capacity).

2. **Visual Scene panel** (col-7 or col-8): Inline SVG illustration of the
   machine doing its job, with a `.scene-label` badge (e.g. "SCENE 03 · STENCIL
   PRINT") in the bottom-left corner. Below the SVG, a **dialogue quip**
   (`.quip` style) with the machine speaking in first person:
   ```
   <div class="quip"><b>Paste Knight:</b> "I am the foundation. If I miss,
   no hero can save the joint."</div>
   ```

3. **Tech specs panel** (col-12, full width): The "Why this matters" explanation
   with spec pills (`.specs-row`), and a **dashed purple `.ai-prompt` box**
   containing a copy-pasteable Midjourney / Stable Diffusion prompt for
   generating the actual anime artwork. Use the MJ `--ar 16:9 --niji 6`
   style suffix.

### SVG character avatar template (use this color-coding)

Each machine gets a 200×200 SVG avatar. Background is always `#050a18` (deep
navy). The "chassis" is a rounded rect. Color-code by function:

| Machine category | Stroke color | Meaning |
|------------------|--------------|---------|
| Magazine / Loader / SPI / Unloader | `#00e5ff` (cyan) | Material handling — the calm ones |
| Pick and Place (high-speed) | `#39ff7a` (neon green) | Speed demons |
| Pick and Place (precision) | `#00e5ff` (cyan) | Precision sages |
| Reflow Oven | `#ff4d8d` (pink) | The fire forge |
| AOI / SPI | `#39ff7a` (neon green) | The seeing eye |
| THT Insertion | `#a56bff` (purple) | The off-line heroes |
| Wave Soldering | `#39ff7a` (neon green) | The wave surfer |

Inside each avatar: status LEDs (use `class="anim-blink"` for the active
one), a small "screen" with the key spec in 9–10px bold (e.g. `30,000 CPH`,
`±0.05 mm`, `245°C`), and a textual name label at the bottom in
`letter-spacing: 2` caps.

### AI Art Prompt box template

Embed one per chapter (and per major scene inside a chapter). The prompt
should describe the scene composition, lighting, and key action. Always end
with `--ar 16:9 --niji 6` for Midjourney niji mode (anime).

```html
<div class="ai-prompt">
  anime style, dynamic action shot, two mecha characters facing each other in
  a sci-fi factory arena, the left one is a green neon ninja holding 4 glowing
  nozzles with speed lines, the right one is a calm cyan scholar with a
  single precise placement head and a crosshair, between them a 1.2-meter
  white PCB conveyor with gold LED chips, 6 violet camera eyes flashing
  above, dramatic lighting, motion blur on the ninja, 8k --ar 16:9 --niji 6
</div>
```

```css
.ai-prompt {
  background: #0a1024; border: 1px dashed rgba(165,107,255,.5);
  border-radius: 10px; padding: 14px 16px; margin-top: 10px;
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: 11.5px; line-height: 1.55; color: #c5b3ff; position: relative;
}
.ai-prompt::before {
  content: "MJ/SD PROMPT"; position: absolute; right: 10px; top: 8px;
  font-size: 9px; letter-spacing: .2em; color: #a56bff;
}
```

### Cover-section animation (use this in storybook hero)

Floating LED "tubes" that travel across the screen left-to-right — sets the
anime tone immediately. Generate 5–8 of them with staggered animation-delay
and varying colors (gold, green, cyan, pink, purple).

```css
.float-led { position: absolute; width: 14px; height: 8px; border-radius: 2px;
  box-shadow: 0 0 18px currentColor;
  animation: ledTravel 9s linear infinite; }
@keyframes ledTravel {
  0%   { transform: translateX(0); opacity: 0; }
  10%  { opacity: 1; } 90% { opacity: 1; }
  100% { transform: translateX(120vw); opacity: 0; }
}
```

### Sticky Table of Contents

8-chapter storybooks get long. Add a 4×2 grid of clickable TOC cards right
after the cover. Each card smooth-scrolls to the chapter anchor. Use the
existing `.toc-item` hover effect (lift + cyan glow).

### When NOT to use the storybook variant

- Pure B2B sales documents where the buyer wants hard specs and ROI math
  (use the standard 7-section structure)
- Quick product overviews / one-pagers (storybook is overkill)
- Cases where the prospect explicitly asked for a "deck" or "PDF" rather
  than a "page" or "story"

### Storybook variant — file size & build cost

Expect 80–100 KB for a full 8-chapter storybook (vs 25–35 KB for the
standard 7-section explainer). The cost is in the SVG character avatars
and per-chapter scene illustrations — 12–16 inline SVGs total. No build
step, no external assets beyond the logo URL.

## Lead-Magnet Variant (turn any explainer into a lead-capture page)

When the page is meant to be shared on LinkedIn / cold email / WhatsApp as a **top-of-funnel lead magnet** (not just a sales-deck artifact), add a 4-field lead-capture form between the SPIN block and the footer. This converts a passive explainer into a working demand-gen asset without breaking the existing 7-section / 8-chapter structure.

### When to use

- User says "make this a lead-magnet landing page", "add a contact form", "capture leads", "落地页", "留资"
- User shares a public URL and asks "deploy it to ph.smthelp.com/xxx"
- The page is going to be linked from LinkedIn / cold email / EDM

### The 4 fields (no more, no less)

```html
<section class="lead-form-section" id="lead-form">
  <h2>Get the Free Line Layout Design</h2>
  <p class="sub">Send us 4 inputs. Our Shenzhen engineering team will return a
    <strong>PCB line Layout + ROI model</strong> within 48 hours. <strong>No cost, no obligation.</strong></p>
  <form id="leadCaptureForm" class="form-grid" novalidate>
    <div class="form-field"><label>Full Name *</label><input type="text" name="name" required></div>
    <div class="form-field"><label>Company *</label><input type="text" name="company" required></div>
    <div class="form-field"><label>Business Email *</label><input type="email" name="email" required></div>
    <div class="form-field"><label>Monthly PCBA Volume *</label>
      <select name="monthly_volume" required>
        <option value="">— Select range —</option>
        <option value="<5K">&lt; 5,000</option>
        <option value="5-30K">5,000 - 30,000</option>
        <option value="30-100K">30,000 - 100,000</option>
        <option value="100-500K">100,000 - 500,000</option>
        <option value=">500K">&gt; 500,000</option>
      </select>
    </div>
    <button type="submit" class="submit-btn" style="grid-column:1/-1">Request My Free Line Layout →</button>
  </form>
  <div id="formStatus" class="form-status"></div>
</section>
```

Volume bucket is critical — Jason uses it to pre-qualify the lead (5-30K / 30-100K are the sweet spot for the Southern Machinery sales motion). Don't change the buckets without checking.

### Submission strategy — progressive enhancement (NEVER skip the fallback)

A "lead-magnet landing page" with a form that doesn't actually capture leads is worse than no form. The progressive-enhancement pattern below works whether or not the n8n webhook is wired up:

```js
var N8N_WEBHOOK_URL = ''; // <-- paste n8n webhook URL when activated
var FALLBACK_EMAIL = 'info@smthelp.com';

form.addEventListener('submit', function(e) {
  e.preventDefault();
  var data = {
    name: form.name.value.trim(),
    company: form.company.value.trim(),
    email: form.email.value.trim(),
    monthly_volume: form.monthly_volume.value,
    source: '<page-slug>',          // e.g. 'radial-feeder-comic'
    submitted_at: new Date().toISOString(),
    page_url: window.location.href
  };
  if (!data.name || !data.company || !data.email || !data.monthly_volume) {
    showStatus('error', 'Please fill in all 4 fields.'); return;
  }
  if (N8N_WEBHOOK_URL) {
    fetch(N8N_WEBHOOK_URL, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data), mode:'cors'})
      .then(r => r.ok ? r : Promise.reject(r))
      .then(() => { showStatus('success', '✅ Request received. We will email your Layout + ROI model within 48 hours.'); form.reset(); })
      .catch(() => { openMailto(data); showStatus('success', '✅ Opening your email client as a backup channel.'); form.reset(); });
  } else {
    openMailto(data);   // <-- THIS is the default. Never let the form do nothing.
    showStatus('success', '✅ Your email client is opening with a pre-filled inquiry.');
  }
});

function openMailto(data) {
  var subject = encodeURIComponent('[' + data.source + '] Line Layout Request — ' + data.company);
  var body = encodeURIComponent('Hello Southern Machinery team,\n\n' +
    'I just finished reading the ' + data.source + ' page and would like a free Line Layout + ROI model.\n\n' +
    'Name: ' + data.name + '\nCompany: ' + data.company + '\nEmail: ' + data.email + '\nMonthly PCBA Volume: ' + data.monthly_volume + '\n\n' +
    'Please send:\n- Suggested SMT + THT line configuration\n- ROI model with my volume and labor cost\n- Reference customers in my region (if any)\n\nThank you,\n' + data.name);
  window.location.href = 'mailto:' + FALLBACK_EMAIL + '?subject=' + subject + '&body=' + body;
}
```

### Activating n8n capture (5 steps, ~5 minutes)

When the user wants real lead capture (not just mailto fallback):

1. Log in to https://n8n.autoinsertion.com
2. New workflow → add **Webhook** node (POST, path matches `source` slug)
3. Add **Google Sheets** node — append row to "Lead Magnet Leads" sheet with the 7 fields above
4. Add **Send Email** node → jasonwu@smthelp.com, subject "New Lead: {Company}", body summary
5. Activate → copy Production URL → paste into `N8N_WEBHOOK_URL` in the HTML → redeploy

If the user asks you to create the n8n workflow programmatically, use the `n8n` skill or `n8n-api-workflow-creation` skill. Don't click through the n8n UI by hand.

### Styling

Add these to the design-system block:

```css
.lead-form-section { margin: 64px 0 48px; padding: 48px 32px;
  background: linear-gradient(135deg, var(--bg-2) 0%, var(--bg) 100%);
  border: 2px solid var(--accent); border-radius: 20px; text-align: center; }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px; max-width: 800px; margin: 0 auto; }
.form-field { text-align: left; }
.form-field label { display: block; font-size: 12px; font-family: "SF Mono", monospace;
  color: var(--accent); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
.form-field input, .form-field select { width: 100%; padding: 12px 14px;
  background: var(--bg); border: 1px solid var(--line); border-radius: 8px;
  color: var(--text); font-size: 15px; font-family: "Inter", sans-serif; }
.form-field input:focus, .form-field select:focus { outline: none;
  border-color: var(--accent); box-shadow: 0 0 0 3px rgba(0,229,255,0.15); }
.submit-btn { margin-top: 24px; padding: 16px 48px;
  background: linear-gradient(135deg, var(--accent) 0%, #0088a8 100%);
  color: var(--bg); border: none; border-radius: 10px; font-size: 16px;
  font-weight: 700; cursor: pointer; text-transform: uppercase; letter-spacing: 0.05em; }
.form-status { margin-top: 16px; padding: 12px; border-radius: 8px; font-size: 14px; display: none; }
.form-status.success { display: block; background: rgba(57,255,122,0.1);
  color: var(--accent-2); border: 1px solid var(--accent-2); }
.form-status.error { display: block; background: rgba(255,77,141,0.1);
  color: var(--warn); border: 1px solid var(--warn); }
```

## PDF Export Variant (Chrome headless print-to-pdf)

When the explainer or storybook is destined for **LinkedIn DM, cold email attachment, WhatsApp file share, or trade-show printed handout** (not just a web URL), export the same single-file HTML to a multi-page A4 PDF. The same HTML ships both formats — no separate "PDF version" to maintain.

### When to use

- User says "export to PDF", "发PDF版", "give me a PDF for LinkedIn", "PDF attachment", "打印版"
- User wants to share the explainer on a channel that doesn't render HTML (email, IM, LinkedIn DM)
- User wants a printable version for a trade-show booth handout
- The user has just finished an HTML explainer and the next step is "send it out"

### The Chrome headless command (macOS)

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --print-to-pdf="/absolute/path/output.pdf" \
  --print-to-pdf-no-header --no-pdf-header-footer \
  --virtual-time-budget=10000 \
  "file:///absolute/path/input.html"
```

- `--print-to-pdf-no-header` + `--no-pdf-header-footer` → kills Chrome's default URL/timestamp header on every page
- `--virtual-time-budget=10000` (10s) → lets CSS animations and Google Fonts settle before the print snapshot. **Without this, fonts flash to fallback and animated counters freeze mid-roll**
- Default page size is **A4 (595×842 pt)**, no explicit `--paper` flag needed
- Resulting PDF: typically 8 pages for a 7-section explainer, 15–20 pages for an 8-chapter storybook
- File size: ~0.8–1.2 MB for a typical explainer (Google Fonts + inline SVGs), well under LinkedIn's 20 MB attachment limit

### The @media print hardening block (REQUIRED)

**This block must be present in the HTML before exporting.** Without it, three classes of breakage appear in the PDF:

1. **Gradient text via `background-clip: text` + `-webkit-text-fill-color: transparent` renders as a solid colored block** — Chrome's print engine applies the gradient as a background fill but the text knockout fails, so the user sees a colored rectangle instead of the title. **This is the #1 PDF bug.** All H1/H2/H3 with `var(--accent)` gradient must be flattened to solid color in print.
2. **Dark background and accent card colors get dropped to white** — Chrome's print defaults strip background colors to save ink. Use `print-color-adjust: exact` on `body`, `.scene`, `.panel`, `header`, `footer`, `.cta-strip`, `.form-card` to preserve them.
3. **Animations render mid-frame as ghost shadows** — particularly the `.pulse-dot` `box-shadow` ring and the KPI counter numbers. Disable animations in print; force a static state.

```css
/* Insert as the LAST block in <style>, right before </style> */
@media print {
  /* Kill the gradient-text bug: force solid color for all headings */
  h1, h2, h3 {
    background: none !important;
    -webkit-background-clip: initial !important;
    background-clip: initial !important;
    -webkit-text-fill-color: var(--accent) !important;
    color: var(--accent) !important;
  }
  h2, .scene-title { color: var(--text) !important; }   /* keep H2 body-color, not accent */

  /* Preserve dark theme and accent card backgrounds */
  body { background: #050a13 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .scene, .panel, header, footer, .cta-strip, .form-card, .lead-form-section {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Disable animations and decorative motion */
  .pulse-dot, .float-led, .machine, .pulse { animation: none !important; }
  .pulse-dot { box-shadow: 0 0 0 2px rgba(57,255,122,.5); }   /* static "alive" indicator */

  /* Strip the top-edge decorative line on .scene cards (gradient renders as a thin grey bar) */
  .scene::before, .scene-2::before, .scene-3::before, .scene-4::before, .scene-5::before { display: none; }

  /* Page geometry */
  @page { size: A4; margin: 12mm; }
}
```

Drop this block into the existing `templates/smt-line-walkthrough.html` and `templates/smt-anime-storybook.html` so the templates ship print-ready by default.

### Pitfall — the gradient-text bug is silent

`h1 { background: linear-gradient(...); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }` looks **perfect in the browser** and **silently breaks in print-to-pdf** — the title becomes a colored rectangle with no visible text. The eye sees the gradient and assumes the text is there. **Always verify the PDF with vision_analyze on the first page before declaring it done.** The `@media print` block above is the only fix; there is no flag in Chrome to make `background-clip: text` work in print.

### Pitfall — SVGs with viewBox only collapse to 0×0 in print

If an inline `<svg>` has only `viewBox="0 0 800 320"` and no `width`/`height` attributes, the browser lays it out fine in screen mode (CSS `width: 100%` on the parent takes effect), but **Chrome's print pipeline collapses it to 0×0**. The page renders with a colored panel border and absolutely no illustration inside — easy to miss in code review because the dev tools show it as 100% wide.

Fix: inject explicit width/height before the print snapshot:

```js
document.querySelectorAll('svg').forEach(s => {
  s.setAttribute('width', '100%');
  s.setAttribute('height', 'auto');
  s.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  s.style.width = '100%';
  s.style.height = 'auto';
  s.style.display = 'block';
});
```

The `@media print` CSS rule on `.scene-art svg, .scene-art-full svg` is a defense-in-depth, but the JS attribute injection is the actually reliable fix. Confirmed by visual diff: with the attribute fix, all 5 SVG panels render at 944×377pt in the A4 page; without it, every panel is empty.

### The Playwright recipe (when Chrome CLI isn't enough)

For one-off PDF exports where you also need to (a) inject custom CSS, (b) mutate the DOM (e.g. replace a live `<form>` with a static summary + READER ACTION callout), or (c) programmatically verify page count, use **Playwright + the system Google Chrome** rather than the Chrome CLI. The CLI only takes a static `file://` URL; Playwright gives you a full DOM lifecycle.

```python
import asyncio
from playwright.async_api import async_playwright

async def export_pdf(html_path, pdf_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            args=['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none'],
        )
        context = await browser.new_context(
            viewport={'width': 1240, 'height': 1754},
            device_scale_factor=2,  # retina-quality output
        )
        page = await context.new_page()
        await page.goto(f'file://{html_path}', wait_until='networkidle', timeout=60000)
        await page.wait_for_timeout(3000)  # let webfonts settle

        # Step 1: SVG width fix (the viewBox-only collapse bug)
        await page.evaluate("""() => {
          document.querySelectorAll('svg').forEach(s => {
            s.setAttribute('width', '100%');
            s.setAttribute('height', 'auto');
            s.setAttribute('preserveAspectRatio', 'xMidYMid meet');
            s.style.width = '100%';
            s.style.height = 'auto';
          });
        }""")

        # Step 2: Inject print CSS (see @media print block above)
        await page.add_style_tag(content=PRINT_CSS)

        # Step 3: Switch to print emulation BEFORE mutating DOM
        await page.emulate_media(media='print')

        # Step 4: Optional DOM mutation (e.g. replace form with static summary)
        await page.evaluate(REPLACE_FORM_JS)
        await page.wait_for_timeout(1000)

        # Step 5: Render
        await page.pdf(
            path=pdf_path,
            format='A4',
            print_background=True,
            margin={'top': '10mm', 'right': '8mm', 'bottom': '10mm', 'left': '8mm'},
            prefer_css_page_size=True,
        )
        await browser.close()
```

A full working implementation is at `scripts/playwright-html-to-pdf.py` — copy it, point it at your HTML, run. It already handles the SVG fix, the @media print injection, the form-replacement pattern (see below), and the final pymupdf/pdftoppm sanity check.

### Form-replacement pattern (turn a live form into a static PDF summary)

A "lead-magnet landing page" has a live `<form>` that does nothing in PDF — Chrome prints the form but you can't submit it. Replace the form with a static 4-field summary + a prominent READER ACTION callout (URL + WhatsApp + email) before the print snapshot. This lets the same HTML ship as both the live web page (interactive form) and a printable PDF (CTA with contact info).

```js
() => {
  const formSection = document.querySelector('.lead-form-section');
  if (!formSection) return;
  const labels = formSection.querySelectorAll('label');
  const fields = Array.from(labels).map(l => l.textContent.trim().replace(/\\s+/g, ' '));

  // Replace the form HTML
  formSection.innerHTML = `
    <div style="background:linear-gradient(135deg,#0a1428,#0f172a);padding:24px;border-radius:14px;border:1px solid rgba(34,211,238,0.4);page-break-inside:avoid;">
      <h2 style="color:#22d3ee;font-size:22px;margin:0 0 8px 0;font-weight:700">Get the Free Line Layout + ROI Model</h2>
      <p style="color:#cbd5e1;font-size:13px;line-height:1.5;margin:0 0 16px 0">Send us 4 inputs. We reply within 48 hours. <strong>No cost, no obligation.</strong></p>
      <div style="background:#020617;padding:14px 18px;border-radius:8px;border:1px dashed rgba(34,211,238,0.4)">
        <div style="color:#22d3ee;font-size:10px;letter-spacing:2.5px;margin-bottom:8px">FIELDS WE NEED (4)</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px 18px;font-size:13px;color:#e2e8f0">
          ${fields.slice(0,4).map(f => `<div>▸ <strong>${f}</strong></div>`).join('')}
        </div>
      </div>
    </div>
  `;

  // Insert the READER ACTION callout right BEFORE the footer
  const footer = document.querySelector('footer');
  if (footer) {
    const callout = document.createElement('div');
    callout.style.cssText = 'margin:24px auto 18px auto;padding:24px 20px;background:linear-gradient(135deg,#0e7490,#0891b2);border-radius:14px;text-align:center;color:#fff;page-break-inside:avoid;';
    callout.innerHTML = `
      <div style="font-size:11px;letter-spacing:2.5px;opacity:0.9;margin-bottom:10px">— READER ACTION —</div>
      <div style="font-size:21px;font-weight:700;margin-bottom:8px">Submit the form on our website</div>
      <div style="font-size:13px;opacity:0.95;margin-bottom:14px;line-height:1.5">We reply within 2 hours during business days. Mention this PDF for a same-day quotation.</div>
      <div style="font-size:16px;font-weight:600;background:#020617;padding:11px 18px;border-radius:8px;display:inline-block;font-family:'JetBrains Mono',ui-monospace,monospace;margin-bottom:12px">ph.smthelp.com/${SLUG}</div>
      <div style="margin-top:10px;font-size:12px;opacity:0.92;line-height:1.6">WhatsApp: <strong>+86-136-0256-2576</strong> &nbsp;&middot;&nbsp; Email: <strong>jasonwu@smthelp.com</strong></div>
    `;
    footer.parentNode.insertBefore(callout, footer);
  }
}
```

Critical: the `page-break-inside: avoid` inline style on the callout is what stops Chrome from splitting it across pages. Without it, the callout can land half on page 8 and half on page 9, with the URL + phone/email on the wrong page from the form summary.

### Multi-page PDF verification — use pdftoppm, not pymupdf

The skill's current verification recipe uses `fitz` (pymupdf), which requires `pip3 install pymupdf`. **A faster, zero-Python-install alternative** is `pdftoppm` from the poppler suite, which Jason almost certainly has via Homebrew:

```bash
brew install poppler 2>&1 | tail -3   # one-time
pdftoppm -png -r 110 output.pdf /tmp/preview/page
# → /tmp/preview/page-1.png, page-2.png, ...
```

The `-r 110` flag gives a print-quality render at 1.5x device-pixel-ratio. The Type 3 glyph warnings (about CJK / emoji bounding boxes) are harmless — they come from Chrome's font rendering for non-Latin glyphs and don't affect the output.

After pdftoppm, use `vision_analyze` on **page 1, the middle page, and the last page** — that's enough to catch gradient-text bugs, empty SVG panels, and footer/form overflow.

### Pitfall — Chrome PDF viewer `#page=N` fragment is unreliable for headless verification

When you try to verify a specific page of the output PDF by loading it in Chrome (`file://path.pdf#page=5`) with Playwright and screenshotting, **the fragment often silently fails to navigate** — you'll get a screenshot of page 1 even though the URL says `#page=5`. Don't waste time debugging this. Use `pdftoppm` (above) to render specific pages deterministically, or open the PDF in Preview with `subprocess.run(['open', '-g', pdf_path])` and screenshot from there.

### Pitfall — file:// URL has no HTTPS hotlink protection on localhost

The `ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png` URL works fine when the HTML is opened locally (file://), and works fine when the HTML is hosted on any HTTPS domain. But if the user later serves the HTML from a non-Southern domain (e.g. Netlify subdomain) and the image hotlink protection kicks in, the logo collapses to a 404. For maximum portability, **always include an SVG fallback or a tiny base64-encoded PNG** in the header. The PDF export already inlines the image for the duration of the print snapshot, so this is only a concern for the live web version.

### Verification (4 steps, ~30 seconds)

1. **Run the Chrome command above** OR the Playwright recipe (see Pitfall — Playwright recipe). Expect a PDF 0.5–2 MB and 6–20 pages depending on content length.
2. **Page count + page size sanity check:**
   ```python
   import fitz
   doc = fitz.open('output.pdf')
   print(f'pages={doc.page_count}')
   for i, p in enumerate(doc):
       print(f'  p{i+1}: {p.rect.width:.0f}x{p.rect.height:.0f}pt')
   ```
   Expect 595×842 pt (A4) per page. If pymupdf isn't installed, use `pdftoppm -png -r 110 output.pdf /tmp/preview/page` instead — renders all pages as PNGs for the same verification, no Python install required (`brew install poppler` is one-time).
3. **Visual verify the first page** with `vision_analyze` (use pymupdf or pdftoppm to render page 1 to PNG first). Confirm: H1 title is **readable solid text** (not a colored block), dark background is preserved, hero KPI numbers display correctly, no animation ghosts, **all SVG storyboard panels contain visible illustrations** (the viewBox-only collapse bug is silent — verify the actual content, not just the page count).
4. **Visual verify the last page** (footer + form). Confirm: social links render, lead form fields are visible, no clipped content at the page break, READER ACTION callout (URL + WhatsApp + email) is fully on the page, not split across two pages.

Pitfall: `sips -s format png file.pdf --out x.png` **only renders the first page**. To verify all pages use pymupdf (`fitz`) or `pdftoppm` from poppler.

Pitfall: Chrome's built-in PDF viewer (in the `file://path.pdf#page=5` URL fragment) is unreliable for headless page-specific navigation — it often silently opens page 1 regardless of the fragment. Use `pdftoppm` or pymupdf instead.

### Distribution tips (LinkedIn / email / WhatsApp)

- **Filename:** rename to `Southern-Machinery_{Topic_Snake_Case}_2026.pdf` before sending — LinkedIn shows the filename in the chat preview
- **LinkedIn DM attachment cap:** 20 MB. PDF is well under.
- **Email clients (Gmail / Outlook):** file ≤ 10 MB preferred; under 2 MB is ideal. Current PDF is ~1 MB. ✓
- **WhatsApp file share cap:** 100 MB. PDF is fine.
- **For Instagram / LinkedIn feed (no attachment):** convert PDF to a 1080-wide PNG strip using `pdftoppm -r 110 -png file.pdf out` and stitch vertically. One PNG posts anywhere.

### Reusable helper script

A wrapper script lives at `scripts/html-to-pdf.sh` — pass the HTML path, it produces the PDF next to it, then runs the pymupdf sanity check. Use it whenever the user asks "export to PDF" rather than retyping the Chrome command.

## Deployment to ph.smthelp.com (after building the page)

Once the HTML is built, the user almost always wants it on `ph.smthelp.com/<slug>`. **ph.smthelp.com is a Chevereto image-host** — it does NOT serve arbitrary HTML pages through its API. The Chevereto API at `http://ph.smthelp.com/api/1/upload` only accepts image files (JPG/PNG/GIF/WebP, max 50MB). It will reject an HTML file with HTTP 421 or similar.

This means deployment is a **manual step** that requires the user (or Hostinger admin) to do via the hosting control panel. The agent's job is to:

1. Build the HTML locally (saves to `/Users/jasonwu/Downloads/<slug>.html` per Output Location)
2. **Tell the user honestly** that the agent cannot push to ph.smthelp.com directly in-session (no FTP/Hostinger creds in scope)
3. Provide a 1-line deploy recipe they can paste in hPanel / SFTP

### The three deploy recipes (in order of speed)

**Method A — Hostinger File Manager (fastest, no terminal)**

1. Login to hPanel → File Manager
2. Navigate to ph.smthelp.com's web root (usually `public_html/` or a vhost folder)
3. Create subdirectory `<slug>/`
4. Upload `<slug>.html` and rename to `index.html`
5. Visit `https://ph.smthelp.com/<slug>/` — page is live

**Method B — SFTP one-liner**

```bash
sftp user@ph.smthelp.com <<EOF
cd public_html
mkdir <slug>
cd <slug>
put /Users/jasonwu/Downloads/<slug>.html index.html
bye
EOF
```

**Method C — GitHub Pages or Netlify fallback (if Hostinger is locked down)**

If ph.smthelp.com can't host HTML for routing reasons, push to a separate repo and link to it from the explainer page or LinkedIn. Chevereto is for images; for landing pages, Netlify / Cloudflare Pages / Vercel is a better fit.

### After deployment, verify

```bash
curl -sI https://ph.smthelp.com/<slug>/ | head -3
# Expect: HTTP/1.1 200 OK, with text/html content-type
```

If 404 → the subdirectory or `index.html` rename step was missed. If 403 → file permissions (chmod 644 on the .html file).

### Pitfall — ph.smthelp.com vs smthelp.com vs smthelp.v5.viwolf.cn

| Domain | Purpose | What to put there |
|--------|---------|-------------------|
| `ph.smthelp.com` | Chevereto image host (public) | Images only. **HTML goes here only via the manual Hostinger/SFTP path above.** |
| `smthelp.com` | Main marketing site (WordPress or similar) | Blog posts, product pages — managed via `smthelp-admin-blog-publishing` skill |
| `smthelp.v5.viwolf.cn/admin888` | Backend admin panel | Use `smthelp-admin-blog-publishing` skill for publishing |
| `file.autoinsertion.com` | Machine catalog (PDFs, datasheets) | Linked from explainer footers, not hosted on |
| `cn.linkedin.com/in/smtsupplier` | Jason's personal profile | Linked from footers only |

Do not try to push an HTML file to ph.smthelp.com via the Chevereto API — it will fail and waste an API call.

## Pitfalls

1. **The `.reveal { opacity: 0 }` missing-class bug.** Content stays hidden
   on screenshot tools, prefers-reduced-motion, short pages, and IO-blocking
   browser extensions. **Always use the `html.js` class gate pattern** (see
   the Animation Patterns section above) — default state is visible, JS
   activates the hiding. Combined with a 2.5s `setTimeout` safety net, the
   page is bulletproof.

2. **Patch mode='replace' can break script structure.** When patching mid-JS to insert a new line, your `old_string` must include enough context (typically the opening + closing of the block) that the patch leaves valid syntax. If you only match the opening `const x = new IntersectionObserver(entries=>{`, you'll orphan the closing `})` and the rest of the script silently breaks. Always re-read the patched file region after a mid-block insertion.

3. **Nozzle / Feeder / MES terms must appear in the body** if your equipment section mentions Pick and Place details — auditors and engineers check. The system prompt requires them kept in UPPERCASE English.

3. **CORS / hotlink risk on the logo.** The ph.smthelp.com logo URL works inline, but if the page is ever served from a non-Southern domain and the image fails, the header collapses to text. Consider an SVG fallback or a small inline data-URI alternative for maximum portability.

4. **Don't put all caps in marketing prose.** Industry terms in UPPERCASE; conversational copy stays in normal case. "The SMT line achieves 30,000 CPH" not "THE SMT LINE ACHIEVES 30,000 CPH".

5. **Hero stats must be self-consistent.** If your capacity math says 2,400 pcs/h, the hero stat card must say 2,400 pcs/h, not 2,500. Engineers will spot the mismatch and discount the rest of the page.

6. **SVG viewBox sizing.** Use `viewBox="0 0 1100 360"` and a `.flow` wrapper with `min-width: 880px; overflow-x: auto` so the diagram scrolls horizontally on mobile rather than squishing the machine labels.

7. **Don't hallucinate the home directory.** The user is `jasonwu`, home is `/Users/jasonwu/`. There is no `/Users/smthelp/` user. If you invent a path like `/Users/smthelp/xxx.html` and try to write to it, you will fail with permission denied. Always write explainer HTML to `/Users/jasonwu/Downloads/` (per the Output Location section) or `/Users/jasonwu/` (root). Verify with `echo $HOME` if uncertain. This has burned real sessions — do not skip the verification step.

## Verification Before Delivery

1. `grep -c "LinkedIn Company Page\|LinkedIn Profile\|Twitter\|Facebook\|YouTube Channel" file.html` — must be ≥ 1 of each
2. `grep -oE "\b(SMT|THT|PCB|PCBA|CPH|Feeder|Nozzle|Reflow Oven|Wave Soldering|Pick and Place|SPI|AOI|MES)\b" file.html | sort -u` — full list, all uppercase
3. Open in browser, scroll top to bottom, confirm: hero counters animate, all 7 sections reveal, SVG flow pulses, footer links present, both SPIN questions render
4. File size typically 25–35 KB; > 50 KB means you probably inlined too much

## Related Skills

- `smt-machine-marketing-image-prompts` — for static product images (use this skill for HTML, that one for images). The `.ai-prompt` boxes embedded in storybook chapters share vocabulary with this skill.
- `smthelp-knowledge-base` — load FIRST for exact model numbers, CPH numbers, and certified specs
- `smthelp-image-hosting-workflow` — for hosting generated **images** on ph.smthelp.com via Chevereto API. NOTE: this skill is image-only and will NOT help with HTML page hosting — for that, see the **Deployment to ph.smthelp.com** section in this skill.
- `smthelp-admin-blog-publishing` — for publishing blog articles to the main smthelp.com WordPress site (different domain, different workflow — not a substitute for HTML landing-page deployment).
- `n8n` and `n8n-api-workflow-creation` — for activating the lead-capture webhook in the Lead-Magnet Variant section.

## Support Files

- `templates/smt-line-walkthrough.html` — single-file base template for the **standard 7-section product explainer** with all sections, SVG flow, and JS animations pre-wired. Copy → fill `{{PLACEHOLDER}}` slots → ship. ~16 KB, no build step, no external deps beyond the logo URL.
- `templates/smt-anime-storybook.html` — single-file base template for the **sci-pop anime storybook variant** (8 chapters, character profiles, AI art prompts, dialogue quips). ~93 KB when filled. Use when the user asks for a "动画科普绘本" or "anime storybook" rather than a standard explainer.
- `scripts/html-to-pdf.sh` — one-shot wrapper for `chrome --headless --print-to-pdf`. Run with `./scripts/html-to-pdf.sh path/to/explainer.html` to produce `<name>.pdf` next to it. Auto-prints page count + A4 page-size sanity check via pymupdf. **Use this whenever the user asks "export to PDF" rather than retyping the Chrome command.** Requires the input HTML to include the `@media print` hardening block from the PDF Export Variant section.
- `scripts/playwright-html-to-pdf.py` — the more powerful Playwright + Chrome headless recipe (SVG width fix, custom CSS injection, DOM mutation for form-replacement, full page-by-page verification). Use this when the user wants (a) the lead-magnet form replaced with a static summary + READER ACTION callout in the PDF, (b) custom `@page` margins, (c) a single Python script as the deliverable. ~150 lines, all dependencies are pre-installed (Playwright is already part of the Hermes venv).
- `references/pdf-export-hardening.md` — pocket reference for the 5 most common PDF bugs and their one-line fixes. Read this when debugging a misbehaving export.
- `references/svg-flow-layout.md` — 7-station SMT line SVG layout cheatsheet (station x-coordinates, stroke colors, animation classes, off-line THT branch geometry). Use when building the `.flow` SVG in any standard explainer.
