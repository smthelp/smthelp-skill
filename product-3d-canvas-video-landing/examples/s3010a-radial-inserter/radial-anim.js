/* S3010A radial insertion cycle - schematic side view (p3cv anim contract, global RadialAnim).
   Sources: S3010A operation manual 2.1/2.3 (sequencer -> chain clips -> CTA -> insertion head cuts
   from tape, forms, inserts; X/Y table + turntable position the PCB; cut & clinch unit cuts and
   clinches from below and checks insertion), PPT/landing (10 feeders, N-type clinch, vision). */
(function (G) {
  var CYCLE = 12, HX = 1200, BOARD_Y = 640, BOARD_H = 20;
  var C = { teal: '#009fa5', tealD: '#087d86', lime: '#82bf32', warm: '#f4b740', cap: '#2563eb', red: '#ef4444' };
  var STEPS = [
    { a: 0, b: 2, name: 'Sequencer feeds the part', box: [130, 90, 820, 280] },
    { a: 2, b: 3.5, name: 'Chain carries it in program order', box: [130, 250, 1010, 150] },
    { a: 3.5, b: 5, name: 'CTA transfers to the head', box: [1020, 260, 260, 260] },
    { a: 5, b: 6.5, name: 'Head cuts the tape and forms the leads', box: [1100, 200, 220, 400] },
    { a: 6.5, b: 8, name: 'X/Y table + vision position the PCB', box: [560, 520, 1000, 230] },
    { a: 8, b: 9.5, name: 'Insert leads into the holes', box: [1080, 380, 240, 360] },
    { a: 9.5, b: 11, name: 'Cut & clinch from below', box: [1080, 600, 240, 260] },
    { a: 11, b: 12, name: 'Head returns, next part', box: [130, 90, 1420, 760] }];
  var FEED = [200, 320, 440, 560, 680, 800], HOLES = [-250, -150, -50, 50, 150, 250];
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x }
  function ez(x) { x = cl(x); return x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2 }
  function seg(t, a, b) { return ez((t - a) / (b - a)) }
  function stepAt(t) { t = ((t % CYCLE) + CYCLE) % CYCLE; for (var i = 0; i < STEPS.length; i++) if (t < STEPS[i].b) return i; return STEPS.length - 1 }
  function state(T) {
    var n = Math.floor(T / CYCLE), t = T - n * CYCLE, k = ((n % 6) + 6) % 6, fx = FEED[k];
    var s = { t: t, k: k, fx: fx, tape: 1, lead: 70, bend: 0, show: true };
    // part position (centre of body bottom)
    if (t < 2) { s.px = fx; s.py = 230 + 100 * seg(t, 0.3, 1.8) }
    else if (t < 3.5) { s.px = fx + (1080 - fx) * seg(t, 2, 3.5); s.py = 330 }
    else if (t < 5) { var q = seg(t, 3.5, 5); s.px = 1080 + (HX - 1080) * q; s.py = 330 + 140 * q - 60 * Math.sin(Math.PI * q) }
    // head bottom
    var hb = 470;
    if (t >= 8 && t < 9.5) hb = 470 + 170 * seg(t, 8, 9.2);
    else if (t >= 9.5 && t < 11) hb = 640;
    else if (t >= 11) hb = 640 - 170 * seg(t, 11, 11.9);
    s.hb = hb;
    if (t >= 5) { s.px = HX; s.py = t >= 9.5 ? BOARD_Y : Math.min(hb, BOARD_Y) }
    if (t >= 5) s.tape = 1 - seg(t, 5.2, 5.8);
    s.tapeDrop = t >= 5.2 && t < 7 ? 260 * seg(t, 5.4, 6.8) : 0;
    if (t >= 9.5) { s.lead = 70 - 40 * seg(t, 9.9, 10.3); s.bend = seg(t, 10.3, 10.9) }
    if (t >= 11) s.bend = 1, s.lead = 30;
    // cutter (anvil) top
    s.cut = 860; if (t >= 9.5 && t < 11) s.cut = 860 - 190 * seg(t, 9.5, 9.95); if (t >= 10.9 && t < 11) s.cut = 670 + 190 * seg(t, 10.9, 11);
    // board x: hole k under the head
    var bxPrev = HX - HOLES[(k + 5) % 6], bxNow = HX - HOLES[k];
    s.bx = t < 6.5 ? bxPrev : t < 8 ? bxPrev + (bxNow - bxPrev) * seg(t, 6.5, 7.9) : bxNow;
    if (k === 0 && t < 8) { s.bx = t < 6.5 ? 300 : 300 + (bxNow - 300) * seg(t, 6.5, 7.9) } // new board from loader
    s.done = k; // parts already inserted on this board
    return s;
  }
  function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath() }
  function part(ctx, x, y, o) { // y = bottom of body; leads go down
    var L = o.lead == null ? 70 : o.lead, b = o.bend || 0, sp = 9;
    ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 4; ctx.lineCap = 'round';
    [-1, 1].forEach(function (d) {
      var lx = x + d * sp; ctx.beginPath(); ctx.moveTo(lx, y);
      if (b > 0 && o.board) { var straight = BOARD_Y + BOARD_H - y + 6; ctx.lineTo(lx, y + straight); var rem = L - (straight - (BOARD_Y - y)); rem = Math.max(rem, 14); var ang = (90 - 60 * b) * Math.PI / 180; ctx.lineTo(lx - d * Math.cos(ang) * rem * 0.9, y + straight + Math.sin(ang) * rem * 0.9) }
      else ctx.lineTo(lx, y + L);
      ctx.stroke();
    });
    ctx.fillStyle = C.cap; rr(ctx, x - 22, y - 62, 44, 62, 9); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.75)'; ctx.fillRect(x + 10, y - 58, 6, 54);
    ctx.fillStyle = '#93c5fd'; ctx.fillRect(x - 22, y - 62, 44, 6);
    if (o.tape > 0.02) { ctx.globalAlpha = o.tape; ctx.fillStyle = '#f8fafc'; ctx.fillRect(x - 34, y + L - 26 + (o.drop || 0), 68, 22); ctx.fillStyle = '#94a3b8'; ctx.beginPath(); ctx.arc(x, y + L - 15 + (o.drop || 0), 4, 0, 7); ctx.fill(); ctx.globalAlpha = 1 }
  }
  function label(ctx, txt, x, y, dark, al) { ctx.font = '700 22px Arial'; ctx.textAlign = al || 'center'; ctx.fillStyle = dark ? '#cbd5e1' : '#334155'; ctx.fillText(txt, x, y) }
  function render(ctx, W, H, o) {
    o = o || {}; var dark = o.theme !== 'light', T = o.t || 0, s = state(T), t = s.t, st = stepAt(t);
    var f = o.focus || { x: 800, y: 500, s: 1 }, sc = Math.min(W / 1600, H / 1000) * f.s, lab = !o.noLabels;
    var metal = dark ? '#475569' : '#94a3b8', metalD = dark ? '#334155' : '#64748b', frame = dark ? '#1e293b' : '#e2e8f0';
    ctx.save(); ctx.clearRect(0, 0, W, H); ctx.translate(W / 2, H / 2); ctx.scale(sc, sc); ctx.translate(-f.x, -f.y);
    // cross beam + feeders (sequencer)
    ctx.fillStyle = frame; ctx.fillRect(140, 84, 1000, 22);
    FEED.forEach(function (x, i) {
      var act = i === s.k && t < 2;
      ctx.fillStyle = act ? C.teal : metal; rr(ctx, x - 40, 106, 80, 110, 8); ctx.fill();
      ctx.fillStyle = metalD; ctx.fillRect(x - 12, 216, 24, 18);
      ctx.strokeStyle = dark ? '#64748b' : '#94a3b8'; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(x, 150, 26, 0, 7); ctx.stroke();
      ctx.fillStyle = act ? '#fff' : (dark ? '#cbd5e1' : '#f8fafc'); ctx.font = '700 18px Arial'; ctx.textAlign = 'center'; ctx.fillText(String(i + 1), x, 157);
    });
    if (lab) label(ctx, 'Feeder stations · sequencer', 520, 70, dark);
    // chain with clips
    ctx.fillStyle = metalD; rr(ctx, 140, 318, 980, 26, 13); ctx.fill();
    var off = t >= 2 && t < 3.5 ? 60 * ((t - 2) / 1.5 * 4 % 1) : 0;
    ctx.fillStyle = dark ? '#94a3b8' : '#475569';
    for (var cx = 150 + off; cx < 1110; cx += 60) ctx.fillRect(cx - 6, 310, 12, 42);
    if (lab) label(ctx, 'Chain clips (program order)', 300, 392, dark);
    // CTA arm
    var ca = t >= 3.5 && t < 5 ? seg(t, 3.5, 5) : 0;
    ctx.fillStyle = t >= 3.5 && t < 5 ? C.warm : metal; ctx.save(); ctx.translate(1080, 340); ctx.rotate(-0.5 + 0.9 * ca); rr(ctx, -14, -14, 150, 28, 12); ctx.fill(); ctx.restore();
    ctx.fillStyle = metalD; ctx.beginPath(); ctx.arc(1080, 340, 20, 0, 7); ctx.fill();
    if (lab) label(ctx, 'CTA', 1060, 300, dark);
    // insertion head column
    ctx.fillStyle = frame; ctx.fillRect(1150, 120, 100, 80);
    ctx.fillStyle = st >= 3 && st <= 5 ? C.teal : metal; rr(ctx, 1165, 190, 70, s.hb - 62 - 190, 10); ctx.fill();
    ctx.fillStyle = metalD; ctx.fillRect(1172, s.hb - 66, 12, 10); ctx.fillRect(1216, s.hb - 66, 12, 10);
    if (lab) label(ctx, 'Insertion head', 1340, 170, dark, 'left');
    // camera
    ctx.fillStyle = dark ? '#0f172a' : '#1e293b'; rr(ctx, 1262, 230, 60, 44, 8); ctx.fill(); ctx.fillStyle = C.lime; ctx.beginPath(); ctx.arc(1292, 274, 9, 0, 7); ctx.fill();
    if (t >= 6.5 && t < 8) { ctx.strokeStyle = C.lime; ctx.lineWidth = 3; ctx.setLineDash([10, 8]); ctx.beginPath(); ctx.moveTo(1292, 282); ctx.lineTo(1215, BOARD_Y - 4); ctx.stroke(); ctx.setLineDash([]); ctx.beginPath(); ctx.arc(1200, BOARD_Y - 4, 16 + 6 * Math.sin(t * 9), 0, 7); ctx.stroke() }
    if (lab) label(ctx, 'Vision', 1340, 262, dark, 'left');
    // X/Y table + turntable + PCB
    ctx.fillStyle = frame; ctx.fillRect(560, 700, 1000, 16);
    ctx.fillStyle = metal; var tl = s.bx - 330, tr = s.bx + 330; if (HX - 55 > tl) { rr(ctx, tl, 668, Math.min(HX - 55, tr) - tl, 22, 6); ctx.fill() } if (HX + 55 < tr) { var l2 = Math.max(HX + 55, tl); rr(ctx, l2, 668, tr - l2, 22, 6); ctx.fill() }
    ctx.fillStyle = metalD; ctx.beginPath(); ctx.ellipse(s.bx, 690, 90, 12, 0, 0, 7); ctx.fill();
    ctx.fillStyle = '#15803d'; ctx.fillRect(s.bx - 300, BOARD_Y, 600, BOARD_H);
    ctx.fillStyle = '#facc15'; HOLES.forEach(function (h) { ctx.fillRect(s.bx + h - 12, BOARD_Y - 3, 6, 3); ctx.fillRect(s.bx + h + 6, BOARD_Y - 3, 6, 3) });
    for (var j = 0; j < s.done; j++) part(ctx, s.bx + HOLES[j], BOARD_Y, { lead: 30, bend: 1, board: 1, tape: 0 });
    if (lab) { label(ctx, 'PCB on X/Y table + turntable', 760, 760, dark); }
    // cut & clinch unit
    ctx.fillStyle = st === 6 ? C.warm : metal; rr(ctx, 1160, s.cut, 80, 120, 8); ctx.fill();
    ctx.fillStyle = metalD; ctx.beginPath(); ctx.moveTo(1170, s.cut); ctx.lineTo(1200, s.cut - 18); ctx.lineTo(1230, s.cut); ctx.fill();
    if (lab) label(ctx, 'Cut & clinch (N-type)', 1290, 930, dark, 'left');
    if (t >= 9.9 && t < 10.4) { ctx.fillStyle = C.red; ctx.globalAlpha = 1 - (t - 9.9) / 0.5; [-1, 1].forEach(function (d) { ctx.fillRect(1200 + d * 9 - 3, 700 + 60 * (t - 9.9), 6, 30) }); ctx.globalAlpha = 1 }
    // the active part
    if (t < 5) part(ctx, s.px, s.py, { tape: 1 });
    else part(ctx, s.px, s.py, { tape: s.tape, drop: s.tapeDrop, lead: s.lead, bend: s.bend, board: t >= 9.5 });
    if (t >= 5.1 && t < 5.7) { ctx.strokeStyle = C.red; ctx.lineWidth = 4; var yy = s.py + 44; ctx.beginPath(); ctx.moveTo(1160, yy); ctx.lineTo(1240, yy); ctx.stroke() }
    if (!o.noHud) {
      ctx.textAlign = 'left'; ctx.fillStyle = C.teal; ctx.font = '800 30px Arial'; ctx.fillText('S3010A · ' + (st + 1) + '/8', 150, 470);
      ctx.fillStyle = dark ? '#f8fafc' : '#0f172a'; ctx.font = '700 26px Arial'; ctx.fillText(STEPS[st].name, 150, 510);
      ctx.fillStyle = dark ? '#94a3b8' : '#475569'; ctx.font = '600 22px Arial'; ctx.fillText('Parts on this board: ' + (s.done + (t >= 9.5 ? 1 : 0)) + ' / 6', 150, 548);
    }
    if (!o.noBox) { var b = STEPS[st].box; ctx.strokeStyle = C.lime; ctx.lineWidth = 4; ctx.setLineDash([14, 10]); ctx.strokeRect(b[0], b[1], b[2], b[3]); ctx.setLineDash([]) }
    ctx.restore(); return { step: st };
  }
  G.RadialAnim = { CYCLE: CYCLE, STEPS: STEPS, stepAt: stepAt, render: render, state: state };
})(window);
