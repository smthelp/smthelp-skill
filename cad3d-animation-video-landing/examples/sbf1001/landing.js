// Interactive SBF1001 bowl feeder viewer for the landing page
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { createStage, ease, seg, lerp, lerp3, orbit, ANCHORS } from './engine.js';

const STEPS = [
  { id: 'overview', dur: 7, cam: [[0, 600, 180], 3100, -140, 16], labels: [['bowl', 'bowl'], ['rail', 'rail'], ['station', 'station'], ['camera', 'camera', 'sky'], ['hmi', 'hmi']] },
  { id: 'drive', dur: 7, cam: [[5, 770, -14], 1350, -108, 10], labels: [['drive', 'drive'], ['bowl', 'bowl']] },
  { id: 'sort', dur: 8, cam: [[5, 860, -14], 860, -140, 50], labels: [['helix', 'helix']] },
  { id: 'rail', dur: 8, cam: [[-120, 870, 390], 1150, -55, 20], labels: [['lindrive', 'lindrive'], ['rail', 'rail'], ['air', 'air', 'sky']] },
  { id: 'pick', dur: 8, cam: [[-118, 892, 600], 560, -55, 24], labels: [['fibre', 'fibre', 'red'], ['station', 'station']] },
  { id: 'platform', dur: 9, cam: [[0, 520, 60], 2600, -150, 12], labels: [['rubber', 'rubber'], ['stud', 'stud'], ['ebox', 'ebox'], ['caster', 'caster']] },
  { id: 'explode', dur: 8, cam: [[0, 760, 160], 4100, -132, 15], labels: [] },
];
ANCHORS.air = [-120, 905, 520];
const TOTAL = STEPS.reduce((a, s) => a + s.dur, 0);

function stepState(id, lt, D, t) {
  const st = { explode: 0, ghost: 0, vib: 1, flowT: t, flow: 1, air: 0, fibre: 0.6, vision: 0.2, helix: 1, highlight: {}, reject: 0, rejT: t, head: 0, time: t, partsVisible: true, railFull: 1 };
  const pulse = 0.6 + 0.4 * Math.sin(lt * 5);
  if (id === 'overview') { st.vision = 0.6; }
  if (id === 'drive') st.highlight = { drive: 0.8 * pulse * seg(lt, 0.4, 1) * (1 - seg(lt, D - 0.6, D)) };
  if (id === 'sort') st.reject = seg(lt, 1, 1.6);
  if (id === 'rail') { st.air = seg(lt, 0.8, 1.4); st.highlight = { lindrive: 0.6 * pulse * seg(lt, 0.6, 1.2) * (1 - seg(lt, 3.5, 4)) }; }
  if (id === 'pick') { st.head = 1; st.fibre = 1; st.highlight = { station: 0.35 * pulse }; }
  if (id === 'platform') { st.ghost = seg(lt, 1.5, 2.3) * (1 - seg(lt, D - 1, D - 0.3)); st.highlight = { ebox: st.ghost * pulse, rubber: pulse * 0.6 * (1 - seg(lt, 1.5, 2)) }; }
  if (id === 'explode') { st.explode = ease.io(seg(lt, 0.3, 2.3)) * (1 - ease.io(seg(lt, D - 2, D - 0.2))); st.vib = 1 - st.explode; }
  return st;
}

export async function mountViewer(opts) {
  const host = opts.host; const canvas = host.querySelector('canvas');
  const stage = await createStage(canvas, { modelB64: opts.model });
  const cam = stage.camera; cam.near = 20; cam.far = 20000;
  const controls = new OrbitControls(cam, canvas);
  controls.enableDamping = true; controls.enablePan = false; controls.minDistance = 350; controls.maxDistance = 6000; controls.target.set(0, 600, 100);
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
    simT += dt * rate;
    const [i, lt] = stepAt(tourT);
    if (i !== curStep || now - lastEmit > 200) { curStep = i; lastEmit = now; emit(); }
    const st = stepState(STEPS[i].id, lt, STEPS[i].dur, simT);
    st.vib *= Math.min(1, 0.35 + rate * 0.65);
    if (ghost !== null) st.ghost = ghost;
    if (manual) { st.explode = 0; st.head = 1; st.fibre = 1; st.air = 1; st.reject = 1; }
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
window.SBF3D = { mountViewer };
