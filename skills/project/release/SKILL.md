---
name: release
description: Freeze a version of the results for the client. Copy the chosen runs into releases/vN, record the source, tag the commit, and log it.
disable-model-invocation: true
---

# Release

A release is what the client saw. Nobody changes it after you make it. A fix is a new release.

## Steps

1. Ask the person which runs go into the release. One release can hold 2 or 3 variants. Each variant is one run. If the person is not available, use the runs with `status: candidate` and write `assumed:` in the log entry.
2. Check each chosen run: `status: candidate`, no check is `fail` or `todo`. A run with `status: shipped` can go into a new release if only the brief or the deck changed, not the numbers. A `warn` with evidence is acceptable. If a check fails, stop and tell the person.
3. Commit all work. Record this commit hash: it is the source of the release.
4. Make `releases/vN-<YYYY-MM-DD>/`. N is the last release number + 1.
5. Copy into it, in one flat folder, only:
   - `brief.md` and `brief.pdf` from the run (if `brief.md` does not exist, tell the person to run `/decision-brief`),
   - `deck.pptx` and `deck.pdf` from the run (if they do not exist, tell the person to run `/decision-deck`),
   - each figure and table that the brief names.
   Do not copy code, intermediate tables, or `*.private.*` files. For 2 or more variants, add the run id to each file name.
6. Write `SOURCE.txt`: for each variant, the run id, the source commit from step 3, and each input file with its md5 checksum. Add one line: "The tag vN marks the release commit. The source commit is the analysis state before it."
7. Set `status: shipped` in each chosen `run.yaml`. For each other run with `status: candidate`, ask the person: `superseded`, `dropped`, or keep. If the person is not available, keep it and write it in `State`.
8. Add a `RELEASE` entry to `LOG.md`: version, runs, what changed from the last release.
9. Update `State` in `CLAUDE.md`: what was released, what the client must decide, next step.
10. Commit with the message `release vN`. Tag this commit `vN`.

## Done when

- `releases/vN-<date>/` has `brief.md`, `deck.pptx`, `SOURCE.txt`, and only the files the brief and the deck use.
- The tag `vN` exists.
- `LOG.md` has the `RELEASE` entry.
