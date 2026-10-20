# Bio decision skills

Skills for Claude Code (and other agents that read SKILL.md) for one path: from the question of a client to a decision that the client can trust.

This repository does not teach methods. Method catalogs exist (see `UPSTREAM.md`). This repository covers the layers around the method. Each skill is one role with one clear action:

- understand the question before the work (`grill-me`, `grilling`),
- fix the threshold and the controls before the data (`planner`),
- check each result before you state it (`checker`),
- keep the project memory and order without manual notes (`setup-project`, `curator`),
- write the brief in a fresh context and judge it from the files only (`editor`, `judge`, `reviewer`),
- give the person a short deck and a signed release (`designer`, `publisher`).

The person is responsible for the result. The person acts at three points: the answers in grilling, the approval of the plan, and the signature of the release.

Scope of version 1: processed tabular data (expression tables, clinical tables, mutation calls, survival). No raw data.

## Start

Type `/ask-kosta` in a project. It tells you the next skill. As a plugin, the commands have the plugin prefix: `/skills:ask-kosta`.

## Skills

| Skill | Who starts it | What it does |
|---|---|---|
| `ask-kosta` | person | Map of the flow. Tells the next skill. |
| `setup-project` | person | Makes the project layout and two service files. |
| `grill-me` | person | Starts `grilling`. |
| `grilling` | agent | Interview in rounds until the question, the decision, and the success threshold are clear. |
| `planner` | person | Writes the plan in the first run: threshold, positive, negative, and robustness controls. The person approves it. |
| `checker` | agent | Checks and controls before each result. Doubts become `todo`. "New" only after a literature search. Stops after 3 failed repairs. |
| `curator` | hook + agent | A script builds the State in `CLAUDE.md` from `run.yaml` after each answer and lists files out of place. |
| `editor` | person | A fresh subagent writes the one-page brief from the files. Then calls `judge` and `reviewer`. |
| `judge` | agent | A fresh subagent answers 5 yes/no questions from the files only. One "no" is a veto. |
| `designer` | person | 4 to 6 slides from the brief for the decision meeting. Calls `reviewer`. |
| `reviewer` | agent | Two review rounds of the deck or the brief with the eyes of the reader. |
| `publisher` | person | Freezes a release. Only without a veto, and only after the person signs. |

"Person" skills have `disable-model-invocation: true`. Type `/name` to start them. "Agent" skills start by themselves when the situation fits. A person skill can call an agent skill, never another person skill.

The `curator` hook (`hooks/hooks.json`, event `Stop`) works in Claude Code when you install the plugin. With a manual install or in Codex, ask the agent to run the curator script.

## Project layout

```
CLAUDE.md   # agent rules + State (built by the curator script)
LOG.md      # decisions of the person and releases
data/       # input, read only
runs/       # iterations, each with run.yaml (plan, controls, checks, todo, verdict)
releases/   # what the client saw, never changed
scratch/    # temporary
```

## Install

As a Claude Code plugin (after the repository is public):

```
claude plugin marketplace add kostachernyshov/skills
claude plugin install skills@kostachernyshov
```

To update: `claude plugin marketplace update kostachernyshov`, then `claude plugin update skills@kostachernyshov`.

Codex (not tested yet) uses the same marketplace and reads `agents/openai.yaml` in each skill folder:

```
codex plugin marketplace add kostachernyshov/skills
codex plugin add skills@kostachernyshov
```

Or copy the skills by hand (the curator hook does not come with this route):

Claude Code finds a skill only one level below the skills folder. Copy each skill folder, not the bucket folder:

```
for d in skills/ask-kosta skills/*/*/; do cp -r "$d" ~/.claude/skills/; done
```

Do not copy `skills/in-progress/` or `skills/deprecated/`.
