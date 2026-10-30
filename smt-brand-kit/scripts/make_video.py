#!/usr/bin/env python3
"""Southern Machinery product video from a storyboard JSON.
English voice-over (edge-tts), burned + SRT subtitles, branded navy layout.

usage: make_video.py <video.json> <out.mp4> [--build DIR]
writes <out>.mp4 (subtitled), <out>-clean.mp4 (no burned subs), <out>.srt, <out>-scenes.json

video.json:
 {"format": "landscape" | "vertical",           1920x1080 promo or 1080x1920 Shorts/Reels
  "product_label": "Smart EMS X3100 X-ray Counter",
  "outro": {"title": "Smart EMS X3100", "subtitle": "X-ray Counter with Inspection", "image": "photos/x.jpg"},
  "voice": "en-US-AndrewNeural", "rate": "-4%",
  "scenes": [
   {"id": "s01", "kind": "still", "media": ["photos/a.jpg"], "box": "v"|"l",
    "kicker": "THE PROBLEM", "head": "Line one\\nLine two", "bullets": ["..."],      bullets: landscape only
    "vo": [["spoken text", "subtitle text or null"]]},
   {"kind": "clip", "clips": [{"src": "videos/a.mp4", "a": 16.3, "b": 22.0, "crop": [0.085, 0.86]}], ...},
   {"kind": "grid", "media": [4 photos], ...},
   {"kind": "specs", "specs": [["80 kV", "closed X-ray tube"], ...]},                  up to 8
   {"kind": "outro", "vo": [...]} ]}
"crop" keeps rows [top, bottom] of a clip (fractions) - use it to cut burned-in supplier
subtitles or watermarks. Spoken text spells numbers as words; subtitle text uses digits."""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
BD = os.path.normpath(os.path.join(HERE, "..", "assets", "brand"))
BRAND = json.load(open(os.path.join(BD, "brand.json"), encoding="utf-8"))
def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
CC = BRAND["colors"]
NAVY, NAVY2, GREEN, TEAL, WHITE, MUTED = rgb(CC["navy_deep"]), rgb(CC["navy_mid"]), rgb(CC["green"]), rgb(CC["teal"]), (255, 255, 255), rgb(CC["muted"])
FD = os.path.join(BD, "fonts") + "/"
LOGO, CIRCUIT = os.path.join(BD, "sm-logo.png"), os.path.join(BD, "circuit.png")
FPS = 30

args = sys.argv[1:]
B = "/tmp/smvid_build"
if "--build" in args:
    i = args.index("--build"); B = args[i + 1]; del args[i:i + 2]
SPEC, OUT = args[0], args[1]
os.makedirs(B, exist_ok=True)
S = json.load(open(SPEC, encoding="utf-8")); BASE = os.path.dirname(os.path.abspath(SPEC))
VERT = S.get("format", "landscape") == "vertical"
W, H = (1080, 1920) if VERT else (1920, 1080)
SCENES = S["scenes"]
for k, sc in enumerate(SCENES): sc.setdefault("id", f"s{k+1:02d}")


def P(p): return p if os.path.isabs(p) else os.path.join(BASE, p)
def F(w, s): return ImageFont.truetype(FD + f"Montserrat-{w}.ttf", int(s))


def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode: print(cmd[:400]); print(r.stderr[-3000:]); sys.exit(1)
    return r.stdout


def dur(p): return float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"'))


# ---------- TTS ----------
NOPROXY = "env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy -u ALL_PROXY -u all_proxy"
VOICE, RATE = S.get("voice", BRAND["voice_tts"]), S.get("rate", "+2%" if VERT else "-4%")
def tts(text, out):
    if os.path.exists(out) and os.path.getsize(out) > 1000 and open(out + ".txt").read() == text + VOICE + RATE: return
    open(B + "/t.txt", "w").write(text)
    for _ in range(3):
        subprocess.run(f'{NOPROXY} python3 -m edge_tts --voice {VOICE} --rate={RATE} -f {B}/t.txt --write-media "{out}.mp3"', shell=True, capture_output=True)
        if os.path.exists(out + ".mp3") and os.path.getsize(out + ".mp3") > 1000: break
    else:
        print("edge-tts failed (pip install edge-tts; it needs direct internet, proxies are unset)"); sys.exit(1)
    run(f'ffmpeg -v error -y -i "{out}.mp3" -af "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse" -ar 48000 -ac 1 "{out}"')
    open(out + ".txt", "w").write(text + VOICE + RATE)

LEAD, GAP, TAIL = (0.35, 0.25, 0.5) if VERT else (0.55, 0.35, 0.7)
cues, t = [], 0.0
for sc in SCENES:
    ls = []
    for i, (spk, sub) in enumerate(sc["vo"]):
        p = f"{B}/{sc['id']}_{i}.wav"; tts(spk, p); ls.append((p, dur(p), sub or spk))
    d = LEAD + sum(x[1] for x in ls) + GAP * (len(ls) - 1) + TAIL + ((1.2 if VERT else 1.5) if sc["kind"] == "outro" else 0)
    sc["dur"], sc["start"] = d, t; tt = t + LEAD
    for p, dd, sub in ls: cues.append((tt, tt + dd, sub, p)); tt += dd + GAP
    t += d
TOTAL = t; print("total", round(TOTAL, 1))


# ---------- helpers ----------
def cover(img, w, h, fx=0.5, fy=0.5):
    s = max(w / img.width, h / img.height); img = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    l = int((img.width - w) * fx); tp = int((img.height - h) * fy); return img.crop((l, tp, l + w, tp + h))


def mask(w, h, r=26):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255); return m


def base_bg():
    im = Image.new("RGB", (W, H), NAVY)
    g = Image.linear_gradient("L").rotate(-30 if VERT else -60, expand=True).resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), NAVY2), im, g)
    c = Image.open(CIRCUIT).convert("RGBA"); c = c.resize((int(c.width * 2.3), int(c.height * 2.3)))
    c.putalpha(c.split()[3].point(lambda v: int(v * 0.16))); im.paste(c, (W - c.width + 50, H - c.height + 50), c)
    d = ImageDraw.Draw(im)
    lx, ly, lw, lh = (60, 90, 330, 100) if VERT else (56, 38, 300, 92)
    d.rounded_rectangle((lx, ly, lx + lw, ly + lh), 15, fill=WHITE)
    lg = Image.open(LOGO).convert("RGBA"); gw = lw - 30; lg = lg.resize((gw, int(gw * lg.height / lg.width)), Image.LANCZOS)
    im.paste(lg, (lx + 15, ly + (lh - lg.height) // 2), lg)
    if not VERT and S.get("product_label"):
        f = F("SemiBold", 22); s = S["product_label"]
        d.text((W - 60 - d.textlength(s, font=f), 72), s, font=f, fill=MUTED)
        d.rectangle((W - 60 - d.textlength(s, font=f), 106, W - 60, 109), fill=GREEN)
    return im


def border(im, x, y, w, h):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x + 10, y + 16, x + w + 10, y + h + 16), 30, fill=(0, 0, 0, 125))
    sh = sh.filter(ImageFilter.GaussianBlur(17)); im.paste(sh, (0, 0), sh)
    ImageDraw.Draw(im).rounded_rectangle((x - 6, y - 6, x + w + 6, y + h + 6), 30, fill=GREEN)


def heading(d, x, y, sc, maxw, ks, hs):
    d.text((x, y), sc.get("kicker", ""), font=F("Bold", ks), fill=GREEN); y += int(ks * 1.9)
    fh = F("ExtraBold", hs)
    for ln in sc["head"].split("\n"):
        while d.textlength(ln, font=fh) > maxw: fh = F("ExtraBold", fh.size - 2)
    for ln in sc["head"].split("\n"): d.text((x, y), ln, font=fh, fill=WHITE); y += int(fh.size * 1.17)
    return y


def specs_panel(d, sc, x0, y0, cols, tw, th):
    for i, (v, l) in enumerate(sc["specs"][:8]):
        cx, cy = x0 + (i % cols) * (tw + 26), y0 + (i // cols) * (th + 26)
        d.rounded_rectangle((cx, cy, cx + tw, cy + th), 22, fill=WHITE)
        d.rectangle((cx, cy + 30, cx + 8, cy + th - 30), fill=GREEN if i % 2 == 0 else TEAL)
        fv = F("ExtraBold", 54)
        while d.textlength(v, font=fv) > tw - 50: fv = F("ExtraBold", fv.size - 2)
        d.text((cx + 34, cy + th * 0.25), v, font=fv, fill=NAVY)
        d.text((cx + 34, cy + th * 0.6), l, font=F("SemiBold", 27), fill=(70, 95, 105))


# ---------- scene backgrounds ----------
for sc in SCENES:
    bg = base_bg(); d = ImageDraw.Draw(bg); k = sc["kind"]; box = None
    if k == "outro":
        o = S.get("outro", {})
        contacts = [BRAND["web"], BRAND["email"], "WhatsApp " + BRAND["whatsapp"]]
        if VERT:
            d.rounded_rectangle((90, 300, 990, 550), 30, fill=WHITE)
            lg = Image.open(LOGO).convert("RGBA"); lg = lg.resize((820, int(820 * lg.height / lg.width)), Image.LANCZOS); bg.paste(lg, (130, 300 + (250 - lg.height) // 2), lg)
            d.text((90, 600), o.get("title", ""), font=F("ExtraBold", 80), fill=WHITE)
            d.text((90, 700), o.get("subtitle", ""), font=F("Bold", 46), fill=GREEN)
            box = (560, 830, 430, 560); y = 850
            for s_ in [BRAND["web"], BRAND["email"], "WhatsApp", BRAND["whatsapp"]]: d.text((90, y), s_, font=F("SemiBold", 38), fill=(230, 240, 244)); y += 68
        else:
            d.rounded_rectangle((150, 200, 970, 428), 26, fill=WHITE)
            lg = Image.open(LOGO).convert("RGBA"); lg = lg.resize((740, int(740 * lg.height / lg.width)), Image.LANCZOS); bg.paste(lg, (190, 200 + (228 - lg.height) // 2), lg)
            d.text((150, 480), o.get("title", ""), font=F("ExtraBold", 64), fill=WHITE)
            d.text((150, 560), o.get("subtitle", ""), font=F("Bold", 40), fill=GREEN)
            box = (1120, 150, 640, 800); y = 660
            for s_ in contacts: d.ellipse((150, y + 12, 170, y + 32), fill=TEAL); d.text((190, y), s_, font=F("SemiBold", 36), fill=(230, 240, 244)); y += 62
        sc["media"] = [o["image"]] if o.get("image") else sc.get("media", [])
        if not sc["media"]: box = None
    elif k == "specs":
        if VERT:
            heading(d, 70, 250, sc, 940, 36, 70); specs_panel(d, sc, 70, 560, 2, 455, 250)
        else:
            d.text((150, 190), sc.get("kicker", ""), font=F("Bold", 28), fill=GREEN)
            d.text((150, 240), sc["head"].replace("\n", " "), font=F("ExtraBold", 64), fill=WHITE)
            specs_panel(d, sc, 150, 380, 4, 380, 250)
    else:
        if VERT:
            heading(d, 70, 250, sc, 940, 36, 76)
            box = (90, 540, 900, 900) if sc.get("box", "v") == "v" else (60, 620, 960, 600)
        else:
            if sc.get("box", "v") == "v": box, tx, tw, top = (150, 150, 600, 832), 860, 980, 250
            else: box, tx, tw, top = (90, 200, 1120, 520), 1290, 560, 230
            y = heading(d, tx, top, sc, tw, 28, 66 if tx < 900 else 60)
            y += 34; d.rectangle((tx, y, tx + 90, y + 6), fill=TEAL); y += 50
            fb = F("SemiBold", 36 if tx < 900 else 33)
            for b in sc.get("bullets", []):
                while d.textlength(b, font=fb) > tw - 42 and fb.size > 22: fb = F("SemiBold", fb.size - 1)
                d.ellipse((tx, y + 10, tx + 22, y + 32), fill=GREEN); d.text((tx + 42, y), b, font=fb, fill=(230, 240, 244)); y += int(fb.size * 1.75)
            if y > 990: print("WARNING text too long in", sc["id"])
    if box:
        border(bg, *box); mask(box[2], box[3]).save(f"{B}/{sc['id']}_mask.png")
    sc["box_xy"] = box
    bg.save(f"{B}/{sc['id']}_bg.png")


# ---------- scene media + compose ----------
def media(sc):
    x, y, w, h = sc["box_xy"]; D = sc["dur"]; out = f"{B}/{sc['id']}_media.mp4"
    if sc["kind"] == "clip":
        ins, fl = "", []; tot = sum(c["b"] - c["a"] for c in sc["clips"])
        for i, c in enumerate(sc["clips"]):
            c0, c1 = c.get("crop", [0, 1])
            ins += f' -ss {c["a"]} -to {c["b"]} -i "{P(c["src"])}"'
            fl.append(f"[{i}:v]crop=iw:ih*{c1-c0}:0:ih*{c0},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={FPS},setsar=1[c{i}]")
        n = len(sc["clips"]); sp = max(1.0, min(D / tot, 1.7))
        fl.append("".join(f"[c{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,setpts={sp:.4f}*PTS,fps={FPS},tpad=stop_mode=clone:stop_duration={D}[v]")
        run(f'ffmpeg -v error -y {ins} -filter_complex "{";".join(fl)}" -map "[v]" -t {D:.3f} -an -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p "{out}"')
    else:
        ms = sc["media"]
        if sc["kind"] == "grid":
            g = Image.new("RGB", (w, h), WHITE); gw, gh = (w - 12) // 2, (h - 12) // 2
            for i, p in enumerate(ms[:4]): g.paste(cover(Image.open(P(p)).convert("RGB"), gw, gh), ((i % 2) * (gw + 12), (i // 2) * (gh + 12)))
            src = g
        else:
            fx, fy = sc.get("focus", [0.5, 0.5]); src = cover(Image.open(P(ms[0])).convert("RGB"), w, h, fx, fy)
        src.resize((w * 2, h * 2), Image.LANCZOS).save(f"{B}/{sc['id']}_still.png"); fr = int(D * FPS)
        run(f'ffmpeg -v error -y -loop 1 -i {B}/{sc["id"]}_still.png -vf "zoompan=z=\'1+0.07*on/{fr}\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={fr}:s={w}x{h}:fps={FPS},setsar=1" -frames:v {fr} -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p "{out}"')
    return out


for sc in SCENES:
    D = sc["dur"]; out = f"{B}/{sc['id']}.mp4"; fo = D - 0.33
    if not sc["box_xy"]:
        run(f'ffmpeg -v error -y -loop 1 -framerate {FPS} -i {B}/{sc["id"]}_bg.png -vf "fade=in:0:8,fade=out:st={fo:.2f}:d=0.33,format=yuv420p" -t {D:.3f} -c:v libx264 -preset veryfast -crf 18 "{out}"')
        continue
    m = media(sc); x, y, w, h = sc["box_xy"]
    run(f'ffmpeg -v error -y -loop 1 -framerate {FPS} -i {B}/{sc["id"]}_bg.png -i "{m}" -loop 1 -i {B}/{sc["id"]}_mask.png '
        f'-filter_complex "[1:v]format=rgba[m];[2:v]format=gray,scale={w}:{h}[k];[m][k]alphamerge[mm];[0:v][mm]overlay={x}:{y}:shortest=1,fade=in:0:8,fade=out:st={fo:.2f}:d=0.33,format=yuv420p[v]" '
        f'-map "[v]" -t {D:.3f} -r {FPS} -c:v libx264 -preset veryfast -crf 18 "{out}"')
    print("scene", sc["id"], round(D, 2))

open(f"{B}/list.txt", "w").write("".join(f"file '{B}/{s['id']}.mp4'\n" for s in SCENES))
run(f'ffmpeg -v error -y -f concat -safe 0 -i {B}/list.txt -c copy {B}/v.mp4')
ins = "".join(f' -i "{c[3]}"' for c in cues)
fl = ";".join(f"[{i}:a]adelay={int(c[0]*1000)}|{int(c[0]*1000)}[a{i}]" for i, c in enumerate(cues))
fl += ";" + "".join(f"[a{i}]" for i in range(len(cues))) + f"amix=inputs={len(cues)}:normalize=0,apad=whole_dur={TOTAL:.3f},loudnorm=I={-14 if VERT else -16}:TP=-1.5:LRA=11[a]"
run(f'ffmpeg -v error -y {ins} -filter_complex "{fl}" -map "[a]" -t {TOTAL:.3f} -ar 48000 -ac 2 -c:a pcm_s16le {B}/vo.wav')


# ---------- subtitles ----------
def ts(s, srt=True):
    h_, r = divmod(s, 3600); m_, s_ = divmod(r, 60)
    return f"{int(h_):02d}:{int(m_):02d}:{int(s_):02d},{int((s_-int(s_))*1000):03d}" if srt else f"{int(h_)}:{int(m_):02d}:{s_:05.2f}"


def split(txt, maxc):
    words = txt.split(); n = max(1, math.ceil(len(txt) / maxc)); per = len(txt) / n; out, cur = [], ""
    for w_ in words:
        if cur and len(cur) + 1 + len(w_) > per + 5 and len(out) < n - 1: out.append(cur); cur = w_
        else: cur = (cur + " " + w_).strip()
    return out + [cur]


srt, ev, k = [], [], 1
for a, b, txt, _ in cues:
    lines = split(txt, 30 if VERT else 52); groups = [lines[i:i + 2] for i in range(0, len(lines), 2)]
    tc = sum(len(" ".join(g)) for g in groups); t0 = a
    for g in groups:
        t1 = t0 + (b - a) * len(" ".join(g)) / tc; e = min(t1 + 0.13, b + 0.28)
        srt.append(f"{k}\n{ts(t0)} --> {ts(e)}\n" + "\n".join(g) + "\n"); k += 1
        ev.append(f"Dialogue: 0,{ts(t0, False)},{ts(e, False)},Sub,,0,0,0,," + "\\N".join(g)); t0 = t1
style = ("Style: Sub,Montserrat ExtraBold,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,3,2,80,80,330,1" if VERT else
         "Style: Sub,Montserrat SemiBold,42,&H00FFFFFF,&H00FFFFFF,&H64000000,&H64000000,0,0,0,0,100,100,0,0,3,14,0,2,200,200,30,1")
open(f"{B}/subs.ass", "w").write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{style}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n")
stem = OUT[:-4] if OUT.endswith(".mp4") else OUT
os.makedirs(os.path.dirname(os.path.abspath(stem)), exist_ok=True)
open(stem + ".srt", "w").write("\n".join(srt))
run(f'ffmpeg -v error -y -i {B}/v.mp4 -i {B}/vo.wav -vf "ass={B}/subs.ass:fontsdir={FD}" -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart -shortest "{stem}.mp4"')
run(f'ffmpeg -v error -y -i {B}/v.mp4 -i {B}/vo.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -movflags +faststart -shortest "{stem}-clean.mp4"')
json.dump([dict(id=s["id"], start=round(s["start"], 2), dur=round(s["dur"], 2)) for s in SCENES], open(stem + "-scenes.json", "w"), indent=1)
print("done", stem + ".mp4", round(dur(stem + ".mp4"), 1), "s")
