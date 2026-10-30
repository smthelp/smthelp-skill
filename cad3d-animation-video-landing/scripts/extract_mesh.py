"""Extract real tessellated geometry from a SolidWorks eDrawings / HOOPS Communicator HTML export.

Usage (run with the env venv python, see setup_env.sh):
  PLAYWRIGHT_BROWSERS_PATH=$PROJ/env/browsers LD_LIBRARY_PATH=$PROJ/env/libs/usr/lib/aarch64-linux-gnu \
  $PROJ/env/venv/bin/python extract_mesh.py ../src/drawing.html ../src/
Outputs:
  tree.json  - assembly tree (id, depth, name, type, child count) -> read it to identify parts
  mesh.json  - per body node: path, net matrix (column-major, metres), triangle positions + normals
  shot_*.png - reference screenshots of the original viewer
How it works: the eDrawings page boots a HOOPS Communicator WebViewer. We wrap every
Communicator.WebViewer.prototype method to capture `this` (window.__hwv) on the next call,
nudge the canvas with mouse events, then read model.getNodeMeshData() for every body node.
Some bodies (markup arrows, empty product bodies) throw "Node has instance, but no mesh data" - skipped.
"""
import sys, json, time, os
from playwright.sync_api import sync_playwright

src = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(src)
ARGS = ["--use-gl=angle", "--use-angle=swiftshader", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader"]
with sync_playwright() as p:
    b = p.chromium.launch(args=ARGS)
    pg = b.new_page(viewport={"width": 1400, "height": 900})
    pg.goto("file://" + src)
    # wait for the model to load (WASM + decompression); large models need longer
    for _ in range(60):
        time.sleep(2)
        if pg.evaluate("typeof Communicator!=='undefined'"):
            break
    time.sleep(20)
    pg.screenshot(path=os.path.join(out, "shot_original.png"))
    pg.evaluate("""()=>{const W=Communicator.WebViewer; for(const n of Object.getOwnPropertyNames(W.prototype)){const f=W.prototype[n];
      if(typeof f==='function'&&n!=='constructor'){W.prototype[n]=function(...a){window.__hwv=this; return f.apply(this,a)}}}}""")
    pg.mouse.move(700, 400); pg.mouse.move(720, 420); pg.mouse.wheel(0, 10); time.sleep(2)
    assert pg.evaluate("!!window.__hwv"), "could not capture the HOOPS WebViewer instance"
    tree = pg.evaluate("""()=>{const m=__hwv.model; const out=[];
      (function walk(id,d){const ch=m.getNodeChildren(id); out.push({id,d,name:m.getNodeName(id),type:m.getNodeType(id),n:ch.length}); for(const c of ch) walk(c,d+1)})(m.getAbsoluteRootNode(),0);
      return out}""")
    json.dump(tree, open(os.path.join(out, "tree.json"), "w"), indent=0, ensure_ascii=False)
    res = pg.evaluate("""async()=>{const m=__hwv.model; const out=[]; const bodies=[];
      (function walk(id,path){const ch=m.getNodeChildren(id); const nm=m.getNodeName(id); if(m.getNodeType(id)===3) bodies.push({id,path:path.concat([nm])}); for(const c of ch) walk(c,path.concat([nm]))})(m.getAbsoluteRootNode(),[]);
      for(const t of bodies){ let md; try{md=await m.getNodeMeshData(t.id)}catch(e){out.push({id:t.id,path:t.path,err:String(e)}); continue}
        const mat=m.getNodeNetMatrix(t.id).m; const pos=[],nor=[];
        for(let i=0;i<md.faces.elementCount;i++){const it=md.faces.element(i).iterate(); while(!it.done()){const v=it.next(); pos.push(...v.position.map(x=>+x.toFixed(6))); nor.push(...(v.normal||[0,0,0]).map(x=>+x.toFixed(3)));}}
        out.push({id:t.id,path:t.path,mat:Array.from(mat),pos,nor});}
      return out}""")
    json.dump(res, open(os.path.join(out, "mesh.json"), "w"))
    for r in res:
        print(r['id'], ' / '.join(r['path'][-3:]), r.get('err') or f"{len(r['pos'])//9} tris")
    b.close()
