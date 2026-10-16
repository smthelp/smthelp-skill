# Page structure, i18n key families and product.json

Section order (ids): top(hero) → metrics/trust → answer → why → how(+concept flow) → fit → spec → disclosure → learn → roi → gallery → videos → catalog → blog → service → faq → contact → footer(CTA band, socials, links).

## Key families in i18n/en.json (n = numbered; builder counts them)
- meta/SEO: `__meta`, seo_title, seo_desc, seo_keys, og_title, og_desc
- header/nav: topbar, brand_sub, nav_*, aria_*, lb_alt
- hero: hero_badge, hero_h1a, hero_h1b, hero_sub, hero_cta1, hero_cta2; metrics `m{n}v/m{n}l`; trust `tr{n}`
- answer: ans_kick, ans_h2, ans_p, qf_h, `qf{n}k/qf{n}v`
- why: why_kick/h2/lead, w1-3 t/d, why_quote
- how: how_kick/h2/lead, h1-4 t/d (labels from product.json how_labels), dg1-6, dg_title, dg_yes, dg_no, ev_v, ev_c, ev_t
- fit: fit_kick/h2/lead, f1-3 tag/t/d/l1-l3/r (images from product.json fit_images)
- spec: spec_kick/h2/lead, sh_p/v/s/e, `s{n}p/s{n}v/s{n}s` (evidence per row in product.json spec_evidence)
- open points: disc_kick/h2/lead/ev, dh_p/a/b/c/s, `d{n}p/a/b/c`
- learn: learn_kick/h2/lead, `l{n}t/l{n}d/l{n}c`, fc_h, fc_lead, `fc{n}`, mc_h, `mc{n}` (mc1 = evidence text, rendered from mc2)
- payback calculator (formula fixed: value = count x share x minutes x rate; cost = count x upkeep minutes x upkeep rate; relabel the inputs per product): roi_*, calc_*, c_*, r_*, unit_month, unit_year (inputs ids are fixed in runtime.js; change formula there)
- gallery: gal_kick/h2/lead + caption keys named in product.json gallery
- videos: vid_kick/h2/lead/more + keys named in product.json videos
- catalog: cat_kick/h2/lead/preview/open/more/frame + keys named in product.json catalogs
- blog: blog_kick/h2/lead/note, `bl{n}t/bl{n}s` (n = 1..len(blogs.json))
- service: svc_kick/h2, `sv{n}t/sv{n}d` (icons in product.json)
- faq: faq_kick/h2, `q{n}/a{n}`
- contact/footer: ct_*, form_*, wa_btn, mail_btn, fcta_*, foot_*, soc_*

## product.json
```json
{
 "file": "<model>-<slug>-smart-ems-pcb-assembly.html",
 "canonical_base": "https://www.smthelp.com/",
 "storage_prefix": "shortname_",
 "product_name": "...", "alternate_names": ["MODEL"], "category": "...", "breadcrumb_category": "...",
 "date_published": "YYYY-MM-DD",
 "gallery": [{"md": "https://ph.smthelp.com/...md.jpg", "full": "https://ph.smthelp.com/....jpg", "key": "g1t"},
             {"file": "photos/local-photo.jpg", "key": "g2t"}],
 "embed_px": 720, "embed_q": 55,
 "calc_defaults": ["count", "share %", "minutes", "rate", "upkeep minutes", "upkeep rate", "price"],
 "hero": [0, 1, 2, 3, 4],
 "fit_images": ["url1", "url2", "url3"],
 "how_labels": ["01", "02", "03", "04"],
 "videos": [{"id": "YouTubeId", "t": "v1t", "d": "v1d", "dur": "1:01"},
            {"src": "videos/clip.mp4", "poster": "videos/clip-poster.jpg", "t": "v2t", "d": "v2d", "dur": "0:48"}],
 "fit_images": [1, 2, "https://ph.smthelp.com/...md.jpg"],
 "catalogs": [{"t": "cat1t", "d": "cat1d", "url": "https://file.autoinsertion.com/...", "type": "PDF"}],
 "spec_evidence": {"1": "v", "2": "c"},
 "ld_spec_rows": [1, 2, 3],
 "disambiguation": "Open points summary for JSON-LD.",
 "howto_name": "...", "howto_tools": ["..."],
 "service_icons": ["🎥", "🧑‍🔧", "⚙️", "🏭"]
}
```
Catalogue URLs from file.autoinsertion.com embed fine in the in-page iframe viewer (no X-Frame-Options as of 2026-10).
