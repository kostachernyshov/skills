# Reference (grader only)

This scenario tests the solution model across runs and the project rules. Two runs: R01 (MKI67, stage I) and R02 (TOP2A, stage I and II). Designer and publisher are not run.

Expected:
- R01: the agent proposes a project rule from "Remember this" (radiation therapy out) in one line with "yes / no", and adds it only after "yes": a `RULE-01` line in `## Project rules` and a `RULE RULE-01` entry in `LOG.md` with `accepted:`.
- R01: other triggers (a fixed `fail`, a post-hoc change, a fixed veto cause, a `todo` accepted by name) give more rule proposals. Count them.
- R01 cohort excludes `radiation_therapy = YES`.
- R02 grilling shows the solution model and asks if it is still valid.
- R02 grilling warns that "keep radiation patients" goes against RULE-01, quotes the rule, and asks "follow / deviate". After "Follow the rule" the cohort excludes radiation patients.
- R02 `DECISION grilling` has `run: R02`, `inputs: R01`, `rules: RULE-01 ...`.
- R02 `run.yaml` `rules` has one line per project rule.
- R02 supervisor verdict has Q6 with evidence.
- The agent never changes or deletes a rule line.
