---
name: ask-kosta
description: Show which skill to use now in a bioinformatics analysis project, from the first question to the decision brief.
disable-model-invocation: true
---

# Ask Kosta

This is a map. It does not run skills. Read the situation, then tell the person which skill to use next and why.

## Main flow: question to decision

1. `/setup-project`: make the layout once (skip if `CLAUDE.md` and `runs/` exist).
2. `/grill-me`: understand the question and the decision before any analysis.
3. `/to-analysis-plan`: write the question, the checks, and the "done" criterion in the first run.
4. Say "run the plan". This is not a skill. The agent works in `runs/` and applies "project-order" and "sanity-check" by itself (see step 7 of "to-analysis-plan").
5. `/decision-brief`: one page for the person who asked.
6. `/decision-deck`: 4 to 6 slides from the brief, for the meeting where they decide.
7. `/release`: freeze what the client sees: brief, deck, and the files they use.

## Other entries

| Situation | Skill |
|---|---|
| The work session ends | `/checkpoint` |
| A result looks wrong or surprising | "sanity-check" (ask the agent to run it) |
| The question changed | `/grill-me` again, then a new run |

## Under the flow (the agent uses them by itself)

- "grilling": the interview method.
- "project-order": where each file goes.
- "sanity-check": checks before each result.

## Not in this repository

Raw data processing and pipelines. Use these instead:
- NGS pipelines: nf-core (https://nf-co.re), Seqera AI skills.
- Skills for one tool or database: K-Dense-AI/scientific-agent-skills, GPTomics/bioSkills.
- Databases and literature: mims-harvard/ToolUniverse, anthropics/life-sciences.

## How to answer

1. Look at the project: does `CLAUDE.md` exist? Which runs exist and what status? Is there a release?
2. Find the step in the main flow.
3. Say the next skill in one line and the reason in one line.
