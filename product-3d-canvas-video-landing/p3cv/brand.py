"""Brand colour helpers shared by templates."""


def rgba(hexc, a):
    h = hexc.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"


def lighten(hexc, f=0.55):
    h = hexc.lstrip("#")
    c = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{int(v + (255 - v) * f):02x}" for v in c)


def tokens(brand):
    p, pd = brand["primary"], brand["primary_dark"]
    return {"__P__": p, "__PD__": pd, "__P08__": rgba(p, .08), "__P45__": rgba(p, .45),
            "__PD35__": rgba(pd, .35), "__DARKBG__": brand["dark_bg"], "__PLIGHT__": lighten(p),
            "__ACCENT__": brand["accent"]}
