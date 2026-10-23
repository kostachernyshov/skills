---
name: planner
description: Turn the grilling result into an analysis plan. Fix the success threshold and the controls before you look at the data, and get the approval of the person. Use when the skill "grill-with-plan" calls it.
user-invocable: false
---

# Planner

The plan says what result ends the analysis and which controls must pass. You write the plan before you see the outcome. The person approves it. This is the first point where the person takes responsibility. The planner does not run the analysis. The skill "analyze" runs it.

## Steps

1. Find the id of the new run: the newest run without a `plan accepted` entry in `LOG.md`, or the highest run number + 1. Each run starts with grilling. Read the newest `DECISION grilling` entry in `LOG.md`. Its `run` line must name the new run. Read the solution model in `CLAUDE.md`. It must have a `Confirmed` line with the name of a person, not `draft`. If either is missing, tell the person: "Run `/grill-with-plan` first. Each run starts with grilling." Stop.
2. Make the run folder `runs/R01-<slug>/` (or the next number). If the folder exists and has no `plan accepted` entry, use it. Copy [RUN.yaml](RUN.yaml) to `run.yaml` if it does not exist. Fill the fields in place:
   - `question`, `decision`, `success`, `success_source`, `inputs`, `context`: from the grilling entry of this run.
   - `samples`: the inclusion rule and the exclusion rule with counts. Write the cohort code in `code/` of this run to get the counts. Do not look at the outcome yet.
   - `method`: the comparison or the model, in one line. Name the package.
   - `prior`: the published result with the reference, or `none found`.
   - `done_when`: the number or the table that ends the analysis. Name the main figure: the figure that answers the question of the run (`out/fig-<what>.png`). Name the other figures that the reader needs. The report and the deck use the main figure.
   - `rules`: one key per rule in the section `## Project rules` of `CLAUDE.md`. The value says in one line how this run follows the rule. If the person chose to deviate in grilling, the value is `"deviation - LOG.md <date>"`. If the section has no rules, leave `rules: {}`.
   - `checks`: open `CHECKS.md` of the skill "checker". Take every check in the sections for your data types (always "Any table with samples"). Add one key per check. Value `todo`, or `n/a - <reason>`.
3. Write the three controls in `controls`. Each control has a `plan` and a `result: "todo"`.
   - **positive**: a known effect that must appear in these data. It must not be the predictor under test, and it must not be computed from the predictor. Give the expected sign. Give an expected size only with a source (a paper or a table); without a source, the rule is the sign and a clear effect (the confidence interval excludes no effect).
   - **negative**: the same analysis with shuffled outcome labels (or another variable with no known link), 100 times. Use 1000 times only when the real effect is near the pass limit. Compare the real result with the shuffled results, not with a fixed narrow band. Pass rule: the median shuffled effect is at the null value, and the real effect is outside the central 95% of the shuffled effects (for a "no effect" answer: inside it). A fixed band that is narrower than the sampling noise fails by design.
   - **robustness**: the answer at 2 or 3 nearby thresholds, and in each named subgroup that the decision cares about. Name the variants before the data. The result is the list of variants where the answer stays the same and where it changes.
   The positive and the negative control test the method. The robustness control tests the answer. The skill "checker" treats them in different ways.
   If the task is new and no published prior exists, these controls are the main evidence that the analysis works. Say this in `notes`.
   Fit the controls to the type of study. For an exploratory study without an outcome (for example new subtypes by clustering): positive = known biology separates as expected (for example sex by chrY genes); negative = shuffled data do not give the same clusters; robustness = the same clusters in 80% subsamples.
   If the person asks to remove a control, say: "⛔ Without the <name> control the supervisor answers no on Q2. Why does this control have no meaning for this question?"
   - A valid reason says why the control cannot test anything for this question (for example: no known effect exists in these data; the study is exploratory). "No time", "a waste of time", or "I decided" is not a reason. Keep the control and say so.
   - With a valid reason, add `## <YYYY-MM-DD> · DECISION override: veto Q2 <RNN>` to `LOG.md` with the words of the person. Set the `result` of the control to `"fail - removed by the person, override <YYYY-MM-DD>"`. The supervisor reads the entry at the end and passes the report with `pass - override Q2`. The report names the missing control as a limit.
4. Check that the data can answer the `success` threshold. Count the cases in the smallest key group. Compute the confidence interval that this count gives at the threshold (for example, 53 positives give a 95% interval of about plus or minus 6 points around 94% sensitivity). If the interval is wider than the margin, write it in `todo` and tell the person: the answer will be "cannot tell" unless the threshold or the data change.
5. Parse `run.yaml` (see the skill "curator"). Fix errors.
6. Show the plan to the person in 5 to 8 lines: question, samples, method, success threshold, the three controls, the project rules that apply (one line), and the `context` line ("<N> of 8 decisions came from the agent"). If a plan choice goes against a project rule, say so before the question. Do not ask the grilling questions again.
   - If 4 or fewer of 8 are `(agent)`, ask: "Approve this plan? yes / change".
   - If more than 4 of 8 are `(agent)`, ask: "<N> of 8 decisions came from me, not from you. Start anyway? yes / more questions". On "more questions", call the Skill tool with "grilling" for these lines. Then fill `run.yaml` again from the new grilling entry (step 2). Then do this step again. On "yes", add `## <YYYY-MM-DD> · DECISION override: start <RNN>` to `LOG.md` with the words of the person. Set `context` in `run.yaml` to `"forced - <N> of 8 (agent)"`. The report and the deck will show a warning.
7. Wait for the answer. Do not start the analysis. After "yes", add one `DECISION` entry to `LOG.md`: `plan accepted by <person>`. Commit.
8. Write the `Next step` line in the State block of `CLAUDE.md`: `/analyze <RNN>`. Tell the person: "Plan <RNN> is accepted. For a clean context, start a new session (/clear) and type /analyze <RNN>."

## Rules

- After the person approves, a change to the threshold, the controls, or the method is post-hoc. The skill "checker" says how to record it.
- Put all analysis code in `code/` of the run. Each script writes each number it computes to a table in `out/`.

## Done when

- `run.yaml` parses and has all fields of the template.
- `controls` has a positive, a negative, and a robustness control, each with a pass rule written before the data, or with `fail - removed by the person, override <date>` and its `DECISION override` entry.
- The negative control compares the real result with the shuffled results.
- `done_when` names one concrete output and the main figure.
- `LOG.md` has the `plan accepted` entry with the name of the person, and a `DECISION override: start` entry if more than 4 of 8 decisions are `(agent)`.
- `LOG.md` has a `DECISION grilling` entry for this run, and the solution model in `CLAUDE.md` is confirmed.
- `rules` has one line for each project rule.
- The analysis has not started.
