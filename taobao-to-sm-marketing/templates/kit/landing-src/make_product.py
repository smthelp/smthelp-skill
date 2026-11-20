#!/usr/bin/env python3
"""Writes landing/product.json for the SMT stencil wiping paper roll page.
Self-hosted promo/Shorts videos are added only if they exist in ../out/video/ (copied to
landing/videos/ with a poster frame); otherwise only YouTube board videos are used.
usage: make_product.py <kit_dir>
"""
import json, os, sys, subprocess
KIT = sys.argv[1]
LD = os.path.join(KIT, "landing")
gal_files = ["01-rolls-hero", "02-roll-ends", "03-rolls-long", "04-rolls-row", "05-fabric", "06-packed", "07-core-types", "08-surface", "09-core-gkg", "10-core-dek", "11-core-mpm", "12-core-panasonic", "13-size-diagram"]
gallery = [{"file": f"photos/{f}.jpg", "key": f"g{i}t"} for i, f in enumerate(gal_files, 1)]
videos = []
own = [("SM-Stencil-Wiping-Paper-Promo-EN.mp4", "promo-poster.jpg", "v6t", "v6d"),
       ("SM-Stencil-Wiping-Paper-Shorts-EN.mp4", "shorts-poster.jpg", "v7t", "v7d")]
found = []
for mp4, poster, tk, dk in own:
    p = os.path.join(KIT, "out", "video", mp4)
    if os.path.exists(p):
        os.makedirs(os.path.join(LD, "videos"), exist_ok=True)
        # skill rule: 540 px wide, CRF 30, faststart, for the published videos/ folder
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-vf", "scale=540:-2", "-c:v", "libx264", "-crf", "30", "-preset", "medium",
                        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", os.path.join(LD, "videos", mp4)], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "3", "-i", p, "-frames:v", "1", "-vf", "scale=480:-2", os.path.join(LD, "videos", poster)], check=True)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())
        found.append({"src": f"videos/{mp4}", "poster": f"videos/{poster}", "t": tk, "d": dk, "dur": f"{int(dur)//60}:{int(dur)%60:02d}"})
videos += found
videos += [{"id": "aqv_UO-2GR0", "t": "v1t", "d": "v1d", "dur": "3:20"},
           {"id": "0rtYCeU_ZZ0", "t": "v2t", "d": "v2d", "dur": "0:31"},
           {"id": "E99XkVBh6yk", "t": "v3t", "d": "v3d", "dur": "3:37"}]
FA = "https://file.autoinsertion.com/public/"
P = {
 "file": "smt-stencil-wiping-paper-roll-dek-mpm-gkg-under-stencil-cleaning-smart-ems-pcb-assembly.html",
 "canonical_base": "https://www.smthelp.com/",
 "storage_prefix": "wipingroll_",
 "product_name": "SMT Stencil Wiping Paper Rolls (under-stencil cleaning rolls)",
 "alternate_names": ["SMT stencil wiping paper", "Under stencil cleaning roll", "Stencil wiper roll", "Solder paste printer cleaning paper"],
 "category": "SMT stencil printer consumables",
 "breadcrumb_category": "SMT printer consumables",
 "date_published": "2026-11-19",
 "gallery": gallery, "embed_px": 720, "embed_q": 55,
 "hero": [0, 1, 6, 4, 12],
 "fit_images": [6, 7, 12],
 "how_labels": ["CLEAN", "LINT", "FIT", "SIZE"],
 "videos": videos,
 "catalogs": [
  {"t": "cat1t", "d": "cat1d", "url": FA + "SMThelp%20Machine%20Presentation/SP-830_Auto%20Solder%20Paste%20Printer.pdf", "type": "PDF"},
  {"t": "cat2t", "d": "cat2d", "url": FA + "SMThelp%20Machine%20Presentation/SP-1200%20Semi-Auto%20Screen%20Printer.pdf", "type": "PDF"},
  {"t": "cat3t", "d": "cat3d", "url": FA + "Southern%20Machinery%20Product/Southern%20Machinery%20Smart%20Stencil%20Storage.pdf", "type": "PDF"},
  {"t": "cat4t", "d": "cat4d", "url": FA + "Southern%20Machinery%20Product/S-SPM01%20Solder%20Paste%20Mixer.pdf", "type": "PDF"},
  {"t": "cat5t", "d": "cat5d", "url": FA + "Southern%20Machinery%20Product/SMT%20Stencil%20storage%20rack%20S120618-3-4.pdf", "type": "PDF"}],
 "spec_evidence": {"1": "v", "2": "v", "3": "v", "4": "v", "5": "v", "6": "c", "7": "c", "8": "v", "9": "v", "10": "v",
                   "11": "c", "12": "v", "13": "v", "14": "v", "15": "v"},
 "ld_spec_rows": [2, 3, 4, 5, 8, 9, 10, 11, 12, 13],
 "disambiguation": "Values marked To be confirmed on the page: wood pulp / polyester ratio (55/45 or 45/55), basis weight (56 or 60 g/m2), MINAMI roll length (15 or 10 m), the core opening for Desen and DEK rolls (straight or cross slot), and Yamaha / EKRA sizes. Sizes are core length x paper width x roll length. Printer brand names identify compatible equipment only.",
 "howto_name": "How to choose and order an SMT stencil wiping paper roll",
 "howto_tools": ["Old wiping roll core", "Ruler or tape measure", "Phone camera"],
 "service_icons": ["📏", "✂️", "🧽", "🏭"],
 "calc_mode": "rolls",
 "calc_defaults": ["", "", "", "", "10"],
 "video_upload_date": "2026-11-19"
}
json.dump(P, open(os.path.join(LD, "product.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("videos self-hosted:", [v["src"] for v in found] or "none")
