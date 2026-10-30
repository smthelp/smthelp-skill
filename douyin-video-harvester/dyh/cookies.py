"""Netscape cookie parsing; keep ONLY douyin-related domains so other sessions never leave the user's file."""
import os
from .errors import DyhError

DOUYIN_DOMAINS = ("douyin.com", "douyinpic.com", "douyinvod.com", "bytedance.com", "snssdk.com", "amemv.com")

def parse(path):
    if not os.path.exists(path):
        raise DyhError("E_COOKIES", f"{path} not found")
    out = []
    for line in open(path, encoding="utf-8", errors="ignore"):
        line = line.rstrip("\n")
        if line.startswith("#HttpOnly_"):
            line = line[10:]
        elif line.startswith("#") or not line.strip():
            continue
        f = line.split("\t")
        if len(f) < 7:
            continue
        out.append(dict(domain=f[0], path=f[2], secure=f[3] == "TRUE", expires=f[4], name=f[5], value=f[6] or ""))
    return out

def douyin_only(cookies):
    return [c for c in cookies if any(c["domain"].lstrip(".").endswith(d) for d in DOUYIN_DOMAINS)]

def write_netscape(cookies, path):
    with open(path, "w") as fh:
        fh.write("# Netscape HTTP Cookie File\n")
        for c in cookies:
            dom = c["domain"]
            fh.write("\t".join([dom, "TRUE" if dom.startswith(".") else "FALSE", c["path"],
                                "TRUE" if c["secure"] else "FALSE", str(c.get("expires") or 0), c["name"], c["value"]]) + "\n")
    os.chmod(path, 0o600)

def load_douyin(path):
    ck = douyin_only(parse(path))
    if not ck:
        raise DyhError("E_COOKIES", "no douyin.com cookies in file (export while logged in to douyin.com)")
    return ck
