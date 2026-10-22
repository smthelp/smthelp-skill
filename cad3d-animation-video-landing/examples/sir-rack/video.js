// Video timeline renderer for SMT Intelligent Reel Storage Rack film (16:9 + 9:16)
import { createStage, ease, seg, lerp, lerp3, orbit, clamp01, ANCHORS, FILL, NK, NL, slotX, slotY, RAIL_TOP, HERO } from './engine.js';

const TEAL = '#00C2AD', TEAL2 = '#00A896', SKY = '#38BDF8', AMBER = '#F5B13D', RED = '#ff5a4f';
let stage, out, ctx, glCanvas, W, H, LW, LH, S, portrait, VO, scenes, logoImg, TOTAL;

// caption phrase map: spoken word sequences -> on-screen text (lower-case match, punctuation kept from the script)
const CAPMAP = [
  [['error', 'prone'], 'error-prone'], [['24', 'millimetre'], '24 mm'], [['220', 'volts'], '220 V'], [['100', 'watts'], '100 W'],
  [['smthelp', 'dot', 'com'], 'smthelp.com'], [['3', 'to', '12', 'months'], '3–12 months'], [['one', 'hundred'], 'one hundred'],
];
const GREEN_C = '#22c55e';
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
  ctx.fillText('INTELLIGENT REEL STORAGE RACK', x + 228, y + 29);
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
  const sx = shiftX ?? (portrait ? 0 : 0.19), sy = shiftY ?? (portrait ? 0.14 : 0.02);
  stage.setCamera(orbit(target, dist, az, el), target, fov, W, H, sx, sy);
}
function camBlend(A, B, k) {
  if (portrait) { A = A.p || A; B = B.p || B; } else { A = A.l || A; B = B.l || B; }
  const kk = ease.io(clamp01(k)); const tg = lerp3(A[0], B[0], kk);
  cam(tg, lerp(A[1], B[1], kk), lerp(A[2], B[2], kk), lerp(A[3], B[3], kk), lerp(A[4] ?? 30, B[4] ?? 30, kk), A[5] == null ? null : lerp(A[5], B[5], kk), A[6] == null ? null : lerp(A[6], B[6], kk));
}
const V = (l, p) => ({ l, p });
const HX = slotX(HERO.k), HY = slotY(HERO.L);
const HOOK0 = V([[-500, 1000, 120], 1500, -62, 6], [[-500, 1000, 120], 2300, -62, 6]);
const HOOK1 = V([[0, 930, 0], 5600, -38, 12], [[0, 930, 0], 6900, -52, 12]);
const WIDE = V([[0, 940, 0], 6200, -24, 10], [[0, 940, 0], 8200, -40, 10]);
const SCAN = V([[HX + 60, HY - 40, 780], 1300, -18, 6], [[HX + 60, HY - 120, 780], 2100, -14, 4]);
const STORE1 = V([[HX + 120, HY - 120, 260], 2300, -26, 8], [[HX + 60, HY - 160, 260], 3300, -26, 8]);
const STORE2 = V([[HX + 60, HY - 40, 120], 1250, -32, 10], [[HX + 40, HY - 40, 120], 1800, -30, 8]);
const PICKW = V([[0, 930, 0], 5900, -14, 6], [[0, 1150, 0], 8200, -34, 8]);
const FIFO = V([[420, 960, 0], 2300, -30, 8], [[380, 960, 0], 3400, -30, 8]);
const EXPL = V([[0, 1250, 0], 8600, -34, 14], [[0, 1300, 0], 12000, -46, 14]);
const CONN = V([[0, 950, 0], 6600, 32, 20], [[0, 1250, 0], 9000, 40, 20]);
const RESULT = V([[0, 940, 0], 6400, -30, 12], [[0, 1350, 0], 9000, -44, 12]);

const TEAL_H = 0x00c2ad, AMB_H = 0xf5b13d, MAG_H = 0xe879f9, SKY_H = 0x38bdf8, RED_H = 0xff4d4d, GRN_H = 0x22c55e, WHT_H = 0xffffff;
// pick list: a deterministic spread of occupied reels, three operators
const PICKS = []; for (let i = 0; i < NL * NK; i++) { if (FILL[i] && Math.abs(Math.sin(i * 91.7) * 1000 % 1) < 0.075) PICKS.push(i); }
const OPCOL = [TEAL_H, AMB_H, MAG_H];
// FIFO: three reels of the same part on layer 2
const FIFO_SET = []; for (let k = 40; k < NK && FIFO_SET.length < 3; k += 9) { for (let j = k; j < NK; j++) if (FILL[2 * NK + j]) { FIFO_SET.push(2 * NK + j); k = j; break; } }
const slotAnchor = (i, dy = 0) => [slotX(i % NK), RAIL_TOP[Math.floor(i / NK)] - 17 + dy, 200];

function card(t, a, b, x, y, w, title, rows, opt = {}) {
  const al = fadeIO(t, a, b, 0.4, 0.4); if (al <= 0) return;
  const rh = opt.rh || 58, h = 86 + rows.length * rh + 20;
  ctx.save(); ctx.globalAlpha = al;
  rr(x, y, w, h, 20); ctx.fillStyle = 'rgba(7,13,30,0.9)'; ctx.fill(); ctx.strokeStyle = opt.col || TEAL; ctx.lineWidth = 2.5; ctx.stroke();
  ctx.fillStyle = opt.col || TEAL; ctx.fillRect(x, y + 18, 6, 48);
  ctx.textBaseline = 'middle'; ctx.font = font(26, 700, 'JetBrains Mono'); ctx.fillStyle = opt.col || TEAL; ctx.fillText(title, x + 28, y + 43);
  rows.forEach((r, i) => {
    const ai = ease.out(seg(t, r.t ?? a, (r.t ?? a) + 0.35)); if (ai <= 0) return;
    ctx.globalAlpha = al * ai; const yy = y + 86 + i * rh + rh / 2;
    ctx.fillStyle = 'rgba(255,255,255,0.06)'; rr(x + 18, yy - rh / 2 + 5, w - 36, rh - 10, 10); ctx.fill();
    if (r.dot != null) { ctx.fillStyle = '#' + r.dot.toString(16).padStart(6, '0'); ctx.beginPath(); ctx.arc(x + 44, yy, 10, 0, 7); ctx.fill(); }
    ctx.font = font(r.k ? 24 : 26, 600, r.k ? 'JetBrains Mono' : 'Inter'); ctx.fillStyle = 'rgba(203,213,225,0.9)'; ctx.fillText(r.k || '', x + (r.dot != null ? 66 : 34), yy);
    ctx.font = font(28, 700); ctx.fillStyle = r.c || '#fff'; const vw = ctx.measureText(r.v).width; ctx.fillText(r.v, x + w - 34 - vw, yy);
  });
  ctx.restore();
}
function stat(t, a, b, x, y, w, big, small, col = TEAL) {
  const al = fadeIO(t, a, b, 0.35, 0.3); if (al <= 0) return;
  ctx.save(); ctx.globalAlpha = al; const h = 170;
  const s = 0.92 + 0.08 * ease.out(seg(t, a, a + 0.5)); ctx.translate(x, y); ctx.scale(s, s);
  rr(0, 0, w, h, 20); ctx.fillStyle = 'rgba(7,13,30,0.85)'; ctx.fill(); ctx.strokeStyle = col; ctx.lineWidth = 3; ctx.stroke();
  ctx.fillStyle = col; ctx.fillRect(0, 20, 7, h - 40);
  ctx.textBaseline = 'alphabetic'; ctx.font = font(84, 900); ctx.fillStyle = '#fff'; ctx.fillText(big, 34, 100);
  ctx.font = font(30, 600); ctx.fillStyle = 'rgba(203,213,225,0.95)'; ctx.fillText(small, 36, 146); ctx.restore();
}
function netDiagram(t, a, b) {
  const al = fadeIO(t, a, b, 0.5, 0.4); if (al <= 0) return;
  const nodes = portrait
    ? [['ERP / MES', 'SAP · Oracle', 160, 640], ['WMS server', 'HTTP + JSON', 540, 640], ['PDA scanner', 'Wi-Fi', 920, 640]]
    : [['ERP / MES', 'SAP · Oracle', 200, 680], ['WMS server', 'HTTP + JSON', 470, 680], ['PDA scanner', 'Wi-Fi', 740, 680]];
  const rack = portrait ? [540, 820] : [470, 850];
  ctx.save(); ctx.globalAlpha = al;
  nodes.forEach(([n, s, x, y], i) => {
    const ai = ease.out(seg(t, a + 0.25 * i, a + 0.25 * i + 0.4)); ctx.globalAlpha = al * ai;
    ctx.strokeStyle = 'rgba(56,189,248,0.8)'; ctx.lineWidth = 3; ctx.setLineDash([12, 10]); ctx.lineDashOffset = -t * 60;
    ctx.beginPath(); ctx.moveTo(x, y + 50); ctx.lineTo(rack[0], rack[1] - 40); ctx.stroke(); ctx.setLineDash([]);
    rr(x - 120, y - 50, 240, 100, 16); ctx.fillStyle = 'rgba(7,13,30,0.92)'; ctx.fill(); ctx.strokeStyle = SKY; ctx.lineWidth = 2; ctx.stroke();
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = font(27, 800); ctx.fillStyle = '#fff'; ctx.fillText(n, x, y - 14);
    ctx.font = font(22, 600, 'JetBrains Mono'); ctx.fillStyle = SKY; ctx.fillText(s, x, y + 20); ctx.textAlign = 'left';
  });
  ctx.globalAlpha = al; rr(rack[0] - 170, rack[1] - 44, 340, 88, 16); ctx.fillStyle = TEAL2; ctx.fill();
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = font(30, 800); ctx.fillStyle = '#fff'; ctx.fillText('Reel rack  ·  LAN / Wi-Fi', rack[0], rack[1] + 2); ctx.textAlign = 'left';
  ctx.restore();
}

function frame(t) {
  const { by } = scenes;
  const st = { explode: 0, time: t, slotFn: null, hero: null, pda: null, laser: 0, top: [0, 0, 0], highlight: {}, fleet: 1 };
  let overlay = () => { };
  const sid = scenes.list.find(s => t >= s.start && t < s.end)?.id || (t < 0.6 ? 'hook' : 'cta');
  const sc = by[sid]; const lt = t - sc.start; const L = sc.len; const PS = portrait;
  const pulse = 0.55 + 0.45 * Math.sin(t * 6);
  const heroIn = t >= wordT(by.store, 'Put') + 1.6;   // hero reel lives in its slot after the store scene
  if (t > by.store.start + 0.2 && sid !== 'build') st.hero = { pos: [HX, HY, 0] };

  if (sid === 'hook') {
    camBlend(HOOK0, HOOK1, seg(lt, 0, L));
    overlay = () => {
      textBlock(t, sc.start + 0.4, sc.end - 0.2, 'THE REEL PROBLEM', 'Which reel? Which shelf?', null, PS ? { y: 250 } : { x: 110, y: 330, w: 720 });
      const tags = [['✕  Slow', wordT(sc, 'slow')], ['✕  Error-prone', wordT(sc, 'error')], ['✕  Line stops', wordT(sc, 'stops')]];
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
    camBlend(HOOK1, WIDE, seg(lt, 0, L * 0.8));
    const tl = wordT(sc, 'LED'), tlay = wordT(sc, 'layers');
    st.slotFn = (i, Ly, k, occ) => { const w = seg(t, tl - 0.4 + k * 0.012 + Ly * 0.05, tl + 0.2 + k * 0.012 + Ly * 0.05) * (1 - seg(t, sc.end - 0.6, sc.end)); return [occ, 0, TEAL_H, w * 0.9]; };
    st.top = [fadeIO(t, tl, sc.end + 2), 0, 0];
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, 'INTRODUCING', 'Intelligent Reel Storage Rack', 'by Southern Machinery', PS ? { hs: 92 } : { hs: 92, y: 300, w: 760 });
      chips(t, tlay - 0.2, sc.end - 0.1, ['5 layers', '100 slots per layer', 'An LED for every slot'], PS ? 64 : 110, PS ? 720 : 700);
      const fa = fadeIO(t, tl, sc.end - 0.1); if (fa > 0) { ctx.save(); ctx.globalAlpha = fa * 0.7; ctx.font = font(22, 500); ctx.fillStyle = '#cbd5e1'; ctx.fillText('Rack geometry from CAD · LEDs, lights and scanner shown illustratively', PS ? 64 : 110, PS ? 1560 : 900); ctx.restore(); }
    };
  }
  else if (sid === 'register') {
    const ts = wordT(sc, 'Scan'), tp = wordT(sc, 'part'), tq = wordT(sc, 'quantity'), tlo = wordT(sc, 'lot'), tid = wordT(sc, 'unique');
    camBlend(WIDE, SCAN, seg(lt, 0, 2.6));
    const fly = ease.io(seg(lt, 0, 2.2));
    st.hero = { pos: [HX, lerp(HY + 260, HY, fly), lerp(1600, 780, fly)], ry: Math.PI / 2 * fly };
    const pin = ease.out(seg(t, ts - 1.0, ts));
    st.pda = { pos: [HX + 250 + 160 * (1 - pin), HY - 230 - 120 * (1 - pin), 900], rx: -0.25, ry: -0.35, rz: 0.75, target: [HX + 40, HY - 60, 786], fan: 110, fanAxis: [1, 0, 0] };
    st.laser = fadeIO(t, ts, ts + 1.2, 0.1, 0.25) * (0.7 + 0.3 * Math.sin(t * 40));
    overlay = () => {
      const yb = textBlock(t, sc.start + 0.3, sc.end - 0.1, '01 · REGISTER', 'Scan once. Traced forever.', null, PS ? {} : { w: 760 }) || 560;
      const x = PS ? 64 : 110, y = yb - 20, w = PS ? LW - 128 : 700;
      card(t, ts + 0.5, sc.end - 0.15, x, y, w, 'REEL REGISTERED', [
        { k: 'Part number', v: 'RC0402-10K', t: tp }, { k: 'Quantity', v: '10 000', t: tq }, { k: 'Lot code', v: 'L2610-0417', t: tlo }, { k: 'Unique ID', v: 'SM-000731', c: TEAL, t: tid }]);
      callout(t, ts - 0.3, ts + 1.6, [HX + 40, HY - 60, 786], 'Manufacturer barcode', 'r', { dx: PS ? 130 : 200, dy: -140, color: RED });
    };
  }
  else if (sid === 'store') {
    const te = wordT(sc, 'empty'), tput = wordT(sc, 'Put'), tc = wordT(sc, 'confirmed'), to = wordT(sc, 'goes'), tinv = wordT(sc, 'inventory');
    camBlend(SCAN, STORE1, seg(lt, 0, 2.4));
    if (t > tput - 0.4) camBlend(STORE1, STORE2, seg(t, tput - 0.4, tc));
    const back = ease.io(seg(lt, 0, 1.6)); const go = ease.io(seg(t, tput, tput + 1.4));
    st.hero = { pos: [HX, HY, lerp(lerp(780, 520, back), 0, go)], ry: Math.PI / 2 * (1 - back) };
    const hi = HERO.L * NK + HERO.k;
    st.slotFn = (i, Ly, k, occ) => {
      if (i === hi) { const blink = t > tc - 0.2 && t < to ? (Math.sin(t * 30) > 0 ? 1 : 0.2) : 1; return [0, 0, t > tc - 0.2 ? WHT_H : GRN_H, seg(t, te - 0.3, te + 0.3) * (1 - seg(t, to, to + 0.25)) * blink]; }
      if (occ) return [1, 0, null, 0];
      return [0, 0, GRN_H, 0.85 * seg(t, te - 0.3 + ((k * 7 + Ly * 13) % 20) * 0.02, te + 0.3 + ((k * 7 + Ly * 13) % 20) * 0.02) * (1 - seg(t, to + 0.2, to + 1.0)) * (0.75 + 0.25 * pulse)];
    };
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '02 · GUIDED STORING', 'Any lit slot will do', 'The system remembers exactly where it went.', PS ? {} : { w: 740 });
      callout(t, tput + 0.2, to + 0.2, ANCHORS.heroLed, 'Slot LED', 'r', { dx: PS ? 130 : 200, dy: 110, color: GREEN_C });
      callout(t, to - 0.1, sc.end - 0.2, ANCHORS.heroLed, 'Placed · light off', 'r', { dx: PS ? 130 : 200, dy: 110, color: TEAL, sub: 'Location: Layer 4 · Slot 30' });
      chips(t, tinv - 0.2, sc.end - 0.1, ['Inventory updated in real time'], PS ? 64 : 110, PS ? 640 : 640, [SKY]);
    };
  }
  else if (sid === 'pick') {
    const ti = wordT(sc, 'imported'), tl = wordT(sc, 'lights'), tc = wordT(sc, 'seven'), tk = wordT(sc, 'kit');
    camBlend(STORE2, PICKW, seg(lt, 0, 2.8));
    const order = PICKS.map((i, j) => [i, j]);
    st.slotFn = (i, Ly, k, occ) => {
      const j = PICKS.indexOf(i); if (j < 0) return [occ, 0, null, 0];
      const on = seg(t, tl - 0.2 + j * 0.05, tl + 0.2 + j * 0.05); const col = t > tc - 0.2 ? OPCOL[j % 3] : TEAL_H;
      const tp = tk - 0.4 + (j % 7) * 0.32 + Math.floor(j / 7) * 0.12; const out = ease.io(seg(t, tp, tp + 0.7)) * 1.4;
      const gone = t > tp + 1.3; return [gone ? 0 : 1, out, col, on * (1 - seg(t, tp + 0.5, tp + 0.8)) * (0.8 + 0.2 * pulse)];
    };
    st.top = [fadeIO(t, tl, sc.end), 0, 0];
    overlay = () => {
      const yb = textBlock(t, sc.start + 0.3, sc.end - 0.1, '03 · REQUEST & PICK', 'The BOM lights the way', null, PS ? {} : { w: 820 }) || 520;
      const x = PS ? 64 : 110, y = yb - 20, w = PS ? LW - 128 : 640;
      card(t, ti - 0.2, sc.end - 0.15, x, y, w, 'JOB  WO-2610-18  ·  BOM', [
        { k: 'RC0402-10K', v: '✓ 2 reels', dot: t > tc - 0.2 ? OPCOL[0] : TEAL_H, t: ti + 0.3 }, { k: 'CC0603-100N', v: '✓ 3 reels', dot: t > tc - 0.2 ? OPCOL[1] : TEAL_H, t: ti + 0.6 },
        { k: 'IC-SOT23-5', v: '✓ 1 reel', dot: t > tc - 0.2 ? OPCOL[2] : TEAL_H, t: ti + 0.9 }, { k: 'LED-0805-W', v: '✓ 2 reels', dot: t > tc - 0.2 ? OPCOL[0] : TEAL_H, t: ti + 1.2 }], { rh: 54 });
      chips(t, tc - 0.2, sc.end - 0.1, ['Operator A', 'Operator B', 'Operator C'], x, y + 370, [TEAL, AMBER, '#e879f9']);
    };
  }
  else if (sid === 'fifo') {
    const tf = wordT(sc, 'first'), tm = wordT(sc, 'missing');
    camBlend(PICKW, FIFO, seg(lt, 0, 2.6));
    st.slotFn = (i, Ly, k, occ) => {
      const j = FIFO_SET.indexOf(i); if (j < 0 || !occ) return [occ, 0, null, 0];
      if (j === 0) return [1, 0.35 * ease.io(seg(t, tf, tf + 0.8)), AMB_H, seg(t, sc.start + 0.8, sc.start + 1.2) * (t > tf ? 0.7 + 0.3 * Math.sin(t * 9) : 0.5)];
      return [1, 0, 0x64748b, seg(t, sc.start + 0.8, sc.start + 1.2) * (1 - seg(t, tf, tf + 0.4)) * 0.5];
    };
    st.top = [0, fadeIO(t, tm - 0.2, sc.end), 0];
    overlay = () => {
      const yb = textBlock(t, sc.start + 0.3, sc.end - 0.1, '04 · FIFO + SHORTAGE', 'Oldest reel first.', 'First in, first out, without thinking about it.', PS ? {} : { w: 760 }) || 560;
      const ds = ['DC 2534', 'DC 2611', 'DC 2618'];
      FIFO_SET.forEach((i, j) => callout(t, sc.start + 1.0 + j * 0.25, j === 0 ? sc.end - 0.2 : tf + 0.3, slotAnchor(i, 30), j === 0 ? 'Pick this one first' : ds[j], j === 2 ? 'r' : 'l', { dx: PS ? 90 : 130, dy: j === 0 ? 150 : (j === 1 ? -110 : -110), color: j === 0 ? AMBER : '#94a3b8', sub: j === 0 ? 'Oldest date code · ' + ds[0] : null }));
      const x = PS ? 64 : 110, y = yb + 10, w = PS ? LW - 128 : 640;
      card(t, tm - 0.2, sc.end - 0.15, x, y, w, 'SHORTAGE ALERT', [{ k: 'CC0603-1U', v: 'Line 2 · 14 min left', c: '#fecaca', t: tm }], { col: '#ef4444' });
    };
  }
  else if (sid === 'build') {
    const tp = wordT(sc, 'panels'), tr = wordT(sc, 'rails'), td = wordT(sc, 'dividers'), tf = wordT(sc, 'feet'), tw = wordT(sc, 'widths');
    st.explode = ease.io(seg(lt, 0.4, 2.8)) * (1 - ease.io(seg(lt, L - 2.4, L - 0.3)));
    st.highlight = { panel: fadeIO(t, tp - 0.3, tr, 0.3, 0.3) * pulse, rail: fadeIO(t, tr - 0.3, td, 0.3, 0.3) * pulse, divider: fadeIO(t, td - 0.3, tf, 0.3, 0.3) * pulse, foot: fadeIO(t, tf - 0.3, tw, 0.3, 0.3) * pulse };
    camBlend(FIFO, EXPL, seg(lt, 0, 2.6));
    if (lt > L - 2.6) camBlend(EXPL, CONN, seg(lt, L - 2.6, L));
    const e = st.explode; const ex = (a, dx, dy) => [a[0] + dx * e, a[1] + dy * e, a[2]];
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, '05 · THE RACK', 'Simple by design', 'Real geometry from the CAD model.', PS ? {} : { w: 700 });
      callout(t, tp - 0.3, tr - 0.1, ex(ANCHORS.panelR, 420, 0), 'End panels', 'l', { dx: PS ? 120 : 200, dy: -120 });
      callout(t, tr - 0.2, td - 0.1, ex(ANCHORS.rail, 0, 3 * 120), '10 rails', 'r', { dx: PS ? 110 : 180, dy: -110 });
      callout(t, td - 0.2, tf - 0.1, ex(ANCHORS.divider, 0, 3 * 120), 'Wire dividers · 24 mm pitch', 'r', { dx: PS ? 100 : 170, dy: -130, color: SKY });
      callout(t, tf - 0.2, tw, ex(ANCHORS.foot, -420, -160), '4 levelling feet', 'r', { dx: PS ? 110 : 180, dy: -90 });
      chips(t, tw - 0.2, sc.end - 0.1, ['Adjustable slot width', '7" · 13" · 15" reels'], PS ? 64 : 110, PS ? 700 : 680, [TEAL, AMBER]);
    };
  }
  else if (sid === 'connect') {
    const tn = wordT(sc, 'network'), ts = wordT(sc, 'SAP'), th = wordT(sc, 'HTTP'), tv = wordT(sc, '220');
    camBlend(CONN, V([[0, 950, 0], 6900, 44, 22], [[0, 1250, 0], 9400, 52, 22]), seg(lt, 0, L));
    const ph = (t * 0.6) % 1; st.top = [0.6 + 0.4 * Math.sin(t * 3), 0, 0];
    st.slotFn = (i, Ly, k, occ) => { const w = Math.max(0, Math.sin((k / NK * 6 - t * 1.4 + Ly * 0.3) * Math.PI)); return [occ, 0, SKY_H, fadeIO(t, tn, sc.end) * w * 0.35]; };
    overlay = () => {
      const yb = textBlock(t, sc.start + 0.3, sc.end - 0.1, '06 · CONNECT', 'Plugs into your systems', null, PS ? {} : { w: 860 }) || 520;
      netDiagram(t, tn - 0.2, sc.end - 0.15);
      chips(t, tv - 0.2, sc.end - 0.1, ['220 V', '< 100 W', 'Ethernet or Wi-Fi'], PS ? 64 : 110, PS ? yb - 30 : yb, [AMBER, AMBER, SKY]);
    };
  }
  else if (sid === 'result') {
    const t1 = wordT(sc, '99'), t2 = wordT(sc, '75'), t3 = wordT(sc, '100'), t4 = wordT(sc, 'payback');
    camBlend(V([[0, 950, 0], 6900, 44, 22], [[0, 1250, 0], 9400, 52, 22]), RESULT, seg(lt, 0, 3));
    st.slotFn = (i, Ly, k, occ) => { const c = [TEAL_H, AMB_H, MAG_H, SKY_H, GRN_H][(Math.floor(k / 20) + Ly) % 5]; const w = 0.5 + 0.5 * Math.sin(k * 0.3 - t * 3 + Ly); return [occ, 0, c, seg(lt, 0.5, 2) * w * 0.7]; };
    st.top = [1, 0, 0];
    overlay = () => {
      textBlock(t, sc.start + 0.3, sc.end - 0.1, 'THE RESULT', 'A transformed warehouse', null, PS ? {} : { w: 900 });
      const x = PS ? 64 : 110, w = PS ? 470 : 560;
      const pos = PS ? [[64, 520], [546, 520], [64, 710], [546, 710]] : [[110, 470], [110, 660], [580, 470], [580, 660]];
      [['99.9%', 'picking accuracy', t1], ['>75%', 'faster kitting', t2], ['100%', 'inventory visibility', t3], ['3–12 mo', 'typical payback', t4]].forEach(([b, s, ta], j) =>
        stat(t, ta - 0.2, sc.end - 0.15, pos[j][0], pos[j][1], PS ? 470 : 450, b, s, j === 3 ? AMBER : TEAL));
    };
  }
  else if (sid === 'cta') {
    camBlend(RESULT, V([[0, 940, 0], 7000, -40, 12, 30, 0.22, 0.02], [[0, 940, 0], 9400, -46, 12, 30, 0, 0.3]), seg(lt, 0, L));
    st.slotFn = (i, Ly, k, occ) => [occ, 0, TEAL_H, (occ ? 0 : 0.6) * seg(lt, 0, 1.5)];
    st.top = [1, 0, 0];
    overlay = () => {
      const a0 = sc.start + 0.6; const al = ease.out(seg(t, a0, a0 + 0.8));
      ctx.save(); ctx.globalAlpha = al;
      const x = PS ? 64 : 110; let y = 150;
      rr(x, y, 300, 83, 14); ctx.fillStyle = '#fff'; ctx.fill(); if (logoImg) ctx.drawImage(logoImg, x + 16, y + 9, 268, 268 * 83 / 300);
      y += 160; ctx.font = font(62, 800); ctx.fillStyle = '#fff'; ctx.textBaseline = 'alphabetic';
      for (const l of wrap('Your reels. Your floor. Configured for you.', PS ? LW - 128 : 780)) { ctx.fillText(l, x, y); y += 72; }
      ctx.restore();
      const bullets = [['LED-guided storing and picking', sc.start + 0.9], ['ERP / MES integration · HTTP + JSON', sc.start + 1.4], ['7" · 13" · 15" reel slots', wordT(sc, 'configure')], ['Source factory since 2011', wordT(sc, 'Southern')]];
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
  const hi = HERO.L * NK + HERO.k;
  stage.apply({ explode: 0, time: 0.3, hero: { pos: [HX, HY, 0] }, pda: null, laser: 0, top: [1, 0, 0], highlight: {}, fleet: 1,
    slotFn: (i, Ly, k, occ) => { const j = PICKS.indexOf(i); if (j >= 0) return [1, 0.5, OPCOL[j % 3], 1]; if (!occ && (k + Ly) % 3 === 0) return [0, 0, GRN_H, 0.8]; return [occ, 0, null, 0]; } });
  const tg = opt.target || [250, 950, 0];
  stage.setCamera(orbit(tg, opt.dist || 4300, opt.az ?? -32, opt.el ?? 10), tg, 30, W, H, opt.sx ?? 0.2, opt.sy ?? 0.0);
  stage.render();
  ctx.setTransform(S, 0, 0, S, 0, 0); drawBG(0);
  const gx = LW * 0.68, gy = LH * 0.5; const g = ctx.createRadialGradient(gx, gy, 10, gx, gy, 620);
  g.addColorStop(0, 'rgba(0,194,173,0.32)'); g.addColorStop(1, 'rgba(0,194,173,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, LW, LH);
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(glCanvas, 0, 0, W, H); ctx.setTransform(S, 0, 0, S, 0, 0);
  drawVignette();
  const lg = ctx.createLinearGradient(0, 0, 900, 0); lg.addColorStop(0, 'rgba(4,8,20,0.85)'); lg.addColorStop(1, 'rgba(4,8,20,0)'); ctx.fillStyle = lg; ctx.fillRect(0, 0, 900, LH);
  const x = 90; ctx.textBaseline = 'alphabetic';
  ctx.font = font(34, 800, 'JetBrains Mono'); const kt = 'SMT SMART WAREHOUSE'; const kw = ctx.measureText(kt).width + 48;
  rr(x, 110, kw, 64, 32); ctx.fillStyle = 'rgba(0,194,173,0.18)'; ctx.fill(); ctx.strokeStyle = TEAL; ctx.lineWidth = 3; ctx.stroke(); ctx.fillStyle = TEAL; ctx.fillText(kt, x + 24, 155);
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,0.6)'; ctx.shadowBlur = 24;
  ctx.font = font(170, 900); ctx.fillStyle = '#fff'; ctx.fillText('FIND ANY', x - 6, 370);
  ctx.fillStyle = TEAL; ctx.fillText('REEL', x - 4, 540); ctx.fillStyle = '#fff'; ctx.font = font(150, 900); ctx.fillText('IN SECONDS', x - 4, 700);
  ctx.restore();
  ctx.font = font(44, 800); const sub = 'Intelligent Reel Storage Rack'; const sw = ctx.measureText(sub).width + 56;
  rr(x, 760, sw, 86, 16); ctx.fillStyle = AMBER; ctx.fill(); ctx.fillStyle = '#111827'; ctx.fillText(sub, x + 28, 818);
  ctx.font = font(40, 700, 'JetBrains Mono'); ctx.fillStyle = 'rgba(255,255,255,0.9)'; ctx.fillText('LED-guided · 99.9% picking accuracy', x, 912);
  rr(x, 960, 300, 83, 14); ctx.fillStyle = '#fff'; ctx.fill(); if (logoImg) ctx.drawImage(logoImg, x + 16, 969, 268, 268 * 83 / 300);
  return out.toDataURL('image/png');
};
window.dbgShot = (o) => { stage.apply(Object.assign({ explode: 0, time: 0, slotFn: null, hero: null, pda: null, laser: 0, top: [0, 0, 0], highlight: {}, fleet: 1 }, o.st || {}));
  stage.setCamera(orbit(o.tg, o.d, o.az, o.el), o.tg, 30, W, H, 0, 0); stage.render(); return glCanvas.toDataURL('image/jpeg', 0.9); };
