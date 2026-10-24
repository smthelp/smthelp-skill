# Output specification

## 1. Files (final/<batch>/ and the Drive folder)
| File | Spec |
|---|---|
| `<prefix>-<slug>-4k.mp4` | 3840x2160, 30 fps CFR, H.264 High yuv420p CRF 20 bt709, AAC-LC 192 kb/s 48 kHz stereo, -15 LUFS integrated / -1.5 dBTP, faststart, 60-180 s |
| `<prefix>-<slug>-4k.srt` | UTF-8, <= 2 lines x 44 chars, cues split at punctuation, identical to burned subtitles |
| `<prefix>-<slug>-thumbnail.png` | 1280x720 RGB, < 2 MB |
| `metadata.json` | per video: slug, file, title, description, tags, thumbnail_text, duration, script, url |
| Google Doc "<Model> YouTube Video Copy - <batch>" | from copy.html: notes, sources, contents, and per video title / description / tags / thumbnail / srt / script |
Naming: lowercase kebab, model first, then search words, then slug (`x3100-x-ray-smd-counter-b2-mes-erp-integration-4k.mp4`). Never overwrite or rename source clips.

## 2. YouTube title standard
- 40-70 characters (lint/meta enforce); main search phrase in the first 40 characters; Title Case.
- Patterns that worked: "How X-Ray SMD Counters Integrate with MES & ERP for SMT Inventory", "Inline vs Offline X-Ray SMD Counter for a Lights-Out SMT Warehouse", "Is X-Ray Counting Safe for Flash Memory, EEPROM & Sensitive ICs?", "What Is an X-Ray SMD Component Counter?".
- Question titles for FAQ/safety topics; "vs" for comparisons; "How to ..." for guides; a number only if it is a confirmed fact.
- No clickbait, no ALL CAPS words except acronyms, no emoji, no supplier names, no unconfirmed numbers. Unique within the channel.

## 3. Description standard (built by meta.py)
1. Line 1 (<= 160 chars, shown above "more"): the search phrase + the answer in one sentence.
2. Line 2: `<desc_cta>: WhatsApp +86 13602562576 (https://wa.me/8613602562576)`.
3. Summary 80-140 words: problem -> how the product solves it -> 3-5 confirmed specs -> what to send / test. Hedged wording copied from facts.md.
4. `Chapters:` from scene `ch` labels, starting 0:00, >= 10 s apart, 4-9 chapters, labels 2-6 words.
5. Landing page link with UTM `utm_source=youtube&utm_medium=video&utm_campaign=<utm_prefix>-<topic>`.
6. Footer: email, website, legal name + "since 2011", disclaimer (brochure figures / price quoted per order).
7. 2-5 hashtags (the first 3 show above the title).
Max 4,900 chars; no `<` or `>`.

## 4. Tags
13-15 tags, total <= ~480 chars: primary keyword, 3-5 long-tail variants of the topic, product category terms, model name ("smart ems x3100"), "southern machinery", 1-2 adjacent searches (e.g. "smt warehouse", "mes integration").

## 5. Thumbnail
3-5 words in 2-3 lines of Inter Black (white, one highlight word in gold), clean product still on the right in a rounded teal frame, SM logo plate top-left, product chip bottom-left. Readable at 320 px wide. No faces, supplier marks or small text.

## 6. Delivery message to Jason (Chinese)
One line on what was made + where; a table (topic, title, duration, Drive link); the Doc link; compromises (softened claims, missing footage, residual marks); the next decision (review, YouTube schedule). Not published until Jason approves.
