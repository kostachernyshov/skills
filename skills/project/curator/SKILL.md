---
name: curator
description: Keep the project memory and file order. The State section in CLAUDE.md is built from run.yaml files by a script, not written by hand. Use each time you create, save, or move a file in a project that has runs/ and releases/ folders, and at the end of a work session.
---

# Curator

The project memory is computed, not written. The source of truth is `run.yaml` in each run. A script builds the `State` section in `CLAUDE.md` from these files.

## How it runs

- In Claude Code, the plugin hook runs the script after each answer of the agent (the `Stop` event). You do not start it.
- Without the hook (Codex, or a manual install), run it yourself at the end of a session: `python3 <this skill>/scripts/curate.py <project root>`.
- The script is fast and has no model. It writes `CLAUDE.md` only when the State changes. It does not delete or move files.

## What the script writes

The block between `<!-- curator:begin -->` and `<!-- curator:end -->` in `CLAUDE.md`:

- **Known**: each run where all checks and controls are `pass`, `warn`, or `n/a`, with its `result`.
- **Open**: each check or control with `todo` or `fail`, each line in the `todo` list of a run, each judge veto, and each `run.yaml` that does not parse.
- **Order**: each file that is not in its place (see the table below).
- **Next step**: one line. You write this line. The script keeps it. It is the only line in the block that you change.

The script never moves an item to "Known". Only the checks move it. To close an item, do the work and change its status in `run.yaml`.

## Where a file goes

| File | Place |
|---|---|
| Input data | `data/` (read only, not in git) |
| Small reference file from a paper or a database (weights, gene lists) | `data/ref/` (in git; write the source in `CLAUDE.md`) |
| Code for one iteration, including cohort selection | `runs/RNN-<slug>/code/` |
| Tables and figures from one iteration | `runs/RNN-<slug>/out/` |
| Facts about one iteration: plan, checks, doubts, result | `runs/RNN-<slug>/run.yaml` |
| What the client sees | `releases/vN-<YYYY-MM-DD>/` (only the skill "publisher" writes here) |
| A decision of the person (plan accepted, post-hoc change, override, release) | one entry in `LOG.md` |
| Anything temporary | `scratch/` |

## Patient-level tables

A table with one row per patient or per sample can identify people. Name it `<what>.private.csv`. Git ignores `*.private.*`. Summary tables (counts, statistics) go in git.

## Runs

- Start a new run when the question, the sample set, or the method changes. Keep the same run for small fixes.
- Number runs in order: `R01`, `R02`, ... Add a short slug: `R02-no-normals`.
- Do not delete a run. Set `status: dropped` and write the reason in `notes`.
- Status values: `open` (in work), `candidate` (checks done, can go to a client), `superseded` (a later run replaces it; name the run in `notes`), `dropped`, `shipped` (in a release).

## Edit run.yaml safely

- Each key appears once. Change a value in place. Do not add a second copy of a key.
- Put text with a colon (`:`) in double quotes.
- After each edit, parse the file: `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" runs/RNN-<slug>/run.yaml`. Fix any error before you continue.

## Do not create

- Handoff files, summary files, notes files, or a README in a run. The State block and `run.yaml` hold this.
- Copies of a table with a new suffix (`_v2`, `_final`). Start a new run or overwrite the file in the same run.
- A `.md` file in a run other than `out/brief.md`.

## Names

- Lowercase, hyphens, no spaces: `de-genes-er-pos-vs-neg.csv`. Python files that other code imports need underscores; keep the style that the project already uses.
- The name says what the file contains, not when it was made.
- Figures: `fig-<what>.png`. Tables: `<what>.csv`.

## At the end of a work session

1. Make sure each doubt is a `todo` line in `run.yaml`, not only a sentence in the chat.
2. Write the `Next step` line in the State block.
3. Read the `Order` line. Move each listed file to its place. Ask the person before you delete a file outside `scratch/`.
4. If anything changed, commit with the message `curator: <next step>`.

## Done when

- The State block exists and the `Order` line says `none`.
- Each `run.yaml` parses and has a status.
- The `Next step` line names one action.
