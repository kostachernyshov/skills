---
name: project-order
description: Rules for where to put each new file in an analysis project, how to name it, and what not to save. Use each time you create, save, or move a file in a project that has runs/ and releases/ folders.
---

# Project order

Each file has one correct place. A file that has no place is not saved.

## Where a file goes

| File | Place |
|---|---|
| Input data | `data/` (read only, not in git) |
| Small reference file from a paper or a database (weights, gene lists) | `data/ref/` (in git; write the source in `CLAUDE.md`) |
| Code for one iteration, including cohort selection | `runs/RNN-<slug>/code/` |
| Tables and figures from one iteration | `runs/RNN-<slug>/out/` |
| Notes on one iteration | `runs/RNN-<slug>/run.yaml` (the `notes` field) |
| What the client sees | `releases/vN-<YYYY-MM-DD>/` (only the skill "release" writes here) |
| A decision | one entry in `LOG.md` |
| Where the work is now | the `State` section in `CLAUDE.md` |
| Anything temporary | `scratch/` |

## Patient-level tables

A table with one row per patient or per sample can identify people. Name it `<what>.private.csv`. Git ignores `*.private.*`. Summary tables (counts, statistics) go in git.

## Runs

- Start a new run when the question, the sample set, or the method changes. Keep the same run for small fixes.
- Number runs in order: `R01`, `R02`, ... Add a short slug: `R02-no-normals`.
- Each run has `run.yaml`. Copy [RUN.yaml](RUN.yaml) as the template.
- Do not delete a run. Set `status: dropped` and write the reason in `notes`.
- Status values: `open` (in work), `candidate` (checks done, can go to a client), `dropped`, `shipped` (in a release).

## Edit run.yaml safely

- Each key appears once. Change a value in place. Do not add a second copy of a key.
- Put text with a colon (`:`) in double quotes.
- After each edit, parse the file: `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" runs/RNN-<slug>/run.yaml`. Fix any error before you continue.

## Do not create

- Handoff files, summary files, or notes files. Update `CLAUDE.md` "State" or `LOG.md`.
- A README in a run folder. Use `run.yaml`.
- Copies of a table with a new suffix (`_v2`, `_final`). Start a new run or overwrite the file in the same run.
- A `.md` file in a run other than `out/brief.md`.

## Names

- Lowercase, hyphens, no spaces: `de-genes-er-pos-vs-neg.csv`.
- The name says what the file contains, not when it was made.
- Figures: `fig-<what>.png`. Tables: `<what>.csv`.

## Done when

- Each new file is in a place from the table above.
- Each `run.yaml` parses and has a status.
