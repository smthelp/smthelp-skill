/* smt-3d-animation-landing-kit · page runtime v1.0.0 — i18n, theme, duel controller, 3D viewer, fit check, ROI, lightbox, videos */
(function () {
  'use strict';
  function $(id) { return document.getElementById(id); }
  var BOOT = JSON.parse($('smt-boot').textContent), I18N = JSON.parse($('smt-i18n').textContent);
  var EN = I18N[BOOT.def] || {}, LANG = BOOT.def;
  function t(k) { return (I18N[LANG] && I18N[LANG][k]) || EN[k] || ''; }
  /* ---------- i18n ---------- */
  function setLang(l) {
    if (BOOT.langs.indexOf(l) < 0) l = BOOT.def; LANG = l;
    document.documentElement.lang = l; document.documentElement.dir = BOOT.rtl.indexOf(l) >= 0 ? 'rtl' : 'ltr';
    Array.prototype.forEach.call(document.querySelectorAll('[data-i18n]'), function (e) { var v = t(e.getAttribute('data-i18n')); if (v) e.textContent = v; });
    var s = $('lang'); if (s) s.value = l;
    try { localStorage.setItem('smt-lang', l); } catch (e) {}
    if (window.__duelRefresh) window.__duelRefresh(); if (window.__fit) window.__fit();
  }
  var q = (location.search.match(/[?&]lang=([a-z]{2})/) || [])[1], saved = null;
  try { saved = localStorage.getItem('smt-lang'); } catch (e) {}
  if ($('lang')) $('lang').addEventListener('change', function () { setLang(this.value); });
  /* ---------- theme + nav ---------- */
  var thm = $('thm');
  if (thm) thm.addEventListener('click', function () { var d = document.documentElement.getAttribute('data-theme') === 'dark'; document.documentElement.setAttribute('data-theme', d ? 'light' : 'dark'); });
  var nt = $('navt'), nv = $('nav');
  if (nt) { nt.addEventListener('click', function () { var o = nv.classList.toggle('open'); nt.setAttribute('aria-expanded', o); });
    nv.addEventListener('click', function (e) { if (e.target.tagName === 'A') nv.classList.remove('open'); }); }
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* ---------- duel (side-by-side mechanism animation) ---------- */
  if (BOOT.duel && window[BOOT.duel.cls] && $('duelRoot')) (function () {
    var root = $('duelRoot'), tabs = $('tabs'), D = new window[BOOT.duel.cls](root), CH = BOOT.duel.chapters, DUR = BOOT.duel.cycle;
    var cur = 0, chStart = 0, playing = !reduce, slow = false, simT = reduce ? 1.35 : 0, last = null, visible = true, count0 = {};
    CH.forEach(function (c, i) { var b = document.createElement('button'); b.className = 'tab'; b.setAttribute('role', 'tab'); b.addEventListener('click', function () { go(i); }); tabs.appendChild(b); });
    function labels() { Array.prototype.forEach.call(tabs.children, function (b, i) { b.textContent = (i + 1) + '. ' + t('duel.chapters.' + i + '.tab'); }); $('dexp').textContent = t('duel.chapters.' + cur + '.text'); }
    window.__duelRefresh = labels;
    function go(i) { cur = i; chStart = simT; var o = D.render(simT, { chapter: CH[i], chapterT: 0 }) || {}; count0 = o;
      Array.prototype.forEach.call(tabs.children, function (b, k) { b.setAttribute('aria-selected', k === i); }); labels(); }
    function frame(ts) { if (last == null) last = ts; var dt = Math.min(0.05, (ts - last) / 1000); last = ts;
      if (playing && visible) { simT += dt * (slow ? 0.3 : 1); if (simT - chStart > DUR) go((cur + 1) % CH.length);
        D.render(simT, { chapter: CH[cur], chapterT: simT - chStart, count0: count0 }); $('prog').style.width = Math.min(100, (simT - chStart) / DUR * 100) + '%'; }
      requestAnimationFrame(frame); }
    go(0); if (reduce) D.render(simT, { chapter: CH[0] });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(root);
    requestAnimationFrame(frame);
    var bp = $('bPlay'); bp.addEventListener('click', function () { playing = !playing; bp.textContent = playing ? t('ui.pause') : '▶'; bp.setAttribute('aria-pressed', playing); });
    var bs = $('bSlow'); bs.addEventListener('click', function () { slow = !slow; bs.setAttribute('aria-pressed', slow); });
  })();
  /* ---------- 3D viewer ---------- */
  var stage = $('v3d'), dataEl = $('smt3d-data');
  if (stage && dataEl && window.SMT3D) {
    var started = false, V = null;
    var start = function () {
      if (started) return; started = true;
      V = SMT3D.mount(stage, JSON.parse(dataEl.textContent), { material: BOOT.model.material, light: BOOT.model.light, auto: !reduce,
        onInteract: function () { if (V) { V.setAuto(false); $('v3dAuto').setAttribute('aria-pressed', 'false'); } } });
      window.__v3d = V;
    };
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { if (e[0].isIntersecting) start(); }, { rootMargin: '200px' }).observe(stage); else start();
    function seg(attr, fn) { Array.prototype.forEach.call(document.querySelectorAll('[' + attr + ']'), function (b) { b.addEventListener('click', function () {
      start(); Array.prototype.forEach.call(document.querySelectorAll('[' + attr + ']'), function (x) { x.setAttribute('aria-pressed', x === b); }); if (V) fn(b.getAttribute(attr)); }); }); }
    seg('data-mat', function (v) { V.setMaterial(v); }); seg('data-light', function (v) { V.setLight(v); });
    $('v3dEx').addEventListener('input', function () { start(); if (V) V.setExplode(this.value / 100); });
    $('v3dAuto').addEventListener('click', function () { start(); var on = this.getAttribute('aria-pressed') !== 'true'; this.setAttribute('aria-pressed', on); if (V) V.setAuto(on); });
    $('v3dReset').addEventListener('click', function () { start(); if (V) V.reset(); $('v3dEx').value = 0; });
  } else if (stage) stage.setAttribute('data-smt3d', 'nowebgl');
  /* ---------- fit check ---------- */
  if ($('fitOut')) {
    var ins = document.querySelectorAll('.fit input');
    window.__fit = function () {
      var rows = [], bad = 0, msg = [];
      Array.prototype.forEach.call(ins, function (e) {
        var v = parseFloat(e.value), mn = parseFloat(e.getAttribute('data-min')), mx = parseFloat(e.getAttribute('data-max')), u = e.getAttribute('data-unit') || '';
        var lab = e.previousElementSibling ? e.previousElementSibling.textContent : e.getAttribute('data-name');
        var ok = !isNaN(v) && (isNaN(mn) || v >= mn) && (isNaN(mx) || v <= mx); if (!ok) bad++;
        var rng = (isNaN(mn) ? '' : mn) + (isNaN(mx) ? '+' : ' – ' + mx) + ' ' + u;
        rows.push('<li class="' + (ok ? 'ok' : 'no') + '"><b>' + (ok ? '✓' : '✕') + '</b><span>' + lab + ': ' + (isNaN(v) ? '?' : v) + ' ' + u + ' (' + rng + ')</span></li>');
        msg.push(lab + ' ' + e.value + ' ' + u);
      });
      $('fitOut').innerHTML = rows.join('');
      $('fitNote').textContent = bad ? t('fit.bad') || 'Outside a published range: send a sample and we will tell you what is possible.' : t('fit.good') || 'Inside every published range. Next step: a sample trial.';
      $('fitCta').href = BOOT.wa + '?text=' + encodeURIComponent(BOOT.fitTpl + msg.join('; '));
    };
    Array.prototype.forEach.call(ins, function (e) { e.addEventListener('input', window.__fit); }); window.__fit();
  }
  /* ---------- ROI ---------- */
  if ($('roi_hourly_cost')) {
    var K = ['operators_saved', 'hourly_cost', 'hours_per_shift', 'shifts_per_day', 'days_per_year', 'extra_output_per_hour', 'margin_per_unit', 'investment'];
    var fmt = function (n) { return isFinite(n) ? Math.round(n).toLocaleString('en-US') : '–'; };
    var roi = function () {
      var v = {}; K.forEach(function (k) { v[k] = parseFloat($('roi_' + k).value) || 0; });
      var hours = v.hours_per_shift * v.shifts_per_day * v.days_per_year;
      var labour = v.operators_saved * v.hourly_cost * hours, output = v.extra_output_per_hour * v.margin_per_unit * hours, total = labour + output;
      $('roiR_labour').textContent = BOOT.currency + ' ' + fmt(labour); $('roiR_output').textContent = BOOT.currency + ' ' + fmt(output);
      $('roiR_total').textContent = BOOT.currency + ' ' + fmt(total);
      $('roiR_payback').textContent = v.investment > 0 && total > 0 ? (v.investment / (total / 12)).toFixed(1) : '–';
    };
    K.forEach(function (k) { $('roi_' + k).addEventListener('input', roi); }); roi();
  }
  /* ---------- lightbox + videos ---------- */
  var lb = $('lb');
  if (lb && $('gal')) { var li = lb.querySelector('img');
    $('gal').addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; li.src = b.getAttribute('data-full'); li.alt = b.querySelector('img').alt; if (lb.showModal) lb.showModal(); });
    lb.querySelector('button').addEventListener('click', function () { lb.close(); }); lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); }); }
  Array.prototype.forEach.call(document.querySelectorAll('.vld'), function (b) { b.addEventListener('click', function () {
    var f = document.createElement('iframe'); f.src = 'https://www.youtube-nocookie.com/embed/' + b.getAttribute('data-id') + '?autoplay=1&rel=0';
    f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'; f.allowFullscreen = true; f.title = b.getAttribute('aria-label');
    b.parentNode.appendChild(f); b.remove(); }); });
  setLang(q || saved || BOOT.def);
})();
