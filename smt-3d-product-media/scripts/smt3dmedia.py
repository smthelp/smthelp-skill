#!/usr/bin/env python3
"""smt-3d-product-media - one entry point for every stage (CLI name smt3dmedia.py; not to be confused with smt-3d-animation-landing-kit/smt3d.py).

usage:  smt3dmedia.py <command> <job.json> [options]
commands (run in this order; `all` runs check..deck):
  doctor                     check python modules, ffmpeg, fonts, TTS, deck builder (no job needed)
  init <dir> --cad F --model M   scaffold a new job folder from the S7040P example
  check    <job>             validate job.json (schema, files, captions, voice lines)
  inspect  <job>             STEP -> GLB, write work/parts.csv (one row per CAD body), show group sizes
  preview  <job> [--t 3 12 33]   render a few frames into work/preview.jpg (fast look before the full render)
  render   <job> [--workers N | --worker i --of N] [--limit K]   render all 3D frames (resumable)
  stills   <job>             render job.stills (posters / marketing images) into out/stills
  real     <job>             cut real_clips into frames
  voice    <job>             TTS voiceover per language (edge-tts)
  compose  <job>             captions + sequence + voice -> out/video/<name>-<LANG>.mp4
  deck     <job>             build product presentation PPTX per language (smt-product-ppt-rebrand)
  publish  <job>             upload out/video + out/deck to publish.drive_folder (gws CLI)
  all      <job>             check, inspect, render, stills, real, voice, compose, deck
Common option: --set key.path=value (JSON value), repeatable, overrides the job without editing it,
  e.g. --set render.width=320 --set render.height=180 --set output.dir=\"out-smoke\"
Exit codes: 0 ok, 2 invalid input (job/CAD/env: J.., C.., doctor), 3 stage failure (R.., M.., V.., D.., P..).
The last stdout line is always one JSON object: {"ok", "command", "skill_version", "results"|"errors", "manifest"}.
Every run updates <out>/manifest.json (skill version, schema, inputs, outputs, stage results)."""
import datetime, hashlib, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from smt3dlib import job as JOB

def manifest(job, stage, result):
    f = job.out("manifest.json"); m = json.load(open(f)) if os.path.exists(f) else {"stages": {}}
    cad = job.path(job["model"]["cad"])
    m.update({"skill": "smt-3d-product-media", "skill_version": JOB.skill_version(), "schema": JOB.SCHEMA,
              "job": job["_file"], "product": job["product"]["model"],
              "cad": {"file": cad, "sha1": hashlib.sha1(open(cad, "rb").read()).hexdigest() if os.path.exists(cad) else None}})
    m["stages"][stage] = {"time": datetime.datetime.now().isoformat(timespec="seconds"), "result": result}
    json.dump(m, open(f, "w"), indent=1, ensure_ascii=False, default=str)

def doctor():
    ok = True
    def chk(name, fn):
        nonlocal ok
        try: print(f"OK   {name}: {fn()}")
        except Exception as e: ok = False; print(f"FAIL {name}: {e}")
    import importlib
    for mod in ("numpy", "PIL", "trimesh", "numba", "cascadio", "edge_tts"):
        chk(mod, lambda m=mod: getattr(importlib.import_module(m), "__version__", "installed"))
    chk("ffmpeg", lambda: subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.split("\n")[0])
    chk("skill", JOB.skill_version)
    b = os.path.normpath(os.path.join(HERE, "..", "..", "smt-product-ppt-rebrand", "scripts", "run.py"))
    chk("deck builder", lambda: b if os.path.exists(b) else (_ for _ in ()).throw(FileNotFoundError(b)))
    print("install: pip install -r requirements.txt" if not ok else "all good")
    _result(ok, "doctor"); return 0 if ok else 2

def init(argv):
    d = argv[0]; cad = argv[argv.index("--cad") + 1]; model = argv[argv.index("--model") + 1]
    os.makedirs(d, exist_ok=True); ex = os.path.join(HERE, "..", "examples", "s7040p")
    j = json.load(open(os.path.join(ex, "job.json"), encoding="utf-8"))
    j["product"].update({"model": model, "seo_slug": model}); j["model"]["cad"] = os.path.relpath(os.path.abspath(cad), d)
    j["real_clips"] = []; j["sequence"] = []; j["deck"]["enabled"] = False; j["publish"]["drive_folder"] = ""
    j["_todo"] = "Run inspect, then rewrite scene.groups/props/animation for this model (see references/method.md). Example values are S7040P's."
    p = os.path.join(d, "job.json"); json.dump(j, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", p); return 0

def main(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return 0
    cmd = argv[0]
    if cmd == "doctor": return doctor()
    if cmd == "init": return init(argv[1:])
    if cmd == "--version": print(JOB.skill_version()); return 0
    if len(argv) < 2: print(__doc__); return 2
    sets = [argv[i + 1] for i, a in enumerate(argv) if a == "--set"]
    job, errs, warns = JOB.load(argv[1], sets); opts = argv[2:]
    for w in warns: print("WARN ", w)
    if errs:
        for e in errs: print("ERROR", e)
        _result(False, cmd, errors=errs); return 2
    stages = ["check", "inspect", "render", "stills", "real", "voice", "compose", "deck"] if cmd == "all" else [cmd]
    res = {}
    for st in stages:
        print(f"== {st}")
        try: r = stage(st, job, opts)
        except SystemExit as e:
            msg = str(e.code); manifest(job, st, {"error": msg}); print("ERROR", msg)
            _result(False, cmd, errors=[msg], results=res, manifest=job.out("manifest.json"))
            return 2 if msg[:1] in "JC" else 3
        manifest(job, st, r); res[st] = r; print(json.dumps(r, ensure_ascii=False, default=str)[:1500])
    _result(True, cmd, results=res, manifest=job.out("manifest.json"))
    return 0

def _result(ok, cmd, **kw):
    print(json.dumps({"ok": ok, "command": cmd, "skill_version": JOB.skill_version(), **kw}, ensure_ascii=False, default=str))

def _sets(opts):
    out = []
    for i, a in enumerate(opts):
        if a == "--set": out += ["--set", opts[i + 1]]
    return out

def stage(st, job, opts):
    from smt3dlib import scene, frames, media, deck
    if st == "check": return {"ok": True}
    if st == "inspect": return scene.inventory(job)
    if st == "preview":
        ts = []
        if "--t" in opts:
            for x in opts[opts.index("--t") + 1:]:
                if x.startswith("--"): break
                ts.append(float(x))
        ts = ts or [1, 8, 20, 33]
        return {"preview": frames.previews(job, ts)}
    if st == "render":
        lim = int(opts[opts.index("--limit") + 1]) if "--limit" in opts else None
        if "--worker" in opts:
            return frames.render_frames(job, int(opts[opts.index("--worker") + 1]), int(opts[opts.index("--of") + 1]), lim)
        n = int(opts[opts.index("--workers") + 1]) if "--workers" in opts else job["render"]["workers"]
        ps = [subprocess.Popen([sys.executable, os.path.abspath(__file__), "render", job["_file"], "--worker", str(i), "--of", str(n)] + _sets(opts)
                               + (["--limit", str(lim)] if lim else [])) for i in range(n)]
        codes = [p.wait() for p in ps]
        have = len([f for f in os.listdir(job.wdir("frames3d")) if f.endswith(".jpg")])
        from smt3dlib.motion import Timeline
        need = int(round(Timeline(job).total * job["render"]["fps"]))
        if any(codes): raise SystemExit(f"R01 a render worker failed: {codes}")
        return {"frames": have, "need": need, "complete": have >= need}
    if st == "stills": return {"stills": frames.stills(job)}
    if st == "real": return {"clips": media.cut_real(job)}
    if st == "voice":
        from smt3dlib.motion import Timeline
        total = _total(job); return {L: media.voice(job, L, total) for L in job["output"]["langs"]}
    if st == "compose":
        out = {}
        for L in job["output"]["langs"]:
            d, n = media.overlay(job, L)
            a = job.work(f"voice_{L}.m4a") if job["voice"].get("enabled") else None
            if a and not os.path.exists(a): raise SystemExit(f"M30 voice enabled but {a} missing: run `voice` first")
            out[L] = media.encode(job, L, d, n, a, job["output"].get("video_variant", "Video"))
        return out
    if st == "deck":
        if not job["deck"].get("enabled"): return {"skipped": "deck.enabled is false"}
        vids = {L: job.out("video", job.name(job["output"].get("video_variant", "Video"), L, ".mp4")) for L in job["output"]["langs"]}
        vids = {L: v for L, v in vids.items() if os.path.exists(v)}
        return deck.build(job, vids)
    if st == "publish":
        fid = job["publish"].get("drive_folder")
        if not fid: return {"skipped": "publish.drive_folder empty"}
        if not shutil.which("gws"): raise SystemExit("P01 gws CLI not found: upload out/video and out/deck by hand")
        up = {}
        for sub in ("video", "deck"):
            d = job.out(sub)
            for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
                if f.endswith((".mp4", ".pptx")):
                    r = subprocess.run(["gws", "drive", "+upload", os.path.join(d, f), "--parent", fid], capture_output=True, text=True)
                    if r.returncode: raise SystemExit(f"P02 upload failed for {f}: {r.stderr[-600:]}")
                    up[f] = json.loads(r.stdout).get("id")
        return up
    raise SystemExit(f"unknown command {st}")

def _total(job):
    fps = job["render"]["fps"]; from smt3dlib.motion import Timeline
    if not job.get("sequence"): return Timeline(job).total
    t = 0.0
    for s in job["sequence"]:
        if s["type"] == "3d": t += s["to"] - s["from"]
        else:
            import glob; t += len(glob.glob(job.wdir(f"real/r{s['clip']+1}") + "/f*.jpg")) / fps or job["real_clips"][s["clip"]]["dur"]
    return t

if __name__ == "__main__":
    try: sys.exit(main(sys.argv[1:]))
    except SystemExit as e:
        if isinstance(e.code, str): print("ERROR", e.code); sys.exit(3)
        raise
