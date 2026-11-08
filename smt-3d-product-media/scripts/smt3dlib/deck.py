"""Product presentation (PPTX) stage. Delegates layout/brand to the smt-product-ppt-rebrand builder (its spec.json format,
slide type 'video' for the embedded animation). This stage only: copies the deck assets, drops in the videos and posters
this run produced, substitutes placeholders, and calls the builder once per language.

Placeholders allowed in any string of deck spec files:
  {video}          produced video file name for that language     {poster}  poster jpg grabbed from it
  {still:<name>}   a still rendered by the `stills` stage         {model}   product.model
"""
import json, os, shutil, subprocess, sys
from . import media

def _subst(o, rep):
    if isinstance(o, str):
        for k, v in rep.items(): o = o.replace(k, v)
        return o
    if isinstance(o, list): return [_subst(x, rep) for x in o]
    if isinstance(o, dict): return {k: _subst(v, rep) for k, v in o.items()}
    return o

def build(job, videos):
    D = job["deck"]; builder = job.path(D["builder"])
    if not os.path.exists(builder): raise SystemExit(f"D01 deck builder not found: {builder} (clone smt-product-ppt-rebrand next to this skill or set deck.builder)")
    res = {}
    for L in job["output"]["langs"]:
        A = job.wdir(f"deck_assets_{L}")
        src = job.path(D.get("assets") or "")
        if src and os.path.isdir(src):
            for f in os.listdir(src):
                p = os.path.join(src, f)
                if os.path.isfile(p) and not os.path.exists(os.path.join(A, f)): shutil.copy(p, A)
        rep = {"{model}": job["product"]["model"]}
        v = videos.get(L)
        if v:
            shutil.copy(v, os.path.join(A, os.path.basename(v)))
            pn = f"poster_{L}.jpg"; media.poster(job, v, D.get("poster_t", 12.0), os.path.join(A, pn))
            rep.update({"{video}": os.path.basename(v), "{poster}": pn})
        sd = job.out("stills")
        if os.path.isdir(sd):
            for f in os.listdir(sd):
                shutil.copy(os.path.join(sd, f), os.path.join(A, f)); rep["{still:%s}" % os.path.splitext(f)[0]] = f
        spec = _subst(json.load(open(job.path(D["spec"][L]), encoding="utf-8")), rep)
        sp = job.work(f"deck_spec_{L}.json"); json.dump(spec, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        name = D["name_pattern"].format(slug=job["product"].get("seo_slug") or job["product"]["model"], model=job["product"]["model"], LANG=L.upper(), lang=L) + ".pptx"; od = job.out("deck")
        cmd = [sys.executable, builder, sp, A, od, "--name", name] + (["--render"] if D.get("render") else [])
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout[-2000:])
        if r.returncode: raise SystemExit(f"D02 deck build failed ({L}):\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
        res[L] = os.path.join(od, name)
    return res
