#!/usr/bin/env python3
"""Extract text from product source attachments: PDF, legacy PPT, PPTX.

usage: extract_source_text.py <file.pdf|file.ppt|file.pptx> [more files ...]

PDF   pypdf page text, one block per page.
PPT   legacy PowerPoint 97-2003 (OLE compound file). `strings`, UTF-16 and GBK
      decodes of the raw "PowerPoint Document" stream all produce garbage; the
      stream must be walked as records instead. TextCharsAtom (type 0x0FA0)
      bodies are UTF-16LE. Container records (SlideListWithText 0x0FF0 and
      friends) nest their text atoms inside, so a linear walk that follows
      record lengths skips them - scan every offset and validate instead.
PPTX  OOXML zip: pull <a:t> runs from ppt/slides/slideN.xml.
Prints plain text to stdout. Requires: pypdf (PDF), olefile (PPT). PPTX needs
only the standard library.
"""
import sys, os, struct, zipfile, re, unicodedata


def fix_path(p):
    """macOS stores Chinese filenames NFD-decomposed; a path typed as NFC fails
    with a bare 'file not found'. Normalize to what the disk actually holds."""
    if sys.platform == "darwin":
        nfd = unicodedata.normalize("NFD", p)
        if os.path.exists(nfd):
            return nfd
    return p


def pdf_text(path):
    from pypdf import PdfReader
    r = PdfReader(path)
    out = []
    for i, p in enumerate(r.pages, 1):
        out.append("----- page %d -----\n%s" % (i, (p.extract_text() or "").strip()))
    return "\n".join(out)


def _printable_ratio(s):
    if not s:
        return 0.0
    ok = sum(1 for ch in s if ch.isprintable() or ch in "\n\r\t")
    return ok / len(s)


def ppt_text(path):
    import olefile
    ole = olefile.OleFileIO(path)
    try:
        data = ole.openstream(["PowerPoint Document"]).read()
    finally:
        ole.close()
    out, i, n = [], 0, len(data)
    while i + 8 <= n:
        rectype, length = struct.unpack_from("<HI", data, i + 2)
        body = data[i + 8:i + 8 + length]
        if rectype == 0x0FA0 and 0 < length <= len(body) and length % 2 == 0:
            txt = body.decode("utf-16-le", "ignore").strip()
            # validate: real slide text, not a random 0x0FA0 byte pair
            if txt and _printable_ratio(txt) > 0.9 and len(txt) >= 2:
                # slide-master placeholder boilerplate, not product content
                if not re.search(r"单击此处编辑母版|Click to edit Master", txt):
                    out.append(txt)
                i += 8 + length
                continue
        i += 1
    return "\n".join(out)


def pptx_text(path):
    out = []
    with zipfile.ZipFile(path) as z:
        names = sorted(
            (n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
            key=lambda n: int(re.search(r"\d+", n.rsplit("/", 1)[-1]).group()),
        )
        for n in names:
            xml = z.read(n).decode("utf-8", "ignore")
            runs = re.findall(r"<a:t>(.*?)</a:t>", xml, re.S)
            txt = "".join(runs).strip()
            if txt:
                out.append("----- %s -----\n%s" % (n.rsplit("/", 1)[-1], txt))
    return "\n".join(out)


HANDLERS = {".pdf": pdf_text, ".ppt": ppt_text, ".pptx": pptx_text}


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not files:
        sys.exit(__doc__)
    for f in files:
        f = fix_path(f)
        ext = os.path.splitext(f)[1].lower()
        fn = HANDLERS.get(ext)
        if not fn:
            print("skip (unsupported): " + f, file=sys.stderr)
            continue
        print("===== %s =====" % os.path.basename(f))
        try:
            print(fn(f))
        except Exception as e:
            print("FAILED: %s: %s" % (type(e).__name__, e), file=sys.stderr)


if __name__ == "__main__":
    main()
