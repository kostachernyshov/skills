#!/usr/bin/env python3
"""Record which files the supervisor saw: each file in out/, except the deck, the reviews, and report.pdf.

Usage:
  stamp.py runs/RNN-<slug>

Writes one line `checked: {"<file>": "<first 8 characters of sha256>", ...}` in run.yaml,
after the `verdict` line. A later change of one of these files shows in the State as
"changed after the supervisor check". It does not block the work.
"""
import hashlib
import json
import os
import re
import sys


def digest(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:8]


SKIP = re.compile(r"^(deck\.|review-|report\.pdf$|\.)")


def tracked_files(out):
    # The deck and the reviews come after the check; report.pdf is made from report.md.
    return [n for n in sorted(os.listdir(out)) if os.path.isfile(os.path.join(out, n)) and not SKIP.match(n)]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    run = sys.argv[1].rstrip("/")
    out, ry = os.path.join(run, "out"), os.path.join(run, "run.yaml")
    if not os.path.isfile(os.path.join(out, "report.md")) or not os.path.isfile(ry):
        print(f"stamp: {run} has no run.yaml or out/report.md")
        return 1
    checked = {n: digest(os.path.join(out, n)) for n in tracked_files(out)}
    line = "checked: " + json.dumps(checked)
    with open(ry) as fh:
        text = fh.read()
    old = re.compile(r"^checked:.*\n?(?:[ \t]+.*\n?)*", re.M)  # a flow or a block mapping
    if old.search(text):
        text = old.sub(lambda _: line + "\n", text, count=1)
    elif re.search(r"^verdict:.*$", text, re.M):
        text = re.sub(r"^(verdict:.*)$", lambda m: m.group(1) + "\n" + line, text, count=1, flags=re.M)
    else:
        text = text.rstrip("\n") + "\n" + line + "\n"
    with open(ry, "w") as fh:
        fh.write(text)
    print(f"stamp: {len(checked)} file(s): " + ", ".join(checked))
    return 0


if __name__ == "__main__":
    sys.exit(main())
