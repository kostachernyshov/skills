#!/usr/bin/env python3
"""Table of skill calls in one test run: skill, turn, who started it.

"person" = a typed command; "agent" = a Skill tool call; "read" = the agent read or ran a file of the skill;
"subagent prompt" = the agent gave a skill file to a subagent.

Usage: skill_usage.py LOG_DIR
Reads turn-NN.jsonl (stream-json of the agent) and transcript.json from run_scenario.py.
"""
import collections
import glob
import json
import os
import re
import sys


KNOWN = {"ask-kosta", "setup-project", "grill-me", "grill-with-plan", "grilling", "planner", "analyze", "checker",
         "curator", "editor", "judge", "designer", "reviewer", "publisher"}
SKILL_FILE = re.compile(r"(?:/skills/(?:[a-z-]+/)?|[\s;'\"])([a-z-]+)/((?:SKILL|[A-Z]+)\.md|scripts/[\w.]+|RUN\.yaml|templates)")


def main(log_dir):
    transcript = {t["turn"]: t for t in json.load(open(os.path.join(log_dir, "transcript.json")))}
    calls = collections.OrderedDict()
    agents, hooks = [], 0
    for path in sorted(glob.glob(os.path.join(log_dir, "turn-*.jsonl"))):
        turn = int(re.search(r"turn-(\d+)", path).group(1))
        prompt = transcript.get(turn, {}).get("prompt", "")
        typed = prompt.split()[0].lstrip("/").split(":")[-1] if prompt.startswith("/") else None
        if typed:
            calls.setdefault(typed, []).append(f"t{turn} person")
        for line in open(path):
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "system" and ev.get("subtype") == "hook_response":
                hooks += 1
            msg = ev.get("message") or {}
            if ev.get("type") != "assistant" or not isinstance(msg.get("content"), list):
                continue
            nested = " (in subagent)" if ev.get("parent_tool_use_id") else ""
            for block in msg["content"]:
                if block.get("type") != "tool_use":
                    continue
                if block["name"] == "Skill":
                    name = str(block["input"].get("skill", "")).split(":")[-1]
                    calls.setdefault(name, []).append(f"t{turn} agent{nested}")
                elif block["name"] in ("Read", "Bash", "Agent", "Task"):
                    text = json.dumps(block["input"])
                    how = "subagent prompt" if block["name"] in ("Agent", "Task") else "read"
                    seen = set()
                    for m in SKILL_FILE.finditer(text):
                        if m.group(1) in KNOWN and m.group(1) not in seen:
                            seen.add(m.group(1))
                            calls.setdefault(m.group(1), []).append(f"t{turn} {how}{nested}")
                if block["name"] in ("Agent", "Task"):
                    agents.append(f"t{turn}: {block['input'].get('description', '')}{nested}")
    print("| Skill | Called | When (turn, by whom) |")
    print("|---|---|---|")
    names = ["ask-kosta", "setup-project", "grill-me", "grilling", "planner", "checker", "curator",
             "editor", "judge", "designer", "reviewer", "publisher"]
    for name in names + [n for n in calls if n not in names]:
        when = calls.get(name, [])
        counted = collections.Counter(when)
        text = ", ".join(f"{k} x{v}" if v > 1 else k for k, v in counted.items())
        print(f"| {name} | {'yes' if when else 'no'} | {text or '-'} |")
    print(f"\nSubagents ({len(agents)}):")
    for a in agents:
        print(f"- {a}")
    print(f"\nHook events seen in stream: {hooks}")


if __name__ == "__main__":
    main(sys.argv[1])
