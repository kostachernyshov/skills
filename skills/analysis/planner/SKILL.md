---
name: planner
description: Turn the grilling result into an analysis plan. Fix the success threshold and the controls before you look at the data, and get the approval of the person.
disable-model-invocation: true
---

# Planner

The plan says what result ends the analysis and which controls must pass. You write the plan before you see the outcome. The person approves it. This is the first point where the person takes responsibility.

## Steps

1. If `LOG.md` has no `DECISION` entry from grilling, call the Skill tool with "grilling" first.
2. Make the run folder `runs/R01-<slug>/` (or the next number). Copy [RUN.yaml](RUN.yaml) to `run.yaml`. Fill the fields in place:
   - `question`, `decision`, `success`, `success_source`: from the grilling entry.
   - `samples`: the inclusion rule and the exclusion rule with counts. Write the cohort code in `code/` of this run to get the counts. Do not look at the outcome yet.
   - `method`: the comparison or the model, in one line. Name the package.
   - `prior`: the published result with the reference, or `none found`.
   - `done_when`: the number or the table that ends the analysis, and one figure of the main result (`out/fig-<what>.png`). The brief and the deck use this figure.
   - `checks`: open `CHECKS.md` of the skill "checker". Take every check in the sections for your data types (always "Any table with samples"). Add one key per check. Value `todo`, or `n/a - <reason>`.
3. Write the three controls in `controls`. Each control has a `plan` and a `result: "todo"`.
   - **positive**: a known effect that must appear in these data. It must not be the predictor under test, and it must not be computed from the predictor. Give the expected sign. Give an expected size only with a source (a paper or a table); without a source, the rule is the sign and a clear effect (the confidence interval excludes no effect).
   - **negative**: the same analysis with shuffled outcome labels (or another variable with no known link), at least 200 times. Compare the real result with the shuffled results, not with a fixed narrow band. Pass rule: the median shuffled effect is at the null value, and the real effect is outside the central 95% of the shuffled effects (for a "no effect" answer: inside it). A fixed band that is narrower than the sampling noise fails by design.
   - **robustness**: the answer at 2 or 3 nearby thresholds, and in each named subgroup that the decision cares about. Name the variants before the data. The result is the list of variants where the answer stays the same and where it changes.
   The positive and the negative control test the method. The robustness control tests the answer. The skill "checker" treats them in different ways.
   If the task is new and no published prior exists, these controls are the main evidence that the analysis works. Say this in `notes`.
4. Check that the data can answer the `success` threshold. Count the cases in the smallest key group. Compute the confidence interval that this count gives at the threshold (for example, 53 positives give a 95% interval of about plus or minus 6 points around 94% sensitivity). If the interval is wider than the margin, write it in `todo` and tell the person: the answer will be "cannot tell" unless the threshold or the data change.
5. Parse `run.yaml` (see the skill "curator"). Fix errors.
6. Show the plan to the person in 5 to 8 lines: question, samples, method, success threshold, the three controls. Ask one question: "Approve this plan? yes / change". Do not ask the grilling questions again.
7. Wait for the answer. Do not start the analysis before the person says yes. Then add one `DECISION` entry to `LOG.md`: `plan accepted by <person>`. Commit. Then run the plan. The person does not need to type another command.
8. Write the `Next step` line in the State block of `CLAUDE.md`.
9. After the analysis and the checks, set `status: candidate` and fill `result`.

## Rules

- After the person approves, a change to the threshold, the controls, or the method is post-hoc. The skill "checker" says how to record it.
- Put all analysis code in `code/` of the run. Each script writes each number it computes to a table in `out/`.

## Done when

- `run.yaml` parses and has all fields of the template.
- `controls` has a positive, a negative, and a robustness control, each with a pass rule written before the data.
- The negative control compares the real result with the shuffled results.
- `done_when` names one concrete output.
- `LOG.md` has the `plan accepted` entry with the name of the person.
