import json, subprocess, os, html
B = os.path.dirname(os.path.abspath(__file__)) + '/'
P = B + '../'
src = open(P + 'src/landing_how.html', encoding='utf-8').read()
subprocess.run([B + 'node_modules/.bin/esbuild', 'landing.js', '--bundle', '--format=iife', '--minify', '--outfile=landing.bundle.js', '--log-level=warning'], cwd=B, check=True)
bundle = open(B + 'landing.bundle.js').read()
model = open(B + 'model.b64').read()
e = html.escape
LABELS = {'top': 'Top stack light', 'led': 'LED for every slot', 'panel': 'End panel', 'barcode': 'Scan the manufacturer barcode', 'slot': 'Lit slot = put it here',
  'opA': 'Operator A', 'opB': 'Operator B', 'opC': 'Operator C', 'oldest': 'Oldest date code: pick first', 'rail': '10 rails', 'divider': 'Wire dividers · 24 mm pitch',
  'foot': 'Levelling feet', 'net': 'LAN / Wi-Fi to WMS'}
TABS = [('overview', 'Overview'), ('register', '1 · Register'), ('store', '2 · Store'), ('pick', '3 · Pick'), ('fifo', '4 · FIFO'), ('build', 'The rack'), ('connect', 'Connect')]
CAPS = {
 'overview': 'Five layers, one hundred slots per layer, and an LED for every slot. Drag to orbit, scroll to zoom, or let the tour run.',
 'register': 'Scan the manufacturer barcode at receiving. Part number, quantity and lot code are captured and the reel gets a unique ID for full traceability.',
 'store': 'Every empty slot lights up. Put the reel in any lit position; the placement is confirmed, the light goes out and inventory updates in real time.',
 'pick': 'The BOM comes in from your MES / ERP. Every reel the job needs lights up, in up to seven colour modes so several operators can kit at once.',
 'fifo': 'Date code and lot code are tracked per reel, so the oldest reel is the one that lights. Missing material is flagged before the line stops.',
 'build': 'Real CAD geometry: two end panels, ten rails and U-wire dividers on a 24 mm pitch, on four levelling feet. Slot widths adjust for 7, 13 and 15 inch reels.',
 'connect': 'Network cable or Wi-Fi (2.4 / 5 GHz) to the warehouse server, with SAP, Oracle and other ERP / MES links through an HTTP + JSON interface.',
}
FEATS = [(1, 'Register', 'One barcode scan captures part number, quantity and lot code, and assigns a unique ID.'),
 (2, 'Guided storing', 'Empty slots light up. Any lit slot will do, and the system remembers where it went.'),
 (3, 'Request & pick', 'BOM import from MES / ERP lights every reel the job needs. Seven colour modes for parallel kitting.'),
 (4, 'FIFO & shortage', 'Date code and lot code per reel: first in, first out happens on its own, and shortages are flagged early.'),
 (5, 'Simple rack', 'End panels, rails and wire dividers on a 24 mm pitch. Adjustable for 7, 13 and 15 inch reels.'),
 (6, 'Plugs into your systems', 'LAN or Wi-Fi, HTTP + JSON interface, SAP / Oracle and other ERP / MES integrations. 220 V, under 100 W.')]
SPECS = [('This model (CAD)', '5 layers · 100 slots per layer'), ('Divider pitch (CAD)', '24 mm'), ('Overall size (CAD)', '≈ 2470 × 400 × 1850 mm'),
 ('Reel sizes', '7 / 13 / 15 inch, adjustable'), ('Indicators', 'LED per slot · 7 colour modes · 2 top lights'), ('Power', '220 V (DC 12 V adapter) · < 100 W'),
 ('Network', 'Ethernet · Wi-Fi 2.4 / 5 GHz'), ('Integration', 'ERP / MES · HTTP + JSON · XML / CSV / Excel'), ('Larger models', '7-layer SIR7000B: 1624 reels, double-sided')]

css = """<style>
#rack-3d{--rb:#1C64F2;--rb2:#0E3A8F;--rteal:#00C2AD;--rcard:#fff;--rline:#e5e7eb;--rfg:#111827;--rfg2:#4b5563;--rfg3:#6b7280}
.dark #rack-3d{--rcard:#111827;--rline:#374151;--rfg:#f3f4f6;--rfg2:#cbd5e1;--rfg3:#9ca3af;--rb:#3b82f6}
#rack-3d{padding:88px 0;background:transparent}
#rack-3d .rs3d-wrap{max-width:1240px;margin:0 auto;padding:0 24px}
#rack-3d .rs3d-kick{display:inline-block;font:700 12px/1 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.12em;color:var(--rb);text-transform:uppercase;margin-bottom:12px}
#rack-3d h2{font-size:clamp(28px,3.4vw,40px);font-weight:800;line-height:1.15;color:var(--rfg);margin:0 0 12px}
#rack-3d .rs3d-lead{font-size:18px;color:var(--rfg2);max-width:780px;margin:0 0 30px}
#rack-3d .rs3d-grid{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:22px;align-items:stretch}
#rs3d-viewer{position:relative;height:clamp(380px,46vw,620px);border-radius:18px;overflow:hidden;border:1px solid var(--rline);box-shadow:0 20px 50px -20px rgba(2,6,23,.45);
  background:radial-gradient(ellipse at 55% 42%,#17305a 0%,#0B132B 50%,#050913 100%)}
#rs3d-viewer::before{content:'';position:absolute;inset:0;pointer-events:none;background-size:28px 28px;
  background-image:linear-gradient(to right,rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(to bottom,rgba(255,255,255,.035) 1px,transparent 1px)}
#rs3d-viewer canvas{position:absolute;inset:0;width:100%;height:100%;display:block;touch-action:none;cursor:grab}
#rs3d-viewer canvas:active{cursor:grabbing}
#rs3d-viewer [data-labels]{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.rs3d-label{position:absolute;left:0;top:0;transition:opacity .25s;opacity:0;will-change:transform}
.rs3d-label i{position:absolute;left:-6px;top:-6px;width:12px;height:12px;border-radius:99px;background:#00C2AD;box-shadow:0 0 0 4px rgba(0,194,173,.25),0 0 18px rgba(0,194,173,.8)}
.rs3d-label span{position:absolute;left:18px;top:-40px;white-space:nowrap;font:600 12px/1 Inter,sans-serif;color:#fff;background:rgba(7,13,30,.88);border:1px solid #00C2AD;border-left-width:4px;padding:7px 10px;border-radius:8px}
.rs3d-label.rs3d-left span{left:auto;right:18px;border-left-width:1px;border-right-width:4px}
.rs3d-sky i{background:#38BDF8}.rs3d-sky span{border-color:#38BDF8!important}.rs3d-red i{background:#ff4d3d}.rs3d-red span{border-color:#ff4d3d!important}
.rs3d-green i{background:#22c55e}.rs3d-green span{border-color:#22c55e!important}.rs3d-amber i{background:#f5b13d}.rs3d-amber span{border-color:#f5b13d!important}.rs3d-mag i{background:#e879f9}.rs3d-mag span{border-color:#e879f9!important}
.rs3d-hud{position:absolute;left:14px;right:14px;bottom:12px;display:flex;align-items:center;gap:10px}
.rs3d-hud .bar{flex:1;height:3px;background:rgba(255,255,255,.15);border-radius:3px;overflow:hidden}.rs3d-hud .bar b{display:block;height:100%;width:0;background:#00C2AD}
.rs3d-play{width:34px;height:34px;border-radius:99px;border:1px solid rgba(255,255,255,.3);background:rgba(7,13,30,.7);color:#fff;cursor:pointer;font-size:13px}
.rs3d-drag{position:absolute;top:12px;right:14px;font-size:11.5px;color:rgba(226,232,240,.75)}
.rs3d-panel{display:flex;flex-direction:column;gap:14px}
.rs3d-card{background:var(--rcard);border:1px solid var(--rline);border-radius:14px;padding:16px 20px}
.rs3d-tabs{display:flex;flex-wrap:wrap;gap:8px}
.rs3d-tab{padding:8px 13px;border-radius:10px;border:1px solid var(--rline);background:var(--rcard);color:var(--rfg2);font:600 13px Inter,sans-serif;cursor:pointer;transition:.15s}
.rs3d-tab:hover{border-color:var(--rb);color:var(--rb)}.rs3d-tab.on{background:var(--rb);border-color:var(--rb);color:#fff}
.rs3d-cap{min-height:88px;font-size:15px;line-height:1.55;color:var(--rfg2);margin:0}
.rs3d-ctl label{display:flex;align-items:center;gap:10px;font-size:14px;color:var(--rfg2);cursor:pointer}
.rs3d-ctl input{accent-color:var(--rb);width:17px;height:17px}
.rs3d-spec h3{font-size:15px;font-weight:700;color:var(--rfg);margin:0 0 6px}
.rs3d-spec div{display:flex;justify-content:space-between;gap:14px;padding:7px 0;border-bottom:1px solid var(--rline);font-size:13px}
.rs3d-spec div:last-child{border:0}.rs3d-spec dt{color:var(--rfg3)}.rs3d-spec dd{margin:0;font-weight:700;color:var(--rfg);text-align:right}
.rs3d-acts{display:flex;flex-wrap:wrap;gap:10px}
.rs3d-btn{display:inline-flex;align-items:center;padding:11px 18px;border-radius:10px;font-weight:700;font-size:14.5px;border:1px solid var(--rb);text-decoration:none}
.rs3d-btn.p{background:var(--rb);color:#fff}.rs3d-btn.p:hover{background:#0E3A8F}.rs3d-btn.s{color:var(--rb);background:transparent}.rs3d-btn.s:hover{background:var(--rb);color:#fff}
.rs3d-feats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:26px}
.rs3d-feat{text-align:left;cursor:pointer;font:inherit;color:inherit;background:var(--rcard);border:1px solid var(--rline);border-radius:14px;padding:18px 20px;transition:.15s}
.rs3d-feat:hover,.rs3d-feat.on{border-color:var(--rb);box-shadow:0 0 0 1px var(--rb)}
.rs3d-feat .n{font:700 12px 'JetBrains Mono',ui-monospace,monospace;color:var(--rb);letter-spacing:.08em}
.rs3d-feat h3{font-size:16px;font-weight:700;color:var(--rfg);margin:6px 0}.rs3d-feat p{font-size:14px;color:var(--rfg2);margin:0}
.rs3d-note{font-size:12.5px;color:var(--rfg3);margin-top:18px}
@media (max-width:960px){#rack-3d .rs3d-grid{grid-template-columns:1fr}#rs3d-viewer{height:min(80vw,470px)}.rs3d-feats{grid-template-columns:1fr}}
</style>
"""
tabs = ''.join(f'<button type="button" class="rs3d-tab" data-rs3d-step="{i}">{e(n)}</button>' for i, (k, n) in enumerate(TABS))
feats = ''.join(f'<button type="button" class="rs3d-feat" data-rs3d-step="{s}"><span class="n">0{j+1}</span><h3>{e(t)}</h3><p>{e(d)}</p></button>' for j, (s, t, d) in enumerate(FEATS))
specs = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in SPECS)
section = f'''
        <!-- ============ 3D VIEWER: SMT Intelligent Reel Storage Rack (real CAD) ============ -->
        <section id="rack-3d"><div class="rs3d-wrap">
          <span class="rs3d-kick">Interactive 3D · real CAD model</span>
          <h2>See the rack work, step by step</h2>
          <p class="rs3d-lead">Spin the 5-layer intelligent reel storage rack and watch the whole workflow: scan a reel, store it in a lit slot, pick a full BOM by light, and keep FIFO automatic.</p>
          <div class="rs3d-grid">
            <div id="rs3d-viewer" aria-label="SMT Intelligent Reel Storage Rack interactive 3D model"><canvas></canvas><div data-labels></div>
              <div class="rs3d-drag">Drag to orbit · scroll to zoom</div>
              <div class="rs3d-hud"><button type="button" class="rs3d-play" id="rs3d-play" aria-label="Play / pause">&#10074;&#10074;</button><div class="bar"><b id="rs3d-prog"></b></div></div>
            </div>
            <div class="rs3d-panel">
              <div class="rs3d-tabs" role="tablist">{tabs}</div>
              <div class="rs3d-card"><p class="rs3d-cap" id="rs3d-cap"></p></div>
              <div class="rs3d-card rs3d-ctl"><label><input type="checkbox" id="rs3d-lights" checked><span>Show empty-slot LEDs when exploring</span></label></div>
              <div class="rs3d-card rs3d-spec"><h3>Key specifications</h3><dl style="margin:0">{specs}</dl></div>
              <div class="rs3d-acts"><a class="rs3d-btn p" href="#contact">Get a configured quote</a><a class="rs3d-btn s" href="https://www.youtube.com/c/Smthelping" target="_blank" rel="noopener">Watch on YouTube</a></div>
            </div>
          </div>
          <div class="rs3d-feats">{feats}</div>
          <p class="rs3d-note">Rack geometry (end panels, rails, wire dividers, levelling feet and a 13-inch reel) comes from the real CAD model. Slot LEDs, glow, top stack lights, the PDA scanner and the stored reel fleet are illustrative, and highlight colours are not material colours. Capacities and electrical data from the SIR7000B / SIS7200A product sheets.</p>
        </div></section>
'''
ld = {"@context": "https://schema.org", "@type": "Product", "name": "SMT Intelligent Reel Storage Rack (5 layer)", "brand": {"@type": "Brand", "name": "Southern Machinery"},
      "manufacturer": {"@type": "Organization", "name": "Southern Machinery", "url": "https://www.smthelp.com"}, "category": "SMT material storage / smart reel rack",
      "description": "LED-guided SMT reel storage rack: barcode registration, guided storing, BOM picking by light with 7 colour modes, automatic FIFO and shortage alerts, ERP/MES integration via HTTP + JSON, Ethernet or Wi-Fi, 220 V under 100 W.",
      "image": ["https://ph.smthelp.com/images/2024/03/18/SMT-Intelligent-Reel-Storage-System-2024_07.jpg"],
      "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in SPECS]}
script = '''
<script type="application/ld+json">''' + json.dumps(ld, ensure_ascii=False) + '''</script>
<script type="text/plain" id="rs3d-model">''' + model + '''</script>
<script>''' + bundle + '''</script>
<script>
(function(){
  var LABELS=''' + json.dumps(LABELS) + ''', CAPS=''' + json.dumps(CAPS) + ''';
  var ids=''' + json.dumps([k for k, _ in TABS]) + ''';
  var viewer=null, cur=-1, host=document.getElementById("rs3d-viewer"), started=false;
  function setCap(i){ document.getElementById("rs3d-cap").textContent=CAPS[ids[i<0?0:i]]; }
  setCap(0);
  function start(){
    if(started) return; started=true;
    RACK3D.mountViewer({host:host, model:document.getElementById("rs3d-model").textContent, label:function(k){return LABELS[k]||k;}}).then(function(v){
      viewer=v; v.setLights(document.getElementById("rs3d-lights").checked);
      v.onChange(function(e){
        if(e.step!==cur){ cur=e.step; setCap(cur);
          document.querySelectorAll(".rs3d-tab").forEach(function(b){ b.classList.toggle("on", +b.getAttribute("data-rs3d-step")===cur); });
          document.querySelectorAll(".rs3d-feat").forEach(function(b){ b.classList.toggle("on", +b.getAttribute("data-rs3d-step")===cur); }); }
        document.getElementById("rs3d-prog").style.width=(100*e.t/e.total).toFixed(1)+"%";
        document.getElementById("rs3d-play").innerHTML=(e.playing&&!e.manual)?"&#10074;&#10074;":"&#9654;";
      });
    }).catch(function(err){ console.error(err); });
  }
  if("IntersectionObserver" in window){ new IntersectionObserver(function(es){ if(es[0].isIntersecting) start(); },{rootMargin:"300px"}).observe(host); } else start();
  document.querySelectorAll("[data-rs3d-step]").forEach(function(b){ b.addEventListener("click",function(){ start(); if(viewer) viewer.goTo(+b.getAttribute("data-rs3d-step"));
    if(b.classList.contains("rs3d-feat")) host.scrollIntoView({behavior:"smooth",block:"center"}); }); });
  document.getElementById("rs3d-play").addEventListener("click",function(){ if(viewer) viewer.toggle(); });
  document.getElementById("rs3d-lights").addEventListener("change",function(e){ if(viewer) viewer.setLights(e.target.checked); });
})();
</script>
'''
out = src
anchor = '        <!-- Workflow Section -->'
assert anchor in out
out = out.replace(anchor, section + '\n' + anchor, 1)
out = out.replace('</head>', css + '</head>', 1)
# hero button to the 3D section
hero_p = 'streamlined, automated process.</p>'
assert hero_p in out
out = out.replace(hero_p, hero_p + '\n                <a href="#rack-3d" class="inline-block mt-8 bg-primary text-white font-semibold py-3 px-6 rounded-lg hover:bg-secondary transition-colors">Explore the 3D rack</a>', 1)
out = out.replace('<title>How It Works: SMT Intelligent Reel Storage Rack | Southern Machinery</title>', '<title>How It Works: SMT Intelligent Reel Storage Rack (Interactive 3D) | Southern Machinery</title>', 1)
out = out.replace('content="How SMT Rack Works, SMT Automation,', 'content="How SMT Rack Works, SMT intelligent reel storage rack 3D, smart reel rack, LED reel shelf, SMT reel storage, FIFO reel management, SMT Automation,', 1)
out = out.replace('content="A step-by-step guide on how the SMT Intelligent Reel Storage Rack automates material handling for unparalleled efficiency and accuracy.">',
  'content="Interactive 3D, step by step: how the SMT Intelligent Reel Storage Rack registers, stores and picks reels by LED, keeps FIFO automatic and connects to your ERP / MES.">\n    <meta property="og:title" content="How the SMT Intelligent Reel Storage Rack Works (Interactive 3D)">\n    <meta property="og:type" content="product">\n    <meta property="og:image" content="https://ph.smthelp.com/images/2024/03/18/SMT-Intelligent-Reel-Storage-System-2024_07.jpg">', 1)
idx = out.rfind('</body>')
out = out[:idx] + script + out[idx:]
os.makedirs(P + 'deliverables', exist_ok=True)
fn = P + 'deliverables/how-smt-intelligent-reel-storage-rack-works-3d.html'
open(fn, 'w', encoding='utf-8').write(out)
print(fn, len(out))
