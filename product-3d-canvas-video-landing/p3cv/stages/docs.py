"""Stage 11 - docs: write the voice-over script (timestamps) and the YouTube SEO file
(title, alternatives, Shorts title, description with auto chapters, tags, Shorts description,
wording notes). Chapters come from segments that carry a "chapter" label; the first chapter is
forced to 0:00 as YouTube requires."""
import json
from . import stage
from .. import log


def mmss(x):
    return f"{int(x // 60)}:{int(x % 60):02d}"


def chapters(tl):
    ch = [(s["start"], s["chapter"]) for s in tl["segments"] if s.get("chapter")]
    if ch:
        ch[0] = (0, ch[0][1])
    return [f"{mmss(a)} {name}" for a, name in ch]


@stage("docs", deps=["mix"], desc="Write VO script and YouTube SEO text")
def run(cfg, state):
    tl = json.loads(cfg.p("vo", "timeline.json").read_text()); seo = cfg["seo"]; v = cfg["voice"]
    vo = cfg.p("out", f"{cfg.slug}-voiceover-script-en.txt")
    lines = [f"{cfg['product_name']} - English voiceover script ({cfg['brand']['name']})",
             f"Voice: {v['voice']} ({v['provider']}), rate {v['rate']}. Total runtime {mmss(tl['total'])}", ""]
    for s in tl["segments"]:
        lines += [f"[{mmss(s['start'])}] {s['text']}", ""]
    vo.write_text("\n".join(lines), encoding="utf-8")
    out = cfg.p("out", f"youtube-seo-title-description-{cfg.slug}.txt")
    P = []
    P += ["=== YOUTUBE TITLE (main, 16:9) ===", seo.get("title", cfg["product_name"]), ""]
    if seo.get("alt_titles"):
        P += ["=== ALTERNATIVE TITLES ==="] + [f"{i+1}. {t}" for i, t in enumerate(seo["alt_titles"])] + [""]
    if seo.get("shorts_title"):
        P += ["=== SHORTS TITLE (9:16) ===", seo["shorts_title"], ""]
    P += ["=== DESCRIPTION ===", seo.get("description", "").rstrip(), ""]
    ch = chapters(tl)
    if ch:
        P += ["Chapters"] + ch + [""]
    if seo.get("hashtags"):
        P += [" ".join(seo["hashtags"]), ""]
    if seo.get("tags"):
        P += ["=== TAGS (comma separated) ===", ", ".join(seo["tags"]), ""]
    if seo.get("shorts_description"):
        P += ["=== SHORTS DESCRIPTION ===", seo["shorts_description"], ""]
    if seo.get("notes"):
        P += ["=== NOTES ON WORDING ==="] + [f"• {n}" for n in seo["notes"]]
    pv = cfg.get("privacy", {}) or {}
    if pv.get("notes") or pv.get("confidential"):
        P += ["", "=== CONFIDENTIALITY (check before publishing) ==="] + [f"• {n}" for n in pv.get("notes", [])]
        P += [f"• confidential source, not used in deliverables: {c}" for c in pv.get("confidential", [])]
    out.write_text("\n".join(P) + "\n", encoding="utf-8")
    tags_len = len(", ".join(seo.get("tags", [])))
    if tags_len > 500:
        log.get("docs").warning("tags are %d chars (YouTube limit 500)", tags_len)
    return {"script": str(vo.relative_to(cfg.proj)), "seo": str(out.relative_to(cfg.proj)), "chapters": len(ch)}
