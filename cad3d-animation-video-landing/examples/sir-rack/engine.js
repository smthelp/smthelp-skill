// SMT Intelligent Reel Storage Rack (5 layer) — shared 3D stage (landing page + video renderer).
// Units mm, Y up. three x = CAD Z - 595 (rack length), y = CAD Y + 401 (floor = 0), z = CAD X + 1176 (depth, front = +z).
// Real CAD: end panels, 10 rails, feet, one 13" reel. Wire dividers are rebuilt at their exact CAD positions as instanced tubes.
// Illustrative (not in CAD): per-slot LEDs, slot light glow, top stack lights, PDA scanner, fleet of stored reels.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { loadModel } from './loader.js';
import EXTRA from './extra.json';

export const NL = 5, NK = 100, PITCH = 24;
export const RAIL_TOP = [154.8, 534.8, 914.8, 1294.8, 1674.8];
export const REEL_DY = 104, REEL_R = 165, REEL_T = 14;
export const HERO = { L: 3, k: 29 };
export const slotX = k => EXTRA.layers[0].xs[0] + 1.5 + PITCH / 2 + PITCH * k;
export const slotY = L => RAIL_TOP[L] + REEL_DY;
export const FRONT_Z = 196;
export const ANCHORS = {
  panelL: [-1205, 1300, 200], panelR: [1205, 1300, 200], rail: [700, 1277, 196], divider: [300, 1340, 160], foot: [-1205, 50, 170],
  topL: [-1205, 2010, 0], topR: [1205, 2010, 0], hero: [slotX(HERO.k), slotY(HERO.L), 0], heroLed: [slotX(HERO.k), 1277, 200],
};
// deterministic fill (~62 %), hero slot empty
function rnd(i) { let x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
export const FILL = new Float32Array(NL * NK).map((_, i) => (rnd(i) < 0.62 ? 1 : 0));
FILL[HERO.L * NK + HERO.k] = 0;
const REEL_COLS = [0x1d4ed8, 0x0b0f17, 0x0b0f17, 0xe5e7eb, 0x1d4ed8, 0x0b0f17, 0x2563eb, 0xd1d5db];

function mat(o) { o = Object.assign({ side: THREE.DoubleSide }, o); return new THREE.MeshStandardMaterial(o); }

function reelFaceTex() {
  const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
  g.fillStyle = '#e8e8e8'; g.beginPath(); g.arc(128, 128, 127, 0, 7); g.fill();
  g.fillStyle = '#9a9a9a'; for (let i = 0; i < 3; i++) { const a = i * 2.094 + 0.5; g.beginPath(); g.moveTo(128 + 40 * Math.cos(a - 0.5), 128 + 40 * Math.sin(a - 0.5)); g.arc(128, 128, 112, a - 0.62, a + 0.62); g.arc(128, 128, 40, a + 0.5, a - 0.5, true); g.fill(); }
  g.fillStyle = '#fff'; g.beginPath(); g.arc(128, 128, 36, 0, 7); g.fill(); g.fillStyle = '#555'; g.beginPath(); g.arc(128, 128, 9, 0, 7); g.fill();
  g.fillStyle = '#ffffff'; g.fillRect(150, 150, 70, 34); g.fillStyle = '#222'; for (let i = 0; i < 18; i++) g.fillRect(155 + i * 3.4, 154, i % 3 ? 1.4 : 2.4, 18);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
function glowTex() {
  const c = document.createElement('canvas'); c.width = 32; c.height = 256; const g = c.getContext('2d');
  const gr = g.createLinearGradient(0, 256, 0, 0); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.25, 'rgba(255,255,255,0.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 32, 256);
  const h = g.createLinearGradient(0, 0, 32, 0); h.addColorStop(0, 'rgba(0,0,0,1)'); h.addColorStop(0.3, 'rgba(0,0,0,0)'); h.addColorStop(0.7, 'rgba(0,0,0,0)'); h.addColorStop(1, 'rgba(0,0,0,1)');
  g.globalCompositeOperation = 'destination-out'; g.fillStyle = h; g.fillRect(0, 0, 32, 256);
  return new THREE.CanvasTexture(c);
}
function dotTex() {
  const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d');
  const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.35, 'rgba(255,255,255,0.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c);
}

export async function createStage(canvas, opts = {}) {
  const geos = await loadModel(opts.modelB64);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: opts.aa !== false, alpha: true, preserveDrawingBuffer: !!opts.preserve, powerPreference: 'high-performance' });
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.6;
  const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(-2500, 4000, 4000); scene.add(key);
  const rim = new THREE.DirectionalLight(0x5ad7ff, 1.6); rim.position.set(3000, 2000, -4000); scene.add(rim);
  const fill = new THREE.DirectionalLight(0x9fffe9, 0.5); fill.position.set(-3000, 800, -2000); scene.add(fill);
  const camera = new THREE.PerspectiveCamera(30, 16 / 9, 20, 40000);

  const M = {
    panel: mat({ color: 0x1a2440, metalness: 0.45, roughness: 0.42 }),
    rail: mat({ color: 0xa9b3c3, metalness: 0.9, roughness: 0.32 }),
    wire: mat({ color: 0xdfe5ec, metalness: 1, roughness: 0.22 }),
    foot: mat({ color: 0x8a94a3, metalness: 0.85, roughness: 0.35 }),
    dark: mat({ color: 0x151a22, metalness: 0.4, roughness: 0.5 }),
    heroReel: mat({ color: 0x2563eb, metalness: 0.15, roughness: 0.35 }),
  };
  const root = new THREE.Group(); scene.add(root);
  const meshes = {}; const base = {};
  const layerG = []; for (let L = 0; L < NL; L++) { const g = new THREE.Group(); root.add(g); layerG.push(g); }
  for (const [name, o] of Object.entries(geos)) {
    if (name === 'reel') continue;
    const m = new THREE.Mesh(o.geo, name.startsWith('panel') ? M.panel : name === 'foot' ? M.foot : name.startsWith('rail') ? M.rail : M.rail); m.name = name;
    if (name.startsWith('rail')) layerG[+name[4]].add(m); else root.add(m);
    meshes[name] = m; base[name] = m.position.clone();
  }
  // hero reel (real CAD mesh), recentred on its own axis
  const heroG = new THREE.Group(); root.add(heroG);
  { const o = geos.reel; const c = [(o.bmin[0] + o.bmax[0]) / 2, (o.bmin[1] + o.bmax[1]) / 2, (o.bmin[2] + o.bmax[2]) / 2];
    const m = new THREE.Mesh(o.geo, M.heroReel); m.position.set(-c[0], -c[1], -c[2]); heroG.add(m); }
  // label on the hero reel face (barcode), faces +x
  const labTex = (() => { const c = document.createElement('canvas'); c.width = 256; c.height = 128; const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, 256, 128);
    g.fillStyle = '#111'; for (let i = 0; i < 46; i++) g.fillRect(14 + i * 4.9, 14, (i * 7) % 3 ? 1.6 : 3.2, 62); g.font = 'bold 22px monospace'; g.fillText('PN 0402-10K  Q 10000', 14, 104); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  for (const s of [1, -1]) { const lab = new THREE.Mesh(new THREE.PlaneGeometry(90, 45), new THREE.MeshStandardMaterial({ map: labTex, roughness: 0.6 })); lab.position.set(s * 7.6, -60, 40); lab.rotation.y = s * Math.PI / 2; heroG.add(lab); }

  // U-wire dividers at exact CAD x positions (layers × 101)
  const DH = EXTRA.divh, Z0 = EXTRA.divz[0] + 1.5, Z1 = EXTRA.divz[1] - 1.5, R = 10;
  const pts = [new THREE.Vector3(0, 0, Z0), new THREE.Vector3(0, DH - 1.5 - R, Z0)];
  for (let i = 1; i <= 3; i++) { const a = i / 3 * Math.PI / 2; pts.push(new THREE.Vector3(0, DH - 1.5 - R + R * Math.sin(a), Z0 + R - R * Math.cos(a))); }
  for (let i = 0; i <= 3; i++) { const a = i / 3 * Math.PI / 2; pts.push(new THREE.Vector3(0, DH - 1.5 - R + R * Math.cos(a), Z1 - R + R * Math.sin(a))); }
  pts.push(new THREE.Vector3(0, 0, Z1));
  const path = new THREE.CurvePath(); for (let i = 0; i < pts.length - 1; i++) path.add(new THREE.LineCurve3(pts[i], pts[i + 1]));
  const wireGeo = new THREE.TubeGeometry(path, pts.length * 2, 1.5, 5, false);
  const divs = [];
  for (let L = 0; L < NL; L++) {
    const xs = EXTRA.layers[L].xs; const im = new THREE.InstancedMesh(wireGeo, M.wire, xs.length); const m4 = new THREE.Matrix4();
    xs.forEach((x, i) => { m4.makeTranslation(x + 1.5, EXTRA.layers[L].y0, 0); im.setMatrixAt(i, m4); });
    layerG[L].add(im); divs.push(im);
  }
  // stored reel fleet (instanced, per-slot colour)
  const faceM = new THREE.MeshStandardMaterial({ map: reelFaceTex(), metalness: 0.1, roughness: 0.45 });
  const edgeM = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.1, roughness: 0.5 });
  const reelGeo = new THREE.CylinderGeometry(REEL_R, REEL_R, REEL_T, 28, 1); reelGeo.rotateZ(Math.PI / 2);
  const reels = []; const col = new THREE.Color();
  for (let L = 0; L < NL; L++) {
    const im = new THREE.InstancedMesh(reelGeo, [edgeM, faceM, faceM], NK); im.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    for (let k = 0; k < NK; k++) im.setColorAt(k, col.setHex(REEL_COLS[Math.floor(rnd(L * NK + k + 7) * REEL_COLS.length)]));
    im.frustumCulled = false; layerG[L].add(im); reels.push(im);
  }
  // LEDs on the front rail + slot glow (illustrative)
  const ledGeo = new THREE.BoxGeometry(14, 7, 3);
  const ledM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const glowM = new THREE.MeshBasicMaterial({ map: glowTex(), color: 0xffffff, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, side: THREE.DoubleSide });
  const dotM = new THREE.MeshBasicMaterial({ map: dotTex(), color: 0xffffff, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, side: THREE.DoubleSide });
  const glowGeo = new THREE.PlaneGeometry(22, 360); glowGeo.translate(0, 180, 0);
  const dotGeo = new THREE.PlaneGeometry(70, 70);
  const leds = [], glows = [], dots = [];
  for (let L = 0; L < NL; L++) {
    const a = new THREE.InstancedMesh(ledGeo, ledM, NK), b = new THREE.InstancedMesh(glowGeo, glowM, NK), c = new THREE.InstancedMesh(dotGeo, dotM, NK); const m4 = new THREE.Matrix4();
    for (let k = 0; k < NK; k++) { m4.makeTranslation(slotX(k), RAIL_TOP[L] - 17.5, FRONT_Z + 1.5); a.setMatrixAt(k, m4); m4.makeTranslation(slotX(k), RAIL_TOP[L] - 4, FRONT_Z - 12); b.setMatrixAt(k, m4); m4.makeTranslation(slotX(k), RAIL_TOP[L] - 17.5, FRONT_Z + 6); c.setMatrixAt(k, m4);
      a.setColorAt(k, col.setHex(0x20262e)); b.setColorAt(k, col.setHex(0)); c.setColorAt(k, col.setHex(0)); }
    a.frustumCulled = b.frustumCulled = c.frustumCulled = false; layerG[L].add(a); layerG[L].add(b); layerG[L].add(c); leds.push(a); glows.push(b); dots.push(c);
  }
  // top stack lights (illustrative, "2 top lights")
  const tops = [];
  for (const sx of [-1, 1]) {
    const g = new THREE.Group(); g.position.set(sx * 1205, 1850, 0); root.add(g);
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(8, 8, 60, 12), M.foot); pole.position.y = 30; g.add(pole);
    const segs = []; [0x22c55e, 0xf5b13d, 0xef4444].forEach((c, i) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(28, 28, 42, 20), new THREE.MeshStandardMaterial({ color: c, emissive: c, emissiveIntensity: 0.1, transparent: true, opacity: 0.92, roughness: 0.3 })); m.position.y = 85 + i * 44; g.add(m); segs.push(m); });
    const cap = new THREE.Mesh(new THREE.CylinderGeometry(24, 28, 14, 20), M.dark); cap.position.y = 85 + 3 * 44 - 15; g.add(cap);
    tops.push({ g, segs });
  }
  // PDA scanner (illustrative)
  const pda = new THREE.Group(); root.add(pda);
  { const body = new THREE.Mesh(new THREE.BoxGeometry(80, 170, 26), M.dark); pda.add(body);
    const scr = new THREE.Mesh(new THREE.PlaneGeometry(64, 90), new THREE.MeshBasicMaterial({ color: 0x0b3b52, toneMapped: false })); scr.position.set(0, 22, 13.2); pda.add(scr);
    const bar = new THREE.Mesh(new THREE.PlaneGeometry(56, 14), new THREE.MeshBasicMaterial({ color: 0x00c2ad, toneMapped: false })); bar.position.set(0, 52, 13.4); pda.add(bar);
    const keys = new THREE.Mesh(new THREE.PlaneGeometry(64, 46), new THREE.MeshStandardMaterial({ color: 0x2b3448, roughness: 0.5 })); keys.position.set(0, -50, 13.2); pda.add(keys);
    const nose = new THREE.Mesh(new THREE.BoxGeometry(60, 20, 34), M.dark); nose.position.set(0, 92, -4); pda.add(nose);
    const win = new THREE.Mesh(new THREE.PlaneGeometry(40, 10), new THREE.MeshBasicMaterial({ color: 0xff3b30, toneMapped: false })); win.position.set(0, 102.2, -4); win.rotation.x = -Math.PI / 2; pda.add(win);
    const grip = new THREE.Mesh(new THREE.BoxGeometry(46, 90, 30), M.dark); grip.position.set(0, -30, -26); grip.rotation.x = 0.5; pda.add(grip); }
  const laserM = new THREE.MeshBasicMaterial({ color: 0xff2a1f, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, side: THREE.DoubleSide });
  const laser = new THREE.Mesh(new THREE.BufferGeometry(), laserM); root.add(laser);
  pda.visible = false;

  const state = { explode: 0, time: 0, slotFn: null, hero: null, pda: null, laser: 0, top: [0, 0, 0], highlight: {}, fleet: 1 };
  const hl = new THREE.Color(0x38bdf8);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3(), pv = new THREE.Vector3();
  function apply(s) {
    Object.assign(state, s || {});
    const e = THREE.MathUtils.smootherstep(state.explode, 0, 1);
    meshes.panelL.position.x = -420 * e; meshes.panelR.position.x = 420 * e; meshes.foot.position.y = -160 * e;
    tops[0].g.position.set(-1205 - 420 * e, 1850, 0); tops[1].g.position.set(1205 + 420 * e, 1850, 0);
    layerG.forEach((g, L) => { g.position.y = L * 120 * e; });
    // slots
    for (let L = 0; L < NL; L++) {
      const rim = reels[L], ld = leds[L], gw = glows[L], dt = dots[L];
      for (let k = 0; k < NK; k++) {
        const i = L * NK + k; let occ = FILL[i], out = 0, lc = null, lk = 0;
        if (state.slotFn) { const r = state.slotFn(i, L, k, occ); occ = r[0]; out = r[1]; lc = r[2]; lk = r[3]; }
        const vis = occ * state.fleet * (1 - e);
        sc.setScalar(vis > 0.01 ? 1 : 0.0001); pv.set(slotX(k), slotY(L) + (vis > 0.01 ? 0 : -5000), out * 220);
        m4.compose(pv, q, sc); rim.setMatrixAt(k, m4);
        if (lc && lk > 0.001) { col.setHex(lc).multiplyScalar(Math.min(1, 0.25 + lk)); ld.setColorAt(k, col); col.setHex(lc).multiplyScalar(lk * 0.75); gw.setColorAt(k, col); col.setHex(lc).multiplyScalar(lk); dt.setColorAt(k, col); }
        else { ld.setColorAt(k, col.setHex(0x20262e)); gw.setColorAt(k, col.setHex(0)); dt.setColorAt(k, col.setHex(0)); }
      }
      rim.instanceMatrix.needsUpdate = true; ld.instanceColor.needsUpdate = true; gw.instanceColor.needsUpdate = true; dt.instanceColor.needsUpdate = true;
    }
    // hero reel
    const h = state.hero; heroG.visible = !!h && e < 0.02;
    if (h) { heroG.position.set(...h.pos); heroG.rotation.set(h.rx || 0, h.ry || 0, h.rz || 0); }
    // pda + laser
    const p = state.pda; pda.visible = !!p;
    if (p) { pda.position.set(...p.pos); pda.rotation.set(p.rx || 0, p.ry || 0, p.rz || 0); }
    laser.visible = !!p && state.laser > 0.01;
    if (laser.visible && p.target) {
      pda.updateMatrixWorld(); const o = new THREE.Vector3(0, 102, -4).applyMatrix4(pda.matrixWorld); const t = new THREE.Vector3(...p.target);
      const w = p.fan || 60; const ax = new THREE.Vector3(...(p.fanAxis || [0, 0, 1])).multiplyScalar(w / 2);
      const a = t.clone().add(ax), b = t.clone().sub(ax);
      laser.geometry.setAttribute('position', new THREE.Float32BufferAttribute([o.x, o.y, o.z, a.x, a.y, a.z, b.x, b.y, b.z], 3)); laser.geometry.attributes.position.needsUpdate = true;
      laserM.opacity = 0.55 * state.laser;
    }
    // stack lights
    tops.forEach(tp => tp.segs.forEach((m, i) => { m.material.emissiveIntensity = 0.1 + 2.2 * (state.top[i] || 0); }));
    // highlights
    for (const [n, m] of Object.entries(meshes)) {
      const kk = (n.startsWith('rail') ? state.highlight.rail : n.startsWith('panel') ? state.highlight.panel : state.highlight[n]) || 0;
      if (kk > 0) { if (!m.userData.hlMat) { m.userData.baseMat0 = m.material; m.userData.hlMat = m.material.clone(); } m.material = m.userData.hlMat; m.material.emissive = new THREE.Color().copy(hl).multiplyScalar(0.5 * kk); }
      else if (m.userData.baseMat0 && m.material === m.userData.hlMat) m.material = m.userData.baseMat0;
    }
    { const kk = state.highlight.divider || 0; M.wire.emissive = new THREE.Color().copy(hl).multiplyScalar(0.55 * kk); }
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
  return { THREE, renderer, scene, camera, root, meshes, state, apply, render, setCamera, setSize, project };
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
