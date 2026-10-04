# Article brief — GEO + SEO B2B product marketing blog

Audience: global EMS / ODM / automotive-electronics / medical / industrial-control
procurement and manufacturing-engineering teams. Language: **English**.

## Structure (in order)

1. **H1** — primary keyword front-loaded + product category or model + `by Southern Machinery`
   (≤ 60 chars). Written as `# H1` in `contentMarkdown`.
2. **Answer block** — first 2–3 sentences after H1. Directly answers
   *"What is this machine used for?"* in plain, extractable language.
   This is what Google AI Overviews / Perplexity / ChatGPT Search lift.
3. **Cover image** right after the answer block, alt text = main keyword + product category.
4. **H2s** — one per concrete buyer question. Rotate the three AEO question types:
   - comparison (X vs Y, manual vs automated)
   - cost / efficiency (what does it really cost, what is the payback)
   - lifecycle (integration, programming, maintenance, training)
5. **H3** sub-sections every 100–150 words.
6. **FAQ** — 4–6 schema-ready `**Question?**` + answer pairs.
7. **CTA** — one clear next action.

## Keyword rules

- Primary keyword must appear in H1, within the first 100 words, and in ≥1 H2.
- LSI terms distributed naturally (THT, through-hole, insertion head, bowl feeder,
  reel feeder, CPH, wave soldering, board handling, EMS, changeover, rework).
- No keyword stuffing.

## Mandatory content blocks

- Typical application scenarios.
- How it integrates into a complete PCB assembly line (link only to confirmed official
  pages: `www.smthelp.com`, `file.autoinsertion.com`, `ph.smthelp.com`).
- Key selection-parameter list/table (AI-extractable).
- ROI / quality / throughput value: **formula block + worked example**, explicitly labelled
  `example` / `depends on configuration` / `subject to final technical confirmation`.
  Never a guaranteed ROI.
- FAQ + CTA.

## Length

- Body 1,000–1,500 English words (cluster-article depth).
- `excerpt` 80–160 words, written to be quotable as an AI summary.

## Truthfulness (non-negotiable)

- Every product fact must come from the selected source document.
- Never invent specs, capacity, accuracy, price, lead time, certifications,
  customer cases or guaranteed ROI.
- If the source has an estimate, label it.
- Missing data → write `not specified in source — contact Southern Machinery to confirm`.
- Model codes, parameters, capacity, accuracy, certifications: verbatim from source.

## Brand block (natural, not boilerplate)

Southern Machinery — founded 2011 in Shenzhen, China; 237+ global customers;
SMT/THT PCB assembly automation equipment; complete-line capability across SMT, THT,
wave soldering, board handling and inspection; high-efficiency, cost-effective,
global service, spare-parts support, professional training.

## API payload fields

```json
{
  "title": "...",
  "slug": "kebab-case-with-primary-keyword",
  "excerpt": "80-160 words",
  "coverImage": "https://ph.smthelp.com/...",
  "contentMarkdown": "# H1\n\n...",
  "status": "published",
  "source": "ai",
  "seoTitle": "Primary Keyword | Southern Machinery",
  "seoDescription": "140-160 chars, procurement intent",
  "tags": ["SMT Line","THT Automation","Wave Soldering","Board Handling",
           "PCB Assembly Automation","EMS Manufacturing","Factory ROI",
           "Terminal Insertion","Odd Form Insertion"],
  "locale": "en"
}
```

## Topic de-duplication

Before writing, diff the planned angle against **every** slug in the blog state file
and the last 4 weeks of topics. If the product is already covered, change the angle:
selection guide → line integration → cost comparison → maintenance → programming/training.
Never republish the same title or slug.
