#!/usr/bin/env python3
"""Estimate machines needed per annual volume tier for pin/terminal insertion.

usage: capacity_calc.py --cph 12000 --pins 20,50,100,270 --volumes 100000,500000,1000000,3000000 [--hours 3000]
--hours = effective hours per machine per year (default 3000 = 2 shifts x 250 days x 16 h x ~75% OEE).
Output is an ESTIMATE from the theoretical CPH; always label it "估算/to be confirmed with samples".
"""
import argparse, math
p = argparse.ArgumentParser()
p.add_argument("--cph", type=float, default=12000, help="theoretical insertions per hour per machine")
p.add_argument("--pins", default="20,50,100,270")
p.add_argument("--volumes", default="100000,500000,1000000,3000000")
p.add_argument("--hours", type=float, default=3000)
a = p.parse_args()
pins = [int(x) for x in a.pins.split(",")]
vols = [int(x) for x in a.volumes.split(",")]
print(f"CPH={a.cph:g}, effective hours/yr={a.hours:g}")
print("pins/part | parts/h | parts/yr per machine")
for n in pins:
    ph = a.cph / n
    print(f"{n:>9} | {ph:>7.0f} | {ph*a.hours:>12,.0f}")
print("\nmachines needed (rows = annual volume, cols = pins/part)")
print("volume".rjust(10) + "".join(f"{n:>8}" for n in pins))
for v in vols:
    print(f"{v:>10,}" + "".join(f"{math.ceil(v / (a.cph / n * a.hours)):>8}" for n in pins))
