# Round 8 (skills v0.8.0), 2026-10-21

Goal: check the solution model in grilling (#2) and the project rules (#3). Two new scenarios, 3 replicates each, same harness and models as round 7 (agent `claude-sonnet-5-5`, persona `claude-haiku-5-5`). Projects: `/mnt/project-files/skill-tests/round8/`.

- `s10-vague-model`: a vague request ("find something useful about ESR1"). The person does not know who gets the benefit. The run stops after `/planner`.
- `s11-two-runs-rule`: two runs in one project. R01: MKI67, stage I. The opening says "Remember this: patients who got radiation therapy are out". R02: TOP2A, stage I and II, and the person asks to keep the radiation patients. Designer and publisher are not run.

The scenarios set their own command order in `flow.json`. `harness/check_rules.py` prints the model, the rules, the rule writes per turn, and the judge answers to Q6. The blind grader with `RUBRIC.md` was not run: the rubric does not score these behaviors. The checks below come from the project files and the logs.

## s10: solution model from a vague request

| Check | s10-1 | s10-2 | s10-3 |
|---|---|---|---|
| Round 1 asks for the useful action first | yes | yes | yes |
| 2 to 4 options for "who gets the benefit", one reason line each | yes (4) | yes (4) | yes (4) |
| Useful action not `assumed`; the person chose it | yes | yes | yes |
| Model has useful action, method, plausibility, limits | yes | yes | yes |
| `Confirmed` names the person | no (account e-mail) | no (account login) | no (account login) |
| `DECISION model` and `DECISION grilling` with `run`, `method`, `plausibility`, `inputs`, `rules` | yes | yes | yes |
| Contradiction "two days" + "independent cohort that does not exist" named | yes | no (only as a limit) | yes |
| Planner starts only after the model is confirmed | yes | yes | yes |

## s11: project rules over two runs

| Check | s11-1 | s11-2 | s11-3 |
|---|---|---|---|
| "Remember this" becomes a rule proposal in one line with "yes / no" | yes | yes | yes |
| Rules written only after "yes" (all rule writes) | 2 of 2 | 3 of 3 | 2 of 2 |
| Rules proposed from other triggers in R01 | 1 (two radiation fields disagree) | 2 (fields; veto cause) | 1 (failed positive control) |
| R01 cohort excludes radiation patients | yes | yes | yes |
| R02 grilling shows the model and asks if it is still valid | yes | through a contradiction question | yes |
| R02 grilling quotes RULE-01 and asks "follow / deviate" | yes | yes | yes |
| R02 `DECISION grilling`: `run: R02`, `inputs: R01`, `rules` | yes | yes | yes |
| R02 `run.yaml` `rules`: one line per rule | yes | yes | yes |
| Judge Q6 answered with evidence | yes | yes | yes |
| Deviation path (the persona changed the answer at the plan) | n/a | `DECISION deviation` with the words, `rules: deviation - LOG.md`, Q6 yes | same |
| No rule line changed or deleted | yes | yes | yes |

## Failures

| # | Failure | Runs | Cause | Proposed fix |
|---|---|---|---|---|
| F1 | `Confirmed`, `accepted`, and `owner` hold the e-mail or login of the Claude account, not the person in the chat. In s11-1 the e-mail is in the client brief (`out/brief.md`, "Decide on the pilot"). | 6 of 6 | The skills say `<person>` but do not say where the name comes from. The agent takes the account identity. | Grilling asks for the name and role of the person in round 1. Never write an e-mail address into project files. The brief names a role, not a person. |
| F2 | A rule added after a run is applied to that run. R01 `run.yaml` gets lines for rules added after R01. In s11-3 the judge vetoed R01 twice on Q6, and the agent wrote a `DECISION deviation RULE-02` for R01. | 3 of 3 (veto in 1) | `planner` and judge Q6 check all rules in `CLAUDE.md`, not the rules that existed when the plan was accepted. | `rules` in `run.yaml` lists the rules that exist at plan acceptance. Q6 checks only those. A new rule starts at the next run. |
| F3 | The rule question is mixed with other questions. In s11-3 the answer "yes. Option 1: yes, write the brief" was taken as "yes" to RULE-02. | 1 of 3 | `curator` step 2 does not say that the rule question stands alone. | Ask the rule question as a separate numbered item. Accept only an answer that names the rule or its number. |
| F4 | One option for the useful action is marked "recommended". | 1 of 3 (s10-2) | `grilling` says "never `assumed`" but does not forbid a recommendation. | Options for the useful action have no recommended mark. |
| F5 | The "two days + independent cohort" contradiction is not named as a contradiction. | 1 of 3 | Model failure; the skill lists the planes to check. | None now. Watch in the next round. |

## Harness notes
- The persona sees only the last message. In s11-2 and s11-3 it first said "Follow the rule", then at the plan it asked to keep the radiation patients (its role says so). The agent handled this correctly with a deviation entry. This tested the deviation path by chance.
- A usage limit hit the persona once (s11-2, turn 13). The persona text "You've hit your session limit" went to the agent as an answer. `run_scenario.py` checks the limit only for the agent. To fix in the harness.
- 5 of 6 runs stopped on a usage limit and continued with `--resume`.

## Time and tokens per run (mean)

| | s10 (stops after planner) | s11 (two runs, no designer or publisher) |
|---|---|---|
| Active minutes | 17 | 33 |
| API calls | 45 | 154 |
| Tokens (all) | 3.4 M | 17.4 M |
| Subagents (judge, editor, reviewer) | 0 | 13 |

Total: 62 M tokens, 96% cache read.
