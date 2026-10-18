# Changelog

## 0.6.0 (2026-10-18)
Fixes from test round 5 (see tests/results/round-5.md).
- decision-brief: 300 words, 1 figure at half width, `scripts/brief_pdf.sh` renders an A4 PDF and counts pages; rule for revising a shipped brief.
- Deck script: table fonts applied and row height from text; big-number size from text length; larger secondary text.
- release: re-release of a shipped run without new numbers; brief.pdf; asks about other candidate runs.
- deck-review: review the rendered brief; replace deck-review.csv per release; source bracket check; space criterion for short bullet slides.
- DECK.md: one figure file for brief and deck, 11 x 5 in, plotting in its own script. Checkpoint and naming fixes.
- Plugin and marketplace manifests.

## 0.5.0 (2026-10-18)
Fixes from test round 4 (see tests/results/round-4.md).
- Deck layout script v2: big-number slides (`kpis`), full-width figures and tables, highlighted recommended option, larger fonts, title height fixed.
- deck-review: renders at 100 dpi, titles test when no subagent, final verify render, new criteria (readability, space, consistency), brief criteria.
- grilling: topics time origin, reference test, measurement transfer; `population`, `reference`, and assay in `success`.
- to-analysis-plan: check that the data can answer the threshold before work starts.
- sanity-check: methylation checks; time-origin, treatment-received, tissue-composition, error-location; endpoint validation at the time origin; weaker-than-prior is post-hoc; post-hoc subgroups flagged in the brief.
- Status `superseded`. Brief: Next steps with owners (no invented owners), cross-run sources.

## 0.4.0 (2026-10-18)
- New skill `decision-deck`: a title slide and 4 to 6 slides from the brief, built with `scripts/make_deck.py`, checked by eye as images.
- Release includes the deck. Router adds `/decision-deck`.
- New skill `deck-review`: two rounds of review from slide images, a cold read by a subagent, a score per slide, fixes, and a record in `deck-review.csv`.

## 0.3.1 (2026-10-18)
Small fixes from test round 3 (see tests/results/round-3.md).
- Post-hoc vs bug fix defined. Prior on the same scale before "not comparable".
- New check threshold-uncertainty. Rules for small gene panels (outliers, positive control).
- Grilling: answers that miss the question. Setup: source status `derived from`.
- Brief: answer directly after Question; captions do not count. Checkpoint: commit only if changed. Router step 4 clarified.

## 0.3.0 (2026-10-18)
Fixes from test round 2 (see tests/results/round-2.md).
- Success threshold: asked in grilling, stored in run.yaml (`success`, `success_source`); an assumed threshold is shown in the brief Answer with a sensitivity line.
- State in CLAUDE.md is updated at plan, status change, and release.
- Grilling DECISION entry has a fixed list of lines, with sources and prior strength; blocked sources are recorded.
- Sample removal counts go in run.yaml; LOG holds the rule.
- New checks: endpoint-validation, follow-up, treatment, test-size, platform-transfer for any cut-off. Sex from Y genes only. Outlier metric. Positive control must not be the predictor.
- to-analysis-plan builds the check list from CHECKS.md.
- Brief: word count rule, embedded figures, at most 4 tables.
- Release: two commits explained, md5 of inputs, State update.
- Checkpoint: commands to find misplaced files.

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
