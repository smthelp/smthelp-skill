/* AxialDuel — side-by-side working-principle animation
   Manual cut-and-form of taped axial parts  vs  SAF1001 axial tape feeder (Southern Machinery)
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
  function lerp(a, b, k) { return a + (b - a) * k; }
  function hash(n) { var x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }

  var C = {
    bg: '#0c1c1a', grid: 'rgba(120,200,185,.07)', teal: '#2fc1aa', teal2: '#0c665c', gold: '#f2b84b', lime: '#9ad04a',
    red: '#ff6b5a', ink2: '#9fb9b4', paper: '#e8dcc0', paperEdge: '#b9a57a', lead: '#c9d3d6', body: '#d9b77a',
    band1: '#8a4b2a', band2: '#2b2b2b', band3: '#c0392b', steel: '#8aa3a5', dark: '#33464c'
  };
  var T = 0.8;                 // SAF1001 published cycle time, s per piece
  var PICK = 600;              // pick / cut station x
  var TY0 = 200, TY1 = 372;    // paper strips (top view)
  var MID = (TY0 + TY1) / 2;

  function defs(svg, id) {
    var d = el('defs', null, svg);
    var p = el('pattern', { id: id + 'g', width: 40, height: 40, patternUnits: 'userSpaceOnUse' }, d);
    el('path', { d: 'M40 0H0V40', fill: 'none', stroke: C.grid, 'stroke-width': 1 }, p);
    var gl = el('filter', { id: id + 'glow', x: '-50%', y: '-50%', width: '200%', height: '200%' }, d);
    el('feGaussianBlur', { stdDeviation: 4, result: 'b' }, gl);
    var m = el('feMerge', null, gl); el('feMergeNode', { in: 'b' }, m); el('feMergeNode', { in: 'SourceGraphic' }, m);
  }
  function bg(svg, id) {
    el('rect', { width: 800, height: 560, fill: C.bg }, svg);
    el('rect', { width: 800, height: 560, fill: 'url(#' + id + 'g)' }, svg);
  }
  function label(parent, x, y, txt, size, fill, anchor, weight) {
    var t = el('text', { x: x, y: y, 'text-anchor': anchor || 'middle', 'font-size': size || 14, 'font-weight': weight || 700, fill: fill || C.ink2, 'font-family': 'Arial', 'letter-spacing': '.06em' }, parent);
    t.textContent = txt; return t;
  }
  function callout(parent, n, x, y, txt, side) {
    var g = el('g', { opacity: 0 }, parent);
    el('circle', { cx: x, cy: y, r: 17, fill: C.gold, stroke: '#fff', 'stroke-width': 2 }, g);
    var t = el('text', { x: x, y: y + 6, 'text-anchor': 'middle', 'font-size': 18, 'font-weight': 800, fill: '#10201e', 'font-family': 'Arial' }, g);
    t.textContent = n;
    var tt = el('text', { x: side === 'l' ? x - 24 : x + 24, y: y + 6, 'text-anchor': side === 'l' ? 'end' : 'start', 'font-size': 19, 'font-weight': 700, fill: '#fff', 'font-family': 'Arial', 'paint-order': 'stroke', stroke: C.bg, 'stroke-width': 5 }, g);
    tt.textContent = txt;
    return g;
  }
  function statusLamp(parent, x, y, id) {
    var g = el('g', null, parent);
    el('rect', { x: x, y: y, width: 250, height: 36, rx: 18, fill: 'rgba(0,0,0,.45)', stroke: 'rgba(255,255,255,.15)' }, g);
    var dot = el('circle', { cx: x + 20, cy: y + 18, r: 8, fill: C.lime, filter: 'url(#' + id + 'glow)' }, g);
    var t = el('text', { x: x + 38, y: y + 24, 'font-size': 15, 'font-weight': 800, fill: '#fff', 'font-family': 'Arial', 'letter-spacing': '.08em' }, g);
    return { dot: dot, t: t };
  }
  function ring(parent, x, y) {
    var g = el('g', { opacity: 0 }, parent);
    el('circle', { cx: x, cy: y, r: 46, fill: 'rgba(12,28,26,.75)', stroke: 'rgba(255,255,255,.15)', 'stroke-width': 6 }, g);
    var arc = el('circle', { cx: x, cy: y, r: 46, fill: 'none', stroke: C.gold, 'stroke-width': 6, 'stroke-linecap': 'round', transform: 'rotate(-90 ' + x + ' ' + y + ')', 'stroke-dasharray': '0 999' }, g);
    label(g, x, y + 4, '0.8 s', 22, '#fff', 'middle', 800);
    label(g, x, y + 22, 'PER PIECE', 11, C.ink2, 'middle', 700);
    return { g: g, arc: arc };
  }
  function head(parent) {
    var g = el('g', null, parent);
    el('rect', { x: -30, y: -150, width: 60, height: 66, rx: 6, fill: C.dark, stroke: '#5f7a80' }, g);
    el('rect', { x: -9, y: -84, width: 18, height: 56, fill: C.steel }, g);
    el('path', { d: 'M-22 -28 h44 l-8 18 h-28 Z', fill: C.gold }, g);
    label(g, 0, -110, 'HEAD', 13, C.ink2, 'middle', 700);
    return g;
  }
  /* axial part in top view: vertical, leads to both strips (len = half lead length) */
  function axialTop(parent) {
    var g = el('g', null, parent);
    var l = el('line', { x1: 0, y1: -(MID - TY0) - 4, x2: 0, y2: (TY1 - MID) + 4, stroke: C.lead, 'stroke-width': 3 }, g);
    var b = el('g', null, g);
    el('rect', { x: -9, y: -26, width: 18, height: 52, rx: 8, fill: C.body, stroke: '#7b6640', 'stroke-width': 1.2 }, b);
    el('rect', { x: -9, y: -16, width: 18, height: 5, fill: C.band1 }, b);
    el('rect', { x: -9, y: -6, width: 18, height: 5, fill: C.band2 }, b);
    el('rect', { x: -9, y: 4, width: 18, height: 5, fill: C.band3 }, b);
    g._l = l; return g;
  }
  function setTop(g, x, y, op, leadHalf) {
    g.setAttribute('transform', 'translate(' + x.toFixed(2) + ',' + y.toFixed(2) + ')');
    g.setAttribute('opacity', op.toFixed(3));
    var h = leadHalf == null ? (MID - TY0) + 4 : leadHalf;
    g._l.setAttribute('y1', (-h).toFixed(1)); g._l.setAttribute('y2', h.toFixed(1));
  }
  /* axial part in side view (body horizontal), legs bend from straight (k=0) to U (k=1); span = pin spacing */
  function axialSide(parent, scale) {
    var g = el('g', null, parent);
    var p = el('path', { fill: 'none', stroke: C.lead, 'stroke-width': 3 / (scale || 1), 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
    var b = el('g', null, g);
    el('rect', { x: -26, y: -9, width: 52, height: 18, rx: 8, fill: C.body, stroke: '#7b6640', 'stroke-width': 1.2 }, b);
    el('rect', { x: -16, y: -9, width: 5, height: 18, fill: C.band1 }, b);
    el('rect', { x: -6, y: -9, width: 5, height: 18, fill: C.band2 }, b);
    el('rect', { x: 4, y: -9, width: 5, height: 18, fill: C.band3 }, b);
    g._p = p; return g;
  }
  function setSide(g, x, y, k, span, len, op, rot) {
    span = span || 80; len = len || 70;
    var a = span / 2, s = 26, flat = a - s, leg = len - flat;
    // straight: lead goes outward horizontally (length len); formed: outward flat to a, then down leg
    var ang = (Math.PI / 2) * clamp(k, 0, 1);
    var ex = a + Math.cos(ang) * leg, ey = Math.sin(ang) * leg;
    var d = 'M' + (-ex).toFixed(1) + ' ' + ey.toFixed(1) + ' L' + (-a) + ' 0 L' + a + ' 0 L' + ex.toFixed(1) + ' ' + ey.toFixed(1);
    if (flat < 0) d = 'M' + (-ex).toFixed(1) + ' ' + ey.toFixed(1) + ' L' + ex.toFixed(1) + ' ' + ey.toFixed(1);
    g._p.setAttribute('d', d);
    g.setAttribute('transform', 'translate(' + x.toFixed(1) + ',' + y.toFixed(1) + ')' + (rot ? ' rotate(' + rot.toFixed(1) + ')' : ''));
    g.setAttribute('opacity', op == null ? 1 : op.toFixed(3));
  }
  function strip(parent, x0, x1, y, holes, P) {
    var g = el('g', null, parent);
    el('rect', { x: x0, y: y - 9, width: x1 - x0, height: 18, fill: C.paper, stroke: C.paperEdge, 'stroke-width': 1.5 }, g);
    var hs = el('g', null, g);
    if (holes) for (var x = x0 + 10; x < x1 + P; x += P) el('circle', { cx: x, cy: y, r: 3.5, fill: '#5a4a2c' }, hs);
    return { g: g, holes: hs };
  }

  /* ================= RIGHT: SAF1001 ================= */
  var P = 40, NV = 12, X0 = PICK - (NV - 1) * P;  // pitch (schematic), visible parts, first visible part x
  function buildSAF(svg) {
    var id = 'saf' + Math.floor(Math.random() * 1e6); svg._id = id;
    defs(svg, id); bg(svg, id);
    var M = el('g', null, svg); M._id = id;
    // frame / tray
    el('rect', { x: 40, y: 168, width: 660, height: 236, rx: 10, fill: 'rgba(47,193,170,.05)', stroke: 'rgba(47,193,170,.35)', 'stroke-width': 2, 'stroke-dasharray': '8 6' }, M);
    label(M, 60, 160, 'HORIZONTAL TAPE TRAY', 13, C.teal, 'start');
    // strips (move with tape) — clip window
    var clipId = id + 'c';
    var cp = el('clipPath', { id: clipId }, el('defs', null, svg));
    el('rect', { x: 40, y: 150, width: 640, height: 260 }, cp);
    var TG = el('g', { 'clip-path': 'url(#' + clipId + ')' }, M);
    var tape = el('g', null, TG);
    var s0 = strip(tape, -P * 2, 760, TY0, true, P), s1 = strip(tape, -P * 2, 760, TY1, true, P);
    // stubs left on the strips after the cut
    var stubs = [];
    for (var i = 0; i < 4; i++) {
      var sg = el('g', null, TG);
      el('line', { x1: 0, y1: TY0 - 4, x2: 0, y2: TY0 + 18, stroke: C.lead, 'stroke-width': 3 }, sg);
      el('line', { x1: 0, y1: TY1 - 18, x2: 0, y2: TY1 + 4, stroke: C.lead, 'stroke-width': 3 }, sg);
      stubs.push(sg);
    }
    var parts = []; for (i = 0; i < NV + 1; i++) parts.push(axialTop(TG));
    // waste tape: chopped pieces dropping vertically at front end
    var waste = [];
    for (i = 0; i < 3; i++) {
      var wg = el('g', null, M);
      el('rect', { x: -16, y: -9, width: 32, height: 18, fill: C.paper, stroke: C.paperEdge }, wg);
      waste.push(wg);
    }
    el('rect', { x: 682, y: 170, width: 18, height: 232, fill: '#2a3a40' }, M);
    label(M, 740, 470, 'WASTE TAPE', 12, C.ink2); label(M, 740, 486, 'FRONT DROP', 12, C.ink2);
    // ratchet wheel engaging the bottom strip
    var RX = 220, RY = TY1 + 58;
    var wheel = el('g', null, M);
    var teeth = 'M'; for (i = 0; i < 24; i++) { var a0 = i / 24 * Math.PI * 2, a1 = (i + 0.5) / 24 * Math.PI * 2; teeth += (Math.cos(a0) * 46).toFixed(1) + ' ' + (Math.sin(a0) * 46).toFixed(1) + ' L' + (Math.cos(a1) * 36).toFixed(1) + ' ' + (Math.sin(a1) * 36).toFixed(1) + ' L'; }
    teeth = teeth.slice(0, -2) + 'Z';
    el('path', { d: teeth, fill: '#5d7176', stroke: '#a9bcbf', 'stroke-width': 1.5 }, wheel);
    el('circle', { r: 10, fill: '#1f2c30', stroke: '#a9bcbf' }, wheel);
    // main cylinder + pawl
    el('rect', { x: 60, y: RY + 30, width: 90, height: 26, rx: 5, fill: '#3e5a66', stroke: '#7fa0aa' }, M);
    var rod = el('rect', { x: 150, y: RY + 38, width: 40, height: 10, fill: C.steel }, M);
    var pawl = el('path', { d: 'M0 0 l30 -16 l6 8 l-28 14 Z', fill: C.gold }, M);
    label(M, 105, RY + 78, 'MAIN CYLINDER', 11, C.ink2);
    label(M, RX, RY + 66, 'RATCHET', 11, C.ink2);
    // anti-reversal pawl
    el('path', { d: 'M' + (RX + 70) + ' ' + (RY - 6) + ' l-26 -14 l4 -6 l28 12 Z', fill: '#c48f2c' }, M);
    // cutter blades (top + bottom, close to strips) + fibre
    var bladeT = el('rect', { x: PICK - 14, y: TY0 + 14, width: 28, height: 10, fill: '#dfe7ea', stroke: '#6a7c80' }, M);
    var bladeB = el('rect', { x: PICK - 14, y: TY1 - 24, width: 28, height: 10, fill: '#dfe7ea', stroke: '#6a7c80' }, M);
    var fib = el('g', null, M);
    el('rect', { x: PICK - 70, y: MID - 8, width: 22, height: 16, rx: 3, fill: '#2b3d42', stroke: C.teal }, fib);
    var beam = el('line', { x1: PICK - 48, y1: MID, x2: PICK - 12, y2: MID, stroke: '#ff3b30', 'stroke-width': 3, filter: 'url(#' + id + 'glow)' }, fib);
    var flash = el('g', { opacity: 0 }, M);
    [TY0 + 19, TY1 - 19].forEach(function (y) { el('path', { d: 'M' + (PICK - 22) + ' ' + y + ' l44 0 M' + PICK + ' ' + (y - 12) + ' l0 24', stroke: '#fff', 'stroke-width': 3, 'stroke-linecap': 'round', filter: 'url(#' + id + 'glow)' }, flash); });
    // the part being formed / picked (side view, at pick point) and head
    var formed = axialSide(M);
    var hd = head(M);
    // inset: side view of cut + U-form with male/female die
    var IN = el('g', null, M);
    el('rect', { x: 290, y: 14, width: 300, height: 146, rx: 10, fill: 'rgba(0,0,0,.55)', stroke: 'rgba(255,255,255,.18)' }, IN);
    label(IN, 302, 152, 'SIDE VIEW · CUT + U-FORM', 12, C.gold, 'start', 800);
    var fem = el('g', null, IN);
    el('rect', { x: 388, y: 98, width: 104, height: 40, rx: 3, fill: '#2f6fd1', opacity: 0.85 }, fem);
    var male = el('g', null, IN);
    el('rect', { x: 376, y: -40, width: 14, height: 40, fill: '#5b8fe6' }, male);
    el('rect', { x: 490, y: -40, width: 14, height: 40, fill: '#5b8fe6' }, male);
    el('rect', { x: 376, y: -48, width: 128, height: 10, fill: '#5b8fe6' }, male);
    var ip = axialSide(IN);
    var O = el('g', null, svg); O._id = id;
    var lamp = statusLamp(O, 30, 24, id);
    var calls = [
      callout(O, 1, RX + 60, RY + 18, 'Ratchet indexing', 'r'),
      callout(O, 2, PICK - 60, MID - 44, 'Fibre presence check', 'l'),
      callout(O, 3, PICK - 40, TY0 - 26, 'Cut + U-form', 'l'),
      callout(O, 4, PICK + 46, 300, 'To the head', 'r'),
      callout(O, 5, 690, 432, 'Waste tape drops', 'l')
    ];
    var rg = ring(O, 724, 122);
    // tapes & parts overlay
    var mat = el('g', { opacity: 0 }, svg);
    label(mat, 400, 66, 'EIA-296 BANDOLEER TAPE', 20, '#fff', 'middle', 800);
    var widths = [['26 mm', 'standard'], ['52 mm', 'standard'], ['35 · 64 · 92 mm', 'custom']];
    widths.forEach(function (w, k) {
      var x = 110 + k * 200;
      el('rect', { x: x, y: 100, width: 180, height: 70, rx: 10, fill: k < 2 ? 'rgba(47,193,170,.14)' : 'rgba(242,184,75,.14)', stroke: k < 2 ? C.teal : C.gold, 'stroke-width': 2 }, mat);
      label(mat, x + 90, 132, w[0], 20, '#fff', 'middle', 800); label(mat, x + 90, 156, w[1].toUpperCase(), 12, C.ink2);
    });
    var kinds = ['RESISTOR', 'DIODE', 'INDUCTOR', 'CAPACITOR', 'JUMPER'];
    kinds.forEach(function (n, k) {
      var x = 120 + k * 140, g = axialSide(mat); setSide(g, x, 250, 0, 60, 46, 1);
      label(mat, x, 290, n, 12, C.ink2);
    });
    label(mat, 400, 360, 'Body 3 × 3 – 6 × 20 mm', 22, C.lime, 'middle', 800);
    label(mat, 400, 396, 'Lead wire 0.4 – 1.0 mm · paper > 0.2 mm', 18, '#fff', 'middle', 700);
    label(mat, 400, 440, 'K-lead forming variant on request', 16, C.gold, 'middle', 700);
    // integration overlay
    var integ = el('g', { opacity: 0 }, svg);
    el('rect', { x: 120, y: 120, width: 560, height: 300, rx: 14, fill: 'rgba(6,16,15,.88)', stroke: C.teal, 'stroke-width': 2 }, integ);
    label(integ, 400, 156, '8-CORE Ø16 mm AVIATION PLUG · IO OR STANDALONE', 15, C.teal, 'middle', 800);
    var sig = [['HOST → FEEDER', 'Request material'], ['FEEDER → HOST', 'Material present'], ['FEEDER → HOST', 'Cut complete'], ['FEEDER → HOST', 'Tape empty alarm']];
    var sigDots = [];
    sig.forEach(function (s, k) {
      var y = 200 + k * 44;
      label(integ, 160, y + 6, s[0], 13, C.ink2, 'start', 700);
      label(integ, 330, y + 6, s[1], 18, '#fff', 'start', 800);
      sigDots.push(el('circle', { cx: 630, cy: y, r: 9, fill: C.lime }, integ));
    });
    label(integ, 400, 396, '24 V · 1 A avg / 3 A peak · 0.4 – 0.6 MPa · 730 × 95 × 212 mm · 8 kg', 14, C.ink2, 'middle', 700);
    var tags = el('g', { opacity: 0 }, svg);
    var tagT = label(tags, 400, 530, '', 18, C.lime, 'middle', 800), tagT2 = label(tags, 400, 552, '', 13, C.ink2, 'middle', 700);

    return {
      type: 'saf', M: M, O: O, calls: calls, ring: rg, tags: tags, tagT: tagT, tagT2: tagT2, mat: mat, integ: integ, inset: IN,
      render: function (t) {
        var n = Math.floor(t / T), p = frac(t / T);
        // phases: 0-.32 index, .32-.42 sense, .42-.62 cut+form, .62-1 pick
        var ix = ease(p / 0.32), shift = (n + ix) * P;
        tape.setAttribute('transform', 'translate(' + (shift % P).toFixed(2) + ',0)');
        // ratchet rotates one tooth per index
        wheel.setAttribute('transform', 'translate(' + RX + ',' + RY + ') rotate(' + ((n + ix) * 15).toFixed(2) + ')');
        var stroke = p < 0.32 ? ease(p / 0.32) : 1 - ease((p - 0.32) / 0.5);
        rod.setAttribute('width', (40 + 40 * stroke).toFixed(1));
        pawl.setAttribute('transform', 'translate(' + (186 + 40 * stroke).toFixed(1) + ',' + (RY + 40) + ')');
        // parts on tape: slot j at x = X0 + j*P + offset; the slot at PICK holds the part being processed
        var off = ix * P;
        for (var j = 0; j <= NV; j++) {
          var x = X0 - P + j * P + off, g = parts[j];
          var atPick = Math.abs(x - PICK) < 1 && p >= 0.32;
          if (x > PICK + 0.5 || atPick) { g.setAttribute('opacity', 0); continue; }
          setTop(g, x, MID, 1);
          if (Math.abs(x - PICK) < 0.5) g.setAttribute('opacity', 1);
        }
        // stubs: positions right of pick for already-cut slots
        for (j = 0; j < stubs.length; j++) {
          var sx = PICK + (j + (p >= 0.42 ? 0 : 1)) * P + off - (p >= 0.42 ? 0 : 0);
          if (p < 0.32) sx = PICK + (j + 1) * P - P + off;
          stubs[j].setAttribute('transform', 'translate(' + sx.toFixed(1) + ',0)');
          stubs[j].setAttribute('opacity', sx > 682 || (j === 0 && p >= 0.32 && p < 0.42) ? 0 : 1);
        }
        // waste pieces falling
        for (j = 0; j < waste.length; j++) {
          var ph = frac(t / T / 1.0 + j / 3), y = 300 + ph * 220;
          waste[j].setAttribute('transform', 'translate(' + (740 + (j - 1) * 6) + ',' + y.toFixed(1) + ') rotate(' + (ph * 140 + j * 40).toFixed(0) + ')');
          waste[j].setAttribute('opacity', (1 - ph).toFixed(2));
        }
        // sensing + cut flash
        var sense = p >= 0.32 && p < 0.62;
        beam.setAttribute('opacity', sense ? 1 : 0.25);
        flash.setAttribute('opacity', p >= 0.42 && p < 0.5 ? 1 : 0);
        var bl = p >= 0.4 && p < 0.52 ? 1 : 0;
        bladeT.setAttribute('y', (TY0 + 14 - 6 * bl).toFixed(1)); bladeB.setAttribute('y', (TY1 - 24 + 6 * bl).toFixed(1));
        // formed part at pick (side view rotated 90 to match top view orientation) then picked
        var fk = ease((p - 0.44) / 0.16);
        var hy = 150, partY = MID, pOp = 0;
        if (p >= 0.32) {
          pOp = 1;
          if (p >= 0.62) {
            var q = (p - 0.62) / 0.38, down = q < 0.35 ? ease(q / 0.35) : q < 0.45 ? 1 : 1 - ease((q - 0.45) / 0.5);
            hy = lerp(150, MID - 14, down);
            if (q >= 0.45) { partY = hy + 14; pOp = q > 0.85 ? clamp(1 - (q - 0.85) / 0.15, 0, 1) : 1; }
          }
        }
        if (p >= 0.32) setSide(formed, PICK, partY, fk, 70, p < 0.42 ? (MID - TY0) + 4 : 44, pOp, 90); else formed.setAttribute('opacity', 0);
        hd.setAttribute('transform', 'translate(' + PICK + ',' + hy.toFixed(1) + ') ');
        hd.setAttribute('transform', 'translate(' + (PICK + 0) + ',' + hy.toFixed(1) + ')');
        // inset
        var md = p < 0.42 ? 0 : p < 0.6 ? ease((p - 0.42) / 0.16) : 1 - ease((p - 0.66) / 0.2);
        male.setAttribute('transform', 'translate(0,' + (64 + 52 * md).toFixed(1) + ')');
        var ik = ease((p - 0.46) / 0.14);
        if (p < 0.32) ip.setAttribute('opacity', 0);
        else setSide(ip, 440, 88, ik, 116, p < 0.44 ? 78 : 60, p > 0.9 ? clamp((1 - p) / 0.1, 0, 1) : 1);
        lamp.t.textContent = p < 0.32 ? 'INDEXING · RATCHET' : p < 0.42 ? 'PART PRESENT · FIBRE' : p < 0.62 ? 'CUT + U-FORM' : 'HEAD PICKS';
        lamp.dot.setAttribute('fill', C.lime);
        for (j = 0; j < sigDots.length; j++) {
          var on = [p < 0.1, p >= 0.32 && p < 0.62, p >= 0.6 && p < 0.75, false][j];
          sigDots[j].setAttribute('fill', on ? C.lime : 'rgba(255,255,255,.18)');
        }
        rg.arc.setAttribute('stroke-dasharray', (p * 289).toFixed(1) + ' 999');
        return n + (p >= 0.8 ? 1 : 0);
      }
    };
  }

  /* ================= LEFT: manual cut-and-form ================= */
  var TM = 3.4, WAITN = 8, WAIT = 3.0;   // illustrative: seconds per hand-formed part, parts per batch, pause (reel / rework)
  function buildMan(svg) {
    var id = 'man' + Math.floor(Math.random() * 1e6); svg._id = id;
    defs(svg, id); bg(svg, id);
    var M = el('g', null, svg); M._id = id;
    // bench
    el('rect', { x: 30, y: 404, width: 470, height: 16, rx: 4, fill: '#3a4a52' }, M);
    label(M, 50, 446, 'OPERATOR BENCH', 13, C.ink2, 'start');
    // tape segment on bench (static, parts get removed)
    var TB = el('g', null, M);
    strip(TB, 40, 300, 250, true, 30); strip(TB, 40, 300, 380, true, 30);
    var bparts = [];
    for (var i = 0; i < 8; i++) {
      var g = el('g', null, TB);
      el('line', { x1: 0, y1: 246, x2: 0, y2: 384, stroke: C.lead, 'stroke-width': 3 }, g);
      el('rect', { x: -8, y: 291, width: 16, height: 48, rx: 7, fill: C.body, stroke: '#7b6640' }, g);
      el('rect', { x: -8, y: 302, width: 16, height: 5, fill: C.band1 }, g);
      el('rect', { x: -8, y: 312, width: 16, height: 5, fill: C.band2 }, g);
      g.setAttribute('transform', 'translate(' + (280 - i * 30) + ',0)');
      bparts.push(g);
    }
    // forming jig
    el('rect', { x: 330, y: 360, width: 120, height: 40, rx: 4, fill: '#2f4f8f', opacity: 0.8 }, M);
    label(M, 390, 386, 'JIG', 13, '#d8e4ff', 'middle', 800);
    // hand with cutters
    var hand = el('g', null, M);
    el('rect', { x: -26, y: -16, width: 52, height: 34, rx: 14, fill: '#e3b48f', stroke: '#9a6b4a', 'stroke-width': 2 }, hand);
    for (i = 0; i < 4; i++) el('rect', { x: -22 + i * 12, y: -36, width: 10, height: 24, rx: 5, fill: '#e3b48f', stroke: '#9a6b4a', 'stroke-width': 1.5 }, hand);
    el('rect', { x: -34, y: 16, width: 68, height: 30, rx: 6, fill: '#4f6a8a' }, hand);
    var cut = el('g', { opacity: 0 }, M);
    el('path', { d: 'M-12 -12 L12 12 M12 -12 L-12 12', stroke: '#fff', 'stroke-width': 3, 'stroke-linecap': 'round', filter: 'url(#' + id + 'glow)' }, cut);
    var carried = axialSide(M);
    // pick point (no positive location)
    el('rect', { x: PICK - 50, y: 300, width: 100, height: 10, rx: 3, fill: '#8a9e9b' }, M);
    var q = label(M, PICK + 76, 312, '?', 30, '#ff9d8f', 'middle', 900);
    var hd = head(M);
    var O = el('g', null, svg); O._id = id;
    var lamp = statusLamp(O, 30, 24, id);
    var warn = el('g', { opacity: 0 }, O);
    el('rect', { x: 250, y: 80, width: 300, height: 44, rx: 10, fill: 'rgba(255,107,90,.18)', stroke: C.red, 'stroke-width': 2 }, warn);
    var warnT = label(warn, 400, 109, 'HOST WAITING FOR OPERATOR', 16, '#ffd0c8', 'middle', 800);
    var calls = [
      callout(O, 1, 160, 200, 'Cut off the tape by hand', 'r'),
      callout(O, 2, 390, 460, 'Leads bent in a jig', 'r'),
      callout(O, 3, PICK + 60, 250, 'Handed to the machine', 'l')
    ];
    var rg = ring(O, 380, 90);
    // tapes & parts overlay (left)
    var mat = el('g', { opacity: 0 }, svg);
    label(mat, 400, 66, 'SAME TAPED PARTS YOU CUT BY HAND TODAY', 18, '#fff', 'middle', 800);
    var spans = [64, 72, 58, 80, 68];
    spans.forEach(function (s, k) {
      var x = 120 + k * 140, g = axialSide(mat); setSide(g, x, 230, 1, s, 50, 1);
      label(mat, x, 330, (k === 3 ? 'TOO WIDE' : k === 2 ? 'TOO NARROW' : 'BY HAND'), 12, k === 2 || k === 3 ? '#ff9d8f' : C.ink2);
    });
    label(mat, 400, 400, 'Hand-bent pin spacing varies part to part', 20, '#ffb3a8', 'middle', 800);
    label(mat, 400, 436, 'Same resistors, diodes, inductors and jumpers', 16, C.ink2, 'middle', 700);
    var tags = el('g', { opacity: 0 }, svg);
    var tagT = label(tags, 400, 530, '', 18, C.red, 'middle', 800), tagT2 = label(tags, 400, 552, '', 13, C.ink2, 'middle', 700);

    return {
      type: 'man', M: M, O: O, calls: calls, ring: rg, tags: tags, tagT: tagT, tagT2: tagT2, mat: mat, warn: warn,
      render: function (t) {
        var TP = WAITN * TM + WAIT, cyc = Math.floor(t / TP), lt = t - cyc * TP;
        var waiting = lt >= WAITN * TM, n = waiting ? WAITN : Math.floor(lt / TM), p = waiting ? 0 : frac(lt / TM);
        var done = cyc * WAITN + n;
        // bench parts: remaining in this batch (8 slots, use the first WAITN)
        for (var i = 0; i < bparts.length; i++) { var vis = waiting ? (lt - WAITN * TM > 2.2) : (i > n || (i === n && p < 0.12)); bparts[i].setAttribute('opacity', vis ? 1 : 0); }
        var bx = 280 - n * 30;
        // phases: .0-.18 reach + cut, .18-.5 bend in jig, .5-.72 carry to pick, .72-1 head picks
        var hx = 120, hy = 470, cOn = 0, k = 0, cx = bx, cy = 315, cOp = 0, hdY = 150, span = 60 + (hash(done) - 0.5) * 22;
        if (!waiting) {
          if (p < 0.18) { var a = ease(p / 0.12); hx = lerp(120, bx, a); hy = lerp(470, 340, a); cOn = p > 0.1 ? 1 : 0; }
          else if (p < 0.5) { var b = ease((p - 0.18) / 0.12); hx = lerp(bx, 390, b); hy = lerp(340, 300, b); cOp = 1; cx = lerp(bx, 390, b); cy = lerp(315, 352, b); k = ease((p - 0.3) / 0.18); }
          else if (p < 0.72) { var c = ease((p - 0.5) / 0.2); hx = lerp(390, PICK, c); hy = lerp(300, 330, c); cOp = 1; k = 1; cx = hx; cy = lerp(352, 286, c); }
          else {
            var qq = (p - 0.72) / 0.28, dn = qq < 0.35 ? ease(qq / 0.35) : qq < 0.45 ? 1 : 1 - ease((qq - 0.45) / 0.5);
            hdY = lerp(150, 268, dn); k = 1; cOp = 1; cx = PICK; cy = qq >= 0.45 ? hdY + 18 : 286;
            hx = lerp(PICK, 120, ease(qq / 0.4)); hy = lerp(330, 470, ease(qq / 0.4));
            if (qq > 0.85) cOp = clamp(1 - (qq - 0.85) / 0.15, 0, 1);
          }
        } else {
          var w = lt - WAITN * TM; hx = lerp(120, 170, Math.sin(w * 2) * 0.5 + 0.5); hy = 470;
        }
        if (cOp > 0) setSide(carried, cx, cy, k, span, 60, cOp); else carried.setAttribute('opacity', 0);
        hand.setAttribute('transform', 'translate(' + hx.toFixed(1) + ',' + hy.toFixed(1) + ')');
        cut.setAttribute('transform', 'translate(' + bx + ',260)'); cut.setAttribute('opacity', cOn);
        hd.setAttribute('transform', 'translate(' + PICK + ',' + hdY.toFixed(1) + ')');
        var idle = waiting || p < 0.72;
        lamp.t.textContent = waiting ? 'WAITING · NEW TAPE STRIP' : p < 0.18 ? 'CUTTING BY HAND' : p < 0.5 ? 'BENDING LEADS' : p < 0.72 ? 'CARRYING TO HEAD' : 'HEAD PICKS';
        lamp.dot.setAttribute('fill', idle ? C.red : C.lime);
        warn.setAttribute('opacity', waiting ? (0.75 + 0.25 * Math.sin(t * 6)).toFixed(2) : 0);
        warnT.textContent = 'HOST WAITING FOR OPERATOR';
        q.setAttribute('opacity', p > 0.6 && !waiting ? 1 : 0.5);
        rg.arc.setAttribute('stroke-dasharray', (waiting ? 289 : p * 289).toFixed(1) + ' 999');
        return done + (!waiting && p >= 0.86 ? 1 : 0);
      }
    };
  }

  /* ---------- chapters ---------- */
  var CH = {
    principle: { title: 'How each method feeds' },
    speed: { title: 'Speed & precision' },
    forming: { title: 'Cut + U-form' },
    tapes: { title: 'Tapes & parts it takes' },
    integration: { title: 'Integration' },
    verdict: { title: 'Proven for 24/7 lines' }
  };
  var METRICS = {
    principle: { man: [['Cut', 'Side cutters'], ['Form', 'By hand / jig'], ['Present', 'Hand to head']], saf: [['Index', 'Hardened ratchet'], ['Check', 'Fibre sensor'], ['Cut + form', 'One cylinder stroke']] },
    speed: { man: [['Cycle', 'Operator-paced'], ['Position', 'Not located'], ['Stops', 'New strip, rework']], saf: [['Cycle time', '0.8 s / piece'], ['Accuracy', '±0.3 mm'], ['Speed', 'Air-pressure regulated']], win: 'saf' },
    forming: { man: [['Pin spacing', 'Varies by hand'], ['Lead length', 'Varies'], ['Springback', 'Not compensated']], saf: [['Blades', 'High-carbon steel'], ['Die', 'Male over female U'], ['Pin spacing', 'Adjustable die blocks']], win: 'saf' },
    tapes: { man: [['Parts', 'Same taped parts'], ['Tape', 'Any, cut by hand'], ['Waste', 'Picked up by hand']], saf: [['Body', '3×3 – 6×20 mm'], ['Leads', '0.4 – 1.0 mm'], ['Tape', '26 / 52 (+35/64/92)']] },
    integration: { man: [['Host signal', 'None'], ['Reel end', 'Found by eye'], ['Labour', 'Tied to the bench']], saf: [['Size', '730 × 95 × 212 mm'], ['Interface', '8-core Ø16 mm plug'], ['IO signals', 'Request · ready · empty']], win: 'saf' },
    verdict: { man: [['Output', 'Paced by a person'], ['U-shape', 'Varies'], ['Operator', 'At the bench']], saf: [['Feeding test', '1,000 feeds, no misfeed'], ['Ageing test', '48 h, no failure'], ['Service life', '1+ year design']], win: 'saf' }
  };
  var BADGE = { speed: '0.8 s · ±0.3 mm', forming: 'CUT + U-FORM', integration: 'IO OR STANDALONE', verdict: '48 h · NO FAILURE' };
  var TAGS = {
    forming: { man: ['PIN SPACING DEPENDS ON THE HAND', ''], saf: ['FORMING DIE SETS THE SAME U EVERY CYCLE', 'Spacing adjusted by moving die blocks A and B'] }
  };

  function applyChapter(m, st, t) {
    var ch = st.chapter || 'principle', k = st.chapterT == null ? 1 : clamp(st.chapterT / 0.6, 0, 1);
    var showMat = ch === 'tapes', showInt = ch === 'integration' && m.type === 'saf';
    m.M.setAttribute('opacity', (showMat ? 1 - 0.92 * k : showInt ? 1 - 0.6 * k : 1).toFixed(2));
    m.mat.setAttribute('opacity', (showMat ? k : 0).toFixed(2));
    if (m.integ) m.integ.setAttribute('opacity', (showInt ? k : 0).toFixed(2));
    if (m.inset) {
      var big = ch === 'forming' ? k : 0;
      var s = 1 + 0.8 * big; m.inset.setAttribute('transform', 'translate(' + ((400 - 440 * s) * big - 24 * (1 - big)).toFixed(1) + ',' + ((270 - 87 * s) * big).toFixed(1) + ') scale(' + s.toFixed(3) + ')');
    }
    var step = st.step == null ? 99 : st.step;
    m.calls.forEach(function (c, i) {
      var on = ch === 'principle' && (st.side == null ? true : st.side === m.type && i < step);
      c.setAttribute('opacity', on ? 1 : 0);
    });
    m.ring.g.setAttribute('opacity', ch === 'speed' && m.type === 'saf' ? 1 : 0);
    m.O.setAttribute('opacity', showMat ? (1 - k).toFixed(2) : 1);
    var tg = TAGS[ch] && TAGS[ch][m.type];
    m.tags.setAttribute('opacity', tg && tg[0] ? 1 : 0);
    if (tg) { m.tagT.textContent = tg[0]; m.tagT2.textContent = tg[1]; }
  }

  function AxialDuel(root) {
    this.root = root; var self = this; this.mech = {};
    ['man', 'saf'].forEach(function (k) {
      var host = root.querySelector('[data-fd="' + k + '"]'); if (!host) return;
      var svg = el('svg', { viewBox: '0 0 800 560', role: 'img', 'aria-label': (k === 'saf' ? 'SAF1001 axial tape feeder' : 'Manual cut-and-form of taped axial parts') + ' working principle animation', preserveAspectRatio: 'xMidYMid meet' });
      host.appendChild(svg);
      self.mech[k] = k === 'saf' ? buildSAF(svg) : buildMan(svg);
    });
  }
  AxialDuel.prototype.render = function (t, st) {
    st = st || {}; var out = {}, root = this.root;
    for (var k in this.mech) { var m = this.mech[k], tk = st.clock && st.clock[k] != null ? st.clock[k] : t; out[k] = m.render(Math.max(0, tk), st); applyChapter(m, st, tk); }
    var met = METRICS[st.chapter] || METRICS.principle;
    if (this._lastCh !== st.chapter) {
      this._lastCh = st.chapter;
      ['man', 'saf'].forEach(function (k) {
        var box = root.querySelector('[data-fd-metrics="' + k + '"]'); if (!box) return;
        var h = ''; met[k].forEach(function (r) { h += '<div class="fd-m"><span>' + r[0] + '</span><b>' + r[1] + '</b></div>'; });
        box.innerHTML = h;
        var card = root.querySelector('[data-fd-card="' + k + '"]'); if (card) card.classList.toggle('fd-win', met.win === k);
      });
      Array.prototype.forEach.call(root.querySelectorAll('[data-badge]'), function (e) { e.textContent = BADGE[st.chapter] || ''; });
      var tl = root.querySelector('[data-fd-title]'); if (tl) tl.textContent = (CH[st.chapter] || CH.principle).title;
    }
    ['man', 'saf'].forEach(function (k) {
      var c = root.querySelector('[data-fd-count="' + k + '"]');
      if (c) c.textContent = Math.max(0, out[k] - (st.count0 ? st.count0[k] : 0));
    });
    return out;
  };
  AxialDuel.CH = CH; AxialDuel.METRICS = METRICS; AxialDuel.BADGE = BADGE;
  G.AxialDuel = AxialDuel;
})(window);
