# Brief writer

You write a one-page decision brief. You did not do the analysis. You know only what the files show.

Read only: `run.yaml` of the run, the files in `out/` of the run, and `LOG.md`. Do not read `code/`.

`<this skill>` is the folder of this file.

## Steps

1. Read `question`, `decision`, `success`, `success_source`, `context`, `controls`, `checks`, `result`, and `notes` in `run.yaml`. Read the `DECISION` entries in `LOG.md`.
   If `context` starts with `forced`, the brief starts with the warning block of [TEMPLATE.md](TEMPLATE.md), above the title. Fill in the numbers from `context`.
2. Write the brief with [TEMPLATE.md](TEMPLATE.md). Keep the text to 300 words or fewer. Tables, figure captions, and source brackets do not count. Embed the main figure that `done_when` names, at half width: `![<what it shows>](fig-<what>.png){width=50%}`. Use a figure that exists in `out/`.
3. Use the words of the reader, not the words of the method. Write "patients with ER-negative tumors", not "ER=0 stratum".
4. Give each option a cost of error and say if the decision can be reversed. Give each next step an owner. If the files name no owner, write `to be named by <who decides>`. Do not invent owners. If there is no date, write the event in the When column ("before the study").
5. If `success_source` is `agent` (in older runs: `assumed`), write the threshold in the Answer line ("No, at the threshold of 95% specificity that the agent chose"). Add one line in Evidence: how the answer changes at nearby thresholds.
6. In "Confidence and limits": name each `warn` that can change the decision; name each post-hoc choice from `LOG.md` or `notes`; name each `DECISION override` from `LOG.md` as a limit: the defect and why it does not change the decision, in the words of the entry. Add one line: "Other technical warnings: see run.yaml."
7. Save the brief as `runs/RNN-<slug>/out/brief.md`. Refer to figures and tables by file name only (`fig-km.png`), not by path.
8. Render it from the project root: `bash <this skill>/scripts/brief_pdf.sh runs/RNN-<slug>/out/brief.md`. It writes `out/brief.pdf` (A4) and prints the page count. If the count is more than 1, cut text, not font size. The script needs `pandoc` and LibreOffice. If they are not installed, say so and use the word limit only.
9. Return one line: the Answer sentence and the word count.

## Numbers

- Each number from the analysis must exist in a table or a figure in `out/`. Give the file name in brackets. For another run, add the run id: `[R01: cv-performance.csv]`.
- A plain-language form of a number ("6 in 100") is allowed if the source number is in a table.
- A number from a paper needs the reference, not a table.
- If a number that the reader needs is not in the files, do not write it. Say in your answer which number is missing.

## Claims

- Do not write a claim stronger than the data. Association is not cause. Agreement is not "replace".
- Do not write "new", "novel", or "first" unless `run.yaml` has `literature` with queries.

## Done when

- The brief has the 7 sections of the template: Question, Answer, Evidence, Confidence and limits, Options, Next steps, Not checked.
- The answer is one sentence directly after the Question line.
- The text is 300 words or fewer, without tables, captions, and source brackets.
- `out/brief.pdf` has 1 page, or you said that the renderer is not installed.
