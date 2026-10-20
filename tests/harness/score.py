#!/usr/bin/env python3
"""Print a score table from grade.py output. Usage: score.py GRADES_JSON [...]"""
import json
import re
import sys
from collections import defaultdict


def main(paths):
    rows, by_s = [], defaultdict(list)
    for path in paths:
        for proj, v in json.load(open(path)).items():
            run = re.search(r"/(s\d+-\d+)/", proj).group(1)
            src = v.get("items", v)
            items = {k: a[0] if isinstance(a, list) else a for k, a in src.items()
                     if re.fullmatch(r"[A-Z]\d+", k)}
            yes = sum(1 for a in items.values() if str(a).lower() == "yes")
            over = len(v.get("overclaims") or [])
            no = sorted(k for k, a in items.items() if str(a).lower() == "no")
            score = yes - over
            by_s[v["scenario"]].append(score)
            rows.append((run, score, yes, len(items), over, ",".join(no)))
    print("| Run | Score | Yes | Items | Overclaims | No |\n|---|---|---|---|---|---|")
    for r in sorted(rows):
        print("| " + " | ".join(map(str, r)) + " |")
    print("\n| Scenario | min | max | mean |\n|---|---|---|---|")
    for s, v in sorted(by_s.items()):
        print(f"| {s} | {min(v)} | {max(v)} | {sum(v) / len(v):.1f} |")


if __name__ == "__main__":
    main(sys.argv[1:])
