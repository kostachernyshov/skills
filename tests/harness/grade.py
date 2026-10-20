#!/usr/bin/env python3
"""Blind grading of test projects with RUBRIC.md.

Each project is copied to a folder with a random name. The grader is a fresh headless Claude Code
session. It sees the copy, the rubric, the traps and the reference answer of the scenario. It does
not see the run number, the version, or the logs.

Usage: grade.py OUT_JSON SCENARIO_ID:PROJECT_DIR [SCENARIO_ID:PROJECT_DIR ...]
"""
import concurrent.futures as cf
import json
import os
import random
import re
import shutil
import string
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.dirname(HERE)
BLIND = os.environ.get("BLIND_DIR", "/tmp/blind")
MODEL = os.environ.get("GRADER_MODEL", "claude-opus-5-5")
sys.path.insert(0, HERE)
from run_scenario import clean_env  # noqa: E402

PROMPT = """You are a blind grader of an analysis project. The project folder is the current directory.
Do not change any file. Read the files you need: CLAUDE.md, LOG.md, runs/*/run.yaml, runs/*/out/*,
releases/*, and `git log --oneline --decorate`. For slides, convert with
`soffice --headless --convert-to pdf` into /tmp and read the text with pdftotext, or read the PDF.

The client question:
{question}

Reference answer (for R1 only):
{reference}

Rubric:
{rubric}

Traps of this scenario (one question each: "found and handled?"; a caveat without an action is "no"):
{traps}

Return only one JSON object, no other text:
{{"items": {{"J1": ["yes|no", "evidence"], "J2": [...], "J3": [...], "J4": [...], "J5": [...],
 "T1": [...], ... one per trap in the order given ...,
 "H1": [...], "H2": [...], "H3": [...], "O1": [...], "O2": [...], "O3": [...], "B1": [...], "B2": [...], "R1": [...]}},
 "overclaims": ["each claim stronger than the data, with the file"],
 "answer": "the answer of the brief in one line"}}
"""


def traps_for(scenario_id):
    text = open(os.path.join(TESTS, "README.md")).read()
    for line in text.splitlines():
        if line.startswith(f"| {scenario_id}"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            return [t.strip() for t in cells[-1].split(";") if t.strip()]
    raise SystemExit(f"no traps for {scenario_id}")


def grade_one(scenario_id, project):
    sdir = [d for d in os.listdir(os.path.join(TESTS, "scenarios")) if d.startswith(scenario_id)][0]
    sdir = os.path.join(TESTS, "scenarios", sdir)
    persona = open(os.path.join(sdir, "persona.md")).read()
    question = re.search(r'## What \w+ says first\n"(.+?)"\n', persona, re.S).group(1)
    traps = traps_for(sdir.split("/")[-1])
    name = "".join(random.choices(string.ascii_lowercase, k=10))
    blind = os.path.join(BLIND, name)
    shutil.copytree(project, blind, symlinks=True)
    prompt = PROMPT.format(
        question=question,
        reference=open(os.path.join(sdir, "reference.md")).read(),
        rubric=open(os.path.join(TESTS, "RUBRIC.md")).read(),
        traps="\n".join(f"T{i + 1}. {t}" for i, t in enumerate(traps)),
    )
    cmd = ["claude", "-p", prompt, "--model", MODEL, "--output-format", "json",
           "--dangerously-skip-permissions", "--setting-sources", ""]
    out = subprocess.run(cmd, cwd=blind, env=clean_env(), capture_output=True, text=True, timeout=3600)
    try:
        result = json.loads(out.stdout.strip().splitlines()[-1])["result"]
        data = json.loads(result[result.index("{"): result.rindex("}") + 1])
    except Exception as exc:  # noqa: BLE001
        data = {"error": str(exc), "raw": out.stdout[-2000:]}
    data["blind_name"] = name
    data["traps"] = traps
    return data


def main():
    out_path = sys.argv[1]
    jobs = [a.split(":", 1) for a in sys.argv[2:]]
    random.shuffle(jobs)
    results = {}
    with cf.ThreadPoolExecutor(max_workers=6) as pool:
        futs = {pool.submit(grade_one, s, p): (s, p) for s, p in jobs}
        for fut in cf.as_completed(futs):
            s, p = futs[fut]
            results[p] = {"scenario": s, **fut.result()}
            print("graded", p, flush=True)
    json.dump(results, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
