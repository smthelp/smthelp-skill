# Output contract

One file: `<out>/<page.json file>`.

- Self-contained: CSS, JS, translations, report images and logo inlined; opens by double-click with no server.
- Offline: hero, quick answer, all report sections, bar charts, tables, galleries, blogs, FAQ, language and theme switch work without network.
- Online extras only from `cdn_whitelist`: YouTube thumbnails/player (i.ytimg.com, youtube.com), catalogue iframe (file.autoinsertion.com), Chatwoot (chat.smthelp.com, skipped on file://).
- Semantic: header > nav, main > section × n, figure/figcaption, table with th scope, details/summary, footer. One h1.
- Responsive 360–1440 px (grid collapses ≤900 px), print stylesheet, prefers localStorage theme, Arabic rtl.
- SEO/GEO: title/description/keywords, canonical, hreflang per language + x-default, OG/Twitter, JSON-LD @graph (Organization, Report, FAQPage, Blog, ItemList of VideoObject, BreadcrumbList), quick-answer paragraph + facts table.
- Sections (default order): hero, quick answer, report slides, videos, documents, blog, FAQ, contact (cta slide), footer with socials, catalogue board, photo site, email, WhatsApp.
- Never contains: customer name, contacts, prices, payment/delivery terms, warranty, destination country, part numbers listed in `redact`.
- `<meta name="generator">` records the skill version used.
