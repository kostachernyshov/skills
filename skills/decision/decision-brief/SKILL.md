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
3. Write the brief with [TEMPLATE.md](TEMPLATE.md). Keep the text to 300 words or fewer. Tables, figure captions, and source brackets do not count. Embed 1 figure at half width: `![<what it shows>](fig-<what>.png){width=50%}`. Use the same figure file as the deck.
4. Use the words of the reader, not the words of the method. Write "patients with ER-negative tumors", not "ER=0 stratum".
5. Give each option a cost of error and say if the decision can be reversed. Give each next step an owner. If the person did not name an owner, write `to be named by <who decides>` in the Owner column. Do not invent owners. If there is no date, write the event in the When column ("before the study").
6. If `success_source` is `assumed`, write the threshold in the Answer line ("No, at the assumed threshold of 95% specificity"). Add one line in Evidence: how the answer changes at nearby thresholds.
7. In "Confidence and limits", name each `warn` that can change the decision. Add one line: "Other technical warnings: see run.yaml."
8. Save the brief as `runs/RNN-<slug>/out/brief.md`. Refer to figures and tables by file name only (`fig-km.png`), not by path. The skill "release" copies them next to the brief.
9. Render it from the project root: `bash <this skill>/scripts/brief_pdf.sh runs/RNN-<slug>/out/brief.md`. It writes `out/brief.pdf` (A4) and prints the page count. If the count is more than 1, cut text, not font size. The script needs `pandoc` and LibreOffice. If they are not installed, tell the person and use the word limit only.

## Revision of a shipped brief

If the numbers do not change (words, layout, figure style), change `out/brief.md` in the same run. The tag of the last release keeps the old version. If a number changes, start a new run.

## Numbers

- Each number from the analysis must exist in a table or a figure. Give the file name in brackets. For another run, add the run id: `[R01: cv-performance.csv]`.
- A plain-language form of a number ("6 in 100") is allowed if the source number is in a table.
- A number from a paper needs the reference, not a table.

## Done when

- The brief has the 7 sections of the template: Question, Answer, Evidence, Confidence and limits, Options, Next steps, Not checked.
- The answer is one sentence directly after the Question line.
- The text is 300 words or fewer, without tables, captions, and source brackets.
- `out/brief.pdf` has 1 page, or the person knows that the renderer is not installed.
