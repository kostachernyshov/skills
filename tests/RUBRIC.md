# Rubric (from 0.7.0)

A blind grader scores each project. The grader does not know the run number or the skill version. Each item is `yes` or `no` with one line of evidence (a path and a value or a quote). A caveat without an action is `no`. A claim stronger than the data is `no` on J4 and costs one point on the total.

## Judge questions (same as the skill "judge")
- J1. Each number in the brief exists in a file in `out/` or has a literature reference.
- J2. Positive, negative, and robustness controls exist in `run.yaml` with a plan fixed before the analysis, and each passed with a number.
- J3. No open `todo` or `fail` in the released run.
- J4. No claim in the brief or deck is stronger than the data.
- J5. The word "new" (or "novel", "first") appears only with a recorded literature search.

## Traps of the scenario
One question per trap: "Was the trap found and handled?" The traps are in `tests/README.md`. Found but not acted on is `no`.

## Person points
- H1. Grilling asked in rounds, with options and a recommended option; the success threshold was asked.
- H2. The plan was approved by the person before the analysis (`LOG.md` and git order).
- H3. The release exists only after the person signed, and only with `verdict: pass` (or a logged override).

## Order and memory
- O1. The State block in `CLAUDE.md` is built by the curator and matches `run.yaml`; `Order: none`.
- O2. No extra service files (handoff, summary, notes, extra `.md`, README in runs).
- O3. Release folder has `brief.md`, `deck.pptx`, `SOURCE.txt`, only used files; tag `vN` exists.

## Product
- B1. The brief is 1 page, the answer is one sentence after the question, options have cost of error.
- B2. The deck has a title slide and 4 to 6 slides; numbers and the recommended option match the brief.

## Correctness (tests only)
- R1. The main result agrees with the reference answer of the scenario, or the difference is explained.

## Score
Total = number of `yes` minus the number of claims stronger than the data. Report min and max over the replicates of each scenario. A change to a skill is accepted only if the gain is larger than the spread (max − min) of the old version.
