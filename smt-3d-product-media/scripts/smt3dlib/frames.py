"""Render animation frames (resumable, splittable across workers) and stills.
Frames -> <out>/work/frames3d/fNNNNN.jpg ; stills -> <out>/stills/<name>.jpg"""
import os, sys, time
import numpy as np
from PIL import Image
from . import scene as SC, motion as MO
from .render import render, look_at

GOLD = np.array([0.86, 0.68, 0.22]); PCBC = np.array([0.10, 0.48, 0.25]); PADC = np.array([0.80, 0.70, 0.40])

class Renderer:
    def __init__(self, job):
        import trimesh; self.trimesh = trimesh
        self.job = job; self.tl = MO.Timeline(job)
        parts = SC.load_parts(job); self.groups = SC.build_groups(job, parts); self.M = SC.merge(job, self.groups)
        self.plugin = MO.load_plugin(job)
        R = job["render"]; self.W, self.H = R["width"], R["height"]

    def _box(self, cx, cy, z0, sx, sy, sz):
        m = self.trimesh.creation.box(extents=(sx, sy, sz)); m.apply_translation((cx, cy, z0 + sz / 2)); return m
    def _pin(self, x, y, z0, h=0.014, r=0.0018):
        """the inserted part: cylinder pin by default; props.part {"shape": "blade", "size": [w, t, h]} draws a flat terminal"""
        pt = self.job["props"].get("part") or {}
        if pt.get("shape") == "blade":
            w, th, hh = pt.get("size", [0.0048, 0.0008, 0.012]); k = h / 0.014
            return self._box(x, y, z0, w, th, hh * k)
        if pt.get("shape") == "eyelet":   # hollow rivet: tube + top flange; size [outer_d, length, flange_d]
            d, L, fd = (pt.get("size", [0.003, 0.0045, 0.0052]) + [0.0052])[:3]; k = h / 0.014; L = L * k
            tube = self.trimesh.creation.annulus(r_min=d * 0.32, r_max=d / 2, height=L, sections=14); tube.apply_translation((x, y, z0 + L / 2))
            fl = self.trimesh.creation.annulus(r_min=d * 0.32, r_max=fd / 2, height=0.0006, sections=18); fl.apply_translation((x, y, z0 + L + 0.0003))
            return self.trimesh.util.concatenate([tube, fl])
        m = self.trimesh.creation.cylinder(radius=r, height=h, sections=10); m.apply_translation((x, y, z0 + h / 2)); return m

    def meshes(self, t):
        J, M = self.job, self.M; P = J["props"]
        s = self.plugin.state(t, J, self) if self.plugin else MO.state_xy_table(t, J, self.tl)
        out = []; GOLD_ = np.array((P.get("part") or {}).get("color", GOLD))
        def add(key, off=(0, 0, 0)):
            m = M.get(key)
            if m is not None: out.append((m[0] + np.asarray(off, float), m[1], m[2]))
        add("static")
        dx, dy = s.get("tab", (0, 0))
        for k in J["animation"].get("x_groups", ["X"]): add(k, (dx, 0, 0))
        for k in J["animation"].get("y_groups", ["Y"]): add(k, (dx, dy, 0))
        for h, hp in P.get("heads", {}).items():
            if hp.get("group"): add(hp["group"], (0, 0, s.get("hz", {}).get(h, 0)))
            if hp.get("clinch_group"): add(hp["clinch_group"], (0, 0, s.get("cz", {}).get(h, 0)))
        for b in P.get("bowls", []):   # vibratory bowls: small oscillating twist about their own centre
            m = M.get(b["group"])
            if m is None: continue
            c = m[0].mean(0); a = np.radians(b.get("amp_deg", 0.6) * np.sin(t * b.get("speed", 37.0) * b.get("dir", 1)))
            Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
            out.append(((m[0] - c) @ Rz.T + c, m[1], m[2]))
        used = set(J["animation"].get("x_groups", ["X"]) + J["animation"].get("y_groups", ["Y"]) + ["static"] +
                   [hp.get("group") for hp in P.get("heads", {}).values()] + [hp.get("clinch_group") for hp in P.get("heads", {}).values()] +
                   [b["group"] for b in P.get("bowls", [])])
        for k in M:   # any other group is drawn static
            if k not in used: add(k)
        ex = []
        pcb = P.get("pcb")
        if pcb and s.get("board") is not None:
            bc = np.asarray(s["board"], float) + (np.array([dx, dy]) if s.get("on_table") else 0)
            top, th = pcb["top_z"], pcb.get("thickness", 0.0016)
            ex.append((self._box(bc[0], bc[1], top - th, pcb["size"][0], pcb["size"][1], th), np.array(pcb.get("color", PCBC))))
            for i, (u, v, h) in enumerate(P.get("points", [])):
                x, y = bc[0] + u, bc[1] + v
                if i < s.get("inserted", 0): ex.append((self._pin(x, y, top - 0.004, *P.get("pin", {}).get("hr", [0.014, 0.0018])), GOLD_))
                else: ex.append((self._box(x, y, top, 0.006, 0.006, 0.0004), PADC))
        if s.get("carry") is not None:
            hp = P["heads"][str(s["carry"])]; hx, hy = hp["xy"]
            ex.append((self._pin(hx, hy, hp.get("pin_z", 0.212) + s["hz"].get(str(s["carry"]), 0)), GOLD_))
        for tr in P.get("feed_tracks", []):   # parts flowing from bowl to head
            for j in range(tr.get("count", 4)):
                u = (t * tr.get("speed", 0.35) + j / tr.get("count", 4)) % 1
                ex.append((self._pin(tr["x"], lerp1(tr["y"][0], tr["y"][1], u), tr["z"], h=0.012, r=0.0022), GOLD_))
        if self.plugin and hasattr(self.plugin, "extra_meshes"): ex += self.plugin.extra_meshes(t, s, J, self)
        for m, col in ex: out.append((np.asarray(m.vertices), np.asarray(m.faces), col))
        return out

    def frame(self, t, cam=None):
        eye, tgt, fov = cam if cam else MO.camera(t, self.job, self.tl)
        R = self.job["render"]
        img = render(self.meshes(t), look_at(eye, tgt, (0, 0, 1)), self.W, self.H, fov_deg=fov, ss=R["supersample"],
                     bg=tuple(R["background"]), edges=R["edges"])
        return np.ascontiguousarray(img[:, ::-1]) if R["flip_x"] else img

def lerp1(a, b, u): return a * (1 - u) + b * u

def render_frames(job, worker=0, workers=1, limit=None):
    r = Renderer(job); fps = job["render"]["fps"]; d = job.wdir("frames3d")
    n = int(round(r.tl.total * fps)); t0 = time.time(); done = 0
    for i in range(worker, n, workers):
        fn = os.path.join(d, f"f{i:05d}.jpg")
        if os.path.exists(fn): continue
        Image.fromarray(r.frame(i / fps)).save(fn, quality=job["render"]["jpeg_quality"]); done += 1
        if limit and done >= limit: break
    have = len([f for f in os.listdir(d) if f.endswith(".jpg")])
    return {"worker": worker, "rendered": done, "have": have, "need": n, "seconds": round(time.time() - t0)}

def previews(job, times):
    """quick look: one contact sheet of frames at the given times -> work/preview.jpg"""
    r = Renderer(job); ims = [Image.fromarray(r.frame(float(t))).resize((640, 360)) for t in times]
    sheet = Image.new("RGB", (640 * min(3, len(ims)), 360 * ((len(ims) + 2) // 3)), "white")
    for i, im in enumerate(ims): sheet.paste(im, ((i % 3) * 640, (i // 3) * 360))
    f = job.work("preview.jpg"); sheet.save(f, quality=88); return f

def stills(job):
    """job.stills: [{"name", "t", "eye", "target", "fov", "width", "height"}] -> marketing / poster stills"""
    if not job.get("stills"): return []
    r = Renderer(job); out = []
    for s in job["stills"]:
        if s.get("width"): r.W, r.H = s["width"], s["height"]
        cam = (np.array(s["eye"], float), np.array(s["target"], float), s.get("fov", 35)) if "eye" in s else None
        f = job.out("stills", s["name"] + ".jpg"); os.makedirs(os.path.dirname(f), exist_ok=True)
        Image.fromarray(r.frame(s.get("t", 0.0), cam)).save(f, quality=94); out.append(f)
        r.W, r.H = job["render"]["width"], job["render"]["height"]
    return out
