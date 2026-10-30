# Error codes
| Code | Meaning | Action |
|---|---|---|
| E01 | project.json missing | set SMV_PROJECT to the project dir |
| E02 / W01 | ffmpeg missing / no libass | install ffmpeg with libass |
| E10-E13 | slug / video keys / SEO entry / first chapter | fix content module |
| W14 | scene > 70 words | split the scene |
| E15 | shot id unknown | add to shots.py or fix typo |
| E16 / W16 | callout too long | shorten headline / bullets |
| E17 | estimated length outside 60-175 s | add or cut scenes |
| W18 | shot used > 2x in a video | swap in a variant or slide |
| E20 / E21 | slide id undefined / unknown slide type | add to SLIDES or slides.py |
| E30 | forbidden claim | rephrase per design-copy-standard §5 |
| W31 | example-only figure not labelled | add "brochure example" / "example" |
| E40-E44 | SEO limits (title, tags, first line, duplicates); E40 in meta also = video not rendered | fix SEO dict / render first |
| E45 | < or > in title/description | write "below" / "above" |
| E50 / E51 | 4K output missing / spec mismatch | re-run `run.sh 4k <slug>`; check log.txt |
| prep failed (build/<slug>.<tag>.prep.log) | ffmpeg filter or missing TTS | read the log tail; run tts for the slug |
| compose job died | session ended / OOM | `rm -rf build/<slug>/4k`, rerun one at a time |
| edge-tts timeout | proxy | run with proxies unset (run.sh does), retry |
| "WARN footage stretched beyond 0.5x" | scene longer than its clips | add a shot or a slide to that scene |
| gws upload fails | credential / folder id | check the connected Google account and folder access; never retry a write without checking whether it landed |
If the same step fails twice, stop and report what is done and what blocks.
