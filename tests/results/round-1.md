# Round 1 (skills v0.1.0), 2026-10-18

Two fresh agents ran the full flow. Projects: `/mnt/project-files/skill-tests/round1/`.

## Scores (0/1/2; max 38 per scenario)

| Item | s1 TCGA ESR1 | s2 GSE7390 | Evidence |
|---|---|---|---|
| G1 rounds with recommendations | 2 | 2 | agent reports: 2 rounds each |
| G2 facts found in data | 2 | 2 | s1 read sample types and sex before asking; s2 found published weights |
| G3 decision + owner sentence | 2 | 2 | LOG.md DECISION entries |
| P1 layout | 2 | 2 | |
| P2 no extra service files | 2 | 2 | only CLAUDE.md, LOG.md, brief.md (+AGENTS.md pointer in s2) |
| P3 run.yaml valid | 0 | 0 | both files fail YAML parsing: leftover `todo` keys from the plan step |
| P4 LOG entries | 2 | 2 | SETUP, DECISION, RELEASE; removals logged |
| P5 State usable | 2 | 2 | |
| P6 release | 2 | 1 | s2 committed a per-patient score table; figures/ links break between run and release |
| C1 input checks with evidence | 2 | 2 | |
| C2 traps found | 1 | 2 | s1 found normals, metastases, males, Y-gene mismatches; did not compare the two ER columns. s2 found typo, ER split, time units, missing weights |
| C3 prior with numbers | 2 | 2 | Filipits 2021; Desmedt 2007 |
| C4 nothing invented | 2 | 2 | s2 weights came from Wang 2005 Table 3, 76/76 probes match; marked "not proof-read" |
| B1 six sections, <=400 words | 2 | 1 | s2 403 words |
| B2 answer early | 2 | 2 | |
| B3 options with cost and reversibility | 2 | 2 | |
| B4 warnings in limits | 2 | 1 | s2 bundled 9 warnings in one line |
| B5 numbers traceable | 1 | 1 | plain-language numbers and literature numbers had no rule |
| R1 agrees with literature | 2 | 2 | |
| **Total** | **34** | **32** | |

## What worked
- The flow from question to release ran end to end in both scenarios without help.
- Grilling with `assumed:` lines let the agent work while the client was away, and left a clear trail.
- Sanity checks found real traps: 114 normal samples, 7 metastases, 12 male patients, 3 "female" samples with Y-gene expression (s1); the "unkown" label, the ER-specific signature, days vs years (s2).
- The prior search changed the answer in s2: the "secret" signature weights are published. This is the most valuable finding for the client.
- Both briefs give a one-sentence answer and options with cost of error.

## What failed (grouped, with the fix in v0.2.0)
| # | Failure | Seen in | Fix |
|---|---|---|---|
| 1 | run.yaml invalid YAML in both runs | s1, s2 | RUN.yaml template has all fields; rule: edit values in place, never append a key twice; validate after each edit |
| 2 | grilling writes to LOG.md before it exists | s1, s2 | flow order: setup-project first, then grill-me |
| 3 | incoming/ vs data/, symlink fails on network disk, empty folders not in git, unknown provenance | s1, s2 | setup-project: move files, AGENTS.md pointer file, .gitkeep, "client file, source not verified" |
| 4 | no place for small reference files from papers | s2 | `data/ref/`, tracked in git |
| 5 | per-patient tables committed to git | s1, s2 | name them `*.private.csv`; ignored by git |
| 6 | no status for a check that does not apply | s1, s2 | add `n/a` with reason |
| 7 | no checks for a published signature or model (weights, cut-off transfer, optimism, convergence); EPV threshold unclear | s2 | new section in CHECKS.md; EPV: warn 5-10, fail <5 |
| 8 | two columns for the same variable not compared | s1 (grader) | new input check `duplicate-variables` |
| 9 | pre-registered rule gave an unusable result; no path | s1 | sanity-check: new run, LOG `DECISION post-hoc` |
| 10 | prior search not in grilling | s1, s2 | grilling step 2: search published results and check if the asset is public |
| 11 | brief: 400 words vs all warnings; derived numbers; literature numbers; broken figure paths | s1, s2 | limit excludes options table; only decision-relevant warnings; derived numbers OK; cite literature; flat release folder |
| 12 | release: warn blocks release; which commit hash | s1, s2 | warn with evidence is OK; record HEAD before the release commit |
| 13 | ask-kosta points to UPSTREAM.md outside the skill | s1 | list upstream resources inside the skill |
| 14 | README install: nested bucket folders are not found by Claude Code | grader | install instruction copies each skill folder flat |
