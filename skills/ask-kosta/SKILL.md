---
name: ask-kosta
description: Show which skill to use now in a bioinformatics analysis project, from the first question to the signed release.
disable-model-invocation: true
---

# Ask Kosta

This is a map. It does not run skills. Read the situation, then tell the person which skill to use next and why.

## Main flow: question to decision

1. `/setup-project`: make the layout once (skip if `CLAUDE.md` and `runs/` exist).
2. `/grill-me`: understand the question and the decision before any analysis. **The person answers.**
3. `/planner`: fix the success threshold and three controls before the data. **The person approves the plan.**
4. Say "run the plan". This is not a skill. The agent works in `runs/` and uses "checker" by itself. The curator hook keeps the State.
5. `/editor`: a fresh subagent writes the one-page brief. The "judge" checks trust. The "reviewer" checks clarity.
6. `/designer`: 4 to 6 slides from the brief, for the meeting where they decide.
7. `/publisher`: freeze what the client sees. Only without a judge veto. **The person signs.**

The person is responsible for the result. The three bold steps are where the person acts. An agent does not do them for the person.

## Other entries

| Situation | Skill |
|---|---|
| A result looks wrong or surprising | "checker" (ask the agent to run it) |
| The judge gave a veto | Fix the cause, then `/editor` again. Only the person can override, with a reason in `LOG.md`. |
| The question changed | `/grill-me` again, then `/planner` for a new run |
| The work session ends | Nothing. The curator hook updates the State. Without the hook, ask the agent to run "curator". |

## Under the flow (the agent uses them by itself)

- "grilling": the interview method.
- "checker": checks and controls before each result; doubts become `todo`.
- "curator": file order and the State block, built from `run.yaml` by a script.
- "judge": a fresh subagent answers 5 yes/no questions; one "no" is a veto.
- "reviewer": two review rounds of the deck and the brief with the eyes of the reader.

## Not in this repository

Raw data processing and pipelines. Use these instead:
- NGS pipelines: nf-core (https://nf-co.re), Seqera AI skills.
- Skills for one tool or database: K-Dense-AI/scientific-agent-skills, GPTomics/bioSkills.
- Databases and literature: mims-harvard/ToolUniverse, anthropics/life-sciences.

## How to answer

1. Look at the project: does `CLAUDE.md` exist? Read the State block. Which runs exist and what status? Is there a verdict? Is there a release?
2. Find the step in the main flow.
3. Say the next skill in one line and the reason in one line.
