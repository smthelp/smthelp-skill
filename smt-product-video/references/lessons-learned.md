# Lessons learned — incident log

Record each new incident here with the date and the job. These are hard rules, not suggestions.

## 2026-09 — S-MVF01: empty CTA link
The first SEO description went out with "Learn more:" followed by no URL. **Rule: verify every CTA link opens and points at the right page before sending.**

## 2026-10 — S7000: empty CTA link again
A second description went out with "Product page:" and no URL. The corrected description lives in `youtube-description-final.txt` — always use the `-final` file, never an earlier draft. (A similarly-named file, `s7000-terminal-insertion-turnkey-line`, is a different product — check the filename.)

## 2026-10 — S7000: corrupt compressed version
A 54 MB YouTube-ready version shipped with a missing moov atom and did not play. **Rule: every compressed version gets a full decode check (`ffmpeg -i file -f null -`) before delivery.**

## 2026-10 — S7000: browser file-grant size limit
A 185 MB file failed the browser's file classification; 115 MB passed. **Rule: compress the upload version to ~100–120 MB.** The 4K master may be 200 MB+ and is not the upload file.

## 2026-10-17/18 — S7000: upload blocked at Google login, session expired
The managed/server browser never shares the user's own device login. Jason chose to log in himself; the session expired after ~2 h idle before he returned. **Rule: open the login-page session only when Jason is ready, and reopen it on his say-so if it expired. Never ask for his password.**

## 2026-11-12 — Radial Splicing Tape v1: subtitle PlayRes bug
The `subtitles` filter's default PlayRes (384×288) inflated 56pt text to ~420pt. Fixed by hand-writing ASS with PlayRes 3840×2160. **Rule: burn subtitles from hand-written ASS only.**

## 2026-11-12 — Radial Splicing Tape v1: missing cutter link
The first SEO description lacked the cutter page link; a post-delivery audit caught it. **Rule: the CTA checklist covers every related product page (tool/accessory included), not just the main product.**

## 2026-11-12 — Radial Splicing Tape: hash routing 404
Plain text fetch of `file.autoinsertion.com/#/Product landing Page` 404s. **Rule: enumerate the list with the live browser; fetch individual pages via `/public/Product landing Page/<file>.html`.**

## 2026-11-13 — Radial Splicing Tape v2: originals-only boundary
Jason corrected the approach: v1's AI clips were discarded; v2 was rebuilt using only his 28 supplied photos, no AI-generated footage. **Rule: when the user supplies originals, Mode B is mandatory and AI footage is never re-proposed for that product.**

## 2026-11-13 — Radial v2: frame-rounding drift
Concatenated video was 90.667 s vs 90.768 s voiceover (340 frames per segment rounds down). Fixed by padding the last frame with `tpad`. **Rule: check concat duration against the voiceover before the final encode.**
