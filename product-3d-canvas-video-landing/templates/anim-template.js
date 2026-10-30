/* p3cv animation module template  ------------------------------------------------------------
   CONTRACT (used by the landing section, the video "mechanism" scene and the thumbnail):
     window.<GLOBAL> = {
       CYCLE:  number            // seconds of one full machine cycle (loops)
       STEPS:  [{a, b, name, box:[x,y,w,h]}]   // step time window [a,b) in cycle seconds, label,
                                 //  and the world-space box highlighted while the step runs
       stepAt(t) -> index        // step index for cycle time t
       render(ctx, W, H, opts)   // draw frame; opts = {t, theme:'dark'|'light', focus:{x,y,s},
                                 //  noBox, noHud, noLabels} - unknown opts must be ignored
     }
   World space is 1600 x 1000 units, scaled to fit W x H; focus {x,y,s} centres/zooms the camera
   (the 9:16 video uses s~1.9 and can track x per step via video.scenes[].track).
   Keep it schematic: simplified side view of the real mechanism, true to the 3D drawing; label
   anything inferred as such in the landing copy and SEO notes.
   Rename MyAnim to your product (e.g. JawAnim) and set anim.global in product.json.
-------------------------------------------------------------------------------------------- */
(function (G) {
  var CYCLE = 8, C = { primary: '#0056b3', accent: '#38BDF8', part: '#f59e0b' };
  var STEPS = [
    { a: 0, b: 2, name: 'Step one', box: [200, 300, 400, 400] },
    { a: 2, b: 4, name: 'Step two', box: [600, 300, 400, 400] },
    { a: 4, b: 6, name: 'Step three', box: [1000, 300, 400, 400] },
    { a: 6, b: 8, name: 'Return', box: [200, 150, 1200, 600] }];
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x }
  function ez(x) { x = cl(x); return x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2 }
  function seg(t, a, b) { return ez((t - a) / (b - a)) }
  function stepAt(t) { t = ((t % CYCLE) + CYCLE) % CYCLE; for (var i = 0; i < STEPS.length; i++) if (t < STEPS[i].b) return i; return STEPS.length - 1 }
  function state(t) { // ALL motion is a pure function of t -> frame-exact video rendering
    var x = t < 6 ? 400 + 800 * seg(t, 0, 6) : 1200 - 800 * seg(t, 6, 8);
    return { x: x, y: 560 };
  }
  function render(ctx, W, H, o) {
    o = o || {}; var dark = o.theme !== 'light', t = ((o.t || 0) % CYCLE + CYCLE) % CYCLE, st = stepAt(t), s = state(t);
    var f = o.focus || { x: 800, y: 500, s: 1 }, sc = Math.min(W / 1600, H / 1000) * f.s;
    ctx.save(); ctx.clearRect(0, 0, W, H); ctx.translate(W / 2, H / 2); ctx.scale(sc, sc); ctx.translate(-f.x, -f.y);
    ctx.fillStyle = dark ? '#334155' : '#cbd5e1'; ctx.fillRect(150, 640, 1300, 40);           // base / rail
    ctx.fillStyle = C.part; ctx.fillRect(s.x - 60, s.y - 80, 120, 80);                         // moving part
    if (!o.noLabels) { ctx.fillStyle = dark ? '#e2e8f0' : '#0f172a'; ctx.font = '700 24px Arial'; ctx.textAlign = 'center'; ctx.fillText('PART', s.x, s.y - 100) }
    if (!o.noHud) { ctx.fillStyle = C.primary; ctx.font = '800 40px Arial'; ctx.textAlign = 'left'; ctx.fillText('x = ' + Math.round(s.x), 1150, 120) }
    if (!o.noBox) { var b = STEPS[st].box; ctx.strokeStyle = C.accent; ctx.lineWidth = 4; ctx.setLineDash([14, 10]); ctx.strokeRect(b[0], b[1], b[2], b[3]) }
    ctx.restore(); return { step: st };
  }
  G.MyAnim = { CYCLE: CYCLE, STEPS: STEPS, stepAt: stepAt, render: render, state: state };
})(window);
