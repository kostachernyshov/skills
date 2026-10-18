# Round 4 (skills v0.4.0 + deck-review), 2026-10-18

Three new scenarios, three fresh agents. Each produced a brief and a deck. Projects: `/mnt/project-files/skill-tests/round4/`.

## Results and self-check against literature

| Scenario | Answer | Key numbers | Literature | Grader view |
|---|---|---|---|---|
| s4 GBM MGMT | Array call separates survival on temozolomide; error against the clinical test is unknown in TCGA. Pre-screen + central confirmation. | Non-G-CIMP, TMZ-treated, n=155: age-adjusted HR 0.49 (0.32-0.74); 47% methylated | Bady 2012 TCGA-27k HR 0.737; 50% methylated; Hegi 2005 direction | Plausible. Coefficients in `data/ref/` match MGMT-STP27 (intercept 4.3215, 0.5271, 0.9265, cut-off 0.358). Agent found the immortal-time risk itself and dropped the "TMZ-specific" claim. |
| s5 SKCM immune | Yes in research data; recommend a qualified claim and assay validation. | Adjusted HR 0.63 per SD (0.54-0.72), n=420, 201 deaths; holds within each tissue site | TCGA 2015 Cell, Rooney 2015 | Plausible. Agent used survival from sampling (time origin trap) and tested lymph-node contamination. |
| s6 CRC MSI | Not yet at the assumed threshold; keep the test, run RNA in parallel. | CV AUC 0.97, sensitivity 0.94 (0.85-0.98); all misses are MLH1-normal tumors | MSIsensor-RNA AUC 0.95-0.997 | Plausible. Nested CV (cut-off chosen inside training folds). Error location in Lynch-relevant group is the key finding. |

All three agents found the main trap of their scenario. Two of three found it by their own initiative, not by a check. These became new checks.

## Deck review: what the grader saw in the slide images
- Slides were clean, nothing cut, titles were messages. The two review rounds fixed real problems: a "Yes" that contradicted the recommended weaker claim (s5), undefined "hazard ratio" for a marketing reader (s5), a label over a curve (s5), a new overlap after round 2 (s6).
- Systematic weakness the review did not catch: slides were half empty with small text, and the answer slide was plain bullets with no visual weight. Cause: the layout script (fixed narrow bullet column, 14-18 pt), not the agent. The review cannot fix what the script cannot do.
- Numbers from different groups sat side by side (s4: adjusted 0.49 next to an all-patient 0.69; s5: "451 patients" in the figure, 420 in the model).
- The cold read was always done by the author: test agents cannot start subagents. Weak.

## Failures and fixes in 0.5.0
| # | Failure | Seen in | Fix |
|---|---|---|---|
| 1 | Layout script: half-empty slides, small fonts, no big numbers, no full-width figure | s4, s5, s6 | Script v2: `kpis`, full-width figure/table, highlighted option row, larger fonts |
| 2 | Review misses empty space, small text, mixed populations | grader | New criteria: readability, space, consistency |
| 3 | Cold read by the author; final deck never re-checked | s4, s5, s6 | Titles test as fallback, marked `self`; final verify render; 100 dpi |
| 4 | Survival time origin not in grilling; endpoint check assumes diagnosis | s5 | Topic "time origin"; endpoint validation at the time origin; check `time-origin` |
| 5 | Treatment-received group (immortal time) | s4 | Check `treatment-received` |
| 6 | Lymph node immune cells confound immune scores | s5 | Check `tissue-composition` |
| 7 | No methylation checks | s4 | Methylation section in CHECKS.md |
| 8 | Threshold not answerable with the data (53 positives) | s6 | to-analysis-plan computes the achievable interval first |
| 9 | Where the errors fall was found by chance | s6 | Check `error-location` |
| 10 | Planned model weaker than prior; R01 left as candidate | s6 | Post-hoc case named; status `superseded` |
| 11 | Brief has no next steps; owners invented; 4-table limit | s4, s6 | Next steps section; owner "to be named by"; limit removed; cross-run sources |
| 12 | Success rule ignores the assay where the decision applies | s5 | `success` names the assay; topic "measurement transfer" |
