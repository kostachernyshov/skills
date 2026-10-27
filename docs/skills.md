# Skills and project layout

This page is the reference for all skills. The short version is in the [README](../README.md).

## Skills

| Skill | Who starts it | What it does |
|---|---|---|
| `ask-kosta` | person | Map of the flow. Tells the next skill. |
| `setup-project` | person | Makes the project layout and two service files. |
| `grill-me` | person | Starts `grilling`. |
| `grill-with-plan` | person | `grilling`, then `planner`. Ends when the person approves the plan. Each new run starts here. |
| `grilling` | agent | Interview in rounds until the solution model of the project and the task of the run are clear. Marks each decision `(person)` or `(agent)`. Checks the project rules. |
| `planner` | agent | Writes the plan: threshold, positive, negative, and robustness controls. The person approves it. If more than half of the decisions came from the agent, the person must say "start anyway". Does not run the analysis. |
| `analyze` | person | Runs the accepted plan, best in a new session: environment, code, figures, checks, then `editor`. Stops without an accepted plan. |
| `checker` | agent | Checks and controls before each result. Doubts become `todo`. "New" only after a literature search. Stops after 3 failed repairs. |
| `curator` | hook + agent | A script builds the State in `CLAUDE.md` from `run.yaml` after each answer and lists files out of place. Keeps the project rules. |
| `editor` | agent | A fresh subagent writes the one-page report from the files. Then calls `supervisor` and `reviewer`. |
| `supervisor` | agent | A fresh subagent answers 7 yes/no questions from the files only. One "no" is a veto. It always runs. It checks the reason of an override. |
| `designer` | person | 4 to 6 slides from the report for the decision meeting. Calls `reviewer`. |
| `reviewer` | agent | Two review rounds of the deck or the report with the eyes of the reader. |
| `publisher` | person | Freezes a release. Only with a supervisor pass or a valid override, and only after the person signs. |
| `animate` | person | Experimental (`skills/in-progress/`). A pixel-art video of 20 to 45 s from the accepted report: question, design, result, limit. Numbers come only from the result files. Checks the colors for color vision deficiency. |

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
