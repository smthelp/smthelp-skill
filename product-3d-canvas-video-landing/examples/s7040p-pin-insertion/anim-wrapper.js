/* S7040P canvas wrapper: InsertAnim (SVG, insert-anim.svg.js) -> p3cv canvas contract via SVG2Canvas.
   World 1600x1000; the 1600x720 SVG sits at y=140. One board = InsertAnim.PERIOD (12.8 s): 8 presses,
   2 per head. Model 'C' = 4 bowls -> 4 heads, pins + multi-finger clips pressed flush (press:true).
   Customer dimensions are NOT in this public example; a project may set them after this file:
     InsertAnim.MODELS.C.dia=[...]; InsertAnim.MODELS.C.hole=[...]   (strings, mm)
   Extra opts: noTitle hides the model title block (video/thumbnail already show the name). */
(function (G) {
  var IA = G.InsertAnim, P = IA.PERIOD, OY = 140, inst = null, svg = null;
  var STEPS = [
    { a: 0, b: 2, name: 'Conveyor in + board stop', f: 0 },
    { a: 2, b: 3.2, name: 'Fiducial vision correction', f: 1 },
    { a: 3.2, b: 4.2, name: 'Bowl 1 → Head 1: medium pin', f: 3 },
    { a: 4.2, b: 5.2, name: 'Bowl 2 → Head 2: large pin', f: 4 },
    { a: 5.2, b: 6.2, name: 'Bowl 3 → Head 3: medium clip', f: 5 },
    { a: 6.2, b: 7.2, name: 'Bowl 4 → Head 4: large clip', f: 6 },
    { a: 7.2, b: 11.2, name: 'Servo press flush + miss check', f: 8 },
    { a: 11.2, b: P, name: 'Conveyor out', f: 10 }];
  function ensure() {
    if (inst) return;
    svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    inst = new IA(svg, { model: 'C', callout: false });
    STEPS.forEach(function (s) { var f = inst.STEPS[s.f].f; s.box = [f[0] - f[2], f[1] - f[2] + OY, 2 * f[2], 2 * f[2]] });
  }
  function stepAt(t) { t = ((t % P) + P) % P; for (var i = 0; i < STEPS.length; i++) if (t < STEPS[i].b) return i; return STEPS.length - 1 }
  var DARK = { '--ia-body': '#22312f', '--ia-stroke': '#4fb8a6', '--ia-ink': '#e6efed', '--ia-dark': '#3a4a48', '--ia-legend': 'rgba(255,255,255,.08)' };
  function render(ctx, W, H, o) {
    o = o || {}; ensure(); var t = ((o.t || 0) % P + P) % P, st = stepAt(t), dark = o.theme === 'dark';
    var f = o.focus || { x: 800, y: 500, s: 1 }, sc = Math.min(W / 1600, H / 1000) * f.s;
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H);
    ctx.translate(W / 2, H / 2); ctx.scale(sc, sc); ctx.translate(-f.x, -f.y);
    inst.render(t, -1, 0);
    var tt = svg.querySelectorAll('[data-title]'); for (var k = 0; k < tt.length; k++) tt[k].setAttribute('display', o.noTitle ? 'none' : 'inline');
    ctx.save(); ctx.translate(0, OY); SVG2Canvas.draw(ctx, svg, { vars: dark ? DARK : null }); ctx.restore();
    if (!o.noBox) { var b = STEPS[st].box; ctx.strokeStyle = '#e0a63b'; ctx.lineWidth = 4; ctx.setLineDash([14, 10]); ctx.strokeRect(b[0], b[1], b[2], b[3]); ctx.setLineDash([]) }
    if (!o.noHud) { ctx.fillStyle = dark ? '#e6efed' : '#0c665c'; ctx.font = '800 34px Inter, Arial, sans-serif'; ctx.textAlign = 'right';
      ctx.fillText('Parts pressed: ' + (inst.count || 0), 1560, 120) }
    ctx.restore(); return { step: st, count: inst.count };
  }
  G.S7040PAnim = { CYCLE: P, STEPS: STEPS, stepAt: stepAt, render: render };
})(window);
