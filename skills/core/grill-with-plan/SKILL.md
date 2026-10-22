---
name: grill-with-plan
description: Start a grilling interview about the next run of my analysis, then write the plan with its threshold and controls and get my approval. Use before each new run.
disable-model-invocation: true
---

# Grill with plan

This skill joins the interview and the plan. It ends when the person approves the plan. It does not start the analysis.

## Steps

1. Find the id of the next run: the newest run without a `plan accepted` entry in `LOG.md`, or the highest run number + 1.
2. If `LOG.md` has a `DECISION grilling` entry whose `run` line names the next run, show its `question`, `decision`, and `method` in 3 lines. Ask: "Is the task of <RNN> still valid? yes / change".
   - On "yes", go to step 4.
   - On "change", go to step 3.
3. Call the Skill tool with "grilling".
4. Call the Skill tool with "planner".

## Done when

- `LOG.md` has a `DECISION grilling` entry for the run and a `plan accepted` entry for it, or the person stopped the work.
- The person knows the next step: `/analyze <RNN>`.
