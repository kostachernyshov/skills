# Round 7 (skills v0.7.1), 2026-10-20

Goal: check the 0.7.1 fixes on the two scenarios where round 6 was weakest: s9 (TMB and survival) and s8 (CLDN18.2). Each ran 3 times with the same persona, data, harness, and blind grader as round 6. Projects: `/mnt/project-files/skill-tests/round7/`.

## Scores

Score = yes count minus overclaims. "Without J2" leaves out J2, because the rubric asks for all controls `pass`, and 0.7.1 allows a robustness `warn` that the Answer names.

| Scenario | Round 6 (0.7.0) | Round 7 (0.7.1) | Round 6 without J2 | Round 7 without J2 |
|---|---|---|---|---|
| s8 | 16-20 | 18-21 | 16-20 | 18-20 |
| s9 | 12-20 | 17-19 | 12-20 | 17-19 |

| Run | Score | "No" items | Overclaims |
|---|---|---|---|
| s8-1 | 21 | T3 | 0 |
| s8-2 | 18 | J2, O2, T3, T8 | 0 |
| s8-3 | 19 | J2, T3, T5 | 0 |
| s9-1 | 17 | J2, J4, T7 | 2 |
| s9-2 | 19 | J2, O2, O3 | 0 |
| s9-3 | 18 | J2, T2, T3, T7 | 0 |

The gain in the mean (s8 +1.0, s9 +2.3) is smaller than the round 6 spread (4 and 8). By the rule "gain > spread" the gain is not proven. The low end is better: in round 6 one s9 run gave the client no brief (12); in round 7 each run gave a brief with a judged verdict. The spread is smaller (s9: 8 to 2).

## What the fixes did

| Fix | Result |
|---|---|
| Robustness fail becomes `warn`, the Answer names it (F2) | Works. 6 of 6 briefs exist, and each Answer says where the answer changes. |
| Controls calibration (F1) | Works. Negative controls use the shuffled distribution (s8-3: real 71.7% vs shuffled 3.9-8.2%). Positive controls have a source. |
| Verdict checksum (F6) | Works. Each verdict has `brief <hash>`. Cost: the judge runs 4-7 times per run (was 2-4). |
| Doubts accepted by name (F7) | Works. LOG entries name each doubt. |
| Plan runs after "yes" (F9) | Works. The "Run the plan" turn now takes 1 minute (was 5). |
| Do not run curate.py by hand (F10) | Does not work. The agent ran or read the script 7-12 times per run, as before. It does not see the hook output. |

## Not fixed (seen again)
- T3 (s8, 3 of 3 runs): normal stomach is called "on-target tissue" and left out of safety. No run names the risk of an attack on healthy stomach cells.
- T7 (s9, 2 of 3 runs): the client asks about publishing a "new finding". No brief says that the link is already published.
- T8 (s8): esophageal cancer is not split by histology (the data have no histology column).

## Time and tokens per run (mean)

| | Round 6 (9 runs) | Round 7 (6 runs) |
|---|---|---|
| Active minutes | 23 | 27 |
| API calls | 114 | 144 |
| Tokens (all) | 11.4 M | 16.6 M |
| of which cache read | 10.9 M | 16.0 M |

Per-stage tables: `python3 tests/harness/cost.py <run dirs>`.
