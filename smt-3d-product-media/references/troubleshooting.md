# Error codes

| code | meaning | fix |
|---|---|---|
| J01 | wrong/missing `schema` | set `smt-3d-product-media/job@1`; older majors: see versioning.md migration |
| J02-J06 | product/CAD missing or unreadable format | give model; export STEP AP214 from SolidWorks (File > Save As > STEP AP214) |
| J10-J12 | scene missing id/dur, unknown action, missing caption | fix the scene |
| J20-J21 | real clip file missing / caption missing | fix path or caption |
| J30-J31 | voice language or line text missing | add `voice.voices.<lang>` / line text |
| J40-J41 | deck enabled but spec missing | add `deck.spec.<lang>` |
| J50 | no disclosure (warning) | add one when the 3D differs from the machine |
| C01-C02 | CAD conversion failed | re-export STEP; check `pip install cascadio`; GLB also accepted |
| R01 | a render worker crashed | read its traceback; rerun `render` (resumes) |
| M01 | an ffmpeg/ffprobe/curl command failed | message shows stderr; output dir on a network FS -> the skill already encodes in /tmp |
| M10-M11 | frames missing for the sequence | run `render` / `real` first |
| M20 | encoded video shorter than its frames | rerun `compose` (interrupted encode) |
| M30 | voice enabled but no audio | run `voice` |
| V01 | TTS request failed | network to speech.platform.bing.com needed; proxies are stripped on purpose (edge-tts rejects proxy logins containing ':'); retry later or set voice.enabled false |
| V10 | voice line longer than its slot (warning) | shorten the text |
| D01-D02 | deck builder missing / failed | clone smt-product-ppt-rebrand next to this skill or set deck.builder; read builder output (E/Q codes in its error-handling.md) |
| P01-P02 | publish failed | install/authorise gws, or upload out/ by hand |

## Known environment limits
- No GPU/OpenGL needed: the renderer is a numba CPU z-buffer (first call compiles, ~10 s).
- eDrawings HTML and Parasolid (.x_t) cannot be read; ask for STEP.
- JuiceFS / network mounts break `ffmpeg -movflags +faststart` in place: encodes go to the temp dir and are copied.
