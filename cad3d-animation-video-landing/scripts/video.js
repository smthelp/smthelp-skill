// Video timeline renderer for SAF1001 axial tape feeder film (16:9 + 9:16)
import { createStage, ease, seg, lerp, lerp3, orbit, clamp01, ANCHORS } from './engine.js';

const TEAL = '#00C2AD', TEAL2 = '#00A896', SKY = '#38BDF8', AMBER = '#F5B13D', RED = '#ff5a4f';
let stage, out, ctx, glCanvas, W, H, LW, LH, S, portrait, VO, scenes, logoImg, TOTAL;

// caption phrase map: spoken word sequences -> on-screen text (lower-case match, punctuation kept from the script)
const CAPMAP = [
  [['0.8 seconds'], '0.8 s'], [['plus', 'or', 'minus', '0.3', 'millimetres'], '±0.3 mm'], [['32', 'millimetre'], 'Ø32 mm'],
  [['24', 'volts'], '24 V'], [['megapascal'], 'MPa'], [['8', 'core'], '8-core'], [['48', 'hour'], '48-hour'], [['smthelp', 'dot', 'com'], 'smthelp.com'],
  [['u', 'formed'], 'U-formed'], [['anti', 'reverse'], 'anti-reverse'], [['mixed', 'technology'], 'mixed-technology'], [['spring', 'loaded'], 'spring-loaded'],
  [['odd', 'form'], 'odd-form'],
];
function buildTimeline(vo) {
  const by = {}; let t = 0.6; const list = [];
  for (const s of vo) {
    const extra = s.id === 'cta' ? 4.8 : 1.15;
    const sc = { id: s.id, start: t, voStart: t + 0.4, len: s.dur + 0.4 + extra, words: s.words, text: s.text };
    sc.end = sc.start + sc.len; list.push(sc); by[s.id] = sc; t = sc.end;
  }
  for (const sc of list) {
    // tokens with trailing punctuation recovered from the script text
    let pos = 0; const low = sc.text;
    let toks = sc.words.map(w => { const i = low.indexOf(w[2], pos); let tr = ''; if (i >= 0) { pos = i + w[2].length; const m = low.slice(pos).match(/^[.,:;!?]+/); if (m) { tr = m[0]; pos += tr.length; } }
      return { a: sc.voStart + w[0], b: sc.voStart + w[1], txt: w[2], tr }; });
    const outT = [];
    for (let i = 0; i < toks.length;) {
      let hit = null; for (const [seq, rep] of CAPMAP) { if (seq.every((w, j) => toks[i + j] && toks[i + j].txt.toLowerCase() === w)) { hit = [seq.length, rep]; break; } }
      if (hit) { const last = toks[i + hit[0] - 1]; outT.push({ a: toks[i].a, b: last.b, txt: hit[1] + last.tr }); i += hit[0]; }
      else { outT.push({ a: toks[i].a, b: toks[i].b, txt: toks[i].txt + toks[i].tr }); i++; }
    }
    sc.tokens = outT;
    const chunks = []; let cur = [];
    for (const k of sc.tokens) { cur.push(k); const len = cur.map(x => x.txt).join(' ').length;
      if (/[.,:;?!]$/.test(k.txt) && len > 14 || len > (portrait ? 26 : 40)) { chunks.push(cur); cur = []; } }
    if (cur.length) chunks.push(cur);
    sc.chunks = chunks.map((c, i) => ({ toks: c, a: c[0].a, b: (i < chunks.length - 1 ? chunks[i + 1][0].a : c[c.length - 1].b + 0.6) }));
  }
  TOTAL = t; return { list, by };
}
function wordT(sc, word, nth = 0) { let k = 0; for (const w of sc.words) if (w[2].toLowerCase().startsWith(word.toLowerCase())) { if (k++ === nth) return sc.voStart + w[0]; } return sc.voStart; }

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
  ctx.fillText('SAF1001  ·  AXIAL TAPE FEEDER', x + 228, y + 29);
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
    if (cx + w > (portrait ? LW - 40 : 980)) { cx = x; cy += h + 14; }
    ctx.globalAlpha = ai; rr(cx, cy, w, h, h / 2);
    ctx.fillStyle = 'rgba(0,194,173,0.12)'; ctx.fill(); ctx.strokeStyle = (colors && colors[i]) || TEAL; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.fillText(it, cx + 22, cy + h / 2 + 1); cx += w + 14;
  });
  ctx.restore();
}
function P(anchor) { return stage.project(anchor, LW, LH); }
function callout(t, a, b, anchor, label, side = 'r', opt = {}) {
  const al = fadeIO(t, a, b, 0.35, 0.35); if (al <= 0) return;
  const p = opt.screen || P(anchor); if (p[2] > 1 || p[0] < 10 || p[0] > LW - 10 || p[1] < 10 || p[1] > LH - 10) return;
  const fs = portrait ? 30 : 28; ctx.save(); ctx.font = font(fs, 700); const tw = ctx.measureText(label).width; const sub = opt.sub; let sw = 0;
  if (sub) { ctx.font = font(fs * 0.72, 500); sw = ctx.measureText(sub).width; } ctx.restore();
  const bw = Math.max(tw, sw) + 40, bh = sub ? fs * 2.6 : fs * 1.75;
  let adx = Math.abs(opt.dx ?? (portrait ? 150 : 210));
  if (side === 'r' && p[0] + adx + bw > LW - 24) side = 'l'; else if (side === 'l' && p[0] - adx - bw < 24) side = 'r';
  if (side === 'r' && p[0] + adx + bw > LW - 24) adx = Math.max(40, LW - 24 - bw - p[0]);
  if (side === 'l' && p[0] - adx - bw < 24) adx = Math.max(40, p[0] - 24 - bw);
  const dx = adx * (side === 'r' ? 1 : -1); let dy = opt.dy ?? -70;
  const capTop = portrait ? LH * 0.75 : LH - 160; if (p[1] + dy + bh / 2 > capTop) dy = capTop - bh / 2 - p[1]; if (p[1] + dy - bh / 2 < 140) dy = 140 + bh / 2 - p[1];
  const grow = ease.out(seg(t, a, a + 0.5));
  ctx.save(); ctx.globalAlpha = al; const col = opt.color || TEAL;
  const pr = 10 + 10 * ((t * 1.4) % 1);
  ctx.strokeStyle = col; ctx.globalAlpha = al * (1 - ((t * 1.4) % 1)); ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(p[0], p[1], pr, 0, 7); ctx.stroke(); ctx.globalAlpha = al;
  ctx.fillStyle = col; ctx.beginPath(); ctx.arc(p[0], p[1], 7, 0, 7); ctx.fill(); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(p[0], p[1], 3, 0, 7); ctx.fill();
  const ex = p[0] + dx * 0.55, ey = p[1] + dy, fx = p[0] + dx, fy = ey;
  ctx.strokeStyle = col; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(p[0], p[1]);
  const k1 = Math.min(1, grow * 2), k2 = clamp01(grow * 2 - 1);
  ctx.lineTo(lerp(p[0], ex, k1), lerp(p[1], ey, k1)); if (k2 > 0) ctx.lineTo(lerp(ex, fx, k2), fy); ctx.stroke();
  if (grow > 0.6) {
    ctx.globalAlpha = al * seg(grow, 0.6, 1); ctx.textBaseline = 'middle';
    const bx = side === 'r' ? fx : fx - bw, by = fy - bh / 2;
    rr(bx, by, bw, bh, 10); ctx.fillStyle = 'rgba(7,13,30,0.88)'; ctx.fill(); ctx.strokeStyle = col; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = col; ctx.fillRect(side === 'r' ? bx : bx + bw - 5, by + 8, 5, bh - 16);
    ctx.fillStyle = '#fff'; ctx.font = font(fs, 700); ctx.fillText(label, bx + 20, sub ? by + bh * 0.36 : by + bh / 2 + 1);
    if (sub) { ctx.font = font(fs * 0.72, 500); ctx.fillStyle = 'rgba(203,213,225,0.95)'; ctx.fillText(sub, bx + 20, by + bh * 0.72); }
  }
  ctx.restore();
}
function scrim(t, sid) {
  const k = sid === 'cta' ? 0.9 : 1; ctx.save();
  if (!portrait) { const g = ctx.createLinearGradient(0, 0, 980, 0); g.addColorStop(0, `rgba(4,8,20,${0.78 * k})`); g.addColorStop(0.55, `rgba(4,8,20,${0.5 * k})`); g.addColorStop(1, 'rgba(4,8,20,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, 980, LH); }
  else { const g = ctx.createLinearGradient(0, 0, 0, 980); g.addColorStop(0, `rgba(4,8,20,${0.8 * k})`); g.addColorStop(0.6, `rgba(4,8,20,${0.5 * k})`); g.addColorStop(1, 'rgba(4,8,20,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, LW, 980); }
  ctx.restore();
}
function arrow(x1, y1, x2, y2, col, w = 6, head = 22) {
  ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = w; ctx.lineCap = 'round';
  const ang = Math.atan2(y2 - y1, x2 - x1);
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2 - Math.cos(ang) * head * 0.8, y2 - Math.sin(ang) * head * 0.8); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(x2, y2); ctx.lineTo(x2 - head * Math.cos(ang - 0.45), y2 - head * Math.sin(ang - 0.45)); ctx.lineTo(x2 - head * Math.cos(ang + 0.45), y2 - head * Math.sin(ang + 0.45)); ctx.closePath(); ctx.fill();
}
function captions(t) {
  if (portrait && t > scenes.by.cta.start + 0.8) return;
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
function cam(target, dist, az, el, fov = 30, shiftX = null, shiftY = null) {
  const pd = portrait ? 1.55 : 1;
  const sx = shiftX ?? (portrait ? 0 : 0.17), sy = shiftY ?? (portrait ? 0.13 : -0.04);
  stage.setCamera(orbit(target, dist * pd, az, el), target, fov, W, H, sx, sy);
}
function camBlend(A, B, k) {
  const kk = ease.io(clamp01(k)); const tg = lerp3(A[0], B[0], kk);
  cam(tg, lerp(A[1], B[1], kk), lerp(A[2], B[2], kk), lerp(A[3], B[3], kk), lerp(A[4] ?? 30, B[4] ?? 30, kk), A[5] == null ? null : lerp(A[5], B[5], kk), A[6] == null ? null : lerp(A[6], B[6], kk));
}
const HOOK0 = [[-215, 230, 0], 300, -8, 38], HOOK1 = [[-200, 230, 0], 360, -32, 30];
const HERO = [[-10, 140, 0], 1500, -52, 18];
const BACK = [[110, 185, 0], 850, 42, 28];
const TRACK = [[-170, 225, 0], 600, -28, 36];
const INDEX = [[-222, 228, 8], 300, -18, 44], INDEX2 = [[-232, 228, 8], 270, -38, 36];
const FRONT = [[-280, 205, 0], 520, -70, 34], FRONT2 = [[-284, 222, 0], 290, -96, 40];
const PICKC = [[-283, 240, 0], 330, -80, 34], PICKC2 = [[-280, 240, 0], 400, -55, 32];
const UNDER = [[-140, 110, 0], 920, -82, 6], UNDER2 = [[-170, 115, 0], 820, -100, 10];
const INSIDE = [[-60, 150, 0], 760, -70, 14];
const MOUNT = [[-180, 50, 0], 900, -48, 10];
const EXPL = [[-10, 150, 0], 2350, -55, 20], EXPLP = [[-10, 150, 0], 2100, -55, 20, 30, 0, 0.1];

const RATE = { hook: 0.5, title: 1, load: 1, index: 0.3, form: 0.3, pick: 0.3, waste: 0.6, inside: 1, connect: 1, cta: 1 };
let mtCache = { t: 0, mt: 0 };
function machineTime(t) { // integral of the playback rate (slow motion in the mechanism scenes, no phase jumps)
  let t0 = 0, mt = 0; if (t >= mtCache.t) { t0 = mtCache.t; mt = mtCache.mt; }
  const dt = 1 / 96; for (let x = t0; x < t; x += dt) { const r = rateAt(x); mt += r * Math.min(dt, t - x); }
  mtCache = { t, mt }; return mt;
}
function rateAt(x) {
  const L = scenes.list; let i = L.findIndex(s => x >= s.start && x < s.end); if (i < 0) i = x < L[0].start ? 0 : L.length - 1;
  const s = L[i]; let r = RATE[s.id]; if (s.id === 'pick') { const tr = wordT(s, 'result'); r = lerp(0.3, 1, seg(x, tr - 0.5, tr + 0.5)); }
  const prev = L[i - 1]; if (prev) r = lerp(prev.id === 'pick' ? 1 : RATE[prev.id], r, seg(x, s.start, s.start + 1));
  return r;
}

function frame(t) {
  const { by } = scenes;
  const st = { explode: 0, ghost: 0, time: t, cycT: machineTime(t), run: 1, head: 0, fibre: 0.6, air: 0, chips: 0, highlight: {}, compsVisible: true };
  let overlay = () => { };
  const sid = scenes.list.find(s => t >= s.start && t < s.end)?.id || (t < 0.6 ? 'hook' : 'cta');
  const sc = by[sid]; const lt = t - sc.start; const L = sc.len; const PS = portrait;
  const pulse = 0.55 + 0.45 * Math.sin(t * 6);
  const TB = PS ? {} : {};

  if (sid === 'hook') {
    st.head = 0; st.fibre = 0;
    camBlend(HOOK0, HOOK1, seg(lt, 0, L));
    overlay = () => {
      textBlock(t, sc.start + 0.4, sc.end - 0.2, 'THE AXIAL PROBLEM', 'Taped parts. Picked by hand.', null, PS ? { y: 250 } : { x: 110, y: 330, w: 700 });
      const tags = [['✕  Slow', wordT(sc, 'slow')], ['✕  Inconsistent', wordT(sc, 'inconsistent')], ['✕  Wrong part, wrong way', wordT(sc, 'wrong')]];
      tags.forEach(([lab, ta], i) => {
        const al = fadeIO(t, ta - 0.1, sc.end - 0.2, 0.25, 0.4); if (al <= 0) return;
        ctx.save(); ctx.globalAlpha = al; ctx.font = font(PS ? 34 : 36, 800); ctx.textBaseline = 'middle';
        const w = ctx.measureText(lab).width + 48; const x = PS ? 64 : 110, y = PS ? 470 + i * 78 : 560 + i * 78;
        rr(x, y - 30, w, 60, 12); ctx.fillStyle = 'rgba(239,68,68,0.16)'; ctx.fill(); ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 2; ctx.stroke();
        ctx.fillStyle = '#fecaca'; ctx.fillText(lab, x + 24, y + 2); ctx.restore();
      });
    };
  }
  else if (sid === 'title') {
    camBlend(HOOK1, HERO, seg(lt, 0, L * 0.8));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, 'INTRODUCING', 'SAF1001', 'Axial tape feeder by Southern Machinery', PS ? { hs: 112 } : { hs: 118, y: 300 });
      chips(t, wordT(sc, 'Taped') - 0.2, sc.end - 0.1, ['Taped parts in', 'Trimmed + U-formed', 'Fixed pick point'], PS ? 64 : 110, PS ? 610 : 640);
    };
  }
  else if (sid === 'load') {
    const tg = wordT(sc, 'Guide'), tp = wordT(sc, 'press'), tc = wordT(sc, 'claws');
    st.highlight = { tray: fadeIO(t, wordT(sc, 'tray') - 0.3, tg, 0.3, 0.3) * pulse * 0.6, carton: fadeIO(t, wordT(sc, 'strip') - 0.3, tg, 0.3, 0.3) * pulse,
      guideblk: fadeIO(t, tg - 0.2, tp, 0.3, 0.3) * pulse, press: fadeIO(t, tp - 0.2, tc, 0.3, 0.3) * pulse, claw: fadeIO(t, tc - 0.3, sc.end, 0.3, 0.3) * pulse };
    camBlend(HERO, BACK, seg(lt, 0, 2.4));
    if (t > tg - 0.6) camBlend(BACK, TRACK, seg(t, tg - 0.6, tp + 0.4));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '01 · LOAD', 'Flat, guided, held', 'Taped resistors, diodes and jump wires feed from a horizontal tray.');
      callout(t, wordT(sc, 'tray') - 0.3, tg - 0.3, ANCHORS.tray, 'Horizontal tape tray', 'l', { dx: PS ? 130 : 200, dy: 80, sub: 'Incoming parts in boxes' });
      callout(t, tg - 0.2, tp + 0.4, ANCHORS.guideblk, 'Guide blocks', 'r', { dx: PS ? 120 : 190, dy: -80 });
      callout(t, tp - 0.2, sc.end - 0.2, ANCHORS.press, 'Press blocks', 'r', { dx: PS ? 120 : 190, dy: -90 });
      callout(t, tc - 0.2, sc.end - 0.2, ANCHORS.claw, 'Anti-reverse claws', 'l', { dx: PS ? 120 : 190, dy: 80, color: AMBER });
    };
  }
  else if (sid === 'index') {
    st.head = 0; st.air = 1;
    const tp = wordT(sc, 'pawls'), ts = wordT(sc, 'stop'), tr = wordT(sc, 'return');
    st.highlight = { feedcyl: fadeIO(t, wordT(sc, 'cylinder') - 0.3, tp, 0.3, 0.3) * pulse, slider: fadeIO(t, wordT(sc, 'slide') - 0.3, ts, 0.3, 0.3) * pulse * 0.5,
      pawls: fadeIO(t, tp - 0.3, sc.end, 0.3, 0.3) * pulse, stop: fadeIO(t, ts - 0.3, tr, 0.3, 0.3) * pulse };
    camBlend(TRACK, INDEX, seg(lt, 0, 2.4));
    if (t > ts - 1) camBlend(INDEX, [[-205, 205, 20], 380, -12, 30], seg(t, ts - 1, ts + 0.6));
    if (t > tr - 0.8) camBlend([[-205, 205, 20], 380, -12, 30], INDEX2, seg(t, tr - 0.8, tr + 0.8));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '02 · INDEX', 'One pitch per cycle', 'Air cylinder + slide + index pawls on the leads.');
      callout(t, wordT(sc, 'cylinder') - 0.3, ts - 0.4, ANCHORS.feedcyl, 'Feed cylinder', 'r', { dx: PS ? 120 : 190, dy: -90, color: SKY, sub: 'Air-pressure speed regulation' });
      callout(t, tp - 0.3, ts - 0.4, ANCHORS.pawl, 'Index pawls', 'l', { dx: PS ? 120 : 190, dy: -80, color: AMBER });
      callout(t, ts - 0.2, tr - 0.2, ANCHORS.stop, 'Adjustable stop block', 'r', { dx: PS ? 110 : 180, dy: 80, color: AMBER, sub: 'Sets the stroke' });
      callout(t, tr - 0.2, sc.end - 0.2, ANCHORS.pawl, 'Pawls tip over on return', 'l', { dx: PS ? 120 : 190, dy: -80, color: AMBER });
      chips(t, sc.start + 2.6, sc.end - 0.2, ['Slowed for clarity'], PS ? 64 : 110, PS ? 1650 : 880, [SKY]);
    };
  }
  else if (sid === 'form') {
    st.head = 0; st.ghost = 0.75 * fadeIO(t, sc.start + 1.4, sc.end - 0.3, 0.6, 0.6); st.ghostU = fadeIO(t, sc.start + 0.8, sc.end + 5, 0.6, 0.6);
    const tk = wordT(sc, 'moving'), tt = wordT(sc, 'trims'), tu = wordT(sc, 'bends');
    st.highlight = { cutcyl: fadeIO(t, wordT(sc, '32') - 0.3, tk + 0.3, 0.3, 0.3) * pulse, knife_move: fadeIO(t, tk - 0.3, sc.end, 0.3, 0.3) * pulse * 0.7, knife_fixed: fadeIO(t, tt - 0.2, tu, 0.3, 0.3) * pulse * 0.5 };
    camBlend(INDEX2, FRONT, seg(lt, 0, 2.4));
    if (t > tt - 0.8) camBlend(FRONT, FRONT2, seg(t, tt - 0.8, tu + 0.6));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '03 · TRIM + FORM', 'One stroke, two jobs', 'Leads trimmed against the fixed knife and bent into a U.');
      callout(t, wordT(sc, '32') - 0.3, tt - 0.3, ANCHORS.cutcyl, 'Ø32 mm cut cylinder', 'r', { dx: PS ? 120 : 190, dy: 70, color: SKY });
      callout(t, tk - 0.2, tu - 0.2, ANCHORS.knife, 'Moving knife', 'l', { dx: PS ? 120 : 190, dy: -90 });
      callout(t, tu - 0.2, sc.end - 0.2, ANCHORS.formed, 'U-formed, ready to insert', 'r', { dx: PS ? 120 : 190, dy: -90, color: AMBER });
      chips(t, sc.start + 2.6, sc.end - 0.2, ['Slowed for clarity'], PS ? 64 : 110, PS ? 1650 : 880, [SKY]);
    };
  }
  else if (sid === 'pick') {
    const to = wordT(sc, 'optical'), tr = wordT(sc, 'result'); st.head = 1; st.ghostU = 1 - seg(lt, L - 2, L);
    st.fibre = 0.15 + 0.85 * fadeIO(t, to - 0.3, sc.end + 2, 0.3, 0.3);
    st.highlight = { fibre: fadeIO(t, to - 0.3, tr, 0.3, 0.3) * pulse };
    camBlend(FRONT2, PICKC, seg(lt, 0, 2.4));
    if (lt > 2.4) camBlend(PICKC, PICKC2, seg(lt, 2.4, L));
    overlay = () => {
      textBlock(t, sc.start + 0.3, tr + 0.1, '04 · PICK POINT', 'Sensed, not timed', 'An optical fibre confirms the part before the head picks.');
      callout(t, to - 0.3, tr - 0.2, ANCHORS.fibre, 'Optical fibre sensing', 'l', { color: RED, dx: PS ? 120 : 190, dy: 90 });
      const stats = [['0.8 s', 'per feed', wordT(sc, '0.8')], ['±0.3 mm', 'feeding accuracy', wordT(sc, 'plus')]];
      stats.forEach(([big, small, tb], i) => {
        const al = fadeIO(t, Math.max(tr - 0.1, tb - 0.2), sc.end - 0.15, 0.35, 0.3); if (al <= 0) return;
        ctx.save(); ctx.globalAlpha = al;
        const x = PS ? 64 + i * 480 : 110, y = PS ? 260 : 300 + i * 220; const w = PS ? 450 : 520, h = 190;
        rr(x, y, w, h, 20); ctx.fillStyle = 'rgba(7,13,30,0.82)'; ctx.fill(); ctx.strokeStyle = TEAL; ctx.lineWidth = 3; ctx.stroke();
        ctx.fillStyle = TEAL; ctx.fillRect(x, y + 20, 7, h - 40);
        ctx.textBaseline = 'alphabetic'; ctx.font = font(PS ? 96 : 104, 900); ctx.fillStyle = '#fff'; ctx.fillText(big, x + 36, y + 112);
        ctx.font = font(32, 600); ctx.fillStyle = 'rgba(203,213,225,0.95)'; ctx.fillText(small, x + 38, y + 160); ctx.restore();
      });
    };
  }
  else if (sid === 'waste') {
    st.ghost = fadeIO(t, sc.start + 0.8, sc.end + 3, 0.8, 0.5); st.chips = fadeIO(t, wordT(sc, 'pieces') - 0.5, sc.end, 0.4, 0.4);
    st.highlight = { tapecyl: fadeIO(t, wordT(sc, 'cylinder') - 0.3, wordT(sc, 'pieces'), 0.3, 0.3) * pulse, tapeknife: fadeIO(t, wordT(sc, 'chops') - 0.3, sc.end, 0.3, 0.3) * pulse * 0.7, chute: fadeIO(t, wordT(sc, 'chute') - 0.4, sc.end, 0.3, 0.3) * pulse * 0.5 };
    camBlend(PICKC2, UNDER, seg(lt, 0, 2.6));
    if (lt > 2.6) camBlend(UNDER, UNDER2, seg(lt, 2.6, L));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '05 · WASTE TAPE', 'Chopped and gone', 'Front-end vertical drop; reflow type optional.');
      callout(t, wordT(sc, 'cylinder') - 0.3, sc.end - 0.2, ANCHORS.tapecyl, 'Tape-cut cylinder', 'r', { dx: PS ? 120 : 190, dy: -90, color: SKY });
      callout(t, wordT(sc, 'chops') - 0.2, sc.end - 0.2, ANCHORS.tapeknife, 'Paper-tape knife', 'l', { dx: PS ? 110 : 180, dy: 80 });
      callout(t, wordT(sc, 'chute') - 0.3, sc.end - 0.2, ANCHORS.chute, 'Waste chute', 'r', { dx: PS ? 110 : 170, dy: 80 });
    };
  }
  else if (sid === 'inside') {
    const tl = wordT(sc, 'locks');
    st.ghost = 1 - seg(t, tl - 0.4, tl + 0.6) * 0.7;
    st.highlight = { valve: fadeIO(t, wordT(sc, 'solenoid') - 0.3, tl, 0.3, 0.3) * pulse, pcb: fadeIO(t, wordT(sc, 'PLC') - 0.3, tl, 0.3, 0.3) * pulse,
      pins: fadeIO(t, wordT(sc, 'locating') - 0.3, sc.end, 0.3, 0.3) * pulse, clamp: fadeIO(t, wordT(sc, 'spring') - 0.3, sc.end, 0.3, 0.3) * pulse, mount: fadeIO(t, tl - 0.2, sc.end, 0.3, 0.3) * pulse * 0.4 };
    camBlend(UNDER2, INSIDE, seg(lt, 0, 2.2));
    if (t > tl - 0.8) camBlend(INSIDE, MOUNT, seg(t, tl - 0.8, tl + 1));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '06 · INSIDE + MOUNTING', 'PLC-controlled, key-located', null);
      callout(t, wordT(sc, 'solenoid') - 0.3, tl - 0.4, ANCHORS.valve, 'Solenoid valve banks', 'r', { dx: PS ? 110 : 180, dy: 90, color: SKY });
      callout(t, wordT(sc, 'PLC') - 0.3, tl - 0.4, ANCHORS.pcb, 'PLC control board', 'r', { dx: PS ? 110 : 180, dy: -90 });
      callout(t, wordT(sc, 'locating') - 0.3, sc.end - 0.2, ANCHORS.pins, 'Locating pins', 'l', { dx: PS ? 110 : 170, dy: -80 });
      callout(t, wordT(sc, 'spring') - 0.3, sc.end - 0.2, ANCHORS.clamp, 'Spring-loaded press block', 'r', { dx: PS ? 100 : 170, dy: -90, color: AMBER });
    };
  }
  else if (sid === 'connect') {
    st.explode = ease.io(seg(lt, 0.3, 2.6)) * (1 - ease.io(seg(lt, L - 2.4, L - 0.3)));
    st.highlight = { plug: fadeIO(t, wordT(sc, 'aviation') - 0.3, wordT(sc, 'Every'), 0.3, 0.3) * pulse, btn_g: fadeIO(t, wordT(sc, 'buttons') - 0.4, wordT(sc, 'Every'), 0.3, 0.3) * pulse };
    const EX = PS ? EXPLP : EXPL;
    camBlend(MOUNT, EX, seg(lt, 0, 2.4));
    if (lt > L - 2.6) camBlend(EX, HERO, seg(lt, L - 2.6, L));
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '07 · PLUG IN & RUN', 'Power, air, IO', 'Or no communication at all: it runs on its own buttons.');
      chips(t, wordT(sc, '24') - 0.2, sc.end - 0.1, ['24 V', '0.4 – 0.6 MPa air', '8-core aviation plug · IO', 'Standalone button operation'], PS ? 64 : 110, PS ? 560 : 560);
      chips(t, wordT(sc, 'Every') - 0.2, sc.end - 0.1, ['1000 consecutive feeds', '48 h ageing test'], PS ? 64 : 110, PS ? 780 : 760, [AMBER, AMBER]);
    };
  }
  else if (sid === 'cta') {
    st.head = 1;
    camBlend([...HERO, 30, PS ? 0 : 0.17, PS ? 0.13 : -0.04], [[-10, 140, 0], PS ? 1700 : 1650, -40, 16, 30, PS ? 0 : 0.2, PS ? 0.3 : -0.04], seg(lt, 0, L));
    overlay = () => {
      const a0 = sc.start + 0.6; const al = ease.out(seg(t, a0, a0 + 0.8));
      ctx.save(); ctx.globalAlpha = al;
      const x = PS ? 64 : 110; let y = PS ? 150 : 150;
      rr(x, y, 300, 83, 14); ctx.fillStyle = '#fff'; ctx.fill(); if (logoImg) ctx.drawImage(logoImg, x + 16, y + 9, 268, 268 * 83 / 300);
      y += 160; ctx.font = font(62, 800); ctx.fillStyle = '#fff'; ctx.textBaseline = 'alphabetic';
      for (const l of wrap('Send us your part and your machine.', PS ? LW - 128 : 780)) { ctx.fillText(l, x, y); y += 72; }
      ctx.restore();
      const bullets = [['Taped resistors, diodes, jump wires', sc.start + 0.9], ['35 / 64 / 92 mm tape widths', sc.start + 1.4], ['Panasonic · JUKI · Yamaha · Mirae installs', wordT(sc, 'Panasonic')], ['Source factory since 2011', wordT(sc, 'Send')]];
      ctx.save(); ctx.font = font(PS ? 34 : 33, 600); ctx.textBaseline = 'middle';
      bullets.forEach(([b, ta], i) => {
        const ai = ease.out(seg(t, ta - 0.2, ta + 0.3)); if (ai <= 0) return;
        ctx.globalAlpha = ai; const yy = y + 20 + i * (PS ? 64 : 60);
        ctx.fillStyle = TEAL; ctx.beginPath(); ctx.arc(x + 14, yy, 12, 0, 7); ctx.fill();
        ctx.strokeStyle = '#04121a'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x + 8, yy); ctx.lineTo(x + 13, yy + 5); ctx.lineTo(x + 21, yy - 5); ctx.stroke();
        ctx.fillStyle = '#e2e8f0'; ctx.fillText(b, x + 44, yy + 1);
      });
      ctx.restore();
      const uy = y + 20 + 4 * (PS ? 64 : 60) + 30;
      const ua = ease.out(seg(t, wordT(sc, 'Visit') - 0.3, wordT(sc, 'Visit') + 0.4));
      if (ua > 0) { ctx.save(); ctx.globalAlpha = ua; ctx.font = font(PS ? 58 : 56, 800); ctx.textBaseline = 'middle';
        const w = ctx.measureText('www.smthelp.com').width + 60; rr(x, uy, w, 92, 18); ctx.fillStyle = TEAL2; ctx.fill(); ctx.fillStyle = '#fff'; ctx.fillText('www.smthelp.com', x + 30, uy + 48); ctx.restore(); }
      const ya = ease.out(seg(t, sc.end - 3.8, sc.end - 3.2));
      if (ya > 0) { ctx.save(); ctx.globalAlpha = ya * (1 - seg(t, sc.end - 0.9, sc.end)); ctx.font = font(30, 800); ctx.textBaseline = 'middle';
        const bx = x, byy = uy + 130; rr(bx, byy, 330, 70, 14); ctx.fillStyle = '#ef0000'; ctx.fill();
        ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.moveTo(bx + 30, byy + 20); ctx.lineTo(bx + 30, byy + 50); ctx.lineTo(bx + 56, byy + 35); ctx.closePath(); ctx.fill();
        ctx.fillText('SUBSCRIBE', bx + 76, byy + 37); ctx.font = font(26, 600); ctx.fillStyle = 'rgba(255,255,255,0.8)'; ctx.fillText('youtube.com/c/Smthelping', PS ? bx : bx + 350, PS ? byy + 105 : byy + 37); ctx.restore(); }
    };
  }

  stage.apply(st);
  if (!GLC) { stage.render(); compose2D(t, overlay, sid); return; }
  const r = stage.renderer; r.autoClear = true;
  if (GLC.rt) { const bg = stage.scene.background; stage.scene.background = null; r.setRenderTarget(GLC.rt); r.setClearColor(0x000000, 0); r.clear(); r.render(stage.scene, stage.camera); r.setRenderTarget(null); stage.scene.background = bg;
    r.render(GLC.bgScene, GLC.cam); r.autoClear = false; r.render(GLC.up, GLC.cam); r.autoClear = true; }
  else r.render(stage.scene, stage.camera);
  // overlay layer drawn in 2D, uploaded as one texture, composited in GL
  const save = ctx; ctx = GLC.ctx; ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H); ctx.setTransform(S, 0, 0, S, 0, 0);
  scrim(t, sid); overlay(); drawBrand(t); captions(t);
  const fin = 1 - seg(t, 0, 0.6), fout = seg(t, TOTAL - 0.9, TOTAL);
  const dip = (x) => Math.max(0, 1 - Math.abs(t - x) / 0.3);
  const f = Math.max(fin, fout, dip(scenes.by.cta.start)); if (f > 0) { ctx.fillStyle = `rgba(0,0,0,${f})`; ctx.fillRect(0, 0, LW, LH); }
  ctx = save;
  GLC.tex.needsUpdate = true;
  const cp = r.clippingPlanes; r.clippingPlanes = []; r.autoClear = false; r.render(GLC.scene, GLC.cam); r.clippingPlanes = cp; r.autoClear = true;
}
function compose2D(t, overlay, sid) {
  ctx.setTransform(S, 0, 0, S, 0, 0);
  drawBG(t);
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(glCanvas, 0, 0, W, H); ctx.setTransform(S, 0, 0, S, 0, 0);
  drawVignette(); scrim(t, sid); overlay(); drawBrand(t); captions(t);
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
  const k = window.R3D || 1;
  if (k < 0.999) {
    const rt = new THREE.WebGLRenderTarget(Math.round(W * k), Math.round(H * k), { samples: window.R3D_MSAA || 0 });
    rt.texture.minFilter = THREE.LinearFilter; rt.texture.magFilter = THREE.LinearFilter;
    const up = new THREE.Scene(); up.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.MeshBasicMaterial({ map: rt.texture, toneMapped: true, transparent: true, depthTest: false, depthWrite: false })));
    const bgScene = new THREE.Scene(); bgScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.MeshBasicMaterial({ map: stage.scene.background, toneMapped: false, depthTest: false, depthWrite: false })));
    GLC.rt = rt; GLC.up = up; GLC.bgScene = bgScene;
    // camera aspect stays W/H; projection is resolution independent
  }
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
  stage.renderer.clippingPlanes = [];
  stage.apply({ explode: 0, ghost: 0, time: 0.3, cycT: 0.5, run: 1, head: 1, fibre: 1, air: 0, chips: 0, highlight: { pawls: 0.6, knife_move: 0.5 }, compsVisible: true });
  const tg = opt.target || [-120, 170, 0];
  stage.setCamera(orbit(tg, opt.dist || 1150, opt.az ?? -50, opt.el ?? 24), tg, 30, W, H, opt.sx ?? 0.22, opt.sy ?? 0.0);
  stage.render();
  ctx.setTransform(S, 0, 0, S, 0, 0); drawBG(0);
  const gx = LW * 0.7, gy = LH * 0.5; const g = ctx.createRadialGradient(gx, gy, 10, gx, gy, 560);
  g.addColorStop(0, 'rgba(0,194,173,0.38)'); g.addColorStop(1, 'rgba(0,194,173,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, LW, LH);
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(glCanvas, 0, 0, W, H); ctx.setTransform(S, 0, 0, S, 0, 0);
  drawVignette();
  const x = 90; ctx.textBaseline = 'alphabetic';
  ctx.font = font(34, 800, 'JetBrains Mono'); const kt = 'SMT / THT AXIAL FEEDING'; const kw = ctx.measureText(kt).width + 48;
  rr(x, 110, kw, 64, 32); ctx.fillStyle = 'rgba(0,194,173,0.18)'; ctx.fill(); ctx.strokeStyle = TEAL; ctx.lineWidth = 3; ctx.stroke(); ctx.fillStyle = TEAL; ctx.fillText(kt, x + 24, 155);
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,0.6)'; ctx.shadowBlur = 24;
  ctx.font = font(172, 900); ctx.fillStyle = '#fff'; ctx.fillText('TAPE IN.', x - 6, 370);
  ctx.fillStyle = TEAL; ctx.font = font(150, 900); ctx.fillText('U-FORMED', x - 4, 540); ctx.fillText('OUT.', x - 4, 700);
  ctx.restore();
  ctx.font = font(44, 800); const sub = 'SAF1001 Axial Tape Feeder'; const sw = ctx.measureText(sub).width + 56;
  rr(x, 760, sw, 86, 16); ctx.fillStyle = AMBER; ctx.fill(); ctx.fillStyle = '#111827'; ctx.fillText(sub, x + 28, 818);
  ctx.font = font(40, 700, 'JetBrains Mono'); ctx.fillStyle = 'rgba(255,255,255,0.9)'; ctx.fillText('0.8 s / feed  ·  ±0.3 mm', x, 912);
  rr(x, 960, 300, 83, 14); ctx.fillStyle = '#fff'; ctx.fill(); if (logoImg) ctx.drawImage(logoImg, x + 16, 969, 268, 268 * 83 / 300);
  return out.toDataURL('image/png');
};
// debug: render the bare 3D stage with any state/camera (used by dbg.py) — catches mesh/quantization/culling bugs early
window.dbgShot = (o) => { stage.apply(Object.assign({}, o.st || {}));
  stage.setCamera(orbit(o.tg, o.d, o.az, o.el), o.tg, 30, W, H, 0, 0); stage.render(); return glCanvas.toDataURL('image/jpeg', 0.9); };
