# One content module per batch (content/batch1.py, batch2.py ...). Select with SMV_BATCH.
# Narration is the subtitle text; every claim must be in content/facts.md.
# Scene keys: text (2-3 sentences), vis (shot ids and/or 'slide:<id>'), co (callout card), ch (YouTube chapter label).
# Callout: k = KICKER (caps), h = headline (<=60 chars), b = up to 4 bullets (<=48 chars), stat = big number (optional).
# Video keys: slug, topic (utm), kicker, title (right-panel title), intro_title (\n = line break), intro_shot (shot, t),
#             music (0-5 chord progression), mirror (footage on the right), outro / outro_head / footer_cta / desc_cta (optional overrides)

OUTRO_TEXT = ("Want to see it on your own parts? Ask us for a free trial. "
              "WhatsApp +86 136 0256 2576, or visit smthelp.com.")

SLIDES = {
  # data-driven motion-graphic slides (types: rows, stat, formula, flow, split, table, grid, bars)
  'howitworks': dict(type='flow', kicker='HOW IT WORKS', heading='Three steps', steps=[('Load', 'up to 4 reels'), ('Count', 'one X-ray shot'), ('Label', 'and upload')], hl=1),
}

VIDEOS = [
 dict(slug='what-is-it', topic='what-is-it', kicker='SMART EMS MODEL · BASICS', music=0,
      title='What is a ...?', intro_title='What is a\n...?', intro_shot=('A1', 1.0),
      scenes=[
        dict(ch='The problem', vis=['A1'], co=dict(k='THE PROBLEM', h='...', b=['...']), text="..."),
        dict(ch='How it works', vis=['slide:howitworks'], co=dict(k='HOW IT WORKS', h='...', b=['...']), text="..."),
      ]),
]

SEO = {
 'what-is-it': dict(
   title='What Is a ...? (40-70 characters, main keyword first)',
   kw="First description line: keyword-rich, <=160 characters, answers the search.",
   summary="80-140 words. Problem, how the product solves it, 3-5 confirmed specs, CTA to test with own parts.",
   tags=['main keyword', '...13-15 tags total...', 'southern machinery'],
   hashtags=['#SMT', '#Keyword'],
   thumb='3-5 WORDS\nIN CAPS', thumb_hi='WORDS', thumb_shot=('A1', 1.0)),
}

NOTES = []      # production notes shown at the top of the copy doc
SOURCES = []    # (name, url, what it supports) for any non-product claim
