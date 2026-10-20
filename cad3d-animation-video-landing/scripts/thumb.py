import os
import json,base64,sys
from playwright.sync_api import sync_playwright
from PIL import Image; import io
PROJ=os.environ.get('PROJ', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
B=os.path.join(PROJ,"build")+"/"
vo=json.load(open(B+'audio/vo_timing.json')); model=open(B+'model.b64').read(); logo='data:image/png;base64,'+base64.b64encode(open(B+'logo.png','rb').read()).decode()
opt=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(); pg.goto('file://'+B+'video.html')
    pg.evaluate("c=>setupVideo(c)",{'portrait':False,'w':3840,'h':2160,'vo':vo,'model':model,'logo':logo})
    u=pg.evaluate("o=>renderThumb(o)",opt)
    im=Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB')
    im.save(B+'../deliverables/CN-SM-2713_thumbnail_4K.png')
    im.resize((1280,720),Image.LANCZOS).save(B+'../deliverables/CN-SM-2713_YouTube_thumbnail_1280x720.jpg',quality=92)
    b.close()
