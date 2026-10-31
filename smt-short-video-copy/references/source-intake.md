# Source intake

| Source type | How to read | What it is good for |
|---|---|---|
| Operation manual PDF | full text; render image-only pages | structure, steps, troubleshooting, parts list, safety; check its "not stated" notes |
| Spec sheet / brochure | full text | numeric specs (tag P/B/S) |
| Product landing page HTML | `fetch_sources.py` text extract | specs table, photo list, embedded YouTube IDs, FAQ; strip service promises (lead time, warranty, free install) |
| 3D drawing HTML (eDrawings) | text < 300 chars = viewer only | 360° turn and exploded-view shots by screen recording; not a spec source |
| Audio / podcast WAV | `transcribe_audio.py` | buyer search phrases, SEO keywords, troubleshooting vocabulary; never competitor names; audio-only specs = to confirm |
| Factory / run videos (YouTube, MP4) | frame sheets (smt-brand-kit extract_sources.py) | shot sources; crop supplier subtitles; no faces |

If a link cannot be opened (HTTP ≠ 200, login wall, empty body): say so in `META.sources` and the delivery message, then fill from public specs of the same SM model and general SMT FAT practice, tagging every such item 推测 / Assumed.
