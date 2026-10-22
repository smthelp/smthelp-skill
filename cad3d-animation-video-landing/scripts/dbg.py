import os,sys,json,base64
from playwright.sync_api import sync_playwright
B=os.environ["PROJ"]+"/build/"; W=B+'../work/prev/'
vo=json.load(open(B+'audio/vo_timing.json')); model=open(B+'model.b64').read()
shots=json.loads(sys.argv[1])
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+B+'video.html')
    pg.evaluate("c=>setupVideo(c)",{'portrait':False,'w':960,'h':540,'vo':vo,'model':model,'logo':None})
    for i,s in enumerate(shots):
        u=pg.evaluate("o=>dbgShot(o)",s); open(W+f"dbg_{i}.jpg",'wb').write(base64.b64decode(u.split(',')[1]))
    print(errs); b.close()
