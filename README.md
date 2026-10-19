# Bio decision skills

Skills for Claude Code (and other agents that read SKILL.md) for one path: from the question of a client to a decision that the client can trust.

This repository does not teach methods. Method catalogs exist (see `UPSTREAM.md`). This repository covers the layers around the method:

- understand the question before the work (`grilling`),
- keep the project in order (`setup-project`, `project-order`, `checkpoint`, `release`),
- check each result before you state it (`sanity-check`),
- give the person who asked a one-page decision brief and a short deck (`decision-brief`, `decision-deck`).

Scope of version 1: processed tabular data (expression tables, clinical tables, survival). No raw data.

## Start

Type `/ask-kosta` in a project. It tells you the next skill.

## Skills

| Skill | Who starts it | What it does |
|---|---|---|
| `ask-kosta` | person | Map of the flow. Tells the next skill. |
| `grill-me` | person | Starts `grilling`. |
| `grilling` | agent | Interview in rounds until the question and the decision are clear. |
| `setup-project` | person | Makes the project layout and two service files. |
| `project-order` | agent | Rules for where each file goes. |
| `checkpoint` | person | Saves the state instead of a handoff file. |
| `release` | person | Freezes a version for the client. |
| `to-analysis-plan` | person | Writes the plan and the "done" criterion into the first run. |
| `sanity-check` | agent | Checks before each result. |
| `decision-brief` | person | One page for the person who decides. |
| `decision-deck` | person | 4 to 6 slides from the brief for the decision meeting. |
| `deck-review` | agent | Two review rounds of the deck with the eyes of the reader; fixes overload and unclear messages. |

"Person" skills have `disable-model-invocation: true`. Type `/name` to start them. "Agent" skills start by themselves when the situation fits.

## Project layout

```
CLAUDE.md   # agent rules + State
LOG.md      # decisions and releases
data/       # input, read only
runs/       # iterations, each with run.yaml
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

Or copy the skills by hand:

Claude Code finds a skill only one level below the skills folder. Copy each skill folder, not the bucket folder:

```
for d in skills/ask-kosta skills/*/*/; do cp -r "$d" ~/.claude/skills/; done
```

Do not copy `skills/in-progress/` or `skills/deprecated/`.
