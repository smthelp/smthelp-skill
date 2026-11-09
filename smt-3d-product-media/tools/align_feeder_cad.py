#!/usr/bin/env python3
"""align_feeder_cad.py (1.7.0) - place multi-bowl feeder carts (STEP/GLB) so every track outlet sits at its head's pick-up point.

Use when a feeder CAD carries several bowls + linear tracks on one cart (e.g. Jason's "Vibration Bowl Feeder x2.STEP":
1 cart, 2 bowls, 2 tracks 41 mm apart) and the outlets must line up with heads that have a different pitch.
What it does, per cart:
  1. maps the CAD to machine coords (model lateral/up/fwd axes -> world x / z / y), mirrored on request;
  2. yaws each track's FRONT module (bodies past `junction_fwd`, minus shared plates) about its bowl-side junction so the
     seat lands exactly at (head_x, pick_y, pick_z) - the rear part and bowls stay as in the CAD;
  3. drops demo parts / hidden hardware, recolours (frame / bowls / feet), fills each bowl with its own customer part;
  4. writes ONE world-placed GLB + a JSON with each head's junction and seat point (feed back into the job).
In the job: props.feeder_cad = {"models": {"vbf": {"file": <glb>, "fwd": "y", "up": "z", "max_body_faces": 200000,
  "min_body": 0.001}}, "items": [{"model": "vbf", "out": [(bbox.lo.x+bbox.hi.x)/2, bbox.hi.y, bbox.hi.z], "vib": 0}],
  "hide_bowls": true} and props.feed_tracks from each head's junction->seat (+ seat->gripper along the head's own rail).
usage: align_feeder_cad.py config.json      (example: examples/feeder_align/vbf_x2_s7040p.json)
Lessons (S7040P v6, 2026-11-09):
  - the seat can NOT sit at the head xy: the X/Y table carries the board ~0.12 m behind the head; put the seat just behind
    the head's own feed-rail entry block (S7020: y -0.623, rail top z 0.269) -> pick = [-0.650, 0.269];
  - re-pitch heads to fit two outlets per cart (S7020 pair pitch 0.1 m) rather than bending tracks a lot (keep yaw < ~5 deg);
  - the cart may end below the machine base; say so (feet / stand to be matched on the real machine);
  - after re-pitching heads, re-check close-up insertion cameras: copied heads/table can block transitions."""
import json, sys, numpy as np, trimesh

def load(cfg):
    src = cfg["cad"]
    if src.lower().endswith((".step", ".stp")):
        import cascadio; out = cfg.get("glb_cache", src.rsplit(".", 1)[0] + ".glb")
        cascadio.step_to_glb(src, out, tol_linear=0.3, tol_angular=0.5); src = out
    s = trimesh.load(src); B = []
    for n in s.graph.nodes_geometry:
        T, g = s.graph[n]; m = s.geometry[g]
        B.append((g, trimesh.transform_points(m.vertices, T), np.asarray(m.faces, np.int64)))
    return B

def main(path):
    C = json.load(open(path)); ax = C.get("axes", {"lateral": 0, "up": 1, "fwd": 2})
    la, up, fw = ax["lateral"], ax["up"], ax["fwd"]
    TRK = C["tracks"]                         # {name: model lateral coord of the track centre}
    SEAT, JUNC, TOP = C["seat_fwd"], C["junction_fwd"], C["seat_top_up"]
    PY, PZ = C["pick"]                        # world y / z of the seat point (x comes from the head)
    shared = C.get("shared_keywords", []); drop = C.get("drop_keywords", []); minb = C.get("min_body", 0.006)
    split = C.get("track_split_lateral", sum(TRK.values()) / len(TRK))
    COL = {k: np.array(v) for k, v in C.get("colors", {}).items()}
    B = load(C)

    def front_of(g, V):
        lo, hi = V.min(0), V.max(0)
        if lo[fw] < JUNC - 0.01 or hi[up] < C.get("front_min_up", 0.0) or any(k in g for k in shared): return None
        c = (lo[la] + hi[la]) / 2; names = sorted(TRK, key=lambda t: TRK[t])
        return names[0] if c < split else names[-1]

    def colour(g):
        for k, kws in C.get("color_keywords", {}).items():
            if any(w in g for w in kws): return COL[k]
        return COL.get("frame", np.array([0.82, 0.84, 0.87]))

    meshes, info = [], {}
    for cart in C["carts"]:
        mir = cart.get("mirror", False); tg = cart["targets"]          # {track: head_x}
        sx = 1.0 if mir else -1.0; mid_m = sum(TRK.values()) / len(TRK); mid_w = sum(tg.values()) / len(tg)
        W = lambda P: np.c_[sx * (P[:, la] - mid_m) + mid_w, (P[:, fw] - SEAT) + PY, (P[:, up] - TOP) + PZ]
        yaw = {}
        for t, xm in TRK.items():
            p = np.zeros((2, 3)); p[:, la] = xm; p[:, up] = TOP; p[0, fw] = JUNC; p[1, fw] = SEAT
            j, s = W(p); a = np.arctan2(tg[t] - j[0], PY - j[1]) - np.arctan2(s[0] - j[0], s[1] - j[1]); yaw[t] = (j, a)
            info[cart["heads"][t]] = {"junction": j.tolist(), "seat": [tg[t], PY, PZ], "yaw_deg": float(np.degrees(a))}
        def Y(P, t):
            j, a = yaw[t]; c, s_ = np.cos(a), np.sin(a); d = P - j
            return np.c_[j[0] + c * d[:, 0] + s_ * d[:, 1], j[1] - s_ * d[:, 0] + c * d[:, 1], P[:, 2]]
        for g, V, F in B:
            if any(k in g for k in drop) or (V.max(0) - V.min(0)).max() < minb: continue
            P = W(V); t = front_of(g, V)
            if t: P = Y(P, t)
            meshes.append((P, F[:, ::-1] if mir else F, colour(g)))
        rng = np.random.default_rng(cart.get("seed", 7))
        for f in cart.get("fill", []):                                   # parts lying in a bowl
            cx, cf = f["center"]; d, L = f["d"], f["L"]; ms = []
            for _ in range(f.get("count", 70)):
                r = f["r"] * np.sqrt(rng.random()); a = rng.random() * 2 * np.pi
                m = (trimesh.creation.cylinder(radius=d / 2, height=L, sections=8) if f.get("shape", "pin") == "pin"
                     else trimesh.creation.annulus(r_min=d * 0.3, r_max=d / 2, height=L, sections=10))
                m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [np.cos(rng.random() * 6.3), np.sin(rng.random() * 6.3), 0]))
                p = np.zeros((1, 3)); p[0, la] = cx + r * np.cos(a); p[0, fw] = cf + r * np.sin(a); p[0, up] = f["floor_up"]
                m.apply_translation(W(p)[0] + [0, 0, d / 2]); ms.append(m)
            m = trimesh.util.concatenate(ms); meshes.append((np.asarray(m.vertices), np.asarray(m.faces, np.int64), np.array(f["color"])))
    sc = trimesh.Scene()
    for i, (V, F, col) in enumerate(meshes):
        tm = trimesh.Trimesh(V, F, process=False)
        tm.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(baseColorFactor=[int(c * 255) for c in col] + [255]))
        sc.add_geometry(tm, geom_name=f"b{i}")
    sc.export(C["out_glb"])
    A = np.vstack([m[0] for m in meshes]); lo, hi = A.min(0), A.max(0)
    info.update(bbox=[lo.tolist(), hi.tolist()], out=[float((lo[0] + hi[0]) / 2), float(hi[1]), float(hi[2])], faces=int(sum(len(m[1]) for m in meshes)))
    json.dump(info, open(C["out_json"], "w"), indent=1); print(json.dumps(info, indent=1))
    bad = [h for h, v in info.items() if isinstance(v, dict) and abs(v["yaw_deg"]) > 5]
    if bad: print("WARN yaw > 5 deg for", bad, "- re-pitch heads or move carts instead of bending tracks", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
