"""Vendored from smt-3d-product-media v1.7.0 (scripts/smt3dlib/render.py), unchanged.
Original: https://github.com/smthelp/smthelp-skill/tree/main/smt-3d-product-media
Minimal CPU renderer (numba z-buffer). load_scene() -> parts; render() -> RGB image.
Vendored so this skill renders a logo STEP without requiring the sibling skill.
If the upstream renderer changes, re-vendor it and bump the version note below.
Vendored-from: smt-3d-product-media 1.7.0.
"""
import numpy as np, trimesh
from numba import njit

def dec(s):
    for enc in ('latin1', 'cp1252'):
        try: return s.encode(enc).decode('gbk')
        except Exception: pass
    return s

def load_scene(path="model.glb"):
    sc = trimesh.load(path)
    parts = []
    for node in sc.graph.nodes_geometry:
        T, g = sc.graph[node]; m = sc.geometry[g]
        V = trimesh.transform_points(m.vertices, T).astype(np.float64)
        try: c = np.array(m.visual.material.baseColorFactor[:3], float) / 255.0
        except Exception: c = np.array([0.8, 0.8, 0.8])
        parts.append(dict(name=dec(g), node=node, V=V, F=np.asarray(m.faces, np.int64), color=c))
    return parts

def look_at(eye, target, up=(0, 0, 1)):
    eye = np.asarray(eye, float); target = np.asarray(target, float); up = np.asarray(up, float)
    f = target - eye; f /= np.linalg.norm(f)
    r = np.cross(f, up); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    M = np.eye(4); M[0, :3] = r; M[1, :3] = u; M[2, :3] = -f
    M[:3, 3] = -M[:3, :3] @ eye
    return M

@njit(cache=True)
def raster(P, Z, F, tri_col, tri_n, W, H, zbuf, cbuf, light1, light2, eyedir):
    nt = F.shape[0]
    for t in range(nt):
        i0, i1, i2 = F[t, 0], F[t, 1], F[t, 2]
        z0, z1, z2 = Z[i0], Z[i1], Z[i2]
        if z0 <= 0.01 or z1 <= 0.01 or z2 <= 0.01: continue
        x0, y0 = P[i0, 0], P[i0, 1]; x1, y1 = P[i1, 0], P[i1, 1]; x2, y2 = P[i2, 0], P[i2, 1]
        minx = int(max(0.0, np.floor(min(x0, min(x1, x2)))))
        maxx = int(min(W - 1.0, np.ceil(max(x0, max(x1, x2)))))
        miny = int(max(0.0, np.floor(min(y0, min(y1, y2)))))
        maxy = int(min(H - 1.0, np.ceil(max(y0, max(y1, y2)))))
        if minx > maxx or miny > maxy: continue
        area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if abs(area) < 1e-12: continue
        n0, n1, n2 = tri_n[t, 0], tri_n[t, 1], tri_n[t, 2]
        # two-sided: flip normal towards the camera
        if n0 * eyedir[0] + n1 * eyedir[1] + n2 * eyedir[2] > 0:
            n0, n1, n2 = -n0, -n1, -n2
        d1 = max(0.0, -(n0 * light1[0] + n1 * light1[1] + n2 * light1[2]))
        d2 = max(0.0, -(n0 * light2[0] + n1 * light2[1] + n2 * light2[2]))
        sh = 0.42 + 0.50 * d1 + 0.22 * d2
        cr = min(1.0, tri_col[t, 0] * sh); cg = min(1.0, tri_col[t, 1] * sh); cb = min(1.0, tri_col[t, 2] * sh)
        iz0, iz1, iz2 = 1.0 / z0, 1.0 / z1, 1.0 / z2
        for y in range(miny, maxy + 1):
            py = y + 0.5
            for x in range(minx, maxx + 1):
                px = x + 0.5
                w0 = ((x1 - px) * (y2 - py) - (x2 - px) * (y1 - py)) / area
                w1 = ((x2 - px) * (y0 - py) - (x0 - px) * (y2 - py)) / area
                w2 = 1.0 - w0 - w1
                if w0 < -1e-6 or w1 < -1e-6 or w2 < -1e-6: continue
                iz = w0 * iz0 + w1 * iz1 + w2 * iz2
                if iz > zbuf[y, x]:
                    zbuf[y, x] = iz
                    cbuf[y, x, 0] = cr; cbuf[y, x, 1] = cg; cbuf[y, x, 2] = cb

def render(meshes, view, W, H, fov_deg=35.0, bg=(0.94, 0.96, 0.97), ss=2, edges=True):
    """meshes: list of (V world Nx3, F, color rgb 0-1)"""
    w, h = W * ss, H * ss
    zbuf = np.zeros((h, w)); cbuf = np.zeros((h, w, 3)); cbuf[:] = bg
    f = 0.5 * h / np.tan(np.radians(fov_deg) / 2)
    R = view[:3, :3]; tvec = view[:3, 3]
    eyedir = np.array([0.0, 0.0, -1.0])
    light1 = R @ (np.array([-0.4, -0.6, -1.0]) / np.linalg.norm([-0.4, -0.6, -1.0]))
    light2 = R @ (np.array([0.7, 0.3, -0.4]) / np.linalg.norm([0.7, 0.3, -0.4]))
    for V, F, col in meshes:
        if len(F) == 0: continue
        Vc = V @ R.T + tvec
        Z = -Vc[:, 2]
        Zs = np.where(Z > 1e-6, Z, 1e-6)
        P = np.empty((len(V), 2)); P[:, 0] = w / 2 + f * Vc[:, 0] / Zs; P[:, 1] = h / 2 - f * Vc[:, 1] / Zs
        a = Vc[F[:, 1]] - Vc[F[:, 0]]; b = Vc[F[:, 2]] - Vc[F[:, 0]]
        n = np.cross(a, b); ln = np.linalg.norm(n, axis=1); ln[ln == 0] = 1; n /= ln[:, None]
        tc = np.repeat(np.asarray(col, float)[None], len(F), 0) if np.ndim(col) == 1 else col
        raster(P, Z, F, tc, n, w, h, zbuf, cbuf, light1, light2, eyedir)
    img = cbuf
    if edges:  # depth-discontinuity outlines for a CAD look
        d = np.where(zbuf > 0, 1.0 / np.maximum(zbuf, 1e-9), 1e3)
        gx = np.abs(np.diff(d, axis=1, append=d[:, -1:])); gy = np.abs(np.diff(d, axis=0, append=d[-1:, :]))
        e = np.maximum(gx, gy) / np.maximum(d, 1e-3)
        m = (e > 0.02).astype(float)[..., None]
        img = img * (1 - 0.55 * m)
    img = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    if ss > 1:
        img = img.reshape(H, ss, W, ss, 3).mean((1, 3)).astype(np.uint8)
    return img
