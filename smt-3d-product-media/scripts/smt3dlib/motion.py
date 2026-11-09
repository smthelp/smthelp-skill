"""Timeline, kinematics and camera for the working-principle animation.

Built-in kinematics "xy_table" (S70xx / PIN / terminal inserters): heads fixed in X/Y, the X/Y table carries the
PCB under each head; head presses down, clinch (anvil) rises under the board, bowls vibrate, pins flow on feed tracks.
Scene actions: idle | board_in | feed | insert | board_out.  A different machine type adds a plugin:
job.animation.plugin = "my_kinematics.py" exporting  state(t, job, ctx) -> dict  and optionally  extra_meshes(t, s, job, ctx).
"""
import importlib.util, os
import numpy as np

def ease(t): t = min(1.0, max(0.0, t)); return t * t * (3 - 2 * t)
def lerp(a, b, t): return np.asarray(a, float) * (1 - t) + np.asarray(b, float) * t

class Timeline:
    def __init__(self, job):
        self.job = job; self.scenes = job["animation"]["scenes"]
        self.start = np.cumsum([0] + [s["dur"] for s in self.scenes]); self.total = float(self.start[-1])
        self.ids = [s["id"] for s in self.scenes]
    def at(self, t):
        k = max(i for i in range(len(self.scenes)) if self.start[i] <= t or i == 0)
        k = min(k, len(self.scenes) - 1)
        return k, self.scenes[k], t - self.start[k]
    def first(self, action):
        for i, s in enumerate(self.scenes):
            if s.get("action") == action: return i
        return None

def _head_xy(P, h): return np.asarray(P["heads"][str(h)]["xy"], float)

def state_xy_table(t, job, tl):
    P = job["props"]; pcb = P.get("pcb") or {}
    heads = list(P["heads"].keys())
    s = dict(tab=np.zeros(2), board=None, on_table=False, inserted=0, hz={h: 0.0 for h in heads}, cz={h: 0.0 for h in heads},
             carry=None, t=t)
    k, sc, ts = tl.at(t); act = sc.get("action", "idle")
    i_in, i_ins, i_out = tl.first("board_in"), tl.first("insert"), tl.first("board_out")
    home = np.asarray(pcb.get("home", [0, 0]), float)
    # board position
    if pcb:
        if i_in is not None and k < i_in: s["board"] = None
        elif act == "board_in":
            s["board"] = lerp(pcb["enter_from"], home, ease(ts / (sc["dur"] * pcb.get("travel", 0.8))))
        elif act == "board_out":
            s["board"] = lerp(home, pcb["exit_to"], ease(ts / (sc["dur"] * pcb.get("travel", 0.875))))
        elif i_out is not None and k > i_out: s["board"] = None if pcb.get("hide_after_out", False) else np.asarray(pcb["exit_to"], float)
        else: s["board"] = home.copy()
        s["on_table"] = act in ("feed", "insert")
    allp = P.get("points", [])
    def rng(scn): a, b = scn.get("points", [0, len(allp)]); return int(a), int(min(b, len(allp)))
    s["bend"] = None
    if act == "insert" and allp:
        a0, b0 = rng(sc); pts = allp[a0:b0]   # v1.5: scene.points [a, b] = this scene inserts points a..b-1 (split insert over several scenes / cameras)
        ret = sc.get("return", 1.0); cyc = (sc["dur"] - ret) / max(1, len(pts))
        n = min(int(ts // cyc), len(pts) - 1) if ts < sc["dur"] - ret else len(pts) - 1
        ph = (ts - n * cyc) / cyc if ts < sc["dur"] - ret else 1.0
        u, v, h = pts[n]; h = str(h)
        tgt = _head_xy(P, h) - (home + np.array([u, v]))
        if n == 0:
            prev = np.zeros(2)
            if a0 > 0 and sc.get("from_prev", True):
                u0, v0, h0 = allp[a0 - 1]; prev = _head_xy(P, h0) - (home + np.array([u0, v0])) if not sc.get("return_prev", True) else np.zeros(2)
        else: prev = _head_xy(P, pts[n - 1][2]) - (home + np.array(pts[n - 1][:2]))
        s["tab"] = lerp(prev, tgt, ease(ph / 0.35))
        hp = P["heads"][h]
        press = np.sin((ph - 0.40) / 0.40 * np.pi) if 0.40 <= ph < 0.80 else 0.0
        s["hz"][h] = -hp.get("press", 0.024) * min(1.0, press * 1.6)
        s["cz"][h] = hp.get("clinch_lift", 0.012) if 0.5 <= ph < 0.85 else 0.0
        s["inserted"] = a0 + n + (1 if ph >= 0.6 else 0)
        s["bend"] = (a0 + n, min(1.0, max(0.0, (ph - 0.6) / 0.2)))   # leads of the part just inserted fold while the clinch is up
        s["carry"] = h if ph < 0.6 else None
        if ts >= sc["dur"] - ret:  # table returns home
            last = _head_xy(P, pts[-1][2]) - (home + np.array(pts[-1][:2]))
            s["tab"] = lerp(last, np.zeros(2), ease((ts - (sc["dur"] - ret)) / ret)); s["hz"] = {x: 0.0 for x in heads}; s["carry"] = None
            s["inserted"] = a0 + len(pts); s["bend"] = None
    elif i_ins is not None and k > i_ins:
        done = [rng(tl.scenes[i])[1] for i in range(k) if tl.scenes[i].get("action") == "insert"]
        s["inserted"] = max(done) if done else 0
    return s

def load_plugin(job):
    p = job["animation"].get("plugin")
    if not p: return None
    spec = importlib.util.spec_from_file_location("smt3d_plugin", job.path(p)); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m

def camera(t, job, tl):
    """scene.camera: {"eye": [from, to]} or {"orbit": {"center", "radius":[a,b], "angle":[a,b] deg, "height":[a,b]}},
    "target": [from, to], "fov": [a, b], "ease_time": s (default = scene dur), "sway": [ax, ay, az] (one sine over the scene).
    'from' may be "prev" = end of previous scene."""
    k, sc, ts = tl.at(t)
    def end_of(i, key):
        c = tl.scenes[i]["camera"]
        return _cam_eval(c, 1.0, tl, i)[key]
    c = sc["camera"]; u = ease(ts / c.get("ease_time", sc["dur"]))
    r = _cam_eval(c, u, tl, k)
    if "sway" in c: r["eye"] = r["eye"] + np.asarray(c["sway"]) * np.sin(ts / sc["dur"] * 2 * np.pi)
    return r["eye"], r["target"], r["fov"]

def _pair(v, tl, k, key):
    a, b = v
    if isinstance(a, str) and a == "prev": a = _cam_eval(tl.scenes[k - 1]["camera"], 1.0, tl, k - 1)[key]
    return a, b

def _cam_eval(c, u, tl, k):
    tg = _pair(c["target"], tl, k, "target") if "target" in c else None
    if "orbit" in c:
        o = c["orbit"]; ctr = np.asarray(o["center"], float)
        a = np.radians(lerp(*o["angle"], u)); rr = lerp(*o["radius"], u); hh = lerp(*o["height"], u)
        eye = ctr + np.array([rr * np.sin(a), rr * np.cos(a), hh]); target = ctr if tg is None else lerp(*tg, u)
    else:
        eye = lerp(*_pair(c["eye"], tl, k, "eye"), u); target = lerp(*tg, u)
    fv = c.get("fov", [40, 40]); fov = float(lerp(*_pair(fv, tl, k, "fov"), u)) if isinstance(fv, list) else float(fv)
    return {"eye": np.asarray(eye, float), "target": np.asarray(target, float), "fov": fov}
