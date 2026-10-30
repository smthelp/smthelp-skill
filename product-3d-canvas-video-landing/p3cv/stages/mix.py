"""Stage 4 - mix: lay segments on a timeline (lead_in, gap, tail), write vo/timeline.json and a
loudness-normalised vo/master.wav (48 kHz stereo, default -14 LUFS / -1.5 dBTP for YouTube)."""
import json
from . import stage
from ..util import ffprobe_duration, run as sh, need
from .. import log


def build_timeline(durs, lead_in, gap, tail):
    t = lead_in; segs = []
    for i, d in enumerate(durs):
        segs.append({"i": i, "start": round(t, 3), "dur": round(d, 3)}); t += d + gap
    return segs, round(t - gap + tail, 2)


@stage("mix", deps=["tts"], desc="Build timeline.json and loudness-normalised master.wav")
def run(cfg, state):
    need("ffmpeg"); v = cfg["voice"]; n = len(cfg["segments"])
    durs = [ffprobe_duration(cfg.p("vo", f"s{i:02d}.mp3")) for i in range(n)]
    segs, total = build_timeline(durs, v["lead_in"], v["gap"], v["tail"])
    for s, seg in zip(segs, cfg["segments"]):
        s["text"] = seg["text"]
        if seg.get("chapter"):
            s["chapter"] = seg["chapter"]
    cfg.p("vo", "timeline.json").write_text(json.dumps({"segments": segs, "total": total}, indent=1))
    inputs, flt = [], []
    for k, s in enumerate(segs):
        inputs += ["-i", str(cfg.p("vo", f"s{k:02d}.mp3"))]; ms = int(s["start"] * 1000)
        flt.append(f"[{k}:a]aresample=48000,adelay={ms}|{ms}[a{k}]")
    flt.append("".join(f"[a{k}]" for k in range(n)) +
               f"amix=inputs={n}:normalize=0,apad,atrim=0:{total},"
               f"loudnorm=I={v['lufs']}:TP={v['true_peak']}:LRA=11[out]")
    sh(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(flt), "-map", "[out]",
        "-ac", "2", "-ar", "48000", str(cfg.p("vo", "master.wav"))], code="E_AUDIO")
    log.get("mix").info("timeline %.1f s, %d segments", total, n)
    return {"total_s": total}
