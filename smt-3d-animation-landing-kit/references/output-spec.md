# Output specification

| File (in `<work>/out/`) | Spec |
|---|---|
| `<slug>.html` | single self-contained file; all CSS/JS inline; images as data: URIs (webp); 3D model as inline JSON (gzip+base64); < 4 MB target |
| `<slug>-16x9-4k.mp4` | 3840×2160, 30 fps, H.264 CRF 18, AAC 192 k, −14 LUFS, 60–180 s, burned-in captions |
| `<slug>-9x16-4k.mp4` | 2160×3840, same audio/timeline |
| `subtitles_en.srt` | word-timed cues ≤ 54 chars, numbers restored via `video.phrases` |
| `youtube-thumbnail-<slug>-1280x720.jpg` (+ `-3840x2160`) | < 2 MB |
| `shorts-cover-<slug>-1080x1920.jpg` | |
| `youtube-seo-<slug>.txt` | title, alt titles, description with chapters (first 0:00), links, tags ≤ 500 chars, Shorts title/description |
| `verify/verify_report.json` + screenshots | automated checks |

## Page modules
hero (stats, 2 photos) · duel (tabs, play/pause, slow-mo, metrics, badges) · why · how (two columns) · **model3d** (WebGL viewer: rotate, zoom, reset,
auto-rotate, materials industrial/matte/x-ray, lighting studio/warm/top, explode; fallback image) · specs · fit check · **ROI** (labour + output, payback) ·
benefits · gallery (lightbox) · videos (click-to-load) · **blogs ×8** · docs · FAQ (FAQPage JSON-LD) · contact · footer (brand blocks) · WhatsApp FAB ·
language selector (7, RTL) · dark-mode toggle.

## Network policy
On load: zero requests (verified). On user action only: YouTube iframe, outbound links. On http/https only: Chatwoot SDK.
