/* svg2canvas - draw a live SVG DOM tree onto a 2D canvas, synchronously (p3cv helper, since 1.3.0).
   Lets an existing SVG mechanism module (one that builds <svg> elements and moves them with
   setAttribute) satisfy the canvas animation contract of templates/anim-template.js:

     var svg = document.createElementNS('http://www.w3.org/2000/svg','svg');   // detached is fine
     var anim = new MySvgAnim(svg, {...});
     render(ctx, W, H, o) { anim.render(o.t); SVG2Canvas.draw(ctx, svg, {vars: THEME}); }

   Supported: g (transform translate/rotate/scale/matrix, opacity), rect (rx), circle, ellipse, line,
   path (d via Path2D), polygon/polyline, text + tspan (font-size/-weight/-family, text-anchor,
   letter-spacing), fill / stroke / stroke-width / stroke-dasharray / opacity / fill-opacity,
   var(--name,fallback) colours (resolved from opts.vars, else the fallback), and mask="url(#id)"
   whose mask is white shapes plus black "holes" (drawn via an offscreen canvas). Not supported:
   gradients, filters, clipPath, CSS classes/stylesheets, images - keep SVG modules to inline attributes.
   Draws in the SVG's user units: set up ctx scale/translate before calling. */
(function (G) {
  function num(e, a, d) { var v = e.getAttribute(a); return v === null || v === '' ? (d || 0) : parseFloat(v) }
  function col(v, vars) {
    if (!v) return v; v = v.trim();
    var m = /^var\(\s*(--[\w-]+)\s*(?:,\s*(.+))?\)$/.exec(v);
    if (m) return (vars && vars[m[1]]) || (m[2] ? col(m[2], vars) : '#000');
    return v;
  }
  function inh(e, a, p) { var v = e.getAttribute(a); return v === null ? p[a] : v }
  function transform(ctx, t) {
    if (!t) return;
    var re = /(\w+)\s*\(([^)]*)\)/g, m;
    while ((m = re.exec(t))) {
      var a = m[2].split(/[\s,]+/).filter(Boolean).map(parseFloat);
      if (m[1] === 'translate') ctx.translate(a[0] || 0, a[1] || 0);
      else if (m[1] === 'rotate') { if (a.length > 2) { ctx.translate(a[1], a[2]); ctx.rotate(a[0] * Math.PI / 180); ctx.translate(-a[1], -a[2]) } else ctx.rotate((a[0] || 0) * Math.PI / 180) }
      else if (m[1] === 'scale') ctx.scale(a[0], a.length > 1 ? a[1] : a[0]);
      else if (m[1] === 'matrix') ctx.transform(a[0], a[1], a[2], a[3], a[4], a[5]);
    }
  }
  function rrect(ctx, x, y, w, h, r) {
    r = Math.max(0, Math.min(r, w / 2, h / 2)); ctx.beginPath();
    if (!r) { ctx.rect(x, y, w, h); return }
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function paint(ctx, e, st, path) {
    var f = st.fill, s = st.stroke, sw = parseFloat(st['stroke-width'] || 1);
    if (f && f !== 'none') { ctx.globalAlpha = st._a * parseFloat(st['fill-opacity'] || 1); ctx.fillStyle = f; path ? ctx.fill(path) : ctx.fill() }
    if (s && s !== 'none' && sw > 0) {
      ctx.globalAlpha = st._a * parseFloat(st['stroke-opacity'] || 1); ctx.strokeStyle = s; ctx.lineWidth = sw;
      var d = st['stroke-dasharray']; ctx.setLineDash(d && d !== 'none' ? d.split(/[\s,]+/).map(parseFloat) : []);
      ctx.lineCap = st['stroke-linecap'] || 'butt'; path ? ctx.stroke(path) : ctx.stroke();
    }
  }
  var KEYS = ['fill', 'stroke', 'stroke-width', 'stroke-dasharray', 'stroke-linecap', 'fill-opacity', 'stroke-opacity',
    'font-size', 'font-weight', 'font-family', 'text-anchor', 'letter-spacing'];
  function node(ctx, e, p, o) {
    var tag = (e.localName || e.nodeName || '').toLowerCase();
    if (!tag || tag === 'defs' || tag === 'mask' || tag === 'clippath' || tag === '#text') return;
    var st = { _a: p._a * num(e, 'opacity', 1) };
    if (st._a <= 0.001 || e.getAttribute('display') === 'none' || e.getAttribute('visibility') === 'hidden') return;
    KEYS.forEach(function (k) { st[k] = inh(e, k, p) });
    st.fill = col(st.fill, o.vars); st.stroke = col(st.stroke, o.vars);
    var mk = e.getAttribute('mask');
    if (mk && o.root) { masked(ctx, e, st, mk, o); return }
    ctx.save(); transform(ctx, e.getAttribute('transform'));
    if (tag === 'g' || tag === 'svg') { for (var c = e.firstElementChild; c; c = c.nextElementSibling) node(ctx, c, st, o) }
    else if (tag === 'rect') { rrect(ctx, num(e, 'x'), num(e, 'y'), num(e, 'width'), num(e, 'height'), num(e, 'rx', num(e, 'ry'))); paint(ctx, e, st) }
    else if (tag === 'circle') { ctx.beginPath(); ctx.arc(num(e, 'cx'), num(e, 'cy'), Math.max(0, num(e, 'r')), 0, 2 * Math.PI); paint(ctx, e, st) }
    else if (tag === 'ellipse') { ctx.beginPath(); ctx.ellipse(num(e, 'cx'), num(e, 'cy'), Math.max(0, num(e, 'rx')), Math.max(0, num(e, 'ry')), 0, 0, 2 * Math.PI); paint(ctx, e, st) }
    else if (tag === 'line') { if (!st.stroke) st.stroke = 'none'; st.fill = 'none'; ctx.beginPath(); ctx.moveTo(num(e, 'x1'), num(e, 'y1')); ctx.lineTo(num(e, 'x2'), num(e, 'y2')); paint(ctx, e, st) }
    else if (tag === 'path') { var d = e.getAttribute('d'); if (d) paint(ctx, e, st, new Path2D(d)) }
    else if (tag === 'polygon' || tag === 'polyline') { var pts = (e.getAttribute('points') || '').trim(); if (pts) paint(ctx, e, st, new Path2D('M' + pts + (tag === 'polygon' ? 'Z' : ''))); }
    else if (tag === 'text') text(ctx, e, st);
    ctx.restore();
  }
  function text(ctx, e, st) {
    var fs = parseFloat(st['font-size'] || 16), fam = st['font-family'] || 'Arial, sans-serif';
    ctx.font = (st['font-weight'] || 400) + ' ' + fs + 'px ' + fam;
    var an = st['text-anchor']; ctx.textAlign = an === 'middle' ? 'center' : an === 'end' ? 'right' : 'left'; ctx.textBaseline = 'alphabetic';
    if ('letterSpacing' in ctx) ctx.letterSpacing = (parseFloat(st['letter-spacing'] || 0) || 0) + 'px';
    ctx.globalAlpha = st._a; ctx.fillStyle = st.fill && st.fill !== 'none' ? st.fill : '#000';
    var spans = e.getElementsByTagName ? Array.prototype.slice.call(e.getElementsByTagName('tspan')) : [];
    if (!spans.length) { ctx.fillText(e.textContent, num(e, 'x'), num(e, 'y')); return }
    spans.forEach(function (s) { ctx.fillText(s.textContent, s.hasAttribute('x') ? num(s, 'x') : num(e, 'x'), s.hasAttribute('y') ? num(s, 'y') : num(e, 'y')) });
  }
  function masked(ctx, e, st, mk, o) {
    var id = /url\(#([^)]+)\)/.exec(mk), m = id && o.root.querySelector('#' + CSS.escape(id[1]));
    var cv = document.createElement('canvas'); cv.width = ctx.canvas.width; cv.height = ctx.canvas.height;
    var c2 = cv.getContext('2d'); c2.setTransform(ctx.getTransform());
    var clone = e.cloneNode(true); clone.removeAttribute('mask'); clone.removeAttribute('opacity');
    node(c2, clone, { _a: 1 }, { vars: o.vars });
    if (m) { c2.globalCompositeOperation = 'destination-out';
      for (var c = m.firstElementChild; c; c = c.nextElementSibling) {
        var f = (c.getAttribute('fill') || '').toLowerCase();
        if (f === '#000' || f === '#000000' || f === 'black') { var k = c.cloneNode(true); k.setAttribute('fill', '#000'); node(c2, k, { _a: 1 }, { vars: o.vars }) } } }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = st._a; ctx.drawImage(cv, 0, 0); ctx.restore();
  }
  function draw(ctx, svg, o) {
    o = o || {}; o.root = svg;
    var base = { _a: 1, fill: '#000', stroke: 'none', 'stroke-width': '1', 'font-size': '16', 'font-weight': '400', 'font-family': 'Arial, sans-serif', 'text-anchor': 'start' };
    for (var c = svg.firstElementChild; c; c = c.nextElementSibling) node(ctx, c, base, o);
  }
  G.SVG2Canvas = { draw: draw };
})(window);
