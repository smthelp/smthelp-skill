import os
PROJ=os.environ.get('PROJ', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
# resumable 4K frame renderer: python render.py l|p fps budget_seconds
import json,base64,time,sys,os
from playwright.sync_api import sync_playwright
B=os.path.join(PROJ,"build")+"/"
mode=sys.argv[1]; fps=int(sys.argv[2]); budget=float(sys.argv[3]); start=time.time()
portrait=mode=='p'; w,h=(2160,3840) if portrait else (3840,2160)
OUT=f"{PROJ}/frames_{mode}/"; os.makedirs(OUT,exist_ok=True)
vo=json.load(open(B+'audio/vo_timing.json')); model=open(B+'model.b64').read(); logo='data:image/png;base64,'+base64.b64encode(open(B+'logo.png','rb').read()).decode()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(); pg.goto('file://'+B+'video.html')
    info=pg.evaluate("c=>setupVideo(c)",{'portrait':portrait,'w':w,'h':h,'vo':vo,'model':model,'logo':logo,'r3':float(os.environ.get('R3','1.0'))})
    pg.evaluate("enableGLComposite()")
    N=int(info['total']*fps)
    json.dump({'N':N,'fps':fps,'total':info['total']},open(OUT+'meta.json','w'))
    done=0
    for i in range(N):
        fn=OUT+f"{i:05d}.jpg"
        if os.path.exists(fn): continue
        if time.time()-start>budget: break
        u=pg.evaluate("t=>renderAt(t,0.94)",i/fps)
        open(fn+'.tmp','wb').write(base64.b64decode(u.split(',')[1])); os.replace(fn+'.tmp',fn); done+=1
    b.close()
have=len([f for f in os.listdir(OUT) if f.endswith('.jpg')])
print(mode,'rendered',done,'have',have,'of',N,'elapsed',round(time.time()-start))
