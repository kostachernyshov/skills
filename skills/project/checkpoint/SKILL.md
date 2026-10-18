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
3. For each run in `runs/`, make sure that `run.yaml` has the correct status.
4. Find files that break the rules of the skill "project-order". Move them or delete them. Ask the person before you delete a file outside `scratch/`.
5. Empty `scratch/`, or tell the person what is in it.
6. Commit with the message `checkpoint: <next step>`.

## Done when

- A new reader can say the next step after reading `CLAUDE.md` and 3 `LOG.md` entries.
- No file is outside its place.
