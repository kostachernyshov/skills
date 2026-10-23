---
name: analyze
description: Run the accepted plan of a run, check the result, draw the figures, and write the brief that the judge checks. Use after /grill-with-plan, best in a new session.
disable-model-invocation: true
---

# Analyze

This skill does the analysis of one run from the files only: the plan in `run.yaml`, the grilling entry in `LOG.md`, and `CLAUDE.md`. A fresh session is best. Then the analysis uses only what the person accepted, and nothing that stayed in the chat.

```
0 gate → 1 needs → 2 environment → 3 input checks → 4 code
       → 5 figures → 6 controls and result checks → 7 brief → 8 report
```

## Steps

0. **Gate.** Find the run: the id that the person gave, or the newest run with `status: open` and a `plan accepted` entry. Check:
   - the solution model in `CLAUDE.md` has a `Confirmed` line with the name of a person, not `draft`;
   - `LOG.md` has a `DECISION grilling` entry and a `plan accepted` entry for this run;
   - if `context` in `run.yaml` starts with `forced` or has more than 4 of 8 `(agent)`, `LOG.md` has `DECISION override: start <RNN>`. A run from before version 0.9.0 has no `context`; skip this check for it.
   If one is missing, tell the person: "⛔ <RNN> has no accepted plan. Run /grill-with-plan first." Stop.
1. **Needs.** Read `run.yaml` and the project rules. List the data files, the packages, and the expected run time. Estimate the time of the controls: the time of one analysis run times the number of shuffles. Tell the person in 3 to 5 lines. Do not wait for an answer, except in these cases:
   - The controls take more than 10 minutes. Ask: "The controls take about <N> minutes. Start? yes / fewer shuffles".
   - A data file is missing. Stop.
2. **Environment.** Install only the packages that the plan names. Install them in `.venv/` in the project root. Never install as root or for the whole system. Write each package and its version in `run.yaml` under `env`. If a package does not install, stop and ask the person. Do not write a statistical method by hand when a package has it.
3. **Input checks.** Call the Skill tool with "checker" and run the input checks. A `fail` stops the work.
4. **Code.** Write the analysis code in `code/` of the run. Run it. Each script writes each number that it computes to a table in `out/`.
5. **Figures.** Draw the main figure that `done_when` names, and the other figures that the reader needs: `out/fig-<what>.png`. Put the plotting code in its own script in `code/`. Look at each figure before you continue.
6. **Controls and result checks.** Call the Skill tool with "checker" for the three controls, the result checks, and the `todo` list. A `fail` (except a `fail` with `override`), an open `todo`, or a post-hoc change stops the work. Ask the person as the checker says. Then set `status: candidate` and fill `result`.
7. **Brief.** Call the Skill tool with "editor". It writes the brief in a fresh context and calls the judge and the reviewer.
8. **Report.** Tell the person: the Answer line of the brief, the verdict (✅ pass or ⛔ veto with the question), and the next step (`/designer`, `/publisher`, or the fix of a veto). Write the `Next step` line in the State block of `CLAUDE.md`.

## Done when

- The gate passed, or the person knows why it did not.
- `run.yaml` has `env`, a status for each check and control, `status: candidate`, and `result`.
- `out/` has the tables, the main figure, and `brief.md` with `brief.pdf`.
- `run.yaml` has a judge `verdict` that is newer than the last change to the brief.
