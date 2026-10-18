---
name: sanity-check
description: Check that a result is plausible before you state it. Use before you report any number, table, figure, or conclusion from a data analysis, and when a result looks surprising.
---

# Sanity check

An analysis has no tests. A wrong result looks the same as a correct result. This skill is the test.

## Rule

Do not state a result until its checks are done. A check that fails stops the result. Write why, then fix the data or the method, or report the failure.

## Steps

1. Find the data type. Open [CHECKS.md](CHECKS.md). Take the checks for that type.
2. Before the analysis, run the **input checks**. Record each in `run.yaml` under `checks` as `pass`, `fail`, or `warn`, with one line of evidence (a number).
3. Run the analysis.
4. After the analysis, run the **result checks**. Record them the same way.
5. For each `fail`: stop. Find the cause. Tell the person what failed and what you propose.
6. For each `warn`: continue. Put the warning in the result text and in the brief.
7. Compare the main result with the `prior` in `run.yaml`. Write: agrees, partly agrees, or disagrees. Give the two numbers side by side.

## Never

- Do not invent a gene name, an annotation, or a reference. If an identifier has no annotation in the data, say so and use the identifier.
- Do not remove a sample without a rule and a `LOG.md` entry.
- Do not call a result significant without the test, the correction method, and the number of tests.

## Done when

- Each check in `run.yaml` has a status and one line of evidence.
- The main result has a comparison with the prior.
