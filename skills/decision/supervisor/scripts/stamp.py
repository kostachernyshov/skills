#!/usr/bin/env python3
"""Record which files the supervisor saw: report.md and each file in out/ that the report names.

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


def named_files(out):
    with open(os.path.join(out, "report.md")) as fh:
        text = fh.read()
    names = ["report.md"]
    for name in sorted(os.listdir(out)):
        if name != "report.md" and os.path.isfile(os.path.join(out, name)) and name in text:
            names.append(name)
    return names


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    run = sys.argv[1].rstrip("/")
    out, ry = os.path.join(run, "out"), os.path.join(run, "run.yaml")
    if not os.path.isfile(os.path.join(out, "report.md")) or not os.path.isfile(ry):
        print(f"stamp: {run} has no run.yaml or out/report.md")
        return 1
    checked = {n: digest(os.path.join(out, n)) for n in named_files(out)}
    line = "checked: " + json.dumps(checked)
    with open(ry) as fh:
        text = fh.read()
    if re.search(r"^checked:.*$", text, re.M):
        text = re.sub(r"^checked:.*$", lambda _: line, text, count=1, flags=re.M)
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
