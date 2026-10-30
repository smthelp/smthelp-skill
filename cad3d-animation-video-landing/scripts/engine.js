// CN-SM-2713 gripper nozzle — shared 3D stage (landing page + video renderer)
import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { loadModel } from './loader.js';

export const PIVOT_L = new THREE.Vector3(-5.5, -15.6, 0);
export const PIVOT_R = new THREE.Vector3(5.5, -15.6, 0);
export const ARM = 5.5;          // pivot -> center pin lever (mm)
export const STROKE = 1.05;      // plunger travel for full open (mm)

export const ANCHORS = {
  shank: [0, 9, 0],
  shankTop: [0, 13, 0],
  plunger: [0, -2.0, 0],
  spring: [2.6, -5.4, 0],
  pinC: [0, -15.15, 3.3],
  pivotL: [-5.5, -15.6, 3.5],
  pivotR: [5.5, -15.6, 3.3],
  jawL: [-6.8, -21, 0],
  jawR: [6.8, -21, 0],
  padR: [6.0, -25.3, 0],
  padL1: [-4.8, -25.3, 3.6],
  padL2: [-4.8, -25.3, -3.6],
  stop: [0, -19.3, 0],
  coilTop: [0, -20.2, 0],
  coil: [4.25, -27, 0],
  leads: [2.5, -37, 0],
  holder: [7, -12, 0],
  clipL: [-5.5, -15.6, 2.9],
};

const EXPLODE = {
  nozzle: [0, 22, 0], pin_inner: [0, 15, 0], spring: [0, 10, 0], plunger: [0, 4.5, 0], setscrew: [0, 0, -9],
  holder: [0, 0, 0], jawL: [-11, -5, 0], jawR: [11, -5, 0],
  padL1: [-15, -5, 4], padL2: [-15, -5, -4], padR: [16, -5, 0],
  pivotL: [-11, -5, 9], washL: [-11, -5, 11.5], clipL: [-11, -5, 14],
  pivotR: [11, -5, -9], washR: [11, -5, -11.5], clipR: [11, -5, -14],
  pinC: [0, -1.5, 10], washC: [0, -1.5, -10], clipC: [0, -1.5, -13],
  stop: [0, -6, 0], coil: [0, -15, 0], coil_leads: [0, -15, 0], lead_ext: [0, -15, 0],
};

function mat(o) { return new THREE.MeshPhysicalMaterial(Object.assign({ side: THREE.FrontSide }, o)); }

export async function createStage(canvas, opts = {}) {
  const geos = await loadModel(opts.modelB64);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: opts.aa !== false, alpha: true, preserveDrawingBuffer: !!opts.preserve, powerPreference: 'high-performance' });
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.localClippingEnabled = true;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.9;
  const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(40, 60, 80); scene.add(key);
  const rim = new THREE.DirectionalLight(0x5ad7ff, 2.4); rim.position.set(-60, 20, -60); scene.add(rim);
  const fill = new THREE.DirectionalLight(0x9fffe9, 0.6); fill.position.set(-40, -30, 50); scene.add(fill);

  const camera = new THREE.PerspectiveCamera(28, 16 / 9, 1, 2000);

  // ---------- materials ----------
  const cutPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), 1000);
  const M = {
    steel: mat({ color: 0xd9dee6, metalness: 1, roughness: 0.26 }),
    steelBright: mat({ color: 0xeef2f7, metalness: 1, roughness: 0.16 }),
    jaw: mat({ color: 0x8a96a6, metalness: 1, roughness: 0.32, clearcoat: 0.4 }),
    anod: mat({ color: 0x1b1f27, metalness: 0.55, roughness: 0.38, clearcoat: 0.6, clearcoatRoughness: 0.25 }),
    blued: mat({ color: 0x2c3646, metalness: 0.9, roughness: 0.3 }),
    accent: mat({ color: 0xf5b13d, metalness: 1, roughness: 0.25, emissive: 0x000000 }),
    coil: mat({ color: 0x1f47c9, metalness: 0.05, roughness: 0.32, clearcoat: 1, clearcoatRoughness: 0.15 }),
    lead: mat({ color: 0xe8ecf2, metalness: 1, roughness: 0.2 }),
  };
  const cutMats = new Set();
  function cutable(m) { const c = m.clone(); c.clippingPlanes = [cutPlane]; c.side = THREE.DoubleSide; cutMats.add(c); return c; }
  const capMat = new THREE.MeshBasicMaterial({ color: 0x00c2ad, side: THREE.BackSide, clippingPlanes: [cutPlane] });

  const partMat = {
    nozzle: cutable(M.steel), pin_inner: cutable(M.steelBright), spring: cutable(M.steelBright), plunger: cutable(M.steelBright),
    holder: cutable(M.anod), setscrew: M.blued,
    jawL: M.jaw, jawR: M.jaw, pivotL: M.steelBright, pivotR: M.steelBright, pinC: M.steelBright,
    clipL: M.blued, clipR: M.blued, clipC: M.blued, washL: M.steel, washR: M.steel, washC: M.steel,
    padL1: M.accent, padL2: M.accent, padR: M.accent, stop: M.accent, coil: M.coil, coil_leads: M.lead,
  };

  // ---------- hierarchy ----------
  const rig = new THREE.Group(); scene.add(rig);
  const plungerG = new THREE.Group(); rig.add(plungerG);
  const jawLG = new THREE.Group(); jawLG.position.copy(PIVOT_L); rig.add(jawLG);
  const jawRG = new THREE.Group(); jawRG.position.copy(PIVOT_R); rig.add(jawRG);
  const coilG = new THREE.Group(); scene.add(coilG);
  const parent = {
    plunger: plungerG, pin_inner: plungerG, pinC: plungerG, clipC: plungerG, washC: plungerG,
    jawL: jawLG, padL1: jawLG, padL2: jawLG, jawR: jawRG, padR: jawRG, coil: coilG, coil_leads: coilG,
  };
  const meshes = {}; const base = {};
  for (const [name, o] of Object.entries(geos)) {
    const m = new THREE.Mesh(o.geo, partMat[name] || M.steel);
    m.name = name;
    const p = parent[name] || rig;
    if (p === jawLG) m.position.copy(PIVOT_L).negate();
    if (p === jawRG) m.position.copy(PIVOT_R).negate();
    base[name] = m.position.clone();
    p.add(m); meshes[name] = m;
    if (partMat[name] && cutMats.has(partMat[name])) { const cap = new THREE.Mesh(o.geo, capMat); m.add(cap); }
  }
  // extend the short CAD leads so through-hole insertion reads clearly
  const leadExtGeo = new THREE.CylinderGeometry(0.3, 0.3, 5, 16); leadExtGeo.translate(0, -35.8 - 2.5 + 0.05, 0);
  const leadExt = new THREE.Group(); leadExt.name = 'lead_ext';
  for (const x of [-2.5, 2.5]) { const l = new THREE.Mesh(leadExtGeo, M.lead); l.position.x = x; leadExt.add(l); }
  const ltip = new THREE.ConeGeometry(0.3, 0.5, 16); ltip.rotateX(Math.PI); ltip.translate(0, -35.8 - 5 - 0.2, 0);
  for (const x of [-2.5, 2.5]) { const l = new THREE.Mesh(ltip, M.lead); l.position.x = x; leadExt.add(l); }
  coilG.add(leadExt); meshes.lead_ext = leadExt; base.lead_ext = new THREE.Vector3();
  const spring = meshes.spring; const springTop = -3.02, springBot = -7.9;

  // ---------- environment props for the pick & place cycle ----------
  const props = new THREE.Group(); props.visible = false; scene.add(props);
  const trayMat = mat({ color: 0x23272f, metalness: 0.2, roughness: 0.6 });
  {
    const s = new THREE.Shape(); s.moveTo(-15, -15); s.lineTo(15, -15); s.lineTo(15, 15); s.lineTo(-15, 15); s.lineTo(-15, -15);
    const h = new THREE.Path(); h.absarc(0, 0, 8.4, 0, Math.PI * 2, true); s.holes.push(h);
    const g = new THREE.ExtrudeGeometry(s, { depth: 4.6, bevelEnabled: true, bevelSize: 0.4, bevelThickness: 0.4, bevelSegments: 2, curveSegments: 64 });
    g.rotateX(-Math.PI / 2); const tray = new THREE.Mesh(g, trayMat); tray.position.set(-30, -37.6, 0); props.add(tray);
    const floor = new THREE.Mesh(new THREE.BoxGeometry(30, 2, 30), trayMat); floor.position.set(-30, -38.6, 0); props.add(floor);
    props.userData.trayCenter = new THREE.Vector3(-30, 0, 0);
  }
  const pcbMat = mat({ color: 0x0f5a3a, metalness: 0.1, roughness: 0.45, clearcoat: 0.7 });
  const copper = mat({ color: 0xe0b060, metalness: 1, roughness: 0.25 });
  {
    const s = new THREE.Shape(); s.moveTo(-18, -14); s.lineTo(18, -14); s.lineTo(18, 14); s.lineTo(-18, 14); s.lineTo(-18, -14);
    for (const x of [-2.5, 2.5]) { const h = new THREE.Path(); h.absarc(x, 0, 0.55, 0, Math.PI * 2, true); s.holes.push(h); }
    const g = new THREE.ExtrudeGeometry(s, { depth: 1.6, bevelEnabled: false, curveSegments: 24 }); g.rotateX(-Math.PI / 2);
    const pcb = new THREE.Mesh(g, pcbMat); pcb.position.set(30, -42.2, 0); props.add(pcb);
    for (const x of [-2.5, 2.5]) { const r = new THREE.Mesh(new THREE.RingGeometry(0.55, 1.25, 32), copper); r.rotation.x = -Math.PI / 2; r.position.set(30 + x, -40.58, 0); props.add(r); }
    // silkscreen outline of the coil footprint
    const ring = new THREE.Mesh(new THREE.RingGeometry(4.45, 4.65, 64), new THREE.MeshBasicMaterial({ color: 0xf2f2f2 })); ring.rotation.x = -Math.PI / 2; ring.position.set(30, -40.57, 0); props.add(ring);
    props.userData.pcbCenter = new THREE.Vector3(30, 0, 0);
  }
  // decorative extra coils in the tray row
  // (single pocket kept clean for clarity)

  // ---------- state ----------
  const state = {
    open: 0, explode: 0, cut: 0, highlight: {}, rigPos: [0, 0, 0], coilPos: [0, 0, 0], coilAttached: true,
    props: false, rigRotY: 0,
  };
  const hl = new THREE.Color(0x00e0c4);

  function apply(s) {
    Object.assign(state, s || {});
    const d = THREE.MathUtils.clamp(state.open, 0, 1) * STROKE;
    plungerG.position.y = -d;
    const th = Math.asin(d / ARM);
    jawLG.rotation.z = -th; jawRG.rotation.z = th;
    const sh = (springTop - d) - springBot; const sy = sh / (springTop - springBot);
    spring.scale.y = sy; spring.position.y = springBot * (1 - sy);
    // explode
    const e = THREE.MathUtils.smootherstep(state.explode, 0, 1);
    for (const [n, m] of Object.entries(meshes)) {
      const off = EXPLODE[n] || [0, 0, 0];
      m.position.set(base[n].x + off[0] * e, base[n].y + off[1] * e, base[n].z + off[2] * e);
      if (n === 'spring') m.position.y += springBot * (1 - sy);
    }
    // cutaway (0 = solid, 1 = half section at z=0)
    cutPlane.constant = state.cut > 0.001 ? THREE.MathUtils.lerp(9, 0, THREE.MathUtils.smootherstep(state.cut, 0, 1)) : 1000;
    // highlights
    for (const [n, m] of Object.entries(meshes)) {
      const k = state.highlight[n] || 0;
      const mats = m.isMesh ? [m] : m.children;
      for (const mm of mats) {
        if (!mm.material || !mm.material.emissive) continue;
        if (k > 0) {
          if (!mm.userData.hlMat) { mm.userData.baseMat = mm.material; mm.userData.hlMat = mm.material.clone(); }
          mm.material = mm.userData.hlMat; mm.material.emissive.copy(hl).multiplyScalar(0.38 * k);
        } else if (mm.userData.baseMat) mm.material = mm.userData.baseMat;
      }
    }
    rig.position.set(...state.rigPos); rig.rotation.y = state.rigRotY;
    if (state.coilAttached) { coilG.position.set(state.rigPos[0], state.rigPos[1], state.rigPos[2]); coilG.rotation.y = state.rigRotY; }
    else { coilG.position.set(...state.coilPos); coilG.rotation.y = 0; }
    coilG.visible = state.coilVisible !== false;
    props.visible = !!state.props;
  }
  apply();

  const _v = new THREE.Vector3();
  function project(anchor, w, h, inRig = true) {
    _v.set(...anchor);
    if (inRig) rig.localToWorld(_v);
    _v.project(camera);
    return [(_v.x * 0.5 + 0.5) * w, (-_v.y * 0.5 + 0.5) * h, _v.z];
  }
  function anchorWorld(name) { const a = ANCHORS[name]; _v.set(...a); rig.localToWorld(_v); return _v.clone(); }

  function setCamera(pos, target, fov, w, h, shiftX = 0, shiftY = 0) {
    camera.fov = fov; camera.aspect = w / h;
    camera.position.set(...pos); camera.up.set(0, 1, 0); camera.lookAt(new THREE.Vector3(...target));
    if (shiftX || shiftY) camera.setViewOffset(w, h, -shiftX * w, -shiftY * h, w, h); else camera.clearViewOffset();
    camera.updateProjectionMatrix();
  }
  function setSize(w, h, pr = 1) { renderer.setPixelRatio(pr); renderer.setSize(w, h, false); }
  function render() { renderer.render(scene, camera); }

  return { THREE, renderer, scene, camera, rig, meshes, state, apply, render, setCamera, setSize, project, anchorWorld, props, coilG };
}

// easing helpers
export const ease = {
  io: t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
  out: t => 1 - Math.pow(1 - t, 3),
  in: t => t * t * t,
  smooth: t => t * t * (3 - 2 * t),
};
export function clamp01(x) { return Math.max(0, Math.min(1, x)); }
export function seg(t, a, b) { return clamp01((t - a) / (b - a)); }
export function lerp(a, b, t) { return a + (b - a) * t; }
export function lerp3(a, b, t) { return [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)]; }
// orbit-style camera from spherical params around a target
export function orbit(target, dist, azDeg, elDeg) {
  const az = azDeg * Math.PI / 180, el = elDeg * Math.PI / 180;
  return [target[0] + dist * Math.cos(el) * Math.sin(az), target[1] + dist * Math.sin(el), target[2] + dist * Math.cos(el) * Math.cos(az)];
}
