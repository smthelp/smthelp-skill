/* TubeDuel — side-by-side working-principle animation
   Manual tube feeding  vs  STF1003 automatic tube feeder (Southern Machinery)
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

  var C = {
    bg: '#0c1c1a', grid: 'rgba(120,200,185,.07)', teal: '#2fc1aa', teal2: '#0c665c', gold: '#f2b84b', lime: '#9ad04a',
    red: '#ff6b5a', part: '#e9eef0', partEdge: '#5d6c70', ink2: '#9fb9b4', tube: 'rgba(170,220,235,.20)', tubeEdge: 'rgba(200,235,245,.75)',
    cover: '#c8312b'
  };
  var T = 0.8;          // STF1003 published feeding speed, s per feed
  var PICK = 712, RAILY = 300;

  function defs(svg, id) {
    var d = el('defs', null, svg);
    var p = el('pattern', { id: id + 'g', width: 40, height: 40, patternUnits: 'userSpaceOnUse' }, d);
    el('path', { d: 'M40 0H0V40', fill: 'none', stroke: C.grid, 'stroke-width': 1 }, p);
    var lg2 = el('linearGradient', { id: id + 'dk', x1: 0, y1: 0, x2: 0, y2: 1 }, d);
    el('stop', { offset: 0, 'stop-color': '#3a4a52' }, lg2); el('stop', { offset: 1, 'stop-color': '#1d282d' }, lg2);
    var gl = el('filter', { id: id + 'glow', x: '-50%', y: '-50%', width: '200%', height: '200%' }, d);
    el('feGaussianBlur', { stdDeviation: 4, result: 'b' }, gl);
    var m = el('feMerge', null, gl); el('feMergeNode', { in: 'b' }, m); el('feMergeNode', { in: 'SourceGraphic' }, m);
  }
  function bg(svg, id) {
    el('rect', { width: 800, height: 560, fill: C.bg }, svg);
    el('rect', { width: 800, height: 560, fill: 'url(#' + id + 'g)' }, svg);
  }
  function partShape(parent) {
    var g = el('g', null, parent);
    el('rect', { x: -10, y: -8, width: 20, height: 16, rx: 2, fill: C.part, stroke: C.partEdge, 'stroke-width': 1.2 }, g);
    el('rect', { x: -10, y: -8, width: 6, height: 16, rx: 1.5, fill: C.teal2 }, g);
    el('line', { x1: -5, y1: 8, x2: -5, y2: 13, stroke: '#aab7ba', 'stroke-width': 2 }, g);
    el('line', { x1: 5, y1: 8, x2: 5, y2: 13, stroke: '#aab7ba', 'stroke-width': 2 }, g);
    return g;
  }
  function setPart(g, x, y, rot, op, tint) {
    g.setAttribute('transform', 'translate(' + x.toFixed(2) + ',' + y.toFixed(2) + ') rotate(' + rot.toFixed(1) + ')');
    g.setAttribute('opacity', op.toFixed(3));
    g.firstChild.setAttribute('fill', tint || C.part);
  }
  function nozzle(parent) {
    var g = el('g', null, parent);
    el('rect', { x: -26, y: -150, width: 52, height: 70, rx: 6, fill: '#33464c', stroke: '#5f7a80' }, g);
    el('rect', { x: -9, y: -80, width: 18, height: 62, fill: '#8aa3a5' }, g);
    el('rect', { x: -6, y: -18, width: 12, height: 10, rx: 2, fill: C.gold }, g);
    var t = el('text', { x: 0, y: -108, 'text-anchor': 'middle', 'font-size': 13, 'font-weight': 700, fill: C.ink2, 'font-family': 'Arial' }, g);
    t.textContent = 'HEAD';
    return g;
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
  function tube(parent, x0, x1, y) {
    var g = el('g', null, parent);
    el('rect', { x: x0, y: y - 15, width: x1 - x0, height: 30, rx: 6, fill: C.tube, stroke: C.tubeEdge, 'stroke-width': 2 }, g);
    el('line', { x1: x0 + 8, y1: y - 9, x2: x1 - 8, y2: y - 9, stroke: 'rgba(255,255,255,.35)', 'stroke-width': 2 }, g);
    return g;
  }
  function statusLamp(parent, x, y) {
    var g = el('g', null, parent);
    el('rect', { x: x, y: y, width: 220, height: 36, rx: 18, fill: 'rgba(0,0,0,.45)', stroke: 'rgba(255,255,255,.15)' }, g);
    var dot = el('circle', { cx: x + 20, cy: y + 18, r: 8, fill: C.lime, filter: 'url(#' + parent._id + 'glow)' }, g);
    var t = el('text', { x: x + 38, y: y + 24, 'font-size': 15, 'font-weight': 800, fill: '#fff', 'font-family': 'Arial', 'letter-spacing': '.08em' }, g);
    return { dot: dot, t: t };
  }
  function ring(parent, x, y) {
    var g = el('g', { opacity: 0 }, parent);
    el('circle', { cx: x, cy: y, r: 46, fill: 'rgba(12,28,26,.75)', stroke: 'rgba(255,255,255,.15)', 'stroke-width': 6 }, g);
    var arc = el('circle', { cx: x, cy: y, r: 46, fill: 'none', stroke: C.gold, 'stroke-width': 6, 'stroke-linecap': 'round', transform: 'rotate(-90 ' + x + ' ' + y + ')', 'stroke-dasharray': '0 999' }, g);
    var t = el('text', { x: x, y: y + 4, 'text-anchor': 'middle', 'font-size': 22, 'font-weight': 800, fill: '#fff', 'font-family': 'Arial' }, g);
    t.textContent = '0.8 s';
    var t2 = el('text', { x: x, y: y + 22, 'text-anchor': 'middle', 'font-size': 11, 'font-weight': 700, fill: C.ink2, 'font-family': 'Arial' }, g);
    t2.textContent = 'PER FEED';
    return { g: g, arc: arc };
  }

  /* ================= RIGHT: STF1003 ================= */
  var K = 13, P = 26, MOUTH = 640, TX0 = 240, CHG = 2.0;   // parts/tube (schematic), pitch, tube mouth, tube rear, changeover (schematic)
  var FEEDY = RAILY, SLOTS = [252, 222, 192, 162];
  function buildSTF(svg) {
    var id = 'stf' + Math.floor(Math.random() * 1e6); svg._id = id;
    defs(svg, id); bg(svg, id);
    var M = el('g', null, svg); M._id = id;
    // stand / frame
    el('rect', { x: 120, y: 330, width: 600, height: 16, rx: 4, fill: '#3a4a52' }, M);
    el('rect', { x: 150, y: 346, width: 14, height: 170, fill: '#33434a' }, M);
    el('rect', { x: 660, y: 346, width: 14, height: 170, fill: '#33434a' }, M);
    // recovery box
    var box = el('g', null, M);
    el('path', { d: 'M200 420 L560 420 L548 510 L212 510 Z', fill: 'rgba(242,184,75,.10)', stroke: C.gold, 'stroke-width': 2.5 }, box);
    label(box, 380, 500, 'RECOVERY BOX · EMPTY TUBES', 14, C.gold);
    var boxPile = [];
    for (var i = 0; i < 3; i++) { var bp = el('rect', { x: 236 + i * 6, y: 474 - i * 14, width: 290, height: 12, rx: 5, fill: C.tube, stroke: C.tubeEdge, 'stroke-width': 1.5, opacity: 0.8 }, box); boxPile.push(bp); }
    // magazine guides + red cover
    el('rect', { x: TX0 - 16, y: 140, width: 10, height: 175, fill: '#50636a' }, M);
    el('rect', { x: MOUTH + 6, y: 140, width: 10, height: 140, fill: '#50636a' }, M);
    var cover = el('rect', { x: TX0 - 20, y: 120, width: MOUTH - TX0 + 40, height: 18, rx: 4, fill: C.cover }, M);
    label(M, (TX0 + MOUTH) / 2, 112, 'TUBE MAGAZINE · MULTIPLE TUBES STACKED', 13, '#ff9d8f');
    // stacked tubes (with parts)
    var stack = [];
    for (i = 0; i < 5; i++) {
      var sg = el('g', null, M);
      tube(sg, TX0, MOUTH, 0);
      for (var j = 0; j < K; j++) { var pp = partShape(sg); setPart(pp, MOUTH - 72 - j * P, 0, 0, 1); }
      stack.push(sg);
    }
    // feed tube (moving) + column parts
    var feed = el('g', null, M); tube(feed, TX0, MOUTH, 0);
    // motor + spring
    var mot = el('g', null, M);
    el('rect', { x: 70, y: FEEDY - 34, width: 92, height: 68, rx: 6, fill: '#2f4046', stroke: '#6a8288' }, mot);
    el('circle', { cx: 116, cy: FEEDY, r: 18, fill: '#55707a', stroke: '#9fb2b0', 'stroke-width': 2 }, mot);
    var rotor = el('path', { d: 'M-12 0H12M0 -12V12', stroke: '#e8f0ee', 'stroke-width': 3 }, mot);
    label(mot, 116, FEEDY + 52, '57 STEPPER', 12, '#fff');
    var spring = el('path', { d: '', fill: 'none', stroke: C.teal, 'stroke-width': 3 }, M);
    var pusher = el('rect', { x: 0, y: FEEDY - 11, width: 10, height: 22, rx: 2, fill: C.teal }, M);
    // rail to pick
    el('rect', { x: MOUTH, y: RAILY + 10, width: PICK + 40 - MOUTH, height: 12, rx: 3, fill: '#8a9e9b', stroke: '#2b3a3a' }, M);
    var key = el('rect', { x: PICK + 13, y: RAILY - 14, width: 10, height: 26, rx: 2, fill: C.gold }, M);
    var press = el('rect', { x: PICK - 40, y: RAILY - 30, width: 26, height: 12, rx: 2, fill: '#9fb2b0' }, M);
    el('rect', { x: PICK + 26, y: RAILY - 36, width: 12, height: 22, rx: 2, fill: '#3d5157' }, M);
    el('rect', { x: PICK + 26, y: RAILY + 24, width: 12, height: 22, rx: 2, fill: '#3d5157' }, M);
    var beam = el('line', { x1: PICK + 32, y1: RAILY - 14, x2: PICK + 32, y2: RAILY + 24, stroke: C.lime, 'stroke-width': 3, filter: 'url(#' + id + 'glow)' }, M);
    // air cylinder
    var cyl = el('g', null, M);
    el('rect', { x: 330, y: 352, width: 70, height: 24, rx: 4, fill: '#2f4046', stroke: '#6a8288' }, cyl);
    var rod = el('rect', { x: 360, y: 336, width: 10, height: 18, fill: '#c9d6d4' }, cyl);
    label(cyl, 322, 369, 'AIR CYLINDER', 12, C.ink2, 'end');
    var col = []; for (i = 0; i < K; i++) col.push(partShape(M));
    var carried = partShape(M);
    var head = nozzle(M);
    var O = el('g', null, svg); O._id = id;
    var lamp = statusLamp(O, 30, 24);
    var calls = [
      callout(O, 1, 36, 150, 'Tube stack magazine', 'r'),
      callout(O, 2, 116, 400, 'Stepper + spring pusher', 'r'),
      callout(O, 3, PICK + 32, RAILY + 100, 'Fibre + software compensation', 'l'),
      callout(O, 4, PICK - 40, RAILY + 50, 'Key + pressing block', 'l'),
      callout(O, 5, 580, 470, 'Empty tube → box', 'r')
    ];
    var rg = ring(O, 110, 170);
    // materials overlay
    var mat = el('g', { opacity: 0 }, svg);
    label(mat, 400, 70, 'PARTS IT FEEDS · 3×3×3 TO 25×25×25 mm', 18, '#fff');
    var names = ['Relays', 'Terminals', 'Transformers', 'Square caps', 'Round caps', 'DIPs', 'Transistors'];
    names.forEach(function (n, k) {
      var x = 120 + (k % 4) * 186, y = 130 + Math.floor(k / 4) * 150;
      var g = el('g', null, mat);
      el('rect', { x: x - 70, y: y, width: 140, height: 120, rx: 14, fill: 'rgba(47,193,170,.10)', stroke: 'rgba(47,193,170,.5)' }, g);
      var ic = el('g', { transform: 'translate(' + x + ',' + (y + 52) + ')' }, g);
      if (k === 0) { el('rect', { x: -22, y: -16, width: 44, height: 32, rx: 3, fill: '#2c3e7a', stroke: '#8fa3e8' }, ic); }
      else if (k === 1) { for (var q = 0; q < 4; q++) el('rect', { x: -24 + q * 13, y: -14, width: 10, height: 28, rx: 2, fill: '#2fa060' }, ic); }
      else if (k === 2) { el('rect', { x: -22, y: -18, width: 44, height: 36, rx: 3, fill: '#5a4a3a', stroke: '#c9a27a' }, ic); el('rect', { x: -14, y: -24, width: 28, height: 8, fill: '#c9a27a' }, ic); }
      else if (k === 3) { el('rect', { x: -18, y: -18, width: 36, height: 36, rx: 4, fill: '#d8c46a', stroke: '#8a7a2a' }, ic); }
      else if (k === 4) { el('rect', { x: -13, y: -24, width: 26, height: 44, rx: 13, fill: '#2a5aa8', stroke: '#9ec0ff' }, ic); }
      else if (k === 5) { el('rect', { x: -24, y: -12, width: 48, height: 24, rx: 3, fill: '#222', stroke: '#888' }, ic); for (q = 0; q < 4; q++) { el('rect', { x: -20 + q * 12, y: -18, width: 4, height: 6, fill: '#bbb' }, ic); el('rect', { x: -20 + q * 12, y: 12, width: 4, height: 6, fill: '#bbb' }, ic); } }
      else { el('path', { d: 'M-16 10 V-8 A16 12 0 0 1 16 -8 V10 Z', fill: '#222', stroke: '#888' }, ic); for (q = -1; q <= 1; q++) el('rect', { x: q * 9 - 2, y: 10, width: 4, height: 12, fill: '#bbb' }, ic); }
      label(g, x, y + 106, n, 15, '#fff');
    });
    // size scale
    el('rect', { x: 150, y: 470, width: 6, height: 6, fill: C.teal }, mat);
    el('rect', { x: 190, y: 426, width: 50, height: 50, fill: 'none', stroke: C.teal, 'stroke-width': 2.5 }, mat);
    label(mat, 153, 500, '3 mm', 13, C.teal);
    label(mat, 215, 500, '25 mm', 13, C.teal);
    label(mat, 262, 462, 'Smallest and largest part, drawn to scale', 14, C.ink2, 'start');
    // integration overlay
    var integ = el('g', { opacity: 0 }, svg);
    el('rect', { x: 30, y: 360, width: 740, height: 140, rx: 16, fill: 'rgba(12,28,26,.94)', stroke: 'rgba(154,208,74,.4)' }, integ);
    var brands = [['Panasonic CM602', 166], ['JUKI', 80], ['YAMAHA', 104], ['Mirae', 86], ['Robot arm cells', 160]], bx = 72;
    brands.forEach(function (b) {
      el('rect', { x: bx, y: 404, width: b[1], height: 40, rx: 20, fill: 'rgba(154,208,74,.16)', stroke: C.lime }, integ);
      label(integ, bx + b[1] / 2, 430, b[0], 15, '#fff'); bx += b[1] + 12;
    });
    label(integ, 400, 392, 'PROVEN ON ODD-FORM MACHINES · READY FOR ROBOT CELLS', 14, C.lime);
    label(integ, 400, 478, '24 V · 8-core Ø16 mm aviation plug · IO or standalone', 16, '#fff');
    var tags = el('g', { opacity: 0 }, svg);
    var tagT = label(tags, 400, 80, '', 20, C.lime, 'middle', 800), tagT2 = label(tags, 400, 104, '', 15, C.ink2, 'middle', 700);

    function springPath(x1) {
      var x0 = 134, n = Math.max(6, Math.round((x1 - x0) / 10)), d = 'M' + x0 + ' ' + FEEDY;
      for (var k = 1; k <= n; k++) d += 'L' + (x0 + (x1 - x0) * k / n).toFixed(1) + ' ' + (FEEDY + (k % 2 ? -7 : 7));
      return d;
    }
    return {
      type: 'stf', M: M, O: O, calls: calls, ring: rg, tags: tags, tagT: tagT, tagT2: tagT2, mat: mat, integ: integ, cover: cover,
      render: function (t) {
        var TP = K * T + CHG, cyc = Math.floor(t / TP), lt = t - cyc * TP, picks = cyc * K;
        rotor.setAttribute('transform', 'translate(116,' + FEEDY + ') rotate(' + ((t * 300) % 360).toFixed(1) + ')');
        var hy = 140, feedY = FEEDY, feedOp = 1, feedX = 0, stackShift = 0, colOff = 0, pushX, rodY = 336, beamOn = false, carriedOn = -1;
        // stack positions
        var slotY = function (k) { return k === 0 ? FEEDY : SLOTS[Math.min(k, 4) - 1]; };
        if (lt < K * T) {
          var n = Math.floor(lt / T), Pp = frac(lt / T), r = K - n;
          picks += n;
          var down = Pp < 0.22 ? ease(Pp / 0.22) : Pp < 0.32 ? 1 : 1 - ease((Pp - 0.32) / 0.25);
          hy = 140 + (RAILY - 4 - 140) * down;
          var shift = (r > 1) ? P * ease((Pp - 0.55) / 0.35) : 0;
          for (var i = 0; i < K; i++) {
            var g = col[i];
            if (i >= r || (i === 0 && Pp >= 0.3)) { g.setAttribute('opacity', 0); continue; }
            setPart(g, PICK - i * P + shift, RAILY, 0, 1);
          }
          pushX = PICK - (r - 1) * P + shift - 26;
          if (Pp >= 0.3) { setPart(carried, PICK, hy + 2, 0, Pp < 0.62 ? 1 : clamp(1 - (Pp - 0.62) / 0.15, 0, 1)); picks += 1; } else carried.setAttribute('opacity', 0);
          beamOn = (Pp < 0.3 || (Pp > 0.9 && r > 1));
          press.setAttribute('y', RAILY - 30 + (Pp > 0.12 && Pp < 0.34 ? -10 : 0));
          lamp.t.textContent = 'AUTO FEEDING'; lamp.dot.setAttribute('fill', C.lime);
          for (i = 0; i < 5; i++) { stack[i].setAttribute('transform', 'translate(0,' + slotY(i + 1) + ')'); stack[i].setAttribute('opacity', i < 4 ? 1 : 0); }
          feed.setAttribute('transform', 'translate(0,' + FEEDY + ')'); feed.setAttribute('opacity', 1);
        } else {
          var c = lt - K * T;
          picks += K;
          carried.setAttribute('opacity', 0);
          lamp.t.textContent = 'AUTO TUBE CHANGE'; lamp.dot.setAttribute('fill', C.gold);
          var last = PICK - 26;
          // 1) spring retracts
          var kr = ease(c / 0.6); pushX = lerp(last, 150, kr);
          // 2) cylinder kicks, empty tube drops
          var kd = ease((c - 0.6) / 0.5); rodY = 336 - 14 * (c > 0.6 && c < 1.25 ? 1 : 0);
          feed.setAttribute('transform', 'translate(0,' + (FEEDY + kd * 160).toFixed(1) + ')'); feed.setAttribute('opacity', (1 - clamp((c - 0.95) / 0.2, 0, 1)).toFixed(2));
          // 3) stack drops one slot
          var ks = ease((c - 1.1) / 0.4);
          for (i = 0; i < 5; i++) {
            var y0 = slotY(i + 1), y1 = slotY(i);
            stack[i].setAttribute('transform', 'translate(0,' + lerp(y0, y1, ks).toFixed(1) + ')');
            stack[i].setAttribute('opacity', i < 4 ? 1 : ks);
          }
          // 4) column slides to pick + pusher follows
          var ka = ease((c - 1.5) / 0.5);
          colOff = 72 * ka;
          if (c > 1.5) pushX = lerp(150, MOUTH - 72 - (K - 1) * P - 26 + 72, ka);
          for (i = 0; i < K; i++) col[i].setAttribute('opacity', 0);
          if (c > 1.5) {
            // hide moving stack[0] parts; draw column instead
            for (i = 0; i < K; i++) setPart(col[i], MOUTH - 72 - i * P + colOff, RAILY, 0, 1);
            stack[0].setAttribute('opacity', 0);
            feed.setAttribute('opacity', 1); feed.setAttribute('transform', 'translate(0,' + FEEDY + ')');
          }
          beamOn = c > 1.95;
          press.setAttribute('y', RAILY - 30);
        }
        boxPile.forEach(function (b, k) { b.setAttribute('opacity', 0.8); });
        rod.setAttribute('y', rodY);
        head.setAttribute('transform', 'translate(' + PICK + ',' + hy.toFixed(1) + ')');
        pusher.setAttribute('x', pushX.toFixed(1));
        spring.setAttribute('d', springPath(pushX));
        beam.setAttribute('stroke', beamOn ? C.lime : C.red);
        var Pc = lt < K * T ? frac(lt / T) : 0;
        rg.arc.setAttribute('stroke-dasharray', (Pc * 289).toFixed(1) + ' 999');
        return picks;
      }
    };
  }

  /* ================= LEFT: manual tube feeding ================= */
  var KM = 10, JAMAT = 5, JAM = 1.4, WAIT = 4.2;
  var A = [190, 196], PP = [PICK, RAILY];
  var L = Math.hypot(PP[0] - A[0], PP[1] - A[1]), ux = (PP[0] - A[0]) / L, uy = (PP[1] - A[1]) / L, ANG = Math.atan2(uy, ux) * 57.2958;
  var TUBE_S0 = 92;  // tube ends this far before pick (rail)
  function buildMan(svg) {
    var id = 'man' + Math.floor(Math.random() * 1e6); svg._id = id;
    defs(svg, id); bg(svg, id);
    var M = el('g', null, svg); M._id = id;
    // bench
    el('rect', { x: 110, y: 380, width: 640, height: 18, rx: 4, fill: '#3a4a52' }, M);
    el('rect', { x: 140, y: 398, width: 14, height: 120, fill: '#33434a' }, M);
    el('rect', { x: 700, y: 398, width: 14, height: 120, fill: '#33434a' }, M);
    // support chute
    el('line', { x1: A[0], y1: A[1] + 20, x2: PP[0] + 30, y2: PP[1] + 26, stroke: '#5b7177', 'stroke-width': 8 }, M);
    el('line', { x1: 220, y1: 222, x2: 220, y2: 380, stroke: '#4a5d63', 'stroke-width': 8 }, M);
    el('line', { x1: 520, y1: 290, x2: 520, y2: 380, stroke: '#4a5d63', 'stroke-width': 8 }, M);
    // empty-tube pile on bench / floor bin
    var bin = el('g', null, M);
    el('path', { d: 'M330 440 L560 440 L548 520 L342 520 Z', fill: 'rgba(255,107,90,.08)', stroke: '#ff9d8f', 'stroke-width': 2, 'stroke-dasharray': '6 5' }, bin);
    label(bin, 445, 510, 'EMPTY TUBES · BY HAND', 13, '#ff9d8f');
    for (var i = 0; i < 2; i++) el('rect', { x: 352 + i * 8, y: 488 - i * 13, width: 180, height: 11, rx: 5, fill: C.tube, stroke: C.tubeEdge, opacity: 0.8 }, bin);
    // tube (on incline) group
    var TG = el('g', null, M);
    var tl = L - TUBE_S0;
    el('rect', { x: 0, y: -15, width: tl, height: 30, rx: 6, fill: C.tube, stroke: C.tubeEdge, 'stroke-width': 2 }, TG);
    el('line', { x1: 8, y1: -9, x2: tl - 8, y2: -9, stroke: 'rgba(255,255,255,.35)', 'stroke-width': 2 }, TG);
    var parts = []; for (i = 0; i < KM; i++) parts.push(partShape(M));
    var carried = partShape(M);
    // outlet (no positive location)
    el('rect', { x: PICK - 30, y: RAILY + 12, width: 70, height: 10, rx: 3, fill: '#8a9e9b' }, M);
    var q = label(M, PICK + 4, RAILY + 52, '?', 30, '#ff9d8f', 'middle', 900);
    // operator hand
    var hand = el('g', null, M);
    el('rect', { x: -26, y: -16, width: 52, height: 34, rx: 14, fill: '#e3b48f', stroke: '#9a6b4a', 'stroke-width': 2 }, hand);
    for (i = 0; i < 4; i++) el('rect', { x: -22 + i * 12, y: -36, width: 10, height: 24, rx: 5, fill: '#e3b48f', stroke: '#9a6b4a', 'stroke-width': 1.5 }, hand);
    el('rect', { x: -34, y: 16, width: 68, height: 30, rx: 6, fill: '#4f6a8a' }, hand);
    var tap = el('g', { opacity: 0 }, M);
    for (i = 0; i < 3; i++) el('path', { d: 'M' + (-24 + i * 18) + ' -12 l' + (6 - i * 6) + ' -14', stroke: C.gold, 'stroke-width': 3, 'stroke-linecap': 'round' }, tap);
    var head = nozzle(M);
    var O = el('g', null, svg); O._id = id;
    var lamp = statusLamp(O, 30, 24);
    var warn = el('g', { opacity: 0 }, O);
    el('rect', { x: 250, y: 80, width: 300, height: 44, rx: 10, fill: 'rgba(255,107,90,.18)', stroke: C.red, 'stroke-width': 2 }, warn);
    var warnT = label(warn, 400, 109, 'HOST WAITING FOR OPERATOR', 16, '#ffd0c8', 'middle', 800);
    var calls = [
      callout(O, 1, 300, 170, 'Gravity + tapping', 'r'),
      callout(O, 2, 120, 330, 'Every tube swapped by hand', 'r'),
      callout(O, 3, PICK - 4, RAILY + 96, 'Uncertain outlet position', 'l')
    ];
    var rg = ring(O, 600, 210);
    // materials overlay (left): tubes it takes
    var mat = el('g', { opacity: 0 }, svg);
    label(mat, 400, 70, 'SAME TUBES YOU LOAD BY HAND TODAY', 18, '#fff');
    var tb = [['PVC tube', 'rgba(170,220,235,.25)'], ['Aluminium tube', 'rgba(200,205,210,.55)']];
    tb.forEach(function (x, k) {
      var y = 150 + k * 90;
      el('rect', { x: 110, y: y, width: 580, height: 34, rx: 8, fill: x[1], stroke: C.tubeEdge, 'stroke-width': 2 }, mat);
      label(mat, 110, y - 12, x[0].toUpperCase(), 15, C.ink2, 'start');
    });
    // length scale 200-650 mm
    var sx = function (mm) { return 110 + (mm / 650) * 580; };
    el('line', { x1: sx(0), y1: 360, x2: sx(650), y2: 360, stroke: 'rgba(255,255,255,.2)', 'stroke-width': 10, 'stroke-linecap': 'round' }, mat);
    el('line', { x1: sx(200), y1: 360, x2: sx(650), y2: 360, stroke: C.gold, 'stroke-width': 10, 'stroke-linecap': 'round' }, mat);
    label(mat, sx(200), 392, '200 mm', 15, '#fff'); label(mat, sx(650) - 10, 392, '650 mm', 15, '#fff', 'end');
    label(mat, 400, 340, 'TUBE LENGTH', 14, C.ink2);
    label(mat, 400, 450, 'Wall thickness ≥ 0.6 mm · no repacking', 18, C.lime, 'middle', 800);
    var tags = el('g', { opacity: 0 }, svg);
    var tagT = label(tags, 400, 80, '', 20, C.red, 'middle', 800), tagT2 = label(tags, 400, 104, '', 15, C.ink2, 'middle', 700);

    function at(s) { return [PP[0] - ux * s, PP[1] - uy * s]; }
    return {
      type: 'man', M: M, O: O, calls: calls, ring: rg, tags: tags, tagT: tagT, tagT2: tagT2, mat: mat, warn: warn,
      render: function (t) {
        var TP = KM * T + JAM + WAIT, cyc = Math.floor(t / TP), lt = t - cyc * TP;
        var hy = 140, tubeShift = 0, tubeLift = 0, handXY = [120, 470], handRot = 0, tapOn = 0, waiting = false, r = KM, jamOn = false, beamDummy;
        var tA = at(L);
        // phases: picks 0..JAMAT-1, jam, picks JAMAT..KM-1, wait/swap
        var tJ0 = JAMAT * T, tJ1 = tJ0 + JAM, tE = tJ1 + (KM - JAMAT) * T;
        var n, Pp = -1;
        if (lt < tJ0) { n = Math.floor(lt / T); Pp = frac(lt / T); }
        else if (lt < tJ1) { n = JAMAT; jamOn = true; }
        else if (lt < tE) { n = JAMAT + Math.floor((lt - tJ1) / T); Pp = frac((lt - tJ1) / T); }
        else { n = KM; waiting = true; }
        r = KM - n;
        var shift = 0, down = 0;
        if (Pp >= 0) {
          down = Pp < 0.22 ? ease(Pp / 0.22) : Pp < 0.32 ? 1 : 1 - ease((Pp - 0.32) / 0.25);
          shift = r > 1 ? P * ease((Pp - 0.55) / 0.35) : 0;
        }
        hy = 140 + (RAILY - 4 - 140) * down;
        var c = lt - tE;
        // tube motion during swap: lift empty away, bring new tube
        var tubeOp = 1, newTube = false;
        if (waiting) {
          var k1 = ease((c - 1.0) / 0.9), k2 = ease((c - 2.2) / 0.9);
          if (c < 2.1) { tubeLift = -160 * k1; tubeOp = 1 - k1; handXY = [lerp(160, tA[0] + 140, ease(c / 0.9)), lerp(470, tA[1] + 40, ease(c / 0.9)) + tubeLift]; }
          else { newTube = true; tubeLift = -160 * (1 - k2); tubeOp = k2; handXY = [tA[0] + 140, tA[1] + 40 + tubeLift]; }
          if (c > 3.2) handXY = [lerp(tA[0] + 140, 120, ease((c - 3.2) / 0.8)), lerp(tA[1] + 40, 470, ease((c - 3.2) / 0.8))];
        } else if (jamOn) {
          var jt = lt - tJ0;
          var hk = ease(jt / 0.35) * (1 - ease((jt - 1.05) / 0.35));
          handXY = [lerp(120, 330, hk), lerp(470, tA[1] + 70, hk)];
          tapOn = (jt > 0.35 && jt < 1.05) ? (Math.sin(jt * 30) > 0 ? 1 : 0.3) : 0;
        }
        TG.setAttribute('transform', 'translate(' + tA[0].toFixed(1) + ',' + (tA[1] + tubeLift).toFixed(1) + ') rotate(' + ANG.toFixed(2) + ')');
        TG.setAttribute('opacity', tubeOp.toFixed(2));
        // parts along incline
        for (var i = 0; i < KM; i++) {
          var g = parts[i];
          if (waiting) {
            if (newTube) { var p = at(TUBE_S0 + 14 + i * P); setPart(g, p[0], p[1] + tubeLift, ANG, tubeOp); }
            else g.setAttribute('opacity', 0);
            continue;
          }
          if (i >= r || (i === 0 && Pp >= 0.3)) { g.setAttribute('opacity', 0); continue; }
          var s = i * P - shift, rot = ANG, tint;
          if (jamOn && i === 1) { rot = ANG + 38 + Math.sin((lt - tJ0) * 30) * 6 * tapOn; tint = '#ffb3a8'; s += 10; }
          var pp = at(Math.max(0, s));
          if (s <= 0.1) { pp = [PICK, RAILY]; rot = 0; }
          setPart(g, pp[0], pp[1], s <= 0.1 ? 0 : rot, 1, tint);
        }
        if (Pp >= 0.3) setPart(carried, PICK, hy + 2, 0, Pp < 0.62 ? 1 : clamp(1 - (Pp - 0.62) / 0.15, 0, 1)); else carried.setAttribute('opacity', 0);
        head.setAttribute('transform', 'translate(' + PICK + ',' + hy.toFixed(1) + ')');
        hand.setAttribute('transform', 'translate(' + handXY[0].toFixed(1) + ',' + handXY[1].toFixed(1) + ') rotate(' + handRot + ')');
        tap.setAttribute('transform', 'translate(' + handXY[0].toFixed(1) + ',' + (handXY[1] - 40).toFixed(1) + ')');
        tap.setAttribute('opacity', tapOn);
        var stop = waiting || jamOn;
        lamp.t.textContent = waiting ? 'WAITING · TUBE SWAP' : jamOn ? 'STOPPED · PART TILTED' : 'RUNNING';
        lamp.dot.setAttribute('fill', stop ? C.red : C.lime);
        warn.setAttribute('opacity', stop ? (0.75 + 0.25 * Math.sin(t * 6)).toFixed(2) : 0);
        warnT.textContent = waiting ? 'HOST WAITING FOR OPERATOR' : 'OPERATOR CLEARS A TILTED PART';
        rg.arc.setAttribute('stroke-dasharray', ((Pp >= 0 ? Pp : 0) * 289).toFixed(1) + ' 999');
        return cyc * KM + n + (Pp >= 0.3 ? 1 : 0);
      }
    };
  }

  /* ---------- chapters ---------- */
  var CH = {
    principle: { title: 'How each method feeds' },
    speed: { title: 'Speed & precision' },
    tubes: { title: 'Tube changeover' },
    materials: { title: 'Tubes & parts it takes' },
    integration: { title: 'Integration' },
    verdict: { title: 'Proven for 24/7 lines' }
  };
  var METRICS = {
    principle: { man: [['Drive', 'Gravity + tapping'], ['Tube change', 'By hand'], ['Outlet', 'Not located']], stf: [['Drive', '57 stepper + spring'], ['Tube change', 'Auto stack + eject'], ['Outlet', 'Fibre + key']] },
    speed: { man: [['Cycle', 'Operator-paced'], ['Position', 'Uncertain'], ['Stops', 'Tilts, empty tubes']], stf: [['Feeding speed', '0.8 s'], ['Accuracy', '±0.5 mm'], ['Speed gears', '4 · 600 rpm']], win: 'stf' },
    tubes: { man: [['Tubes loaded', 'One at a time'], ['Empty tube', 'Removed by hand'], ['Host', 'Waits']], stf: [['Tubes loaded', 'Multiple, stacked'], ['Empty tube', 'Cylinder → box'], ['Tube length', '200 – 650 mm']], win: 'stf' },
    materials: { man: [['Tubes', 'PVC or aluminium'], ['Length', '200 – 650 mm'], ['Wall', '≥ 0.6 mm']], stf: [['Part size', '3 – 25 mm cube'], ['Types', 'Relays, terminals…'], ['Channels', '1 (2 custom)']] },
    integration: { man: [['Host signal', 'None'], ['Record', 'Operator memory'], ['Labour', 'Tied to the tube']], stf: [['Size', '1350 × 92 × 115 mm'], ['Interface', '8-core Ø16 mm plug'], ['Control', 'ARM · IO / standalone']], win: 'stf' },
    verdict: { man: [['Feeding', 'Stops for tubes'], ['Outlet', 'Uncertain'], ['Operator', 'At the feeder']], stf: [['Feeding test', '1,000 feeds, no fault'], ['Ageing test', '48 h, no fault'], ['Spring life', '4 million bends']], win: 'stf' }
  };
  var BADGE = { speed: '0.8 s · ±0.5 mm', tubes: 'AUTO TUBE CHANGE', integration: 'IO OR STANDALONE', verdict: '48 h · NO FAULT' };
  var TAGS = {
    verdict: { man: ['', ''], stf: ['', ''] }
  };

  function applyChapter(m, st, t) {
    var ch = st.chapter || 'principle', k = st.chapterT == null ? 1 : clamp(st.chapterT / 0.6, 0, 1);
    var showMat = ch === 'materials', showInt = ch === 'integration' && m.type === 'stf';
    m.M.setAttribute('opacity', (showMat ? 1 - 0.92 * k : showInt ? 1 - 0.55 * k : 1).toFixed(2));
    m.mat.setAttribute('opacity', (showMat ? k : 0).toFixed(2));
    if (m.integ) m.integ.setAttribute('opacity', (showInt ? k : 0).toFixed(2));
    var step = st.step == null ? 99 : st.step, my = st.side == null || st.side === m.type;
    m.calls.forEach(function (c, i) {
      var on = ch === 'principle' && my && i < (st.side === m.type ? step : (st.side == null ? 99 : 0));
      c.setAttribute('opacity', on ? 1 : 0);
    });
    m.ring.g.setAttribute('opacity', ch === 'speed' && m.type === 'stf' ? 1 : 0);
    m.O.setAttribute('opacity', showMat ? (1 - k).toFixed(2) : 1);
    var tg = TAGS[ch] && TAGS[ch][m.type];
    m.tags.setAttribute('opacity', tg && tg[0] ? 1 : 0);
    if (tg) { m.tagT.textContent = tg[0]; m.tagT2.textContent = tg[1]; }
  }

  function TubeDuel(root) {
    this.root = root; var self = this; this.mech = {};
    ['man', 'stf'].forEach(function (k) {
      var host = root.querySelector('[data-fd="' + k + '"]'); if (!host) return;
      var svg = el('svg', { viewBox: '0 0 800 560', role: 'img', 'aria-label': (k === 'stf' ? 'STF1003 automatic tube feeder' : 'Manual tube feeding') + ' working principle animation', preserveAspectRatio: 'xMidYMid meet' });
      host.appendChild(svg);
      self.mech[k] = k === 'stf' ? buildSTF(svg) : buildMan(svg);
    });
  }
  TubeDuel.prototype.render = function (t, st) {
    st = st || {}; var out = {}, root = this.root;
    for (var k in this.mech) { var m = this.mech[k], tk = st.clock && st.clock[k] != null ? st.clock[k] : t; out[k] = m.render(tk, st); applyChapter(m, st, tk); }
    var met = METRICS[st.chapter] || METRICS.principle;
    if (this._lastCh !== st.chapter) {
      this._lastCh = st.chapter;
      ['man', 'stf'].forEach(function (k) {
        var box = root.querySelector('[data-fd-metrics="' + k + '"]'); if (!box) return;
        var h = ''; met[k].forEach(function (r) { h += '<div class="fd-m"><span>' + r[0] + '</span><b>' + r[1] + '</b></div>'; });
        box.innerHTML = h;
        var card = root.querySelector('[data-fd-card="' + k + '"]'); if (card) card.classList.toggle('fd-win', met.win === k);
      });
      Array.prototype.forEach.call(root.querySelectorAll('[data-badge]'), function (e) { e.textContent = BADGE[st.chapter] || ''; });
      var tl = root.querySelector('[data-fd-title]'); if (tl) tl.textContent = (CH[st.chapter] || CH.principle).title;
    }
    ['man', 'stf'].forEach(function (k) {
      var c = root.querySelector('[data-fd-count="' + k + '"]');
      if (c) c.textContent = Math.max(0, out[k] - (st.count0 ? st.count0[k] : 0));
    });
    return out;
  };
  TubeDuel.CH = CH; TubeDuel.METRICS = METRICS; TubeDuel.BADGE = BADGE;
  G.TubeDuel = TubeDuel;
})(window);
