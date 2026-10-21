import json, subprocess, os, html
B = os.path.dirname(os.path.abspath(__file__)) + '/'
P = B + '../'
src = open(P + 'src/landing.html', encoding='utf-8').read()
I = json.load(open(B + 's3d_i18n.json', encoding='utf-8'))
E = I['en']
subprocess.run([B + 'node_modules/.bin/esbuild', 'landing.js', '--bundle', '--format=iife', '--minify', '--outfile=landing.bundle.js', '--log-level=warning'], cwd=B, check=True)
bundle = open(B + 'landing.bundle.js').read()
model = open(B + 'model.b64').read()
t = lambda k: html.escape(E[k])

css = """<style>
#sbf-3d .s3d-grid{display:grid;grid-template-columns:minmax(0,1.65fr) minmax(0,1fr);gap:22px;align-items:stretch}
#s3d-viewer{position:relative;height:clamp(360px,46vw,600px);border-radius:var(--radius);overflow:hidden;border:1px solid var(--line);box-shadow:var(--shadow2);
  background:radial-gradient(ellipse at 55% 42%,#17305a 0%,#0B132B 50%,#050913 100%)}
#s3d-viewer::before{content:'';position:absolute;inset:0;pointer-events:none;background-size:28px 28px;
  background-image:linear-gradient(to right,rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(to bottom,rgba(255,255,255,.035) 1px,transparent 1px)}
#s3d-viewer canvas{position:absolute;inset:0;width:100%;height:100%;display:block;touch-action:none;cursor:grab}
#s3d-viewer canvas:active{cursor:grabbing}
#s3d-viewer [data-labels]{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.s3d-label{position:absolute;left:0;top:0;transition:opacity .25s;opacity:0;will-change:transform}
.s3d-label i{position:absolute;left:-6px;top:-6px;width:12px;height:12px;border-radius:99px;background:#00C2AD;box-shadow:0 0 0 4px rgba(0,194,173,.25),0 0 18px rgba(0,194,173,.8)}
.s3d-label span{position:absolute;left:18px;top:-40px;white-space:nowrap;font:600 12px/1 Inter,sans-serif;color:#fff;background:rgba(7,13,30,.88);border:1px solid #00C2AD;border-left-width:4px;padding:7px 10px;border-radius:8px}
.s3d-label.s3d-left span{left:auto;right:18px;border-left-width:1px;border-right-width:4px}
.s3d-label.s3d-sky i{background:#38BDF8;box-shadow:0 0 0 4px rgba(56,189,248,.25),0 0 18px rgba(56,189,248,.8)}.s3d-label.s3d-sky span{border-color:#38BDF8}
.s3d-label.s3d-red i{background:#ff4d3d;box-shadow:0 0 0 4px rgba(255,77,61,.25),0 0 18px rgba(255,77,61,.8)}.s3d-label.s3d-red span{border-color:#ff4d3d}
.s3d-hud{position:absolute;left:14px;right:14px;bottom:12px;display:flex;align-items:center;gap:10px;color:#e2e8f0;font-size:12px}
.s3d-hud .bar{flex:1;height:3px;background:rgba(255,255,255,.15);border-radius:3px;overflow:hidden}.s3d-hud .bar b{display:block;height:100%;width:0;background:#00C2AD}
.s3d-play{width:34px;height:34px;border-radius:99px;border:1px solid rgba(255,255,255,.3);background:rgba(7,13,30,.7);color:#fff;cursor:pointer;font-size:13px}
.s3d-drag{position:absolute;top:12px;right:14px;font-size:11.5px;color:rgba(226,232,240,.7)}
.s3d-panel{display:flex;flex-direction:column;gap:14px}
.s3d-tabs{display:flex;flex-wrap:wrap;gap:8px}
.s3d-tab{padding:8px 13px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--fg2);font:600 13px Inter,sans-serif;cursor:pointer;transition:.15s}
.s3d-tab:hover{border-color:var(--brand);color:var(--brand)}.s3d-tab.on{background:var(--brand);border-color:var(--brand);color:#fff}
html[data-theme="dark"] .s3d-tab.on{color:#04110f}
.s3d-cap{min-height:96px;font-size:15px;color:var(--fg2)}
.s3d-ctl{display:flex;flex-direction:column;gap:12px}
.s3d-ctl label{display:flex;align-items:center;gap:10px;font-size:13.5px;color:var(--fg2)}
.s3d-ctl input[type=range]{flex:1;accent-color:var(--brand)}
.s3d-ctl input[type=checkbox]{accent-color:var(--brand);width:17px;height:17px}
.s3d-spec dl{margin:0}.s3d-spec div{display:flex;justify-content:space-between;gap:14px;padding:8px 0;border-bottom:1px solid var(--line);font-size:13.5px}
.s3d-spec div:last-child{border:0}.s3d-spec dt{color:var(--fg3)}.s3d-spec dd{margin:0;font-weight:700;color:var(--fg);text-align:end}
.s3d-feats{margin-top:22px;align-items:stretch}.s3d-feat{text-align:start;cursor:pointer;font:inherit;color:inherit;width:100%;display:flex;flex-direction:column;justify-content:flex-start;align-items:flex-start}
.s3d-feat.on{border-color:var(--brand);box-shadow:0 0 0 1px var(--brand),var(--shadow2)}
.s3d-feat .n{font:700 12px "JetBrains Mono",monospace;color:var(--gold2);letter-spacing:.08em}
.s3d-feat h3{font-size:16px;margin:6px 0 6px}.s3d-feat p{font-size:14px;color:var(--fg2);margin:0}
.s3d-btn2{background:transparent;color:var(--brand);border-color:var(--brand)}.s3d-btn2:hover{background:var(--brand);color:#fff;text-decoration:none}
.s3d-note{font-size:12.5px;color:var(--fg3);margin-top:16px}
.s3d-acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
[dir=rtl] #s3d-viewer,[dir=rtl] #s3d-viewer *{direction:ltr}
@media (max-width:900px){#sbf-3d .s3d-grid{grid-template-columns:1fr}#s3d-viewer{height:min(78vw,460px)}#sbf-3d .s3d-feats{grid-template-columns:1fr}}
</style>
"""
tabs_ids = ['overview', 'drive', 'sort', 'rail', 'pick', 'platform', 'explode']
tabs = ''.join(f'<button type="button" class="s3d-tab" data-s3d-step="{i}" data-i18n="s3d_tab_{k}">{t("s3d_tab_" + k)}</button>' for i, k in enumerate(tabs_ids))
feat_step = [1, 2, 3, 4, 5, 0]
feats = ''.join(f'''<button type="button" class="card s3d-feat" data-s3d-step="{feat_step[i]}"><span class="n">0{i+1}</span><h3 data-i18n="s3d_f{i+1}_t">{t(f"s3d_f{i+1}_t")}</h3><p data-i18n="s3d_f{i+1}_d">{t(f"s3d_f{i+1}_d")}</p></button>''' for i in range(6))
specs = ''.join(f'<div><dt data-i18n="s3d_s{i}_k">{t(f"s3d_s{i}_k")}</dt><dd data-i18n="s3d_s{i}_v">{t(f"s3d_s{i}_v")}</dd></div>' for i in range(1, 7))

section = f'''
<!-- ============ 3D MECHANISM VIEWER (SBF1001 CAD) ============ -->
<section id="sbf-3d"><div class="wrap">
<span class="kick" data-i18n="s3d_kick">{t("s3d_kick")}</span>
<h2 class="sec" data-i18n="s3d_h2">{t("s3d_h2")}</h2>
<p class="lead" data-i18n="s3d_lead">{t("s3d_lead")}</p>
<div class="s3d-grid">
 <div id="s3d-viewer" aria-label="SBF1001 interactive 3D model"><canvas></canvas><div data-labels></div>
  <div class="s3d-drag" data-i18n="s3d_ui_drag">{t("s3d_ui_drag")}</div>
  <div class="s3d-hud"><button type="button" class="s3d-play" id="s3d-play" aria-label="Play / pause">&#10074;&#10074;</button><div class="bar"><b id="s3d-prog"></b></div></div>
 </div>
 <div class="s3d-panel">
  <div class="s3d-tabs" role="tablist">{tabs}</div>
  <div class="card" style="padding:18px 20px"><p class="s3d-cap" id="s3d-cap" style="margin:0"></p></div>
  <div class="card s3d-ctl" style="padding:18px 20px">
   <label><span data-i18n="s3d_ui_rate">{t("s3d_ui_rate")}</span><input type="range" id="s3d-rate" min="0.2" max="2" step="0.05" value="1"></label>
   <label><input type="checkbox" id="s3d-xray"><span data-i18n="s3d_ui_xray">{t("s3d_ui_xray")}</span></label>
  </div>
  <div class="card s3d-spec" style="padding:16px 20px"><h3 style="font-size:15px;margin-bottom:6px" data-i18n="s3d_specs_h">{t("s3d_specs_h")}</h3><dl>{specs}</dl></div>
  <div class="s3d-acts"><a class="btn btn-p" href="#contact" data-i18n="s3d_cta1">{t("s3d_cta1")}</a><a class="btn s3d-btn2" href="https://www.youtube.com/c/Smthelping" target="_blank" rel="noopener" data-i18n="s3d_cta2">{t("s3d_cta2")}</a></div>
 </div>
</div>
<h3 style="margin-top:30px;font-size:19px" data-i18n="s3d_feat_h">{t("s3d_feat_h")}</h3>
<div class="grid g3 s3d-feats">{feats}</div>
<p class="s3d-note" data-i18n="s3d_note">{t("s3d_note")}</p>
</div></section>
'''

script = '''
<script type="text/plain" id="s3d-model">''' + model + '''</script>
<script>''' + bundle + '''</script>
<script>
(function(){
  var S3D_I18N = ''' + json.dumps(I, ensure_ascii=False) + ''';
  Object.keys(S3D_I18N).forEach(function(l){ if(!I18N[l]) I18N[l]={}; Object.assign(I18N[l], S3D_I18N[l]); });
  var ids=["overview","drive","sort","rail","pick","platform","explode"];
  function lang(){ return document.documentElement.getAttribute("lang")||"en"; }
  function tr(k){ return T(lang(),k); }
  var viewer=null, cur=-1;
  function setCap(i){ var c=document.getElementById("s3d-cap"); if(c&&i>=0) c.textContent=tr("s3d_cap_"+ids[i]); }
  var _al=applyLang; applyLang=function(l,p){ _al(l,p); setCap(cur<0?0:cur); };
  document.querySelectorAll("[data-i18n^=s3d_]").forEach(function(el){ el.textContent=tr(el.getAttribute("data-i18n")); });
  setCap(0);
  var host=document.getElementById("s3d-viewer"); var started=false;
  function start(){
    if(started) return; started=true;
    SBF3D.mountViewer({host:host, model:document.getElementById("s3d-model").textContent, label:tr}).then(function(v){
      viewer=v;
      v.onChange(function(e){
        if(e.step!==cur){ cur=e.step; setCap(cur);
          document.querySelectorAll(".s3d-tab").forEach(function(b){ b.classList.toggle("on", +b.getAttribute("data-s3d-step")===cur); });
          document.querySelectorAll(".s3d-feat").forEach(function(b){ b.classList.toggle("on", +b.getAttribute("data-s3d-step")===cur); }); }
        document.getElementById("s3d-prog").style.width=(100*e.t/e.total).toFixed(1)+"%";
        document.getElementById("s3d-play").innerHTML=(e.playing&&!e.manual)?"&#10074;&#10074;":"&#9654;";
      });
    }).catch(function(err){ console.error(err); });
  }
  if("IntersectionObserver" in window){ new IntersectionObserver(function(es){ if(es[0].isIntersecting) start(); },{rootMargin:"300px"}).observe(host); } else start();
  document.querySelectorAll("[data-s3d-step]").forEach(function(b){ b.addEventListener("click",function(){ start(); if(viewer) viewer.goTo(+b.getAttribute("data-s3d-step"));
    if(b.classList.contains("s3d-feat")) host.scrollIntoView({behavior:"smooth",block:"center"}); }); });
  document.getElementById("s3d-play").addEventListener("click",function(){ if(viewer) viewer.toggle(); });
  document.getElementById("s3d-rate").addEventListener("input",function(e){ if(viewer) viewer.setRate(+e.target.value); });
  document.getElementById("s3d-xray").addEventListener("change",function(e){ if(viewer) viewer.setGhost(e.target.checked); });
})();
</script>
'''

out = src
anchor = '<section id="machine">'
assert anchor in out
out = out.replace(anchor, section + anchor, 1)
out = out.replace('</head>', css + '</head>', 1)
hero_btn = '<a class="btn btn-s" href="#machine" data-i18n="hero_cta2">Read the full specification</a>'
assert hero_btn in out
out = out.replace(hero_btn, hero_btn + '\n<a class="btn btn-s" href="#sbf-3d" data-i18n="s3d_hero">' + t('s3d_hero') + '</a>', 1)
# keyword meta enrichment
out = out.replace('content="bowl feeder, vibratory bowl feeder, SBF1001,', 'content="bowl feeder, vibratory bowl feeder, SBF1001, bowl feeder 3D model, how a vibratory bowl feeder works,', 1)
idx = out.rfind('</body>')
out = out[:idx] + script + out[idx:]
os.makedirs(P + 'deliverables', exist_ok=True)
fn = P + 'deliverables/sbf1001-vibratory-bowl-feeder-odd-form-auto-insertion-smart-ems-3d.html'
open(fn, 'w', encoding='utf-8').write(out)
print(fn, len(out))
