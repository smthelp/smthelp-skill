// SBF1001 vibratory bowl feeder — shared 3D stage (landing page + video renderer). Units: mm, Y up, floor at y=0.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { loadModel } from './loader.js';

export const BOWL_C = new THREE.Vector3(4.7, 0, -13.7);   // bowl axis (x,z)
export const BOWL_FLOOR = 824, BOWL_RIM = 916, BOWL_R = 140;
export const RAIL_X = -119.5, RAIL_Y = 893.5, RAIL_Z0 = 126, RAIL_Z1 = 626;   // part centre line on the linear rail
export const PICK = [-119.5, 900, 626];

export const ANCHORS = {
  bowl: [-120, 900, -40], bowlRim: [4.7, 916, -153], bowlIn: [4.7, 840, -13.7], drive: [-88, 730, -14], mount: [130, 611, 100],
  stud: [-100, 640, -133], rubber: [80, 631, 50], rail: [-120, 901, 380], lindrive: [-115, 835, 330], liniso: [-115, 772, 300],
  station: [-115, 880, 560], pick: PICK, fibre: [-142, 898, 620], camera: [-90, 950, -34], light: [-141, 965, -58],
  hmi: [176, 1020, 0], top: [150, 550, 150], ebox: [0, 360, -150], caster: [190, 70, -190], cart: [200, 380, -200],
  handle: [-196, 420, -230], outlet: [-122, 905, 110], bracket: [-100, 700, 115], helix: [125, 870, -13.7],
};

const EXPLODE = {
  caster: [0, -60, 0], caster_plate: [0, -30, 0], alu: [0, 0, 0], panel: [0, 0, -70], handle: [0, 0, -110], ebox: [0, 0, -40], logo: [0, 0, -70],
  top: [0, 40, 0], stud: [0, 90, 0], mount: [0, 110, 0], rubber: [0, 170, 0], drive: [0, 230, 0], bowl: [0, 340, 0], parts: [0, 340, 0], helix: [0, 340, 0],
  clamp: [-60, 420, 0], cam: [-60, 440, 0], light: [-60, 440, 0], hmi: [120, 380, 0], screen: [120, 380, 0],
  bracket: [0, 60, 140], liniso: [0, 120, 140], lindrive: [0, 170, 140], counter: [0, 170, 140], rail: [0, 250, 160], station_plate: [0, 190, 230],
  station: [0, 230, 260], stopper: [0, 270, 280], railparts: [0, 250, 160],
};

function mat(o) { o = Object.assign({ side: THREE.DoubleSide }, o); delete o.clearcoat; delete o.clearcoatRoughness; return new THREE.MeshStandardMaterial(o); }

export async function createStage(canvas, opts = {}) {
  const geos = await loadModel(opts.modelB64);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: opts.aa !== false, alpha: true, preserveDrawingBuffer: !!opts.preserve, powerPreference: 'high-performance' });
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.85;
  const key = new THREE.DirectionalLight(0xffffff, 2.3); key.position.set(900, 1800, -1200); scene.add(key);
  const rim = new THREE.DirectionalLight(0x5ad7ff, 2.2); rim.position.set(-1400, 900, 1400); scene.add(rim);
  const fill = new THREE.DirectionalLight(0x9fffe9, 0.55); fill.position.set(-900, 300, -900); scene.add(fill);
  const camera = new THREE.PerspectiveCamera(30, 16 / 9, 20, 20000);

  // ---------- materials ----------
  const M = {
    stainless: mat({ color: 0xe6ebf2, metalness: 1, roughness: 0.18 }),
    bowl: mat({ color: 0xdfe6ee, metalness: 1, roughness: 0.14, clearcoat: 0.5 }),
    alu: mat({ color: 0xc3cad4, metalness: 0.9, roughness: 0.34 }),
    plate: mat({ color: 0xb8c0cb, metalness: 0.85, roughness: 0.3 }),
    navy: mat({ color: 0x14203a, metalness: 0.35, roughness: 0.45, clearcoat: 0.5, clearcoatRoughness: 0.3 }),
    dark: mat({ color: 0x1b1f27, metalness: 0.5, roughness: 0.42, clearcoat: 0.4 }),
    drive: mat({ color: 0x2a3140, metalness: 0.75, roughness: 0.32, clearcoat: 0.6 }),
    rubber: mat({ color: 0x0e1014, metalness: 0, roughness: 0.85 }),
    teal: mat({ color: 0x00a896, metalness: 0.45, roughness: 0.35, clearcoat: 0.6 }),
    tealBright: mat({ color: 0x00c2ad, metalness: 0.3, roughness: 0.3, emissive: 0x003d36 }),
    amber: mat({ color: 0xf5b13d, metalness: 0.9, roughness: 0.28 }),
    glass: new THREE.MeshPhysicalMaterial({ color: 0x0b1a2a, metalness: 0.1, roughness: 0.05, emissive: 0x06303a, side: THREE.DoubleSide }),
    cover: new THREE.MeshPhysicalMaterial({ color: 0xbfe9ff, metalness: 0, roughness: 0.08, transparent: true, opacity: 0.28, depthWrite: false, side: THREE.DoubleSide }),
  };
  const partMat = {
    bowl: M.bowl, drive: M.drive, rubber: M.rubber, stud: M.stainless, mount: M.plate, top: M.plate,
    alu: M.alu, panel: M.navy, handle: M.dark, ebox: M.dark, logo: M.teal, caster: M.dark, caster_plate: M.alu,
    cam: M.dark, light: M.tealBright, clamp: M.alu, hmi: M.navy, screen: M.glass,
    lindrive: M.drive, counter: M.stainless, liniso: M.rubber, bracket: M.navy, rail: M.stainless,
    station_plate: M.plate, station: M.teal, stopper: M.amber,
  };
  const cartGhostable = new Set(['alu', 'panel', 'handle', 'top', 'logo', 'caster_plate']);

  // ---------- hierarchy ----------
  const root = new THREE.Group(); scene.add(root);
  const bowlG = new THREE.Group(); root.add(bowlG);        // vibrating bowl (torsion about its axis)
  bowlG.position.copy(BOWL_C);
  const railG = new THREE.Group(); root.add(railG);        // vibrating linear rail
  const parent = { bowl: bowlG, rail: railG };
  const meshes = {}; const base = {};
  for (const [name, o] of Object.entries(geos)) {
    const m = new THREE.Mesh(o.geo, partMat[name] || M.alu);
    m.name = name;
    const p = parent[name] || root;
    if (p === bowlG) m.position.copy(BOWL_C).negate();
    base[name] = m.position.clone();
    p.add(m); meshes[name] = m;
  }
  // split the rail cover off as clear so the parts in the channel stay visible
  // (cover is the 2 mm strip on top of the rail; rendered translucent for clarity)
  meshes.rail.material = M.stainless;

  // ---------- illustrated helical track inside the bowl ----------
  const helixG = new THREE.Group(); bowlG.add(helixG); meshes.helix = helixG; base.helix = new THREE.Vector3();
  const TURNS = 1.6, R_TRACK = 122, TH_OUT = Math.atan2(-124.5, 64);   // outlet angle (x=-124 from axis toward rail)
  const TH0 = TH_OUT - TURNS * Math.PI * 2;
  const helixPt = (u) => { const th = TH0 + (TH_OUT - TH0) * u; const y = BOWL_FLOOR + 4 + (BOWL_RIM - 10 - BOWL_FLOOR - 4) * u; return new THREE.Vector3(Math.sin(th) * R_TRACK, y, Math.cos(th) * R_TRACK); };
  {
    const N = 260, w = 16; const pos = []; const idx = [];
    for (let i = 0; i <= N; i++) {
      const u = i / N; const p = helixPt(u); const rdir = new THREE.Vector3(p.x, 0, p.z).normalize();
      const a = p.clone().addScaledVector(rdir, w / 2), b = p.clone().addScaledVector(rdir, -w / 2); a.y -= 3; b.y -= 3;
      pos.push(a.x, a.y, a.z, b.x, b.y, b.z);
      if (i < N) { const k = i * 2; idx.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); }
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals();
    const hm = new THREE.MeshPhysicalMaterial({ color: 0x00c2ad, metalness: 0.6, roughness: 0.3, emissive: 0x00594f, transparent: true, opacity: 0.9, side: THREE.DoubleSide });
    helixG.add(new THREE.Mesh(g, hm));
    // inner lip (wall) of the track
    const wall = []; const widx = [];
    for (let i = 0; i <= N; i++) { const p = helixPt(i / N); const rdir = new THREE.Vector3(p.x, 0, p.z).normalize(); const a = p.clone().addScaledVector(rdir, -w / 2); a.y -= 3; const b = a.clone(); b.y += 5;
      wall.push(a.x, a.y, a.z, b.x, b.y, b.z); if (i < N) { const k = i * 2; widx.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); } }
    const wg = new THREE.BufferGeometry(); wg.setAttribute('position', new THREE.Float32BufferAttribute(wall, 3)); wg.setIndex(widx); wg.computeVertexNormals();
    helixG.add(new THREE.Mesh(wg, hm));
  }
  // bowl floor cone so the pile reads
  { const g = new THREE.CircleGeometry(BOWL_R - 6, 64); g.rotateX(-Math.PI / 2); g.translate(0, BOWL_FLOOR, 0); bowlG.add(new THREE.Mesh(g, M.bowl)); }

  // ---------- components (illustrative slot-type switch bodies) ----------
  const partGeo = (() => { // U-shaped slot switch, ~12 x 6 x 10 mm, slot up
    const s = new THREE.Shape(); s.moveTo(-6, 0); s.lineTo(6, 0); s.lineTo(6, 10); s.lineTo(3.4, 10); s.lineTo(3.4, 3.2); s.lineTo(-3.4, 3.2); s.lineTo(-3.4, 10); s.lineTo(-6, 10); s.lineTo(-6, 0);
    const g = new THREE.ExtrudeGeometry(s, { depth: 6, bevelEnabled: false }); g.translate(0, 0, -3); g.rotateY(Math.PI / 2); return g; })();
  const partMatP = mat({ color: 0x15171c, metalness: 0.1, roughness: 0.5, clearcoat: 0.8 });
  const partMatHL = mat({ color: 0x15171c, metalness: 0.1, roughness: 0.5, emissive: 0x00c2ad, emissiveIntensity: 0.0 });
  const flowG = new THREE.Group(); root.add(flowG); meshes.parts = flowG; base.parts = new THREE.Vector3();
  const QN = Math.floor((RAIL_Z1 - RAIL_Z0) / 13) - 1, HN = 16, NF = QN + HN; const flow = [];
  for (let i = 0; i < NF; i++) { const m = new THREE.Mesh(partGeo, partMatP); flowG.add(m); flow.push(m); }
  const pileG = new THREE.Group(); bowlG.add(pileG);
  const rnd = (() => { let s = 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
  const pile = [];
  for (let i = 0; i < 70; i++) { const m = new THREE.Mesh(partGeo, partMatP); const r = Math.sqrt(rnd()) * 85, a = rnd() * Math.PI * 2;
    m.position.set(Math.sin(a) * r, BOWL_FLOOR + rnd() * 8 * (1 - r / 95), Math.cos(a) * r); m.rotation.set(rnd() * 3, rnd() * 6, rnd() * 3); m.userData.p0 = m.position.clone(); m.userData.r0 = m.rotation.clone(); pileG.add(m); pile.push(m); }
  // rejected parts: climb part way, tip off the track and fall back
  const rej = []; for (let i = 0; i < 4; i++) { const m = new THREE.Mesh(partGeo, mat({ color: 0x15171c, roughness: 0.5, emissive: 0xff4d3d, emissiveIntensity: 0.0 })); bowlG.add(m); rej.push(m); }

  // world path: helix (bowl local -> world) + outlet chute + rail
  const pathPts = [];
  for (let i = 0; i <= 200; i++) { const p = helixPt(i / 200); pathPts.push(p.add(BOWL_C)); }
  pathPts.push(new THREE.Vector3(RAIL_X, RAIL_Y + 1, RAIL_Z0 - 10));
  const railSteps = 40; for (let i = 0; i <= railSteps; i++) pathPts.push(new THREE.Vector3(RAIL_X, RAIL_Y, RAIL_Z0 + (RAIL_Z1 - RAIL_Z0) * i / railSteps));
  const cum = [0]; for (let i = 1; i < pathPts.length; i++) cum.push(cum[i - 1] + pathPts[i].distanceTo(pathPts[i - 1]));
  const PATH_LEN = cum[cum.length - 1]; const RAIL_START_S = cum[201]; const GAP = 13;
  function pathAt(s) {
    s = Math.max(0, Math.min(PATH_LEN, s)); let lo = 0, hi = cum.length - 1; while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (cum[mid] < s) lo = mid; else hi = mid; }
    const t = (s - cum[lo]) / Math.max(1e-6, cum[hi] - cum[lo]); const p = pathPts[lo].clone().lerp(pathPts[hi], t); const dir = pathPts[hi].clone().sub(pathPts[lo]).normalize(); return [p, dir];
  }

  // ---------- effects ----------
  const fx = new THREE.Group(); root.add(fx);
  const addMat = (c, o = 0.6) => new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: o, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
  // vibration rings around the coil drive
  const rings = []; for (let i = 0; i < 3; i++) { const r = new THREE.Mesh(new THREE.TorusGeometry(100, 1.6, 8, 96), addMat(0x00e0c4, 0.0)); r.rotation.x = Math.PI / 2; r.position.set(BOWL_C.x, 730, BOWL_C.z); fx.add(r); rings.push(r); }
  // air-blow streaks along the rail
  const air = []; for (let i = 0; i < 9; i++) { const g = new THREE.CylinderGeometry(0.9, 0.9, 46, 6); g.rotateX(Math.PI / 2); const m = new THREE.Mesh(g, addMat(0x7fe7ff, 0.0)); fx.add(m); air.push(m); }
  // optical fibre beam at the pick point
  const beamG = new THREE.CylinderGeometry(1.8, 1.8, 50, 10); beamG.rotateZ(Math.PI / 2);
  const beam = new THREE.Mesh(beamG, addMat(0xff3b30, 0.0)); beam.position.set(RAIL_X, RAIL_Y + 4, RAIL_Z1 - 6); fx.add(beam);
  const beamDot = new THREE.Mesh(new THREE.SphereGeometry(5, 16, 12), addMat(0xff3b30, 0.0)); beamDot.position.set(RAIL_X - 24, RAIL_Y + 4, RAIL_Z1 - 6); fx.add(beamDot);
  // camera field of view into the bowl
  const fovG = new THREE.ConeGeometry(78, 76, 48, 1, true); fovG.translate(0, -38, 0);
  const fov = new THREE.Mesh(fovG, addMat(0x38bdf8, 0.0)); fov.position.set(-113, 901, -34); fov.rotation.z = -0.32; fov.rotation.x = 0.0; fx.add(fov);
  // pick head (illustrative nozzle that takes the part)
  const head = new THREE.Group(); fx.add(head);
  { const b = new THREE.Mesh(new THREE.CylinderGeometry(7, 7, 60, 24), M.stainless); b.position.y = 30; head.add(b); const t = new THREE.Mesh(new THREE.CylinderGeometry(3.4, 5, 10, 24), M.amber); t.position.y = -1; head.add(t); }
  head.visible = false;

  // ---------- state ----------
  const state = { explode: 0, ghost: 0, vib: 0, flowT: 0, flow: 0, air: 0, fibre: 0, vision: 0, helix: 1, highlight: {}, reject: 0, rejT: 0, pickEvery: 0.8, railFull: 0, head: 0, time: 0, partsVisible: true };
  const hl = new THREE.Color(0x00e0c4);

  function apply(s) {
    Object.assign(state, s || {});
    const t = state.time;
    const e = THREE.MathUtils.smootherstep(state.explode, 0, 1);
    for (const [n, m] of Object.entries(meshes)) {
      const off = EXPLODE[n] || [0, 0, 0];
      m.position.set(base[n].x + off[0] * e, base[n].y + off[1] * e, base[n].z + off[2] * e);
    }
    const eb = EXPLODE.bowl, er = EXPLODE.rail;
    bowlG.position.set(BOWL_C.x + eb[0] * e, eb[1] * e, BOWL_C.z + eb[2] * e);
    meshes.bowl.position.copy(BOWL_C).negate(); meshes.helix.position.set(0, 0, 0);
    railG.position.set(er[0] * e, er[1] * e, er[2] * e); meshes.rail.position.set(0, 0, 0);
    // vibration (visible but small): bowl torsion + lift, rail fore/aft
    const v = state.vib;
    bowlG.rotation.y = v * 0.006 * Math.sin(t * 2 * Math.PI * 7.3);
    bowlG.position.y += v * 0.7 * Math.sin(t * 2 * Math.PI * 7.3 + 1.2);
    railG.position.z += v * 0.6 * Math.sin(t * 2 * Math.PI * 9.1);
    rings.forEach((r, i) => { const ph = ((t * 1.4 + i / 3) % 1); r.scale.setScalar(1 + ph * 0.55); r.material.opacity = v * 0.55 * (1 - ph) * (1 - e); r.position.y = 730 + EXPLODE.drive[1] * e; });
    // ghost cart (reveal controller inside)
    const g = state.ghost;
    for (const n of cartGhostable) { const m = meshes[n]; if (!m) continue;
      if (g > 0.001) { if (!m.userData.gm) { m.userData.bm = m.material; m.userData.gm = m.material.clone(); m.userData.gm.transparent = true; m.userData.gm.depthWrite = false; } m.material = m.userData.gm; m.material.opacity = 1 - 0.82 * g; }
      else if (m.userData.bm) m.material = m.userData.bm; }
    // highlights
    for (const [n, m] of Object.entries(meshes)) {
      const k = state.highlight[n] || 0; if (!m.isMesh) continue;
      if (k > 0) { if (!m.userData.hlMat) { m.userData.baseMat0 = m.material; m.userData.hlMat = m.material.clone(); } m.material = m.userData.hlMat; m.material.emissive = new THREE.Color().copy(hl).multiplyScalar(0.4 * k); }
      else if (m.userData.baseMat0 && m.material === m.userData.hlMat) m.material = m.userData.baseMat0;
    }
    meshes.helix.visible = state.helix > 0.01;
    // parts: rail is a full queue that steps forward one pitch per pick; helix parts climb continuously
    const showParts = state.partsVisible && e < 0.02;
    flowG.visible = showParts; pileG.visible = state.partsVisible;
    const Tp = state.pickEvery, T = state.flowT;
    const cyc = T / Tp, k = Math.floor(cyc), ph = (cyc - k) * Tp;          // ph: seconds into the current pick cycle
    const lift = state.flow > 0 ? THREE.MathUtils.smoothstep(ph, 0.08, 0.32) : 0;     // front part leaves
    const adv = state.flow > 0 ? THREE.MathUtils.smoothstep(ph, 0.34, 0.62) : 1;      // queue steps forward
    let mi = 0;
    for (let q = 0; q < QN; q++) {
      const m = flow[mi++]; m.visible = state.flow > 0 || state.railFull;
      let z = RAIL_Z1 - (q + 1 - adv) * GAP; if (q === 0) z = RAIL_Z1;
      m.position.set(RAIL_X, RAIL_Y, z); m.rotation.set(0, 0, 0);
      if (q === 0 && state.flow > 0) { m.position.y += 75 * lift; m.visible = lift < 0.999; if (lift > 0) { m.position.z = RAIL_Z1; } if (ph > 0.34) { m.visible = true; m.position.y = RAIL_Y; m.position.z = RAIL_Z1 - (1 - adv) * GAP; } }
    }
    const uSpeed = 0.055; // helix revolutions of path per second (normalised u)
    for (let h = 0; h < HN; h++) {
      const m = flow[mi++]; const u = ((T * uSpeed + h / HN) % 1);
      m.visible = state.flow > 0 && u > 0.04 && u < 0.985;
      const p = helixPt(u); const p2 = helixPt(Math.min(1, u + 0.01));
      m.position.copy(p); m.position.y += 0.5; m.rotation.set(0, Math.atan2(p2.x - p.x, p2.z - p.z), 0);
      m.position.applyAxisAngle(new THREE.Vector3(0, 1, 0), bowlG.rotation.y).add(bowlG.position);
    }
    for (; mi < flow.length; mi++) flow[mi].visible = false;
    head.visible = state.head > 0.01 && showParts;
    if (head.visible) { const down = ph < 0.1 ? THREE.MathUtils.smoothstep(ph, -0.2, 0.1) : 1 - lift; head.position.set(RAIL_X, RAIL_Y + 10 + (1 - down) * 75 + 0, RAIL_Z1); if (ph >= 0.08) head.position.y = RAIL_Y + 10 + 75 * lift; if (ph > 0.32) head.position.y = RAIL_Y + 10 + 75 * (1 - THREE.MathUtils.smoothstep(ph, Tp - 0.25, Tp)); }
    const present = state.flow > 0 ? !(ph > 0.1 && ph < 0.6) : !!state.railFull;
    const fb = state.fibre * (present ? 1 : 0.15);
    beam.material.opacity = 0.85 * fb * (showParts ? 1 : 0); beamDot.material.opacity = fb * (showParts ? 1 : 0);
    // pile jiggle when vibrating
    for (const m of pile) { const j = v * 0.6; m.position.set(m.userData.p0.x + j * Math.sin(t * 40 + m.userData.p0.z), m.userData.p0.y + Math.abs(j * Math.sin(t * 46 + m.userData.p0.x)), m.userData.p0.z); }
    // rejected parts: climb, tip off, fall back to the pile
    rej.forEach((m, i) => {
      const cyc = 3.2; const lt = ((state.rejT + i * cyc / rej.length) % cyc) / cyc; m.visible = state.reject > 0.01 && e < 0.02;
      if (!m.visible) return; const u0 = 0.18 + i * 0.12; const climb = Math.min(lt / 0.6, 1); const p = helixPt(u0 * climb);
      if (lt < 0.6) { m.position.copy(p); m.rotation.set(Math.PI / 2, 0, 0.6); m.material.emissiveIntensity = 0.25 * state.reject; }
      else { const f = (lt - 0.6) / 0.4; const pr = helixPt(u0); const c = new THREE.Vector3(pr.x * 0.45, BOWL_FLOOR + 6, pr.z * 0.45); m.position.lerpVectors(pr, c, f); m.position.y += 30 * Math.sin(f * Math.PI) * 0.5; m.rotation.set(Math.PI / 2 + f * 3, f * 2, 0.6); m.material.emissiveIntensity = 0.9 * state.reject * (1 - f * 0.5); }
    });
    // air streaks
    air.forEach((m, i) => { const ph = ((t * 1.7 + i / air.length) % 1); m.position.set(RAIL_X + ((i % 3) - 1) * 5, RAIL_Y + 9 + (i % 2) * 3 + EXPLODE.rail[1] * e, RAIL_Z0 + 30 + ph * (RAIL_Z1 - RAIL_Z0 - 60) + EXPLODE.rail[2] * e); m.material.opacity = state.air * 0.55 * Math.sin(ph * Math.PI); });
    // vision cone + light
    fov.material.opacity = state.vision * 0.16 * (1 - e); fov.position.y = 901 + EXPLODE.cam[1] * e; fov.position.x = -113 + EXPLODE.cam[0] * e;
    meshes.light.material.emissive = new THREE.Color(0x00c2ad).multiplyScalar(0.25 + 0.9 * state.vision);
  }
  apply();

  const _v = new THREE.Vector3();
  function project(anchor, w, h) {
    _v.set(...anchor); _v.project(camera);
    return [(_v.x * 0.5 + 0.5) * w, (-_v.y * 0.5 + 0.5) * h, _v.z];
  }
  function setCamera(pos, target, fovDeg, w, h, shiftX = 0, shiftY = 0) {
    camera.fov = fovDeg; camera.aspect = w / h;
    camera.position.set(...pos); camera.up.set(0, 1, 0); camera.lookAt(new THREE.Vector3(...target));
    if (shiftX || shiftY) camera.setViewOffset(w, h, -shiftX * w, -shiftY * h, w, h); else camera.clearViewOffset();
    camera.updateProjectionMatrix();
  }
  function setSize(w, h, pr = 1) { renderer.setPixelRatio(pr); renderer.setSize(w, h, false); }
  function render() { renderer.render(scene, camera); }
  return { THREE, renderer, scene, camera, root, meshes, state, apply, render, setCamera, setSize, project, head, PATH_LEN };
}

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
export function orbit(target, dist, azDeg, elDeg) {
  const az = azDeg * Math.PI / 180, el = elDeg * Math.PI / 180;
  return [target[0] + dist * Math.cos(el) * Math.sin(az), target[1] + dist * Math.sin(el), target[2] + dist * Math.cos(el) * Math.cos(az)];
}
