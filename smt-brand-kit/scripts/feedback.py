#!/usr/bin/env python3
"""Record feedback on a deliverable so the skill improves run by run.

usage:
  feedback.py add  <area> "<what Jason said>" [--product X3100] [--rule "<the rule it becomes>"]
  feedback.py done <id> "<what was changed: file + version>"
  feedback.py list [--open]
area: voice | facts | landing | deck | manual | poster | video | workflow
Entries live in references/feedback-log.md (newest first). An entry is closed only when
its rule is written into the matching reference/script and the skill version is bumped."""
import datetime, os, re, sys

LOG = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "references", "feedback-log.md"))
HEAD = "# Feedback log\n\nOne entry per piece of feedback. Status open -> done once the rule is in the skill.\n\n"


def load():
    if not os.path.exists(LOG): return []
    return re.findall(r"^### (FB-\d+) .*?(?=^### FB-|\Z)", open(LOG, encoding="utf-8").read(), re.S | re.M)


def blocks():
    t = open(LOG, encoding="utf-8").read() if os.path.exists(LOG) else HEAD
    body = t[len(HEAD):] if t.startswith(HEAD) else t
    return [b for b in re.split(r"(?=^### FB-)", body, flags=re.M) if b.strip()]


def save(bs): open(LOG, "w", encoding="utf-8").write(HEAD + "".join(b if b.endswith("\n\n") else b.rstrip() + "\n\n" for b in bs))


a = sys.argv[1:]
cmd = a[0] if a else "list"
today = datetime.date.today().isoformat()
bs = blocks()
if cmd == "add":
    area, said = a[1], a[2]
    opt = dict(zip(a[3::2], a[4::2]))
    n = max([int(x) for x in re.findall(r"### FB-(\d+)", "".join(bs))] + [0]) + 1
    b = (f"### FB-{n:03d} [{area}] open - {today}\n- Product: {opt.get('--product', '-')}\n- Feedback: {said}\n"
         f"- Rule: {opt.get('--rule', '(write the general rule this implies)')}\n- Applied: -\n\n")
    save([b] + bs); print(f"FB-{n:03d} added")
elif cmd == "done":
    fid, what = a[1], a[2]
    for i, b in enumerate(bs):
        if b.startswith(f"### {fid} "):
            b = b.replace(" open - ", " done - ", 1); b = re.sub(r"- Applied: .*", f"- Applied: {what} ({today})", b); bs[i] = b
    save(bs); print(fid, "closed")
else:
    for b in bs:
        if "--open" in a and " open - " not in b.split("\n")[0]: continue
        print(b.strip(), "\n")
