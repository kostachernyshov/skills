---
name: decision-brief
description: Write a one-page brief for the person who asked the question. It gives the answer, the evidence, the confidence, and the options for the decision.
disable-model-invocation: true
---

# Decision brief

The reader is the person who asked. The reader makes the decision. The brief gives the reader everything for the decision on one page.

## Steps

1. Read the `question` and `decision` in `run.yaml`. Read the `checks` and the `result`.
2. If any check is `fail`, stop. Tell the person. A brief does not hide a failed check.
3. Write the brief with [TEMPLATE.md](TEMPLATE.md). Keep it to one page: 400 words or fewer, 1 or 2 figures, 1 table.
4. Use the words of the reader, not the words of the method. Write "patients with ER-negative tumors", not "ER=0 stratum".
5. Give each option a cost of error and say if the decision can be reversed.
6. Put each `warn` from the checks into "Confidence and limits".
7. Save the brief as `runs/RNN-<slug>/out/brief.md`. The skill "release" copies it into a release.

## Done when

- The brief has the 6 sections of the template.
- The answer is one sentence in the first 3 lines.
- Each number in the brief is in a table or a figure in the same run.
