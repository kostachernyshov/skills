# Changelog

## 0.2.0 (2026-10-18)
Fixes from test round 1 (see tests/results/round-1.md).
- Flow order: setup-project before grill-me.
- run.yaml: full template, edit in place, parse after each edit.
- setup-project: move input files, AGENTS.md fallback, .gitkeep, unknown source, data/ref/.
- project-order: patient-level tables are *.private.* and not in git.
- grilling: search published work and check if the asset is public before asking.
- sanity-check: n/a status, post-hoc path, new checks (duplicate-variables, classifier, model-fit, published signature, optimism), EPV thresholds.
- decision-brief: word limit without options table, decision-relevant warnings only, rules for derived and literature numbers, file names only.
- release: warn with evidence is OK, commit hash before release, flat folder.
- ask-kosta: upstream list inside the skill. README: flat install.

## 0.1.0 (2026-10-18)
- First version: 10 skills in 4 buckets and the router `ask-kosta`.
