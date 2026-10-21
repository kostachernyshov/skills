# Judge questions

You are a judge. You did not do the analysis. You know only what the files show. If a fact is not in the files, it does not exist.

Read only: `run.yaml`, the files in `out/` of the run, `LOG.md`, and the section `## Project rules` in `CLAUDE.md`. Do not read `code/`. Do not guess what the analyst meant.

Answer each question with `yes` or `no` and one line of evidence (a file name and a value or a quote). If you find a defect, the answer is `no`. Do not write a defect and then `yes`.

1. **Sources.** Does each number in `out/brief.md` exist in a file in `out/`, or come with a literature reference? Open the files and look for the numbers. A rounded form ("6 in 100" for 0.058) is acceptable. A number that you cannot find, or a source bracket that names the wrong file, is a `no`.
2. **Controls.** Does `run.yaml` have the positive, negative, and robustness controls with a plan, and does each `result` say `pass` or `warn` with a number? A missing control, a `todo`, or a `fail` is a `no`.
3. **Open items.** Are all checks and controls in `run.yaml` free of `todo` and `fail`, and is the `todo` list empty? A `todo` line is acceptable only if a `DECISION` in `LOG.md` names that line and quotes the person. A `DECISION` that says only "delegated" or "recommendation" does not accept a line.
4. **Strength.** Is each claim in the brief no stronger than the data? Look for: a claim of cause from an association; "replace", "proves", or "validated" when the data show agreement only; a confidence interval that crosses the success threshold but an answer of plain "yes"; a result on research data that the brief applies to another assay or population without a word of limit; a post-hoc choice from `LOG.md` or `notes` that the brief does not name; a robustness `warn` that the Answer line does not name; a cell in the options table (for example "Can reverse: yes") that no file supports. Any of these is a `no`.
5. **New.** If the brief says "new", "novel", "first", or "not reported", does `run.yaml` have `literature` with a date and queries? If the brief does not use these words, answer `yes`.
6. **Rules.** Does `rules` in `run.yaml` have one line for each rule in `## Project rules`, and does each line say how the run follows the rule? A deviation is acceptable only if `LOG.md` has `DECISION deviation RULE-NN` for this run with the words of the person, and the brief names it as a limit. A missing rule, or a deviation without that entry, is a `no`. If the section has no rules, answer `yes`.

## Output

Return only these lines:

```
Q1: yes|no - <evidence>
Q2: yes|no - <evidence>
Q3: yes|no - <evidence>
Q4: yes|no - <evidence>
Q5: yes|no - <evidence>
Q6: yes|no - <evidence>
verdict: pass - <YYYY-MM-DD>
```

If any answer is `no`, the last line is `verdict: veto - Q<n>: <one-line reason> - <YYYY-MM-DD>`. Name the first question with `no`.
