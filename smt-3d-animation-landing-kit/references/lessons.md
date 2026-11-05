# Lessons from the field (2026-10 / 2026-11)

- Sandbox resets can wipe apt/pip installs mid-job (symptom: `No module named playwright`, chromium missing): re-run `scripts/setup_env.sh`; work files under /workspace survive.
- Playwright's own browser download is blocked on linux-arm64 sandboxes: use system `/usr/bin/chromium` (`common.chromium_path()`); WebGL via `--use-angle=swiftshader --enable-unsafe-swiftshader`.
- 4K CDP screenshots ≈ 0.45 s/frame on 2 vCPU (0.76 s when the box is busy). Background jobs die at 20 min → 30 s segments, one renderer at a time; two in parallel are not faster.
- Never `pkill -f render.py` from a command line that contains that string (kills the shell itself); use `pkill -f "render[.]py"`.
- `-movflags +faststart` directly on the network filesystem fails with "Error writing trailer": write to /tmp, then copy (`finish_video.py` does).
- edge-tts: run requests sequentially with retries (parallel → "No audio was received"); behind an authenticated proxy aiohttp needs explicit proxy headers (`tts.py` patches it).
- Spell numbers for TTS ("zero point eight seconds") and map back in captions via `video.phrases`; a merged token like "57-type" needs keyword "57", not "fifty".
- eDrawings exports often have unnamed bodies and return black face colours: pack one part per body and use `model_groups` for meaningful colours.
- Hidden PDF watermark/logo overlays of eDrawings: hide `#edrawings-logo*` before screenshots.
- Source landing pages may use a different salesperson's contacts (e.g. Leon for feeders): ask before publishing.
- Do not let a JS constant shadow another (`CH` changeover time vs `CH` chapters map broke the first tube animation) — keep module-level names distinct.
