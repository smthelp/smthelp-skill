#!/usr/bin/env python3
"""Lightweight a 3D model for the single-HTML viewer.

usage: pack_mesh.py <mesh.json | model.stl|.obj|.glb|.gltf> <out model.b64> [--budget 120000] [--groups groups.json] [--depth 1]

- mesh.json comes from extract_mesh.py (eDrawings). STL/OBJ/GLB need `pip install trimesh` (optional).
- World-transform to mm, group bodies into parts (path element at --depth, or a groups.json {"Part name": ["substring", ...]}),
  vertex-cluster decimation down to the triangle budget, int16 quantization over the bounding box,
  gzip + base64.  Output is read by templates/landing/viewer3d.js (format "smt3d-v1").
"""
import sys, os, json, gzip, base64, argparse, colorsys
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--budget', type=int, default=120000)
ap.add_argument('--groups'); ap.add_argument('--depth', type=int, default=-1, help='-1 = one part per body (default)')
a = ap.parse_args()

parts = {}  # name -> list of (N,3,3) arrays
colors = {}
if a.src.endswith('.json'):
    for r in json.load(open(a.src)):
        p = np.array(r['pos'], dtype=np.float64).reshape(-1, 3)
        if len(p) < 3: continue
        M = np.array(r['mat'], dtype=np.float64).reshape(4, 4).T  # column-major -> row-major
        p = (np.c_[p, np.ones(len(p))] @ M.T)[:, :3] * 1000.0  # metres -> mm
        path = r.get('path') or ['part']
        if a.depth < 0:
            nm = next((x for x in reversed(path) if x and x.lower() not in ('instance', 'body')), 'part')
            name = f"{nm}#{r['id']}"
        else:
            name = path[min(a.depth, len(path) - 1)]
        parts.setdefault(name, []).append(p.reshape(-1, 3, 3))
        if r.get('col') and sum(r['col']) > 0 and name not in colors: colors[name] = r['col']
else:
    import trimesh
    sc = trimesh.load(a.src, force='scene')
    for nm, g in sc.geometry.items():
        tm = g.copy()
        try: tm.apply_transform(sc.graph.get(nm)[0])
        except Exception: pass
        parts.setdefault(nm, []).append(np.asarray(tm.triangles, dtype=np.float64))
if a.groups:
    G = json.load(open(a.groups)); merged = {}
    for name, arrs in parts.items():
        tgt = next((g for g, keys in G.items() if any(k.lower() in name.lower() for k in keys)), 'Other')
        merged.setdefault(tgt, []).extend(arrs)
    parts = merged

tris = {k: np.concatenate(v) for k, v in parts.items()}
total = sum(len(v) for v in tris.values())
allp = np.concatenate([v.reshape(-1, 3) for v in tris.values()])
lo, hi = allp.min(0), allp.max(0); ext = (hi - lo).max()
# vertex clustering decimation
cell = 0.0
if total > a.budget:
    cell = ext / 2000.0
    for _ in range(40):
        n = 0
        for v in tris.values():
            q = np.floor((v - lo) / cell).astype(np.int64).reshape(-1, 3, 3)
            ok = ~((q[:, 0] == q[:, 1]).all(1) | (q[:, 1] == q[:, 2]).all(1) | (q[:, 0] == q[:, 2]).all(1))
            n += ok.sum()
        if n <= a.budget: break
        cell *= 1.25
    for k, v in tris.items():
        q = np.floor((v - lo) / cell).reshape(-1, 3, 3)
        ok = ~((q[:, 0] == q[:, 1]).all(1) | (q[:, 1] == q[:, 2]).all(1) | (q[:, 0] == q[:, 2]).all(1))
        tris[k] = ((q[ok] + 0.5) * cell + lo)
# quantize
scale = (hi - lo); scale[scale == 0] = 1
out_parts = []; buf = []; off = 0
for i, (k, v) in enumerate(sorted(tris.items(), key=lambda kv: -len(kv[1]))):
    if len(v) == 0: continue
    q = np.round((v.reshape(-1, 3) - lo) / scale * 65534 - 32767).astype('<i2')
    buf.append(q.tobytes())
    c = colors.get(k) or [*colorsys.hsv_to_rgb(0.53, 0.06, 0.62 + 0.28 * ((i * 0.618) % 1))]  # aluminium greys
    c = [float(x) if max(c) <= 1 else float(x) / 255 for x in c]
    out_parts.append({'name': str(k), 'color': [round(x, 3) for x in c], 'start': off, 'count': len(v) * 3})
    off += len(v) * 3
raw = b''.join(buf)
payload = {'format': 'smt3d-v1', 'units': 'mm', 'min': lo.round(3).tolist(), 'max': hi.round(3).tolist(),
           'triangles': off // 3, 'source_triangles': int(total), 'cluster_mm': round(cell, 3), 'parts': out_parts,
           'pos': base64.b64encode(gzip.compress(raw, 9)).decode()}
s = json.dumps(payload, separators=(',', ':'))
open(a.out, 'w').write(s)
print(f"{len(out_parts)} parts, {total} -> {off//3} triangles, bbox {np.round(hi-lo,1).tolist()} mm, {len(s)/1e6:.2f} MB -> {a.out}")
