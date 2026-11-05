#!/usr/bin/env python3
"""3D model parse + lightweight pass -> one small .glb for the landing page.

usage: python3 model_prep.py <input> <workdir> [--ratio 0.25] [--max-tri 150000] [--compress meshopt|draco|none] [--tex 1024]

Accepts: .glb .gltf .stl .obj .ply .off (trimesh); .step/.stp via FreeCAD or cadquery if installed;
         .fbx via assimp if installed; .pptx -> extracts embedded ppt/media/*.glb first.
Steps:   1 extract/convert to GLB   2 report (meshes, triangles, size, bbox)
         3 decimate meshes above --max-tri (fast-simplification)   4 gltf-transform optimize
           (dedup, prune, weld, texture resize to --tex, meshopt or draco)   5 write <workdir>/model.glb + model_report.json
Never invents geometry: if conversion fails it stops and says which tool is missing.
"""
import sys, os, json, zipfile, subprocess, shutil, argparse

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('workdir')
ap.add_argument('--ratio', type=float, default=0.25); ap.add_argument('--max-tri', type=int, default=150000)
ap.add_argument('--compress', default='meshopt'); ap.add_argument('--tex', type=int, default=1024)
a = ap.parse_args()
W = os.path.abspath(a.workdir); os.makedirs(W, exist_ok=True)
src = os.path.abspath(a.src); ext = src.rsplit('.', 1)[-1].lower()
raw = os.path.join(W, 'model_raw.glb')

def run(cmd):
    print('$', ' '.join(cmd)); r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stdout[-800:], r.stderr[-800:]); raise SystemExit('command failed: ' + cmd[0])
    return r.stdout

# 1 extract / convert
if ext == 'pptx':
    z = zipfile.ZipFile(src); g = [n for n in z.namelist() if n.lower().endswith(('.glb', '.gltf'))]
    if not g: raise SystemExit('no embedded 3D model in pptx (ppt/media/*.glb)')
    open(raw, 'wb').write(z.read(max(g, key=lambda n: z.getinfo(n).file_size))); print('extracted', g)
elif ext == 'glb':
    shutil.copy(src, raw)
elif ext in ('gltf', 'stl', 'obj', 'ply', 'off'):
    import trimesh
    trimesh.load(src, force='scene').export(raw)
elif ext in ('step', 'stp'):
    stl = os.path.join(W, 'model_raw.stl')
    if shutil.which('FreeCADCmd'):
        py = f"import Part,Mesh;s=Part.read(r'{src}');m=Mesh.Mesh(s.tessellate(0.5));m.write(r'{stl}')"
        run(['FreeCADCmd', '-c', py])
    else:
        try:
            import cadquery as cq
            cq.exporters.export(cq.importers.importStep(src), stl, tolerance=0.3)
        except ImportError:
            raise SystemExit('STEP needs FreeCADCmd or cadquery (pip install cadquery). Or export GLB/STL from the CAD tool.')
    import trimesh; trimesh.load(stl, force='scene').export(raw)
elif ext == 'fbx':
    if not shutil.which('assimp'): raise SystemExit('FBX needs assimp (apt install assimp-utils) or export GLB from the CAD tool.')
    run(['assimp', 'export', src, raw])
else:
    raise SystemExit('unsupported format: ' + ext)

# 2 report + 3 decimate
import trimesh
sc = trimesh.load(raw, force='scene')
tri0 = sum(len(g.faces) for g in sc.geometry.values() if hasattr(g, 'faces'))
rep = {'source': os.path.basename(src), 'meshes': len(sc.geometry), 'triangles_in': int(tri0), 'bytes_in': os.path.getsize(raw),
       'bbox_m': [round(float(x), 4) for x in sc.extents]}
if tri0 > a.max_tri:
    import fast_simplification, numpy as np
    for k, gm in list(sc.geometry.items()):
        if hasattr(gm, 'faces') and len(gm.faces) > 2000:
            gm.merge_vertices()  # CAD exports split vertices per face; merge first or decimation stalls
            v, f = fast_simplification.simplify(np.asarray(gm.vertices, dtype=np.float32), np.asarray(gm.faces), target_reduction=1 - a.ratio, agg=9)
            nm = trimesh.Trimesh(v, f, process=False); nm.visual = trimesh.visual.ColorVisuals(nm)
            try: nm.visual.face_colors = gm.visual.main_color
            except Exception: pass
            sc.geometry[k] = nm
    dec = os.path.join(W, 'model_dec.glb'); sc.export(dec); raw = dec
rep['triangles_after_decimate'] = int(sum(len(g.faces) for g in trimesh.load(raw, force='scene').geometry.values() if hasattr(g, 'faces')))

# 4 optimize with gltf-transform (npx), fallback = decimated file
out = os.path.join(W, 'model.glb')
if shutil.which('npx') and a.compress != 'none':
    cmd = ['npx', '-y', '@gltf-transform/cli@4', 'optimize', raw, out, '--texture-size', str(a.tex), '--compress', a.compress]
    try: run(cmd)
    except SystemExit: shutil.copy(raw, out); rep['note'] = 'gltf-transform failed, decimated file used'
else:
    shutil.copy(raw, out)
rep['bytes_out'] = os.path.getsize(out); rep['compress'] = a.compress
json.dump(rep, open(os.path.join(W, 'model_report.json'), 'w'), indent=1)
print(json.dumps(rep, indent=1))
