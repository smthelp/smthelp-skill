"""Engine for smt-logo-looks-stickers: brand looks + GIF stickers from a logo STEP.

Called by smtlogomedia.py with a job dict (see references/job-spec.md).
The logo is rendered with the vendored CPU renderer (logo_render.py) from the
inspected GLB; part colours are overridden to the brand colours (logo_cad.py).
Stickers are assembled with ffmpeg (palettegen/paletteuse) — PIL's GIF writer
corrupts multi-frame RGBA sequences, so it is never used for GIF output.
"""
import math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import logo_render as R
import logo_cad

S = 512  # sticker canvas (square, WhatsApp/Telegram sticker size)


# ---------------------------------------------------------------- job access
def _hex(rgb_hex):
    h = rgb_hex.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Engine:
    def __init__(self, job):
        self.job = job
        self.colors = {k: _hex(v) for k, v in job["colors"].items()}
        self.brand_dir = job["brand_dir"]
        self.out_looks = os.path.join(job["out_dir"], "looks")
        self.out_stick = os.path.join(job["out_dir"], "stickers")
        for d in (self.out_looks, self.out_stick):
            os.makedirs(d, exist_ok=True)
        self._meshes = {}   # thicken -> meshes
        self._mark = None
        self.logo_png = job.get("logo_png")  # optional clean 2D logo (flat looks)
        self.drop_zone = job.get("drop_zone")  # optional [z_below, x_below]

    # -- brand assets (graceful fallbacks: plain navy bg, DejaVu fonts) --
    def font(self, kind, size):
        names = {"XB": "Montserrat-ExtraBold.ttf", "B": "Montserrat-Bold.ttf",
                 "SB": "Montserrat-SemiBold.ttf", "R": "Montserrat-Regular.ttf"}
        cands = [os.path.join(self.brand_dir, "fonts", names[kind])]
        if kind in ("XB", "B"):
            cands.append("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
        else:
            cands.append("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        for c in cands:
            if os.path.exists(c):
                return ImageFont.truetype(c, size)
        return ImageFont.load_default()

    def circuit_bg(self, W, H, base=None, opacity=0.15):
        base = base or self.colors["navy"]
        img = Image.new("RGB", (W, H), base)
        pat_path = os.path.join(self.brand_dir, "circuit.png")
        if not os.path.exists(pat_path):
            return img
        pat = Image.open(pat_path).convert("RGBA")
        pw, ph = pat.size
        tile = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for x in range(W - pw * 3, W, pw):
            for y in range(H - ph * 3, H, ph):
                tile.alpha_composite(pat, (x, y))
        a = tile.split()[3].point(lambda v: int(v * opacity))
        tile.putalpha(a)
        return Image.alpha_composite(img.convert("RGBA"), tile).convert("RGB")

    # -- logo meshes --
    def logo(self, thicken=1.0):
        if thicken not in self._meshes:
            parts = logo_cad.load_parts(self.job["glb"])
            meshes = logo_cad.stand_upright(
                parts, self.job["colors"]["green"], self.job["colors"]["teal"], thicken)
            if self.drop_zone:
                meshes = logo_cad.drop_zone(meshes, *self.drop_zone)
            self._meshes[thicken] = meshes
        return self._meshes[thicken]

    def mark(self, thicken=1.0):
        if self._mark is None:
            self._mark = logo_cad.mark_only(self.logo(thicken))
        return self._mark

    def text(self, key, default=""):
        return self.job.get("texts", {}).get(key, default)

    def contact_line(self):
        c = self.job["contacts"]
        return f"{c['web']}  ·  {c['email']}  ·  WhatsApp {c['whatsapp']}"


# ---------------------------------------------------------------- mesh helpers
def xform(meshes, M):
    return [(V @ M.T, F, col) for V, F, col in meshes]


def rot_z(deg):
    a = math.radians(deg)
    return np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]], float)


def rot_x(deg):
    a = math.radians(deg)
    return np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]], float)


def translate(meshes, dx=0.0, dy=0.0, dz=0.0):
    out = []
    for V, F, col in meshes:
        V2 = V.copy()
        V2[:, 0] += dx; V2[:, 1] += dy; V2[:, 2] += dz
        out.append((V2, F, col))
    return out


def scale_mesh(meshes, sx=1.0, sy=1.0, sz=1.0):
    out = []
    for V, F, col in meshes:
        V2 = V.copy()
        V2[:, 0] *= sx; V2[:, 1] *= sy; V2[:, 2] *= sz
        out.append((V2, F, col))
    return out


def render_rgba(meshes, eye, W, H, fov=35, target=(0, 0, 0)):
    """Difference matting: render on white and on black, recover alpha + colour."""
    v = R.look_at(eye, target)
    iw = R.render(meshes, v, W, H, fov_deg=fov, bg=(1, 1, 1), ss=2, edges=True).astype(np.float32) / 255.0
    ib = R.render(meshes, v, W, H, fov_deg=fov, bg=(0, 0, 0), ss=2, edges=True).astype(np.float32) / 255.0
    diff = (iw - ib).mean(axis=2)
    alpha = np.clip(1.0 - diff, 0, 1)
    fg = np.zeros_like(ib)
    m = alpha > 0.02
    fg[m] = ib[m] / np.clip(alpha[m, None], 0.02, 1)
    out = np.dstack([np.clip(fg, 0, 1), alpha])
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


def rounded_card(base, box, radius=28, fill=(255, 255, 255, 255)):
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=fill)


def logo_on_white_card(e, W=1100, H=380, pad=46, eye=(0.0, 0.95, 0.0), thicken=1.0):
    """Front logo on a white rounded card (brand rule: the logo always sits
    on a white rounded card when the background is dark). When the job
    supplies logo_png, the clean 2D logo is used (exact official art, no
    render); otherwise the 3D render is used."""
    if e.logo_png and os.path.exists(e.logo_png):
        img = Image.open(e.logo_png).convert("RGBA")
        inner_w, inner_h = W - pad * 2, H - pad * 2
        s = min(inner_w / img.width, inner_h / img.height)
        img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
    else:
        img = render_rgba(e.logo(thicken), eye, W, H, fov=35)
        img = img.crop(img.getbbox())
    card = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    rounded_card(card, (0, 0, card.width - 1, card.height - 1), radius=30)
    card.alpha_composite(img, (pad, pad))
    return card

# ---------------------------------------------------------------- static looks
def look_hero(e):
    W, H = 1920, 1080
    c = e.colors
    img = e.circuit_bg(W, H).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.text((120, 110), e.text("hero_kicker", "SMT  /  THT  AUTOMATION  ·  SINCE 2011"),
           font=e.font("B", 34), fill=c["green"])
    d.text((120, 165), e.text("hero_headline_1", "Auto Insertion,"), font=e.font("XB", 110), fill=(255, 255, 255))
    d.text((120, 285), e.text("hero_headline_2", "Built for Your Line"), font=e.font("XB", 110), fill=(255, 255, 255))
    d.text((120, 440), e.text("hero_sub", "Radial · Axial · Odd-Form · Pin / Eyelet / Terminal — one partner\nfrom manual stations to a fully automated THT line."),
           font=e.font("SB", 36), fill=c["muted"])
    card = logo_on_white_card(e, W=1000, H=360, pad=44)
    img.alpha_composite(card, (120, 590))
    d = ImageDraw.Draw(img)
    d.text((120, 1000), e.contact_line(), font=e.font("SB", 30), fill=c["muted"])
    img.convert("RGB").save(os.path.join(e.out_looks, "01-tradeshow-hero-1920x1080.png"))
    return "01-tradeshow-hero-1920x1080.png"


def look_business_card(e):
    W, H = 1050, 600
    c = e.colors
    img = Image.new("RGBA", (W, H), c["light"] + (255,))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 14), fill=c["green"])
    card = logo_on_white_card(e, W=880, H=300, pad=36, eye=(0.0, 0.78, 0.0))
    img.alpha_composite(card, ((W - card.width) // 2, 90))
    d = ImageDraw.Draw(img)
    d.text((78, 400), e.job["company"]["full"], font=e.font("B", 30), fill=c["navy"])
    d.text((78, 448), e.text("card_tagline", "SMT / THT equipment, PCB separators and spare parts since 2011"),
           font=e.font("SB", 26), fill=c["grey"])
    d.text((78, 510), e.contact_line(), font=e.font("SB", 26), fill=c["teal"])
    img.convert("RGB").save(os.path.join(e.out_looks, "02a-business-card-front-1050x600.png"))
    img2 = e.circuit_bg(W, H).convert("RGBA")
    big = render_rgba(e.mark(), (0.0, 1.5, 0.0), 430, 430, fov=35)
    img2.alpha_composite(big, ((W - 430) // 2, 22))
    d = ImageDraw.Draw(img2)
    d.text((W // 2, 500), e.job["company"]["short"].upper(), font=e.font("XB", 40),
           fill=(255, 255, 255), anchor="ma")
    img2.convert("RGB").save(os.path.join(e.out_looks, "02b-business-card-back-1050x600.png"))
    return ["02a-business-card-front-1050x600.png", "02b-business-card-back-1050x600.png"]


def look_email_signature(e):
    W, H = 720, 170
    c = e.colors
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    card = logo_on_white_card(e, W=300, H=120, pad=14)
    img.alpha_composite(card, (14, 24))
    d = ImageDraw.Draw(img)
    d.rectangle((330, 24, 335, H - 24), fill=c["green"])
    p = e.job.get("person", {})
    d.text((352, 20), f"{p.get('name', '')}  ·  {p.get('title', '')}", font=e.font("B", 24), fill=c["navy"])
    d.text((352, 52), e.job["company"]["short"], font=e.font("SB", 20), fill=c["grey"])
    d.text((352, 78), e.text("sig_line", "SMT / THT Automation"), font=e.font("SB", 20), fill=c["grey"])
    ct = e.job["contacts"]
    d.text((352, 106), f"{ct['email']}  ·  {ct['web']}", font=e.font("SB", 20), fill=c["teal"])
    d.text((352, 132), f"WhatsApp {ct['whatsapp']}", font=e.font("SB", 20), fill=c["teal"])
    img.convert("RGB").save(os.path.join(e.out_looks, "03-email-signature-720x170.png"))
    return "03-email-signature-720x170.png"


def look_social(e):
    c = e.colors
    S = 512
    img = Image.new("RGBA", (S, S), c["navy"] + (255,))
    rounded_card(img, (26, 26, S - 27, S - 27), radius=90)
    mark = render_rgba(e.mark(), (0.0, 1.5, 0.0), 400, 400, fov=35)
    img.alpha_composite(mark, ((S - 400) // 2, (S - 400) // 2))
    img.convert("RGB").save(os.path.join(e.out_looks, "04a-social-avatar-512x512.png"))
    W, H = 1584, 396
    img2 = e.circuit_bg(W, H).convert("RGBA")
    card = logo_on_white_card(e, W=640, H=220, pad=30)
    img2.alpha_composite(card, (70, 88))
    d = ImageDraw.Draw(img2)
    d.text((740, 130), e.text("banner_kicker", "SMT / THT AUTOMATION"), font=e.font("B", 30), fill=c["green"])
    d.text((740, 175), e.text("banner_headline", "Auto Insertion for EMS"), font=e.font("XB", 48), fill=(255, 255, 255))
    d.text((740, 245), e.text("banner_sub", "Factories  ·  Shenzhen  ·  Since 2011  ·  smthelp.com"),
           font=e.font("SB", 28), fill=c["muted"])
    img2.convert("RGB").save(os.path.join(e.out_looks, "04b-linkedin-banner-1584x396.png"))
    return ["04a-social-avatar-512x512.png", "04b-linkedin-banner-1584x396.png"]


def look_endcard(e):
    W, H = 1920, 1080
    c = e.colors
    img = e.circuit_bg(W, H).convert("RGBA")
    card = logo_on_white_card(e, W=1100, H=380, pad=46)
    img.alpha_composite(card, ((W - card.width) // 2, 210))
    d = ImageDraw.Draw(img)
    d.text((W // 2, 660), e.text("endcard_headline", "FREE LIVE DEMO + EVALUATION REPORT"),
           font=e.font("XB", 64), fill=(140, 220, 120), anchor="ma")
    d.text((W // 2, 770), e.text("endcard_sub_1", "Send your component mix — we map your manual stations"),
           font=e.font("SB", 36), fill=c["muted"], anchor="ma")
    d.text((W // 2, 820), e.text("endcard_sub_2", "to an automated line, before any price is discussed."),
           font=e.font("SB", 36), fill=c["muted"], anchor="ma")
    ct = e.job["contacts"]
    d.text((W // 2, 950), f"{ct['email']}   ·   {ct['whatsapp']}   ·   {ct['web']}",
           font=e.font("B", 34), fill=(255, 255, 255), anchor="ma")
    img.convert("RGB").save(os.path.join(e.out_looks, "05-video-endcard-1920x1080.png"))
    return "05-video-endcard-1920x1080.png"


def look_rollup(e):
    W, H = 800, 2000
    c = e.colors
    img = e.circuit_bg(W, H).convert("RGBA")
    card = logo_on_white_card(e, W=620, H=220, pad=30)
    img.alpha_composite(card, ((W - card.width) // 2, 90))
    d = ImageDraw.Draw(img)
    d.text((W // 2, 400), e.text("rollup_kicker", "SMT / THT AUTOMATION"), font=e.font("B", 30), fill=c["green"], anchor="ma")
    d.text((W // 2, 450), e.text("rollup_headline_1", "Stop Hand-Placing."), font=e.font("XB", 72), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 530), e.text("rollup_headline_2", "Start Inserting."), font=e.font("XB", 72), fill=(255, 255, 255), anchor="ma")
    rows = e.job.get("rollup_rows", [
        ("RADIAL / AXIAL", "S3000A · S3010A — taped parts, no stops"),
        ("ODD-FORM", "S-70LD · S7040 — vision-guided placement"),
        ("PIN / EYELET / TERMINAL", "S7020 · S7020T — one pin, seated right"),
        ("FULL LINE", "Conveyor · wave soldering · AOI · cleaning"),
    ])
    y = 700
    for kicker, line in rows:
        d.text((80, y), kicker, font=e.font("B", 30), fill=c["green"])
        d.text((80, y + 44), line, font=e.font("SB", 30), fill=(255, 255, 255))
        y += 150
    d.rectangle((80, y + 10, W - 80, y + 14), fill=c["green"])
    d.text((W // 2, y + 60), e.text("rollup_cta", "FREE LIVE DEMO + EVALUATION REPORT"),
           font=e.font("XB", 34), fill=(140, 220, 120), anchor="ma")
    ct = e.job["contacts"]
    d.text((W // 2, y + 120), ct["email"], font=e.font("B", 32), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, y + 165), f"WhatsApp {ct['whatsapp']}", font=e.font("B", 32), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, y + 210), ct["web"], font=e.font("B", 32), fill=c["muted"], anchor="ma")
    wm = render_rgba(e.mark(), (0.0, 1.5, 0.0), 520, 520, fov=35)
    wm.putalpha(wm.split()[3].point(lambda v: v * 30 // 255))
    img.alpha_composite(wm, ((W - 520) // 2, 1470))
    img.convert("RGB").save(os.path.join(e.out_looks, "06-rollup-banner-800x2000.png"))
    return "06-rollup-banner-800x2000.png"


LOOKS = {"hero": look_hero, "business_card": look_business_card,
         "email_signature": look_email_signature, "social": look_social,
         "endcard": look_endcard, "rollup": look_rollup}

# ---------------------------------------------------------------- GIF stickers
def sticker_text_layer(e, text, size=64, y=None, font_kind="XB"):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    yy = y if y is not None else S - 110
    d.text((S // 2, yy), text, font=e.font(font_kind, size), fill=(255, 255, 255),
           stroke_width=4, stroke_fill=e.colors["navy"], anchor="ma")
    return layer


def save_gif(e, frames, name, duration=80):
    """Assemble via ffmpeg (palettegen/paletteuse). Never use PIL's GIF writer
    for multi-frame RGBA: it writes corrupt LZW data (verified 2026-11-14)."""
    tmp = os.path.join(e.job["work_dir"], "gif-" + name.replace(".gif", ""))
    os.makedirs(tmp, exist_ok=True)
    for i, fr in enumerate(frames):
        fr.convert("RGBA").save(os.path.join(tmp, f"{i:02d}.png"))
    out = os.path.join(e.out_stick, name)
    fps = 1000 / duration
    cmd = ["ffmpeg", "-y", "-v", "error", "-framerate", str(fps), "-i",
           os.path.join(tmp, "%02d.png"),
           "-vf", "split[s0][s1];[s0]palettegen=max_colors=128:reserve_transparent=1[p];[s1][p]paletteuse",
           "-loop", "0", out]
    subprocess.run(cmd, check=True)
    return name, len(frames), os.path.getsize(out) // 1024


def gif_spin(e):
    base = e.logo(thicken=6.0)
    frames = []
    for i in range(20):
        frames.append(render_rgba(xform(base, rot_z(i * 18)), (0.0, 1.9, 0.0), S, S, fov=35))
    return save_gif(e, frames, "01-logo-spin.gif", duration=60)


def gif_hello(e):
    base = e.logo(thicken=4.0)
    frames = []
    ys = [0.30, 0.22, 0.12, 0.04, 0.0, 0.0, 0.10, 0.05, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0]
    sq = [1.0, 1.0, 1.0, 1.0, 1.0, 0.78, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    for i, (y, s) in enumerate(zip(ys, sq)):
        m = scale_mesh(translate(base, dz=y), sx=1.0 + (1 - s) * 0.6, sz=s)
        fr = render_rgba(m, (0.0, 1.9, 0.0), S, S, fov=35)
        if i >= 9:
            pop = 0.7 + 0.3 * ((i - 9) / 4)
            fr.alpha_composite(sticker_text_layer(e, "HELLO!", size=int(72 * pop)))
        frames.append(fr)
    return save_gif(e, frames, "02-hello.gif", duration=90)


def gif_demo_ready(e):
    base = e.logo(thicken=4.0)
    logo = render_rgba(base, (0.0, 1.9, 0.0), S, S, fov=35)
    frames = []
    for i in range(16):
        fr = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        pulse = 0.5 + 0.5 * math.sin(i / 16 * 2 * math.pi)
        rx, ry = int(228 + 10 * pulse), int(108 + 6 * pulse)
        ring = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(ring)
        d.ellipse((S // 2 - rx, S // 2 - 30 - ry, S // 2 + rx, S // 2 - 30 + ry),
                  outline=e.colors["green"] + (int(90 + 165 * pulse),), width=7)
        fr.alpha_composite(ring)
        fr.alpha_composite(logo)
        fr.alpha_composite(sticker_text_layer(e, "DEMO READY", size=62))
        frames.append(fr)
    return save_gif(e, frames, "03-demo-ready.gif", duration=90)


def gif_lets_talk(e):
    base = e.logo(thicken=4.0)
    frames = []
    for i in range(14):
        t = min(1.0, i / 6)
        ease = 1 - (1 - t) ** 3
        fr = render_rgba(translate(base, dx=-0.75 * (1 - ease)), (0.0, 1.9, 0.0), S, S, fov=35)
        if i >= 7:
            a = int(255 * min(1.0, (i - 7) / 4))
            txt = sticker_text_layer(e, "LET'S TALK SMT", size=56)
            txt.putalpha(txt.split()[3].point(lambda v: v * a // 255))
            fr.alpha_composite(txt)
        frames.append(fr)
    return save_gif(e, frames, "04-lets-talk-smt.gif", duration=90)


def gif_thank_you(e):
    mark = e.mark(thicken=4.0)
    frames = []
    for i in range(14):
        fr = render_rgba(xform(mark, rot_z(i * (360 / 14))), (0.0, 1.5, 0.0), S, S, fov=35)
        fr.alpha_composite(sticker_text_layer(e, "THANK YOU", size=60))
        frames.append(fr)
    return save_gif(e, frames, "05-thank-you.gif", duration=80)


def gif_see_you(e):
    base = e.logo(thicken=4.0)
    frames = []
    for i in range(16):
        a = 10 * math.sin(i / 16 * 2 * math.pi)
        b = 6 * math.sin(i / 16 * 2 * math.pi + 0.9)
        fr = render_rgba(xform(xform(base, rot_z(a)), rot_x(b)), (0.0, 1.9, 0.0), S, S, fov=35)
        fr.alpha_composite(sticker_text_layer(e, "SEE YOU AT", size=52, y=S - 150))
        fr.alpha_composite(sticker_text_layer(e, "THE SHOW", size=52, y=S - 95))
        frames.append(fr)
    return save_gif(e, frames, "06-see-you-at-the-show.gif", duration=90)


STICKERS = {"spin": gif_spin, "hello": gif_hello, "demo_ready": gif_demo_ready,
            "lets_talk": gif_lets_talk, "thank_you": gif_thank_you, "see_you": gif_see_you}


def run_looks(e, keys=None):
    out = []
    for k in (keys or list(LOOKS)):
        r = LOOKS[k](e)
        out += r if isinstance(r, list) else [r]
    return out


def run_stickers(e, keys=None):
    out = []
    for k in (keys or list(STICKERS)):
        out.append(STICKERS[k](e))
    return out
