#!/usr/bin/env python3
"""Browser test with Playwright (headless Chromium, SwiftShader WebGL).
usage: python3 render_test.py <page.html> [--modes N] [--out /tmp/rt]
Checks: no page JS errors; every mode chip switches; material/light buttons cycle when present; zh, ar (dir=rtl) and
390 px mobile have no horizontal overflow. Screenshots go to --out for a visual look (always look at them).
Setup (sandbox): pip install playwright; PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright python3 -m playwright install chromium-headless-shell;
sudo apt-get install -y libatk1.0-0t64 libxcomposite1 libxdamage1 libatspi2.0-0t64. A proxy in PROXY / HTTPS_PROXY env (http://user:pass@host:port) is used automatically."""
import sys, os, asyncio
from playwright.async_api import async_playwright
F = 'file://' + os.path.abspath(sys.argv[1]); N = int(sys.argv[sys.argv.index('--modes') + 1]) if '--modes' in sys.argv else 0
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/tmp/rt'; os.makedirs(OUT, exist_ok=True)
import urllib.parse
def _proxy():
    for k in ('PROXY', 'HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy', 'ALL_PROXY'):
        v = os.environ.get(k)
        if v:
            u = urllib.parse.urlparse(v); d = {'server': f'{u.scheme}://{u.hostname}:{u.port}'}
            if u.username: d['username'] = urllib.parse.unquote(u.username); d['password'] = urllib.parse.unquote(u.password or '')
            return d
PX = _proxy()   # CDN (three.js, fonts) must be reachable or the 3D falls back to the hero image
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(proxy=PX, args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        errs = []
        pg = await b.new_page(viewport={'width': 1366, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        await pg.goto(F, wait_until='domcontentloaded', timeout=60000); await pg.wait_for_timeout(5000)
        await pg.screenshot(path=f'{OUT}/top.png')
        await pg.evaluate('document.getElementById("line3d").scrollIntoView()'); await pg.wait_for_timeout(4000)
        n = N or await pg.evaluate('document.querySelectorAll("#chips .chip").length')
        for i in range(1, n + 1):
            await pg.click(f'#chips .chip:nth-child({i})'); await pg.wait_for_timeout(2500); await pg.screenshot(path=f'{OUT}/mode{i}.png')
        for bid in ('bMat', 'bLight'):
            if not await pg.evaluate(f'document.getElementById("{bid}").hidden'):
                await pg.click('#' + bid); print(bid, await pg.evaluate(f'document.getElementById("{bid}").textContent'))
        await pg.close()
        for q, name, w in [('?lang=zh', 'zh', 1366), ('?lang=ar', 'ar', 1366), ('', 'mobile', 390)]:
            pg = await b.new_page(viewport={'width': w, 'height': 844}); pg.on('pageerror', lambda e: errs.append(name + ':' + str(e)[:200]))
            await pg.goto(F + q, wait_until='domcontentloaded', timeout=60000); await pg.wait_for_timeout(4000)
            sw, iw, d = await pg.evaluate('[document.documentElement.scrollWidth,innerWidth,document.documentElement.dir]')
            await pg.screenshot(path=f'{OUT}/{name}.png'); print(name, 'overflow' if sw > iw else 'ok', d); await pg.close()
        await b.close(); print('page errors:', errs or 'none'); sys.exit(1 if errs else 0)
asyncio.run(main())
