#!/usr/bin/env python3
"""USD price rule shared by every kit. usage: price_usd.py 180 380 1200  ->  55 115 364
Default USD = round(CNY * 2 / 6.6); override with --markup / --fx (keep in kit.yaml)."""
import sys, argparse
def usd(cny, markup=2.0, fx=6.6):
    return None if cny is None else int(round(cny * markup / fx))
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cny", nargs="+", type=float); ap.add_argument("--markup", type=float, default=2.0); ap.add_argument("--fx", type=float, default=6.6)
    a = ap.parse_args(); print(" ".join(str(usd(c, a.markup, a.fx)) for c in a.cny))
