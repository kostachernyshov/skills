# Glossary

| Word | Meaning |
|---|---|
| run | One iteration of the analysis. A folder `runs/RNN-<slug>/` with `run.yaml`. |
| run.yaml | The record of one run: question, plan, controls, checks, todo, result, verdict. The single source for the State. |
| status | State of a run: open, candidate, superseded, dropped, shipped. |
| control | A test fixed in the plan before the data: positive (a known effect must appear), negative (shuffled labels: the median effect is at the null value), robustness (nearby thresholds and subgroups, the answer must not flip). |
| check | One test of plausibility with a status: pass, warn, fail, n/a, todo. |
| todo | An open doubt in `run.yaml`. A run with a todo cannot go to a report. |
| prior | A published result that the analysis compares with. |
| literature | The record of a literature search (date, queries, findings). Needed before the word "new". |
| supervisor | A fresh subagent that checks the report against the files with 7 yes/no questions. The role comes from Yoon et al. 2026. A judge that compares several reports is a later role. |
| verdict | The answer of the supervisor in `run.yaml`: pass, or veto with each question that has "no" and its reason. |
| checked | The files that the supervisor saw, with a checksum each, in `run.yaml`. A later change shows in the State; the publisher shows it to the person before the signature. |
| veto | One "no" from the supervisor. It stops the release. Only the person can override it, with a reason in `LOG.md`. |
| override | A `DECISION override` entry in `LOG.md`. The report must name it. |
| fresh context | A subagent that sees only the files, not the chat of the analysis. The editor and the supervisor work in it. |
| release | A frozen set of results that the client saw. `releases/vN-<date>/`. Never changed. The person signs it. |
| report | The one-page decision report. |
| frontier | The open questions in a grilling interview. |
| solution model | A short explanation of the project in `CLAUDE.md`: useful action (who gets the benefit), method (how), plausibility (why it can work). It has no details of one run. Grilling writes it; the planner can change it after a "yes" of the person. The person confirms it before each run. |
| task of the run | The `DECISION grilling` entry for one run: question, method, plausibility, inputs, threshold. |
| project rule | A lesson of one run for all later runs: `RULE-NN` in `## Project rules` in `CLAUDE.md`. The agent adds it after the person says yes. Only the person edits or deletes it. |
| deviation | A `DECISION deviation RULE-NN` entry in `LOG.md`: the person chose not to follow a rule in one run. The report names it. |
| State | The block in `CLAUDE.md` that says where the work is now. The curator script builds it from `run.yaml`. |
| Person | The line `Person: <name>, <role>` in `CLAUDE.md`. The only source of the name in `Confirmed`, `plan accepted by`, and `signed`. Never an e-mail address. |
| responsibility points | The three steps where the person acts: grilling answers, plan approval, release signature. |
