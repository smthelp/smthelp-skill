/* SMT3D viewer — dependency-free WebGL 1 viewer for "smt3d-v1" packed models (scripts/pack_mesh.py).
   Rotate (drag), zoom (wheel / pinch), double-click reset, auto-rotate, material presets, lighting presets, explode.
   API: SMT3D.mount(el, data, opts) -> {setMaterial(name), setLight(name), setExplode(0..1), setAuto(bool), reset(), destroy()}
   Extension point: add entries to SMT3D.MATERIALS / SMT3D.LIGHTS before mount (see references/extension-points.md).
   (c) Southern Machinery — smthelp.com */
(function (G) {
  'use strict';
  var MATERIALS = {
    industrial: { spec: 0.55, shin: 48, alpha: 1, tint: [1, 1, 1], label: 'Industrial' },
    matte: { spec: 0.04, shin: 8, alpha: 1, tint: [1, 1, 1], label: 'Matte' },
    xray: { spec: 0.3, shin: 24, alpha: 0.28, tint: [0.55, 0.95, 1], label: 'X-ray' }
  };
  var LIGHTS = {
    studio: { amb: [0.34, 0.36, 0.38], l1: [0.4, 0.8, 0.5], c1: [0.95, 0.95, 0.95], l2: [-0.6, 0.2, -0.7], c2: [0.35, 0.42, 0.48], bg: [0.94, 0.96, 0.96], label: 'Studio' },
    warm: { amb: [0.36, 0.3, 0.26], l1: [0.6, 0.7, 0.3], c1: [1.0, 0.86, 0.68], l2: [-0.5, 0.3, -0.6], c2: [0.25, 0.3, 0.45], bg: [0.98, 0.95, 0.9], label: 'Warm' },
    top: { amb: [0.2, 0.22, 0.25], l1: [0.05, 1, 0.1], c1: [1, 1, 1], l2: [0, -1, 0], c2: [0.12, 0.2, 0.22], bg: [0.08, 0.13, 0.13], label: 'Top light' }
  };
  var VS = 'attribute vec3 p;attribute vec3 n;uniform mat4 mvp;uniform mat3 nm;uniform vec3 off;varying vec3 vn;varying vec3 vp;' +
    'void main(){vec3 q=p+off;vn=normalize(nm*n);vp=q;gl_Position=mvp*vec4(q,1.0);}';
  var FS = 'precision mediump float;varying vec3 vn;varying vec3 vp;uniform vec3 col;uniform vec3 amb;uniform vec3 l1;uniform vec3 c1;uniform vec3 l2;uniform vec3 c2;' +
    'uniform vec3 eye;uniform float spec;uniform float shin;uniform float alpha;uniform float hl;' +
    'void main(){vec3 N=normalize(vn);if(!gl_FrontFacing)N=-N;vec3 V=normalize(eye);' +
    'float d1=max(dot(N,l1),0.0);float d2=max(dot(N,l2),0.0);vec3 H=normalize(l1+V);float s=pow(max(dot(N,H),0.0),shin)*spec;' +
    'vec3 c=col*(amb+c1*d1+c2*d2)+c1*s;float rim=pow(1.0-max(dot(N,V),0.0),3.0)*hl;c+=vec3(0.95,0.72,0.29)*rim;gl_FragColor=vec4(c,alpha);}';

  function b64ToBytes(b) { var s = atob(b), u = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return u; }
  function gunzip(u) {
    if (!('DecompressionStream' in G)) return Promise.reject(new Error('DecompressionStream unsupported'));
    var ds = new DecompressionStream('gzip'), w = ds.writable.getWriter(); w.write(u); w.close();
    return new Response(ds.readable).arrayBuffer();
  }
  function decode(data) {
    return gunzip(b64ToBytes(data.pos)).then(function (buf) {
      var q = new Int16Array(buf), n = q.length / 3, P = new Float32Array(q.length), N = new Float32Array(q.length);
      var mn = data.min, mx = data.max, c = [(mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, (mn[2] + mx[2]) / 2];
      for (var i = 0; i < q.length; i++) { var k = i % 3; P[i] = (q[i] + 32767) / 65534 * (mx[k] - mn[k]) + mn[k] - c[k]; }
      for (var t = 0; t < n; t += 3) {
        var o = t * 3, ax = P[o + 3] - P[o], ay = P[o + 4] - P[o + 1], az = P[o + 5] - P[o + 2], bx = P[o + 6] - P[o], by = P[o + 7] - P[o + 1], bz = P[o + 8] - P[o + 2];
        var nx = ay * bz - az * by, ny = az * bx - ax * bz, nz = ax * by - ay * bx, l = Math.sqrt(nx * nx + ny * ny + nz * nz) || 1;
        for (var v = 0; v < 3; v++) { N[o + v * 3] = nx / l; N[o + v * 3 + 1] = ny / l; N[o + v * 3 + 2] = nz / l; }
      }
      var parts = data.parts.map(function (pt) {
        var sx = 0, sy = 0, sz = 0; for (var j = pt.start; j < pt.start + pt.count; j++) { sx += P[j * 3]; sy += P[j * 3 + 1]; sz += P[j * 3 + 2]; }
        return { name: pt.name, color: pt.color, start: pt.start, count: pt.count, c: [sx / pt.count, sy / pt.count, sz / pt.count] };
      });
      return { P: P, N: N, parts: parts, r: Math.hypot(mx[0] - mn[0], mx[1] - mn[1], mx[2] - mn[2]) / 2 };
    });
  }
  function persp(f, a, n, fa) { var t = 1 / Math.tan(f / 2); return [t / a, 0, 0, 0, 0, t, 0, 0, 0, 0, (fa + n) / (n - fa), -1, 0, 0, 2 * fa * n / (n - fa), 0]; }
  function mul(a, b) { var o = new Array(16); for (var i = 0; i < 4; i++) for (var j = 0; j < 4; j++) { var s = 0; for (var k = 0; k < 4; k++) s += a[k * 4 + j] * b[i * 4 + k]; o[i * 4 + j] = s; } return o; }
  function view(yaw, pitch, dist) {
    var cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
    var R = [cy, sy * sp, -sy * cp, 0, 0, cp, sp, 0, sy, -cy * sp, cy * cp, 0, 0, 0, -dist, 1];
    return R;
  }

  function mount(el, data, opts) {
    opts = opts || {};
    var cv = document.createElement('canvas'); cv.className = 'smt3d-canvas'; cv.style.cssText = 'width:100%;height:100%;display:block;touch-action:none;cursor:grab';
    el.appendChild(cv);
    var gl = cv.getContext('webgl', { antialias: true, premultipliedAlpha: false, preserveDrawingBuffer: !!opts.preserve });
    if (!gl) { el.setAttribute('data-smt3d', 'nowebgl'); if (opts.onError) opts.onError(new Error('WebGL unavailable')); return null; }
    function sh(t, s) { var x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); return x; }
    var pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr); gl.useProgram(pr);
    var U = {}; ['mvp', 'nm', 'off', 'col', 'amb', 'l1', 'c1', 'l2', 'c2', 'eye', 'spec', 'shin', 'alpha', 'hl'].forEach(function (k) { U[k] = gl.getUniformLocation(pr, k); });
    var st = { yaw: opts.yaw != null ? opts.yaw : -0.7, pitch: opts.pitch != null ? opts.pitch : 0.38, zoom: 1, explode: 0, mat: opts.material || 'industrial', light: opts.light || 'studio', auto: opts.auto !== false, hl: 0, dirty: true, alive: true };
    var home = { yaw: st.yaw, pitch: st.pitch, zoom: 1 };
    var M = null, raf = 0, last = 0;
    decode(data).then(function (m) {
      M = m;
      var bp = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bp); gl.bufferData(gl.ARRAY_BUFFER, m.P, gl.STATIC_DRAW);
      var ap = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(ap); gl.vertexAttribPointer(ap, 3, gl.FLOAT, false, 0, 0);
      var bn = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bn); gl.bufferData(gl.ARRAY_BUFFER, m.N, gl.STATIC_DRAW);
      var an = gl.getAttribLocation(pr, 'n'); gl.enableVertexAttribArray(an); gl.vertexAttribPointer(an, 3, gl.FLOAT, false, 0, 0);
      el.setAttribute('data-smt3d', 'ready'); if (opts.onReady) opts.onReady(api); loop(0);
    }).catch(function (e) { el.setAttribute('data-smt3d', 'error'); if (opts.onError) opts.onError(e); });

    function draw() {
      var w = cv.clientWidth, h = cv.clientHeight, dpr = Math.min(G.devicePixelRatio || 1, opts.maxDpr || 2);
      if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
      gl.viewport(0, 0, cv.width, cv.height);
      var L = LIGHTS[st.light] || LIGHTS.studio, Mt = MATERIALS[st.mat] || MATERIALS.industrial;
      gl.clearColor(L.bg[0], L.bg[1], L.bg[2], opts.transparent ? 0 : 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      var dist = M.r * 1.9 / st.zoom, V = view(st.yaw, st.pitch, dist), Pm = persp(0.6, cv.width / Math.max(1, cv.height), M.r * 0.05, M.r * 10);
      gl.uniformMatrix4fv(U.mvp, false, new Float32Array(mul(Pm, V)));
      gl.uniformMatrix3fv(U.nm, false, new Float32Array([V[0], V[1], V[2], V[4], V[5], V[6], V[8], V[9], V[10]]));
      function nl(v) { var r = [V[0] * v[0] + V[4] * v[1] + V[8] * v[2], V[1] * v[0] + V[5] * v[1] + V[9] * v[2], V[2] * v[0] + V[6] * v[1] + V[10] * v[2]]; var l = Math.hypot(r[0], r[1], r[2]) || 1; return [r[0] / l, r[1] / l, r[2] / l]; }
      gl.uniform3fv(U.amb, L.amb); gl.uniform3fv(U.l1, nl(L.l1)); gl.uniform3fv(U.c1, L.c1); gl.uniform3fv(U.l2, nl(L.l2)); gl.uniform3fv(U.c2, L.c2);
      gl.uniform3fv(U.eye, [0, 0, 1]); gl.uniform1f(U.spec, Mt.spec); gl.uniform1f(U.shin, Mt.shin); gl.uniform1f(U.alpha, Mt.alpha); gl.uniform1f(U.hl, st.hl);
      gl.enable(gl.DEPTH_TEST);
      if (Mt.alpha < 1) { gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.depthMask(false); gl.disable(gl.CULL_FACE); }
      else { gl.disable(gl.BLEND); gl.depthMask(true); }
      for (var i = 0; i < M.parts.length; i++) {
        var pt = M.parts[i], e = st.explode * 0.6;
        gl.uniform3fv(U.off, [pt.c[0] * e, pt.c[1] * e, pt.c[2] * e]);
        gl.uniform3fv(U.col, [pt.color[0] * Mt.tint[0], pt.color[1] * Mt.tint[1], pt.color[2] * Mt.tint[2]]);
        gl.drawArrays(gl.TRIANGLES, pt.start, pt.count);
      }
      gl.depthMask(true);
    }
    function loop(ts) {
      if (!st.alive) return;
      var dt = last ? Math.min(0.05, (ts - last) / 1000) : 0; last = ts;
      if (st.auto && !drag && visible) { st.yaw += dt * (opts.autoSpeed || 0.35); st.dirty = true; }
      if (M && st.dirty && visible) { draw(); st.dirty = false; }
      raf = requestAnimationFrame(loop);
    }
    var visible = true;
    if ('IntersectionObserver' in G) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; st.dirty = true; }).observe(el);
    var drag = null, pinch = null, ptrs = {};
    cv.addEventListener('pointerdown', function (e) { cv.setPointerCapture(e.pointerId); ptrs[e.pointerId] = [e.clientX, e.clientY]; drag = [e.clientX, e.clientY]; cv.style.cursor = 'grabbing'; if (opts.onInteract) opts.onInteract(); });
    cv.addEventListener('pointermove', function (e) {
      if (!ptrs[e.pointerId]) return; ptrs[e.pointerId] = [e.clientX, e.clientY];
      var ids = Object.keys(ptrs);
      if (ids.length === 2) { var a = ptrs[ids[0]], b = ptrs[ids[1]], d = Math.hypot(a[0] - b[0], a[1] - b[1]); if (pinch) zoomBy(d / pinch); pinch = d; return; }
      if (!drag) return; st.yaw += (e.clientX - drag[0]) * 0.008; st.pitch = Math.max(-1.45, Math.min(1.45, st.pitch + (e.clientY - drag[1]) * 0.006)); drag = [e.clientX, e.clientY]; st.dirty = true;
    });
    function up(e) { delete ptrs[e.pointerId]; pinch = null; if (!Object.keys(ptrs).length) { drag = null; cv.style.cursor = 'grab'; } }
    cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up);
    function zoomBy(k) { st.zoom = Math.max(0.5, Math.min(6, st.zoom * k)); st.dirty = true; }
    cv.addEventListener('wheel', function (e) { e.preventDefault(); zoomBy(Math.exp(-e.deltaY * 0.0012)); }, { passive: false });
    cv.addEventListener('dblclick', function () { api.reset(); });
    var api = {
      setMaterial: function (n) { if (MATERIALS[n]) { st.mat = n; st.dirty = true; } },
      setLight: function (n) { if (LIGHTS[n]) { st.light = n; st.dirty = true; } },
      setExplode: function (v) { st.explode = Math.max(0, Math.min(1, +v)); st.dirty = true; },
      setHighlight: function (v) { st.hl = +v; st.dirty = true; },
      setAuto: function (v) { st.auto = !!v; },
      zoom: zoomBy,
      setView: function (yaw, pitch, zoom) { st.yaw = yaw; st.pitch = pitch; if (zoom) st.zoom = zoom; st.dirty = true; },
      reset: function () { st.yaw = home.yaw; st.pitch = home.pitch; st.zoom = home.zoom; st.explode = 0; st.dirty = true; },
      render: function () { if (M) draw(); },
      state: st,
      destroy: function () { st.alive = false; cancelAnimationFrame(raf); el.removeChild(cv); }
    };
    return api;
  }
  G.SMT3D = { mount: mount, MATERIALS: MATERIALS, LIGHTS: LIGHTS, version: '1.0.0' };
})(window);
