---
name: ask-kosta
description: Show which skill to use now in a bioinformatics analysis project, from the first question to the signed release.
disable-model-invocation: true
---

# Ask Kosta

This is a map. It does not run skills and does not change files. Read the situation, then tell the person which skill to use next and why.

If the skills come as a plugin, each command has the plugin prefix. Write the command as the person must type it (for example `/kostachernyshov-skills:grill-me`). Find the prefix in the name of this skill.

## Main flow: question to decision

1. `/setup-project`: make the layout once (skip if `CLAUDE.md` and `runs/` exist).
2. `/grill-with-plan`: build the solution model (who gets the benefit, how, why it can work) and the task of the run, then the plan with the success threshold and three controls. **The person answers and approves the plan.** Each new run starts here. If more than half of the decisions came from the agent, the person must say "start anyway", and the report shows a red warning.
3. `/analyze <RNN>`: best in a new session (`/clear`). The agent runs the plan, uses "checker", draws the figures, and writes the one-page report. The "supervisor" checks trust. The "reviewer" checks clarity.
4. `/designer`: 4 to 6 slides from the report, for the meeting where they decide.
5. `/publisher`: freeze what the client sees. Only with a supervisor pass, or a veto that the person overrode with a valid reason. **The person signs.**

The person is responsible for the result. The bold steps are where the person acts. An agent does not do them for the person.

Only the person starts these skills: `/setup-project`, `/grill-me`, `/grill-with-plan`, `/analyze`, `/designer`, `/publisher`, `/animate`, `/ask-kosta`. The agent cannot start them.

## Other entries

| Situation | Skill |
|---|---|
| A result looks wrong or surprising | "checker" (ask the agent to run it) |
| The person asks for an analysis in plain text ("compute X", "just do it") | `/grill-with-plan`, then `/analyze`. Without an accepted plan the agent does not start. |
| The task is vague, and the person wants only to understand it | `/grill-me` (no plan) |
| The supervisor gave a veto | Fix the cause and ask the agent to rewrite the report. Only the person can override: name the defect and why it does not change the decision. A deadline is not a reason. |
| A new run: a new data type, a new question, or a merge of earlier runs | `/grill-with-plan`. Grilling asks if the solution model is still valid. |
| The question changed | `/grill-with-plan` for a new run |
| A large task: a description of the biology and work with the outcome in one request | `/grill-with-plan`. Grilling proposes a split into runs. The next runs are in the `later runs` line of `LOG.md`. |
| A report must change (words, layout) | Ask the agent to rewrite the report ("editor"). The supervisor runs again. |
| You changed the report, a figure, or the deck yourself | Nothing. `/publisher` shows the files that changed after the supervisor check. You choose: run the supervisor again, or keep them and sign. |
| A lesson must hold for later runs | Ask the agent to add a project rule ("curator"). Only you edit or delete rules, by hand in `CLAUDE.md`. |
| The person wants a short video that explains the design and the result to a reader who does not read reports | `/animate` (experimental). Only after `/analyze` wrote the report. The person accepts the voice-over and the storyboard. |
| The work session ends | Nothing. The curator hook updates the State. Without the hook, ask the agent to run "curator". |

## Under the flow (the agent uses them by itself)

- "grilling": the interview method. It builds the solution model and checks the project rules.
- "planner": the plan with the threshold and the controls. The person approves it.
- "editor": a fresh subagent writes the one-page report from the files, then calls the supervisor and the reviewer.
- "checker": checks and controls before each result; doubts become `todo`.
- "curator": file order, the State block built from `run.yaml` by a script, and the project rules.
- "supervisor": a fresh subagent answers 7 yes/no questions; one "no" is a veto. It always runs.
- "reviewer": two review rounds of the deck and the report with the eyes of the reader.

## Not in this repository

Raw data processing and pipelines. Use these instead:
- NGS pipelines: nf-core (https://nf-co.re), Seqera AI skills.
- Skills for one tool or database: K-Dense-AI/scientific-agent-skills, GPTomics/bioSkills.
- Databases and literature: mims-harvard/ToolUniverse, anthropics/life-sciences.

## How to answer

1. Look at the project: does `CLAUDE.md` exist? Is the solution model confirmed or `draft`? Does `LOG.md` have a grilling entry and a `plan accepted` entry for the next run? Does a `later runs` line name a run that does not exist yet? Read the State block. Which runs exist and what status? Is there a verdict? Is there a release?
2. Find the step in the main flow.
3. Say the next skill in one line and the reason in one line.
