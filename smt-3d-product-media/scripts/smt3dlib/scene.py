"""CAD -> GLB -> parts -> motion groups (all driven by job['scene']).

Part selectors (used by groups, copies, hide, logos), all keys optional, ALL given keys must match:
  nums: [int]            node number (digits of the node id before '_', e.g. NAUO84_1 -> 84)
  ranges: [[a, b]]       node number within any inclusive range
  node_prefix: "NAUO84"  node id startswith
  name_contains: "logo"  part (body) name contains, case-insensitive
  box: [[x0,y0,z0],[x1,y1,z1]]   part bounding box fully inside (animation coords, metres)
  any: [selector, ...]   OR of sub-selectors;  not: selector
"""
import csv, json, os, subprocess, sys
import numpy as np
from .job import SKILL as JOBSKILL

def convert(job, force=False):
    """STEP/STP/IGES -> GLB via cascadio (OpenCascade). GLB/GLTF/OBJ/STL used as-is."""
    src = job.path(job["model"]["cad"]); ext = os.path.splitext(src)[1].lower()
    if ext in (".glb", ".gltf", ".obj", ".stl", ".ply"): return src
    glb = job.work("model.glb")
    if os.path.exists(glb) and not force and os.path.getmtime(glb) > os.path.getmtime(src): return glb
    import cascadio
    if ext in (".step", ".stp"):
        r = cascadio.step_to_glb(src, glb, tol_linear=0.3, tol_angular=0.5)
    elif ext in (".iges", ".igs") and hasattr(cascadio, "iges_to_glb"):
        r = cascadio.iges_to_glb(src, glb)
    else:
        raise SystemExit(f"C01 cannot convert {ext}: export STEP AP214 from the CAD tool")
    if not os.path.exists(glb): raise SystemExit(f"C02 conversion failed ({r}) for {src}")
    return glb

def _dec(s):
    for enc in ("latin1", "cp1252"):
        try: return s.encode(enc).decode("gbk")
        except Exception: pass
    return s

def _num(node):
    d = "".join(ch for ch in node.split("_")[0] if ch.isdigit())
    return int(d) if d else -1

def load_parts(job):
    import trimesh
    glb = convert(job)
    sc = trimesh.load(glb)
    ax = np.array(job["model"]["axis"], float) * float(job["model"]["scale"])
    flipw = np.prod(np.sign(ax)) < 0
    parts = []
    for node in sc.graph.nodes_geometry:
        T, g = sc.graph[node]; m = sc.geometry[g]
        V = trimesh.transform_points(m.vertices, T).astype(np.float64) * ax
        F = np.asarray(m.faces, np.int64)
        if flipw: F = F[:, ::-1].copy()
        try: c = np.array(m.visual.material.baseColorFactor[:3], float) / 255.0
        except Exception: c = np.array([0.8, 0.8, 0.8])
        parts.append(dict(name=_dec(g), node=node, n=_num(node), V=V, F=F, color=c, b0=V.min(0), b1=V.max(0)))
    return parts

def match(p, sel):
    if not sel: return False
    if "any" in sel and not any(match(p, s) for s in sel["any"]): return False
    if "not" in sel and match(p, sel["not"]): return False
    if "nums" in sel and p["n"] not in sel["nums"]: return False
    if "ranges" in sel and not any(a <= p["n"] <= b for a, b in sel["ranges"]): return False
    if "node_prefix" in sel and not p["node"].startswith(sel["node_prefix"]): return False
    if "name_contains" in sel and sel["name_contains"].lower() not in p["name"].lower(): return False
    if "box" in sel:
        lo, hi = np.array(sel["box"][0]), np.array(sel["box"][1])
        if not (np.all(p["b0"] >= lo - 1e-4) and np.all(p["b1"] <= hi + 1e-4)): return False
    return True

def _cp(p, off, tag=None):
    off = np.asarray(off, float); q = dict(p)
    q["V"] = p["V"] + off; q["b0"] = p["b0"] + off; q["b1"] = p["b1"] + off
    if tag: q["name"] = tag
    return q

def build_groups(job, parts):
    """returns dict group -> list of parts ('static' holds the rest)."""
    S = job["scene"]
    parts = [p for p in parts if not any(match(p, h) for h in S.get("hide", []))]
    groups = {k: [] for k in S["groups"]}; groups["static"] = []
    for p in parts:   # first matching group wins, in job order
        for k, sel in S["groups"].items():
            if match(p, sel): groups[k].append(p); break
        else: groups["static"].append(p)
    # duplicate whole motion groups (e.g. add heads 3 and 4 from heads 1 and 2)
    for c in S.get("copies", []):
        groups[c["as"]] = [_cp(p, c["offset"]) for p in groups[c["group"]]]
    # duplicate static sub-assemblies (head frames, bowls, tracks)
    add = []
    for c in S.get("static_copies", []):
        add += [_cp(p, c["offset"]) for p in groups["static"] if match(p, c["match"])]
    groups["static"] += add
    # logos: extra copies (e.g. move a logo from a hidden back face onto a visible front face)
    lg = S.get("logos", {}); extra = []
    for e in lg.get("extra", []):
        for p in parts:
            if match(p, e["match"]):
                for off in e["offsets"]: extra.append(_cp(p, off, "logo-extra-m" if e.get("premirror") else "logo-extra"))
    groups["static"] += extra
    # when the final image is mirrored (flip_x), pre-mirror every logo about its own centre so text reads correctly.
    # Extra copies are NOT pre-mirrored unless they say "premirror": true (a back-face logo copied to the front face
    # already appears mirrored from the camera, and the image flip turns it right again).
    if job["render"]["flip_x"] and lg.get("match"):
        for k, lst in groups.items():
            for i, p in enumerate(lst):
                if p["name"] == "logo-extra": continue
                if match(p, lg["match"]) or p["name"] == "logo-extra-m":
                    q = dict(p); V = p["V"].copy(); cx = (V[:, 0].min() + V[:, 0].max()) / 2
                    V[:, 0] = 2 * cx - V[:, 0]; q["V"] = V; q["F"] = p["F"][:, ::-1].copy(); lst[i] = q
    return groups

def recolor(job, C):
    pal = json.load(open(os.path.join(JOBSKILL, "config", "palettes.json"), encoding="utf-8"))
    rules = job["scene"]["palette"] if isinstance(job["scene"]["palette"], list) else pal[job["scene"]["palette"]]
    c = C.copy()
    for r in rules:
        # rules see the result of earlier rules (order matters)
        if "exact" in r: m = np.all(np.abs(c - np.array(r["exact"]) / 255.0) < r.get("tol", 0.02), axis=1)
        elif r.get("green"): m = (c[:, 1] > 0.85) & (c[:, 0] < 0.6) & ((c.max(1) - c.min(1)) > 0.4)
        elif r.get("red"): m = (c[:, 0] > 0.9) & (c[:, 1] < 0.3)
        else: continue
        c[m] = np.array(r["to"])
    return c

def merge(job, groups):
    M = {}
    for k, lst in groups.items():
        if not lst: M[k] = None; continue
        Vs, Fs, Cs, off = [], [], [], 0
        for p in lst:
            Vs.append(p["V"]); Fs.append(p["F"] + off); Cs.append(np.repeat(p["color"][None], len(p["F"]), 0)); off += len(p["V"])
        M[k] = [np.vstack(Vs), np.vstack(Fs), recolor(job, np.vstack(Cs))]
    return M

def inventory(job):
    """writes work/parts.csv (one row per CAD body) + prints group sizes: the starting point for writing scene.groups."""
    parts = load_parts(job); f = job.work("parts.csv")
    with open(f, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["n", "node", "name", "r", "g", "b", "x0", "y0", "z0", "x1", "y1", "z1", "faces"])
        for p in sorted(parts, key=lambda p: p["n"]):
            w.writerow([p["n"], p["node"], p["name"], *[int(v * 255) for v in p["color"]], *[f"{v:.4f}" for v in p["b0"]], *[f"{v:.4f}" for v in p["b1"]], len(p["F"])])
    allV = np.vstack([p["V"] for p in parts])
    info = {"parts": len(parts), "bbox": [allV.min(0).round(3).tolist(), allV.max(0).round(3).tolist()], "csv": f}
    if job["scene"]["groups"]:
        g = build_groups(job, parts); info["groups"] = {k: len(v) for k, v in g.items()}
    return info
