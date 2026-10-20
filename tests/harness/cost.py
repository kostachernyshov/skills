#!/usr/bin/env python3
"""Time and tokens per stage, from the Claude Code session files of a test run.

Usage: cost.py RUN_DIR [RUN_DIR ...]
RUN_DIR is a folder of run_scenario.py (it holds proj/ and log/). The script reads the
session file of the agent and the files of its subagents in ~/.claude/projects/.

Tokens: "fresh" = input + cache write (new text the model reads), "cache" = cache read
(the old context read again on each call), "out" = output. Each API call is counted once.
Minutes: active time; a gap over 10 minutes (a usage limit, a wait) is not counted.
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

PROJECTS = os.path.expanduser("~/.claude/projects")
GAP = 600
STAGE_OF = [(r"skills:ask-kosta", "ask-kosta"), (r"skills:setup-project", "setup-project"),
            (r"skills:grill-me", "grill-me"), (r"skills:planner", "planner"),
            (r"^Run the plan", "analysis"), (r"skills:editor", "editor"),
            (r"skills:designer", "designer"), (r"skills:publisher", "publisher"),
            (r"^The test is over", "friction report")]
ORDER = [s for _, s in STAGE_OF]


def ts(entry):
    return datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00")).timestamp()


def session_file(run_dir):
    enc = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(os.path.join(run_dir, "proj")))
    files = [f for f in glob.glob(os.path.join(PROJECTS, enc, "*.jsonl"))]
    return max(files, key=os.path.getsize) if files else None


def usage_events(path):
    """(time, model, fresh, cache, out) once per API call."""
    seen, out = set(), []
    for line in open(path):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") != "assistant":
            continue
        m = e.get("message") or {}
        u = m.get("usage")
        key = (m.get("id"), e.get("requestId"))
        if not u or key in seen:
            continue
        seen.add(key)
        fresh = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
        out.append((ts(e), m.get("model", "?"), fresh, u.get("cache_read_input_tokens", 0),
                    u.get("output_tokens", 0)))
    return out


def run_cost(run_dir):
    main = session_file(run_dir)
    if not main:
        return None
    bounds, times = [], []
    for line in open(main):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if "timestamp" in e:
            times.append(ts(e))
        if e.get("type") == "user" and isinstance((e.get("message") or {}).get("content"), str):
            text = e["message"]["content"]
            for pat, stage in STAGE_OF:
                if re.search(pat, text, re.M):
                    bounds.append((ts(e), stage))
                    break
    bounds.sort()

    def stage_at(t):
        cur = "other"
        for bt, s in bounds:
            if bt <= t:
                cur = s
        return cur

    tok = defaultdict(lambda: defaultdict(int))
    events = usage_events(main)
    sub_dir = main[:-6] + "/subagents"
    n_sub = 0
    for f in glob.glob(os.path.join(sub_dir, "*.jsonl")):
        n_sub += 1
        events += [(t, mdl, a, b, c) for t, mdl, a, b, c in usage_events(f)]
    for t, mdl, fresh, cache, out in events:
        s = stage_at(t)
        tok[s]["fresh"] += fresh
        tok[s]["cache"] += cache
        tok[s]["out"] += out
        tok[s]["calls"] += 1
        tok["_models"][mdl] += fresh + cache + out
    times.sort()
    for a, b in zip(times, times[1:]):
        if b - a < GAP:
            tok[stage_at(a)]["sec"] += b - a
    tok["_sub"]["n"] = n_sub
    return tok


def k(x):
    return f"{x / 1e3:,.0f}"


def main(dirs):
    stage = defaultdict(lambda: defaultdict(float))
    rows = []
    for d in dirs:
        c = run_cost(d)
        if c is None:
            print(f"{d}: no session file", file=sys.stderr)
            continue
        tot = defaultdict(float)
        for s, v in c.items():
            if s.startswith("_"):
                continue
            for key, x in v.items():
                stage[s][key] += x
                tot[key] += x
        rows.append((os.path.basename(os.path.abspath(d)), tot, c["_sub"]["n"], dict(c["_models"])))
    n = len(rows)
    print(f"Per stage, mean of {n} runs. Tokens in thousands.\n")
    print("| Stage | active min | API calls | fresh in | cache read | out |\n|---|---|---|---|---|---|")
    for s in ORDER + ["other"]:
        if s in stage:
            v = stage[s]
            print(f"| {s} | {v['sec'] / 60 / n:.1f} | {v['calls'] / n:.0f} | {k(v['fresh'] / n)} | "
                  f"{k(v['cache'] / n)} | {k(v['out'] / n)} |")
    print("\n| Run | active min | API calls | subagents | fresh in | cache read | out |\n|---|---|---|---|---|---|---|")
    for name, t, ns, _ in rows:
        print(f"| {name} | {t['sec'] / 60:.0f} | {t['calls']:.0f} | {ns} | {k(t['fresh'])} | {k(t['cache'])} | {k(t['out'])} |")
    models = defaultdict(float)
    for *_, m in rows:
        for key, x in m.items():
            models[key] += x
    print("\nAll tokens by model: " + ", ".join(f"{m} {x / 1e6:.1f} M" for m, x in sorted(models.items())))


if __name__ == "__main__":
    main(sys.argv[1:])
