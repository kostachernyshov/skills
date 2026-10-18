---
name: decision-brief
description: Write a one-page brief for the person who asked the question. It gives the answer, the evidence, the confidence, and the options for the decision.
disable-model-invocation: true
---

# Decision brief

The reader is the person who asked. The reader makes the decision. The brief gives the reader everything for the decision on one page.

## Steps

1. Read the `question`, `decision`, `checks`, and `result` in `run.yaml`.
2. If any check is `fail`, stop. Tell the person. A brief does not hide a failed check.
3. Write the brief with [TEMPLATE.md](TEMPLATE.md). Keep the text to 400 words or fewer. The options table does not count. Use 1 or 2 figures.
4. Use the words of the reader, not the words of the method. Write "patients with ER-negative tumors", not "ER=0 stratum".
5. Give each option a cost of error and say if the decision can be reversed.
6. In "Confidence and limits", name each `warn` that can change the decision. Add one line: "Other technical warnings: see run.yaml."
7. Save the brief as `runs/RNN-<slug>/out/brief.md`. Refer to figures and tables by file name only (`fig-km.png`), not by path. The skill "release" copies them next to the brief.

## Numbers

- Each number from the analysis must exist in a table or a figure of the same run. Give the file name in brackets.
- A plain-language form of a number ("6 in 100") is allowed if the source number is in a table.
- A number from a paper needs the reference, not a table.

## Done when

- The brief has the 6 sections of the template.
- The answer is one sentence in the first 3 lines.
- The text is 400 words or fewer, without the options table.
