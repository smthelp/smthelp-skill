"""SolidWorks eDrawings / HOOPS HTML exports. Slow under SwiftShader: the first frames stall and
the page may show 'Connection timed-out' if its streaming fails - then the capture is skipped with a
warning (use a Three.js viewer or photos instead). Mouse wheel ZOOMS OUT in eDrawings, so the
default zoom_delta is inverted here."""
import time


def capture(page, c, out_dir, lg):
    time.sleep(max(c["settle_s"], 60))
    body = page.inner_text("body")[:2000]
    if "timed-out" in body.lower():
        raise RuntimeError("eDrawings viewer reported 'Connection timed-out'")
    w, h = c["viewport"]; cx, cy = w // 2, h // 2
    page.mouse.move(cx, cy)
    for _ in range(c["zoom_steps"]):
        page.mouse.wheel(0, abs(c["zoom_delta"])); time.sleep(1.5)  # inverted: positive = zoom in here
    for _ in range(c.get("zoom_out_steps", 0)):  # large machines overflow the default framing
        page.mouse.wheel(0, -abs(c["zoom_delta"])); time.sleep(1.5)
    # drag where no part sits (e.g. [0.5, 0.92]): hovering a part pops a name tooltip into the frame
    dx, dy = c.get("drag_at") or [0.5, 0.5]; dx, dy = int(w * dx), int(h * dy)
    frames = []
    for i in range(c["frames"]):
        page.mouse.move(dx, dy); page.mouse.down(); page.mouse.move(dx + c["drag_px"], dy, steps=6); page.mouse.up()
        page.mouse.move(2, 2); page.keyboard.press("Escape")  # park the cursor: hovering the model shows a part-name tooltip
        time.sleep(3)
        f = out_dir / f"raw_{i:03d}.jpg"; page.screenshot(path=str(f), type="jpeg", quality=92); frames.append(f)
        lg.info("frame %d/%d", i + 1, c["frames"])
    return frames
