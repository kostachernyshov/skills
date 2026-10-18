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
   - `checks`: one key for each check from the skill "sanity-check" that applies. Value `todo`. Use `n/a - <reason>` for a check that does not apply.
   - `prior`: the published result with the reference, or `none found`.
   - `done_when`: the number, the table, or the figure that ends the analysis.
3. Parse `run.yaml` (see "project-order"). Fix errors.
4. Show the plan to the person in 5 to 8 lines. Ask one question: "Start with this plan? yes / change". If the person is not available, continue and write `assumed: plan accepted` in `LOG.md`.
5. Add a `DECISION` entry to `LOG.md`: the plan is accepted.
6. After the analysis and the checks, set `status: candidate` and fill `result`.

## Done when

- `run.yaml` parses and has all fields of the template.
- `done_when` names one concrete output.
