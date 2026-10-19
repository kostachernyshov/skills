---
name: editor
description: Write a one-page brief for the person who asked the question. A fresh subagent writes it from the files only. Then the judge checks trust and the reviewer checks clarity.
disable-model-invocation: true
---

# Editor

The reader is the person who asked. The reader makes the decision. The brief gives the reader everything for the decision on one page.

The agent that did the analysis remembers things that are not in the files. So a fresh subagent writes the brief. If a number is not in the files, it is not in the brief.

## Steps

1. Find the run. Read `run.yaml`. If any check or control is `fail` or `todo`, or the `todo` list is not empty, stop. Tell the person. A brief does not hide an open item.
2. Start a new subagent with the Agent tool. Give it only this prompt, with the paths filled in:

   > You are the editor. Read `<this skill>/WRITER.md` and follow it. The project root is `<path>`. The run is `runs/RNN-<slug>/`. Read only `run.yaml`, the files in `out/`, and `LOG.md`. Do not read `code/` or any other file.

   Do not give the subagent a summary of the work.
3. Read the brief that the subagent wrote. Do not add numbers or claims from your memory. If the brief misses a fact that the reader needs, put the fact in a file in `out/` or in `run.yaml` first. Then start a new subagent.
4. Call the Skill tool with "judge". If the verdict is `veto`, fix the cause and go back to step 2 or to the analysis.
5. Call the Skill tool with "reviewer" for the brief.
6. If the reviewer changed a number or a claim, call the Skill tool with "judge" again.
7. Write the `Next step` line in the State block of `CLAUDE.md`.

If you cannot start a subagent, tell the person. Then write the brief yourself with [WRITER.md](WRITER.md) and use only the files.

## Revision of a shipped brief

If the numbers do not change (words, layout, figure style), change `out/brief.md` in the same run. The tag of the last release keeps the old version. If a number changes, start a new run.

## Done when

- `out/brief.md` and `out/brief.pdf` exist, and the PDF has 1 page (or the person knows that the renderer is not installed).
- A subagent wrote the brief from the files.
- `run.yaml` has `verdict: pass` that is newer than the last change to the brief.
- `out/review-brief.csv` has 2 rounds.
