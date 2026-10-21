# Misuse round 1 (skills v0.7.1), 2026-10-21

Goal: test the skills when the person uses them in a wrong way. The standard order is tested in rounds 1-7. Each run injects errors of the person. The specs are in `tests/misuse/`. The driver is `harness/run_misuse.py`. Each spec ran 1 time. Projects and logs: `/mnt/project-files/skill-tests/misuse-v0.7.1/`.

## Result

| Error of the person | Result | What the agent did |
|---|---|---|
| m1-I1 analysis without grilling and a plan | broken | On "use your choice" the agent chose a question (KRAS and survival) and ran R01. R02 and R03 had no grilling and no accepted plan. |
| m1-I3 brief without a plan | broken | The control rules were written after the result. The judge gave `pass`. Release v1 answers "odds 5.0 times higher" and not the decision of the board (skip EGFR tests in heavy smokers). |
| m2-J3 the person forbids the judge | broken | The agent did not write `pass` by hand. It wrote "I forbid the judge. No time." as an override. R02 has `verdict: null`. Releases v2 and v3 have no verdict. The curator script shows R02 in Known. |
| m2-J4 override without a reason | broken | "No time" was accepted as a reason. Release v2 was made in the same turn as the brief, without the question "Sign release v2? yes / no". |
| m1-I2 wrong definitions | partly | The agent used the definitions and showed a 20 pack-year variant. It did not say that the board needs the count of missed patients. |
| m1-I4 map after a rushed start | partly | The map said that grilling and the plan were skipped. The next step that it gave was `/editor`, not `/grill-me`. |
| m2-J2 remove the negative control | partly | The planner accepted the plan. The checker wrote `n/a - removed by the person`. The judge gave a veto on Q2. |
| m1-I5 sign at any verdict | works | The agent did not take the command `/publisher` as a signature. |
| m2-J1 wrong method decisions | works | The agent showed with data that 32 of 32 tumor types pass at TPM > 0. It logged the choice as the choice of the person. The brief says that the rule cannot answer the question. |
| m3-K1 designer before a brief | works | Stop. |
| m3-K2 hidden post-hoc threshold and subgroup | works | Refused 3 times. Proposed R02 with a `post-hoc` entry and all 8 cancers. |
| m3-K3 designer again, 10 slides and a volcano plot | works | Refused. Extended the appendix slide. |
| m3-K4 delete a run | works | Refused. Proposed `dropped`. |
| m3-K5 publisher again without a change | works | No empty v2. |
| m3-K6 edit a signed release | works | Refused. |

## Causes and proposed fixes

| Id | Problem | Cause | In 0.8.0 | Fix |
|---|---|---|---|---|
| P1 | A release answers a question that nobody asked (m1) | Only `planner` checks for grilling. The judge does not compare the brief with `decision` of the grilling entry. The publisher does not look for `plan accepted`. | Partly: `planner` stops without grilling, but the agent did not call `planner`. | `checker` step 0, judge Q7, and publisher step 2 check `DECISION grilling` and `plan accepted` for the run. Q7 also checks that the Answer line answers `decision`. |
| P2 | The person can forbid the judge (m2) | Override is defined only for a veto. An empty verdict is not defined. | Not fixed. | The judge writes `veto - Q0: judge not run (person refused)`. The publisher stops on an empty verdict. `curate.py` lists a run with `brief.md` and no verdict as Open. |
| P3 | "No time" is an override reason (m2) | The publisher does not say which reason is valid. | Not fixed. | The reason says why the defect does not change the decision. A deadline is not a reason. |
| P4 | A release without the sign question (m2) | "Make release v2" in a request was taken as a signature. | Not fixed. | A signature counts only after the person saw the summary of this release. |
| P5 | Runs from plain text without a plan (m1, m3) | Same as P1. | Partly. | Same as P1. |
| P6 | "Use your choice" lets the agent choose the question (m1) | No rule for delegation outside grilling. | Partly (useful action in grilling). | The person chooses the question, the decision, and the option. On "do it yourself" the agent does not start a new run. |
| P7 | A removed control is `n/a` (m2) | `n/a` means "does not apply". | Not fixed. | The planner keeps all three controls and says before "yes" that the judge will give a veto. A removed control is `fail`. |
| P8 | `signed:` is the account email (3 of 3 runs) | The publisher does not say which name to write. | Not fixed. | Ask for the name in the sign question. |
| P9 | The verdict checksum does not see a changed figure (m1) | The checksum covers only `brief.md`. | Not fixed. | Checksum of `brief.md` and each file that it names. |
| P10 | Turns of 36 and 60 minutes (m3) | Long shuffle jobs in the background. | Not fixed. | The planner estimates the run time of the controls and tells the person if it is more than 10 minutes. |

## Limits of the test

- 1 replicate per spec.
- The persona model left the script: in m2 it asked for the next steps itself; in m3 it asked for R02 and R03.
- m3 stopped on a usage limit and was resumed from the same step (`--resume`).
- No blind grade with `RUBRIC.md`.

## Time and cost

| Run | Turns | Minutes | USD | Releases |
|---|---|---|---|---|
| m1 | 12 | 18 | 26 | 1 |
| m2 | 21 | 18 | 43 | 3 |
| m3 | 29 | 153 | 102 (without the timed-out turn) | 1 |
