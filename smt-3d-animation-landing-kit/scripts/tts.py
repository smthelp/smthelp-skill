#!/usr/bin/env python3
"""Narration -> per-scene MP3 + word timings (edge-tts).  usage: tts.py <job.json>
Reads job.video.script (list of {id,text}); writes <work>/video/vo_<id>.mp3 and timing.json.
Sequential with retries (parallel requests get 'No audio was received'). Patches aiohttp for authenticated HTTPS proxies."""
import os, sys, json, asyncio, subprocess, urllib.parse, base64
sys.path.insert(0, os.path.dirname(__file__))
from common import load_job, W
job = load_job(sys.argv[1]); cfg = job['_cfg']['video']; P = job['_P']
px = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or os.environ.get('HTTP_PROXY')
import aiohttp
if px and '@' in px:
    u = urllib.parse.urlsplit(px); PROXY = f'{u.scheme}://{u.hostname}:{u.port}'
    cred = base64.b64encode(f'{urllib.parse.unquote(u.username)}:{urllib.parse.unquote(u.password)}'.encode()).decode()
    for name in ('ws_connect', '_request'):
        orig = getattr(aiohttp.ClientSession, name)
        def wrap(self, *a, _o=orig, **k):
            k['proxy'] = PROXY; k['proxy_headers'] = {'Proxy-Authorization': 'Basic ' + cred}; return _o(self, *a, **k)
        setattr(aiohttp.ClientSession, name, wrap)
import edge_tts
S = json.load(open(P(job['video']['script']), encoding='utf8')); OUT = W(job, 'video')
async def one(s):
    c = edge_tts.Communicate(s['text'], cfg['voice'], rate=cfg.get('rate', '+0%'), boundary='WordBoundary'); words = []
    fn = os.path.join(OUT, f"vo_{s['id']}.mp3")
    with open(fn, 'wb') as f:
        async for ch in c.stream():
            if ch['type'] == 'audio': f.write(ch['data'])
            elif ch['type'] == 'WordBoundary': words.append([ch['offset'] / 1e7, (ch['offset'] + ch['duration']) / 1e7, ch['text']])
    s['dur'] = float(subprocess.check_output(['ffprobe', '-v', '0', '-show_entries', 'format=duration', '-of', 'csv=p=0', fn])); s['words'] = words
    s['audio'] = fn
async def main():
    for s in S:
        for k in range(6):
            try: await one(s); break
            except Exception as e: print('retry', s['id'], e); await asyncio.sleep(2 + 2 * k)
        else: sys.exit('TTS failed for ' + s['id'])
    json.dump(S, open(os.path.join(OUT, 'timing.json'), 'w'), indent=0)
    tot = sum(s['dur'] for s in S); print([(s['id'], round(s['dur'], 1)) for s in S], round(tot, 1), 's of narration')
    lo, hi = cfg['target_duration_s']
    if not lo - 15 <= tot <= hi - 10: print(f'WARN narration {tot:.0f}s outside target {lo}-{hi}s')
asyncio.run(main())
