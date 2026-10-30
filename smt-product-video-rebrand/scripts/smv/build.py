"""Timeline planner + renderer. Usage: python3 build.py <slug> <prev|4k>
Writes build/<slug>/<tag>/{window.mp4, audio.wav, subs.srt, subs.ass, plan.json, compose.sh}.
Run compose.sh (render.sh does it) to get out.mp4. Needs tts.py output first."""
import json, os, re, subprocess, sys, math, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg
import gfx
from PIL import Image

VIDEOS, OUTRO_TEXT, SEO = cfg.VIDEOS, cfg.OUTRO_TEXT, cfg.SEO
SHOTS, SRC = cfg.SHOTS, cfg.SRC
FPS = cfg.FPS
INTRO = cfg.B['video']['intro_seconds']
SR = 48000
# crop geometry per shot kind, in source pixels (override per shot with cw/ch)
KIND = {'p': (720, 864), 'm': (540, 648)}

def fr(t):  # round to frame
    return round(t * FPS) / FPS

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:]); raise RuntimeError(cmd[:300])
    return r.stdout

# ---------------------------------------------------------------- timeline
def plan(v):
    tts = json.load(open(f"{cfg.TTS}/{v['slug']}.json"))
    scenes = []
    t = INTRO
    for si, sl in enumerate(tts):
        outro = si == len(tts) - 1
        lead = 0.6 if outro else 0.15
        sents = []
        tt = t + lead
        for x in sl:
            sents.append(dict(text=x['text'], mp3=x['mp3'], start=tt, end=tt + x['dur']))
            tt += x['dur'] + 0.22
        end = fr(tt - 0.22 + (2.2 if outro else 0.45))
        sc = dict(start=fr(t), end=end, sents=sents, outro=outro)
        if not outro:
            sc.update(v['scenes'][si])
        scenes.append(sc)
        t = end
    return scenes, t

def alloc_visuals(sc):
    """split scene into window items: (kind, id, dur, speed/src_len)"""
    D = sc['end'] - sc['start']
    vis = sc['vis']
    foot = [x for x in vis if not x.startswith('slide:')]
    slides = [x for x in vis if x.startswith('slide:')]
    items = []
    want = {x: (SHOTS[x]['b'] - SHOTS[x]['a']) / 0.75 for x in foot}
    maxlen = {x: (SHOTS[x]['b'] - SHOTS[x]['a']) / 0.5 for x in foot}
    if slides:
        fsum = sum(want.values())
        rem = D - fsum
        if rem < 3.0 * len(slides):
            k = max(0.2, (D - 3.0 * len(slides)) / max(fsum, 0.01)) if fsum else 0
            want = {x: want[x] * k for x in foot}
            rem = D - sum(want.values())
        dur = {x: want[x] for x in foot}
        for s in slides: dur[s] = rem / len(slides)
    else:
        fsum = sum(want.values())
        k = D / fsum
        dur = {x: want[x] * k for x in foot}
        over = [x for x in foot if dur[x] > maxlen[x] + 0.01]
        if over:
            print('  WARN footage stretched beyond 0.5x in scene:', sc.get('ch') or sc['text'][:40], {x: round(dur[x] / maxlen[x], 2) for x in over})
    # minimum on-screen time per footage item
    mn = 1.6
    fixed = set()
    for _ in range(6):
        small = [x for x in foot if x not in fixed and dur[x] < mn]
        if not small: break
        fixed |= set(small)
        rest = [x for x in vis if x not in fixed]
        if not rest: break
        fsum_fixed = mn * len(fixed)
        tot_rest = sum(dur[x] for x in rest)
        k2 = (D - fsum_fixed) / tot_rest
        for x in fixed: dur[x] = mn
        for x in rest: dur[x] *= k2
    # frame-accurate
    acc = sc['start']; out = []
    for i, x in enumerate(vis):
        end = sc['end'] if i == len(vis) - 1 else fr(acc + dur[x])
        out.append((x, end - acc)); acc = end
    return out

# ---------------------------------------------------------------- window segments
def seg_filter(sid, d, S):
    W, H = int(1400 * S), int(1680 * S)
    sh = SHOTS[sid]
    L = sh['b'] - sh['a']
    boom = L / d < 0.5
    LL = 2 * L if boom else L
    speed = min(1.0, max(0.5, LL / d))
    srcl = min(L, d * speed)
    sharp = ',unsharp=5:5:0.5' if S >= 1 else ''
    if sh['kind'] in ('p', 'm'):
        cw, ch = sh.get('cw'), sh.get('ch')
        if not cw: cw, ch = KIND[sh['kind']]
        f = f"[0:v]crop={cw}:{ch}:{sh.get('x0', 0)}:{sh['y0']}"
        if sh.get('blur'):
            f += ',split=2[m][b0]'
            chain = '[m]'
            for i, bx in enumerate(sh['blur']):
                x, y, w, h = bx[:4]; sg = bx[4] if len(bx) > 4 else 16
                f += f";[b{i}]crop={w}:{h}:{x}:{y},gblur=sigma={sg}:steps=3[bb{i}]"
                nxt = f'[o{i}]'
                if i < len(sh['blur']) - 1:
                    f += f";{chain}[bb{i}]overlay={x}:{y},split=2{nxt}[b{i+1}]"
                else:
                    f += f";{chain}[bb{i}]overlay={x}:{y}{nxt}"
                chain = nxt
            f += f";{chain}"
        else:
            f += ','
            f = f[:-1] + ','
        if sh.get('zoom'):
            zx, zy, zw = sh['zoom']; zh = int(zw * ch / cw) // 2 * 2
            f += f"crop={zw}:{zh}:{zx}:{zy},"
        f += f"scale={W}:{H}:flags=lanczos{sharp},eq=contrast=1.04:saturation=1.05"
    else:  # landscape
        lw, lh, lx, ly = sh.get('lcrop', (960, 356, 0, 90))   # landscape crop in source px
        fh = int(W * lh / lw) // 2 * 2
        f = (f"[0:v]crop={lw}:{lh}:{lx}:{ly},split=2[a][b];[b]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.18:saturation=0.7[bg];"
             f"[a]scale={W}:{fh}:flags=lanczos{sharp}[fg];[bg][fg]overlay=0:(H-h)/2")
    if boom:
        f += f",trim=duration={L:.3f},setpts=PTS-STARTPTS,split=2[ff][rr];[rr]reverse[rv];[ff][rv]concat=n=2:v=1:a=0"
    f += f",setpts=(PTS-STARTPTS)/{speed:.4f},fps={FPS},tpad=stop_mode=clone:stop_duration=3,trim=duration={d:.4f},setsar=1,format=yuv420p[out]"
    return f, sh['a'], (L if boom else srcl) + 0.2

def render_window(v, scenes, S, tag):
    wd = f"{cfg.BUILD}/{v['slug']}/{tag}"
    os.makedirs(wd, exist_ok=True)
    W, H = int(1400 * S), int(1680 * S)
    items = [('slide:blank', INTRO)]
    for sc in scenes:
        if sc['outro']:
            items.append(('slide:blank', sc['end'] - sc['start']))
        else:
            items += alloc_visuals(sc)
    cmds = []; files = []
    slide_cache = {}
    for i, (vid, d) in enumerate(items):
        out = f"{wd}/w{i:03d}.mp4"; files.append(out)
        if vid.startswith('slide:'):
            sid = vid[6:]
            if sid not in slide_cache:
                ims = gfx.make_slide(sid, S); ps = []
                for j, im in enumerate(ims):
                    p = f"{wd}/slide_{sid}_{j}.png"; im.convert('RGB').save(p); ps.append(p)
                slide_cache[sid] = ps
            ps = slide_cache[sid]
            n = len(ps); per = d / n
            inp = ' '.join(f"-framerate {FPS} -loop 1 -t {per + 0.1:.3f} -i {p}" for p in ps)
            cc = ''.join(f"[{j}:v]scale={W}:{H},setsar=1,fps={FPS},trim=duration={(per if j < n - 1 else d - per * (n - 1)):.4f},setpts=PTS-STARTPTS[s{j}];" for j in range(n))
            cc += ''.join(f"[s{j}]" for j in range(n)) + f"concat=n={n}:v=1:a=0,format=yuv420p,trim=duration={d:.4f}[out]"
            cmd = f"ffmpeg -v error -y {inp} -filter_complex \"{cc}\" -map [out] -c:v libx264 -preset ultrafast -crf 14 -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r {FPS} -frames:v {round(d * FPS)} {out}"
        else:
            f, a, ln = seg_filter(vid, d, S)
            src = SRC + SHOTS[vid]['src'] + '.mp4'
            cmd = f"ffmpeg -v error -y -ss {a} -t {ln:.3f} -i {src} -filter_complex \"{f}\" -map [out] -an -c:v libx264 -preset ultrafast -crf 14 -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r {FPS} -frames:v {round(d * FPS)} {out}"
        cmds.append(cmd)
    # run 2 at a time
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(2) as ex:
        list(ex.map(run, cmds))
    with open(f"{wd}/list.txt", 'w') as fh:
        for p in files: fh.write(f"file '{p}'\n")
    run(f"ffmpeg -v error -y -f concat -safe 0 -i {wd}/list.txt -c copy {wd}/window.mp4")
    json.dump(items, open(f"{wd}/items.json", 'w'), indent=0)
    return f"{wd}/window.mp4", items

# ---------------------------------------------------------------- audio
def load_mp3(p):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', p, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-']).astype if False else \
        subprocess.check_output(['ffmpeg', '-v', 'error', '-i', p, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'])
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768

PROGS = [
 [[110.0, 138.59, 164.81, 220.0], [92.5, 138.59, 185.0, 220.0], [73.42, 146.83, 185.0, 220.0], [82.41, 123.47, 164.81, 207.65]],  # A F#m D E (batch 1)
 [[130.81, 164.81, 196.0, 261.63], [110.0, 130.81, 164.81, 220.0], [87.31, 130.81, 174.61, 220.0], [98.0, 123.47, 146.83, 196.0]],  # C Am F G
 [[146.83, 174.61, 220.0, 293.66], [116.54, 146.83, 174.61, 233.08], [87.31, 130.81, 174.61, 220.0], [130.81, 164.81, 196.0, 261.63]],  # Dm Bb F C
 [[98.0, 123.47, 146.83, 196.0], [82.41, 123.47, 164.81, 196.0], [130.81, 164.81, 196.0, 261.63], [146.83, 185.0, 220.0, 293.66]],  # G Em C D
 [[82.41, 123.47, 164.81, 196.0], [130.81, 164.81, 196.0, 261.63], [98.0, 123.47, 146.83, 196.0], [146.83, 185.0, 220.0, 293.66]],  # Em C G D
 [[116.54, 146.83, 174.61, 233.08], [98.0, 116.54, 146.83, 196.0], [77.78, 116.54, 155.56, 196.0], [87.31, 110.0, 130.81, 174.61]],  # Bb Gm Eb F
]

def music_bed(T, seed=0):
    n = int(T * SR); t = np.arange(n) / SR
    chords = PROGS[seed % len(PROGS)]
    seg = 8.0 if seed == 0 else [8.0, 6.0, 7.0, 9.0, 6.5][seed % 5]
    if seed:
        rng = np.random.default_rng(seed)
    out = np.zeros(n, np.float32)
    for ci in range(int(T / seg) + 2):
        ch = chords[ci % 4]
        s0 = (ci * seg - 2.0); s1 = s0 + seg + 4.0
        i0, i1 = max(0, int(s0 * SR)), min(n, int(s1 * SR))
        if i0 >= i1: continue
        tt = t[i0:i1]
        env = np.clip(np.minimum((tt - s0) / 2.0, (s1 - tt) / 2.0), 0, 1)
        env = 0.5 - 0.5 * np.cos(np.pi * env)
        sig = np.zeros_like(tt)
        for f in ch:
            for det in (-0.6, 0.6):
                sig += np.sin(2 * np.pi * (f + det) * tt) * 0.5
                sig += np.sin(2 * np.pi * (2 * f + det) * tt) * 0.12
        out[i0:i1] += (sig * env).astype(np.float32)
    if seed:
        # soft plucked arpeggio layer for variety (batch 2)
        pl = np.zeros(n, np.float32)
        step = seg / 8
        k = 0
        while k * step < T:
            ch = chords[int(k * step / seg) % 4]
            f0 = ch[[0, 1, 2, 3, 2, 1, 3, 2][k % 8]] * 2
            i0 = int(k * step * SR); i1 = min(n, i0 + int(1.6 * SR))
            tt = np.arange(i1 - i0) / SR
            pl[i0:i1] += (np.sin(2 * np.pi * f0 * tt) * np.exp(-tt * 3.2) * 0.35).astype(np.float32)
            k += 1
        out = out / (np.abs(out).max() + 1e-6) + pl * (0.5 + 0.3 * rng.random())
    out *= 0.5 + 0.15 * np.sin(2 * np.pi * 0.08 * t)
    out /= (np.abs(out).max() + 1e-6)
    fade = np.minimum(1, np.minimum(t / 2.5, (T - t) / 3.0)).clip(0, 1)
    return (out * fade).astype(np.float32)

def write_wav(p, x):
    x = np.clip(x, -1, 1)
    with wave.open(p, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def build_audio(v, scenes, T, wd):
    n = int(T * SR) + SR
    voice = np.zeros(n, np.float32)
    for sc in scenes:
        for s in sc['sents']:
            a = load_mp3(s['mp3']); i = int(s['start'] * SR)
            voice[i:i + len(a)] += a[:max(0, n - i)]
    write_wav(f"{wd}/voice.wav", voice[:int(T * SR)])
    write_wav(f"{wd}/music.wav", music_bed(T, v.get('music', 0)) * 0.5)
    run(f"ffmpeg -v error -y -i {wd}/voice.wav -i {wd}/music.wav -filter_complex "
        f"\"[0]asplit=2[v][sc];[1]volume={cfg.B['video']['music_volume']}[m];[m][sc]sidechaincompress=threshold=0.015:ratio=5:attack=40:release=700[md];"
        f"[v][md]amix=inputs=2:normalize=0:duration=first,loudnorm=I={cfg.B['video']['loudness_lufs']}:TP=-1.5:LRA=11,aresample=48000\" -ac 2 {wd}/audio.wav")
    return f"{wd}/audio.wav"

# ---------------------------------------------------------------- subtitles
def split_cue(text, maxc=84):
    if len(text) <= maxc: return [text]
    # split at punctuation closest to middle
    best = None
    for m in re.finditer(r'[,:;] ', text):
        k = m.end()
        a, b = text[:k].strip(), text[k:].strip()
        sc = max(len(a), len(b))
        if best is None or sc < best[0]: best = (sc, a, b)
    if best is None or best[0] > len(text) * 0.8:
        words = text.split(' '); half = len(text) / 2; acc = 0
        for i, w in enumerate(words):
            acc += len(w) + 1
            if acc >= half:
                best = (0, ' '.join(words[:i + 1]), ' '.join(words[i + 1:])); break
    return split_cue(best[1], maxc) + split_cue(best[2], maxc)

def wrap2(text, maxl=44):
    if len(text) <= maxl: return [text]
    words = text.split(' '); best = None
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        sc = max(len(a), len(b))
        if best is None or sc < best[0]: best = (sc, a, b)
    return [best[1], best[2]]

def cues(scenes):
    out = []
    for sc in scenes:
        for s in sc['sents']:
            parts = split_cue(s['text'])
            tot = sum(len(p) for p in parts); t0 = s['start']; dd = s['end'] - s['start']
            for p in parts:
                t1 = t0 + dd * len(p) / tot
                out.append(dict(start=t0, end=t1, text=p, outro=sc['outro']))
                t0 = t1
    for i in range(len(out) - 1):  # close tiny gaps
        if out[i + 1]['start'] - out[i]['end'] < 0.3: out[i]['end'] = out[i + 1]['start'] - 0.02
    return out

def ts_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def ts_ass(t):
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def write_subs(cl, srt, ass, mirror=False):
    with open(srt, 'w') as f:
        for i, c in enumerate(cl, 1):
            f.write(f"{i}\n{ts_srt(c['start'])} --> {ts_srt(c['end'])}\n" + '\n'.join(wrap2(c['text'])) + "\n\n")
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 3840
PlayResY: 2160
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Inter SemiBold,72,&H00FFFFFF,&H00FFFFFF,&H00100B04,&H80000000,0,0,0,0,100,100,0,0,1,3,0,2,1720,160,280,1
Style: Outro,Inter SemiBold,64,&H00FFFFFF,&H00FFFFFF,&H00100B04,&H80000000,0,0,0,0,100,100,0,0,1,3,0,2,200,200,190,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass, 'w') as f:
        if mirror:
            hdr = hdr.replace('0,0,1,3,0,2,1720,160,280,1', '0,0,1,3,0,2,160,1720,280,1')
        f.write(hdr)
        for c in cl:
            st = 'Outro' if c['outro'] else 'Main'
            txt = '\\N'.join(wrap2(c['text'], 44 if not c['outro'] else 70))
            f.write(f"Dialogue: 0,{ts_ass(c['start'])},{ts_ass(c['end'])},{st},,0,0,0,,{{\\fad(120,120)}}{txt}\n")

# ---------------------------------------------------------------- compose
def compose_cmd(v, scenes, T, S, tag, window, audio, out, crf=20):
    gfx.set_layout(bool(v.get('mirror')))
    wd = f"{cfg.BUILD}/{v['slug']}/{tag}"
    bg = gfx.make_bg(v, S, f"{wd}/bg.png")
    fx, fy = gfx.make_frame(bg, S, f"{wd}/frame.png")
    # intro still: X-ray tray image
    still = f"{wd}/still.png"
    if v.get('intro_shot'):
        shot_still(*v['intro_shot'], still)
    else:
        shot_still(*cfg.P['default_intro_shot'], still)
    gfx.make_intro(v, S, f"{wd}/intro_bg.png", f"{wd}/intro_txt.png", still)
    gfx.make_outro(S, f"{wd}/outro.png", v.get('outro_head'))
    co = []
    for i, sc in enumerate(scenes):
        if sc['outro'] or not sc.get('co'): continue
        p = f"{wd}/co{i:02d}.png"; gfx.make_callout(sc['co'], S, p)
        co.append((p, sc['start'] + 0.25, sc['end'] - 0.1))
    to = [sc for sc in scenes if sc['outro']][0]['start']
    wx, wy = int(gfx.WIN[0] * S), int(gfx.WIN[1] * S)
    cx, cy = int(gfx.CO[0] * S), int(gfx.CO[1] * S)
    NF = round(T * FPS)
    inputs = [f"-i {wd}/bg.png", f"-reinit_filter 0 -i {window}", f"-i {wd}/frame.png", f"-i {wd}/intro_bg.png", f"-i {wd}/intro_txt.png", f"-i {wd}/outro.png"]
    fc = [f"[0]loop=loop={NF}:size=1:start=0,setpts=N/{FPS}/TB,format=yuv420p[bg]",
          f"[2]loop=loop={NF}:size=1:start=0,setpts=N/{FPS}/TB[fr]",
          f"[bg][1:v]overlay={wx}:{wy}:eof_action=repeat[a0]",
          f"[a0][fr]overlay={fx}:{fy}:eof_action=repeat[a1]"]
    last = 'a1'
    for k, (p, a, b) in enumerate(co):
        inputs.append(f"-i {p}")
        idx = 6 + k; nf = round((b - a) * FPS); dd = b - a
        fc.append(f"[{idx}]loop=loop={nf}:size=1:start=0,setpts=N/{FPS}/TB,format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={dd - 0.3:.3f}:d=0.3:alpha=1,setpts=PTS+{a:.3f}/TB[c{k}]")
        fc.append(f"[{last}][c{k}]overlay=x='{cx}+{int(90 * S)}*max(0\\,1-(t-{a:.3f})/0.4)':y={cy}:eof_action=pass[b{k}]")
        last = f"b{k}"
    ni = round(INTRO * FPS)
    fc.append(f"[3]loop=loop={ni}:size=1:start=0,setpts=N/{FPS}/TB,format=rgba,fade=t=out:st={INTRO - 0.5}:d=0.5:alpha=1[ib]")
    fc.append(f"[4]loop=loop={ni}:size=1:start=0,setpts=N/{FPS}/TB,format=rgba,fade=t=in:st=0.15:d=0.5:alpha=1,fade=t=out:st={INTRO - 0.5}:d=0.5:alpha=1[it]")
    fc.append(f"[{last}][ib]overlay=0:0:eof_action=pass[i1]")
    fc.append(f"[i1][it]overlay=x='-{int(80 * S)}*max(0\\,1-t/0.7)':y=0:eof_action=pass[i2]")
    no = round((T - to) * FPS)
    fc.append(f"[5]loop=loop={no}:size=1:start=0,setpts=N/{FPS}/TB,format=rgba,fade=t=in:st=0:d=0.5:alpha=1,setpts=PTS+{to:.3f}/TB[oc]")
    fc.append(f"[i2][oc]overlay=0:0:eof_action=pass[o1]")
    fc.append(f"[o1]ass={wd}/subs.ass:fontsdir={cfg.FONT_DIR},fade=t=in:st=0:d=0.4,fade=t=out:st={T - 0.6:.3f}:d=0.6,format=yuv420p[vout]")
    open(f"{wd}/fc.txt", 'w').write(';\n'.join(fc))
    cmd = (f"ffmpeg -y -v error -stats -progress {wd}/progress.txt " + ' '.join(inputs) + f" -i {audio} -filter_complex_script {wd}/fc.txt "
           f"-map [vout] -map {6 + len(co)}:a -c:v libx264 -preset veryfast -crf {crf} -pix_fmt yuv420p -r {FPS} -frames:v {NF} "
           f"-c:a aac -b:a {cfg.B['video']['audio_bitrate']} -ar 48000 -movflags +faststart -t {T:.3f} {out}")
    return cmd

def chapters(v, scenes):
    chs = [(0.0, scenes[0].get('ch', 'Intro'))]
    for sc in scenes[1:]:
        if sc['outro']:
            chs.append((sc['start'], v.get('outro_ch', cfg.PRODUCT.get('outro_chapter', 'Contact')))); continue
        if sc.get('ch'): chs.append((sc['start'], sc['ch']))
    # enforce >=10 s spacing
    out = [chs[0]]
    for t, l in chs[1:]:
        if t - out[-1][0] >= 10: out.append((t, l))
    return out

def shot_still(sid, t, path):
    """one cleaned frame of a catalogued shot (crop + blur + zoom), portrait/medium kinds"""
    from PIL import ImageFilter
    sh = SHOTS[sid]
    cw, ch = sh.get('cw'), sh.get('ch')
    if not cw: cw, ch = KIND.get(sh['kind'], (960, 400))
    y0 = sh.get('y0', 50)
    run(f"ffmpeg -v error -y -ss {sh['a'] + t} -i {SRC}{sh['src']}.mp4 -frames:v 1 -vf crop={cw}:{ch}:{sh.get('x0', 0)}:{y0} -update 1 {path}")
    im = Image.open(path).convert('RGB')
    for bx in sh.get('blur', []):
        x, y, w, h = bx[:4]; sg = bx[4] if len(bx) > 4 else 16
        im.paste(im.crop((x, y, x + w, y + h)).filter(ImageFilter.GaussianBlur(sg)), (x, y))
    if sh.get('zoom'):
        zx, zy, zw = sh['zoom']; zh = int(zw * ch / cw)
        im = im.crop((zx, zy, zx + zw, zy + zh)).resize((cw, ch), Image.LANCZOS)
    im.save(path)
    return path

def prep(v, S, tag):
    gfx.set_layout(bool(v.get('mirror')))
    wd = f"{cfg.BUILD}/{v['slug']}/{tag}"; os.makedirs(wd, exist_ok=True)
    scenes, T = plan(v)
    T = fr(T)
    window, items = render_window(v, scenes, S, tag)
    audio = build_audio(v, scenes, T, wd)
    cl = cues(scenes)
    write_subs(cl, f"{wd}/subs.srt", f"{wd}/subs.ass", bool(v.get('mirror')))
    json.dump(dict(T=T, scenes=scenes, chapters=chapters(v, scenes)), open(f"{wd}/plan.json", 'w'), indent=1)
    return scenes, T, window, audio

if __name__ == '__main__':
    slug, tag = sys.argv[1], sys.argv[2]   # tag: prev | 4k
    S = 0.25 if tag == 'prev' else 1.0
    v = [x for x in VIDEOS if x['slug'] == slug][0]
    scenes, T, window, audio = prep(v, S, tag)
    wd = f"{cfg.BUILD}/{v['slug']}/{tag}"
    out = f"{wd}/out.mp4"
    cmd = compose_cmd(v, scenes, T, S, tag, window, audio, out, crf=23 if tag == 'prev' else 20)
    tmp = f"/tmp/smv_{v['slug']}_{tag}.mp4"
    cmd = cmd.replace(f" {out}", f" {tmp}")
    open(f"{wd}/compose.sh", 'w').write(f"rm -f {wd}/done.txt\n" + cmd + f" && cp {tmp} {out} && rm -f {tmp} && echo DONE > {wd}/done.txt\n")
    print('T=', T, 'prepared; compose script', f"{wd}/compose.sh")
