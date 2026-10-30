#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Start a new product folder from the reference example.

Usage:
    python3 scripts/scaffold.py <new-product-dir> --filename <seo-file-name>.html [--line <product-line>]

Copies examples/radial-splice-tape (config, i18n, blogs, css) without its photos and illustration,
sets filename / product_line / pub_date, and empties product-specific lists (hero, gallery, videos,
docs, family, JSON-LD products) so nothing from the splicing tape can leak into the new page.
Then rewrite i18n/en.json and blogs.json for the new product, translate, and build.
"""
import argparse, datetime, json, os, shutil

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(SKILL, "examples", "radial-splice-tape")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir"); ap.add_argument("--filename", required=True); ap.add_argument("--line", default="materials-consumables")
    a = ap.parse_args()
    if os.path.exists(a.dir):
        raise SystemExit("%s already exists" % a.dir)
    shutil.copytree(EX, a.dir, ignore=shutil.ignore_patterns("assets", "illustration.svg", "dist", "product.css"))
    os.makedirs(os.path.join(a.dir, "assets"))
    open(os.path.join(a.dir, "product.css"), "w").write("/* product-specific CSS (optional) */\n")
    p = os.path.join(a.dir, "product.json")
    c = json.load(open(p, encoding="utf-8"))
    c.update({"filename": a.filename, "product_line": a.line, "pub_date": datetime.date.today().isoformat(),
              "storage_prefix": a.filename.split(".")[0][:24].replace("-", "_")})
    c["hero"]["images"] = []
    c["gallery"] = []
    c["videos"]["items"] = []
    c["docs"]["items"] = []
    c["family"] = []
    c["how"]["illustration"] = ""
    c["how"]["legend"] = []
    c["jsonld"]["products"] = []
    c["jsonld"]["breadcrumb"] = [["<category>", "https://file.autoinsertion.com"], ["<product>", "{{canonical}}"]]
    c["seo"] = {"og_image": "", "og_image_alt": "", "primary_image": ""}
    c["verify"] = {"forbidden_terms": []}
    json.dump(c, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("scaffolded", a.dir, "- now replace every string in i18n/en.json and blogs.json, then fill product.json lists")


if __name__ == "__main__":
    main()
