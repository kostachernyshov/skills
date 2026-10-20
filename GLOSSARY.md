# Glossary

| Word | Meaning |
|---|---|
| run | One iteration of the analysis. A folder `runs/RNN-<slug>/` with `run.yaml`. |
| run.yaml | The record of one run: question, plan, controls, checks, todo, result, verdict. The single source for the State. |
| status | State of a run: open, candidate, superseded, dropped, shipped. |
| control | A test fixed in the plan before the data: positive (a known effect must appear), negative (shuffled labels, the effect must disappear), robustness (nearby thresholds and subgroups, the answer must not flip). |
| check | One test of plausibility with a status: pass, warn, fail, n/a, todo. |
| todo | An open doubt in `run.yaml`. A run with a todo cannot go to a brief. |
| prior | A published result that the analysis compares with. |
| literature | The record of a literature search (date, queries, findings). Needed before the word "new". |
| verdict | The answer of the judge in `run.yaml`: pass, or veto with the question number and reason. |
| veto | One "no" from the judge. It stops the release. Only the person can override it, with a reason in `LOG.md`. |
| override | A `DECISION override` entry in `LOG.md`. The brief must name it. |
| fresh context | A subagent that sees only the files, not the chat of the analysis. The editor and the judge work in it. |
| release | A frozen set of results that the client saw. `releases/vN-<date>/`. Never changed. The person signs it. |
| brief | The one-page decision brief. |
| frontier | The open questions in a grilling interview. |
| State | The block in `CLAUDE.md` that says where the work is now. The curator script builds it from `run.yaml`. |
| responsibility points | The three steps where the person acts: grilling answers, plan approval, release signature. |
