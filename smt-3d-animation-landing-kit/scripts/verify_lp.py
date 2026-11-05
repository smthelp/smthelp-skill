#!/usr/bin/env python3
"""Automated self-check of a built landing page (file:// or https://).

usage: verify_lp.py <page.html|url> [--job job.json] [--shots out_dir]
Checks (exit code 1 if any FAIL):
  load      no pageerror / console error, no broken <img>
  offline   no network request on load (file://) except data: URIs
  3d        viewer reaches data-smt3d=ready (WebGL via SwiftShader), material + light buttons switch
  i18n      every configured language switches <html lang>, RTL languages set dir=rtl
  blogs     article count == config.blog_count
  roi       ROI outputs are numeric after input
  duel      tabs exist and SVG panels rendered (if the page has a duel)
  mobile    390 px viewport has no horizontal overflow
Writes verify_report.json next to the screenshots.
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(__file__))
from common import launch_browser, SKILL, load_job
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser(); ap.add_argument('page'); ap.add_argument('--job'); ap.add_argument('--shots')
a = ap.parse_args()
cfg = load_job(a.job)['_cfg'] if a.job else json.load(open(os.path.join(SKILL, 'config', 'defaults.json')))
url = a.page if '://' in a.page else 'file://' + os.path.abspath(a.page)
shots = a.shots or (os.path.dirname(os.path.abspath(a.page)) if '://' not in a.page else '.')
os.makedirs(shots, exist_ok=True)
R = []
def check(name, ok, detail=''):
    R.append({'check': name, 'ok': bool(ok), 'detail': str(detail)[:300]}); print(('PASS ' if ok else 'FAIL ') + name, detail if not ok else '')

with sync_playwright() as p:
    b = launch_browser(p, gl=True)
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    errs, reqs = [], []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.on('request', lambda r: reqs.append(r.url) if not r.url.startswith(('data:', 'file:', 'blob:')) else None)
    pg.goto(url, timeout=120000, wait_until='load'); pg.wait_for_timeout(1500)
    pg.screenshot(path=os.path.join(shots, 'v_top.png'))
    broken = pg.evaluate("Array.from(document.images).filter(i=>i.getAttribute('src')&&i.complete&&i.naturalWidth===0).map(i=>i.alt||i.src.slice(0,60))")
    check('load: no broken images', not broken, broken)
    if url.startswith('file://'): check('offline: no network request on load', not reqs, reqs[:5])
    if pg.query_selector('#v3d'):
        pg.evaluate("document.getElementById('v3d').scrollIntoView()")
        try:
            pg.wait_for_function("['ready','error','nowebgl'].includes(document.getElementById('v3d').getAttribute('data-smt3d'))", timeout=60000)
        except Exception: pass
        st = pg.evaluate("document.getElementById('v3d').getAttribute('data-smt3d')")
        check('3d: viewer ready', st == 'ready', st)
        for attr in ['data-mat', 'data-light']:
            btns = pg.query_selector_all(f'[{attr}]')
            if btns: btns[-1].click(); pg.wait_for_timeout(300)
            check(f'3d: {attr} buttons switch', btns and btns[-1].get_attribute('aria-pressed') == 'true', len(btns))
        pg.fill('#v3dEx', '60'); pg.dispatch_event('#v3dEx', 'input'); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(shots, 'v_3d.png'))
    langs = cfg['languages']; bad = []
    for l in langs:
        pg.select_option('#lang', l); pg.wait_for_timeout(150)
        lang, d = pg.evaluate("[document.documentElement.lang, document.documentElement.dir]")
        if lang != l or (d == 'rtl') != (l in cfg['rtl_languages']): bad.append((l, lang, d))
        if l in ('zh', 'ar'): pg.screenshot(path=os.path.join(shots, f'v_lang_{l}.png'))
    check(f'i18n: {len(langs)} languages switch (rtl {cfg["rtl_languages"]})', not bad, bad)
    pg.select_option('#lang', cfg['default_language'])
    n = pg.evaluate("document.querySelectorAll('article.blog').length")
    check(f'blogs: {cfg["blog_count"]} articles', n == cfg['blog_count'], n)
    if pg.query_selector('#roi_hourly_cost'):
        pg.fill('#roi_investment', '20000'); pg.dispatch_event('#roi_investment', 'input')
        v = pg.evaluate("[document.getElementById('roiR_total').textContent, document.getElementById('roiR_payback').textContent]")
        check('roi: outputs numeric', any(ch.isdigit() for ch in v[0]) and any(ch.isdigit() for ch in v[1]), v)
    else:
        check('roi: module present', False, 'missing #roi_hourly_cost')
    if pg.query_selector('#duelRoot'):
        k = pg.evaluate("[document.querySelectorAll('#tabs .tab').length, document.querySelectorAll('#duelRoot svg').length]")
        check('duel: tabs + panels rendered', k[0] > 0 and k[1] >= 2, k)
        pg.evaluate("document.getElementById('duel').scrollIntoView()"); pg.wait_for_timeout(800); pg.screenshot(path=os.path.join(shots, 'v_duel.png'))
    check('load: no page/console errors', not errs, errs[:5])
    m = b.new_page(viewport={'width': 390, 'height': 844})
    m.goto(url, timeout=120000); m.wait_for_timeout(1200)
    ov = m.evaluate("document.documentElement.scrollWidth - window.innerWidth")
    check('mobile: no horizontal overflow', ov <= 2, ov)
    m.screenshot(path=os.path.join(shots, 'v_mobile.png'))
    b.close()
ok = all(r['ok'] for r in R)
json.dump({'page': url, 'ok': ok, 'results': R}, open(os.path.join(shots, 'verify_report.json'), 'w'), indent=1)
print('ALL PASS' if ok else 'SOME CHECKS FAILED'); sys.exit(0 if ok else 1)
