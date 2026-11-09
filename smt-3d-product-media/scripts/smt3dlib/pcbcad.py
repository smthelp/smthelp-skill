"""Real PCB / PCBA CAD model in the animation (v1.3).
props.pcb.cad = {
  "file": "inputs/board.STEP" | ".glb",       # converted once to work/pcb_cad.glb
  "array": [nx, ny], "gap": 0.004,              # panel of identical boards (machine min PCB is 80 x 80 mm)
  "rot_deg": 0, "flip": false,                  # extra in-plane rotation / flip board over
  "insert": [{"groups": ["NAUO18"], "head": "1"}, ...],   # parts the machine inserts (per board, in order)
  "absent": ["NAUO55"], "board_color": [0.08, 0.42, 0.22]                          # parts not yet on the board and not inserted here (optional)
}
Groups = STEP assembly instances (node name prefix before '_', e.g. NAUO18). `inspect-pcb` lists them with names.
The board body = the part with the largest footprint. It is laid flat (PCA), squared up (min-area rectangle),
centred, component side up, board top at local z = 0. Inserted parts appear when the head presses them in;
the carried part rides under the head. props.points is generated from the inserts (overrides the job's)."""
import os, json, numpy as np

def _num(node): return node.split('_')[0]

class PcbCad:
    def __init__(self, job):
        import trimesh
        self.job = job; c = job["props"]["pcb"]["cad"]; self.cfg = c
        src = job.path(c["file"]); glb = job.work("pcb_cad.glb")
        if src.lower().endswith(".glb"): glb = src
        elif not os.path.exists(glb):
            import cascadio; cascadio.step_to_glb(src, glb)
        sc = trimesh.load(glb); parts = []
        for n in sc.graph.nodes_geometry:
            T, g = sc.graph[n]; m = sc.geometry[g]
            try: col = np.array(m.visual.material.baseColorFactor[:3], float) / 255.0
            except Exception: col = np.array([0.7, 0.7, 0.7])
            parts.append(dict(node=n, name=g, grp=_num(n), V=trimesh.transform_points(m.vertices, T), F=np.asarray(m.faces, np.int64), col=col))
        b = max(parts, key=lambda p: np.prod(np.sort(p["V"].max(0) - p["V"].min(0))[1:]))
        V = b["V"]; c0 = V.mean(0); _, _, vt = np.linalg.svd(V - c0, full_matrices=False); n = vt[2]
        allv = np.vstack([p["V"] for p in parts if p is not b])
        if ((allv - c0) @ n).mean() < 0: n = -n
        if c.get("flip"): n = -n
        x = vt[0] - (vt[0] @ n) * n; x /= np.linalg.norm(x); R = np.vstack([x, np.cross(n, x), n])
        loc = lambda v: (v - c0) @ R.T
        bv = loc(V); best = None   # square up: min-area rectangle over 0..90 deg
        for a in np.radians(np.arange(0, 90, 0.5)):
            r = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]); q = bv[:, :2] @ r.T; e = q.max(0) - q.min(0)
            if best is None or e[0] * e[1] < best[0]: best = (e[0] * e[1], a)
        a = best[1] + np.radians(c.get("rot_deg", 0)); r2 = np.eye(3); r2[:2, :2] = [[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]
        R = r2 @ R; bv = loc(V); ctr = (bv.max(0) + bv.min(0)) / 2; ctr[2] = bv[:, 2].max()
        for p in parts: p["V"] = loc(p["V"]) - ctr
        self.board_grp = b["grp"]; self.size = (bv.max(0) - bv.min(0))[:2]
        self.groups = {}
        for p in parts: self.groups.setdefault(p["grp"], []).append(p)
        ins = c.get("insert", []); used = {g for e in ins for g in e["groups"]}; absent = set(c.get("absent", []))
        if c.get("board_color"):
            for p in self.groups[self.board_grp]:
                if p is b or len(self.groups[self.board_grp]) == 1 or np.prod(np.sort(p["V"].max(0) - p["V"].min(0))[1:]) > 0.5 * np.prod(self.size): p["col"] = np.array(c["board_color"], float)
        self.static = [(p["V"], p["F"], p["col"]) for g, ps in self.groups.items() if g not in used and g not in absent for p in ps]
        nx, ny = c.get("array", [1, 1]); gap = c.get("gap", 0.004); px, py = self.size + gap
        self.offsets = [np.array([(i - (nx - 1) / 2) * px, (j - (ny - 1) / 2) * py]) for j in range(ny) for i in range(nx)]
        self.items = []; pts = []
        for o in self.offsets:
            for e in ins:
                ms = [(p["V"], p["F"], p["col"]) for g in e["groups"] for p in self.groups[g]]
                allp = np.vstack([m[0] for m in ms]); cxy = (allp.max(0)[:2] + allp.min(0)[:2]) / 2
                self.items.append(dict(meshes=ms, at=o, cxy=cxy, zmin=allp[:, 2].min(), ext=allp.max(0)[:2] - allp.min(0)[:2]))
                pts.append([float(o[0] + cxy[0]), float(o[1] + cxy[1]), str(e["head"])])
        job["props"]["points"] = pts
        job["props"]["pcb"]["size"] = [float(nx * px), float(ny * py)]

    def meshes(self, bc, top, inserted, carry_xyz):
        out = []
        for o in self.offsets:
            t = np.array([bc[0] + o[0], bc[1] + o[1], top])
            out += [(V + t, F, col) for V, F, col in self.static]
        for i, it in enumerate(self.items):
            if i < inserted:
                t = np.array([bc[0] + it["at"][0], bc[1] + it["at"][1], top]); out += [(V + t, F, col) for V, F, col in it["meshes"]]
        if carry_xyz is not None:
            i, hx, hy, z = carry_xyz; it = self.items[i]
            t = np.array([hx - it["cxy"][0], hy - it["cxy"][1], z - it["zmin"]]); out += [(V + t, F, col) for V, F, col in it["meshes"]]
        return out

def inspect(job):
    """list PCB groups: id, part names, centre and size (mm) -> work/pcb_groups.csv"""
    P = PcbCad.__new__(PcbCad); job["props"]["pcb"]["cad"].setdefault("insert", [])
    PcbCad.__init__(P, job); rows = ["group,names,cx_mm,cy_mm,sx_mm,sy_mm,sz_mm,board"]
    for g, ps in sorted(P.groups.items(), key=lambda t: t[0]):
        v = np.vstack([p["V"] for p in ps]); lo, hi = v.min(0), v.max(0); c = (lo + hi) / 2 * 1000; s = (hi - lo) * 1000
        rows.append(f"{g},{'|'.join(sorted({p['name'] for p in ps}))},{c[0]:.1f},{c[1]:.1f},{s[0]:.1f},{s[1]:.1f},{s[2]:.1f},{int(g == P.board_grp)}")
    f = job.work("pcb_groups.csv"); open(f, "w").write("\n".join(rows)); return {"file": f, "board_mm": (P.size * 1000).round(1).tolist(), "groups": len(P.groups)}
