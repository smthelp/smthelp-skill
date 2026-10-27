# Changelog

## 2.1.0 - 2026-10-27
- HTML report output (render_html.py, assets/html/report.css; run.py --html/--no-pptx): one self-contained page per language from the deck spec. --customer-alias anonymises customer name in every output (QA E8), --slug sets file stem. First use: LED Driver Manufacturer THT auto insertion line solution evaluation report.

## 2.0.0 - 2026-10-26
- line_evaluation report type (several boards on a multi-machine line from PCBA photos: marked photos, cycle per machine, bottleneck + balance option, feeder plan, component readiness); mark_board.py; render16 'board' slide; machines S-3010 and S-70DL; Acuity Brands example reissuing the 2020 S-70DL PCBA Evaluation; EN fallback for untranslated strings (QA W3); PO-prevails disclaimer on every report; bullets slide full width without photo. sample_test cases from v1 run unchanged (Zebu figures identical).

## 1.0.0 - 2026-10-20
- First release, distilled from the Zebu (Brazil) ZK50 AUTO / S3000 radial sample test: case.json input, calc.py model (capacity, ramp, ROI, payback, benefits), make_spec.py (EN/PT i18n), render16.py on SM PPT template 202309 (A4 via smt-brand-kit), qa.py gate (E1-E6), run.py pipeline, bump_version.py, feedback log. Reference figures in references/method.md.

## 2.2.0 (2026-10-27)
- `scripts/render_web.py` + `assets/html/web.css`/`web.js`: multilingual marketing page (EN default, ES, PT, FR, AR rtl, RU, ZH), theme + language in localStorage (`?lang=` overrides), YouTube video modal, catalogue iframe viewer, 8 six-step blogs, FAQ, GEO quick answer, JSON-LD (Organization, Report, FAQPage, Blog, VideoObject list, Breadcrumb), hreflang, Chatwoot.
- `run.py --web` (exports web/strings_en.json, builds page) and `--board-alias` (Board 1..n, PCB/model numbers dropped).
- Example web dir for the LED driver line (assets/examples/acuity-pcba-line/web, 7 languages, 313 keys).
