# Design and copy standard (SM-VIDEO-2026-10)

## 1. Frame layout (4K design units)
- Background: dark teal gradient (#07302b -> #04110f) with an 80 px grid at 4 % white. Footer rule at y=1985.
- Footage window 1400x1680 at (160,220), radius 44, teal glow and border. `mirror=True` moves it to (2280,220).
- Right panel (left when mirrored): kicker (JetBrains Mono, gold, tracked) + 120 px teal rule + video title (Inter Bold 92, <= 3 lines).
- Callout card 1960x900 max at (1720,600): kicker (mono, teal) -> headline (Inter Bold 82) or big stat (Inter ExtraBold 210, gold) + subline -> up to 4 bullets (Inter Medium 54). Slides in from the right, fades out before the scene ends. Auto-shrinks to fit.
- Top-left: SM logo on white plate. Top-right: product tag (mono, muted).
- Footer: left = footer CTA (gold); right = "WhatsApp +86 136 0256 2576 · smthelp.com".
- Subtitles: Inter SemiBold 72, white, dark outline, bottom of the right panel (margin 280), max 2 lines x 44 chars.
- Intro (4 s): hero gradient, logo plate, product tag, intro_title in Inter Black 150 (2 lines), tagline "Southern Machinery · Shenzhen, since 2011", product still right.
- Outro: opaque card with logo, outro headline (Black 132), green WhatsApp pill, web + email, outro line. Stays to the end; narration reads the CTA.
- Colours, fonts and contacts only from brand.json; never hard-code.

## 2. Footage treatment
- Crop to the clean area (portrait 720x864, medium 540x648, landscape fitted over a blurred fill), Lanczos upscale + light unsharp, contrast 1.04 / saturation 1.05.
- Speed 0.5-1.0x; short clips "boomerang" rather than freeze. >= 1.6 s on screen per shot.
- Blur (Gaussian sigma 10-16) or crop: supplier logos, supplier model numbers, software title bars and version strings, watermarks, Chinese UI text larger than a few characters, burned-in Chinese subtitles, faces/bodies. Hands and gloves are fine.
- Zoom variants (`z`) and mirrored layouts are how one clip appears fresh across many videos.

## 3. Narration (voice-over = subtitles)
- en-US-AndrewNeural, +3 % rate, ~2.55 words/s. 2-3 sentences per scene, <= 60 words; 150-330 words per video.
- Plain engineer English for overseas EMS buyers: short sentences, active voice, concrete numbers with units, no hype adjectives ("revolutionary", "best-in-class"), no "we are proud".
- Write numbers as they should be read on screen (`6–10 s`, `01005`, `3072 x 3072`); fix the reading in pronunciations, not in the text.
- Open with the viewer's problem or question in the first sentence; say the product name in scene 1 or 2; end with the outro CTA (free trial / send samples + WhatsApp + website).
- Hedging templates: "brochure example - we recommend a trial count with your own reels"; "for example, assume ..."; "engineered per project"; "send us samples and we will test them"; "follow the component maker's guidance"; "results depend on part, package and settings".

## 4. Callouts and slides
- Kicker: 1-3 words CAPS (<= 30 chars). Headline: <= 60 chars, says the takeaway, not the topic. Bullets: <= 4, <= 48 chars, no full stops.
- Stat callout for one confirmed number per scene at most; never a stat that is an example unless the subline says example.
- One idea per slide; slide heading <= 40 chars; any illustrative data on a slide carries a foot note "Example" / "Illustrative layout".
- Prefer data SLIDES (8 types). Bespoke drawings only for a concept that needs a diagram (e.g. ghost inventory, dry bag, lights-out flow).

## 5. Claims policy
| Claim kind | Allowed when | How |
|---|---|---|
| Product spec | in facts.md Confirmed | state plainly with unit |
| Brochure accuracy / speed example | in facts.md Brochure example | "brochure example" + test offer |
| Example calculation / sample data | always, if labelled | "Example", "assume", foot note |
| Integration concept (MES interlock, AGV, lights-out) | product supports the interface | "example rule in your MES", "engineered per project" |
| Safety / physics / standards | public source opened and listed in SOURCES | general wording, cite in Doc, advise validation |
| Capability not confirmed (BGA voids, AI, trays ...) | never as fact | "send samples, we test" |
| Customer names, savings %, payback, certifications | only with written source | otherwise leave out |
