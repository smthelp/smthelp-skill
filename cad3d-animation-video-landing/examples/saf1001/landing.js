// Interactive SAF1001 axial tape feeder viewer for the landing page
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { createStage, ease, seg, lerp, lerp3, orbit, ANCHORS } from './engine.js';

const STEPS = [
  { id: 'overview', dur: 7, slow: 1, cam: [[-10, 150, 0], 1050, -52, 20], labels: [['tray', 'tray'], ['pawl', 'pawl'], ['pick', 'pick'], ['ebox', 'ebox']] },
  { id: 'load', dur: 8, slow: 1, cam: [[60, 190, 0], 750, 30, 30], labels: [['tray', 'tray'], ['guideblk', 'guideblk'], ['press', 'press'], ['claw', 'claw']] },
  { id: 'index', dur: 9, slow: 0.3, cam: [[-222, 228, 8], 340, -18, 44], labels: [['pawl', 'pawl'], ['feedcyl', 'feedcyl', 'sky'], ['stop', 'stop']] },
  { id: 'form', dur: 9, slow: 0.3, cam: [[-284, 222, 0], 330, -96, 40], labels: [['knife', 'knife'], ['formed', 'formed'], ['cutcyl', 'cutcyl', 'sky']] },
  { id: 'pick', dur: 8, slow: 0.35, cam: [[-282, 240, 0], 380, -70, 32], labels: [['fibre', 'fibre', 'red'], ['pick', 'pick']] },
  { id: 'waste', dur: 8, slow: 0.6, cam: [[-150, 112, 0], 700, -88, 8], labels: [['tapecyl', 'tapecyl', 'sky'], ['tapeknife', 'tapeknife'], ['chute', 'chute']] },
  { id: 'explode', dur: 8, slow: 1, cam: [[-10, 150, 0], 1700, -55, 20], labels: [['plug', 'plug'], ['mount', 'mount']] },
];
const TOTAL = STEPS.reduce((a, s) => a + s.dur, 0);

function stepState(id, lt, D, t) {
  const st = { explode: 0, ghost: 0, ghostU: 0, time: t, cycT: t, run: 1, head: 0, fibre: 0.6, air: 0, chips: 0, highlight: {}, compsVisible: true };
  const pulse = 0.6 + 0.4 * Math.sin(lt * 5), on = seg(lt, 0.5, 1.1) * (1 - seg(lt, D - 0.6, D));
  if (id === 'overview') st.head = 1;
  if (id === 'load') st.highlight = { carton: on * pulse * 0.6, guideblk: on * pulse, claw: on * pulse };
  if (id === 'index') { st.air = 1; st.highlight = { pawls: on * pulse, stop: on * pulse * 0.6 }; }
  if (id === 'form') { st.ghostU = on; st.ghost = 0.7 * on; st.highlight = { knife_move: on * pulse * 0.7, cutcyl: on * pulse * 0.6 }; }
  if (id === 'pick') { st.ghostU = on; st.head = 1; st.fibre = 1; }
  if (id === 'waste') { st.ghost = on; st.chips = on; st.highlight = { tapeknife: on * pulse * 0.7 }; }
  if (id === 'explode') { st.explode = ease.io(seg(lt, 0.3, 2.3)) * (1 - ease.io(seg(lt, D - 2, D - 0.2))); st.highlight = { plug: pulse * st.explode * 0.6 }; }
  return st;
}

export async function mountViewer(opts) {
  const host = opts.host; const canvas = host.querySelector('canvas');
  const stage = await createStage(canvas, { modelB64: opts.model });
  const cam = stage.camera; cam.near = 5; cam.far = 10000;
  const controls = new OrbitControls(cam, canvas);
  controls.enableDamping = true; controls.enablePan = false; controls.minDistance = 120; controls.maxDistance = 3500; controls.target.set(-10, 140, 0);
  const labelLayer = host.querySelector('[data-labels]');
  const labelEls = {}; const txt = opts.label || (k => k);
  let w = 0, h = 0;
  function resize() {
    const r = host.getBoundingClientRect(); w = Math.max(10, r.width); h = Math.max(10, r.height);
    stage.setSize(w, h, Math.min(window.devicePixelRatio || 1, 1.75)); cam.aspect = w / h; cam.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(host); resize();

  let tourT = 0, simT = 0, rate = 1, ghost = null, playing = true, manual = false, visible = true, last = performance.now();
  let blendFrom = null; const listeners = [];
  function stepAt(t) { let a = 0; for (let i = 0; i < STEPS.length; i++) { if (t < a + STEPS[i].dur) return [i, t - a]; a += STEPS[i].dur; } return [STEPS.length - 1, STEPS[STEPS.length - 1].dur]; }
  function stepStart(i) { let a = 0; for (let k = 0; k < i; k++) a += STEPS[k].dur; return a; }
  let curStep = -1;
  controls.addEventListener('start', () => { manual = true; playing = false; emit(); });
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(host);
  function camFromStep(i, lt) {
    const s = STEPS[i]; const prev = STEPS[(i + STEPS.length - 1) % STEPS.length];
    const k = ease.io(seg(lt, 0, 1.5)); const A = prev.cam, B = s.cam;
    const tg = lerp3(A[0], B[0], k); const pos = orbit(tg, lerp(A[1], B[1], k) * (w < 640 ? 1.35 : 1), lerp(A[2], B[2], k) + lt * 1.0, lerp(A[3], B[3], k));
    return { pos, tg };
  }
  function emit() { listeners.forEach(f => f({ step: curStep, id: STEPS[curStep]?.id, playing, manual, t: tourT, total: TOTAL })); }
  let lastEmit = 0;
  function tick(now) {
    requestAnimationFrame(tick);
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (!visible) return;
    if (playing) tourT = (tourT + dt) % TOTAL;
    simT += dt * rate * (manual ? 1 : STEPS[stepAt(tourT)[0]].slow);
    const [i, lt] = stepAt(tourT);
    if (i !== curStep || now - lastEmit > 200) { curStep = i; lastEmit = now; emit(); }
    const st = stepState(STEPS[i].id, lt, STEPS[i].dur, simT);
    if (ghost !== null) st.ghost = ghost;
    if (manual) { st.explode = 0; st.head = 1; st.fibre = 1; st.ghostU = 0; }
    stage.apply(st);
    if (!manual) {
      const c = camFromStep(i, lt); let pos = c.pos, tg = c.tg;
      if (blendFrom) { const k = ease.io(seg(now, blendFrom.t, blendFrom.t + 900)); pos = lerp3(blendFrom.pos, pos, k); tg = lerp3(blendFrom.tg, tg, k); if (k >= 1) blendFrom = null; }
      cam.position.set(...pos); controls.target.set(...tg); cam.lookAt(...tg);
    } else controls.update();
    stage.render();
    const want = manual ? [] : STEPS[i].labels;
    const fade = Math.min(seg(lt, 1.3, 1.8), 1 - seg(lt, STEPS[i].dur - 0.4, STEPS[i].dur));
    const used = new Set();
    for (const [anc, key, tone] of want) {
      const id = STEPS[i].id + anc; used.add(id);
      let el = labelEls[id];
      if (!el) { el = document.createElement('div'); el.className = 's3d-label' + (tone ? ' s3d-' + tone : ''); el.innerHTML = '<i></i><span></span>'; el.dataset.key = key; labelLayer.appendChild(el); labelEls[id] = el; }
      el.querySelector('span').textContent = txt('s3d_l_' + key);
      const p = stage.project(ANCHORS[anc], w, h);
      el.style.transform = `translate(${p[0].toFixed(1)}px, ${p[1].toFixed(1)}px)`;
      el.style.opacity = (p[2] < 1 ? fade : 0).toFixed(3);
      el.classList.toggle('s3d-left', p[0] > w * 0.6);
    }
    for (const [k, el] of Object.entries(labelEls)) if (!used.has(k)) el.style.opacity = 0;
  }
  requestAnimationFrame(tick);
  return {
    steps: STEPS.map(s => s.id), total: TOTAL,
    onChange(f) { listeners.push(f); },
    goTo(idx) { blendFrom = { pos: cam.position.toArray(), tg: controls.target.toArray(), t: performance.now() }; manual = false; playing = true; tourT = stepStart(idx) + 1.51; emit(); },
    play() { if (manual) blendFrom = { pos: cam.position.toArray(), tg: controls.target.toArray(), t: performance.now() }; manual = false; playing = true; emit(); },
    pause() { playing = false; emit(); },
    toggle() { (playing && !manual) ? this.pause() : this.play(); },
    setRate(v) { rate = v; },
    setGhost(v) { ghost = v ? 1 : null; },
  };
}
window.SAF3D = { mountViewer };
