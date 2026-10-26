"""Filename rules: lowercase ascii, hyphen-separated, keyword-first, no rank prefix, unique, .mp4."""
import re
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+){1,11}\.mp4$")

def check(name):
    errs = []
    if not SLUG.match(name): errs.append("must match lowercase-hyphen-words.mp4 (2-12 words)")
    if re.match(r"^\d+[-_]", name): errs.append("no rank/number prefix")
    if len(name) > 90: errs.append("too long (>90 chars)")
    return errs
