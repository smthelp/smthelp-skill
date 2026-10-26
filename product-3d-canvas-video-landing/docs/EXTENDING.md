# Extending p3cv without touching core logic

Rule: product-specific behaviour lives in `product.json`, the product's `anim.js`, or a **plugin file**.
Core changes are only for things every product benefits from (and get a version bump + test).

## 1. Plugins (preferred)
List Python files in product.json: `"plugins": ["plugins/my_plugin.py"]`. They are imported before the
pipeline runs and may register anything below. Working example: `examples/plugins/example_plugin.py`
(adds a `manifest` stage and a `webhook` sink).

## 2. New stage
```python
from p3cv.stages import stage
@stage("translate", deps=["subtitles"], desc="Spanish SRT")
def run(cfg, state):
    ...                                  # read cfg.p("vo","cues.json"), write cfg.p("out", "...")
    return {"srt": "out/x-es.srt"}       # recorded in state.json + events.jsonl
```
Raise `p3cv.errors.P3VError(code, message, hint)` for expected failures.

## 3. New 3D viewer (capture adapter)
`ADAPTERS[kind] = fn(page, capture_cfg, out_dir, log) -> [frame paths]`. `kind` must match what
`stages/download.classify()` returns (extend classify for a new viewer, or set `viewer` in sources).

## 4. New voice provider
`from p3cv.tts import PROVIDERS; PROVIDERS["azure"] = synth` with `synth(text, out_mp3, voice_cfg) -> [[start, end, word], …]`.
Word timings are required (subtitles). Select with `"voice": {"provider": "azure"}`.

## 5. New delivery sink
`from p3cv.sinks import SINKS; SINKS["webdav"] = upload` with
`upload(files, folder_name, upload_cfg, log) -> {"location": str, "files": [{"name", "bytes"}]}`.

## 6. New video scene type
In `templates/video.html` add to `SCENE_TYPES`:
```js
SCENE_TYPES.quote = function(sc, L, api){
  var q = mk(L, '<div class="big" style="font-size:6vh">'+sc.text+'</div>', V ? "left:7vw;top:30vh" : "left:8vw;top:35vh");
  return function(t, tAbs){ setIn(q, t, 0.3) };   // t = seconds since scene start
};
```
Then use `{"type": "quote", "from_segment": 4, "text": "…"}` and add the type to the schema enum.
Helpers: `mk`, `setIn`, `chip`, `times`, `turntable`, `pick` (per-aspect values), `V` (true in 9:16).

## 7. Animation module
Copy `templates/anim-template.js`. Keep every motion a pure function of `t` (no timers, no randomness),
world space 1600×1000, honour `focus`, `theme`, `noBox`, `noHud`, `noLabels`. One `STEPS` entry per landing step.

## 8. Hooks
Quick checks without Python: `"hooks": {"post_video": "test -s r/preview/sheet_169.jpg"}`.

## Upgrading the core safely
1. Change code; keep `DEFAULTS` backward compatible (new keys get defaults).
2. `python3 -m unittest discover -s tests`; smoke render the example (`video.scale 1, max_seconds 3`).
3. Bump `VERSION`, add a `CHANGELOG.md` entry, update `SKILL.md` version line; commit + tag `p3cv-vX.Y.Z`.
