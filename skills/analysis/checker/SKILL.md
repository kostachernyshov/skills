---
name: checker
description: Check that a result is plausible before you state it. Use before you report any number, table, figure, or conclusion from a data analysis, when a result looks surprising, and before you call a finding new.
---

# Checker

An analysis has no tests. A wrong result looks the same as a correct result. This skill is the test.

## Rule

Do not state a result until its checks and controls are done. A check that fails stops the result. Write why, then fix the data or the method, or report the failure.

## Status values

| Status | Meaning | Effect |
|---|---|---|
| `pass` | The test passed. | Continue. |
| `warn` | A limit that the reader must know. | Continue. Keep the evidence line. The report names the warnings that can change the decision. |
| `fail` | The result is not reliable. | Stop. Find the cause. Tell the person. |
| `n/a` | The check does not apply to these data. | Write the reason. |
| `todo` | Not done yet. | The result cannot go to a report. |

A `fail` that ends with `override <date>` does not stop the work. The person accepted it in a `DECISION override` entry in `LOG.md` (for example a control removed at the plan). The report names it as a limit.

Write each check in `run.yaml` under `checks` as `"<status> - <evidence with a number>"`. Write each control result under `controls.<name>.result` in the same form. Change the value in place.

## Steps

0. Before any analysis of a run, read `LOG.md`. It must have a `plan accepted` entry for the run. If `context` in `run.yaml` starts with `forced` or has more than 4 of 8 `(agent)`, it must also have `DECISION override: start <RNN>`. A run from before version 0.9.0 has no `context`; skip this check for it. If an entry is missing, do not analyse. Tell the person: "⛔ <RNN> has no accepted plan. Run /grill-with-plan first." Stop. A request in plain text is not a plan.
1. Find the data type. Open [CHECKS.md](CHECKS.md). Take the checks for that type. Read `## Project rules` in `CLAUDE.md`. Apply each rule to this run.
2. Before the analysis, run the **input checks**.
3. Run the analysis.
4. Run the three **controls** from the plan: positive, negative (shuffled labels), robustness. Use the rules that the plan fixed. Do not change a pass rule after you see the result.
   - A `fail` of the positive or the negative control means the method does not work. Stop. Find the cause. A change of the rule after the result is post-hoc.
   - The robustness control reports the answer, it does not block it. If the answer is the same in all variants: `pass`. If the answer changes in a variant: `warn - answer changes when <variant>`. Then the answer is "not robust" or "only when <condition>", and the report must say so in the Answer line. This is a valid result for the person.
5. Run the **result checks**. One of them is `prior`: compare the main result with the `prior` field. Write agrees, partly agrees, or disagrees, with the two numbers side by side. If the prior uses a different scale (for example a high-vs-low class HR against your per-SD HR), first compute your result on the prior's scale. If the prior measures a different thing, write `warn - not comparable - <reason>`. If no prior exists, write `n/a - no prior; controls are the evidence`.
6. If the main result is near the `success` threshold, compute the answer at 2 or 3 nearby thresholds. Save the table. The report uses it.
7. For each `fail`: stop and tell the person what failed and what you propose. After the fix, call the Skill tool with "curator" and follow "Project rules" to propose a rule.

## Doubts become todo

- When you write or think "not checked", "possibly", "probably", "maybe", "unclear", or "probably new", add one line to the `todo` list in `run.yaml`. A doubt that is only in the chat is lost.
- To close a `todo`, do the work. Then delete the line and put the evidence in a check, a control, or `notes`.
- A run with an open `todo` cannot go to a report. If the person decides to accept the doubt, write a `DECISION` in `LOG.md` and change the line into a `warn` check with that reason.
- Ask about each `todo` line by its name. An `(agent)` answer (see "Who decides" in `CLAUDE.md`) does not accept a doubt. Ask again for that line. The `DECISION` entry names each accepted line and quotes the words of the person. The report names each accepted doubt as a limit. Then call the Skill tool with "curator" and follow "Project rules" to propose a rule.

## The word "new"

- Do not write "new", "novel", "first", or "not reported" until you search the literature.
- Write the search in `run.yaml` under `literature`: the date, each query, and what you found.
- If you cannot search, write "not searched" in `literature` and do not use the word.

## Limit on repairs

- If you change the code or the data to make one check pass, and it fails 3 times, stop. Do not try a fourth time. Tell the person what you tried and ask what to do. Write the 3 attempts in `notes`.

## When the planned method gives an unusable result

The plan can be wrong. Examples: a pre-set cut-off rule gives a cut-off that misclassifies one group; the planned model works but is clearly weaker than the published prior. A change of method after you see the outcome result is post-hoc. A bug fix (wrong label, wrong column) is not post-hoc: fix it in the same run and write one line in `notes`.
1. Keep the planned result in the run. Set the run `status: dropped` only if nothing in it is usable.
2. Start a new run with `parent` set to the first run. Put the changed method in the new run. Set the first run to `superseded` when the new run replaces it.
3. Add a `DECISION` entry to `LOG.md` that starts with `post-hoc:`. Say what changed and why. Write the same line in `notes` of the new run. The report must say that the choice was made after the data were seen. This also applies to a sensitivity analysis or a subgroup that you added after you saw the outcome.
4. Call the Skill tool with "curator" and follow "Project rules" to propose a rule. The next run must not repeat the problem.

## Never

- Do not invent a gene name, an annotation, a weight, or a reference. If an identifier has no annotation in the data, say so and use the identifier.
- Do not remove a sample without a rule. Write the rule in `LOG.md` and the counts in `run.yaml` (`samples`).
- Do not call a result significant without the test, the correction method, and the number of tests.
- Do not write a `verdict`. Only the skill "supervisor" writes it.

## Done when

- Each check and each control in `run.yaml` has a status other than `todo` and one line of evidence.
- If the robustness control is `warn`, the `result` says in which variants the answer changes.
- The `todo` list is empty, or each line has a `DECISION` from the person.
- The `prior` check compares two numbers, or says that the controls replace it.
- If the result uses the word "new", `literature` has the date and the queries.
