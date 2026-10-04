---
name: smart-smt
description: Use this skill whenever the user needs English marketing copy paired with image-generation prompts or visual directions for Southern Machinery SMT/THT equipment, PCB assembly automation, EMS factory outreach, LinkedIn/YouTube/blog visuals, landing page hero images, or sales campaign illustrations. This skill is especially relevant when the user asks for concise, direct, futuristic, high-tech, minimal illustration styles for SMT machine export marketing, even if they do not explicitly say "Smart-SMT".
---

# Smart-SMT

Create English marketing copy and image-generation prompts for Southern Machinery's SMT/THT automation business. The output should feel clear, industrial, high-tech, and globally credible.

This skill is for paired copy + visuals, not standalone long-form writing. Use it when the task needs an image concept, an imagegen prompt, campaign visual direction, or short English text that will appear with a generated image.

## Brand Context

Southern Machinery Co., Ltd. is a Shenzhen-based SMT/THT PCB assembly automation company founded in 2011. It helps global EMS factories upgrade manual or semi-manual production into line-ready automation.

Core message:

```text
Automation Partner, Not Supplier
```

Primary business:

- SMT pick and place machines
- THT auto insertion machines
- Wave soldering and soldering automation
- Board handling equipment
- Complete SMT + THT production line solutions

Useful contact footer for customer-facing copy:

```text
Southern Machinery Co., Ltd.
Email: jasonwu@smthelp.com
Website: www.smthelp.com
WhatsApp: +8613602562576
Shenzhen, China | Smart PCB Assembly Automation Since 2011
```

## Visual Direction

Use `references/style-guide.md` when the user asks for image style, campaign visuals, or multiple image options.

The default Smart-SMT visual identity:

- Minimal, direct, high-tech, futuristic
- Clean industrial illustration, not decorative poster art
- Sharp geometry, simple silhouettes, strong negative space
- Blue, cyan, white, graphite, and small controlled green accents
- PCB traces, machine gantries, conveyors, robotic nozzles, LED strips, and factory lines
- Humans may appear as simplified engineers or operators, but machines and process flow should be the hero

Avoid:

- Cute mascot-led cartoons
- Busy comic panels
- Handwritten text
- Cluttered factories
- Low-end marketplace style
- Overly dark cyberpunk scenes
- Fake certification badges, prices, delivery dates, customer names, or unverifiable metrics

## Workflow

1. Identify the asset type: LinkedIn post image, YouTube thumbnail, blog hero, landing page hero, sales email visual, proposal cover, or product explainers.
2. Identify the business goal: labor saving, higher output, stable quality, line expansion, ROI discussion, sample testing, or technical consultation.
3. Choose one focused visual metaphor. Prefer a single machine/process idea over a crowded scene.
4. Write concise English copy first. Keep it direct and useful for B2B EMS buyers.
5. Create 1-4 imagegen prompts in the Smart-SMT style. Each prompt should produce a complete bitmap asset.
6. Add a short human-review note for any claims involving price, delivery, warranty, certification, custom specs, or ROI.

## Output Formats

### Campaign Visual Set

Use this structure when the user asks for several image options:

```markdown
## Concept 1: [Name]
Copy: [one short English headline or caption]
Imagegen prompt:
[prompt]

## Concept 2: [Name]
Copy: [one short English headline or caption]
Imagegen prompt:
[prompt]

## Concept 3: [Name]
Copy: [one short English headline or caption]
Imagegen prompt:
[prompt]

Review note:
[what must be checked by a human, if relevant]
```

### Single Asset

Use this structure when the user asks for one visual:

```markdown
Copy:
[headline or caption]

Imagegen prompt:
[prompt]

Alt text:
[plain English description]

Review note:
[only if needed]
```

### LinkedIn Post With Visual

Keep the post 150-300 words and include exactly 3 relevant hashtags.

```markdown
Visual concept:
[one-sentence description]

Imagegen prompt:
[prompt]

LinkedIn copy:
[150-300 words]

#SMTautomation #PCBassembly #EMS
```

## Imagegen Prompt Pattern

Use this prompt pattern by default:

```text
Use case: ads-marketing
Asset type: [LinkedIn image / YouTube thumbnail / landing page hero / blog hero / proposal cover]
Primary request: Create a concise futuristic high-tech illustration for Southern Machinery, showing [one focused SMT/THT automation idea].
Scene/backdrop: clean modern EMS factory or abstract PCB-production environment, minimal background, strong negative space.
Subject: [machine/process], simplified engineers only if useful, PCB panels, conveyors, robotic placement or insertion motion.
Style/medium: premium minimal industrial illustration, crisp vector-like shapes rendered as a polished bitmap, subtle 3D depth, not childish, not photorealistic.
Composition/framing: direct central composition, clear focal point, readable at thumbnail size, space for optional headline.
Lighting/mood: cool clean studio lighting, futuristic but practical, reliable engineering tone.
Color palette: Southern Machinery brand-inspired blue and graphite with cyan highlights, white space, small green PCB accents.
Text (verbatim): "[exact short English text, or 'no text']"
Constraints: concise, uncluttered, high-tech, B2B industrial, no fake UI, no fake badges, no unreadable tiny text, no copied comic character.
Avoid: cyberpunk darkness, cute mascot style, excessive gradients, crowded panels, handwritten typography, low-end ecommerce look, watermarks.
```

## Copy Guidelines

Prefer short, concrete English:

- "Automate THT insertion with stable output."
- "From manual PCB assembly to line-ready automation."
- "A practical SMT + THT upgrade for high-mix EMS factories."
- "Reduce manual handling. Improve process consistency."
- "Send your PCB details. We will suggest the right line setup."

Do not overclaim:

- Do not invent prices, delivery times, warranty terms, certifications, customer names, or ROI.
- Use confirmed product parameters only when they are provided by the user or an approved catalog.
- If a number is not sourced, write: "needs further confirmation by our engineering team."

## Product Hints

Use these only as directional matching notes. If the user needs exact specifications, ask for or cite the official catalog.

- Radial THT components: S3010A
- Axial THT components: S4000
- Odd-form parts such as connectors, relays, and electrolytic capacitors: S7020
- Standard LED placement: S-600SV
- Long LED boards: S-530SV
- LED + lens assembly: S-V8
- Full line visuals: printer, pick and place, reflow oven, AOI, board handling, insertion, wave soldering

## Human Review Reminder

Before using outputs externally, remind the user to review any formal claim involving:

- Price
- Lead time
- Payment terms
- Warranty
- Acceptance criteria
- Custom machine specifications
- Customer names or case details
- ROI calculations
