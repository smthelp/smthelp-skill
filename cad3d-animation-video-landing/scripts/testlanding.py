# usage: PAGE=../deliverables/x.html SECTION=rack-3d TAB='.rs3d-tab' python testlanding.py  -> ../work/land*.png + console errors
import os,time
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
f=os.path.abspath(os.environ['PAGE']); sec=os.environ.get('SECTION','saf-3d'); tab=os.environ.get('TAB','.s3d-tab')
px=os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy'); proxy=None
if px:
    u=urlparse(px); proxy={'server':f'{u.scheme}://{u.hostname}:{u.port}'}
    if u.username: proxy.update(username=u.username,password=u.password or '')
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"],proxy=proxy)
    pg=b.new_context(viewport={'width':1360,'height':900},ignore_https_errors=True).new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append('PE '+str(e))); pg.on('console',lambda m: errs.append(m.text[:150]) if m.type=='error' else None)
    pg.goto('file://'+f,timeout=90000,wait_until='domcontentloaded'); time.sleep(3)
    pg.evaluate(f"document.getElementById('{sec}').scrollIntoView()"); time.sleep(12); pg.screenshot(path='../work/land1.png',timeout=120000)
    n=pg.evaluate(f"document.querySelectorAll('{tab}').length")
    for j,i in enumerate(range(1,n,2)):
        pg.evaluate(f"document.querySelectorAll('{tab}')[{i}].click()"); time.sleep(7); pg.screenshot(path=f'../work/land{j+2}.png',timeout=120000)
    print('page errors:',[e for e in errs if 'ERR_TUNNEL' not in e and '407' not in e and '400' not in e][:8]); b.close()
