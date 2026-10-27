# AGENTS.md

Rules for agents (Claude Code, Codex) that work in this repository. Claude Code and Codex read this file from the root. Do not add `CLAUDE.md` at the root: the root is also the plugin root, and `claude plugin validate . --strict` fails on it.

## What this repository is

A plugin for Claude Code and Codex: `kostachernyshov-skills`. Its skills take a bioinformatics project from the question of a client to a decision and a signed release. The users are heads of bioinformatics, bioinformaticians, and the wet-lab and clinical researchers who work with them.

## Layout

```
AGENTS.md              rules for agents (this file)
README.md              for people: what it is, install, examples, why, all skills
CHANGELOG.md           one entry for each version
LICENSE
.claude-plugin/
  plugin.json          version and the list of skill paths
  marketplace.json     makes this repository a marketplace
hooks/hooks.json       Stop hook: runs the curator script
skills/
  ask-kosta/           the map of the flow (person skill)
  core/                grilling
  analysis/            planner, analyze, checker
  decision/            editor, supervisor, reviewer, designer
  project/             setup-project, curator, publisher
  in-progress/         new skills before a test round
  deprecated/          old skills, not in the plugin
  <bucket>/<skill>/
    SKILL.md
    agents/openai.yaml Codex metadata
tests/
  README.md            the test protocol
  RUBRIC.md            for the grader only
  harness/             Python scripts for test rounds
  scenarios/<id>/      persona.md, optional flow.json
  misuse/              misuse specs
  results/             one file for each round
docs/
  skills.md            all skills and the layout of a user project
  media/               README images and video
  media/how-it-works/  sources of the README animation
```

The only code is in `tests/harness/`, `skills/project/curator/scripts/curate.py` (builds the State section of the `CLAUDE.md` of a user project), and `skills/in-progress/animate/scripts/`.

## Commands

- Validate the plugin: `claude plugin validate . --strict`. Run it before each commit that changes skills or manifests.
- Unit tests of the harness: `python3 tests/harness/test_harness.py`. One test: `python3 -m unittest tests/harness/test_harness.py -k <name>`.
- One scenario in real Claude Code: `python3 tests/harness/run_scenario.py --scenario <dir> --data <dir> --project <dir> --log <file> --plugin <repo>`. Use `--stop-after N` to stop after step N. Use `--resume` after a usage limit.
- Misuse test: `python3 tests/harness/run_misuse.py --spec tests/misuse/<id>.json` with the same `--data`, `--project`, `--log`, and `--plugin` arguments.
- Grade, skill usage, and cost: `tests/harness/grade.py`, `skill_usage.py`, `cost.py`. Read `tests/README.md` for the protocol.
- The curator in a user project: `python3 skills/project/curator/scripts/curate.py <project dir>`. It needs PyYAML.
- The animation: `uv run --with pillow --with numpy --with pyyaml python3 skills/in-progress/animate/scripts/animate.py <command>`.

A full test round costs about 60 M tokens. Use the smallest test that can show the failure. Write the budget in the results file before the start.

## Communication

- In chat, use ASD-STE100 Simplified Technical English at 80% strictness. Write in the language of the person.
- In documentation, `SKILL.md` files, and other files, use ASD-STE100 at 100% strictness: short sentences, active voice, one instruction per sentence. Write files in English.
- For a large or complex concept, prefer an ASCII diagram. For a simple thing, use plain text.

## Scope

In scope:
- The path from a question to a decision on processed tabular data.
- Project order, versions, and releases for analysis projects.
- Checks of plausibility before a result.
- Communication of a result to the person who decides.

Out of scope:
- Methods for raw data and pipelines. The README names other projects for them.
- Wrappers for one tool or one database.

Use only public data (TCGA, GEO, GTEx, and similar) in tests and examples. Do not ask for private data or data under NDA.

## Skills

There are two types of skill:

- A person skill starts only when the person types `/name`. It has `disable-model-invocation: true` in `SKILL.md` and `allow_implicit_invocation: false` in `agents/openai.yaml`. The person skills are `ask-kosta`, `setup-project`, `grill-me`, `grill-with-plan`, `analyze`, `designer`, `publisher`, `animate`.
- An agent skill starts by itself when the situation fits.

The flow is `ask-kosta` → `setup-project` → `grill-with-plan` → `analyze` → `designer` → `publisher`. `docs/skills.md` has the full table.

Rules for each skill:

- Write `SKILL.md` in ASD-STE100 at 100% strictness.
- Each skill has a "Done when" section with checks that can be verified.
- A person skill can call an agent skill. A person skill never calls another person skill.
- Write a dependency as: Call the Skill tool with "<name>". Do not link to files of another skill.
- Use the words of the glossary below in the same meaning.

## Add or change a skill

1. Find a failure in a real project or in a test in `tests/`. Do not add a skill without a seen failure.
2. Write the failure as an issue (see "Issues").
3. Put the fix into an existing skill if possible.
4. A new skill starts in `skills/in-progress/`. The maintainer moves it into a bucket after it passes a test round.
5. When you add, remove, or rename a skill:
   - Update the `skills` list in `.claude-plugin/plugin.json`.
   - Update `docs/skills.md`.
   - Add `agents/openai.yaml` to the skill folder.
   - For a person skill, update `skills/ask-kosta/SKILL.md` in the same commit.
6. Run `claude plugin validate . --strict`.

Pull requests that add checks to `skills/analysis/checker/CHECKS.md` or scenarios to `tests/` are welcome.

## Issues

- One issue is one failure or one idea.
- Title: `<skill>: <failure>`.
- Body: where you saw it (test round, scenario, public dataset), what you expected, what you got, the evidence (a quote or a file), and a proposed fix.
- Labels: `failure`, `idea`, `out-of-scope`.
- Close a rejected idea as "not planned", with the label `out-of-scope` and the reason.
- An agent creates issues by itself only after a test round. At other times, it creates an issue only when the person asks.

## Release

- Record each change in `CHANGELOG.md`. Each version starts with "What changes for you", then "Changes".
- For each release, increase `version` in `.claude-plugin/plugin.json` to match `CHANGELOG.md`. Users get an update only when the version changes.
- Before a release of a version, run a full test round with 2 replicates for each scenario.

## Glossary

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
