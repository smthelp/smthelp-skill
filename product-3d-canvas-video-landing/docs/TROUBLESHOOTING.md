# Troubleshooting

Every failure is recorded in `state.json` (stage → error.code/message/hint), `logs/p3cv.log` (with traceback)
and `logs/events.jsonl`. `python3 -m p3cv status product.json` shows all of it plus render progress.

## Error codes
| code | typical cause | fix |
|---|---|---|
| E_CONFIG | missing key, bad JSON, scene `from_segment` out of range | follow the message; compare with the example |
| E_DEPENDENCY | ffmpeg / playwright / edge-tts missing | `bash scripts/setup_env.sh` |
| E_STAGE_ORDER | stage run before its dependency | run the stages named in the hint |
| E_DOWNLOAD | 404, spaces not encoded, proxy, file > max_mb | check URL (`%20`), raise `download.max_mb` |
| E_CAPTURE | viewer never rendered, eDrawings "Connection timed-out" | use another drawing (`capture:true`), or put frames in `img/tt/` and set `capture.enabled=false` |
| E_TTS | edge-tts network error or proxy | proxies are removed automatically; retry; check `voice.voice` name |
| E_AUDIO / E_FFMPEG | broken mp3, disk/I-O error | re-run `tts` for that segment (delete `vo/sNN.json`), keep tmp_dir on /tmp |
| E_SUBTITLE | word timings missing | re-voice the segment |
| E_ANIM | anim.module path wrong | path is relative to the project folder |
| E_ASSEMBLE | `insert_before` not found or not unique, template token unfilled | copy an exact unique line from `src/<base>.html` |
| E_VIDEO_BUILD | JS error in video page (bad scene keys, anim crash) | message shows the JS error; open `build/video_built.html?ar=169` |
| E_RENDER | workers keep dying | read `<tmp_dir>/<ar>_<k>.log`; lower `video.chunks` if RAM is short |
| E_THUMB | JS error in thumbnail | check `thumbnail.anim_*` |
| E_UPLOAD | gws not authenticated, quota | connect the Google account; re-run upload (skips files already there) |
| E_HOOK | hook command failed | run it by hand in the project folder |

## Sandbox / environment gotchas (learned in production)
- The sandbox can reset between turns: re-run `scripts/setup_env.sh` when imports fail (exit code 127 / ModuleNotFound).
- Playwright 1.49.1 works on Debian 13 arm64 with the "ubuntu20.04-arm64 fallback" build; WebGL needs SwiftShader flags (set by capture).
- Shell calls are limited to ~20 min: that is why render is detached and `mux --timeout 1100` can be called repeatedly.
- Never `pkill -f` a pattern that also appears in your own shell command line (it kills the shell).
- Writing MP4 directly to a network-mounted workspace can fail with I/O errors → renders go to `/tmp`, then copied.
- Parallel renders from other projects on the same machine slow everything down (≈2 frames/s total); `status` shows progress.
- Tailwind CDN pages show unstyled in sandbox screenshots (proxy); the delivered HTML is fine online.
- eDrawings: the mouse wheel zooms OUT, first frames stall; Three.js viewers are faster and more reliable.
