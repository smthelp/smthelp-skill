/* Duel skeleton — copy to <job>/duel.js and rename the class (job.duel.class).
   Contract used by templates/landing/app.js and templates/video/video.html:
     new MyDuel(rootEl)            rootEl contains [data-fd="<key>"] hosts, [data-fd-metrics="<key>"], [data-fd-count="<key>"], [data-badge]
     duel.render(t, st) -> {key: pickCount}
        t   seconds (deterministic: same t -> same frame; never use Date/Math.random at render time)
        st  {chapter, chapterT, step, side, count0, clock:{key:t}}
     MyDuel.METRICS[chapter][key] = [[label, value], ...]   MyDuel.BADGE[chapter] = 'WINNER TEXT'
   Real examples: examples/stf1003-tube-feeder/duel.js (TubeDuel), examples/bowl-vs-belt/duel.js (FeederDuel). */
(function (G) {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function el(tag, a, p) { var e = document.createElementNS(NS, tag); for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; }
  var CYCLE = { a: 1.75, b: 0.8 };   // published cycle times per side (s) — from the spec sheet only
  var METRICS = { principle: { a: [['Drive', '…']], b: [['Drive', '…']] }, speed: { a: [['Cycle', '1.75 s']], b: [['Cycle', '0.8 s']], win: 'b' } };
  var BADGE = { speed: 'FASTER' };
  function build(svg, key) {
    el('rect', { width: 800, height: 560, fill: '#0c1c1a' }, svg);
    var part = el('rect', { x: -10, y: -8, width: 20, height: 16, rx: 2, fill: '#e9eef0' }, svg);
    return { render: function (t) { var p = (t / CYCLE[key]) % 1; part.setAttribute('transform', 'translate(' + (100 + 600 * p) + ',300)'); return Math.floor(t / CYCLE[key]); } };
  }
  function MyDuel(root) {
    this.root = root; this.m = {};
    var self = this;
    ['a', 'b'].forEach(function (k) { var host = root.querySelector('[data-fd="' + k + '"]'); if (!host) return;
      var svg = el('svg', { viewBox: '0 0 800 560' }); host.appendChild(svg); self.m[k] = build(svg, k); });
  }
  MyDuel.prototype.render = function (t, st) {
    st = st || {}; var out = {}, root = this.root, met = METRICS[st.chapter] || METRICS.principle;
    for (var k in this.m) { var tk = st.clock && st.clock[k] != null ? st.clock[k] : t; out[k] = this.m[k].render(tk); }
    if (this._ch !== st.chapter) { this._ch = st.chapter;
      ['a', 'b'].forEach(function (k) { var box = root.querySelector('[data-fd-metrics="' + k + '"]'); if (!box || !met[k]) return;
        box.innerHTML = met[k].map(function (r) { return '<div class="fd-m"><span>' + r[0] + '</span><b>' + r[1] + '</b></div>'; }).join('');
        var c = root.querySelector('[data-fd-card="' + k + '"]'); if (c) c.classList.toggle('fd-win', met.win === k); });
      Array.prototype.forEach.call(root.querySelectorAll('[data-badge]'), function (e) { e.textContent = BADGE[st.chapter] || ''; }); }
    for (k in out) { var c = root.querySelector('[data-fd-count="' + k + '"]'); if (c) c.textContent = Math.max(0, out[k] - ((st.count0 || {})[k] || 0)); }
    return out;
  };
  MyDuel.METRICS = METRICS; MyDuel.BADGE = BADGE;
  G.MyDuel = MyDuel;
})(window);
