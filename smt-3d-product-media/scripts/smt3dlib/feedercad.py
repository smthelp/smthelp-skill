"""Real feeder CAD models on the rear feeding platform (v1.4).
props.feeder_cad = {
  "models": {"mvf": {"file": "inputs/mvf01.STEP" | ".glb",   # converted once to work/feeder_<key>.glb
                     "fwd": "-x",          # model axis that points from the feeder toward the head (part outlet side)
                     "up": "z",            # model axis that points up
                     "max_body_faces": 20000,   # heavier bodies drawn as their convex hull (render speed)
                     "min_body": 0.004,         # bodies smaller than this (m, longest edge) are dropped (screws)
                     "color": [r, g, b]}},      # optional: replaces the CAD colour of every body
  "items": [{"model": "mvf", "out": [x, y, ztop], "vib": 0.0004, "label": "head 1"}],
            # out = outlet end of the feeder: x centre, y of the outlet face, z of the feeder top (machine coords, m)
            # vib = vibration amplitude along the feed direction (m), 0 = still
  "hide_bowls": true                       # props.bowls are not drawn (hide their stands with scene.hide)
}
The feeder is turned so its 'fwd' axis points to +y (from the rear platform toward the heads) and 'up' to +z."""
import os, numpy as np

AX = {"x": 0, "y": 1, "z": 2}

def _axis(s):
    v = np.zeros(3); v[AX[s[-1]]] = -1.0 if s.startswith("-") else 1.0; return v

class FeederCad:
    def __init__(self, job):
        import trimesh
        self.job = job; c = job["props"]["feeder_cad"]; self.cfg = c; self.models = {}
        for key, m in c["models"].items():
            src = job.path(m["file"]); glb = src if src.lower().endswith(".glb") else job.work(f"feeder_{key}.glb")
            if not os.path.exists(glb):
                import cascadio; cascadio.step_to_glb(src, glb)
            sc = trimesh.load(glb); f = _axis(m.get("fwd", "x")); u = _axis(m.get("up", "z"))
            R = np.vstack([np.cross(f, u), f, u])   # rows: world x, y, z expressed in model axes
            Vs, Fs, Cs, off = [], [], [], 0
            for n in sc.graph.nodes_geometry:
                T, g = sc.graph[n]; mesh = sc.geometry[g]
                V = trimesh.transform_points(mesh.vertices, T); F = np.asarray(mesh.faces, np.int64)
                if (V.max(0) - V.min(0)).max() < m.get("min_body", 0.004): continue
                if len(F) > m.get("max_body_faces", 20000):
                    h = trimesh.Trimesh(V, F, process=False).convex_hull; V, F = np.asarray(h.vertices), np.asarray(h.faces, np.int64)
                if m.get("color"): col = np.array(m["color"], float)
                else:
                    try: col = np.array(mesh.visual.material.baseColorFactor[:3], float) / 255.0
                    except Exception: col = np.array([0.7, 0.7, 0.7])
                Vs.append(V @ R.T); Fs.append(F + off); Cs.append(np.repeat(col[None], len(F), 0)); off += len(V)
            V = np.vstack(Vs); lo, hi = V.min(0), V.max(0)
            V = V - np.array([(lo[0] + hi[0]) / 2, hi[1], hi[2]])   # origin: outlet face centre (x), outlet y, top z
            self.models[key] = (V, np.vstack(Fs), np.vstack(Cs))

    def size(self, key):
        V = self.models[key][0]; return (V.max(0) - V.min(0)).tolist()

    def meshes(self, t, explode=None):
        out = []
        for i, it in enumerate(self.cfg["items"]):
            V, F, C = self.models[it["model"]]
            o = np.asarray(it["out"], float).copy()
            a = it.get("vib", 0.0004)
            if a: o[1] += a * np.sin(t * 2 * np.pi * 9.0 + i)
            if explode is not None: o = o + explode.get(f"F{i}", 0)
            out.append((V + o, F, C))
        return out
