---
name: checkpoint
description: Save where the work is now, so that a person or a new agent session can continue. Use at the end of a work session instead of writing a handoff file.
disable-model-invocation: true
---

# Checkpoint

The next reader gets the full state from two places: the `State` section in `CLAUDE.md` and the last 3 entries in `LOG.md`.

## Steps

1. Update the `State` section in `CLAUDE.md`. Keep it at 20 lines or fewer. Replace old text. Do not add history.
   - Question, decision it serves, current run, open items, next step.
2. Add a `LOG.md` entry for each decision from this session that is not in the log.
3. For each run, parse `run.yaml` and make sure that the status is correct.
4. Find files that break the rules of the skill "project-order". Run `git status --porcelain` and `find . -path ./.git -prune -o -path ./data -prune -o -type f -print`. Compare each path with the table in "project-order". Look for: `.md` files other than `CLAUDE.md`, `AGENTS.md`, `LOG.md`, `out/brief.md`, `releases/*/brief.md`; names with `_v2`, `_final`, `copy`; files at the root that are not service files. Move them. Ask the person before you delete a file outside `scratch/`. Output files that the brief does not use can stay in `out/`.
5. In `scratch/`: move any file that is evidence for a check into the `out/` of its run. Then empty `scratch/`.
6. Commit with the message `checkpoint: <next step>`.

## Done when

- A new reader can say the next step after reading `CLAUDE.md` and 3 `LOG.md` entries.
- No file is outside its place.
