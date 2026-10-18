---
name: to-analysis-plan
description: Turn the grilling result into a short analysis plan with the question, the comparisons, the checks, and a clear "done" criterion.
disable-model-invocation: true
---

# To analysis plan

The plan says what result ends the analysis. Without it, the analysis does not stop.

## Steps

1. If `LOG.md` has no `DECISION` entry from grilling, call the Skill tool with "grilling" first.
2. Make the run folder `runs/R01-<slug>/` (or the next number). Copy the template `RUN.yaml` from the skill "project-order". Fill the fields in place:
   - `question`, `decision`: from the grilling entry.
   - `samples`: the inclusion rule and the exclusion rule with counts. Write the cohort code in `code/` of this run to get the counts.
   - `method`: the comparison or the model, in one line. Name the package.
   - `checks`: open `CHECKS.md` of the skill "sanity-check". Take every check in the sections for your data types (always "Any table with samples"). Add one key per check. Value `todo`, or `n/a - <reason>`.
   - `prior`: the published result with the reference, or `none found`.
   - `done_when`: the number, the table, or the figure that ends the analysis.
   - `success`, `success_source`: from the grilling entry.
   Put all analysis code in `code/` of the run. Use as many scripts as you need. Each script writes each number it computes to a table in `out/`.
3. Parse `run.yaml` (see "project-order"). Fix errors.
4. Show the plan to the person in 5 to 8 lines. Ask one question: "Start with this plan? yes / change". Do not ask the grilling questions again.
5. Add one `DECISION` entry to `LOG.md`: the plan is accepted. If the person is not available, add the line `assumed: plan accepted`.
6. Update `State` in `CLAUDE.md`: question, current run, next step. Commit.
7. After the analysis and the checks, set `status: candidate` and fill `result`.

## Done when

- `run.yaml` parses and has all fields of the template.
- `done_when` names one concrete output.
