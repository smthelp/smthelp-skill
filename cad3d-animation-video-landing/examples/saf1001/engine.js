// SAF1001 axial tape feeder — shared 3D stage (landing page + video renderer).
// Units mm, Y up. three x = CAD X - 350 (front/pick end at -350, tape tray at the rear +x), y = CAD Z + 160 (floor of locating pins = 0), z = 46 - CAD Y.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { loadModel } from './loader.js';
import EXTRA from './extra.json';

export const PITCH = 5.0;
export const PICK = [-282.45, 231.35, 0];        // formed part position at the pick point (CAD)
export const LEAD_Y = 231.35, LEAD_HALF = 28.5;  // lead centre height and half length (CAD)
export const ANCHORS = {
  pick: [-282.4, 236, 0], fibre: [-318, 231, 0], knife: [-290, 214, 9], cutcyl: [-285, 130, 30], formed: [-282.4, 228, 6],
  pawl: [-262, 232, 23], slider: [-215, 205, 40], feedcyl: [-160, 205, 10], stop: [-200, 182, 44], press: [-240, 247, 20],
  claw: [-266, 242, 18], guideblk: [-60, 228, 20], tray: [180, 175, -40], carton: [200, 222, 0], tape: [-200, 232, -28],
  tapeknife: [-312, 140, 30], tapecyl: [-160, 130, 20], chute: [60, 70, 34], valve: [-50, 130, 16], pcb: [-56, 202, 20],
  ebox: [-40, 222, 30], plug: [15, 200, 26], btn: [-35, 214, 44], switch: [-15, 212, 54], mount: [-200, 30, 46],
  pins: [-326, 5, 30], clamp: [-20, 30, 30], width: [-235, 185, 38], unload: [-330, 220, 46], front: [-345, 200, 0],
};

const EXPLODE = {
  tray: [190, 0, 0], carton: [190, 110, 0], hanger: [150, 0, 0], logo: [190, 0, 0], guideblk: [90, 70, 0],
  ebox: [40, 150, 0], pcb: [40, 110, 0], btn_g: [40, 150, 0], btn_r: [40, 150, 0], switch: [40, 150, 0], plug: [40, 150, 0],
  press: [0, 120, 0], claw: [0, 120, 0], slider: [0, 70, 0], pawls: [0, 70, 0], comps: [0, 160, 0], transport: [0, 35, 0], width: [0, 20, 0],
  feedcyl: [0, 70, 0], stop: [0, 55, 60], guide: [0, 15, 0],
  knife_fixed: [-70, 60, 0], knife_move: [-70, 20, 0], fibre: [-140, 60, 0], unload: [-110, 0, 0],
  cutcyl: [-70, -70, 0], tapeknife: [-40, -45, 0], tapecyl: [0, -70, 0], tube: [0, -90, 0], valve: [30, -100, 0], fitting: [30, -100, 0], silencers: [30, -100, 0],
  chute: [0, -150, 0], mount: [0, -170, 0], pins: [0, -200, 0], clamp: [0, -170, 0], springs: [0, -170, 0],
  side: [0, 0, 0], frame: [0, 0, 0], plate: [0, 0, 0],
};

function mat(o) { o = Object.assign({ side: THREE.DoubleSide }, o); return new THREE.MeshStandardMaterial(o); }

export async function createStage(canvas, opts = {}) {
  const geos = await loadModel(opts.modelB64);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: opts.aa !== false, alpha: true, preserveDrawingBuffer: !!opts.preserve, powerPreference: 'high-performance' });
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.62;
  const key = new THREE.DirectionalLight(0xffffff, 2.3); key.position.set(-600, 1200, 900); scene.add(key);
  const rim = new THREE.DirectionalLight(0x5ad7ff, 2.0); rim.position.set(900, 500, -1200); scene.add(rim);
  const fill = new THREE.DirectionalLight(0x9fffe9, 0.55); fill.position.set(-900, 200, -600); scene.add(fill);
  const camera = new THREE.PerspectiveCamera(30, 16 / 9, 5, 10000);

  const M = {
    alu: mat({ color: 0x9aa4b1, metalness: 0.9, roughness: 0.34 }),
    plate: mat({ color: 0x7f8996, metalness: 0.85, roughness: 0.32 }),
    anod: mat({ color: 0x1c2333, metalness: 0.55, roughness: 0.38 }),
    navy: mat({ color: 0x14203a, metalness: 0.35, roughness: 0.45 }),
    dark: mat({ color: 0x1b1f27, metalness: 0.5, roughness: 0.42 }),
    steel: mat({ color: 0xd2d8e0, metalness: 1, roughness: 0.22 }),
    cyl: mat({ color: 0xd5dbe3, metalness: 0.95, roughness: 0.26 }),
    teal: mat({ color: 0x00a896, metalness: 0.45, roughness: 0.35 }),
    tealB: mat({ color: 0x00c2ad, metalness: 0.3, roughness: 0.3, emissive: 0x003d36 }),
    amber: mat({ color: 0xf5b13d, metalness: 0.85, roughness: 0.28 }),
    kraft: mat({ color: 0xb08a5a, metalness: 0, roughness: 0.85, transparent: true, opacity: 0.55, depthWrite: false }),
    pcb: mat({ color: 0x0f6b3a, metalness: 0.2, roughness: 0.5 }),
    green: mat({ color: 0x22c55e, metalness: 0.2, roughness: 0.35, emissive: 0x0a3d1d }),
    red: mat({ color: 0xef4444, metalness: 0.2, roughness: 0.35, emissive: 0x3d0a0a }),
    blue: mat({ color: 0x2563eb, metalness: 0.3, roughness: 0.4 }),
    logo: mat({ color: 0xffffff, metalness: 0.1, roughness: 0.4, emissive: 0x335555 }),
    anod2: mat({ color: 0x2b3448, metalness: 0.6, roughness: 0.36 }),
    black: mat({ color: 0x0e1014, metalness: 0.2, roughness: 0.7 }),
  };
  const partMat = {
    plate: M.plate, side: M.anod, frame: M.anod, mount: M.alu, pins: M.steel, clamp: M.steel, transport: M.anod2, width: M.steel, guide: M.steel,
    slider: M.plate, feedcyl: M.cyl, stop: M.amber, press: M.alu, claw: M.steel, unload: M.alu, fibre: M.black,
    knife_fixed: M.steel, knife_move: M.teal, cutcyl: M.cyl, tapeknife: M.steel, tapecyl: M.cyl, valve: M.dark, fitting: M.blue,
    ebox: M.navy, pcb: M.pcb, btn_g: M.green, btn_r: M.red, switch: M.dark, plug: M.amber, guideblk: M.alu, tray: M.teal, carton: M.kraft,
    hanger: M.steel, chute: M.alu, tube: M.steel, logo: M.logo, misc: M.alu,
  };
  const ghostable = new Set(['side', 'frame', 'ebox', 'tray', 'logo']);

  const root = new THREE.Group(); scene.add(root);
  const meshes = {}; const base = {};
  const pawlG = new THREE.Group(); root.add(pawlG); meshes.pawls = pawlG; base.pawls = new THREE.Vector3();
  const pawls = [];
  for (const [name, o] of Object.entries(geos)) {
    if (name.startsWith('pawl_')) { // each index pawl rotates about its own pivot screw
      o.geo.computeBoundingBox(); const bb = o.geo.boundingBox; const pv = new THREE.Vector3(bb.max.x - 4, 222.3, (bb.min.z + bb.max.z) / 2);
      const g = new THREE.Group(); g.position.copy(pv); const m = new THREE.Mesh(o.geo, M.amber); m.position.copy(pv).negate(); m.name = name; g.add(m); pawlG.add(g); pawls.push(g); continue; }
    const m = new THREE.Mesh(o.geo, partMat[name] || M.alu); m.name = name; base[name] = m.position.clone(); root.add(m); meshes[name] = m;
  }
  // procedural springs (spring press block) and silencers
  const sprG = new THREE.Group(); root.add(sprG); meshes.springs = sprG; base.springs = new THREE.Vector3();
  for (const [lo, hi] of EXTRA.springs) {
    const c = [(lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2], r = (hi[1] - lo[1]) / 2 - 0.6, L = hi[0] - lo[0];
    const pts = []; for (let i = 0; i <= 160; i++) { const a = i / 160 * Math.PI * 2 * 7; pts.push(new THREE.Vector3(lo[0] + L * i / 160, c[0] + r * Math.cos(a), c[1] + r * Math.sin(a))); }
    sprG.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 320, 0.6, 6), M.steel));
  }
  const silG = new THREE.Group(); root.add(silG); meshes.silencers = silG; base.silencers = new THREE.Vector3();
  for (const [lo, hi] of EXTRA.silencers) { const g = new THREE.CylinderGeometry(3.6, 4.2, hi[2] - lo[2], 16); g.rotateX(Math.PI / 2); const m = new THREE.Mesh(g, M.dark); m.position.set((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2); silG.add(m); }

  // ---------- taped components (axial resistors, from CAD positions) ----------
  const compG = new THREE.Group(); root.add(compG); meshes.comps = compG; base.comps = new THREE.Vector3();
  const bodyGeo = new THREE.CylinderGeometry(1.15, 1.15, 6.4, 20); bodyGeo.rotateX(Math.PI / 2);
  const capGeo = new THREE.CylinderGeometry(1.25, 1.25, 1.2, 20); capGeo.rotateX(Math.PI / 2);
  const leadGeo = new THREE.CylinderGeometry(0.28, 0.28, LEAD_HALF * 2, 6); leadGeo.rotateX(Math.PI / 2);
  const bodyM = mat({ color: 0x5aa0d8, metalness: 0.1, roughness: 0.45 }), bandM = mat({ color: 0xc8a24a, metalness: 0.4, roughness: 0.4 }), leadM = mat({ color: 0xdfe5ec, metalness: 1, roughness: 0.25 });
  const mkComp = (formed) => {
    const g = new THREE.Group(); g.add(new THREE.Mesh(bodyGeo, bodyM));
    for (const z of [-2.2, -0.9, 0.6, 2.4]) { const b = new THREE.Mesh(capGeo, bandM); b.scale.set(1, 1, 0.35); b.position.z = z; g.add(b); }
    if (!formed) g.add(new THREE.Mesh(leadGeo, leadM));
    else { const h = new THREE.CylinderGeometry(0.28, 0.28, 2.0, 6); h.rotateX(Math.PI / 2); for (const s of [-1, 1]) { const a = new THREE.Mesh(h, leadM); a.position.z = s * 4.2; g.add(a); const v = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 5, 6), leadM); v.position.set(0, -2.5, s * 5.2); g.add(v); } }
    return g; };
  const NC = 34; const comps = [];
  for (let k = 0; k < NC; k++) { const c = mkComp(false); c.userData.k = k; compG.add(c); comps.push(c); }
  const formed = mkComp(true); compG.add(formed);
  // paper tape strips (both sides) with the front turn-down into the unload guide
  const tapeM = mat({ color: 0xf2efe6, metalness: 0, roughness: 0.9 });
  const tapePts = []; for (let i = 0; i <= 20; i++) tapePts.push(new THREE.Vector3(-110 - i * 8.8, LEAD_Y - 0.4, 0));
  for (let i = 1; i <= 12; i++) { const a = i / 12 * Math.PI / 2; tapePts.push(new THREE.Vector3(-286 - 22 * Math.sin(a), LEAD_Y - 0.4 - 22 * (1 - Math.cos(a)), 0)); }
  for (let i = 1; i <= 6; i++) tapePts.push(new THREE.Vector3(-308, LEAD_Y - 22.4 - i * 8, 0));
  for (const zc of [29, -29]) {
    const pos = [], idx = []; tapePts.forEach((p, i) => { pos.push(p.x, p.y, zc - 3, p.x, p.y, zc + 3); if (i) { const k = (i - 1) * 2; idx.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); } });
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals(); compG.add(new THREE.Mesh(g, tapeM));
  }
  // waste tape chips sliding down the chute
  const chips = []; for (let i = 0; i < 6; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(5, 0.4, 6), tapeM); root.add(m); chips.push(m); }

  // ---------- effects ----------
  const fx = new THREE.Group(); root.add(fx);
  const addMat = (c, o = 0.6) => new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: o, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
  const beamG = new THREE.CylinderGeometry(0.9, 0.9, 3.5, 10); beamG.rotateZ(Math.PI / 2);
  const beam = new THREE.Mesh(beamG, addMat(0xff3b30, 0)); beam.position.set(-286.2, LEAD_Y, 0); fx.add(beam);
  const beamDot = new THREE.Mesh(new THREE.SphereGeometry(2.6, 16, 12), addMat(0xff3b30, 0)); beamDot.position.set(-285, LEAD_Y, 0); fx.add(beamDot);
  const airM = addMat(0x7fe7ff, 0); const airRings = []; for (let i = 0; i < 3; i++) { const r = new THREE.Mesh(new THREE.TorusGeometry(12, 0.6, 6, 40), airM.clone()); r.rotation.y = Math.PI / 2; fx.add(r); airRings.push(r); }
  // illustrative insertion head
  const head = new THREE.Group(); fx.add(head);
  { const b = new THREE.Mesh(new THREE.CylinderGeometry(5, 5, 50, 24), M.steel); b.position.y = 31; head.add(b);
    for (const s of [-1, 1]) { const f = new THREE.Mesh(new THREE.BoxGeometry(3, 8, 1.6), M.amber); f.position.set(0, 3, s * 3.0); head.add(f); }
    const c = new THREE.Mesh(new THREE.BoxGeometry(8, 3, 9), M.amber); c.position.y = 6.5; head.add(c); }
  head.visible = false;

  const state = { explode: 0, ghost: 0, ghostU: 0, time: 0, cycT: 0, period: 0.8, run: 1, head: 0, fibre: 0.6, air: 0, chips: 0, highlight: {}, compsVisible: true };
  const hl = new THREE.Color(0x00e0c4);
  const sm = THREE.MathUtils.smoothstep;
  function apply(s) {
    Object.assign(state, s || {});
    const e = THREE.MathUtils.smootherstep(state.explode, 0, 1);
    for (const [n, m] of Object.entries(meshes)) { const off = EXPLODE[n] || [0, 0, 0]; m.position.set(base[n].x + off[0] * e, base[n].y + off[1] * e, base[n].z + off[2] * e); }
    // ----- feed cycle (phase in [0,1)) -----
    const run = state.run; const cyc = state.cycT / state.period; const ph = run > 0 ? cyc - Math.floor(cyc) : 0.95;
    const feed = run > 0 ? sm(ph, 0.02, 0.24) : 1;                 // tape advance (slide forward)
    const ret = run > 0 ? sm(ph, 0.66, 0.9) : 1;                   // slide return
    const slide = -PITCH * (feed - ret);
    const tilt = run > 0 ? Math.sin(Math.PI * sm(ph, 0.64, 0.92)) : 0;
    meshes.slider.position.x += slide; pawlG.position.x += slide;
    pawls.forEach(g => { g.rotation.z = -0.13 * tilt; });
    const kup = run > 0 ? sm(ph, 0.26, 0.38) * (1 - sm(ph, 0.6, 0.72)) : 1;   // moving knife: up = trim + form
    meshes.knife_move.position.y += -9 * (1 - kup);
    const tcut = run > 0 ? Math.sin(Math.PI * sm(ph, 0.4, 0.62)) : 0;      // paper-tape knife
    meshes.tapeknife.position.x += -11 * tcut;
    // components: the row steps one pitch per cycle (relabelled at the wrap so the strip is endless)
    const showC = state.compsVisible && e < 0.02; compG.visible = state.compsVisible;
    const cut = run > 0 ? ph > 0.33 : true;
    const shiftC = run > 0 ? -PITCH * feed : 0;
    const ex = EXPLODE.comps, ce = [ex[0] * e, ex[1] * e, ex[2] * e];
    comps.forEach((c, k) => {
      const x = PICK[0] + (k + (run > 0 ? 1 : 0)) * PITCH + shiftC; // k=0 is the next part to arrive at the pick point
      c.position.set(x + ce[0], LEAD_Y + ce[1], ce[2]);
      const atPick = Math.abs(x - PICK[0]) < 0.5;
      c.visible = !(atPick && cut) && x < -118 && x > PICK[0] - 0.5;
      const fade = THREE.MathUtils.clamp((-118 - x) / 14, 0, 1); c.scale.setScalar(0.4 + 0.6 * fade);
    });
    // formed part: appears at the cut, leaves with the head
    const pickUp = run > 0 ? sm(ph, 0.52, 0.66) : 0, headDown = run > 0 ? sm(ph, 0.3, 0.46) : 0;
    formed.visible = (run > 0 ? cut : true) && pickUp < 0.98;
    formed.position.set(PICK[0] + ce[0], LEAD_Y - 0.6 + 80 * pickUp + ce[1], ce[2]);
    head.visible = state.head > 0.01 && showC;
    head.position.set(PICK[0], LEAD_Y + 2 + 80 * (1 - headDown) + 80 * pickUp, 0);
    // fibre: red when the part is present at the pick point
    const present = run > 0 ? (ph > 0.24 && ph < 0.55) : true;
    const fb = state.fibre * (present ? 1 : 0.12) * (showC ? 1 : 0);
    beam.material.opacity = 0.9 * fb; beamDot.material.opacity = 0.9 * fb;
    // air pulse on the feed cylinder
    airRings.forEach((r, i) => { const p = ((ph + i / 3) % 1); r.position.set(-130 + 30 * p, 198, 0); r.scale.setScalar(0.6 + p); r.material.opacity = state.air * 0.5 * (1 - p) * (1 - e); });
    // waste chips
    chips.forEach((m, i) => { const u = ((state.time * 0.35 + i / chips.length) % 1); m.visible = state.chips > 0.01 && e < 0.02;
      const a = new THREE.Vector3(-322, 112, 0), b = new THREE.Vector3(-300, 92, 0), c = new THREE.Vector3(150, 48, 0);
      if (u < 0.2) m.position.lerpVectors(a, b, u / 0.2); else m.position.lerpVectors(b, c, (u - 0.2) / 0.8); m.position.z = ((i * 37) % 40) - 20; m.rotation.set(i, u * 3, i * 0.5); });
    // ghost
    const g = state.ghost;
    for (const n of ghostable) { const m = meshes[n]; if (!m) continue;
      if (g > 0.001) { if (!m.userData.gm) { m.userData.bm = m.material; m.userData.gm = m.material.clone(); m.userData.gm.transparent = true; m.userData.gm.depthWrite = false; } m.material = m.userData.gm; m.material.opacity = (n === 'tray' || n === 'logo' ? 1 - 0.6 * g : 1 - 0.86 * g); }
      else if (m.userData.bm) m.material = m.userData.bm; }
    { const m = meshes.unload, gu = state.ghostU;
      if (gu > 0.001) { if (!m.userData.gm) { m.userData.bm = m.material; m.userData.gm = m.material.clone(); m.userData.gm.transparent = true; m.userData.gm.depthWrite = false; } m.material = m.userData.gm; m.material.opacity = 1 - 0.85 * gu; }
      else if (m.userData.bm) m.material = m.userData.bm; }
    // highlights
    const all = { ...meshes }; pawls.forEach((p, i) => { all['pawl' + i] = p.children[0]; });
    for (const [n, m] of Object.entries(all)) {
      const k = (n.startsWith('pawl') ? state.highlight.pawls : state.highlight[n]) || 0; if (!m.isMesh) continue;
      if (k > 0) { if (!m.userData.hlMat) { m.userData.baseMat0 = m.material; m.userData.hlMat = m.material.clone(); } m.material = m.userData.hlMat; m.material.emissive = new THREE.Color().copy(hl).multiplyScalar(0.45 * k); }
      else if (m.userData.baseMat0 && m.material === m.userData.hlMat) m.material = m.userData.baseMat0;
    }
    return ph;
  }
  apply();
  const _v = new THREE.Vector3();
  function project(anchor, w, h) { _v.set(...anchor); _v.project(camera); return [(_v.x * 0.5 + 0.5) * w, (-_v.y * 0.5 + 0.5) * h, _v.z]; }
  function setCamera(pos, target, fovDeg, w, h, shiftX = 0, shiftY = 0) {
    camera.fov = fovDeg; camera.aspect = w / h; camera.position.set(...pos); camera.up.set(0, 1, 0); camera.lookAt(new THREE.Vector3(...target));
    if (shiftX || shiftY) camera.setViewOffset(w, h, -shiftX * w, -shiftY * h, w, h); else camera.clearViewOffset();
    camera.updateProjectionMatrix();
  }
  function setSize(w, h, pr = 1) { renderer.setPixelRatio(pr); renderer.setSize(w, h, false); }
  function render() { renderer.render(scene, camera); }
  return { THREE, renderer, scene, camera, root, meshes, state, apply, render, setCamera, setSize, project, head };
}

export const ease = {
  io: t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
  out: t => 1 - Math.pow(1 - t, 3), in: t => t * t * t, smooth: t => t * t * (3 - 2 * t),
};
export function clamp01(x) { return Math.max(0, Math.min(1, x)); }
export function seg(t, a, b) { return clamp01((t - a) / (b - a)); }
export function lerp(a, b, t) { return a + (b - a) * t; }
export function lerp3(a, b, t) { return [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)]; }
export function orbit(target, dist, azDeg, elDeg) {
  const az = azDeg * Math.PI / 180, el = elDeg * Math.PI / 180;
  return [target[0] + dist * Math.cos(el) * Math.sin(az), target[1] + dist * Math.sin(el), target[2] + dist * Math.cos(el) * Math.cos(az)];
}
