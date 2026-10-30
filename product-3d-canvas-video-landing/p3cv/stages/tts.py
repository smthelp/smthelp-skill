"""Stage 3 - tts: one mp3 + word-timing json per segment in vo/ (sNN.mp3, sNN.json).
Resumable: a segment whose json exists AND whose text is unchanged is skipped, so editing one
sentence only re-voices that sentence."""
import json
from . import stage
from ..tts import PROVIDERS
from ..errors import P3VError
from ..util import retry
from .. import log


@stage("tts", desc="Synthesize voice-over per segment (edge-tts by default)")
def run(cfg, state):
    lg = log.get("tts"); v = cfg["voice"]
    synth = PROVIDERS.get(v["provider"])
    if not synth:
        raise P3VError("E_CONFIG", f"unknown voice.provider {v['provider']}", "see p3cv/tts/__init__.py")
    made = 0
    for i, seg in enumerate(cfg["segments"]):
        js, mp3 = cfg.p("vo", f"s{i:02d}.json"), cfg.p("vo", f"s{i:02d}.mp3")
        if js.exists() and mp3.exists() and json.loads(js.read_text()).get("text") == seg["text"]:
            continue
        try:
            words = retry(lambda: synth(seg["text"], str(mp3), v), tries=3, what=f"tts s{i:02d}")
        except Exception as e:
            raise P3VError("E_TTS", f"segment {i}: {e}", "network/proxy? edge-tts needs proxy vars unset")
        if not words:
            raise P3VError("E_TTS", f"segment {i}: no word timings returned")
        js.write_text(json.dumps({"text": seg["text"], "words": words}, ensure_ascii=False))
        made += 1; lg.info("voiced s%02d (%d words)", i, len(words))
    return {"segments": len(cfg["segments"]), "new": made}
