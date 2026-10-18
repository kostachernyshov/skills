---
name: to-analysis-plan
description: Turn the grilling result into a short analysis plan with the question, the comparisons, the checks, and a clear "done" criterion.
disable-model-invocation: true
---

# To analysis plan

The plan says what result ends the analysis. Without it, the analysis does not stop.

## Steps

1. If the question is not clear, call the Skill tool with "grilling" first.
2. Write the plan in `runs/R01-<slug>/run.yaml` (the first run) as the fields below. If runs exist, write it in the next run. Do not make a separate plan file.
   - `question`: one sentence.
   - `decision`: the decision the result serves, and who makes it.
   - `samples`: the inclusion rule and the exclusion rule. Give counts.
   - `method`: the comparison or the model, in one line. Name the package.
   - `checks`: the list of checks from the skill "sanity-check" that apply. Mark each `todo`.
   - `prior`: the published result to compare with. Give the reference. Write `none found` if you did not find one.
   - `done_when`: the number, the table, or the figure that ends the analysis.
3. Show the plan to the person. Ask for "yes" or a change. If the person is not available, continue and write `assumed: plan` in `LOG.md`.
4. Add a `DECISION` entry to `LOG.md`: the plan is accepted.

## Done when

- `run.yaml` has all fields above.
- `done_when` names one concrete output.
