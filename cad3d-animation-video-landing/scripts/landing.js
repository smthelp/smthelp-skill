// Interactive CN-SM-2713 mechanism viewer for the landing page
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { createStage, ease, seg, lerp, lerp3, orbit, clamp01, ANCHORS } from './engine.js';

const STEPS = [
  { id: 'overview', dur: 6, cam: [[0, -14, 0], 128, 30, 14], labels: [['shank', 'JUKI-standard shank'], ['padR', 'Contact pins', 'amber'], ['coil', 'Ø8.5 mm coil']] },
  { id: 'shank', dur: 6, cam: [[0, 1, 0], 92, 30, 18], labels: [['shank', 'JUKI-standard nozzle shank']] },
  { id: 'mech', dur: 9, cam: [[0, -13, 0], 120, 2, 3], labels: [['plunger', 'Plunger'], ['spring', 'Return spring'], ['pinC', 'Center pin', '', 'l'], ['pivotR', 'Pivot pin']] },
  { id: 'grip', dur: 7, cam: [[0, -25.3, 0], 62, 25, -72], fov: 30, labels: [['padL1', '2 pins', 'amber'], ['padR', '1 pin', 'amber']] },
  { id: 'stop', dur: 7, cam: [[0, -21, 0], 100, 75, 6], labels: [['stop', 'Center stop pin · Z datum', 'amber'], ['leads', 'Leads hang free']] },
  { id: 'explode', dur: 7, cam: [[0, -8, 0], 215, 28, 16], labels: [['clipL', 'E-clip retained pins']] },
  { id: 'cycle', dur: 10, cam: [[0, -22, 0], 245, 8, 20], labels: [] },
];
const TOTAL = STEPS.reduce((a, s) => a + s.dur, 0);

function stepState(id, lt, D) {
  const st = { open: 0, explode: 0, cut: 0, highlight: {}, rigPos: [0, 0, 0], coilPos: [0, 0, 0], coilAttached: true, props: false, rigRotY: 0, yClip: 0 };
  const pulse = 0.6 + 0.4 * Math.sin(lt * 5);
  if (id === 'overview') { st.rigRotY = lerp(-0.4, 0.4, ease.io(seg(lt, 0, D))); st.open = Math.sin(Math.PI * seg(lt, 2.5, 3.6)); }
  if (id === 'shank') st.highlight = { nozzle: 0.7 * pulse * seg(lt, 0.3, 1) * (1 - seg(lt, D - 0.6, D)) };
  if (id === 'mech') {
    st.cut = ease.io(seg(lt, 0, 1.2)) * (1 - ease.io(seg(lt, D - 0.8, D)));
    const c = (lt - 1.6) % 3.4; st.open = lt > 1.6 ? (c < 1.0 ? ease.io(c / 1.0) : c < 1.9 ? 1 : 1 - ease.out(Math.min(1, (c - 1.9) / 0.3))) : 0;
    st.highlight = { plunger: 0.6, pin_inner: 0.6, pinC: 0.8, spring: 0.4 };
  }
  if (id === 'grip') {
    st.open = 1 - ease.out(seg(lt, 1.6, 2.0)); st.open = Math.min(st.open, ease.io(seg(lt, 0, 0.6)));
    st.yClip = ease.io(seg(lt, 0.4, 1.3)) * (1 - ease.io(seg(lt, D - 0.8, D)));
    const p = seg(lt, 1.8, 2.4) * pulse; st.highlight = { padL1: p, padL2: p, padR: p };
  }
  if (id === 'stop') { st.highlight = { stop: pulse, coil_leads: 0.6 * pulse * seg(lt, 3, 3.6), lead_ext: 0.6 * pulse * seg(lt, 3, 3.6) }; }
  if (id === 'explode') { st.explode = ease.io(seg(lt, 0.3, 2.3)) * (1 - ease.io(seg(lt, D - 2, D - 0.2))); st.rigRotY = lerp(0, 0.8, ease.io(seg(lt, 0, D))); }
  if (id === 'cycle') {
    st.props = true; st.coilAttached = false;
    const up = 22, tray = [-30, -6, 0], pcb = [30, -9, 0]; const a = (x, y) => seg(lt, x, y);
    let pos = lerp3([-30, up, 0], tray, ease.io(a(0.8, 2.2))), open = ease.io(a(0.2, 0.8)), att = false, cp = tray;
    if (lt > 2.4) open = 1 - ease.out(a(2.4, 2.8));
    if (lt > 2.9) { att = true; pos = lerp3(tray, [-30, up, 0], ease.io(a(2.9, 3.9))); }
    if (lt > 3.9) pos = lerp3([-30, up, 0], [30, up, 0], ease.io(a(3.9, 5.3)));
    if (lt > 5.3) pos = lerp3([30, up, 0], pcb, ease.io(a(5.3, 6.5)));
    if (lt > 6.6) { att = false; cp = pcb; open = ease.out(a(6.6, 6.9)); pos = pcb; }
    if (lt > 7.0) { pos = lerp3(pcb, [30, up, 0], ease.io(a(7.0, 8.2))); open = 1 - ease.io(a(8.0, 8.6)); }
    st.rigPos = pos; st.open = open; st.coilAttached = att; st.coilPos = att ? pos : cp;
  }
  return st;
}

export async function mountViewer(opts) {
  const host = opts.host; const canvas = host.querySelector('canvas');
  const stage = await createStage(canvas, { modelB64: opts.model });
  const cam = stage.camera;
  const controls = new OrbitControls(cam, canvas);
  controls.enableDamping = true; controls.enablePan = false; controls.minDistance = 45; controls.maxDistance = 320; controls.target.set(0, -11, 0);
  const yPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 60);
  const labelLayer = host.querySelector('[data-labels]');
  const labelEls = {};
  let w = 0, h = 0;
  function resize() {
    const r = host.getBoundingClientRect(); w = Math.max(10, r.width); h = Math.max(10, r.height);
    stage.setSize(w, h, Math.min(window.devicePixelRatio || 1, 1.75)); cam.aspect = w / h; cam.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(host); resize();

  let tourT = 0, playing = true, manual = false, manualOpen = null, visible = true, last = performance.now();
  let blendFrom = null; // camera blend when resuming / jumping
  const listeners = [];
  function stepAt(t) { let a = 0; for (let i = 0; i < STEPS.length; i++) { if (t < a + STEPS[i].dur) return [i, t - a]; a += STEPS[i].dur; } return [STEPS.length - 1, STEPS[STEPS.length - 1].dur]; }
  function stepStart(i) { let a = 0; for (let k = 0; k < i; k++) a += STEPS[k].dur; return a; }
  let curStep = -1;

  controls.addEventListener('start', () => { manual = true; playing = false; emit(); });
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(host);

  function camFromStep(i, lt) {
    const s = STEPS[i]; const prev = STEPS[(i + STEPS.length - 1) % STEPS.length];
    const k = ease.io(seg(lt, 0, 1.3));
    const A = prev.cam, B = s.cam;
    const tg = lerp3(A[0], B[0], k); const pos = orbit(tg, lerp(A[1], B[1], k), lerp(A[2], B[2], k) + lt * 1.2, lerp(A[3], B[3], k));
    return { pos, tg, fov: lerp(prev.fov || 28, s.fov || 28, k) };
  }
  function emit() { listeners.forEach(f => f({ step: curStep, id: STEPS[curStep]?.id, playing, manual })); }

  function tick(now) {
    requestAnimationFrame(tick);
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (!visible) return;
    if (playing) tourT = (tourT + dt) % TOTAL;
    const [i, lt] = stepAt(tourT);
    if (i !== curStep) { curStep = i; emit(); }
    const st = stepState(STEPS[i].id, lt, STEPS[i].dur);
    if (manualOpen !== null) st.open = manualOpen;
    stage.renderer.clippingPlanes = st.yClip > 0.001 ? [yPlane] : [];
    yPlane.constant = lerp(60, 25.3, st.yClip);
    stage.apply(st);
    if (!manual) {
      const c = camFromStep(i, lt);
      let pos = c.pos, tg = c.tg;
      if (blendFrom) { const k = ease.io(seg(now, blendFrom.t, blendFrom.t + 900)); pos = lerp3(blendFrom.pos, pos, k); tg = lerp3(blendFrom.tg, tg, k); if (k >= 1) blendFrom = null; }
      cam.position.set(...pos); cam.fov = c.fov; cam.updateProjectionMatrix(); controls.target.set(...tg); cam.lookAt(...tg);
    } else controls.update();
    stage.render();
    // labels
    const want = manual ? [] : STEPS[i].labels;
    const fade = Math.min(seg(lt, 1.1, 1.6), 1 - seg(lt, STEPS[i].dur - 0.4, STEPS[i].dur));
    const used = new Set();
    for (const [anc, text, tone, side] of want) {
      const key = STEPS[i].id + anc; used.add(key);
      let el = labelEls[key];
      if (!el) { el = document.createElement('div'); el.className = 'cn-label' + (tone === 'amber' ? ' cn-amber' : ''); el.innerHTML = '<i></i><span></span>'; el.querySelector('span').textContent = text; labelLayer.appendChild(el); labelEls[key] = el; }
      const p = stage.project(ANCHORS[anc], w, h);
      el.style.transform = `translate(${p[0].toFixed(1)}px, ${p[1].toFixed(1)}px)`;
      el.style.opacity = (p[2] < 1 ? fade : 0).toFixed(3);
      el.classList.toggle('cn-left', side === 'l' || p[0] > w * 0.62);
    }
    for (const [k, el] of Object.entries(labelEls)) if (!used.has(k)) el.style.opacity = 0;
  }
  requestAnimationFrame(tick);

  return {
    steps: STEPS.map(s => s.id),
    onChange(f) { listeners.push(f); },
    goTo(idx) { blendFrom = { pos: cam.position.toArray(), tg: controls.target.toArray(), t: performance.now() }; manual = false; playing = true; tourT = stepStart(idx) + 1.31; emit(); },
    play() { if (manual) blendFrom = { pos: cam.position.toArray(), tg: controls.target.toArray(), t: performance.now() }; manual = false; playing = true; manualOpen = null; emit(); },
    pause() { playing = false; emit(); },
    toggle() { (playing && !manual) ? this.pause() : this.play(); },
    setOpen(v) { manualOpen = v; },
    releaseOpen() { manualOpen = null; },
  };
}
window.CNSM2713 = { mountViewer };
