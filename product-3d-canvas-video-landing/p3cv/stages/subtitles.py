"""Stage 5 - subtitles: word timings -> readable cues (<= max_cue_chars, break on punctuation),
voice.replacements applied to the displayed text (e.g. 'info at smthelp dot com' -> 'info@smthelp.com').
Writes vo/cues.json (used for burned-in subs) and out/<slug>-subtitles-en.srt."""
import json
from . import stage
from .. import log


def build_cues(segments, max_chars=42):
    """segments: [{start, text, words:[[s,e,w]...]}] -> [[t0, t1, text]]"""
    cues = []
    for seg in segments:
        text, t0 = seg["text"], seg["start"]; pos = 0; toks = []
        for w in seg["words"]:
            k = text.find(w[2], pos)
            k = pos if k < 0 else k
            toks.append([w[0], w[1], k]); pos = k + len(w[2])
        for n, tk in enumerate(toks):
            end = toks[n + 1][2] if n + 1 < len(toks) else len(text)
            tk.append(text[tk[2]:end].strip())
        cur = []

        def flush():
            if cur:
                cues.append([t0 + cur[0][0], t0 + cur[-1][1], " ".join(x[3] for x in cur)])
        for tk in toks:
            if cur and len(" ".join(x[3] for x in cur + [tk])) > max_chars:
                flush(); cur = []
            cur.append(tk); last = tk[3]; L = len(" ".join(x[3] for x in cur))
            if last.endswith((".", ":", "?", "!")) or (last.endswith(",") and L > max_chars // 2):
                flush(); cur = []
        flush()
    merged = []
    for c in cues:  # glue tiny orphan cues to the previous one
        if merged and len(c[2]) <= 8 and not merged[-1][2].endswith((".", ":")) and c[0] - merged[-1][1] < 0.3 \
                and len(merged[-1][2]) + len(c[2]) <= max_chars + 8:
            merged[-1] = [merged[-1][0], c[1], merged[-1][2] + " " + c[2]]
        else:
            merged.append(c)
    for i, c in enumerate(merged):
        nxt = merged[i + 1][0] if i + 1 < len(merged) else c[1] + 1
        c[1] = min(c[1] + 0.35, nxt - 0.02)
    return merged


def ts(x):
    h, m, s = int(x // 3600), int(x % 3600 // 60), x % 60
    ms = min(999, int(round((s - int(s)) * 1000)))
    return f"{h:02d}:{m:02d}:{int(s):02d},{ms:03d}"


def to_srt(cues):
    return "".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(cues))


@stage("subtitles", deps=["mix"], desc="Build cues.json and the SRT file")
def run(cfg, state):
    tl = json.loads(cfg.p("vo", "timeline.json").read_text())
    segs = []
    for s in tl["segments"]:
        j = json.loads(cfg.p("vo", f"s{s['i']:02d}.json").read_text())
        segs.append({"start": s["start"], "text": j["text"], "words": j["words"]})
    cues = build_cues(segs, cfg["voice"]["max_cue_chars"])
    for c in cues:
        for a, b in cfg["voice"]["replacements"].items():
            c[2] = c[2].replace(a, b)
    cfg.p("vo", "cues.json").write_text(json.dumps(cues))
    srt = cfg.p("out", f"{cfg.slug}-subtitles-en.srt"); srt.write_text(to_srt(cues), encoding="utf-8")
    log.get("subtitles").info("%d cues", len(cues))
    return {"cues": len(cues), "srt": str(srt.relative_to(cfg.proj))}
