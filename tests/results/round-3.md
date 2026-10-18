# Round 3 (skills v0.3.0), 2026-10-18

One fresh agent on s2 (GSE7390), the lowest score in round 1 (32/38). Project: `/mnt/project-files/skill-tests/round3/`.

## Score: 37/38 (round 1: 32/38)

| Item | Round 1 | Round 3 | Evidence |
|---|---|---|---|
| P3 run.yaml valid | 0 | 2 | parses |
| P6 release | 1 | 2 | per-patient score is `score.private.csv`, not in git (0 private files tracked) |
| B1 brief length | 1 | 2 | 396 words without tables |
| B4 warnings | 1 | 2 | decision-relevant warnings named; CI of the gain crosses the threshold, stated |
| B5 numbers traceable | 1 | 2 | derived numbers added to tables |
| B2 answer early | 2 | 1 | answer on line 5 (template order); rule changed in 0.3.1 |

New behavior from v0.3.0 that worked:
- Grilling asked for the success threshold; the client had none; the agent assumed one and the brief names it in the Answer line, with `threshold-sensitivity.csv`.
- The agent found the public weights again (genefu `sig.gene76`) and placed them in `data/ref/` with source status.

Independent check by the grader: the weights from round 1 (Wang 2005 PDF, Table 3) and round 3 (genefu) agree for 76 of 76 probes (correlation 1.0). Nothing was invented.

Stable conclusion across rounds 1 and 3: the score adds to clinical factors (adjusted HR per SD 1.59 and 1.72).

## Remaining friction and fixes in 0.3.1
| # | Failure | Fix |
|---|---|---|
| 1 | Bug fix vs post-hoc change unclear | defined in sanity-check |
| 2 | Prior on a different scale | compute own result on the prior's scale first |
| 3 | CI crosses the threshold, no check | new check `threshold-uncertainty` |
| 4 | Small panel: PCA on top 2000 genes, no ER genes | rules for small panels |
| 5 | Answer that misses the question | grilling rule |
| 6 | Source status for derived files | `derived from <source>` |
| 7 | Answer-line position, caption words | brief rules |
| 8 | Empty checkpoint commit | commit only if changed |

## Not fixed (needs Kosta)
- Binary reference formats (.rda) need R or a parser; the cloud has no R. Decide: add R to the environment, or accept `warn`.
- 32 checks for a small panel is heavy. Option: "core" and "extended" check sets.
