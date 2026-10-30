# Example: JUKI gripper nozzle SM-2070 / SM-2071

Delivered 2026-10-22. 3D sources: three.js viewers for the custom JUKI 2583 C (captured turntable) and
A 2723 grippers; eDrawings export (timed out, not used). Base page: JUKI JM odd-form gripper landing page
(dark navy / teal palette). Animation `jaw-anim.js`: 7-step pick-and-insert cycle of the horizontal slide
gripper (open 11 mm → descend into matrix tray → parallel clamp → transfer → upward camera → insert → release).
Video 2:11, 6 scenes. Claims left out: "≥99.99% pick-up rate", Industry 4.0 telemetry figures.

    python3 -m p3cv init ~/work/juki --example juki-gripper-nozzle
    python3 -m p3cv run ~/work/juki/product.json download capture tts mix subtitles landing video thumbnail docs
