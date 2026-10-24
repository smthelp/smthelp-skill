"""English voice-over per sentence with edge-tts. Usage: python3 tts.py [slug ...]
Pronunciations = brand.json pronunciations + project.json pronunciations (regex -> spoken).
Run with proxy variables unset if edge-tts times out (env -u http_proxy -u https_proxy ...)."""
import asyncio, json, os, re, subprocess, sys
import edge_tts
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg
VIDEOS, OUTRO_TEXT = cfg.VIDEOS, cfg.OUTRO_TEXT
VOICE = cfg.B['voice']['name']
RATE = cfg.B['voice']['rate']
OUT = cfg.TTS
SUBS = [tuple(x) for x in cfg.P.get('pronunciations', [])] + [tuple(x) for x in cfg.B['pronunciations']]

def spoken(s):
    for a, b in SUBS:
        s = re.sub(a, b, s)
    return s

def sentences(text):
    return [x.strip() for x in re.split(r'(?<=[.?!])\s+(?=[A-Z"])', text.strip()) if x.strip()]

async def synth(text, path, sem):
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return
    async with sem:
        for attempt in range(4):
            try:
                c = edge_tts.Communicate(text, VOICE, rate=RATE)
                await c.save(path)
                if os.path.getsize(path) > 1000:
                    return
            except Exception as e:
                print('retry', path, e, file=sys.stderr)
                await asyncio.sleep(2)
        raise RuntimeError('tts failed ' + path)

def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).decode().strip())

async def main(only=None):
    sem = asyncio.Semaphore(6)
    jobs = []
    plan = {}
    for v in VIDEOS:
        if only and v['slug'] not in only:
            continue
        scenes = [dict(text=s['text']) for s in v['scenes']] + [dict(text=v.get('outro', OUTRO_TEXT), outro=True)]
        vp = []
        for si, s in enumerate(scenes):
            sl = []
            for ji, sent in enumerate(sentences(s['text'])):
                p = f"{OUT}/{v['slug']}_{si:02d}_{ji:02d}.mp3"
                jobs.append(synth(spoken(sent), p, sem))
                sl.append(dict(text=sent, spoken=spoken(sent), mp3=p))
            vp.append(sl)
        plan[v['slug']] = vp
    await asyncio.gather(*jobs)
    for slug, vp in plan.items():
        for sl in vp:
            for x in sl:
                x['dur'] = dur(x['mp3'])
        json.dump(vp, open(f'{OUT}/{slug}.json', 'w'), indent=1)
        print(slug, round(sum(x['dur'] for sl in vp for x in sl), 1), 's speech')

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:] or None))
