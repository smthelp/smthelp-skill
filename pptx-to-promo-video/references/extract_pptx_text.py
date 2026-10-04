#!/usr/bin/env python3
"""Extract per-slide text from a PPTX, and flag a malformed soffice export.

Why this exists: when a .pptx is the source, the rendered PDF sometimes has an
EMPTY text layer -- the words live in the PPTX XML, not the rasterized page. And
soffice's export can be malformed: `pdfinfo` reports N pages but `pdftoppm`
actually renders many more (the extras are image-only machine/line photos). This
tool reads the real slide text from the PPTX XML so narration can be written
even when `pdftotext` returns nothing, and optionally cross-checks the rendered
PNG count against the slide count to catch the malformed-export case.

Usage:
    python3 extract_pptx_text.py doc.pptx
    python3 extract_pptx_text.py doc.pptx --slides slides_1080
"""
import argparse, glob, os, re, sys, zipfile


def slide_texts(pptx):
    z = zipfile.ZipFile(pptx)
    slides = sorted(
        [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
        key=lambda x: int(re.findall(r"\d+", x)[0]))
    out = []
    for i, s in enumerate(slides, 1):
        xml = z.read(s).decode("utf-8", "ignore")
        txt = [m for m in re.findall(r"<a:t>(.*?)</a:t>", xml, re.S) if m.strip()]
        out.append((i, " | ".join(t.strip() for t in txt)))
    return out


def page_of(path):
    return int("".join(ch for ch in os.path.basename(path) if ch.isdigit()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx", help="source .pptx file")
    ap.add_argument("--slides", default=None,
                    help="optional rendered slides dir to cross-check page count")
    args = ap.parse_args()

    slides = slide_texts(args.pptx)
    print(f"PPTX slides with text: {len(slides)}")
    for i, joined in slides:
        print(f"\nslide {i:02d}:")
        print(f"  {joined[:300]}")

    if args.slides:
        pngs = sorted(glob.glob(os.path.join(args.slides, "slide-*.png")),
                      key=page_of)
        n_png = len(pngs)
        n_xml = len(slides)
        print(f"\n--- render cross-check ---")
        print(f"  PPTX text slides : {n_xml}")
        print(f"  Rendered PNGs    : {n_png}")
        if n_png > n_xml * 1.5:
            print("  WARNING: rendered page count >> slide count.")
            print("  soffice export is malformed -- the extra pages are")
            print("  image-only machine/line photos. Use profile_slides.py")
            print("  to pick the best visual pages; lock in the text slides above.")
        else:
            print("  OK: render count consistent with slide count.")


if __name__ == "__main__":
    main()
