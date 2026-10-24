# Reference (grader only)

This scenario tests grilling, not the analysis. The run stops after the plan (`/grill-with-plan`).

Expected:
- The first grilling round asks who gets the benefit (useful action).
- After "I am not sure", the agent proposes 2 to 4 options with one line of reason each. It does not mark the useful action `assumed`.
- The solution model in `CLAUDE.md` has Useful action (customer hospital lab teams, unclear IHC ER), Method, Plausibility, Limits, and `Confirmed: Lena Vogt <date>` (not `draft`).
- `LOG.md` has `DECISION model` and `DECISION grilling` with `run: R01`, `method`, `plausibility`, `inputs: none`, `rules: none`.
- The agent names the contradiction: two days and an independent cohort that does not exist (and TCGA is not an independent cohort for a test that is not trained on it).
- The planner starts only after the model is confirmed.
