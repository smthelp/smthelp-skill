# Feedback log

One entry per piece of feedback. Status open -> done once the rule is in the skill.

### FB-004 [deck] done - 2026-10-16
- Product: X3100
- Feedback: Convert the Chinese supplier manual into the Southern Machinery 2025 PPT template in English.
- Rule: Manuals use the A4 template via make_deck.py; supplier brand and contacts removed; Chinese only allowed inside screenshots, explained in English captions.
- Applied: references/deliverables.md section 3, qa_kit.py CJK check (1.0.0)

### FB-003 [video] done - 2026-10-16
- Product: X3100
- Feedback: English promo and Shorts without people, supplier subtitles hidden.
- Rule: People-free footage by default; burned supplier subtitles cropped with clip "crop" rows; TTS en-US-AndrewNeural; burned subs + SRT.
- Applied: scripts/make_video.py (1.0.0)

### FB-002 [facts] done - 2026-10-15
- Product: S-D508 blade
- Feedback: Different values across documents often mean versions for different machine brands, not errors.
- Rule: Version-type differences go to a "By version" table matched per order from nameplate/old part; ask Jason when unsure.
- Applied: references/extraction-rewrite.md section 2 (1.0.0)

### FB-001 [voice] done - 2026-10-13
- Product: FUJI NXT jig
- Feedback: Titles must never contain hook/diagnosis/framework/vehicle/loop/CTA; never invent specs, prices, lead times, certificates.
- Rule: Banned heading words + never-publish list enforced in brand-guide.md and qa_kit.py.
- Applied: references/brand-guide.md, scripts/qa_kit.py (1.0.0)

