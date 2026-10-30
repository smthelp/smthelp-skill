"""Three.js viewer pages (Southern Machinery WordPress single-HTML viewers with OrbitControls).
Steps: settle -> click toggle buttons (stop auto-rotate, hide grid) -> hide UI except <canvas>
-> wheel-zoom in -> drag horizontally between frames for a 360 degree turntable."""
import time

HIDE = "body *{visibility:hidden!important} canvas{visibility:visible!important}"


def capture(page, c, out_dir, lg):
    time.sleep(c["settle_s"])
    for name in c.get("click_buttons", []):
        try:
            page.get_by_role("button", name=name).first.click(timeout=3000); time.sleep(0.8)
        except Exception as e:  # buttons are optional
            lg.warning("button %r not clicked: %s", name, str(e).splitlines()[0])
    if c.get("hide_ui", True):
        page.add_style_tag(content=HIDE); time.sleep(1)
    w, h = c["viewport"]; cx, cy = w // 2, h // 2
    page.mouse.move(cx, cy)
    for _ in range(c["zoom_steps"]):
        page.mouse.wheel(0, c["zoom_delta"]); time.sleep(0.8)
    time.sleep(2)
    frames = []
    for i in range(c["frames"]):
        f = out_dir / f"raw_{i:03d}.jpg"
        page.screenshot(path=str(f), type="jpeg", quality=92); frames.append(f)
        page.mouse.move(cx, cy); page.mouse.down(); page.mouse.move(cx + c["drag_px"], cy, steps=4); page.mouse.up()
        time.sleep(0.6)
        lg.info("frame %d/%d", i + 1, c["frames"])
    return frames
