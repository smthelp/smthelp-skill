import json,sys,base64,io
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
shots=json.loads(open(sys.argv[1]).read())
data=open('../work/world.json').read()
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--ignore-gpu-blocklist","--enable-unsafe-swiftshader"])
    pg=b.new_page(viewport={"width":1400,"height":1000})
    pg.set_content("<body style='margin:0'><script>"+open('ana.bundle.js').read()+"</script></body>")
    pg.evaluate("d=>run(JSON.parse(d))",data)
    for s in shots:
        u,lab=pg.evaluate("a=>shot(a.dir,a.c,a.h,a.o||{})",s)
        im=Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB'); d=ImageDraw.Draw(im)
        for id,x,y in lab: d.text((x,y),str(id),fill=(0,0,0)); 
        im.save('../work/'+s['name']+'.png')
    b.close()
