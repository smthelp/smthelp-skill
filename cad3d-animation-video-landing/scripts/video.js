// Video timeline renderer for CN-SM-2713 marketing film (16:9 + 9:16)
import { createStage, ease, seg, lerp, lerp3, orbit, clamp01, ANCHORS } from './engine.js';

const TEAL = '#00C2AD', TEAL2 = '#00A896', SKY = '#38BDF8', AMBER = '#F5B13D', LIME = '#84CC16', NAVY = '#0B132B', DARK = '#070D1E';

let stage, out, ctx, glCanvas, W, H, LW, LH, S, portrait, VO, scenes, logoImg, TOTAL;

function buildTimeline(vo) {
  const by = {}; let t = 0.6; const list = [];
  for (const s of vo) {
    const extra = s.id === 'cta' ? 4.6 : 1.25;
    const sc = { id: s.id, start: t, voStart: t + 0.4, len: s.dur + 0.4 + extra, words: s.words, text: s.text };
    sc.end = sc.start + sc.len; list.push(sc); by[s.id] = sc; t = sc.end;
  }
  // caption tokens aligned to word timings
  for (const sc of list) {
    const toks = sc.text.split(/\s+/);
    sc.tokens = sc.words.map((w, i) => ({ a: sc.voStart + w[0], b: sc.voStart + w[1], txt: toks.length === sc.words.length ? toks[i] : w[2] }));
    for (const k of sc.tokens) {
      const m = { 'eight-point-five': '8.5', 'millimeter': 'mm', 'smthelp': 'smthelp.com.', 'dot': '', 'com.': '', 'Twenty-one': '21' };
      if (k.txt in m) k.txt = m[k.txt];
    }
    sc.tokens = sc.tokens.filter(k => k.txt);
    // chunk into caption lines
    const chunks = []; let cur = [];
    for (const k of sc.tokens) {
      cur.push(k); const len = cur.map(x => x.txt).join(' ').length;
      if (/[.,:;?!]$/.test(k.txt) && len > 14 || len > (portrait ? 26 : 40)) { chunks.push(cur); cur = []; }
    }
    if (cur.length) chunks.push(cur);
    sc.chunks = chunks.map((c, i) => ({ toks: c, a: c[0].a, b: (i < chunks.length - 1 ? chunks[i + 1][0].a : c[c.length - 1].b + 0.6) }));
  }
  TOTAL = t;
  return { list, by };
}
function wordT(sc, word, nth = 0) { // absolute time of the n-th occurrence of a spoken word
  let k = 0; for (const w of sc.words) if (w[2].toLowerCase().startsWith(word.toLowerCase())) { if (k++ === nth) return sc.voStart + w[0]; }
  return sc.voStart;
}

// ---------------------------------------------------------------- drawing helpers
function font(px, wt = 700, fam = 'Inter') { return `${wt} ${px}px ${fam}`; }
function rr(x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
function fadeIO(t, a, b, fi = 0.45, fo = 0.45) { return Math.min(ease.out(seg(t, a, a + fi)), 1 - ease.in(seg(t, b - fo, b))); }

let bgCache = null, vigCache = null;
function drawBG(t) {
  if (bgCache) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(bgCache, 0, 0); ctx.restore(); return; }
  const g = ctx.createRadialGradient(LW * (portrait ? 0.5 : 0.66), LH * (portrait ? 0.38 : 0.45), 10, LW * 0.6, LH * 0.5, Math.max(LW, LH) * 0.85);
  g.addColorStop(0, '#16305a'); g.addColorStop(0.45, '#0B132B'); g.addColorStop(1, '#04070f');
  ctx.fillStyle = g; ctx.fillRect(0, 0, LW, LH);
  ctx.strokeStyle = 'rgba(255,255,255,0.035)'; ctx.lineWidth = 1;
  const off = 0;
  for (let x = -48 + off; x < LW; x += 48) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, LH); ctx.stroke(); }
  for (let y = -48 + off; y < LH; y += 48) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(LW, y); ctx.stroke(); }
}
function drawVignette() {
  if (vigCache) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(vigCache, 0, 0); ctx.restore(); return; }
  const g = ctx.createRadialGradient(LW / 2, LH / 2, Math.min(LW, LH) * 0.35, LW / 2, LH / 2, Math.max(LW, LH) * 0.75);
  g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0.55)'); ctx.fillStyle = g; ctx.fillRect(0, 0, LW, LH);
}
function drawBrand(t) {
  const a = clamp01(seg(t, 0.8, 1.8)) * (1 - seg(t, scenes.by.cta.start + 0.2, scenes.by.cta.start + 1.0));
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha = a;
  const x = portrait ? 48 : 64, y = portrait ? 64 : 52;
  rr(x, y, 210, 58, 12); ctx.fillStyle = 'rgba(255,255,255,0.96)'; ctx.fill();
  if (logoImg) ctx.drawImage(logoImg, x + 12, y + 7, 186, 186 * 83 / 300);
  ctx.font = font(15, 600, 'JetBrains Mono'); ctx.fillStyle = 'rgba(255,255,255,0.7)'; ctx.textBaseline = 'middle';
  ctx.fillText('CN-SM-2713  ·  JUKI GRIPPER NOZZLE', x + 228, y + 29);
  ctx.restore();
}
function textBlock(t, a, b, kicker, head, sub, opt = {}) {
  const al = fadeIO(t, a, b); if (al <= 0) return;
  const slide = (1 - ease.out(seg(t, a, a + 0.7))) * 40;
  ctx.save(); ctx.globalAlpha = al; ctx.textBaseline = 'alphabetic';
  let x = opt.x ?? (portrait ? 64 : 110), y = opt.y ?? (portrait ? 250 : 330);
  const maxW = opt.w ?? (portrait ? LW - 128 : 720);
  ctx.translate(-slide * (portrait ? 0 : 1), portrait ? slide * 0.6 : 0);
  if (kicker) {
    ctx.font = font(portrait ? 26 : 24, 700, 'JetBrains Mono'); ctx.fillStyle = TEAL;
    ctx.fillRect(x, y - 22, 6, 28); ctx.fillText(kicker, x + 20, y); y += Math.max(portrait ? 82 : 76, (opt.hs ?? 70) * 1.05);
  }
  const hs = opt.hs ?? (portrait ? 74 : 70);
  ctx.font = font(hs, 800); ctx.fillStyle = '#fff';
  for (const line of wrap(head, maxW)) { ctx.fillText(line, x, y); y += hs * 1.1; }
  if (sub) {
    y += 10; const ss = portrait ? 34 : 30; ctx.font = font(ss, 500); ctx.fillStyle = 'rgba(226,232,240,0.86)';
    for (const line of wrap(sub, maxW)) { ctx.fillText(line, x, y); y += ss * 1.4; }
  }
  ctx.restore();
  return y;
}
function wrap(txt, maxW) {
  const words = txt.split(' '); const lines = []; let cur = '';
  for (const w of words) { const tst = cur ? cur + ' ' + w : w; if (ctx.measureText(tst).width > maxW && cur) { lines.push(cur); cur = w; } else cur = tst; }
  if (cur) lines.push(cur); return lines;
}
function chips(t, a, b, items, x, y, colors) {
  const al = fadeIO(t, a, b); if (al <= 0) return;
  ctx.save(); ctx.font = font(portrait ? 28 : 25, 600); ctx.textBaseline = 'middle';
  let cx = x, cy = y;
  items.forEach((it, i) => {
    const ai = al * ease.out(seg(t, a + 0.15 * i, a + 0.15 * i + 0.5)); if (ai <= 0) return;
    const w = ctx.measureText(it).width + 44, h = portrait ? 58 : 52;
    if (cx + w > LW - 40) { cx = x; cy += h + 14; }
    ctx.globalAlpha = ai; rr(cx, cy, w, h, h / 2);
    ctx.fillStyle = 'rgba(0,194,173,0.12)'; ctx.fill(); ctx.strokeStyle = (colors && colors[i]) || TEAL; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.fillText(it, cx + 22, cy + h / 2 + 1); cx += w + 14;
  });
  ctx.restore();
}
function P(anchor, inRig = true) { const p = stage.project(anchor, LW, LH, inRig); return p; }
function callout(t, a, b, anchor, label, side = 'r', opt = {}) {
  const al = fadeIO(t, a, b, 0.35, 0.35); if (al <= 0) return;
  const p = opt.screen || P(anchor);
  const dx = (opt.dx ?? (portrait ? 150 : 210)) * (side === 'r' ? 1 : -1), dy = opt.dy ?? -70;
  const grow = ease.out(seg(t, a, a + 0.5));
  ctx.save(); ctx.globalAlpha = al;
  const col = opt.color || TEAL;
  // pulse ring
  const pr = 10 + 10 * ((t * 1.4) % 1);
  ctx.strokeStyle = col; ctx.globalAlpha = al * (1 - ((t * 1.4) % 1)); ctx.lineWidth = 2.5;
  ctx.beginPath(); ctx.arc(p[0], p[1], pr, 0, 7); ctx.stroke(); ctx.globalAlpha = al;
  ctx.fillStyle = col; ctx.beginPath(); ctx.arc(p[0], p[1], 7, 0, 7); ctx.fill();
  ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(p[0], p[1], 3, 0, 7); ctx.fill();
  const ex = p[0] + dx * 0.55, ey = p[1] + dy, fx = p[0] + dx, fy = ey;
  ctx.strokeStyle = col; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(p[0], p[1]);
  const k1 = Math.min(1, grow * 2), k2 = clamp01(grow * 2 - 1);
  ctx.lineTo(lerp(p[0], ex, k1), lerp(p[1], ey, k1)); if (k2 > 0) ctx.lineTo(lerp(ex, fx, k2), fy); ctx.stroke();
  if (grow > 0.6) {
    ctx.globalAlpha = al * seg(grow, 0.6, 1);
    const fs = portrait ? 30 : 28; ctx.font = font(fs, 700); ctx.textBaseline = 'middle';
    const tw = ctx.measureText(label).width; const sub = opt.sub; let sw = 0;
    if (sub) { ctx.font = font(fs * 0.72, 500); sw = ctx.measureText(sub).width; }
    const bw = Math.max(tw, sw) + 40, bh = sub ? fs * 2.6 : fs * 1.75;
    const bx = side === 'r' ? fx : fx - bw, by = fy - bh / 2;
    rr(bx, by, bw, bh, 10); ctx.fillStyle = 'rgba(7,13,30,0.86)'; ctx.fill(); ctx.strokeStyle = col; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = col; ctx.fillRect(side === 'r' ? bx : bx + bw - 5, by + 8, 5, bh - 16);
    ctx.fillStyle = '#fff'; ctx.font = font(fs, 700); ctx.fillText(label, bx + 20, sub ? by + bh * 0.36 : by + bh / 2 + 1);
    if (sub) { ctx.font = font(fs * 0.72, 500); ctx.fillStyle = 'rgba(203,213,225,0.95)'; ctx.fillText(sub, bx + 20, by + bh * 0.72); }
  }
  ctx.restore();
}
function arrow(x1, y1, x2, y2, col, w = 6, head = 22) {
  ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = w; ctx.lineCap = 'round';
  const ang = Math.atan2(y2 - y1, x2 - x1);
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2 - Math.cos(ang) * head * 0.8, y2 - Math.sin(ang) * head * 0.8); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(x2, y2); ctx.lineTo(x2 - head * Math.cos(ang - 0.45), y2 - head * Math.sin(ang - 0.45)); ctx.lineTo(x2 - head * Math.cos(ang + 0.45), y2 - head * Math.sin(ang + 0.45)); ctx.closePath(); ctx.fill();
}
function captions(t) {
  for (const sc of scenes.list) {
    for (const ch of sc.chunks) {
      if (t < ch.a || t >= ch.b) continue;
      const al = Math.min(1, (t - ch.a) / 0.08 + 0.3, (ch.b - t) / 0.08 + 0.3);
      ctx.save(); ctx.globalAlpha = clamp01(al);
      const fs = portrait ? 50 : 46; ctx.font = font(fs, 800); ctx.textBaseline = 'middle';
      const parts = ch.toks.map(k => k.txt); const sp = ctx.measureText(' ').width;
      const widths = parts.map(p => ctx.measureText(p).width); const total = widths.reduce((a, b) => a + b, 0) + sp * (parts.length - 1);
      const cy = portrait ? (t > scenes.by.cta.start ? LH * 0.93 : LH * 0.795) : LH - 104; const bx = LW / 2 - total / 2 - 30, bw = total + 60, bh = fs * 1.7;
      rr(bx, cy - bh / 2, bw, bh, 14); ctx.fillStyle = 'rgba(4,8,18,0.72)'; ctx.fill();
      let x = LW / 2 - total / 2;
      ch.toks.forEach((k, i) => {
        const active = t >= k.a - 0.03 && t < (ch.toks[i + 1] ? ch.toks[i + 1].a : ch.b);
        const spoken = t >= k.a - 0.03;
        ctx.fillStyle = active ? TEAL : spoken ? '#ffffff' : 'rgba(255,255,255,0.55)';
        ctx.fillText(k.txt, x, cy + 2); x += widths[i] + sp;
      });
      ctx.restore();
    }
  }
}

// ---------------------------------------------------------------- per-scene choreography
function cam(target, dist, az, el, fov = 28, shiftX = null, shiftY = null) {
  const pd = portrait ? 1.32 : 1;
  const sx = shiftX ?? (portrait ? 0 : 0.17), sy = shiftY ?? (portrait ? 0.09 : -0.045);
  stage.setCamera(orbit(target, dist * pd, az, el), target, fov, W, H, sx, sy);
}
function camBlend(A, B, k) { // A,B = [target,dist,az,el,fov,sx,sy]
  const kk = ease.io(clamp01(k));
  const tg = lerp3(A[0], B[0], kk);
  cam(tg, lerp(A[1], B[1], kk), lerp(A[2], B[2], kk), lerp(A[3], B[3], kk), lerp(A[4] ?? 28, B[4] ?? 28, kk), A[5] == null ? null : lerp(A[5], B[5], kk), A[6] == null ? null : lerp(A[6], B[6], kk));
}

function frame(t) {
  const { by } = scenes;
  const st = { open: 0, explode: 0, cut: 0, highlight: {}, rigPos: [0, 0, 0], coilPos: [0, 0, 0], coilAttached: true, props: false, rigRotY: 0, coilVisible: true };
  let overlay = () => { };
  const sid = scenes.list.find(s => t >= s.start && t < s.end)?.id || (t < 0.6 ? 'hook' : 'cta');
  const sc = by[sid]; const lt = t - sc.start; const L = sc.len;
  const PS = portrait; // shorthand
  const yClip = { on: false };

  if (sid === 'hook') {
    // coil alone, then the gripper drops in and grabs it
    const arrive = sc.end - 3.2, grab = sc.end - 1.25;
    st.coilAttached = false;
    const wob = Math.sin((t - sc.start) * 7) * 0.05 * seg(t, wordT(sc, 'tilt') - 0.2, wordT(sc, 'tilt') + 0.2) * (1 - seg(t, wordT(sc, 'leads') + 0.4, wordT(sc, 'leads') + 0.9));
    stage.coilG.rotation.z = wob;
    const k = ease.io(seg(t, arrive, grab - 0.1));
    st.rigPos = [0, lerp(70, 0, k), 0];
    st.open = 1 - ease.io(seg(t, grab, grab + 0.35));
    st.coilPos = [0, 0, 0];
    const A = [[0, -26, 0], 62, 20, 10, 28], B = [[0, -12, 0], 125, 42, 12, 28];
    camBlend([[0, -27, 0], 70, -10, 6, 28], A, seg(lt, 0, 3));
    if (lt > 3) camBlend(A, B, seg(t, arrive - 1.0, sc.end));
    overlay = () => {
      const blockY = PS ? 260 : 300;
      textBlock(t, sc.start + 0.4, arrive + 0.6, 'THE ODD-FORM PROBLEM', 'Heavy. Round. Hard to hold.', null, PS ? { y: blockY } : { x: 110, y: 330, w: 640 });
      const tags = [['✕  Tilt', wordT(sc, 'tilt')], ['✕  Slip', wordT(sc, 'slip')], ['✕  Bent leads', wordT(sc, 'bend')]];
      tags.forEach(([lab, ta], i) => {
        const al = fadeIO(t, ta, arrive + 0.6, 0.25, 0.4); if (al <= 0) return;
        ctx.save(); ctx.globalAlpha = al; ctx.font = font(PS ? 38 : 36, 800); ctx.textBaseline = 'middle';
        const x = PS ? 64 + i * 300 : 110, y = PS ? 520 : 560 + i * 78; const w = ctx.measureText(lab).width + 48;
        rr(x, y - 30, w, 60, 12); ctx.fillStyle = 'rgba(239,68,68,0.16)'; ctx.fill(); ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 2; ctx.stroke();
        ctx.fillStyle = '#fecaca'; ctx.fillText(lab, x + 24, y + 2); ctx.restore();
      });
    };
  }
  else if (sid === 'title') {
    st.rigRotY = lerp(0.5, -0.35, ease.io(seg(lt, 0, L)));
    const A = [[0, -12, 0], 125, 42, 12], B = [[0, -11, 0], 112, 10, 16];
    camBlend(A, B, seg(lt, 0, L));
    // gentle demonstration of the jaw action
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, 'INTRODUCING', 'CN-SM-2713', 'Custom gripper nozzle for JUKI odd-form insertion machines', PS ? { hs: 104 } : { hs: 108, y: 300 });
      chips(t, wordT(sc, 'engineered') - 0.2, sc.end - 0.1, ['Ø8.5 mm coil', 'JUKI JM / KE series', 'Spring-closed jaws'], PS ? 64 : 110, PS ? 600 : 640);
    };
  }
  else if (sid === 'shank') {
    const pulse = 0.5 + 0.5 * Math.sin(lt * 5);
    st.highlight = { nozzle: seg(lt, 0.4, 1.0) * (0.35 + 0.4 * pulse) * (1 - seg(lt, L - 0.8, L)) };
    camBlend([[0, -11, 0], 112, 10, 16], [[0, 3, 0], 92, 38, 20], seg(lt, 0, 2.2));
    if (lt > 2.2) camBlend([[0, 3, 0], 92, 38, 20], [[0, 1, 0], 96, 18, 14], seg(lt, 2.2, L));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '01 · PLUG & PLAY', 'JUKI-standard nozzle shank', 'Drops straight into your nozzle changer. No adapters. No head modifications.');
      callout(t, wordT(sc, 'shank') - 0.3, sc.end - 0.2, ANCHORS.shank, 'JUKI-standard shank', PS ? 'r' : 'r', { dx: PS ? 120 : 190, dy: -60, sub: 'Native tool-changer fit' });
    };
  }
  else if (sid === 'mech') {
    st.cut = ease.io(seg(lt, 0.0, 1.4));
    const tDown = wordT(sc, 'down') - 0.2, tOpen = wordT(sc, 'open') - 0.1, tClose = wordT(sc, 'snaps') - 0.05;
    st.open = ease.io(seg(t, tDown, tOpen + 0.2)) * (1 - ease.out(seg(t, tClose, tClose + 0.28)));
    // second quick cycle at the end
    const tEnd = sc.end - 1.25; st.open = Math.max(st.open, Math.sin(Math.PI * seg(t, tEnd, tEnd + 1.0)));
    st.highlight = {
      plunger: fadeIO(t, wordT(sc, 'plunger') - 0.1, wordT(sc, 'center') - 0.1, 0.2, 0.3) + fadeIO(t, wordT(sc, 'plunger', 1) - 0.1, wordT(sc, 'moves') + 0.6, 0.2, 0.3),
      spring: fadeIO(t, wordT(sc, 'spring') - 0.1, wordT(sc, 'plunger') + 0.3, 0.2, 0.3) + fadeIO(t, wordT(sc, 'spring', 1) - 0.1, sc.end, 0.2, 0.3),
      pinC: fadeIO(t, wordT(sc, 'center') - 0.1, wordT(sc, 'As') + 0.2, 0.2, 0.3) + fadeIO(t, wordT(sc, 'pin', 1) - 0.1, wordT(sc, 'arms') + 0.3, 0.2, 0.3),
      jawL: fadeIO(t, wordT(sc, 'jaw') - 0.1, wordT(sc, 'Release'), 0.2, 0.3), jawR: fadeIO(t, wordT(sc, 'jaw') - 0.1, wordT(sc, 'Release'), 0.2, 0.3),
    };
    st.highlight.pin_inner = st.highlight.plunger;
    camBlend([[0, 1, 0], 96, 18, 14], [[0, -11, 0], 122, 4, 3, 28], seg(lt, 0, 1.6));
    if (lt > 1.6) camBlend([[0, -11, 0], 122, 4, 3, 28], [[0, -12, 0], 112, -6, 3, 28], seg(lt, 1.6, L));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '02 · MECHANISM', 'Spring-closed toggle jaws', 'One plunger. One center pin. Two pivot jaws.');
      const sd = PS ? 'r' : 'l';
      callout(t, wordT(sc, 'plunger') - 0.25, sc.end - 0.2, ANCHORS.plunger, 'Plunger', 'r', { dx: PS ? 130 : 200, dy: -50 });
      callout(t, wordT(sc, 'spring') - 0.25, sc.end - 0.2, ANCHORS.spring, 'Return spring', 'r', { dx: PS ? 120 : 190, dy: 40 });
      callout(t, wordT(sc, 'center') - 0.25, sc.end - 0.2, ANCHORS.pinC, 'Center pin', 'l', { dx: PS ? 140 : 210, dy: -40 });
      callout(t, wordT(sc, 'twin') - 0.25, sc.end - 0.2, ANCHORS.pivotR, 'Pivot pins', 'r', { dx: PS ? 120 : 180, dy: 70 });
      // motion arrows on plunger + jaws
      const op = fadeIO(t, tDown, tClose + 0.4, 0.2, 0.3);
      if (op > 0) {
        ctx.save(); ctx.globalAlpha = op;
        const p = P([0, -11, 4]); arrow(p[0] + (PS ? 70 : 90), p[1] - 40, p[0] + (PS ? 70 : 90), p[1] + 40, AMBER, 6, 20);
        const l = P([-7.5, -25, 2]), r = P([7.5, -25, 2]);
        const opening = t < tClose; const d = opening ? 1 : -1;
        arrow(l[0] + 10 * d, l[1], l[0] - 50 * d, l[1], AMBER, 6, 20); arrow(r[0] - 10 * d, r[1], r[0] + 50 * d, r[1], AMBER, 6, 20);
        ctx.restore();
      }
    };
  }
  else if (sid === 'grip') {
    st.cut = 1 - ease.io(seg(lt, 0, 0.8));
    const tc = wordT(sc, 'close') - 0.15;
    st.open = Math.min(ease.io(seg(lt, 0, 0.6)), 1 - ease.out(seg(t, tc, tc + 0.4)));
    const pads = fadeIO(t, wordT(sc, 'three') - 0.2, sc.end, 0.3, 0.3) * (0.55 + 0.45 * Math.sin(lt * 6));
    st.highlight = { padL1: pads, padL2: pads, padR: pads };
    yClip.on = seg(lt, 0.6, 1.4) > 0; yClip.k = ease.io(seg(lt, 0.6, 1.6)) * (1 - ease.io(seg(lt, L - 0.9, L)));
    camBlend([[0, -12, 0], 112, -6, 3], [[0, -25.3, 0], 62, 25, -72, 30, PS ? 0 : 0.17, PS ? 0.09 : -0.045], seg(lt, 0, 1.8));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '03 · 3-POINT GRIP', 'Self-centering, every time', '2 + 1 contact pins lock the round body on center.');
      const al = fadeIO(t, wordT(sc, 'That') - 0.2, sc.end - 0.15, 0.4, 0.3);
      if (al > 0) {
        const c1 = P([4.25, -25.3, 0]), c2 = P([-3.47, -25.3, 2.45]), c3 = P([-3.47, -25.3, -2.45]), c0 = P([0, -25.3, 0]);
        ctx.save(); ctx.globalAlpha = al; ctx.strokeStyle = AMBER; ctx.lineWidth = 4; ctx.setLineDash([14, 10]);
        ctx.beginPath(); ctx.moveTo(c1[0], c1[1]); ctx.lineTo(c2[0], c2[1]); ctx.lineTo(c3[0], c3[1]); ctx.closePath(); ctx.stroke(); ctx.setLineDash([]);
        for (const c of [c1, c2, c3]) { ctx.fillStyle = AMBER; ctx.beginPath(); ctx.arc(c[0], c[1], 10, 0, 7); ctx.fill(); }
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 3; const r = 26; ctx.beginPath(); ctx.moveTo(c0[0] - r, c0[1]); ctx.lineTo(c0[0] + r, c0[1]); ctx.moveTo(c0[0], c0[1] - r); ctx.lineTo(c0[0], c0[1] + r); ctx.stroke();
        ctx.restore();
      }
      callout(t, wordT(sc, 'two') - 0.2, sc.end - 0.2, [-4.6, -25.3, 0], '2 pins', 'l', { color: AMBER, dx: PS ? 130 : 190, dy: -60 });
      callout(t, wordT(sc, 'one', 1) - 0.2, sc.end - 0.2, [6.0, -25.3, 0], '1 pin', 'r', { color: AMBER, dx: PS ? 120 : 170, dy: -60 });
    };
  }
  else if (sid === 'stop') {
    const hs = fadeIO(t, sc.voStart, wordT(sc, 'Insertion'), 0.3, 0.3) * (0.6 + 0.4 * Math.sin(lt * 6));
    const hlv = fadeIO(t, wordT(sc, 'leads') - 0.2, sc.end, 0.3, 0.3) * (0.5 + 0.4 * Math.sin(lt * 6));
    st.highlight = { stop: hs, coil_leads: hlv, lead_ext: hlv };
    const sy2 = PS ? 0.15 : -0.045;
    camBlend([[0, -25.3, 0], 62, 25, -72, 30, PS ? 0 : 0.17, PS ? 0.09 : -0.045], [[0, -22, 0], PS ? 118 : 92, 88, 6, 28, PS ? 0 : 0.17, sy2], seg(lt, 0, 1.6));
    if (lt > 1.6) camBlend([[0, -22, 0], PS ? 118 : 92, 88, 6, 28, PS ? 0 : 0.17, sy2], [[0, -20, 0], PS ? 130 : 102, 66, 8, 28, PS ? 0 : 0.17, sy2], seg(lt, 1.6, L));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '04 · Z-DATUM STOP', 'Fixed depth. Straight leads.', 'Insertion force goes through the body, never the leads.');
      callout(t, wordT(sc, 'stop') - 0.25, sc.end - 0.2, ANCHORS.stop, 'Center stop pin', 'r', { color: AMBER, dx: PS ? 140 : 220, dy: -110, sub: 'Fixed Z datum' });
      const fa = fadeIO(t, wordT(sc, 'Insertion') - 0.2, wordT(sc, 'while') + 0.3, 0.3, 0.3);
      if (fa > 0) {
        const a = P([0, 16, 0]), b = P([0, -30, 0]);
        ctx.save(); ctx.globalAlpha = fa * 0.9; const off = PS ? -120 : -150;
        const k = ease.out(seg(t, wordT(sc, 'Insertion') - 0.2, wordT(sc, 'body')));
        arrow(a[0] + off, a[1], a[0] + off, lerp(a[1], b[1], k), TEAL, 10, 34);
        ctx.font = font(PS ? 28 : 26, 700); ctx.fillStyle = TEAL; ctx.textAlign = 'right'; ctx.fillText('INSERTION FORCE', a[0] + off - 24, lerp(a[1], b[1], 0.35));
        ctx.restore();
      }
      callout(t, wordT(sc, 'leads') - 0.2, sc.end - 0.2, ANCHORS.leads, 'Leads hang free', 'r', { dx: PS ? 120 : 190, dy: 30, sub: 'Untouched, straight' });
    };
  }
  else if (sid === 'explode') {
    st.explode = ease.io(seg(lt, 0.2, 2.4)) * (1 - ease.io(seg(lt, L - 2.0, L - 0.2)));
    st.rigRotY = lerp(0, 0.9, ease.io(seg(lt, 0, L)));
    st.coilVisible = true;
    const sy3 = PS ? 0.15 : -0.045, sx3 = PS ? 0 : 0.17;
    camBlend([[0, -20, 0], PS ? 130 : 102, 66, 8, 28, sx3, sy3], [[0, -8, 0], 215, 28, 16, 28, sx3, sy3], seg(lt, 0, 2.0));
    if (lt > 2) camBlend([[0, -8, 0], 215, 28, 16, 28, sx3, sy3], [[0, -10, 0], 150, 10, 12, 28, sx3, PS ? 0.09 : -0.045], seg(lt, L - 2.2, L));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '05 · BUILT TO LAST', '21 precision parts', 'E-clip–locked pivot pins. Rigid in production, easy to service.');
      const al = fadeIO(t, sc.start + 1.2, sc.end - 1.6);
      if (al > 0) callout(t, wordT(sc, 'E-clips') - 0.3, sc.end - 1.8, [-5.5, -15.6, 2.9], 'E-clip retained', 'l', { dx: PS ? 120 : 160, dy: -90 });
    };
  }
  else if (sid === 'cycle') {
    st.props = true; st.coilAttached = false;
    const T = { pick: wordT(sc, 'Pick'), seat: wordT(sc, 'Seat'), grip: wordT(sc, 'Grip'), ins: wordT(sc, 'Insert'), rel: wordT(sc, 'release'), go: wordT(sc, 'go') };
    const up = 22, tray = [-30, -6, 0], pcb = [30, -9, 0];
    let pos = [-30, up, 0], open = 0, attached = false, coilPos = tray.slice();
    const a = (x, y) => seg(t, x, y);
    open = ease.io(a(T.pick - 0.6, T.pick + 0.1));
    pos = lerp3([-30, up, 0], tray, ease.io(a(T.pick + 0.2, T.seat + 0.35)));
    if (t > T.grip - 0.15) { open = 1 - ease.out(a(T.grip - 0.15, T.grip + 0.2)); }
    if (t > T.grip + 0.25) { attached = true; const k1 = ease.io(a(T.grip + 0.25, T.ins - 0.05)); pos = lerp3(tray, [-30, up, 0], k1); }
    if (t > T.ins - 0.05) { pos = lerp3([-30, up, 0], [30, up + 2, 0], ease.io(a(T.ins - 0.05, T.ins + 0.9))); }
    if (t > T.ins + 0.9) { pos = lerp3([30, up + 2, 0], pcb, ease.io(a(T.ins + 0.9, T.rel - 0.05))); }
    if (t > T.rel - 0.05) { attached = false; coilPos = pcb.slice(); open = ease.out(a(T.rel - 0.05, T.rel + 0.25)); pos = pcb; }
    if (t > T.rel + 0.35) { pos = lerp3(pcb, [30, up + 4, 0], ease.io(a(T.rel + 0.35, T.go + 0.7))); open = 1 - ease.io(a(T.go + 0.3, T.go + 0.9)); }
    st.rigPos = pos; st.open = open; st.coilAttached = attached; st.coilPos = coilPos;
    if (attached) st.coilPos = pos;
    camBlend([[0, -10, 0], 150, 10, 12], [[0, -22, 0], 255, 8, 20, 28, PS ? 0 : 0.0, PS ? 0.06 : 0.0], seg(lt, 0, 1.2));
    if (t > T.go) camBlend([[0, -22, 0], 255, 8, 20, 28, 0, PS ? 0.06 : 0], [[30, -42, 0], 95, 30, 10, 28, PS ? 0 : 0.14, PS ? 0.09 : -0.045], seg(t, T.go, sc.end - 0.3));
    overlay = () => {
      const steps = [['PICK', T.pick], ['SEAT', T.seat], ['GRIP', T.grip], ['INSERT', T.ins], ['RELEASE', T.rel]];
      const al = fadeIO(t, sc.start + 0.2, T.go + 0.6); if (al <= 0) return;
      ctx.save(); ctx.globalAlpha = al; ctx.font = font(PS ? 32 : 30, 800); ctx.textBaseline = 'middle';
      const gap = 16; const ws = steps.map(s => ctx.measureText(s[0]).width + 50); const tw = ws.reduce((a, b) => a + b, 0) + gap * (steps.length - 1);
      let x = LW / 2 - tw / 2; const y = PS ? 300 : 150;
      steps.forEach((s, i) => {
        const on = t >= s[1] - 0.1; rr(x, y - 32, ws[i], 64, 32);
        ctx.fillStyle = on ? 'rgba(0,194,173,0.95)' : 'rgba(255,255,255,0.07)'; ctx.fill(); ctx.strokeStyle = on ? TEAL : 'rgba(255,255,255,0.25)'; ctx.lineWidth = 2; ctx.stroke();
        ctx.fillStyle = on ? '#04121a' : 'rgba(255,255,255,0.7)'; ctx.fillText(s[0], x + 25, y + 2); x += ws[i] + gap;
      });
      ctx.restore();
      textBlock(t, T.go + 0.3, sc.end - 0.1, '06 · THE RESULT', 'No tilt. No slip. No bent leads.', null, PS ? { y: 270, hs: 66 } : { y: 330, w: 680, hs: 66 });
    };
  }
  else if (sid === 'cta') {
    st.rigRotY = lerp(-0.6, 0.6, ease.io(seg(lt, 0, L)));
    st.open = Math.max(0, Math.sin(Math.PI * seg(lt, 3.0, 4.2)));
    camBlend([[30, -42, 0], 95, 30, 10, 28, PS ? 0 : 0.14, PS ? 0.09 : -0.045], [[0, -11, 0], PS ? 200 : 140, 25, 14, 28, PS ? 0 : 0.2, PS ? -0.23 : -0.045], seg(lt, 0, 1.8));
    overlay = () => {
      const a0 = sc.start + 0.6;
      const al = ease.out(seg(t, a0, a0 + 0.8));
      ctx.save(); ctx.globalAlpha = al;
      const x = PS ? 64 : 110; let y = PS ? 880 : 170;
      rr(x, y, 300, 83, 14); ctx.fillStyle = '#fff'; ctx.fill(); if (logoImg) ctx.drawImage(logoImg, x + 16, y + 9, 268, 268 * 83 / 300);
      y += PS ? 170 : 165; ctx.font = font(PS ? 66 : 64, 800); ctx.fillStyle = '#fff'; ctx.textBaseline = 'alphabetic';
      for (const l of wrap('Custom gripper nozzles for JUKI', PS ? LW - 128 : 760)) { ctx.fillText(l, x, y); y += 74; }
      ctx.restore();
      const bullets = [['Designed around your component', wordT(sc, 'designs')], ['JUKI JM & KE series compatible', wordT(sc, 'JUKI')], ['Tooling in as little as 7 days', wordT(sc, 'tooling')], ['Source factory since 2011', wordT(sc, 'Send')]];
      ctx.save(); ctx.font = font(PS ? 36 : 34, 600); ctx.textBaseline = 'middle';
      bullets.forEach(([b, ta], i) => {
        const ai = ease.out(seg(t, ta - 0.2, ta + 0.3)); if (ai <= 0) return;
        ctx.globalAlpha = ai; const yy = y + 30 + i * (PS ? 66 : 62);
        ctx.fillStyle = TEAL; ctx.beginPath(); ctx.arc(x + 14, yy, 12, 0, 7); ctx.fill();
        ctx.strokeStyle = '#04121a'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x + 8, yy); ctx.lineTo(x + 13, yy + 5); ctx.lineTo(x + 21, yy - 5); ctx.stroke();
        ctx.fillStyle = '#e2e8f0'; ctx.fillText(b, x + 44, yy + 1);
      });
      ctx.restore();
      const uy = y + 30 + 4 * (PS ? 66 : 62) + 40;
      const ua = ease.out(seg(t, wordT(sc, 'Visit') - 0.3, wordT(sc, 'Visit') + 0.4));
      if (ua > 0) {
        ctx.save(); ctx.globalAlpha = ua; ctx.font = font(PS ? 58 : 56, 800); ctx.textBaseline = 'middle';
        const w = ctx.measureText('www.smthelp.com').width + 60; rr(x, uy, w, 92, 18); ctx.fillStyle = TEAL2; ctx.fill();
        ctx.fillStyle = '#fff'; ctx.fillText('www.smthelp.com', x + 30, uy + 48);
        ctx.font = font(PS ? 30 : 28, 600); ctx.fillStyle = 'rgba(226,232,240,0.85)'; ctx.fillText('Send us your component — we engineer the grip.', x, uy + 140);
        ctx.restore();
      }
      const ya = ease.out(seg(t, sc.end - 3.6, sc.end - 3.0));
      if (ya > 0) {
        ctx.save(); ctx.globalAlpha = ya * (1 - seg(t, sc.end - 0.9, sc.end)); ctx.font = font(30, 800); ctx.textBaseline = 'middle';
        const bx = PS ? 64 : 110, byy = uy + (PS ? 210 : 200); rr(bx, byy, 330, 70, 14); ctx.fillStyle = '#ef0000'; ctx.fill();
        ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.moveTo(bx + 30, byy + 20); ctx.lineTo(bx + 30, byy + 50); ctx.lineTo(bx + 56, byy + 35); ctx.closePath(); ctx.fill();
        ctx.fillText('SUBSCRIBE', bx + 76, byy + 37); ctx.font = font(26, 600); ctx.fillStyle = 'rgba(255,255,255,0.8)'; ctx.fillText('youtube.com/c/Smthelping', bx + 350, byy + 37);
        ctx.restore();
      }
    };
  }

  // apply y-section for grip scene (global clipping plane)
  if (yClip.on && yClip.k > 0.001) {
    const THREE = stage.THREE;
    if (!stage._yPlane) stage._yPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
    stage._yPlane.constant = lerp(60, 25.3, yClip.k);
    stage.renderer.clippingPlanes = [stage._yPlane];
  } else stage.renderer.clippingPlanes = [];
  if (sid !== 'hook') stage.coilG.rotation.z = 0;

  stage.apply(st);
  if (!GLC) { stage.render(); compose2D(t, overlay); return; }
  const r = stage.renderer; r.autoClear = true;
  r.render(stage.scene, stage.camera);
  // overlay layer drawn in 2D, uploaded as one texture, composited in GL
  const save = ctx; ctx = GLC.ctx; ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H); ctx.setTransform(S, 0, 0, S, 0, 0);
  overlay(); drawBrand(t); captions(t);
  const fin = 1 - seg(t, 0, 0.6), fout = seg(t, TOTAL - 0.9, TOTAL);
  const dip = (x) => Math.max(0, 1 - Math.abs(t - x) / 0.3);
  const f = Math.max(fin, fout, dip(scenes.by.cycle.start), dip(scenes.by.cta.start)); if (f > 0) { ctx.fillStyle = `rgba(0,0,0,${f})`; ctx.fillRect(0, 0, LW, LH); }
  ctx = save;
  GLC.tex.needsUpdate = true;
  const cp = r.clippingPlanes; r.clippingPlanes = []; r.autoClear = false; r.render(GLC.scene, GLC.cam); r.clippingPlanes = cp; r.autoClear = true;
}
function compose2D(t, overlay) {
  ctx.setTransform(S, 0, 0, S, 0, 0);
  drawBG(t);
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(glCanvas, 0, 0, W, H); ctx.setTransform(S, 0, 0, S, 0, 0);
  drawVignette(); overlay(); drawBrand(t); captions(t);
}
let GLC = null;
function setupGLComposite() {
  const THREE = stage.THREE;
  const mk = () => { const c = document.createElement('canvas'); c.width = W; c.height = H; return c; };
  const bg = mk(); const save = ctx; ctx = bg.getContext('2d'); ctx.setTransform(S, 0, 0, S, 0, 0); drawBG(0); drawVignette(); ctx = save;
  const bgTex = new THREE.CanvasTexture(bg); bgTex.colorSpace = THREE.SRGBColorSpace; stage.scene.background = bgTex;
  const ov = mk(); const octx = ov.getContext('2d');
  const tex = new THREE.CanvasTexture(ov); tex.colorSpace = THREE.SRGBColorSpace; tex.premultiplyAlpha = true; tex.generateMipmaps = false; tex.minFilter = THREE.LinearFilter;
  const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false, depthTest: false, depthWrite: false, premultipliedAlpha: true });
  const scene = new THREE.Scene(); scene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), mat));
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  GLC = { ctx: octx, tex, scene, cam };
}

window.setupVideo = async (cfg) => {
  portrait = cfg.portrait; W = cfg.w; H = cfg.h; LW = portrait ? 1080 : 1920; LH = portrait ? 1920 : 1080; S = W / LW;
  VO = cfg.vo; scenes = buildTimeline(VO);
  out = document.createElement('canvas'); out.width = W; out.height = H; document.body.appendChild(out); ctx = out.getContext('2d', { willReadFrequently: !!cfg.cpu2d });
  const R3 = cfg.r3 || 1; glCanvas = document.createElement('canvas'); glCanvas.width = Math.round(W * R3); glCanvas.height = Math.round(H * R3);
  stage = await createStage(glCanvas, { modelB64: cfg.model, preserve: true, aa: cfg.aa });
  stage.setSize(glCanvas.width, glCanvas.height, 1);
  { const mk = (fn) => { const c = document.createElement('canvas'); c.width = W; c.height = H; const save = ctx; ctx = c.getContext('2d'); ctx.setTransform(S, 0, 0, S, 0, 0); fn(); ctx = save; return c; };
    /* caches disabled */ }
  if (cfg.logo) { logoImg = new Image(); logoImg.src = cfg.logo; await logoImg.decode(); }
  await document.fonts.load('800 40px Inter'); await document.fonts.load('700 20px "JetBrains Mono"');
  return { total: TOTAL, scenes: scenes.list.map(s => ({ id: s.id, start: s.start, voStart: s.voStart, end: s.end })), chunks: scenes.list.flatMap(s => s.chunks.map(c => ({ a: c.a, b: c.b, text: c.toks.map(k => k.txt).join(' ') }))) };
};
window.renderAt = (t, q = 0.93) => { frame(t); return (GLC ? glCanvas : out).toDataURL('image/jpeg', q); };
window.enableGLComposite = () => { setupGLComposite(); return true; };
window.renderOnly = (t) => { frame(t); return true; };
window.profile = (t) => {
  const r = {}; let t0 = performance.now();
  frame(t); const gl = stage.renderer.getContext(); const px = new Uint8Array(4); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
  r.frame3d = performance.now() - t0; t0 = performance.now();
  ctx.getImageData(0, 0, 1, 1); r.flush2d = performance.now() - t0; t0 = performance.now();
  const u = out.toDataURL('image/jpeg', 0.92); r.jpeg = performance.now() - t0; t0 = performance.now();
  const u2 = out.toDataURL('image/png'); r.png = performance.now() - t0;
  return r;
};
window.renderThumb = (opt = {}) => {
  const st = { open: opt.open ?? 0, explode: 0, cut: opt.cut ?? 0, highlight: { padL1: 0.9, padL2: 0.9, padR: 0.9, stop: 0.6 }, rigPos: [0, 0, 0], coilPos: [0, 0, 0], coilAttached: true, props: false, rigRotY: opt.rot ?? 0.25, coilVisible: true };
  stage.renderer.clippingPlanes = [];
  stage.apply(st);
  stage.setCamera(orbit(opt.target || [0, -16, 0], opt.dist || 78, opt.az ?? 32, opt.el ?? 10), opt.target || [0, -16, 0], 28, W, H, opt.sx ?? 0.2, opt.sy ?? 0.0);
  stage.render();
  ctx.setTransform(S, 0, 0, S, 0, 0);
  drawBG(0);
  // glow behind product
  const gx = LW * 0.7, gy = LH * 0.5; const g = ctx.createRadialGradient(gx, gy, 10, gx, gy, 520);
  g.addColorStop(0, 'rgba(0,194,173,0.35)'); g.addColorStop(1, 'rgba(0,194,173,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, LW, LH);
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(glCanvas, 0, 0, W, H); ctx.setTransform(S, 0, 0, S, 0, 0);
  drawVignette();
  // triangle of contact points
  const c1 = P([4.25, -25.3, 0]), c2 = P([-3.47, -25.3, 2.45]), c3 = P([-3.47, -25.3, -2.45]);
  ctx.strokeStyle = AMBER; ctx.lineWidth = 6; ctx.setLineDash([18, 12]); ctx.beginPath(); ctx.moveTo(c1[0], c1[1]); ctx.lineTo(c2[0], c2[1]); ctx.lineTo(c3[0], c3[1]); ctx.closePath(); ctx.stroke(); ctx.setLineDash([]);
  for (const c of [c1, c2, c3]) { ctx.fillStyle = AMBER; ctx.beginPath(); ctx.arc(c[0], c[1], 14, 0, 7); ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; ctx.stroke(); }
  // text
  const x = 90; ctx.textBaseline = 'alphabetic';
  ctx.font = font(34, 800, 'JetBrains Mono'); const kt = 'JUKI ODD-FORM INSERTION'; const kw = ctx.measureText(kt).width + 48;
  rr(x, 120, kw, 64, 32); ctx.fillStyle = 'rgba(0,194,173,0.18)'; ctx.fill(); ctx.strokeStyle = TEAL; ctx.lineWidth = 3; ctx.stroke(); ctx.fillStyle = TEAL; ctx.fillText(kt, x + 24, 165);
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,0.6)'; ctx.shadowBlur = 24;
  ctx.font = font(176, 900); ctx.fillStyle = '#fff'; ctx.fillText('NO SLIP.', x - 6, 380);
  ctx.fillText('NO TILT.', x - 6, 560);
  ctx.fillStyle = TEAL; ctx.font = font(150, 900); ctx.fillText('3-POINT GRIP', x - 4, 730);
  ctx.restore();
  ctx.font = font(46, 800); const sub = 'Custom Gripper Nozzle · Ø8.5 mm Coil'; const sw = ctx.measureText(sub).width + 56;
  rr(x, 790, sw, 86, 16); ctx.fillStyle = AMBER; ctx.fill(); ctx.fillStyle = '#111827'; ctx.fillText(sub, x + 28, 849);
  rr(x, 940, 330, 92, 16); ctx.fillStyle = '#fff'; ctx.fill(); if (logoImg) ctx.drawImage(logoImg, x + 18, 949, 294, 294 * 83 / 300);
  ctx.font = font(40, 700, 'JetBrains Mono'); ctx.fillStyle = 'rgba(255,255,255,0.85)'; ctx.fillText('CN-SM-2713', x + 360, 1000);
  return out.toDataURL('image/png');
};
window.profile2 = (t) => {
  const r = {}; frame(t); const gl = stage.renderer.getContext(); const px = new Uint8Array(4); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px); ctx.getImageData(0,0,1,1);
  let t0 = performance.now(); stage.render(); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px); r.gl = performance.now() - t0;
  t0 = performance.now(); ctx.setTransform(1,0,0,1,0,0); ctx.drawImage(glCanvas, 0, 0, W, H); ctx.getImageData(0,0,1,1); r.drawGL = performance.now() - t0;
  t0 = performance.now(); ctx.setTransform(S,0,0,S,0,0); drawBG(t); ctx.getImageData(0,0,1,1); r.bg = performance.now() - t0;
  t0 = performance.now(); drawVignette(); ctx.getImageData(0,0,1,1); r.vig = performance.now() - t0;
  t0 = performance.now(); captions(t); drawBrand(t); ctx.getImageData(0,0,1,1); r.text = performance.now() - t0;
  t0 = performance.now(); glCanvas.toDataURL('image/jpeg', 0.94); r.glJpeg = performance.now() - t0;
  return r;
};
