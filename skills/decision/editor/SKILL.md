---
name: editor
description: Write a one-page report for the person who asked the question. A fresh subagent writes it from the files only. Then the supervisor checks trust and the reviewer checks clarity. Use when the skill "analyze" calls it, or when the person asks to write or change a report.
user-invocable: false
---

# Editor

The reader is the person who asked. The reader makes the decision. The report gives the reader everything for the decision on one page.

The agent that did the analysis remembers things that are not in the files. So a fresh subagent writes the report. If a number is not in the files, it is not in the report.

## Steps

1. Find the run. Read `run.yaml`. If any check or control is `fail` or `todo`, or the `todo` list is not empty, stop. Tell the person. A report does not hide an open item. Exception: an item that a `DECISION override: veto Q<n> <run>` entry in `LOG.md` names. The report names it as a limit, and the supervisor checks the reason.
2. Start a new subagent with the Agent tool. Give it only this prompt, with the paths filled in:

   > You are the editor. Read `<this skill>/WRITER.md` and follow it. The project root is `<path>`. The run is `runs/RNN-<slug>/`. Read only `run.yaml`, the files in `out/`, and `LOG.md`. Do not read `code/` or any other file.

   Do not give the subagent a summary of the work.
3. Read the report that the subagent wrote. You may change words and layout (for example to fit one page or to apply a fix of the reviewer). You may not add a number or a claim. If the report misses a fact that the reader needs, put the fact in a file in `out/` or in `run.yaml` first. Then start a new subagent.
   After each change, render the PDF again: `bash <this skill>/scripts/report_pdf.sh runs/RNN-<slug>/out/report.md`. It prints the page count.
4. Call the Skill tool with "reviewer" for the report.
5. Call the Skill tool with "supervisor". The supervisor runs last, so it checks the final words. If the verdict is `veto`, fix the cause and go back to step 2 or to the analysis. After the fix, call the Skill tool with "curator" and follow "Project rules" to propose a rule.
6. Write the `Next step` line in the State block of `CLAUDE.md`.

If you cannot start a subagent, tell the person. Then write the report yourself with [WRITER.md](WRITER.md) and use only the files.

## The supervisor always runs

The person cannot turn off the supervisor. If the person asks you to skip it, or to write `pass` by hand, say: "⛔ Without the supervisor there is no release." Then do step 5.

## Revision of a shipped report

If the numbers do not change (words, layout, figure style), change `out/report.md` in the same run. The tag of the last release keeps the old version. If a number changes, start a new run.

## Render a release copy

When the skill "publisher" asks you to render a copy in `releases/vN-<date>/`, run `bash <this skill>/scripts/report_pdf.sh <that report.md>`. Do nothing else.

## Done when

- `out/report.md` and `out/report.pdf` exist, and the PDF has 1 page (or the person knows that the renderer is not installed).
- A subagent wrote the report from the files.
- The supervisor ran after the last change of the agent to the report, and `run.yaml` has its `verdict`.
- `out/review-report.csv` has 2 rounds.
