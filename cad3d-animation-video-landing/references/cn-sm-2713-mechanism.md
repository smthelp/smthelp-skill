# Reference: CN-SM-2713 mechanism analysis (worked example)

Source: `JUKI Customized Nozzle CN-SM-2713.html` (eDrawings). Assembly `115.900 Gripper for coil 2713`. Units mm, Y up.

| Body id | File (part) | Role | Motion group |
|---|---|---|---|
| 8 | E3681729000 | JUKI-standard nozzle body / shank | static |
| 26 | 40097271 | return spring (Ø5.7, y −7.9…−3.0) | scales with plunger |
| 14 | 40119856 | inner pin | plunger |
| 62 | 40119855 | plunger (y −16.7…−0.4) | plunger (translate −Y) |
| 20 | e3686729000 | set screw | static |
| 38 | 39.03.557 | holder block | static |
| 44 / 80 | 39.03.556 ×2 | left / right jaw | rotate about pivots (±5.5, −15.6) |
| 50/86, 68 | e3685729000 ×3 | pivot pins L/R, center pin C | pivots static, center pin with plunger |
| 56/92/74 | e3689729000 ×3 | E-clips | follow their pin |
| 122/128/134 | 39.03.589 ×3 | washers | follow their pin |
| 98/104/110 | 40158022 ×3 | contact pins (1 right jaw, 2 left jaw) | follow jaw |
| 116 | 40158022 | center stop pin = Z datum on coil top | static |
| 32 | 49-prt4 | Ø8.5 coil (component), leads x=±2.5 | separate |

Kinematics: plunger down by d → center pin pushes both jaw inner arms down → jaws rotate θ = asin(d/5.5)
(left −θ, right +θ about Z) → lower tips swing outward = OPEN. Return spring pushes plunger up = CLOSED/gripping.
Animation stroke 1.05 mm (visual). 21 gripper parts + coil.

Selling points derived: JUKI-standard shank (plug & play), spring-closed toggle linkage (single driver, symmetric jaws),
3-point self-centering grip (2+1 pins), Z-datum stop pin (fixed depth, force through body), leads untouched,
E-clip retained pins (serviceable).

Scene timing used (16:9 & 9:16, 112.76 s): hook 0.6 · title 11.7 · shank 23.8 · mech 33.5 · grip 48.7 · stop 59.9 ·
explode 72.7 · cycle 81.5 · cta 93.0.
