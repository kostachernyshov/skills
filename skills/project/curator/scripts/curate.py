#!/usr/bin/env python3
"""Build the State block in CLAUDE.md from runs/*/run.yaml and list files out of place.

Usage:
  curate.py [project_root]      # manual run; prints the block
  curate.py --hook              # Claude Code Stop hook; reads the hook JSON on stdin

Deterministic, no model, idempotent: CLAUDE.md changes only when the block changes.
It never moves or deletes files. It never exits with an error code, so it never blocks the agent.
"""
import hashlib
import json
import os
import re
import sys

BEGIN = "<!-- curator:begin -->"
END = "<!-- curator:end -->"
OK_STATUS = {"pass", "warn", "n/a"}
OPEN_STATUS = {"todo", "fail"}
RUN_STATUS = {"open", "candidate", "superseded", "dropped", "shipped"}
INACTIVE = {"dropped", "superseded"}
ROOT_FILES = {"CLAUDE.md", "AGENTS.md", "LOG.md", ".gitignore"}
ROOT_DIRS = {"data", "runs", "releases", "scratch"}
RUN_DIR = re.compile(r"^R\d{2,}-[a-z0-9][a-z0-9-]*$")
BAD_NAME = re.compile(r"(_v\d+\b|_final\b|[ _-]copy\b|\(\d+\)|handoff|summary\.md$|notes\.md$)", re.I)
MAX_LINES = 15


def find_root(start):
    d = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(d, "CLAUDE.md")) and os.path.isdir(os.path.join(d, "runs")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def status_of(value):
    if isinstance(value, dict):
        value = value.get("result", "")
    if value is None:
        return "todo"
    text = str(value).strip()
    if not text:
        return "todo"
    first = re.split(r"\s+-\s+|\s", text, maxsplit=1)[0].lower().rstrip(":,;")
    return first


def load_runs(root, yaml):
    runs, errors = [], []
    runs_dir = os.path.join(root, "runs")
    for name in sorted(os.listdir(runs_dir)):
        path = os.path.join(runs_dir, name)
        if not os.path.isdir(path):
            continue
        ry = os.path.join(path, "run.yaml")
        if not os.path.isfile(ry):
            errors.append(f"runs/{name}: no run.yaml")
            continue
        try:
            with open(ry) as fh:
                data = yaml.safe_load(fh) or {}
            if not isinstance(data, dict):
                raise ValueError("not a mapping")
        except Exception as exc:  # noqa: BLE001 - report any parse problem
            errors.append(f"runs/{name}/run.yaml does not parse: {str(exc).splitlines()[0][:80]}")
            continue
        data["_dir"] = name
        data["_root"] = root
        runs.append(data)
    return runs, errors


def run_items(run):
    """Return (open_items, all_ok) for one run."""
    rid = run.get("id") or run["_dir"].split("-")[0]
    items, all_ok, n = [], True, 0
    for group in ("checks", "controls"):
        block = run.get(group) or {}
        if not isinstance(block, dict):
            continue
        for key, value in block.items():
            n += 1
            st = status_of(value)
            if st in OPEN_STATUS:
                items.append(f"{rid} {group}.{key}: {st}")
                all_ok = False
            elif st not in OK_STATUS:
                items.append(f"{rid} {group}.{key}: unknown status '{st}'")
                all_ok = False
    todo = run.get("todo") or []
    if isinstance(todo, str):
        todo = [todo]
    for t in todo:
        items.append(f"{rid} todo: {t}")
        all_ok = False
    verdict = str(run.get("verdict") or "")
    if verdict.lower().startswith("veto"):
        items.append(f"{rid} judge {verdict}")
        all_ok = False
    m = re.search(r"brief ([0-9a-f]{8})", verdict)
    brief = os.path.join(run["_root"], "runs", run["_dir"], "out", "brief.md")
    if m and os.path.isfile(brief):
        with open(brief, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()[:8]
        if digest != m.group(1):
            items.append(f"{rid} judge verdict is old: brief.md changed after it (run the judge again)")
            all_ok = False
    status = str(run.get("status", "")).strip()
    if status not in RUN_STATUS:
        items.append(f"{rid} status '{status}' is not valid")
        all_ok = False
    return items, all_ok and n > 0


def order_issues(root):
    issues = []
    for name in sorted(os.listdir(root)):
        if name.startswith("."):
            continue
        path = os.path.join(root, name)
        if os.path.isdir(path):
            if name not in ROOT_DIRS:
                issues.append(f"{name}/ (folder not in the layout)")
        elif name not in ROOT_FILES:
            issues.append(f"{name} (file at the root)")
    runs_dir = os.path.join(root, "runs")
    for name in sorted(os.listdir(runs_dir)):
        path = os.path.join(runs_dir, name)
        if name.startswith("."):
            continue
        if not os.path.isdir(path):
            issues.append(f"runs/{name} (file in runs/)")
            continue
        if not RUN_DIR.match(name):
            issues.append(f"runs/{name}/ (name is not RNN-slug)")
        for sub in sorted(os.listdir(path)):
            if sub.startswith("."):
                continue
            if sub not in {"run.yaml", "code", "out"}:
                issues.append(f"runs/{name}/{sub} (only run.yaml, code/, out/)")
        for dirpath, dirnames, filenames in os.walk(path):
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
            for fn in filenames:
                rel = os.path.relpath(os.path.join(dirpath, fn), root)
                if fn.endswith(".md") and rel != f"runs/{name}/out/brief.md":
                    issues.append(f"{rel} (.md file in a run)")
                elif BAD_NAME.search(fn):
                    issues.append(f"{rel} (name has a version or copy suffix)")
    return issues


def capped(lines):
    if len(lines) <= MAX_LINES:
        return lines
    return lines[:MAX_LINES] + [f"... and {len(lines) - MAX_LINES} more"]


def build_block(runs, errors, issues, next_step):
    known, open_items = [], list(errors)
    active = [r for r in runs if str(r.get("status", "")).strip() not in INACTIVE]
    for r in active:
        items, ok = run_items(r)
        open_items += items
        if ok:
            rid = r.get("id") or r["_dir"].split("-")[0]
            result = str(r.get("result") or "").strip() or "(no result written)"
            verdict = status_of(r.get("verdict")) if r.get("verdict") else "not judged"
            known.append(f"{rid} ({r.get('status')}, judge: {verdict}): {result}")
    question = ""
    for r in reversed(active):
        if r.get("question"):
            question = str(r["question"]).strip()
            break
    runs_line = ", ".join(f"{r.get('id') or r['_dir']} {r.get('status')}" for r in runs) or "none"
    lines = [BEGIN, "Built by the curator script from run.yaml. Do not edit by hand, except the Next step line.", ""]
    lines.append(f"- Question: {question or '(no run yet)'}")
    lines.append(f"- Runs: {runs_line}")
    lines.append("- Known:")
    lines += [f"  - {k}" for k in capped(known)] or ["  - nothing yet"]
    lines.append("- Open:")
    lines += [f"  - {o}" for o in capped(open_items)] or ["  - nothing"]
    lines.append("- Order: " + ("none" if not issues else f"{len(issues)} file(s) out of place"))
    lines += [f"  - {i}" for i in capped(issues)]
    lines.append(f"- Next step: {next_step}")
    lines.append(END)
    return "\n".join(lines), len(open_items), len(issues)


def current_next_step(text):
    m = re.search(r"^- Next step:\s*(.*)$", text, re.M)
    if m and m.group(1).strip():
        return m.group(1).strip()
    return "<the agent writes one action here>"


def write_state(claude_md, block):
    with open(claude_md) as fh:
        text = fh.read()
    if BEGIN in text and END in text:
        start = text.index(BEGIN)
        end = text.index(END) + len(END)
        new = text[:start] + block + text[end:]
    else:
        m = re.search(r"^## State[ \t]*$", text, re.M)
        if m:
            nxt = re.search(r"^## ", text[m.end():], re.M)
            stop = m.end() + nxt.start() if nxt else len(text)
            new = text[: m.end()] + "\n\n" + block + "\n\n" + text[stop:].lstrip("\n")
        else:
            new = text.rstrip("\n") + "\n\n## State\n\n" + block + "\n"
    if new != text:
        with open(claude_md, "w") as fh:
            fh.write(new)
        return True
    return False


def main():
    hook = "--hook" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    start = args[0] if args else os.getcwd()
    if hook:
        try:
            payload = json.load(sys.stdin)
            start = payload.get("cwd") or start
        except Exception:  # noqa: BLE001 - hook input is optional
            pass
    root = find_root(start)
    if root is None:
        if not hook:
            print("curator: no project here (needs CLAUDE.md and runs/).")
        return
    try:
        import yaml
    except ImportError:
        msg = "curator: PyYAML is not installed (pip install pyyaml). State not built."
        print(json.dumps({"systemMessage": msg}) if hook else msg)
        return
    claude_md = os.path.join(root, "CLAUDE.md")
    with open(claude_md) as fh:
        old = fh.read()
    seg = old[old.index(BEGIN):old.index(END)] if (BEGIN in old and END in old) else old
    runs, errors = load_runs(root, yaml)
    issues = order_issues(root)
    block, n_open, n_issues = build_block(runs, errors, issues, current_next_step(seg))
    changed = write_state(claude_md, block)
    if hook:
        if changed or n_issues:
            parts = ["curator: State updated" if changed else "curator: State unchanged",
                     f"{n_open} open item(s)"]
            if n_issues:
                parts.append(f"{n_issues} file(s) out of place, see CLAUDE.md State")
            print(json.dumps({"systemMessage": "; ".join(parts) + "."}))
    else:
        print(block)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - a hook must never break the session
        print(json.dumps({"systemMessage": f"curator: script error: {exc}"}))
    sys.exit(0)
