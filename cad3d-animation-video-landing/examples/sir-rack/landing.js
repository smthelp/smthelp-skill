// Interactive SMT Intelligent Reel Storage Rack viewer for the "How it works" landing page
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { createStage, ease, seg, lerp, lerp3, orbit, ANCHORS, FILL, NK, NL, slotX, slotY, RAIL_TOP, HERO } from './engine.js';

const HX = slotX(HERO.k), HY = slotY(HERO.L), HI = HERO.L * NK + HERO.k;
const PICKS = []; for (let i = 0; i < NL * NK; i++) { if (FILL[i] && Math.abs(Math.sin(i * 91.7) * 1000 % 1) < 0.075) PICKS.push(i); }
const FIFO_SET = []; for (let k = 40; k < NK && FIFO_SET.length < 3; k += 9) { for (let j = k; j < NK; j++) if (FILL[2 * NK + j]) { FIFO_SET.push(2 * NK + j); k = j; break; } }
const sa = (i, dy = 0) => [slotX(i % NK), RAIL_TOP[Math.floor(i / NK)] - 17 + dy, 200];
const OPC = [0x00c2ad, 0xf5b13d, 0xe879f9];
const STEPS = [
  { id: 'overview', dur: 8, cam: [[0, 940, 0], 5600, -30, 12], labels: [['topR', 'top'], ['heroLed', 'led'], ['panelL', 'panel']] },
  { id: 'register', dur: 8, cam: [[HX + 60, HY - 40, 780], 1500, -18, 6], labels: [[[HX + 40, HY - 60, 787], 'barcode', 'red']] },
  { id: 'store', dur: 9, cam: [[HX + 60, HY - 60, 160], 1900, -30, 10], labels: [['heroLed', 'slot', 'green']] },
  { id: 'pick', dur: 10, cam: [[0, 940, 0], 5200, -14, 6], labels: [[sa(PICKS[2] ?? 0), 'opA'], [sa(PICKS[4] ?? 0), 'opB', 'amber'], [sa(PICKS[8] ?? 0), 'opC', 'mag']] },
  { id: 'fifo', dur: 8, cam: [[420, 960, 0], 2500, -30, 8], labels: [[sa(FIFO_SET[0] ?? 0, 30), 'oldest', 'amber']] },
  { id: 'build', dur: 9, cam: [[0, 1250, 0], 7600, -34, 14], labels: [['panelR', 'panel'], ['rail', 'rail'], ['divider', 'divider', 'sky'], ['foot', 'foot']] },
  { id: 'connect', dur: 8, cam: [[0, 950, 0], 6000, 36, 20], labels: [['topL', 'top'], ['topR', 'net', 'sky']] },
];
const TOTAL = STEPS.reduce((a, s) => a + s.dur, 0);

function stepState(id, lt, D, t) {
  const st = { explode: 0, time: t, slotFn: null, hero: { pos: [HX, HY, 0] }, pda: null, laser: 0, top: [0, 0, 0], highlight: {}, fleet: 1 };
  const pulse = 0.6 + 0.4 * Math.sin(lt * 5), on = seg(lt, 0.4, 1.0) * (1 - seg(lt, D - 0.6, D));
  if (id === 'overview') { st.top = [1, 0, 0]; st.slotFn = (i, L, k, occ) => [occ, 0, 0x00c2ad, on * 0.8 * Math.max(0, Math.sin((k / NK * 5 - t * 1.2 + L * 0.3) * Math.PI))]; }
  if (id === 'register') {
    const fly = ease.io(seg(lt, 0, 1.6)); st.hero = { pos: [HX, lerp(HY + 260, HY, fly), lerp(1500, 780, fly)], ry: Math.PI / 2 * fly };
    const pin = ease.out(seg(lt, 1.4, 2.4));
    st.pda = { pos: [HX + 250 + 160 * (1 - pin), HY - 230 - 120 * (1 - pin), 900], rx: -0.25, ry: -0.35, rz: 0.75, target: [HX + 40, HY - 60, 787], fan: 110, fanAxis: [1, 0, 0] };
    st.laser = seg(lt, 2.4, 2.6) * (1 - seg(lt, 4.5, 4.8)) * (0.7 + 0.3 * Math.sin(t * 40));
  }
  if (id === 'store') {
    const back = ease.io(seg(lt, 0, 1.4)), go = ease.io(seg(lt, 3.2, 4.6)); st.hero = { pos: [HX, HY, lerp(lerp(780, 520, back), 0, go)], ry: Math.PI / 2 * (1 - back) };
    const off = seg(lt, 5.0, 5.3);
    st.slotFn = (i, L, k, occ) => { if (i === HI) return [0, 0, lt > 4.6 ? 0xffffff : 0x22c55e, seg(lt, 1.2, 1.6) * (1 - off)]; if (occ) return [1, 0, null, 0];
      return [0, 0, 0x22c55e, 0.85 * seg(lt, 1.2 + ((k * 7 + L * 13) % 20) * 0.02, 1.6 + ((k * 7 + L * 13) % 20) * 0.02) * (1 - seg(lt, 5.4, 6.2)) * pulse]; };
  }
  if (id === 'pick') {
    st.top = [1, 0, 0];
    st.slotFn = (i, L, k, occ) => { const j = PICKS.indexOf(i); if (j < 0) return [occ, 0, null, 0];
      const tp = 3 + (j % 7) * 0.5 + Math.floor(j / 7) * 0.15; const out = ease.io(seg(lt, tp, tp + 0.7)) * 1.4;
      return [lt > tp + 1.3 && lt < D - 0.8 ? 0 : 1, lt < D - 0.8 ? out : 0, OPC[j % 3], seg(lt, 0.6 + j * 0.04, 1.0 + j * 0.04) * (1 - seg(lt, tp + 0.5, tp + 0.8)) * (0.8 + 0.2 * pulse)]; };
  }
  if (id === 'fifo') {
    st.top = [0, seg(lt, 3, 3.4), 0];
    st.slotFn = (i, L, k, occ) => { const j = FIFO_SET.indexOf(i); if (j < 0 || !occ) return [occ, 0, null, 0];
      if (j === 0) return [1, 0.35 * ease.io(seg(lt, 2, 2.8)), 0xf5b13d, on * (0.7 + 0.3 * Math.sin(t * 9))]; return [1, 0, 0x64748b, on * (1 - seg(lt, 2, 2.4)) * 0.5]; };
  }
  if (id === 'build') { st.explode = ease.io(seg(lt, 0.3, 2.3)) * (1 - ease.io(seg(lt, D - 2, D - 0.2))); st.highlight = { divider: pulse * st.explode * 0.6, panel: pulse * st.explode * 0.3 }; }
  if (id === 'connect') { st.top = [0.6 + 0.4 * Math.sin(t * 3), 0, 0]; st.slotFn = (i, L, k, occ) => [occ, 0, 0x38bdf8, on * 0.4 * Math.max(0, Math.sin((k / NK * 6 - t * 1.4 + L * 0.3) * Math.PI))]; }
  return st;
}

export async function mountViewer(opts) {
  const host = opts.host; const canvas = host.querySelector('canvas');
  const stage = await createStage(canvas, { modelB64: opts.model });
  const cam = stage.camera; cam.near = 20; cam.far = 40000;
  const controls = new OrbitControls(cam, canvas);
  controls.enableDamping = true; controls.enablePan = false; controls.minDistance = 600; controls.maxDistance = 12000; controls.target.set(0, 940, 0);
  const labelLayer = host.querySelector('[data-labels]');
  const labelEls = {}; const txt = opts.label || (k => k);
  let w = 0, h = 0;
  function resize() {
    const r = host.getBoundingClientRect(); w = Math.max(10, r.width); h = Math.max(10, r.height);
    stage.setSize(w, h, Math.min(window.devicePixelRatio || 1, 1.75)); cam.aspect = w / h; cam.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(host); resize();

  let tourT = 0, simT = 0, playing = true, manual = false, visible = true, last = performance.now(), lights = 1;
  let blendFrom = null; const listeners = [];
  function stepAt(t) { let a = 0; for (let i = 0; i < STEPS.length; i++) { if (t < a + STEPS[i].dur) return [i, t - a]; a += STEPS[i].dur; } return [STEPS.length - 1, STEPS[STEPS.length - 1].dur]; }
  function stepStart(i) { let a = 0; for (let k = 0; k < i; k++) a += STEPS[k].dur; return a; }
  let curStep = -1;
  controls.addEventListener('start', () => { manual = true; playing = false; emit(); });
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(host);
  function camFromStep(i, lt) {
    const s = STEPS[i]; const prev = STEPS[(i + STEPS.length - 1) % STEPS.length];
    const k = ease.io(seg(lt, 0, 1.6)); const A = prev.cam, B = s.cam; const nar = w < 640 ? 1.45 : 1;
    const tg = lerp3(A[0], B[0], k); const pos = orbit(tg, lerp(A[1], B[1], k) * nar, lerp(A[2], B[2], k) + lt * 0.8, lerp(A[3], B[3], k));
    return { pos, tg };
  }
  function emit() { listeners.forEach(f => f({ step: curStep, id: STEPS[curStep]?.id, playing, manual, t: tourT, total: TOTAL })); }
  let lastEmit = 0;
  function tick(now) {
    requestAnimationFrame(tick);
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (!visible) return;
    if (playing) tourT = (tourT + dt) % TOTAL;
    simT += dt;
    const [i, lt] = stepAt(tourT);
    if (i !== curStep || now - lastEmit > 200) { curStep = i; lastEmit = now; emit(); }
    let st = stepState(STEPS[i].id, lt, STEPS[i].dur, simT);
    if (manual) st = { explode: 0, time: simT, hero: { pos: [HX, HY, 0] }, pda: null, laser: 0, top: [lights, 0, 0], highlight: {}, fleet: 1,
      slotFn: lights ? (j, L, k, occ) => [occ, 0, occ ? null : 0x22c55e, occ ? 0 : 0.7] : null };
    stage.apply(st);
    if (!manual) {
      const c = camFromStep(i, lt); let pos = c.pos, tg = c.tg;
      if (blendFrom) { const k = ease.io(seg(now, blendFrom.t, blendFrom.t + 900)); pos = lerp3(blendFrom.pos, pos, k); tg = lerp3(blendFrom.tg, tg, k); if (k >= 1) blendFrom = null; }
      cam.position.set(...pos); controls.target.set(...tg); cam.lookAt(...tg);
    } else controls.update();
    stage.render();
    const want = manual ? [] : STEPS[i].labels;
    const fade = Math.min(seg(lt, 1.6, 2.1), 1 - seg(lt, STEPS[i].dur - 0.4, STEPS[i].dur));
    const used = new Set();
    for (const [anc, key, tone] of want) {
      const id = STEPS[i].id + key; used.add(id);
      let el = labelEls[id];
      if (!el) { el = document.createElement('div'); el.className = 'rs3d-label' + (tone ? ' rs3d-' + tone : ''); el.innerHTML = '<i></i><span></span>'; labelLayer.appendChild(el); labelEls[id] = el; }
      el.querySelector('span').textContent = txt(key);
      const p = stage.project(typeof anc === 'string' ? ANCHORS[anc] : anc, w, h);
      el.style.transform = `translate(${p[0].toFixed(1)}px, ${p[1].toFixed(1)}px)`;
      el.style.opacity = (p[2] < 1 && p[0] > 0 && p[0] < w && p[1] > 0 && p[1] < h ? fade : 0).toFixed(3);
      el.classList.toggle('rs3d-left', p[0] > w * 0.6);
    }
    for (const [k, el] of Object.entries(labelEls)) if (!used.has(k)) el.style.opacity = 0;
  }
  requestAnimationFrame(tick);
  return {
    steps: STEPS.map(s => s.id), total: TOTAL,
    onChange(f) { listeners.push(f); },
    goTo(idx) { blendFrom = { pos: cam.position.toArray(), tg: controls.target.toArray(), t: performance.now() }; manual = false; playing = true; tourT = stepStart(idx) + 0.01; emit(); },
    play() { if (manual) blendFrom = { pos: cam.position.toArray(), tg: controls.target.toArray(), t: performance.now() }; manual = false; playing = true; emit(); },
    pause() { playing = false; emit(); },
    toggle() { (playing && !manual) ? this.pause() : this.play(); },
    setLights(v) { lights = v ? 1 : 0; },
  };
}
window.RACK3D = { mountViewer };
