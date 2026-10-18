---
name: release
description: Freeze a version of the results for the client. Copy the chosen runs into releases/vN, record the source, tag the commit, and log it.
disable-model-invocation: true
---

# Release

A release is what the client saw. Nobody changes it after you make it. A fix is a new release.

## Steps

1. Ask the person which runs go into the release. One release can hold 2 or 3 variants. Each variant is one run.
2. Check that each chosen run has `status: candidate` and that all its `checks` are `pass` or have a written reason in `notes`. If not, stop and tell the person.
3. Make `releases/vN-<YYYY-MM-DD>/`. N is the last release number + 1.
4. Copy into it only the files that the client needs:
   - `brief.md` (make it with the skill "decision-brief"),
   - `tables/` and `figures/` that the brief uses.
   Do not copy code, intermediate tables, or logs.
5. Write `SOURCE.txt`: for each variant, the run id, the commit hash, the input files.
6. Set `status: shipped` in each chosen `run.yaml`.
7. Add a `RELEASE` entry to `LOG.md`: version, runs, what changed from the last release.
8. Commit. Tag the commit `vN`.

## Done when

- `releases/vN-<date>/` has `brief.md`, `SOURCE.txt`, and only the files the brief uses.
- The tag `vN` exists.
- `LOG.md` has the `RELEASE` entry.
