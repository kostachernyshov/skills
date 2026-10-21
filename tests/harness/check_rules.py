#!/usr/bin/env python3
"""Check the solution model and the project rules in a test project (from 0.8.0).

Prints facts for the grader: the model block, grilling and model entries, RULE entries,
the rules section, and when the agent asked for a rule versus when it wrote the rule.

Usage: check_rules.py <run dir with proj/ and log/>
"""
import glob
import json
import os
import re
import sys


def turns(log):
    out = []
    for path in sorted(glob.glob(os.path.join(log, "turn-*.jsonl"))):
        n = int(re.search(r"turn-(\d+)", path).group(1))
        edits = []
        for line in open(path):
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            for c in (ev.get("message") or {}).get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    s = json.dumps(c.get("input"))
                    if "RULE-" in s and ("CLAUDE.md" in s or "LOG.md" in s):
                        edits.append(c.get("name"))
        out.append((n, edits))
    return out


def main(run):
    proj, log = os.path.join(run, "proj"), os.path.join(run, "log")
    claude = open(os.path.join(proj, "CLAUDE.md")).read() if os.path.exists(os.path.join(proj, "CLAUDE.md")) else ""
    logmd = open(os.path.join(proj, "LOG.md")).read() if os.path.exists(os.path.join(proj, "LOG.md")) else ""
    m = re.search(r"<!-- model:begin -->(.*?)<!-- model:end -->", claude, re.S)
    print("## model\n" + (m.group(1).strip() if m else "MISSING"))
    r = re.search(r"## Project rules\n(.*?)(\n## |\Z)", claude, re.S)
    print("\n## project rules\n" + (r.group(1).strip() if r else "MISSING"))
    print("\n## LOG entries")
    for h in re.findall(r"^## .*$", logmd, re.M):
        print(h)
    for kind in ("DECISION grilling", "DECISION model", "RULE", "DECISION deviation"):
        for e in re.findall(r"^## [^\n]*" + kind + r"[^\n]*\n(?:(?!^## ).*\n?)*", logmd, re.M):
            print("\n---\n" + e.strip())
    for path in sorted(glob.glob(os.path.join(proj, "runs", "*", "run.yaml"))):
        y = open(path).read()
        rm = re.search(r"^rules:.*?(?=^\w)", y, re.M | re.S)
        st = re.search(r"^status:.*$", y, re.M)
        vd = re.search(r"^verdict:.*$", y, re.M)
        print(f"\n## {path}\n" + (st.group(0) if st else "status: ?") + "\n" + (vd.group(0) if vd else "verdict: none"))
        print("rules block:\n" + (rm.group(0).strip() if rm else "MISSING"))
    print("\n## judge answers to Q6 (from the logs)")
    for path in sorted(glob.glob(os.path.join(log, "turn-*.jsonl"))):
        for q6 in sorted(set(re.findall(r"Q6: (?:yes|no)[^\\\n\"]{0,160}", open(path).read()))):
            print(os.path.basename(path) + ": " + q6)
    tr = json.load(open(os.path.join(log, "transcript.json")))
    print("\n## turns that mention a rule")
    edits = dict(turns(log))
    for t in tr:
        ask = bool(re.search(r"RULE-\d+", t["reply"]))
        if ask or edits.get(t["turn"]) or "RULE" in t["prompt"]:
            print(f"turn {t['turn']} step {t['step']}: prompt={t['prompt'][:70]!r} | rule-edit tools={edits.get(t['turn'])} | reply mentions RULE={ask}")


if __name__ == "__main__":
    main(sys.argv[1])
