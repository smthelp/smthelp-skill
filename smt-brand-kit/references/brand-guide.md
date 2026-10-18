# Southern Machinery brand guide (voice + visual)

Machine-readable tokens: `assets/brand/brand.json` (colours, contacts, socials, TTS voice). Scripts read that file; change a colour or contact there once.

## Who we are in every output
- Maker line: **Shenzhen Southern Machinery Sales and Service Co., Ltd.** - "Southern Machinery" in running text; SMT / THT equipment, PCB separators and spare parts since 2011, Xixiang, Bao'an, Shenzhen.
- Product naming: `Smart EMS <SM model> <plain product name>` on first mention, then `<SM model>`. Hero lines may add "made by Southern Machinery" / "by Southern Machinery".
- The supplier's model code (e.g. XC-3100E) appears only when Jason asks; default is the SM model (X3100). The supplier's company name, brand, logo, domain, phone, email, address, QR code and software splash never appear.
- Contact block (always the same order): smthelp.com · info@smthelp.com · WhatsApp +86 136 0256 2576 (link wa.me/8613602562576). Socials and libraries as in brand.json.

## Voice
- Engineering, concise, specific. Shop-floor scenes, real numbers with units, no hype adjectives ("revolutionary", "world-leading", "best-in-class").
- Lead with the buyer's problem, then the method, then the product. The product carries a method; it is not the hero of every sentence.
- Numbers only from sources, with their condition: "99.99 % (0201 example)", "6 - 10 s per 4 reels (chip 0201)". Ranges written `6 - 10 s`, units spaced `430 mm`, `< 1 µSv/h`.
- Every buyer-facing piece ends with a concrete next step: what facts to send (volume, parts, machine models, voltage, photo of label/nameplate) and where (info@smthelp.com / WhatsApp / form). Price is "quoted per order".
- English is the source language; other languages are translations of the English (see smt-product-landing-page translation brief).
- Headings and titles never contain: hook, diagnosis, framework, vehicle, loop, CTA (zh: 钩子, 诊断, 框架, 载体, 循环, 行动号召). Never name the Dan Koe steps.
- Banned in copy: price, discount, lead time, stock, warranty, payment terms, customer names/orders, certificates without a certificate on file, throw-rate / yield / ROI / saving percentages, OEM affiliation. Third-party machine brands only to state compatibility, with a non-affiliation line.
- ROI is shown as a method or a calculator on the buyer's own inputs, never as a promised saving.

## Visual system
| Token | Value | Use |
|---|---|---|
| Navy | #003142 (deep #00243A, mid #003E57) | titles, backgrounds of video/poster, table headers |
| Green | #93AC3E | kicker text, rules, frames, accent bars, numbers in odd cards |
| Teal | #0097B2 | metric values, secondary accent, even cards |
| Grey | #4A5A63 | body text on white |
| Light | #EEF5F7 | card and metric backgrounds |
| Muted | #B2CDD6 | secondary text on navy |

- Logo: `assets/brand/sm-logo.png` always on a white rounded card when the background is dark; never recoloured, never stretched. Web pages use the logo URL in brand.json.
- Type: PPTX Microsoft YaHei (Latin + CJK safe); video and poster Montserrat ExtraBold (headlines) / SemiBold (body) / Bold (kickers, uppercase); web pages use the landing-page CSS.
- Pattern: faint circuit artwork (`circuit.png`, 15 % opacity) on navy, bottom-right.
- Photos: rounded corners with a 6-7 px green frame and soft shadow on navy; cover-crop with an explicit focus point; one subject per photo; no people's faces in marketing video unless Jason supplies them.
- Layout grammar shared by all outputs: KICKER (green, uppercase) -> headline (navy or white, ExtraBold) -> short sub -> evidence (photo / metric tiles / table) -> next step.
- PPTX: Southern Machinery template 2025 (A4 portrait), content inside x 0.45-7.82 in, y 1.3-10.85 in, title right of the template logo, green rule under it, template contact slide last.
- Poster: navy gradient, logo card top-left, product label top-right with green underline, headline, framed photo, 4 white metric tiles, benefits with green dots, white footer band with CTA, contacts and optional WhatsApp QR.
- Video: 1920x1080 promo (photo/clip box left, text right) and 1080x1920 Shorts (headline top, media box below), burned subtitles + .srt, voice en-US-AndrewNeural, outro with logo card and contacts.
