#!/usr/bin/env python3
"""Extract real tessellated geometry from a SolidWorks eDrawings / HOOPS Communicator HTML export.

usage: extract_mesh.py <drawing.html> <out_dir> [--wait 25]
outputs: out_dir/tree.json (assembly tree), out_dir/mesh.json (per body: path, column-major net matrix, positions, normals)

Technique credit: smthelp-skill/cad3d-animation-video-landing (v2.1.0) extract_mesh.py.
We wrap Communicator.WebViewer prototype methods to capture the live viewer, nudge the canvas, then call
model.getNodeMeshData() for every body node. Bodies that throw "no mesh data" (markups, empty bodies) are skipped.
"""
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(__file__))
from common import launch_browser

ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out'); ap.add_argument('--wait', type=int, default=25)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = launch_browser(p, gl=True)
    pg = b.new_page(viewport={'width': 1400, 'height': 900})
    pg.goto('file://' + os.path.abspath(a.src), timeout=180000)
    for _ in range(60):
        time.sleep(2)
        if pg.evaluate("typeof Communicator!=='undefined'"): break
    time.sleep(a.wait)
    pg.evaluate("""()=>{const W=Communicator.WebViewer; for(const n of Object.getOwnPropertyNames(W.prototype)){const f=W.prototype[n];
      if(typeof f==='function'&&n!=='constructor'){W.prototype[n]=function(...x){window.__hwv=this; return f.apply(this,x)}}}}""")
    pg.mouse.move(700, 400); pg.mouse.move(720, 420); pg.mouse.wheel(0, 10); time.sleep(2)
    if not pg.evaluate("!!window.__hwv"):
        sys.exit('could not capture the HOOPS WebViewer instance - use turntable mode (shot_views.py) instead')
    tree = pg.evaluate("""()=>{const m=__hwv.model; const out=[];
      (function walk(id,d){const ch=m.getNodeChildren(id); out.push({id,d,name:m.getNodeName(id),type:m.getNodeType(id),n:ch.length}); for(const c of ch) walk(c,d+1)})(m.getAbsoluteRootNode(),0);
      return out}""")
    json.dump(tree, open(os.path.join(a.out, 'tree.json'), 'w'), ensure_ascii=False)
    res = pg.evaluate("""async()=>{const m=__hwv.model; const out=[]; const bodies=[];
      (function walk(id,path){const ch=m.getNodeChildren(id); const nm=m.getNodeName(id); if(m.getNodeType(id)===3) bodies.push({id,path:path.concat([nm])}); for(const c of ch) walk(c,path.concat([nm]))})(m.getAbsoluteRootNode(),[]);
      for(const t of bodies){ let md; try{md=await m.getNodeMeshData(t.id)}catch(e){continue}
        const mat=m.getNodeNetMatrix(t.id).m; const pos=[];
        for(let i=0;i<md.faces.elementCount;i++){const it=md.faces.element(i).iterate(); while(!it.done()){const v=it.next(); pos.push(...v.position.map(x=>+x.toFixed(6)));}}
        let col=null; try{const c=await m.getNodesEffectiveFaceColor([t.id]); if(c&&c[0]) col=[c[0].r,c[0].g,c[0].b]}catch(e){}
        out.push({id:t.id,path:t.path,mat:Array.from(mat),pos,col});}
      return out}""")
    json.dump(res, open(os.path.join(a.out, 'mesh.json'), 'w'))
    print(f'{len(res)} bodies, {sum(len(r["pos"]) for r in res)//9} triangles -> {a.out}/mesh.json')
    b.close()
