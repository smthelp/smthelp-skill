import os,sys,json,base64,time
from playwright.sync_api import sync_playwright
PROJ=os.environ.get('PROJ', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
B=os.path.join(PROJ,"build")+"/"; W=B+"../work/prev/"
import os; os.makedirs(W,exist_ok=True)
portrait=sys.argv[1]=='p'; times=[float(x) for x in sys.argv[2].split(',')]; scale=float(sys.argv[3]) if len(sys.argv)>3 else 0.5
w,h=(1080,1920) if portrait else (1920,1080); w=int(w*scale*2); h=int(h*scale*2)
vo=json.load(open(B+'audio/vo_timing.json')); model=open(B+'model.b64').read(); logo='data:image/png;base64,'+base64.b64encode(open(B+'logo.png','rb').read()).decode()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto('file://'+B+'video.html')
    info=pg.evaluate("c=>setupVideo(c)",{'portrait':portrait,'w':w,'h':h,'vo':vo,'model':model,'logo':logo})
    json.dump(info,open(B+('timeline_p.json' if portrait else 'timeline_l.json'),'w'),indent=1)
    print('total',info['total']); 
    for s in info['scenes']: print(s)
    for t in times:
        t0=time.time(); u=pg.evaluate("t=>renderAt(t,0.9)",t)
        open(W+f"{'p' if portrait else 'l'}_{t:06.2f}.jpg",'wb').write(base64.b64decode(u.split(',')[1])); print(t,round(time.time()-t0,2))
    print(errs[:5]); b.close()
