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
        self.pcad = None
        if (job["props"].get("pcb") or {}).get("cad"):
            from .pcbcad import PcbCad; self.pcad = PcbCad(job)
        self.fcad = None
        if job["props"].get("feeder_cad"):
            from .feedercad import FeederCad; self.fcad = FeederCad(job)

    def _box(self, cx, cy, z0, sx, sy, sz):
        m = self.trimesh.creation.box(extents=(sx, sy, sz)); m.apply_translation((cx, cy, z0 + sz / 2)); return m
    def _part(self, head=None):
        """v1.6: heads[id].part overrides props.part, so each head can insert its own part type"""
        P = self.job["props"]; hp = (P.get("heads") or {}).get(str(head)) or {}
        return hp.get("part") or P.get("part") or {}

    @staticmethod
    def _below(pt):
        """depth of the part under the board top once seated: press_pin seats its shoulder flush, clip its collar flush"""
        sh, sz = pt.get("shape"), pt.get("size") or []
        if sh == "press_pin": D, L = sz[0], sz[1]; return L * pt.get("tail", 0.38)
        if sh == "clip": D, L = sz[0], sz[1]; return L - pt.get("proud", 0.0003)
        return 0.004

    def _pin(self, x, y, z0, h=0.014, r=0.0018, pt=None):
        """the inserted part: cylinder pin by default; props.part {"shape": "blade", "size": [w, t, h]} draws a flat terminal.
        v1.6 shapes: "press_pin" size [max_d, length] (tail + shoulder + body with open ring top, shoulder at tail*length),
        "clip" size [max_d, length] (collar ring on top, six spring fingers converging downward)."""
        pt = pt if pt is not None else (self.job["props"].get("part") or {})
        T = self.trimesh
        if pt.get("shape") == "press_pin":
            D, L = pt["size"][:2]; tl = L * pt.get("tail", 0.38); sh = max(L * 0.06, 0.0004)
            tail = T.creation.cylinder(radius=D * 0.3, height=tl, sections=12); tail.apply_translation((x, y, z0 + tl / 2))
            tip = T.creation.cone(radius=D * 0.3, height=D * 0.35, sections=12); tip.apply_transform(T.transformations.rotation_matrix(np.pi, (1, 0, 0))); tip.apply_translation((x, y, z0))
            col = T.creation.cylinder(radius=D * 0.5, height=sh, sections=16); col.apply_translation((x, y, z0 + tl + sh / 2))
            bl = L - tl - sh; body = T.creation.annulus(r_min=D * 0.18, r_max=D * 0.36, height=bl, sections=14); body.apply_translation((x, y, z0 + tl + sh + bl / 2))
            return T.util.concatenate([tail, tip, col, body])
        if pt.get("shape") == "clip":
            D, L = pt["size"][:2]; ch = max(L * 0.22, 0.0003)
            col = T.creation.annulus(r_min=D * 0.3, r_max=D / 2, height=ch, sections=16); col.apply_translation((x, y, z0 + L - ch / 2))
            parts = [col]
            for k in range(6):
                a = k * np.pi / 3; ca, sa = np.cos(a), np.sin(a)
                p0 = np.array([x + ca * D * 0.4, y + sa * D * 0.4, z0 + L - ch]); p1 = np.array([x + ca * D * 0.18, y + sa * D * 0.18, z0])
                parts.append(self._seg(p0, p1, D * 0.07))
            return T.util.concatenate(parts)
        if pt.get("shape") == "blade":
            w, th, hh = pt.get("size", [0.0048, 0.0008, 0.012]); k = h / 0.014
            return self._box(x, y, z0, w, th, hh * k)
        if pt.get("shape") == "eyelet":   # hollow rivet: tube + top flange; size [outer_d, length, flange_d]
            d, L, fd = (pt.get("size", [0.003, 0.0045, 0.0052]) + [0.0052])[:3]; k = h / 0.014; L = L * k
            tube = self.trimesh.creation.annulus(r_min=d * 0.32, r_max=d / 2, height=L, sections=14); tube.apply_translation((x, y, z0 + L / 2))
            fl = self.trimesh.creation.annulus(r_min=d * 0.32, r_max=fd / 2, height=0.0006, sections=18); fl.apply_translation((x, y, z0 + L + 0.0003))
            return self.trimesh.util.concatenate([tube, fl])
        m = self.trimesh.creation.cylinder(radius=r, height=h, sections=10); m.apply_translation((x, y, z0 + h / 2)); return m

    def _ring(self, x, y, top, d):
        """v1.6: plated-hole pad (annular ring) on a bare board, d = finished hole diameter"""
        m = self.trimesh.creation.annulus(r_min=d / 2, r_max=d / 2 + 0.0008, height=0.0002, sections=16); m.apply_translation((x, y, top + 0.0001)); return m

    def _seg(self, a, b, r):
        return self.trimesh.creation.cylinder(radius=r, segment=[np.asarray(a, float), np.asarray(b, float)], sections=8)

    def explode_offsets(self, t):
        """scene.explode {"groups": {group: [dx,dy,dz]}, "curve": out|in|hold|outin, "ramp": s} -> exploded / teardown view"""
        k, sc, ts = self.tl.at(t); e = sc.get("explode")
        if not e: return {}
        d = sc["dur"]; r = e.get("ramp", d * 0.35); cv = e.get("curve", "outin")
        if cv == "out": a = MO.ease(ts / r)
        elif cv == "in": a = 1 - MO.ease((ts - (d - r)) / r)
        elif cv == "hold": a = 1.0
        else: a = MO.ease(ts / r) * (1 - MO.ease((ts - (d - r)) / r))
        return {g: np.asarray(v, float) * a for g, v in e.get("groups", {}).items()}

    def meshes(self, t):
        J, M = self.job, self.M; P = J["props"]
        s = self.plugin.state(t, J, self) if self.plugin else MO.state_xy_table(t, J, self.tl)
        out = []; GOLD_ = np.array((P.get("part") or {}).get("color", GOLD))
        EX = self.explode_offsets(t)
        _, scn, _ = self.tl.at(t); cut = scn.get("cut")   # v1.5: scene.cut {"box": [[x0,y0,z0],[x1,y1,z1]], "keep": [groups]} = cutaway for close-ups
        def add(key, off=(0, 0, 0)):
            m = M.get(key)
            if m is None: return
            V = m[0] + np.asarray(off, float) + EX.get(key, 0); Fc = m[1]; Cc = m[2]
            if cut and key not in cut.get("keep", []):
                lo, hi = np.asarray(cut["box"][0], float), np.asarray(cut["box"][1], float); c = V[Fc].mean(1)
                ok = ~np.all((c > lo) & (c < hi), axis=1)
                if not ok.all(): Fc = Fc[ok]; Cc = Cc[ok] if np.ndim(Cc) == 2 and len(Cc) == len(m[1]) else Cc
            out.append((V, Fc, Cc))
        add("static")
        dx, dy = s.get("tab", (0, 0))
        for k in J["animation"].get("x_groups", ["X"]): add(k, (dx, 0, 0))
        for k in J["animation"].get("y_groups", ["Y"]): add(k, (dx, dy, 0))
        for h, hp in P.get("heads", {}).items():
            if hp.get("group"): add(hp["group"], (0, 0, s.get("hz", {}).get(h, 0)))
            if hp.get("clinch_group"): add(hp["clinch_group"], (0, 0, s.get("cz", {}).get(h, 0)))
        if self.fcad:
            for V_, F_, c_ in self.fcad.meshes(t, EX): out.append((V_, F_, c_))
        for b in ([] if (P.get("feeder_cad") or {}).get("hide_bowls") else P.get("bowls", [])):   # vibratory bowls: small oscillating twist about their own centre
            m = M.get(b["group"])
            if m is None: continue
            c = m[0].mean(0); a = np.radians(b.get("amp_deg", 0.6) * np.sin(t * b.get("speed", 37.0) * b.get("dir", 1)))
            Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
            out.append(((m[0] - c) @ Rz.T + c + EX.get(b["group"], 0), m[1], m[2]))
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
            if self.pcad:
                cz = None
                if s.get("carry") is not None:
                    hp = P["heads"][str(s["carry"])]; cz = (min(s.get("inserted", 0), len(self.pcad.items) - 1), hp["xy"][0], hp["xy"][1], hp.get("pin_z", 0.212) + s["hz"].get(str(s["carry"]), 0))
                for V_, F_, c_ in self.pcad.meshes(bc, top, s.get("inserted", 0), cz): out.append((V_, F_, c_))
            else: ex.append((self._box(bc[0], bc[1], top - th, pcb["size"][0], pcb["size"][1], th), np.array(pcb.get("color", PCBC))))
            for i, (u, v, h) in enumerate([] if self.pcad else P.get("points", [])):
                x, y = bc[0] + u, bc[1] + v; pt = self._part(h)
                if i < s.get("inserted", 0):
                    if pt.get("shape") in ("press_pin", "clip"): ex.append((self._pin(x, y, top - self._below(pt), pt=pt), np.array(pt.get("color", GOLD_))))
                    else: ex.append((self._pin(x, y, top - 0.004, *P.get("pin", {}).get("hr", [0.014, 0.0018]), pt=pt), np.array(pt.get("color", GOLD_))))
                elif pt.get("hole"): ex.append((self._ring(x, y, top, pt["hole"]), PADC))
                else: ex.append((self._box(x, y, top, 0.006, 0.006, 0.0004), PADC))
        if s.get("carry") is not None and not self.pcad:
            hp = P["heads"][str(s["carry"])]; hx, hy = hp["xy"]
            pt = self._part(s["carry"]); ex.append((self._pin(hx, hy, hp.get("pin_z", 0.212) + s["hz"].get(str(s["carry"]), 0), pt=pt), np.array(pt.get("color", GOLD_))))
        for tr in P.get("feed_tracks", []):   # parts flowing from bowl / feeder outlet to head
            col = np.array(tr.get("color", GOLD_), float)
            if "from" in tr:   # v1.5: 3D transfer track {"from": [x,y,z], "to": [x,y,z], "rail": true, "part": [sx, sy, sz]}
                a_, b_ = np.asarray(tr["from"], float), np.asarray(tr["to"], float)
                if tr.get("rail", True): ex.append((self._seg(a_ - [0, 0, 0.004], b_ - [0, 0, 0.004], tr.get("rail_r", 0.0035)), np.array(tr.get("rail_color", [0.55, 0.58, 0.62]))))
                sx, sy, sz = tr.get("part", [0.006, 0.006, 0.006])
                for j in range(tr.get("count", 5)):
                    u = (t * tr.get("speed", 0.35) + j / tr.get("count", 5)) % 1; c_ = a_ * (1 - u) + b_ * u
                    ex.append((self._box(c_[0], c_[1], c_[2], sx, sy, sz), col))
                continue
            for j in range(tr.get("count", 4)):
                u = (t * tr.get("speed", 0.35) + j / tr.get("count", 4)) % 1
                ex.append((self._pin(tr["x"], lerp1(tr["y"][0], tr["y"][1], u), tr["z"], h=0.012, r=0.0022), GOLD_))
        cl = P.get("clinch_leads")
        if cl and self.pcad and pcb and s.get("board") is not None:   # v1.5: leads under the board, folded by the clinch
            bc = np.asarray(s["board"], float) + (np.array([dx, dy]) if s.get("on_table") else 0)
            bot = pcb["top_z"] - pcb.get("thickness", 0.0016); L = cl.get("length", 0.004); r = cl.get("radius", 0.0005)
            ang = np.radians(cl.get("angle_deg", 75)); keep = cl.get("straight", 0.0012); colL = np.array(cl.get("color", [0.85, 0.85, 0.88]))
            bend = s.get("bend")
            for i, it in enumerate(self.pcad.items[:s.get("inserted", 0)]):
                f = 1.0
                if bend and bend[0] == i: f = bend[1]
                cx, cy = bc[0] + it["at"][0] + it["cxy"][0], bc[1] + it["at"][1] + it["cxy"][1]
                ax = 0 if it["ext"][0] >= it["ext"][1] else 1; half = it["ext"][ax] * cl.get("span", 0.32)
                for sg in (-1, 1):
                    p0 = np.array([cx, cy, bot]); p0[ax] += sg * half
                    p1 = p0 - [0, 0, keep]; d = np.zeros(3); d[ax] = sg * np.sin(ang * f); d[2] = -np.cos(ang * f)
                    p2 = p1 + d * (L - keep)
                    ex.append((self._seg(p0, p1, r), colL)); ex.append((self._seg(p1, p2, r), colL))
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
