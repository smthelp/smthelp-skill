import json, re, subprocess, os
B = os.path.dirname(os.path.abspath(__file__)) + '/'
P = B + '../'
src = open(P + 'src/landing.html', encoding='utf-8').read()
I = json.load(open(B + 'cn_i18n.json', encoding='utf-8'))
E = I['en']
subprocess.run(['npx', 'esbuild', 'landing.js', '--bundle', '--format=iife', '--minify', '--outfile=landing.bundle.js', '--log-level=warning'], cwd=B, check=True)
bundle = open(B + 'landing.bundle.js').read()
model = open(B + 'model.b64').read()

def t(k): return E[k]

css = """
  <style>
    #cn-viewer { position: relative; }
    #cn-viewer canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; touch-action: none; cursor: grab; }
    #cn-viewer canvas:active { cursor: grabbing; }
    .cn-stage-bg { background: radial-gradient(ellipse at 55% 42%, #17305a 0%, #0B132B 48%, #050913 100%); }
    .cn-stage-bg::before { content: ''; position: absolute; inset: 0; pointer-events: none;
      background-size: 28px 28px; background-image: linear-gradient(to right, rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.035) 1px, transparent 1px); }
    .cn-label { position: absolute; left: 0; top: 0; pointer-events: none; transition: opacity .25s; opacity: 0; will-change: transform; }
    .cn-label i { position: absolute; left: -6px; top: -6px; width: 12px; height: 12px; border-radius: 99px; background: #00C2AD; box-shadow: 0 0 0 4px rgba(0,194,173,.25), 0 0 18px rgba(0,194,173,.8); }
    .cn-label span { position: absolute; left: 18px; top: -40px; white-space: nowrap; font: 600 12px/1 Inter, sans-serif; color: #fff; background: rgba(7,13,30,.88);
      border: 1px solid #00C2AD; border-left-width: 4px; padding: 7px 10px; border-radius: 8px; }
    .cn-label span::before { content: ''; position: absolute; left: -22px; top: 100%; width: 22px; height: 1px; background: #00C2AD; transform-origin: right; transform: rotate(-58deg) translateY(4px); }
    .cn-label.cn-left span { left: auto; right: 18px; border-left-width: 1px; border-right-width: 4px; }
    .cn-label.cn-left span::before { left: 100%; transform-origin: left; transform: rotate(58deg) translateY(4px); }
    .cn-label.cn-amber i { background: #F5B13D; box-shadow: 0 0 0 4px rgba(245,177,61,.25), 0 0 18px rgba(245,177,61,.8); }
    .cn-label.cn-amber span { border-color: #F5B13D; }
    .cn-label.cn-amber span::before { background: #F5B13D; }
    .cn-tab { white-space: nowrap; }
    .cn-tab.active { background: #00A896; color: #fff; border-color: #00A896; }
    .cn-feat.active { border-color: #00A896; box-shadow: 0 0 25px rgba(0,168,150,.22); }
    .cn-progress { transition: width .2s linear; }
    #cn-jaw { accent-color: #00A896; }
    [dir=rtl] #cn-viewer, [dir=rtl] #cn-viewer * { direction: ltr; }
  </style>
"""

feat_icons = ['fa-plug', 'fa-gears', 'fa-crosshairs', 'fa-ruler-vertical', 'fa-arrows-down-to-line', 'fa-screwdriver-wrench']
feat_step = [1, 2, 3, 4, 4, 5]
feats = ''.join(f"""
            <button type="button" data-cn-step="{feat_step[i]}" class="cn-feat text-left p-4 rounded-xl bg-white dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 hover:border-brand-teal transition-all group">
              <div class="flex items-start gap-3">
                <div class="w-10 h-10 shrink-0 rounded-lg bg-brand-teal/10 text-brand-teal flex items-center justify-center group-hover:scale-110 transition-transform"><i class="fa-solid {feat_icons[i]}"></i></div>
                <div>
                  <h3 class="text-sm font-bold text-slate-900 dark:text-white mb-1" data-i18n="cn_f{i+1}_t">{t(f'cn_f{i+1}_t')}</h3>
                  <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed" data-i18n="cn_f{i+1}_d">{t(f'cn_f{i+1}_d')}</p>
                </div>
              </div>
            </button>""" for i in range(6))
tabs_ids = ['overview', 'shank', 'mech', 'grip', 'stop', 'explode', 'cycle']
tabs = ''.join(f"""<button type="button" data-cn-step="{i}" class="cn-tab px-3 py-1.5 rounded-lg text-xs font-semibold border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:text-brand-teal transition-all" data-i18n="cn_tab_{k}">{t('cn_tab_' + k)}</button>""" for i, k in enumerate(tabs_ids))
specs = ''.join(f"""
              <div class="flex items-start justify-between gap-4 py-2.5 border-b border-slate-100 dark:border-slate-800 last:border-0">
                <dt class="text-xs text-slate-500 dark:text-slate-400" data-i18n="cn_s{i}_k">{t(f'cn_s{i}_k')}</dt>
                <dd class="text-xs font-semibold text-slate-800 dark:text-slate-100 text-right" data-i18n="cn_s{i}_v">{t(f'cn_s{i}_v')}</dd>
              </div>""" for i in range(1, 7))

section = f"""
  <!-- SECTION: CN-SM-2713 INTERACTIVE 3D MECHANISM (real-time WebGL from production CAD) -->
  <section id="cn-sm-2713" class="py-16 sm:py-24 bg-slate-100 dark:bg-brand-dark border-b border-slate-200 dark:border-slate-800 transition-colors">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-3xl mx-auto space-y-4">
        <div class="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-brand-amber/10 border border-brand-amber/30 text-brand-amber text-xs font-semibold uppercase tracking-wider">
          <span class="w-2 h-2 rounded-full bg-brand-amber animate-pulse"></span><span data-i18n="cn_badge">{t('cn_badge')}</span>
        </div>
        <h2 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-slate-900 dark:text-white leading-tight" data-i18n="cn_title">{t('cn_title')}</h2>
        <p class="text-slate-600 dark:text-slate-400 text-sm sm:text-base leading-relaxed" data-i18n="cn_sub">{t('cn_sub')}</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-12 items-start">
        <!-- Viewer -->
        <div class="lg:col-span-8">
          <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-3 sm:p-4 shadow-xl">
            <div class="flex items-center justify-between pb-3">
              <div class="flex items-center space-x-2">
                <span class="w-3 h-3 rounded-full bg-red-400 inline-block"></span><span class="w-3 h-3 rounded-full bg-amber-400 inline-block"></span><span class="w-3 h-3 rounded-full bg-emerald-400 inline-block"></span>
                <span class="text-xs font-mono text-slate-500 dark:text-slate-400 pl-2">CN-SM-2713 · Gripper for coil Ø8.5</span>
              </div>
              <span class="text-[11px] font-mono bg-brand-teal/10 text-brand-teal px-2 py-0.5 rounded border border-brand-teal/20"><i class="fa-solid fa-cube mr-1"></i>Live 3D · CAD</span>
            </div>
            <div id="cn-viewer" class="cn-stage-bg relative rounded-xl overflow-hidden" style="height:clamp(400px,46vw,540px)">
              <canvas aria-label="Interactive 3D model of the CN-SM-2713 JUKI coil gripper nozzle"></canvas>
              <div data-labels class="absolute inset-0 pointer-events-none overflow-hidden"></div>
              <div id="cn-loading" class="absolute inset-0 flex items-center justify-center text-slate-300 text-xs font-mono"><i class="fa-solid fa-circle-notch fa-spin mr-2 text-brand-teal"></i>Loading 3D model…</div>
              <div class="absolute left-3 top-3 text-[11px] font-mono text-slate-300/80 pointer-events-none"><i class="fa-solid fa-hand-pointer mr-1"></i><span data-i18n="cn_drag">{t('cn_drag')}</span></div>
              <button id="cn-play" type="button" aria-label="Play or pause the tour" class="absolute right-3 top-3 w-9 h-9 rounded-lg bg-slate-900/70 border border-slate-600 text-white hover:border-brand-teal"><i class="fa-solid fa-pause"></i></button>
              <div class="absolute left-0 right-0 bottom-0 p-3 sm:p-4 bg-gradient-to-t from-black/80 to-transparent pointer-events-none">
                <p id="cn-caption" class="text-white text-xs sm:text-sm font-medium min-h-[2.5em]"></p>
                <div class="h-1 mt-2 rounded bg-white/10 overflow-hidden"><div id="cn-progress" class="cn-progress h-full bg-brand-teal" style="width:0%"></div></div>
              </div>
            </div>
            <div class="flex flex-wrap gap-2 pt-3">{tabs}</div>
            <div class="flex items-center gap-3 pt-3 border-t border-slate-100 dark:border-slate-800 mt-3">
              <label for="cn-jaw" class="text-xs font-semibold text-slate-600 dark:text-slate-300 whitespace-nowrap"><i class="fa-solid fa-hand-back-fist mr-1 text-brand-teal"></i><span data-i18n="cn_jaw">{t('cn_jaw')}</span></label>
              <input id="cn-jaw" type="range" min="0" max="100" value="0" class="w-full">
              <span id="cn-jaw-val" class="text-xs font-mono text-slate-500 w-10 text-right">0%</span>
            </div>
          </div>
        </div>
        <!-- Features & specs -->
        <div class="lg:col-span-4 space-y-3">
          {feats}
          <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-brand-teal mb-1" data-i18n="cn_spec_title">{t('cn_spec_title')}</h3>
            <dl>{specs}</dl>
          </div>
          <div class="flex flex-col sm:flex-row lg:flex-col gap-2 pt-1">
            <a href="#rfq" class="inline-flex items-center justify-center px-5 py-3 rounded-xl font-bold text-white bg-brand-teal hover:bg-brand-darkteal shadow-lg transition-all"><i class="fa-solid fa-paper-plane mr-2"></i><span data-i18n="cn_cta">{t('cn_cta')}</span></a>
            <a href="https://www.youtube.com/c/Smthelping" target="_blank" rel="noopener noreferrer" class="inline-flex items-center justify-center px-5 py-3 rounded-xl font-semibold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 hover:border-brand-teal transition-all"><i class="fa-brands fa-youtube mr-2 text-red-500"></i><span data-i18n="cn_cta2">{t('cn_cta2')}</span></a>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

ld = {
  "@context": "https://schema.org", "@type": "Product", "name": "CN-SM-2713 JUKI Coil Gripper Nozzle",
  "sku": "CN-SM-2713", "mpn": "CN-SM-2713", "category": "SMT / THT odd-form insertion gripper nozzle",
  "brand": {"@type": "Brand", "name": "Southern Machinery"},
  "manufacturer": {"@id": "https://www.smthelp.com/#organization"},
  "description": "Custom gripper nozzle for JUKI odd-form insertion machines, engineered for an Ø8.5 mm wire-wound coil: JUKI-standard nozzle shank, spring-closed toggle linkage with twin pivot jaws, 3-point self-centering contact pins and a center Z-datum stop pin.",
  "additionalProperty": [
    {"@type": "PropertyValue", "name": "Target component", "value": "Ø8.5 mm wire-wound coil, radial leads"},
    {"@type": "PropertyValue", "name": "Actuation", "value": "Plunger-driven toggle linkage, spring return"},
    {"@type": "PropertyValue", "name": "Contact", "value": "3 contact pins (2 + 1), self-centering"},
    {"@type": "PropertyValue", "name": "Parts", "value": "21"}
  ]
}

init_js = """
  <script type="text/plain" id="cn-model-data">""" + model + """</script>
  <script>""" + bundle + """</script>
  <script>
    (function () {
      var CN_I18N = """ + json.dumps(I, ensure_ascii=False) + """;
      try { Object.keys(CN_I18N).forEach(function (l) { if (typeof i18n !== 'undefined' && i18n[l]) Object.assign(i18n[l], CN_I18N[l]); }); } catch (e) {}
      function cnLang() { var l = localStorage.getItem('lang') || 'en'; return CN_I18N[l] ? l : 'en'; }
      var host = document.getElementById('cn-viewer'); if (!host) return;
      var steps = ['overview', 'shank', 'mech', 'grip', 'stop', 'explode', 'cycle'], durs = [6, 6, 9, 7, 7, 7, 10];
      var viewer = null, started = false, cur = 0, t0 = performance.now();
      function setCaption(i) { var c = document.getElementById('cn-caption'); c.textContent = CN_I18N[cnLang()]['cn_cap_' + steps[i]] || CN_I18N.en['cn_cap_' + steps[i]]; }
      function highlight(i) {
        document.querySelectorAll('#cn-sm-2713 .cn-tab').forEach(function (b) { b.classList.toggle('active', +b.dataset.cnStep === i); });
        document.querySelectorAll('#cn-sm-2713 .cn-feat').forEach(function (b) { b.classList.toggle('active', +b.dataset.cnStep === i); });
      }
      function start() {
        if (started) return; started = true;
        var b64 = document.getElementById('cn-model-data').textContent.trim();
        window.CNSM2713.mountViewer({ host: host, model: b64 }).then(function (v) {
          viewer = v; document.getElementById('cn-loading').remove();
          v.onChange(function (e) {
            if (e.step !== cur || e.manual) { cur = e.step; t0 = performance.now(); }
            setCaption(e.step); highlight(e.manual ? -1 : e.step);
            document.querySelector('#cn-play i').className = 'fa-solid ' + (e.playing && !e.manual ? 'fa-pause' : 'fa-play');
          });
          setCaption(0); highlight(0);
        }).catch(function (err) { document.getElementById('cn-loading').textContent = 'WebGL is not available in this browser.'; console.error(err); });
      }
      var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { start(); io.disconnect(); } }, { rootMargin: '300px' });
      io.observe(host);
      document.querySelectorAll('#cn-sm-2713 [data-cn-step]').forEach(function (b) {
        b.addEventListener('click', function () { if (!viewer) return; var i = +b.dataset.cnStep; viewer.goTo(i); document.getElementById('cn-jaw').value = 0; document.getElementById('cn-jaw-val').textContent = '0%'; });
      });
      document.getElementById('cn-play').addEventListener('click', function () { if (viewer) viewer.toggle(); });
      var jaw = document.getElementById('cn-jaw');
      jaw.addEventListener('input', function () { if (!viewer) return; viewer.setOpen(jaw.value / 100); document.getElementById('cn-jaw-val').textContent = jaw.value + '%'; });
      setInterval(function () {
        if (!viewer) return; var p = Math.min(100, (performance.now() - t0) / 10 / durs[cur]);
        document.getElementById('cn-progress').style.width = p + '%';
      }, 200);
      document.getElementById('langSelector').addEventListener('change', function () { setCaption(cur); });
    })();
  </script>
  <script type="application/ld+json">""" + json.dumps(ld, ensure_ascii=False, indent=1) + """</script>
"""

out = src
# head css
out = out.replace('</head>', css + '</head>', 1)
# nav links (desktop + mobile)
out = out.replace('<a href="#models" data-i18n="nav_models" class="block',
                  '<a href="#cn-sm-2713" data-i18n="cn_nav" class="block text-slate-700 dark:text-slate-200 hover:text-brand-teal font-medium py-1">' + E['cn_nav'] + '</a>\n      <a href="#models" data-i18n="nav_models" class="block', 1)
# hero: extra CTA to the 3D section
out = out.replace('<a href="#videos" class="inline-flex items-center justify-center px-5 py-3.5',
                  '<a href="#cn-sm-2713" class="inline-flex items-center justify-center px-5 py-3.5 rounded-xl font-semibold text-brand-amber hover:text-brand-teal transition-colors"><i class="fa-solid fa-cube mr-2"></i><span data-i18n="cn_nav">' + E['cn_nav'] + '</span></a>\n            <a href="#videos" class="inline-flex items-center justify-center px-5 py-3.5', 1)
# section after hero
marker = '<!-- SECTION 2: TECHNICAL CHALLENGE'
assert marker in out
out = out.replace(marker, section.strip() + '\n\n  ' + marker, 1)
# meta keywords
out = out.replace('content="JUKI JM gripper nozzle,', 'content="CN-SM-2713, JUKI coil gripper nozzle, JUKI JM gripper nozzle,', 1)
# scripts at end
idx = out.rindex('</body>')
out = out[:idx] + init_js + out[idx:]
open(P + 'deliverables/juki-jm-odd-form-insertion-gripper-nozzle-cn-sm-2713.html', 'w', encoding='utf-8').write(out)
print(len(out))
