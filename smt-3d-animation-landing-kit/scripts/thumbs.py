#!/usr/bin/env python3
"""YouTube thumbnail 1280x720 + 3840x2160 and Shorts cover 1080x1920 from build/thumb.html?f=h|v.  usage: thumbs.py <job.json>"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from common import load_job, W, launch_browser
from playwright.sync_api import sync_playwright
job = load_job(sys.argv[1]); s = job['slug']
with sync_playwright() as p:
    b = launch_browser(p)
    for f, vp, sc, out in [('h', (1280, 720), 1, f'youtube-thumbnail-{s}-1280x720'), ('h', (1280, 720), 3, f'youtube-thumbnail-{s}-3840x2160'), ('v', (1080, 1920), 1, f'shorts-cover-{s}-1080x1920')]:
        pg = b.new_page(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=sc)
        pg.goto('file://' + W(job, 'build', 'thumb.html') + '?f=' + f); pg.wait_for_timeout(900)
        png = f'/tmp/{out}.png'; pg.screenshot(path=png); pg.close()
        subprocess.run(['convert', png, '-quality', '90', W(job, 'out', out + '.jpg')], check=True); print(out + '.jpg')
    b.close()
