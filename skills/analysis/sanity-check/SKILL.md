---
name: sanity-check
description: Check that a result is plausible before you state it. Use before you report any number, table, figure, or conclusion from a data analysis, and when a result looks surprising.
---

# Sanity check

An analysis has no tests. A wrong result looks the same as a correct result. This skill is the test.

## Rule

Do not state a result until its checks are done. A check that fails stops the result. Write why, then fix the data or the method, or report the failure.

## Status values

| Status | Meaning | Effect |
|---|---|---|
| `pass` | The test passed. | Continue. |
| `warn` | A limit that the reader must know. | Continue. Keep the evidence line. The brief names the warnings that can change the decision. |
| `fail` | The result is not reliable. | Stop. Find the cause. Tell the person. |
| `n/a` | The check does not apply to these data. | Write the reason. |

Write each check in `run.yaml` under `checks` as `"<status> - <evidence with a number>"`. Change the `todo` value in place.

## Steps

1. Find the data type. Open [CHECKS.md](CHECKS.md). Take the checks for that type.
2. Before the analysis, run the **input checks**.
3. Run the analysis.
4. After the analysis, run the **result checks**. One of them is `prior`: compare the main result with the `prior` field. Write agrees, partly agrees, or disagrees, with the two numbers side by side. If the prior uses a different scale (for example a high-vs-low class HR against your per-SD HR), first compute your result on the prior's scale. If the prior measures a different thing, write `warn - not comparable - <reason>`.
5. If the main result is near the `success` threshold, compute the answer at 2 or 3 nearby thresholds. Save the table. The brief uses it.
6. For each `fail`: stop and tell the person what failed and what you propose.

## When the planned method gives an unusable result

The plan can be wrong. Examples: a pre-set cut-off rule gives a cut-off that misclassifies one group; the planned model works but is clearly weaker than the published prior. A change of method after you see the outcome result is also post-hoc: write it in `notes`. A bug fix (wrong label, wrong column) is not post-hoc: fix it in the same run and write one line in `notes`.
1. Keep the planned result in the run. Set the run `status: dropped` only if nothing in it is usable.
2. Start a new run with `parent` set to the first run. Put the changed method in the new run. Set the first run to `superseded` when the new run replaces it.
3. Add a `DECISION` entry to `LOG.md` that starts with `post-hoc:`. Say what changed and why. The brief must say that the choice was made after the data were seen. This also applies to a sensitivity analysis or a subgroup that you added after you saw the outcome.

## Never

- Do not invent a gene name, an annotation, a weight, or a reference. If an identifier has no annotation in the data, say so and use the identifier.
- Do not remove a sample without a rule. Write the rule in `LOG.md` and the counts in `run.yaml` (`samples`).
- Do not call a result significant without the test, the correction method, and the number of tests.

## Done when

- Each check in `run.yaml` has a status other than `todo` and one line of evidence.
- The `prior` check compares two numbers.
