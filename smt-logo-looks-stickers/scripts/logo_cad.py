"""Logo CAD handling for smt-logo-looks-stickers.

STEP -> GLB (cascadio, same call as smt-3d-product-media scene.convert),
parts.csv inventory, and logo mesh loading with the brand colour override:
a logo STEP usually stores arbitrary SolidWorks appearance colours, so the
two bodies are re-coloured to the job's brand colours (green body vs teal
body, told apart by which STEP colour is greener).
"""
import csv, os
import numpy as np


def convert_step_to_glb(step_path, glb_path):
    """STEP/STP -> GLB via cascadio. Returns the GLB path."""
    import cascadio
    ext = os.path.splitext(step_path)[1].lower()
    if ext not in (".step", ".stp"):
        raise SystemExit(f"C01 cannot convert {ext}: export STEP AP214 from the CAD tool")
    if os.path.exists(glb_path) and os.path.getmtime(glb_path) > os.path.getmtime(step_path):
        return glb_path
    cascadio.step_to_glb(step_path, glb_path, tol_linear=0.3, tol_angular=0.5)
    if not os.path.exists(glb_path):
        raise SystemExit(f"C02 conversion failed for {step_path}")
    return glb_path


def load_parts(glb_path):
    """GLB -> list of parts {name, node, V, F, color} in raw CAD coords.
    No axis mapping here: orientation is applied once, in stand_upright.
    (Applying an axis map here AND the stand mapping double-transforms the
    logo and renders it mirrored/rotated — caught 2026-11-14.)"""
    import trimesh
    sc = trimesh.load(glb_path)
    parts = []
    for node in sc.graph.nodes_geometry:
        T, g = sc.graph[node]
        m = sc.geometry[g]
        V = trimesh.transform_points(m.vertices, T).astype(np.float64)
        F = np.asarray(m.faces, np.int64)
        try:
            c = np.array(m.visual.material.baseColorFactor[:3], float) / 255.0
        except Exception:
            c = np.array([0.8, 0.8, 0.8])
        parts.append(dict(name=g, node=node, V=V, F=F, color=c,
                          b0=V.min(0), b1=V.max(0)))
    return parts


def inventory(glb_path, csv_path):
    """Write parts.csv (one row per CAD body) and return {parts, bbox, csv}."""
    parts = load_parts(glb_path)
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "node", "name", "r", "g", "b", "x0", "y0", "z0", "x1", "y1", "z1", "faces"])
        for i, p in enumerate(sorted(parts, key=lambda p: p["node"])):
            w.writerow([i, p["node"], p["name"], *[int(v * 255) for v in p["color"]],
                        *[f"{v:.4f}" for v in p["b0"]], *[f"{v:.4f}" for v in p["b1"]], len(p["F"])])
    allV = np.vstack([p["V"] for p in parts])
    return {"parts": len(parts),
            "bbox": [allV.min(0).round(4).tolist(), allV.max(0).round(4).tolist()],
            "csv": csv_path}


def _hex_to_f(rgb_hex):
    h = rgb_hex.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)])


def stand_upright(parts, brand_green, brand_teal, thicken=1.0):
    """Stand the flat logo upright, centre it, scale width to 1.0, brand colours.

    Mapping (x,y,z) -> (-x, z, y): un-mirrors the SolidWorks Y-down export,
    keeps the top up, and puts the front face toward a +y camera.
    The greener STEP body -> brand green; the other body -> brand teal.
    Returns list of (V, F, color) meshes.
    """
    green = _hex_to_f(brand_green)
    teal = _hex_to_f(brand_teal)
    meshes = []
    for p in parts:
        V = np.empty_like(p["V"])
        V[:, 0] = -p["V"][:, 0]
        V[:, 1] = p["V"][:, 2]
        V[:, 2] = p["V"][:, 1]
        V[:, 0] -= (V[:, 0].min() + V[:, 0].max()) / 2
        V[:, 2] -= (V[:, 2].min() + V[:, 2].max()) / 2
        w = V[:, 0].max() - V[:, 0].min()
        V /= w
        if thicken != 1.0:
            V[:, 1] *= thicken
        col = green if p["color"][1] > 0.5 else teal
        meshes.append((V, p["F"], col))
    return meshes


def drop_zone(meshes, z_below=-0.085, x_below=-0.15):
    """Drop faces in a corner zone of the stood-up logo (face-centroid
    z < z_below AND x < x_below). Use for a small sub-line under the main
    wordmark, e.g. a 'SMT help.com' tagline that the clean logo does not
    carry. Values are in stood-up logo units (width 1.0). Check the first
    preview after setting them: the main wordmark must be untouched.
    SM logo values: z_below=-0.085, x_below=-0.15 (verified 2026-11-14)."""
    out = []
    for V, F, col in meshes:
        if not len(F):
            out.append((V, F, col))
            continue
        c = V[F].mean(axis=1)
        keep = ~((c[:, 2] < z_below) & (c[:, 0] < x_below))
        out.append((V, F[keep], col))
    return out


def mark_only(meshes, threshold=0.18, width=0.8):
    """Keep only the graphic mark (image-left part of the logo, face-centroid
    x > threshold), then re-centre and scale it to `width`.

    The mark sits on the image-left side, which is positive x after
    stand_upright; the text extends to negative x. Threshold 0.18 splits
    them at the gap between the mark and the first letter.
    """
    out = []
    for V, F, col in meshes:
        cx = V[F].mean(axis=1)[:, 0]
        out.append((V, F[cx > threshold], col))
    pts = np.vstack([V[F].reshape(-1, 3) for V, F, col in out if len(F)])
    cx0 = (pts[:, 0].min() + pts[:, 0].max()) / 2
    cz0 = (pts[:, 2].min() + pts[:, 2].max()) / 2
    w = pts[:, 0].max() - pts[:, 0].min()
    s = width / w
    res = []
    for V, F, col in out:
        V2 = V.copy()
        V2[:, 0] = (V2[:, 0] - cx0) * s
        V2[:, 2] = (V2[:, 2] - cz0) * s
        res.append((V2, F, col))
    return res
