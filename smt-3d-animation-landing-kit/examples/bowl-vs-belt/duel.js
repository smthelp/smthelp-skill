/* FeederDuel — side-by-side working-principle animation
   SBF1001 vibratory bowl feeder  vs  S-MVF01 reciprocating belt feeder
   Deterministic: everything is a pure function of time t (seconds) + state.
   (c) Southern Machinery — smthelp.com */
(function (G) {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function ease(x) { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); }
  function frac(x) { return x - Math.floor(x); }
  function hash(a, b) { var s = Math.sin(a * 127.1 + b * 311.7) * 43758.5453; return s - Math.floor(s); }

  var C = {
    bg: '#0c1c1a', grid: 'rgba(120,200,185,.07)', steel1: '#c9d6d4', steel2: '#7f9592', steel3: '#4b5d5a',
    dark: '#26343a', dark2: '#1a2529', teal: '#2fc1aa', teal2: '#0c665c', gold: '#f2b84b', lime: '#9ad04a',
    red: '#ff6b5a', part: '#e9eef0', partEdge: '#5d6c70', ink: '#eaf3f1', ink2: '#9fb9b4'
  };

  var DATA = {
    bowl: { name: 'SBF1001 Vibratory Bowl Feeder', short: 'Bowl', cycle: 0.8, cycleLabel: '0.8 s' },
    belt: { name: 'S-MVF01 Reciprocating Belt Feeder', short: 'Belt', cycle: 1.75, cycleLabel: '1.5–2 s' }
  };

  /* ---------- shared bits ---------- */
  function defs(svg, id) {
    var d = el('defs', null, svg);
    var p = el('pattern', { id: id + 'g', width: 40, height: 40, patternUnits: 'userSpaceOnUse' }, d);
    el('path', { d: 'M40 0H0V40', fill: 'none', stroke: C.grid, 'stroke-width': 1 }, p);
    var lg = el('linearGradient', { id: id + 'st', x1: 0, y1: 0, x2: 0, y2: 1 }, d);
    el('stop', { offset: 0, 'stop-color': '#e6eeed' }, lg); el('stop', { offset: 0.55, 'stop-color': '#93a6a3' }, lg); el('stop', { offset: 1, 'stop-color': '#5b6d6a' }, lg);
    var lg2 = el('linearGradient', { id: id + 'dk', x1: 0, y1: 0, x2: 0, y2: 1 }, d);
    el('stop', { offset: 0, 'stop-color': '#3a4a52' }, lg2); el('stop', { offset: 1, 'stop-color': '#1d282d' }, lg2);
    var rg = el('radialGradient', { id: id + 'fl', cx: 0.5, cy: 0.45, r: 0.6 }, d);
    el('stop', { offset: 0, 'stop-color': '#55706c' }, rg); el('stop', { offset: 1, 'stop-color': '#22302f' }, rg);
    var gl = el('filter', { id: id + 'glow', x: '-50%', y: '-50%', width: '200%', height: '200%' }, d);
    el('feGaussianBlur', { stdDeviation: 4, result: 'b' }, gl);
    var m = el('feMerge', null, gl); el('feMergeNode', { in: 'b' }, m); el('feMergeNode', { in: 'SourceGraphic' }, m);
    return d;
  }
  function partShape(parent) {
    var g = el('g', null, parent);
    el('rect', { x: -8, y: -5, width: 16, height: 10, rx: 2, fill: C.part, stroke: C.partEdge, 'stroke-width': 1.2 }, g);
    el('rect', { x: -8, y: -5, width: 5, height: 10, rx: 1.5, fill: C.teal2 }, g); // polarity mark
    return g;
  }
  function setPart(g, x, y, rot, op, tint) {
    g.setAttribute('transform', 'translate(' + x.toFixed(2) + ',' + y.toFixed(2) + ') rotate(' + rot.toFixed(1) + ')');
    g.setAttribute('opacity', op.toFixed(3));
    var r = g.firstChild; r.setAttribute('fill', tint || C.part);
  }
  function nozzle(parent) {
    var g = el('g', null, parent);
    el('rect', { x: -26, y: -150, width: 52, height: 70, rx: 6, fill: '#33464c', stroke: '#5f7a80' }, g);
    el('rect', { x: -9, y: -80, width: 18, height: 62, fill: '#8aa3a5' }, g);
    el('rect', { x: -6, y: -18, width: 12, height: 14, rx: 2, fill: C.gold }, g);
    var t = el('text', { x: 0, y: -108, 'text-anchor': 'middle', 'font-size': 13, 'font-weight': 700, fill: C.ink2, 'font-family': 'Arial' }, g);
    t.textContent = 'HEAD';
    return g;
  }
  function callout(parent, n, x, y, label, side) {
    var g = el('g', { class: 'fd-call', 'data-n': n, opacity: 0 }, parent);
    el('circle', { cx: x, cy: y, r: 17, fill: C.gold, stroke: '#fff', 'stroke-width': 2 }, g);
    var t = el('text', { x: x, y: y + 6, 'text-anchor': 'middle', 'font-size': 18, 'font-weight': 800, fill: '#10201e', 'font-family': 'Arial' }, g);
    t.textContent = n;
    var lx = side === 'l' ? x - 24 : x + 24;
    var tt = el('text', { x: lx, y: y + 6, 'text-anchor': side === 'l' ? 'end' : 'start', 'font-size': 19, 'font-weight': 700, fill: '#fff', 'font-family': 'Arial', 'paint-order': 'stroke', stroke: C.bg, 'stroke-width': 5 }, g);
    tt.textContent = label;
    return g;
  }
  function label(parent, x, y, txt, size, fill, anchor, weight) {
    var t = el('text', { x: x, y: y, 'text-anchor': anchor || 'middle', 'font-size': size || 14, 'font-weight': weight || 700, fill: fill || C.ink2, 'font-family': 'Arial', 'letter-spacing': '.06em' }, parent);
    t.textContent = txt; return t;
  }
  function ring(parent, x, y) {
    var g = el('g', { opacity: 0 }, parent);
    el('circle', { cx: x, cy: y, r: 46, fill: 'rgba(12,28,26,.75)', stroke: 'rgba(255,255,255,.15)', 'stroke-width': 6 }, g);
    var arc = el('circle', { cx: x, cy: y, r: 46, fill: 'none', stroke: C.gold, 'stroke-width': 6, 'stroke-linecap': 'round', transform: 'rotate(-90 ' + x + ' ' + y + ')', 'stroke-dasharray': '0 999' }, g);
    var t = el('text', { x: x, y: y + 2, 'text-anchor': 'middle', 'font-size': 22, 'font-weight': 800, fill: '#fff', 'font-family': 'Arial' }, g);
    var t2 = el('text', { x: x, y: y + 22, 'text-anchor': 'middle', 'font-size': 11, 'font-weight': 700, fill: C.ink2, 'font-family': 'Arial' }, g);
    t2.textContent = 'PER PICK';
    return { g: g, arc: arc, t: t };
  }
  function footprint(parent, id, wmm, dmm, hmm, kg, cap) {
    // drawn at common scale 0.42 px/mm so both panels are directly comparable
    var S = 0.42, g = el('g', { opacity: 0 }, parent);
    el('rect', { x: 40, y: 40, width: 720, height: 480, fill: 'url(#' + id + 'g)', stroke: 'rgba(120,200,185,.25)', 'stroke-dasharray': '6 6' }, g);
    label(g, 400, 75, 'TOP VIEW · SAME SCALE (grid = 95 mm)', 15, C.ink2);
    var w = wmm * S, d = dmm * S, x = 400 - w / 2, y = 250 - d / 2;
    var r = el('rect', { x: x, y: y, width: w, height: d, rx: 6, fill: 'rgba(47,193,170,.22)', stroke: C.teal, 'stroke-width': 3 }, g);
    label(g, 400, y - 14, wmm + ' mm', 20, '#fff');
    label(g, x + w + 12, 255, dmm + ' mm', 20, '#fff', 'start');
    label(g, 400, 255 + 4, cap, 18, C.teal, 'middle', 800);
    // weight bar (max 190 kg)
    var bw = 560 * kg / 190;
    el('rect', { x: 120, y: 430, width: 560, height: 26, rx: 13, fill: 'rgba(255,255,255,.08)' }, g);
    var bar = el('rect', { x: 120, y: 430, width: 0.001, height: 26, rx: 13, fill: C.gold }, g);
    label(g, 120, 418, 'WEIGHT', 14, C.ink2, 'start');
    var kt = label(g, 680, 418, kg + ' kg', 22, '#fff', 'end', 800);
    label(g, 120, 492, 'HEIGHT ' + hmm + ' mm', 14, C.ink2, 'start');
    return { g: g, bar: bar, bw: bw, rect: r };
  }

  /* ---------- BOWL ---------- */
  function buildBowl(svg) {
    var id = 'fdb' + Math.floor(Math.random() * 1e6);
    defs(svg, id);
    el('rect', { width: 800, height: 560, fill: C.bg }, svg);
    el('rect', { width: 800, height: 560, fill: 'url(#' + id + 'g)' }, svg);
    var M = el('g', null, svg); // mechanism layer
    var cx = 300, cy = 318;
    // coil base + springs
    var base = el('g', null, M);
    el('rect', { x: 170, y: 410, width: 260, height: 80, rx: 8, fill: 'url(#' + id + 'dk)', stroke: '#4e6168' }, base);
    label(base, 300, 457, 'COIL DRIVE', 15, C.ink2);
    var coilWaves = el('path', { d: '', fill: 'none', stroke: C.teal, 'stroke-width': 2.5, opacity: 0.9 }, base);
    var springs = [];
    [215, 300, 385].forEach(function (sx) { springs.push(el('path', { d: '', fill: 'none', stroke: C.steel2, 'stroke-width': 4 }, base)); springs[springs.length - 1]._x = sx; });
    // bowl group (vibrates)
    var B = el('g', null, M);
    el('path', { d: 'M100 300 C 105 360, 160 392, 300 396 C 440 392, 495 360, 500 300 Z', fill: 'url(#' + id + 'st)', stroke: '#2b3a3a', 'stroke-width': 1.5 }, B);
    el('ellipse', { cx: cx, cy: 300, rx: 200, ry: 86, fill: '#a9bab8', stroke: '#e9f0ef', 'stroke-width': 3 }, B);
    el('ellipse', { cx: cx, cy: 314, rx: 178, ry: 72, fill: 'url(#' + id + 'fl)' }, B);
    // spiral track
    var TH = 3.0 * Math.PI, th0 = -0.12 * Math.PI - TH;
    function sp(u) { var th = u * TH, r = 48 + 128 * u; return [cx + r * Math.cos(th + th0), cy + 0.42 * r * Math.sin(th + th0) - 24 * u, th + th0]; }
    var dpath = '';
    for (var i = 0; i <= 160; i++) { var p = sp(i / 160); dpath += (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1); }
    el('path', { d: dpath, fill: 'none', stroke: '#283836', 'stroke-width': 16, 'stroke-linecap': 'round' }, B);
    var track = el('path', { d: dpath, fill: 'none', stroke: '#c7d5d3', 'stroke-width': 10, 'stroke-linecap': 'round' }, B);
    var trackHi = el('path', { d: dpath, fill: 'none', stroke: C.gold, 'stroke-width': 12, 'stroke-linecap': 'round', opacity: 0 }, B);
    // pile in the middle
    var pile = [];
    for (i = 0; i < 26; i++) {
      var a = hash(i, 1) * Math.PI * 2, rr = Math.sqrt(hash(i, 2)) * 38;
      var pg = partShape(B); pg._x = cx + rr * Math.cos(a); pg._y = cy + 6 + rr * 0.45 * Math.sin(a); pg._r = hash(i, 3) * 360; pile.push(pg);
    }
    // gate (orientation selector)
    var uG = 0.70, pGate = sp(uG);
    var gate = el('g', null, B);
    el('rect', { x: pGate[0] - 5, y: pGate[1] - 22, width: 10, height: 18, rx: 2, fill: C.gold }, gate);
    // spiral parts
    var NS_ = 18, sparts = [];
    for (i = 0; i < NS_; i++) sparts.push(partShape(B));
    var sparks = [];
    for (i = 0; i < 7; i++) sparks.push(el('path', { d: 'M0 -9 L2.5 -2.5 9 0 2.5 2.5 0 9 -2.5 2.5 -9 0 -2.5 -2.5Z', fill: C.red, opacity: 0, filter: 'url(#' + id + 'glow)' }, B));
    // rail
    var pEnd = sp(1), railY = pEnd[1], railX0 = pEnd[0] - 4, pickX = 712;
    var R = el('g', null, M);
    el('rect', { x: railX0, y: railY - 7, width: 760 - railX0, height: 22, rx: 3, fill: '#8a9e9b', stroke: '#2b3a3a' }, R);
    el('rect', { x: railX0, y: railY + 3, width: 760 - railX0, height: 4, fill: '#55686a' }, R);
    el('rect', { x: railX0 + 30, y: railY + 15, width: 200, height: 40, rx: 5, fill: 'url(#' + id + 'dk)', stroke: '#4e6168' }, R);
    label(R, railX0 + 130, railY + 40, 'LINEAR VIBRATOR', 12, C.ink2);
    var railWaves = el('path', { d: '', fill: 'none', stroke: C.teal, 'stroke-width': 2 }, R);
    // air nozzles
    var puffs = [];
    [railX0 + 60, railX0 + 150].forEach(function (ax) {
      el('rect', { x: ax - 6, y: railY - 46, width: 12, height: 26, rx: 2, fill: '#5b7177' }, R);
      el('path', { d: 'M' + ax + ' ' + (railY - 20) + 'l10 8', stroke: '#5b7177', 'stroke-width': 4 }, R);
      for (var k = 0; k < 3; k++) { var pf = el('circle', { r: 4, fill: '#bfe9ff', opacity: 0 }, R); pf._ax = ax; pf._k = k; puffs.push(pf); }
    });
    label(R, railX0 + 105, railY - 56, 'AIR BLOW', 12, '#bfe9ff');
    // fibre sensor
    el('rect', { x: pickX + 14, y: railY - 36, width: 12, height: 22, rx: 2, fill: '#3d5157' }, R);
    el('rect', { x: pickX + 14, y: railY + 16, width: 12, height: 22, rx: 2, fill: '#3d5157' }, R);
    var beam = el('line', { x1: pickX + 20, y1: railY - 14, x2: pickX + 20, y2: railY + 16, stroke: C.red, 'stroke-width': 3, filter: 'url(#' + id + 'glow)' }, R);
    var NQ = 9, pitch = 26, queue = [];
    for (i = 0; i < NQ; i++) queue.push(partShape(R));
    var carried = partShape(R);
    var head = nozzle(R);
    // stand
    el('rect', { x: 540, y: railY + 56, width: 14, height: 434 - railY, fill: '#3a4a52' }, M);
    // overlays
    var O = el('g', null, svg);
    var calls = [
      callout(O, 1, 300, 505, 'Coil-driven vibration', 'r'),
      callout(O, 2, sp(0.42)[0], sp(0.42)[1], 'Spiral track, tooled per part', 'l'),
      callout(O, 3, pGate[0], pGate[1] - 40, 'Wrong attitude falls back', 'r'),
      callout(O, 4, railX0 + 230, railY - 92, 'Vibration + air blowing', 'l'),
      callout(O, 5, pickX + 20, railY + 70, 'Fibre check · pick ±0.5 mm', 'l')
    ];
    var rg = ring(O, 600, 120);
    var fp = footprint(svg, id, 1120, 460, 910, 190, 'DOUBLE-BOWL FRAME');
    var tags = el('g', { opacity: 0 }, O);
    var tagT = label(tags, 300, 182, '', 20, C.red, 'middle', 800);
    var tagT2 = label(tags, 300, 206, '', 15, C.ink2, 'middle', 700);
    return {
      type: 'bowl', svg: svg, M: M, O: O, calls: calls, ring: rg, fp: fp, tags: tags, tagT: tagT, tagT2: tagT2, trackHi: trackHi,
      render: function (t, st) {
        var T = DATA.bowl.cycle, sp_ = st.speed || 1;
        var tt = t * sp_;
        var jx = Math.sin(tt * 97) * 1.6, jy = Math.cos(tt * 113) * 1.0;
        B.setAttribute('transform', 'translate(' + jx.toFixed(2) + ',' + jy.toFixed(2) + ')');
        // springs / coil waves
        springs.forEach(function (s) {
          var x = s._x, y0 = 396, y1 = 412, d = 'M' + x + ' ' + (y0 + jy);
          for (var k = 1; k <= 6; k++) d += 'L' + (x + (k % 2 ? 7 : -7)) + ' ' + (y0 + jy + (y1 - y0 - jy) * k / 6);
          s.setAttribute('d', d);
        });
        var dw = 'M195 430'; for (var k = 0; k <= 52; k++) { var xx = 195 + k * 4; dw += 'L' + xx + ' ' + (430 - Math.abs(Math.sin(k * 0.9 + tt * 40)) * 9).toFixed(1); }
        coilWaves.setAttribute('d', dw);
        var rw = 'M' + (railX0 + 40) + ' ' + (railY + 48); for (k = 0; k <= 45; k++) rw += 'L' + (railX0 + 40 + k * 4) + ' ' + (railY + 48 - Math.abs(Math.sin(k * 1.1 + tt * 46)) * 6).toFixed(1);
        railWaves.setAttribute('d', rw);
        pile.forEach(function (p, i) { setPart(p, p._x + Math.sin(tt * 60 + i) * 1.4, p._y + Math.cos(tt * 70 + i * 2) * 1.1, p._r + Math.sin(tt * 9 + i) * 8, 1); });
        // spiral parts
        var v = 0.085, nsp = 0;
        for (var i = 0; i < NS_; i++) {
          var ph = tt * v + i / NS_, cyc = Math.floor(ph), u = frac(ph);
          var bad = hash(i, cyc) < 0.38, g = sparts[i];
          if (bad && u > uG) {
            var f = (u - uG) / 0.06; // falling phase
            if (f > 1) { g.setAttribute('opacity', 0); continue; }
            var p0 = sp(uG), x = p0[0] + (cx - p0[0]) * f * 0.55, y = p0[1] - 30 * Math.sin(f * Math.PI) + (cy + 8 - p0[1]) * f;
            setPart(g, x, y, f * 260, 1 - f * 0.6, '#ffb3a8');
          } else {
            var p = sp(u), ang = p[2] * 180 / Math.PI + 90;
            var tint = (bad && u > uG - 0.18) ? '#ffd7a0' : C.part;
            setPart(g, p[0], p[1] - 6, ang + (bad ? 90 : 0), u < 0.04 ? u / 0.04 : (u > 0.96 ? (1 - u) / 0.04 : 1), tint);
          }
        }
        // sparks (friction) in 'gentle'
        var showSp = st.chapter === 'gentle' ? 1 : 0;
        sparks.forEach(function (s, k) {
          var cyc = Math.floor(tt * 2.2 + k * 0.37), u = 0.15 + hash(k, cyc) * 0.7, p = sp(u), lf = frac(tt * 2.2 + k * 0.37);
          s.setAttribute('transform', 'translate(' + p[0].toFixed(1) + ',' + (p[1] - 8).toFixed(1) + ') scale(' + (0.6 + lf).toFixed(2) + ')');
          s.setAttribute('opacity', (showSp * (1 - lf)).toFixed(2));
        });
        // puffs
        puffs.forEach(function (pf) { var q = frac(tt * 2.6 + pf._k / 3); pf.setAttribute('cx', pf._ax + 10 + q * 46); pf.setAttribute('cy', railY - 8 + q * 4); pf.setAttribute('opacity', (0.9 * (1 - q)).toFixed(2)); pf.setAttribute('r', 3 + q * 5); });
        // pick cycle
        var P = frac(tt / T);
        var down = P < 0.22 ? ease(P / 0.22) : P < 0.32 ? 1 : 1 - ease((P - 0.32) / 0.25);
        var tipY = railY - 4, hy = 160 + (tipY - 160) * down;
        head.setAttribute('transform', 'translate(' + pickX + ',' + hy.toFixed(1) + ')');
        var shift = pitch * ease((P - 0.55) / 0.35);
        for (i = 0; i < NQ; i++) {
          var x = pickX - i * pitch + shift + Math.sin(tt * 120 + i) * 0.8;
          var vis = 1; if (i === 0 && P >= 0.3) vis = 0;
          if (x < railX0 + 10) vis = clamp((x - railX0) / 10, 0, 1);
          setPart(queue[i], x, railY - 1, 0, vis);
        }
        if (P >= 0.3) setPart(carried, pickX, hy + 4, 0, P < 0.62 ? 1 : clamp(1 - (P - 0.62) / 0.15, 0, 1)); else carried.setAttribute('opacity', 0);
        var present = P < 0.3 || P > 0.9;
        beam.setAttribute('stroke', present ? C.lime : C.red);
        // ring
        rg.arc.setAttribute('stroke-dasharray', (P * 289).toFixed(1) + ' 999');
        rg.t.textContent = DATA.bowl.cycleLabel;
        return Math.floor(tt / T);
      }
    };
  }

  /* ---------- BELT ---------- */
  function buildBelt(svg) {
    var id = 'fdt' + Math.floor(Math.random() * 1e6);
    defs(svg, id);
    el('rect', { width: 800, height: 560, fill: C.bg }, svg);
    el('rect', { width: 800, height: 560, fill: 'url(#' + id + 'g)' }, svg);
    var M = el('g', null, svg);
    var A = [176, 392], Bp = [470, 214], railY = 214, pickX = 712;
    // body housing
    el('path', { d: 'M60 300 L60 450 L770 450 L770 300 L560 300 L470 214 L360 214 L250 300 Z', fill: 'url(#' + id + 'dk)', stroke: '#4e6168', 'stroke-width': 1.5, opacity: 0.55 }, M);
    // control panel
    var cp = el('g', null, M);
    el('rect', { x: 700, y: 300, width: 64, height: 140, rx: 5, fill: '#2b3940', stroke: '#5f7a80' }, cp);
    ['#ffb020', C.red, C.lime, C.lime].forEach(function (c, i) { el('circle', { cx: 732, cy: 324 + i * 24, r: 8, fill: c }, cp); });
    label(cp, 732, 428, 'PLC', 13, C.ink2);
    // hopper
    var H = el('g', null, M);
    el('path', { d: 'M70 238 L250 238 L218 404 L96 404 Z', fill: 'rgba(154,208,74,.14)', stroke: C.lime, 'stroke-width': 2.5 }, H);
    label(H, 160, 228, 'BULK HOPPER', 14, C.lime);
    var pile = [];
    for (var i = 0; i < 30; i++) { var pg = partShape(H); pg._x = 110 + hash(i, 4) * 96; pg._y = 330 + hash(i, 5) * 62; pg._r = hash(i, 6) * 360; pile.push(pg); }
    // return belt (NG)
    var Rr0 = [520, 250], Rr1 = [236, 352];
    el('line', { x1: Rr0[0], y1: Rr0[1], x2: Rr1[0], y2: Rr1[1], stroke: '#33454b', 'stroke-width': 16, 'stroke-linecap': 'round' }, M);
    var retDash = el('line', { x1: Rr0[0], y1: Rr0[1], x2: Rr1[0], y2: Rr1[1], stroke: '#6b8287', 'stroke-width': 4, 'stroke-dasharray': '10 12' }, M);
    var retHi = el('line', { x1: Rr0[0], y1: Rr0[1], x2: Rr1[0], y2: Rr1[1], stroke: C.red, 'stroke-width': 18, 'stroke-linecap': 'round', opacity: 0 }, M);
    var retLbl = label(M, 420, 318, 'NG RETURN BELT', 13, '#ff9d8f');
    retLbl.setAttribute('transform', 'rotate(-19.7 420 318)');
    // main inclined belt
    var bl = Math.hypot(Bp[0] - A[0], Bp[1] - A[1]), ang = Math.atan2(Bp[1] - A[1], Bp[0] - A[0]);
    var beltHi = el('line', { x1: A[0], y1: A[1], x2: Bp[0], y2: Bp[1], stroke: C.lime, 'stroke-width': 34, 'stroke-linecap': 'round', opacity: 0 }, M);
    el('line', { x1: A[0], y1: A[1], x2: Bp[0], y2: Bp[1], stroke: '#1c2629', 'stroke-width': 26, 'stroke-linecap': 'round' }, M);
    var cleats = el('line', { x1: A[0], y1: A[1], x2: Bp[0], y2: Bp[1], stroke: '#6f878b', 'stroke-width': 22, 'stroke-dasharray': '3 25' }, M);
    var pul = [];
    [A, Bp].forEach(function (p) {
      var g = el('g', null, M); el('circle', { cx: 0, cy: 0, r: 15, fill: '#9fb2b0', stroke: '#2b3a3a', 'stroke-width': 2 }, g);
      el('path', { d: 'M-11 0H11M0 -11V11', stroke: '#2b3a3a', 'stroke-width': 3 }, g); g._p = p; pul.push(g);
    });
    // motor
    var mot = el('g', null, M);
    el('rect', { x: 150, y: 410, width: 70, height: 34, rx: 5, fill: '#3e5157', stroke: '#6a8288' }, mot);
    label(mot, 185, 432, 'MOTOR', 12, '#fff');
    el('line', { x1: 185, y1: 410, x2: 178, y2: 398, stroke: '#6a8288', 'stroke-width': 4 }, mot);
    // selection track (top)
    var sel = el('g', null, M);
    el('rect', { x: 462, y: railY - 7, width: 96, height: 22, rx: 3, fill: '#8a9e9b', stroke: '#2b3a3a' }, sel);
    var key = el('rect', { x: 528, y: railY - 24, width: 10, height: 16, rx: 2, fill: C.gold }, sel);
    label(sel, 510, railY - 32, 'SELECTION TRACK', 12, C.gold);
    // direct vibration rail
    var R = el('g', null, M);
    el('rect', { x: 556, y: railY - 7, width: 204, height: 22, rx: 3, fill: '#8a9e9b', stroke: '#2b3a3a' }, R);
    el('rect', { x: 556, y: railY + 3, width: 204, height: 4, fill: '#55686a' }, R);
    el('rect', { x: 572, y: railY + 18, width: 118, height: 34, rx: 5, fill: '#2c3b41', stroke: '#4e6168' }, R);
    label(R, 631, railY + 40, 'DIRECT VIBRATION', 11, C.ink2);
    var railWaves = el('path', { d: '', fill: 'none', stroke: C.teal, 'stroke-width': 2 }, R);
    el('rect', { x: pickX + 14, y: railY - 36, width: 12, height: 22, rx: 2, fill: '#3d5157' }, R);
    el('rect', { x: pickX + 14, y: railY + 16, width: 12, height: 22, rx: 2, fill: '#3d5157' }, R);
    var beam = el('line', { x1: pickX + 20, y1: railY - 14, x2: pickX + 20, y2: railY + 16, stroke: C.red, 'stroke-width': 3, filter: 'url(#' + id + 'glow)' }, R);
    var NB = 9, bparts = []; for (i = 0; i < NB; i++) bparts.push(partShape(M));
    var NG = 4, ngparts = []; for (i = 0; i < NG; i++) ngparts.push(partShape(M));
    var NQ = 6, pitch = 26, queue = []; for (i = 0; i < NQ; i++) queue.push(partShape(R));
    var carried = partShape(R);
    var head = nozzle(R);
    var halo = el('line', { x1: A[0], y1: A[1] - 18, x2: Bp[0], y2: Bp[1] - 18, stroke: C.lime, 'stroke-width': 10, 'stroke-linecap': 'round', opacity: 0, filter: 'url(#' + id + 'glow)' }, M);
    var O = el('g', null, svg);
    var calls = [
      callout(O, 1, 70, 190, 'Bulk hopper, no packaging', 'r'),
      callout(O, 2, 250, 486, 'Motor-driven belt lifts parts gently', 'r'),
      callout(O, 3, 470, 140, 'Selection track + key', 'r'),
      callout(O, 4, 380, 360, 'NG parts return to hopper', 'r'),
      callout(O, 5, pickX + 20, railY + 74, 'Fibre check · pick ±1 mm', 'l')
    ];
    var rg = ring(O, 600, 96);
    var fp = footprint(svg, id, 850, 140, 260, 12, '');
    var tags = el('g', { opacity: 0 }, O);
    var tagT = label(tags, 300, 120, '', 20, C.lime, 'middle', 800);
    var tagT2 = label(tags, 300, 144, '', 15, C.ink2, 'middle', 700);
    var keyHi = el('rect', { x: 456, y: railY - 30, width: 108, height: 50, rx: 6, fill: 'none', stroke: C.lime, 'stroke-width': 4, opacity: 0 }, O);
    return {
      type: 'belt', svg: svg, M: M, O: O, calls: calls, ring: rg, fp: fp, tags: tags, tagT: tagT, tagT2: tagT2, beltHi: beltHi, keyHi: keyHi, halo: halo, retHi: retHi,
      render: function (t, st) {
        var T = DATA.belt.cycle, tt = t * (st.speed || 1);
        var bv = 58; // px/s belt speed
        cleats.setAttribute('stroke-dashoffset', (-tt * bv).toFixed(1));
        retDash.setAttribute('stroke-dashoffset', (-tt * 30).toFixed(1));
        pul.forEach(function (g) { g.setAttribute('transform', 'translate(' + g._p[0] + ',' + g._p[1] + ') rotate(' + ((tt * bv / 15) * 57.3 % 360).toFixed(1) + ')'); });
        pile.forEach(function (p, i) { setPart(p, p._x + Math.sin(tt * 3 + i) * 0.8, p._y, p._r, 1); });
        var rw = 'M580 ' + (railY + 47); for (var k = 0; k <= 26; k++) rw += 'L' + (580 + k * 4) + ' ' + (railY + 47 - Math.abs(Math.sin(k * 1.1 + tt * 46)) * 5).toFixed(1);
        railWaves.setAttribute('d', rw);
        // belt parts: one arrives at top every T seconds
        var travel = bl / bv, ca = Math.cos(ang), sa = Math.sin(ang), deg = ang * 57.3;
        for (var i = 0; i < NB; i++) {
          var n = Math.floor(tt / T) - i, t0 = n * T, u = (tt - t0) / travel, g = bparts[i];
          if (u < 0 || u > 1.0) { g.setAttribute('opacity', 0); continue; }
          var bad = hash(n, 9) < 0.3, x = A[0] + ca * bl * u, y = A[1] + sa * bl * u - 16;
          setPart(g, x, y, deg + (bad ? 90 : 0), u < 0.05 ? u / 0.05 : 1, bad && u > 0.6 ? '#ffd7a0' : C.part);
        }
        // NG parts riding the return belt
        var rl = Math.hypot(Rr1[0] - Rr0[0], Rr1[1] - Rr0[1]);
        var act = [];
        for (var m = 0; m < 10 && act.length < NG; m++) {
          var n2 = Math.floor(tt / T) - m; if (hash(n2, 9) >= 0.3) continue;
          var dt = tt - (n2 * T + travel);
          if (dt >= 0 && dt < 0.45 + rl / 34) act.push(dt);
        }
        for (i = 0; i < NG; i++) {
          var g2 = ngparts[i];
          if (i >= act.length) { g2.setAttribute('opacity', 0); continue; }
          var d2 = act[i], x2, y2, r2;
          if (d2 < 0.45) { var f = d2 / 0.45; x2 = Bp[0] + 30 * f; y2 = Bp[1] - 16 + (Rr0[1] - Bp[1] + 6) * f * f; r2 = deg + 90 + f * 90; }
          else { var q = (d2 - 0.45) * 34 / rl; x2 = Rr0[0] + (Rr1[0] - Rr0[0]) * q; y2 = Rr0[1] + (Rr1[1] - Rr0[1]) * q - 12; r2 = 160; }
          setPart(g2, x2, y2, r2, 1, '#ffb3a8');
        }
        // pick cycle
        var P = frac(tt / T);
        var down = P < 0.2 ? ease(P / 0.2) : P < 0.3 ? 1 : 1 - ease((P - 0.3) / 0.22);
        var tipY = railY - 4, hy = 150 + (tipY - 150) * down;
        head.setAttribute('transform', 'translate(' + pickX + ',' + hy.toFixed(1) + ')');
        var shift = pitch * ease((P - 0.55) / 0.35);
        for (i = 0; i < NQ; i++) {
          var xq = pickX - i * pitch + shift + Math.sin(tt * 120 + i) * 0.8, vis = 1;
          if (i === 0 && P >= 0.28) vis = 0;
          if (xq < 575) vis = clamp((xq - 562) / 13, 0, 1);
          setPart(queue[i], xq, railY - 1, 0, vis);
        }
        if (P >= 0.28) setPart(carried, pickX, hy + 4, 0, P < 0.6 ? 1 : clamp(1 - (P - 0.6) / 0.15, 0, 1)); else carried.setAttribute('opacity', 0);
        beam.setAttribute('stroke', (P < 0.28 || P > 0.9) ? C.lime : C.red);
        key.setAttribute('y', railY - 24 + Math.sin(tt * 30) * 1.2);
        rg.arc.setAttribute('stroke-dasharray', (P * 289).toFixed(1) + ' 999');
        rg.t.textContent = DATA.belt.cycleLabel;
        return Math.floor(tt / T);
      }
    };
  }

  /* ---------- chapter layer logic ---------- */
  var CH = {
    principle: { title: 'How each feeder works' },
    speed: { title: 'Speed & precision' },
    space: { title: 'Footprint & weight' },
    gentle: { title: 'Gentle handling' },
    change: { title: 'Changeover & cost' },
    verdict: { title: 'Which one fits your line?' }
  };
  var METRICS = {
    principle: { bowl: [['Drive', 'Coil vibration'], ['Orientation', 'Tooled spiral track'], ['Conveying', 'Vibration + air blow']], belt: [['Drive', 'Motor-driven belt'], ['Orientation', 'Selection track + key'], ['Rejects', 'Return belt to hopper']] },
    speed: { bowl: [['Cycle', '0.8 s'], ['Accuracy', '±0.5 mm'], ['Part size', '3×3 – 50×50 mm']], belt: [['Cycle', '1.5 – 2 s'], ['Accuracy', '±1 mm'], ['Part size', '3 – 20 mm cube']], win: 'bowl' },
    space: { bowl: [['Footprint', '1120 × 460 mm'], ['Height', '910 mm'], ['Weight', '190 kg (2 bowls)']], belt: [['Footprint', '850 × 140 mm'], ['Height', '260 mm'], ['Weight', '12 kg']], win: 'belt' },
    gentle: { bowl: [['Handling', 'Continuous vibration'], ['Risk', 'Part-on-part friction'], ['Best for', 'Robust, simple parts']], belt: [['Handling', 'Gentle belt transport'], ['Noise', 'Quieter belt drive'], ['Best for', 'Connectors, buzzers, ports']], win: 'belt' },
    change: { bowl: [['Tooling', 'Track per part no.'], ['Changeover', 'Re-tool the bowl'], ['Control', 'PLC · IO / standalone']], belt: [['Tooling', 'Re-set belt, key, delay'], ['Changeover', '12 kg quick swap'], ['Control', 'Mitsubishi PLC · IO']], win: 'belt' },
    verdict: { bowl: [['Choose it for', 'Highest speed'], ['Parts', 'Robust, up to 50 mm'], ['Ageing test', '48 h, no fault']], belt: [['Choose it for', 'Compact & gentle'], ['Parts', 'Delicate odd-form'], ['Ageing test', '48 h, no fault']] }
  };
  var TAGS = {
    gentle: { bowl: ['FRICTION & SCRATCH RISK', 'parts rub on parts, all cycle long'], belt: ['GENTLE TRANSPORT', 'no part-on-part grinding'] },
    change: { bowl: ['ONE TRACK = ONE PART', 'new part number → new tooling'], belt: ['RE-SET, NOT RE-TOOLED', 'belt speed · key · vibration delay'] }
  };

  function applyChapter(m, st, t) {
    var ch = st.chapter || 'principle';
    var k = st.chapterT == null ? 1 : clamp(st.chapterT / 0.6, 0, 1);
    var isSpace = ch === 'space';
    m.M.setAttribute('opacity', (isSpace ? 1 - 0.9 * k : 1).toFixed(2));
    m.fp.g.setAttribute('opacity', (isSpace ? k : 0).toFixed(2));
    if (isSpace) m.fp.bar.setAttribute('width', Math.max(0.001, m.fp.bw * ease((st.chapterT || 9) / 1.6)).toFixed(1));
    // callouts
    var step = st.step == null ? 99 : st.step;
    m.calls.forEach(function (c, i) {
      var on = ch === 'principle' && i < step;
      c.setAttribute('opacity', on ? (st.step != null && i === step - 1 ? 1 : (st.step != null ? 0.85 : 1)) : 0);
    });
    m.ring.g.setAttribute('opacity', ch === 'speed' ? 1 : 0);
    var tg = TAGS[ch] && TAGS[ch][m.type];
    m.tags.setAttribute('opacity', tg ? 1 : 0);
    if (tg) { m.tagT.textContent = tg[0]; m.tagT2.textContent = tg[1]; }
    if (m.trackHi) m.trackHi.setAttribute('opacity', ch === 'change' ? 0.55 + 0.25 * Math.sin(t * 4) : 0);
    if (m.beltHi) {
      m.beltHi.setAttribute('opacity', ch === 'change' ? 0.35 : 0);
      m.keyHi.setAttribute('opacity', ch === 'change' ? 0.9 : 0);
      m.halo.setAttribute('opacity', ch === 'gentle' ? 0.45 + 0.2 * Math.sin(t * 3) : 0);
    }
  }

  /* ---------- public API ---------- */
  function FeederDuel(root, opts) {
    opts = opts || {};
    this.root = root;
    var self = this;
    this.st = { chapter: 'principle', speed: 1 };
    this.mech = {};
    ['bowl', 'belt'].forEach(function (k) {
      var host = root.querySelector('[data-fd="' + k + '"]');
      if (!host) return;
      var svg = el('svg', { viewBox: '0 0 800 560', role: 'img', 'aria-label': DATA[k].name + ' working principle animation', preserveAspectRatio: 'xMidYMid meet' });
      host.appendChild(svg);
      self.mech[k] = k === 'bowl' ? buildBowl(svg) : buildBelt(svg);
    });
  }
  FeederDuel.prototype.render = function (t, st) {
    st = st || this.st;
    var out = {};
    for (var k in this.mech) { var m = this.mech[k]; out[k] = m.render(t, st); applyChapter(m, st, t); }
    // metric strips (HTML)
    var met = METRICS[st.chapter] || METRICS.principle;
    var root = this.root;
    if (this._lastCh !== st.chapter) {
      this._lastCh = st.chapter;
      ['bowl', 'belt'].forEach(function (k) {
        var box = root.querySelector('[data-fd-metrics="' + k + '"]');
        if (!box) return;
        var h = '';
        met[k].forEach(function (r) { h += '<div class="fd-m"><span>' + r[0] + '</span><b>' + r[1] + '</b></div>'; });
        box.innerHTML = h;
        var card = root.querySelector('[data-fd-card="' + k + '"]');
        if (card) card.classList.toggle('fd-win', met.win === k);
      });
      var tl = root.querySelector('[data-fd-title]'); if (tl) tl.textContent = (CH[st.chapter] || CH.principle).title;
    }
    ['bowl', 'belt'].forEach(function (k) {
      var c = root.querySelector('[data-fd-count="' + k + '"]');
      if (c) c.textContent = out[k] - (st.count0 ? st.count0[k] : 0);
    });
    return out;
  };
  FeederDuel.DATA = DATA; FeederDuel.CH = CH; FeederDuel.METRICS = METRICS;
  G.FeederDuel = FeederDuel;
})(window);
