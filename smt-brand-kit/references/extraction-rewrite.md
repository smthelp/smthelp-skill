# Extraction and rewrite logic

## 1. Source priority (from learn-SMT-in-3-hours + product AGENTS.md)
1. Southern Machinery's own manual / spec sheet / brochure (current)
2. Supplier manual and brochure (current revision)
3. Quotation / packing list - structure and scope only, never prices or terms
4. Photos and video - appearance and process only
5. Old HTML, third-party pages - background only, never a spec source

## 2. Build facts.json (single source of truth)
- One row per fact: `key, label, value, unit, source (file + page/chapter), evidence`.
- Evidence labels: `v` Verified source, `c` To be confirmed, `t` Concept view (diagrams, flows we drew).
- Copy numbers exactly; keep the condition ("0201 example", "with printer", "Inline version").
- Two documents disagree:
  - If the difference matches a version, machine brand or option (steel grade, size, voltage, offline vs inline), record both under `versions` with what decides the choice - shown as a green "By version" table (Jason 2026-10-15).
  - Otherwise record both under `conflicts`, mark `c`, show both values with "confirm per order". Never average, never silently pick one.
- Translate Chinese supplier text into English facts yourself; keep the Chinese only in `extracted/`.

## 3. Scrub the supplier
- `kit.json supplier_terms`: company names (CN + EN + pinyin), brand marks, software names on splash screens, domains, emails, phone numbers, addresses, WeChat IDs. extract_sources.py lists candidates; add them before writing.
- Text: replace supplier contact with the SM contact block; drop "copyright / do not translate / reproduction prohibited" clauses of the supplier.
- Photos: paint over logos and nameplates (`rebrand_media.py photo --box`), write SOUTHERN MACHINERY or the SM model; skip photos where the mark cannot be removed cleanly; screenshots showing a supplier login or splash are left out.
- Video: cover watermark with the SM logo card, trim intro and end cards, drop supplier audio (`rebrand_media.py video`); burned Chinese subtitles are cropped out with the `crop` rows in video.json.
- Renaming: supplier model -> SM model (e.g. XC-3100E -> X3100) everywhere, including file names; keep the supplier code only if Jason asks.

## 4. Rewrite into copy.json (Southern Machinery voice)
Write the master copy once, in English, then every output pulls from it:
- `tagline` (<= 8 words, verb first), `headline` (what it does, with the key number), `subhead` (how, one sentence).
- `one_paragraph_answer`: who makes it, what it is, what it does, how, who uses it - quotable by AI answer engines (GEO).
- `pains` (3): shop-floor problem -> cost -> why the usual fix fails.
- `steps` (3-4): how the product works, each a verb + object, values from facts.json.
- `metrics` (4): the four numbers a buyer remembers, each with its condition.
- `benefits` (3-4): one line each, <= 52 characters for the poster.
- `before_you_order` (5): facts the buyer sends; ends every deliverable.
- `faq` (6-8): speed/accuracy, compatibility, packages/sizes, data/integration, safety, inspection/extra mode, price & lead time (answer: quoted per order), power & space.
- `evidence_note`: one sentence naming the documents behind the numbers.
Supplier marketing claims without a document behind them ("best", "No.1", "patented", percentages of savings) are dropped, not softened.

## 5. Language and numbers
- English source; translations by one subagent per language (smt-product-landing-page translation-brief.md) for the landing page. PPT, poster, video and manual are English unless Jason asks for another language - then translate copy.json first and render again.
- Spoken video text writes numbers as words ("zero one zero zero five"); subtitles use digits ("01005").
