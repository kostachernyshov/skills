#!/usr/bin/env python3
"""Run one test scenario in a real Claude Code session with the plugin installed.

A driver types the person commands in order. A persona model answers the questions of the agent.
Each turn is a headless `claude -p` call that resumes the same session, so hooks, slash commands,
skills, and subagents work as they do for a user.

Usage:
  run_scenario.py --scenario tests/scenarios/s7-... --data DIR --project DIR --log DIR \
                  --plugin DIR [--model M] [--persona-model M] [--stop-after N]
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time

CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
TURN_TIMEOUT = 3600
LIMIT = "You've hit your session limit"

FRICTION = (
    "The test is over. Do not change any file now. Report in plain text with these headings:\n"
    "1. Skills used: each skill, when, and who started it (the person by a command, or you).\n"
    "2. Friction: each point where a skill was unclear, wrong, contradicted another skill, or slowed you. "
    "Quote the skill text.\n"
    "3. Not covered: what you did that no skill told you to do.\n"
    "4. Skills or rules you did not use, and why."
)

PERSONA_RULES = """You play a person in a test. Stay in the role below. You talk to an analysis agent.

Rules:
- Read the last message of the agent. If it asks you a question, asks for approval, or asks you to sign, answer in 1 to 6 short lines, as this person.
- Use only facts from your role. If your role does not have the answer, say: "I do not know. Use your recommendation."
- If the agent proposes a plan and it fits your goal, approve it with "yes".
- If the agent asks you to sign a release: sign ("yes, I sign") only if the agent says the judge gave no veto. If there is a veto, say "No. Fix the cause first." Never invent an override.
- If the message asks nothing of you, says the work is done, or only asks if it should continue or run the next step or command, reply exactly: NO_QUESTION. The next command comes from someone else.
- Do not do the analysis. Do not give numbers that are not in your role.
- Do not say what the answer of the analysis should be, and do not give your own recommendation on the decision. You wait for the analysis.

Your role:
"""


def clean_env():
    env = dict(os.environ)
    for key in list(env):
        if key in {
            "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_REMOTE_SESSION_ID", "CLAUDE_CODE_PROJECTS_SESSION",
            "CLAUDE_CODE_CHILD_SESSION", "CLAUDECODE", "CLAUDE_CODE_MESSAGING_SOCKET",
            "CLAUDE_CODE_MESSAGING_TOKEN", "CLAUDE_CODE_SYNC_SESSION_REFS", "CLAUDE_CODE_TEE_SDK_STDOUT",
            "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH", "CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD",
            "CLAUDE_ADDITIONAL_DIRECTORIES", "CLAUDE_CODE_SYNC_SKILLS", "CLAUDE_CODE_SYNC_PLUGINS",
            "CLAUDE_CODE_COORDINATOR_EXTRA_TOOLS",
        }:
            env.pop(key)
    env.update({
        "IS_SANDBOX": "1",
        "GIT_AUTHOR_NAME": "analyst", "GIT_AUTHOR_EMAIL": "analyst@example.org",
        "GIT_COMMITTER_NAME": "analyst", "GIT_COMMITTER_EMAIL": "analyst@example.org",
    })
    return env


def run_claude(args, cwd, log_path, prompt):
    cmd = [CLAUDE, "-p", prompt, "--output-format", "stream-json", "--verbose"] + args
    t0 = time.time()
    with open(log_path, "w") as fh:
        try:
            subprocess.run(cmd, cwd=cwd, env=clean_env(), stdout=fh, stderr=subprocess.STDOUT,
                           timeout=TURN_TIMEOUT, check=False)
        except subprocess.TimeoutExpired:
            fh.write(json.dumps({"type": "harness", "error": "timeout"}) + "\n")
    result, session = read_log(log_path)
    return result, session, round(time.time() - t0)


def read_log(log_path):
    result, session = None, None
    with open(log_path) as fh:
        for line in fh:
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("session_id"):
                session = ev["session_id"]
            if ev.get("type") == "result":
                result = ev
    return result, session


def persona_answer(persona, message, model, log_dir, n):
    prompt = "The agent wrote:\n\n<<<\n" + message[-6000:] + "\n>>>\n\nYour reply:"
    args = ["--model", model, "--tools", "", "--system-prompt", PERSONA_RULES + persona,
            "--setting-sources", "", "--max-turns", "1"]
    res, _, _ = run_claude(args, log_dir, os.path.join(log_dir, f"persona-{n:02d}.jsonl"), prompt)
    text = (res or {}).get("result") or "I do not know. Use your recommendation."
    return text.strip()


def truncate_session(project, session):
    """Cut the stored session at the first usage-limit message.

    A run that hits the limit keeps sending prompts that fail; the session file stores them.
    Without the cut, the resumed agent reads those prompts (for example "the test is over")."""
    key = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(project))
    path = os.path.join(os.path.expanduser("~/.claude/projects"), key, f"{session}.jsonl")
    if not os.path.exists(path):
        print(f"no session file {path}", flush=True)
        return
    lines = open(path).readlines()
    for i, line in enumerate(lines):
        if LIMIT in line:
            shutil.copy(path, path + ".before-cut")
            with open(path, "w") as fh:
                fh.writelines(lines[:i])
            print(f"session cut at line {i} of {len(lines)}", flush=True)
            return


def candidate_exists(project):
    for path in glob.glob(os.path.join(project, "runs", "*", "run.yaml")):
        with open(path) as fh:
            if re.search(r"^status:\s*(candidate|shipped)", fh.read(), re.M):
                return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--plugin", required=True)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--persona-model", default="claude-haiku-5-5")
    ap.add_argument("--stop-after", type=int, default=99)
    ap.add_argument("--resume", action="store_true", help="continue a run that stopped on a usage limit")
    a = ap.parse_args()

    persona = open(os.path.join(a.scenario, "persona.md")).read()
    m = re.search(r'## What \w+ says first\n"(.+?)"\n', persona, re.S)
    opening = m.group(1).strip() if m else ""
    os.makedirs(a.log, exist_ok=True)
    start_step, start_prompt, session, n, transcript = 0, None, None, 0, []
    if a.resume:
        old = json.load(open(os.path.join(a.log, "transcript.json")))
        bad = [t for t in old if t["reply"].startswith(LIMIT) or t["reply"] == "(no result)"]
        transcript = [t for t in old if t["turn"] < bad[0]["turn"]] if bad else old
        start_step, start_prompt = (bad[0]["step"], bad[0]["prompt"] + "\n\n(Your last turn was cut by a usage limit. Continue from where you stopped.)") if bad else (len(old), None)
        n = transcript[-1]["turn"] if transcript else 0
        for t in reversed(transcript):
            _, sid = read_log(os.path.join(a.log, f"turn-{t['turn']:02d}.jsonl"))
            if sid:
                session = sid
                break
        if session:
            truncate_session(a.project, session)
        print(f"resume at step {start_step}, turn {n + 1}, session {session}", flush=True)
    else:
        os.makedirs(os.path.join(a.project, "incoming"), exist_ok=True)
        for f in os.listdir(a.data):
            shutil.copy(os.path.join(a.data, f), os.path.join(a.project, "incoming", f))

    steps = [
        ("/skills:ask-kosta " + opening, 0),
        ("/skills:setup-project", 1),
        ("/skills:grill-me " + opening, 4),
        ("/skills:planner", 3),
        ("Run the plan.", 4),
        ("/skills:editor", 2),
        ("/skills:designer", 2),
        ("/skills:publisher", 3),
        (FRICTION, 0),
    ]
    agent_args = ["--plugin-dir", a.plugin, "--model", a.model, "--dangerously-skip-permissions"]
    for i, (prompt, loops) in enumerate(steps[: a.stop_after]):
        if i < start_step:
            continue
        if i == start_step and start_prompt:
            prompt = start_prompt
        tries = 0
        while True:
            n += 1
            args = agent_args + (["--resume", session] if session else [])
            res, sid, secs = run_claude(args, a.project, os.path.join(a.log, f"turn-{n:02d}.jsonl"), prompt)
            session = sid or session
            text = (res or {}).get("result") or "(no result)"
            if text.startswith(LIMIT):
                print(f"usage limit at turn {n}; stop. Run again with --resume.", flush=True)
                transcript.append({"turn": n, "step": i, "prompt": prompt, "reply": text, "seconds": secs, "cost": None})
                with open(os.path.join(a.log, "transcript.json"), "w") as fh:
                    json.dump(transcript, fh, indent=1)
                return 2
            transcript.append({"turn": n, "step": i, "prompt": prompt, "reply": text, "seconds": secs,
                               "cost": (res or {}).get("total_cost_usd")})
            with open(os.path.join(a.log, "transcript.json"), "w") as fh:
                json.dump(transcript, fh, indent=1)
            print(f"[{time.strftime('%H:%M:%S')}] turn {n} step {i} {secs}s: {prompt[:50]!r}", flush=True)
            if i == len(steps) - 1:
                with open(os.path.join(a.log, "friction.md"), "w") as fh:
                    fh.write(text)
                break
            if tries >= loops:
                break
            tries += 1
            answer = persona_answer(persona, text, a.persona_model, a.log, n)
            if answer.strip().startswith("NO_QUESTION"):
                if steps[i][0] == "Run the plan." and not candidate_exists(a.project) and tries < loops:
                    prompt = "Continue until the plan is done and the run is a candidate."
                    continue
                break
            prompt = answer
    print("done", session)


if __name__ == "__main__":
    sys.exit(main())
