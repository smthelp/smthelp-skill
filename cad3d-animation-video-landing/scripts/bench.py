import json,base64,time,sys,os
from playwright.sync_api import sync_playwright
B=os.path.dirname(os.path.abspath(__file__))+'/'
vo=json.load(open(B+'audio/vo_timing.json')); model=open(B+'model.b64').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(); pg.goto('file://'+B+'video.html'); pg.evaluate('window.R3D=%s;window.R3D_MSAA=%s'%(sys.argv[1],sys.argv[3]))
    pg.evaluate("c=>setupVideo(c)",{'portrait':False,'w':3840,'h':2160,'vo':vo,'model':model,'aa':sys.argv[4]=='1'})
    pg.evaluate("enableGLComposite()"); pg.evaluate("renderAt(8).length")
    for t in [4,30,60,100]:
        t0=time.time(); pg.evaluate("t=>renderAt(t,0.93).length",t); print(t, round(time.time()-t0,2))
    b.close()
