# Round 2 (skills v0.2.0), 2026-10-18

Two fresh agents. s1 repeats the round 1 scenario (regression test). s3 is new (generalization test). Projects: `/mnt/project-files/skill-tests/round2/`.

## Scores (0/1/2; max 38)

| Item | s1 round 1 | s1 round 2 | s3 round 2 | Note |
|---|---|---|---|---|
| G1-G3 grilling | 6 | 6 | 6 | |
| P1 layout | 2 | 2 | 2 | .gitkeep and AGENTS.md fallback worked |
| P2 no extra service files | 2 | 2 | 2 | |
| P3 run.yaml valid | 0 | 2 | 2 | fixed: both files parse |
| P4 LOG entries | 2 | 2 | 2 | |
| P5 State usable | 2 | 1 | 2 | s1: State stayed "not yet defined" until checkpoint |
| P6 release | 2 | 2 | 2 | private tables now out of git; flat folder |
| C1 input checks | 2 | 2 | 2 | |
| C2 traps found | 1 | 2 | 2 | s1: two ER fields cross-tabulated (0 of 758 disagree). s3: OS built from two columns, "[Discrepancy]" removed, unspecified stage I kept, 1 sex mismatch |
| C3 prior with numbers | 2 | 1 | 2 | s1: only a kappa between pathologists was found; not comparable |
| C4 nothing invented | 2 | 2 | 2 | |
| B1-B5 brief | 9 | 9 | 10 | text 395 and 388 words without tables |
| R1 agrees with literature | 2 | 2 | 2 | |
| **Total** | **34** | **35** | **38** | s2 (round 1 only): 32 |

The main answer was stable between two independent runs of s1: "ESR1 alone does not replace IHC; use RNA with IHC". Round 1: overall agreement 94.8%. Round 2: specificity 93.7%, sensitivity 86.9%.

## What improved
- run.yaml parse rule removed the most serious defect (0 → 2 in both runs).
- `duplicate-variables` caught the two ER fields.
- `*.private.csv` kept patient tables out of git.
- New survival and classifier checks were used in s3 without help: optimism-corrected C-index, split stability, error balance, EPV.

## New failures and fixes for v0.3.0
| # | Failure | Seen in | Fix |
|---|---|---|---|
| 1 | The agent invented the success threshold (95%/90%) because the client had none. The threshold decided the "No". The brief did not show this clearly. | s1 | RUN.yaml `success` field with `set by person` or `assumed`. Brief: an assumed threshold appears in the Answer line, and the brief shows how the answer changes at nearby thresholds. |
| 2 | State in CLAUDE.md was stale between setup and checkpoint. | s1 | to-analysis-plan and release update State. |
| 3 | No record of the sources found during grilling; DECISION entry too long for 1-4 lines. | s1, s3 | Fixed field order for the grilling DECISION entry, with a `sources:` line. Question rounds stay in the chat. |
| 4 | Sample removals as many LOG entries. | s3 | Removals with counts go in `run.yaml samples`; LOG holds only the exclusion rule. |
| 5 | No follow-up maturity check; no treatment confounding. | s3 | New checks `follow-up` and `treatment`. |
| 6 | Sex-gene rule gave false mismatches (male tumors express XIST). | s3 | Call sex from Y genes only; threshold from the gap between the two groups. |
| 7 | Positive control was circular (ESR1 is the predictor); no endpoint validation for survival. | s1, s3 | Control must not be the predictor; for survival, validate the endpoint with a known factor (stage). |
| 8 | Outlier check has no metric; classifier group size has no rule; own cut-off moved to another assay not covered; prior not comparable. | s1 | Metric and threshold; CI width rule; `platform-transfer` for any cut-off; `prior: not comparable - <reason>`. |
| 9 | Plan template lists only one check. | s1 | to-analysis-plan builds the list from CHECKS.md by data type. |
| 10 | Brief: what counts as words; figure embedding; too many tables in the release. | s1, s3 | All text except tables counts; embed `![](fig.png)`; brief names at most 4 tables. |
| 11 | SOURCE.txt hash vs tag on different commits; no checksums. | s1, s3 | State the two commits; add md5 of each input file. |
| 12 | Data table in CLAUDE.md lacks size and source status. | s1, s3 | Columns: Source, Source status, Received, Size, Shape. |
| 13 | Literature sites blocked (captcha). | s1, s3 | grilling: record blocked sources; use the abstract; mark the prior as weak. |
| 14 | checkpoint step "find files that break rules" has no method. | s1, s3 | Give the commands. |
