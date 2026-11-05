#!/usr/bin/env python3
"""Render the video stage to 4K H.264, one time segment per call (resumable).
usage: render.py <job.json> <169|916> <t0> <t1>      -> <work>/out/seg_<fmt>_<t0>.mp4 (+ .done marker)
The stage (build/video.html?fmt=..) must define window.READY and window.seek(t). CDP screenshots at
device scale 2 give native 3840x2160 / 2160x3840.  ~0.45 s/frame on 2 vCPU: keep each call < 20 min
(30 s segment = 900 frames ~ 7 min). Run ONE render at a time; two in parallel are not faster on 2 cores."""
import asyncio, sys, os, base64, subprocess, json, time
sys.path.insert(0, os.path.dirname(__file__))
from common import load_job, W, chromium_path
job = load_job(sys.argv[1]); fmt, t0, t1 = sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
cfg = job['_cfg']['video']; FPS = cfg['fps']; SC = cfg.get('scale', 2)
TL = json.load(open(W(job, 'video', 'timeline.json'))); t1 = min(t1, TL['total'])
out = W(job, 'out', f'seg_{fmt}_{sys.argv[3]}.mp4')
if os.path.exists(out + '.done'): print('skip (done)', out); sys.exit(0)
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        exe = chromium_path()
        b = await (p.chromium.launch(executable_path=exe, args=['--allow-file-access-from-files']) if exe else p.chromium.launch(args=['--allow-file-access-from-files']))
        vp = {'width': 1920, 'height': 1080} if fmt == '169' else {'width': 1080, 'height': 1920}
        pg = await b.new_page(viewport=vp, device_scale_factor=SC)
        await pg.goto('file://' + W(job, 'build', 'video.html') + '?fmt=' + fmt); await pg.wait_for_function('window.READY', timeout=60000)
        cdp = await pg.context.new_cdp_session(pg)
        tmp = '/tmp/' + os.path.basename(out)
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
        n = int(round((t1 - t0) * FPS)); st = time.time()
        for i in range(n):
            await pg.evaluate(f'seek({t0 + i / FPS:.4f})')
            r = await cdp.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 90, 'clip': {'x': 0, 'y': 0, 'width': vp['width'], 'height': vp['height'], 'scale': SC}})
            ff.stdin.write(base64.b64decode(r['data']))
            if i % 300 == 0: print(i, n, round(time.time() - st, 1), flush=True)
        ff.stdin.close(); ff.wait(); await b.close()
        subprocess.run(['cp', tmp, out], check=True); open(out + '.done', 'w').write(str(n))
        print('done', n, 'frames', round(time.time() - st, 1), 's ->', out)
asyncio.run(main())
