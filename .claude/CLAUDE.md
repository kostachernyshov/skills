# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This file is `.claude/CLAUDE.md`, not `CLAUDE.md` at the root. The repository root is also the plugin root. `claude plugin validate --strict` fails if `CLAUDE.md` is at the plugin root. `AGENTS.md` at the root is a link to this file, so Codex reads the same rules.

## What this repository is

A Claude Code and Codex plugin (`kostachernyshov-skills`). Its skills take a bioinformatics project from the question of a client to a signed release. The skills work on processed tables only. Methods for raw data are out of scope (see `SCOPE.md` and `UPSTREAM.md`).

Most of the repository is Markdown. The only code is in these folders:

- `tests/harness/`: Python scripts that run test rounds in real Claude Code sessions.
- `skills/project/curator/scripts/curate.py`: builds the State section of the `CLAUDE.md` of a user project. The `Stop` hook in `hooks/hooks.json` runs it.
- `skills/in-progress/animate/scripts/`: the pixel-art video renderer.

## Commands

- Validate the plugin: `claude plugin validate . --strict`. Run it before each commit that changes skills or manifests.
- Unit tests of the harness: `python3 tests/harness/test_harness.py`. Run one test: `python3 -m unittest tests/harness/test_harness.py -k <name>` from the repository root.
- One scenario in real Claude Code: `python3 tests/harness/run_scenario.py --scenario <dir> --data <dir> --project <dir> --log <file> --plugin <repo>`. Use `--stop-after N` to stop after step N. Use `--resume` after a usage limit.
- Misuse test: `python3 tests/harness/run_misuse.py --spec tests/misuse/<id>.json` with the same `--data`, `--project`, `--log`, and `--plugin` arguments.
- Grade, skill usage, and cost: `tests/harness/grade.py`, `skill_usage.py`, `cost.py`. Read `tests/README.md` for the protocol.
- The curator by hand, in a user project: `python3 skills/project/curator/scripts/curate.py <project dir>`. It needs PyYAML.
- The animation: `uv run --with pillow --with numpy --with pyyaml python3 skills/in-progress/animate/scripts/animate.py <command>`.

A full test round costs about 60 M tokens. Use the smallest test that can show the failure. Write the budget in the results file before the start.

## Structure

- `skills/<bucket>/<skill>/`: buckets are `core`, `analysis`, `decision`, `project`. New skills start in `skills/in-progress/`. `skills/ask-kosta/` is at the top level. Each skill folder has `SKILL.md` and `agents/openai.yaml` (the Codex metadata).
- There are two types of skill:
  - A person skill has `disable-model-invocation: true` in `SKILL.md` and `allow_implicit_invocation: false` in `agents/openai.yaml`. The person types `/name`. The person skills are `ask-kosta`, `setup-project`, `grill-me`, `grill-with-plan`, `analyze`, `designer`, `publisher`, `animate`.
  - An agent skill starts by itself when the situation fits.
- The flow is `ask-kosta` → `setup-project` → `grill-with-plan` → `analyze` → `designer` → `publisher`. Read `docs/skills.md` for the full table and the layout of a user project (`CLAUDE.md`, `LOG.md`, `data/`, `runs/`, `releases/`).
- `GLOSSARY.md` defines the terms (run, control, check, verdict, veto, override, project rule). Use these words in the same meaning.
- `.claude-plugin/plugin.json` lists each skill path and holds `version`. `.claude-plugin/marketplace.json` makes the repository a marketplace.
- `tests/scenarios/<id>/` has `persona.md` and an optional `flow.json`. `tests/RUBRIC.md` is for the grader only. Do not give it to the agent under test. Round results go to `tests/results/`.
- `.out-of-scope/<idea>.md` keeps rejected ideas with the reason.
- `promo/` has the sources of the README animation.

## Rules for a change

- Write `SKILL.md` files in ASD-STE100 Simplified Technical English: short sentences, active voice, one instruction per sentence. Use the same style in other documentation.
- Each skill has a "Done when" section with checks that can be verified.
- A person skill can call an agent skill. A person skill never calls another person skill.
- Write a dependency as: Call the Skill tool with "<name>". Do not link to files of another skill.
- When you add, remove, or rename a person skill, update `skills/ask-kosta/SKILL.md` in the same commit.
- Add a skill only for a failure that was seen in a real test (see `SCOPE.md` and `tests/`). Put the fix into an existing skill if possible.
- When you add, remove, or rename a skill, update the `skills` list in `.claude-plugin/plugin.json`, `docs/skills.md`, and add `agents/openai.yaml` to the skill folder.
- Record each change in `CHANGELOG.md`. Each version starts with "What changes for you", then "Changes".
- For each release, increase `version` in `.claude-plugin/plugin.json` to match `CHANGELOG.md`. Users get an update only when the version changes.
- Use only public data (TCGA, GEO, GTEx and similar) in tests and examples. Do not ask for private or NDA data.
