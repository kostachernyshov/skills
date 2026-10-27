# Changelog

## 0.12.1 (2026-10-27)
A promo video of the whole flow, made with `/animate`. Requested and accepted by Kosta (storyboard, voice-over, sprites) in the thread "Animation of how the skills repository works".

What changes for you:
- `promo/how-it-works/`: a video of about two minutes for the README. One road from the question to the release: grilling, a split into two runs (describe first, then the outcome), plan, analysis, report, supervisor veto and fix, signature, slides and video. Two asides: up to five runs, and several tasks at the same time. Numbers come from the SKCM demo files.
- `README.md` shows the animation at the top. The file is `docs/media/how-it-works.webp`: an animated WebP without loss, 960x540, 10 fps, 66 s, 0.7 MB, no sound. A GIF of the same video was 1.3 MB at half the size (480x270), so WebP is half the bytes at twice the size. The title and the last frame are calm; the last frame says: type `/ask-kosta`. Each scene has `dur` for the animation without voice; when the voice is added, its cues set the time. Record your voice for the MP4 with `promo/how-it-works/voiceover.md`.

Changes:
- `animate`: a plan can set `max_s` (a longer video of a process); a scene can set `fade: false` (one continuous shot); a `summary` can have a `module` (a custom final frame). See `SCENES.md`.
- `pixel_kit`: new sprites `person` (the one who decides), `agent`, `supervisor`, `lock`, `deck` (`STYLE.md`).
- `.gitignore`: demo data and video outputs.

## 0.12.0 (2026-10-27)
New experimental skill `animate`: a short pixel-art video that explains the design and the result of a run. Decision by Kosta (2026-10-27): `decisions/2026-10-27-animate-v0.12.0.md` in the project files.

What changes for you:
- Type `/animate` after `/analyze`. The agent writes an English voice-over, then a plan `animation.yaml`. You accept the voice-over and the storyboard. Then the agent renders `animation.mp4` (1920x1080) and `animation.gif`.
- The video ends with a summary frame (graphical abstract): the question, the design, the result chart, and the conclusion. It holds still for 10 s.
- Each number on screen comes from a result file. `animation-numbers.tsv` shows the file, the column, and the row of each number. Each scene points to a line of the report.
- Blue is the group with the better outcome, orange is the group with the worse outcome. Grey and lavender are for groups without "better" or "worse". `animate.py colors` checks contrast and the colors for deuteranopia and protanopia.
- A voice is optional. Give a WAV file and a transcript with times (for example from VoiceStudio). The scenes then start on the words.
- The skill is in `skills/in-progress/`. Do not copy it to a client project yet.

Changes:
- `skills/in-progress/animate`: `SKILL.md`, `SCENES.md` (plan format and scene types), `STYLE.md` (palette, meaning of colors, contrast, bio cast), `agents/openai.yaml`.
- `scripts/pixel_kit`: the pixel library from the cancer_wars project, on a light background (`PAPER` #FBFAF7, dotted grid), with a 1 px outline on sprites. The GIF uses one palette for the whole video. Unifont is a Latin subset (9 KB). New: the `summary` scene, charts (Kaplan-Meier, strip, distribution, heatmap, volcano), `data.py` (numbers from files only), `colorcheck.py` (Machado 2009 simulation, WCAG contrast, Delta E), `story.py` (plan to timeline), a 3x5 mini font, new props (`tube`, `plate`, `sequencer`, `datasheet`) and `clinician`.
- `scripts/animate.py`: commands `check`, `cues`, `board`, `colors`, `frames`, `animatic`, `render`, `preview`, `sheet`.
- `examples/skcm-demo`: a demo on public TCGA SKCM data (UCSC Xena): cytolytic score and overall survival. The repository keeps only the inputs (code, voice-over, plan, report); the README shows how to get the data and render.
- `ask-kosta`, `README.md`: the new skill.

## 0.11.1 (2026-10-24)
Small fixes after the check of 0.11.0 (`tests/results/check-0.11.0.md`). New issues: #47, #48, #49, #50.

What changes for you:
- The release copy of the report says "Report checked by the supervisor". The summary before the signature says that the supervisor does not check the deck.

Changes:
- `curator` ("Who decides") and the `LOG.md` template: `override: start` does not replace a plan; only the planner writes it. The agent says "Run /grill-with-plan first" each time the person asks. An existing project keeps its old section; copy the new line from `scripts/sections.md`.
- `planner`: a too-wide interval at the threshold is a known limit in `notes`, not a `todo`.
- `reviewer`: a self cold read has its own record line.
- `editor`: if the subagent cannot write the file, it returns the text, and the agent saves it without a change.
- Tests: scenario `s12-kirc-angio`.

## 0.11.0 (2026-10-24)
Fewer contradictions between the skills, and fewer loops. Decision by Kosta (2026-10-24): `decisions/2026-10-24-issues-v0.11.0.md` in the project files. Closes #18, #19, #20, #21, #23, #24, #25, #26, #27, #28, #29, #30, #31, #32, #33, #34, #35, #37, #38, #39, #40.

What changes for you:
- The supervisor checks the work of the agent. After its check you can change the report, the figures, and the deck. Nothing blocks you. `/publisher` shows the files that changed after the check and asks: run the supervisor again, or keep them. The release copy names the kept files. A change by the agent gets a new supervisor check.
- A veto names each question with "no", not only the first. The supervisor runs once, after the reviewer.
- A project rule starts at the next run. It does not apply to the run that it came from. The agent asks "Add RULE-NN?" in a separate message.
- The solution model in `CLAUDE.md` is for the whole project. The details of one run (a control, a threshold, a gene) go only in `run.yaml`. The planner can change the model after your "yes".
- To accept a doubt, the agent writes the existing `DECISION override: veto Q3 RNN` entry. A limit that the model or the plan already names is not a doubt.
- The report has no "Can reverse" column and no "see run.yaml" line. The owner of a next step is the person who decides. The main figure uses the full width of the page.

Changes:
- `supervisor`: `scripts/stamp.py` writes `checked` (each table, figure, and `report.md` in `out/`, with a checksum) in `run.yaml`; it replaces `- report <sha>` in the verdict. Q1 accepts a number from `run.yaml`. Q3 accepts a doubt only with a `DECISION override: veto Q3` entry. Q6 checks only the rules that existed when the plan was accepted. Stop after 3 vetoes of one report.
- `curator`: the script shows `changed after the supervisor check: <files>` (not a block), and a verdict without `checked` (not for a shipped run). A manual run of the script is allowed. The rule question is a separate message.
- `publisher`: shows the changed files before the signature; the release copy names the files that the person kept.
- `editor`: order is report, reviewer, supervisor. `WRITER.md` and `TEMPLATE.md`: no "Can reverse", no "see run.yaml", owner from `decision`, numbers from `run.yaml` with `[run.yaml]`, figure at full width.
- `reviewer`: one process for the deck and the report; report criteria with 2/0 definitions; CSV column `part`; the score is the score before the fix; the cold read uses only the images and names the part.
- `planner`: "do not look at the outcome" means the link between the predictor and the outcome; group sizes and event counts are allowed. Negative control: the median shuffled effect is at the null value of the statistic, independent of the answer; a rule for descriptive questions. Positive control examples moved here from `CHECKS.md`. `rules` holds the rules at plan acceptance. A path to change the model.
- `checker`: one table for changes after the result (bug fix, extra variant, new method). Known limits are not `todo`. The check `positive-control` is removed (the plan control covers it).
- `grilling`: one fixed order (useful action, search, run questions); continue a running grilling; 6 questions or fewer per round, all questions count; no run details in the model.
- `analyze`, `designer`: figures at 11 x 5 inches, fonts of 16 pt or more, one file for the report and the deck.
- `ask-kosta`: a row for changes that the person makes.
- Tests: the harness stops on a persona usage limit and resumes with a repeat of the last message (`test_harness.py`); default steps, `flow.json` files, and misuse specs use `/grill-with-plan` and `/analyze`; `tests/README.md` has a cost rule.

## 0.10.0 (2026-10-23)
Names, the person, and controls that the person removes. Decision by Kosta (grilling Q1-Q16, 2026-10-23): `decisions/2026-10-23-names-person-controls-v0.10.0.md` in the project files. Closes #7, #12, #14, #16, #17, #22, #36, #42.

What changes for you:
- The plugin is `kostachernyshov-skills`. Commands are `/kostachernyshov-skills:grill-me` and so on. Install again: `claude plugin install kostachernyshov-skills@kostachernyshov`.
- The skill `judge` is now `supervisor`. It checks one report against the files (the role of the supervisor in Yoon et al. 2026). A judge that compares several reports is a later role.
- The "brief" is now the "report": `out/report.md`, `out/report.pdf`, `releases/vN/report.md`, `scripts/report_pdf.sh`, `out/review-report.csv`, and `- report <sha>` in the verdict. In an older project, rename `out/brief.md` to `out/report.md` and run the supervisor again.
- `/setup-project` asks for your first name, last name, and role, and says where they go. They are in the `Person:` line of `CLAUDE.md`. Skills never write an e-mail address or an account login.
- A release is signed only by a "yes" in a reply to the release summary. A request such as "release v2" is not a signature.
- You can remove a control at the plan with a reason (why the control has no meaning for this question). The supervisor then passes the report with `pass - override Q2` and does not send the work back.

Changes:
- `setup-project`: asks for the name and the role; `Person:` line in the `CLAUDE.md` template; source status `public, not checked`; md5 of each data file; `.gitignore` no longer hides `*.gz` in `data/ref/`.
- `curator`: "Who decides" says where `<person>` comes from and forbids e-mail addresses; "Chat style": a new session starts at Q1. The script counts a `fail` with `override` as accepted. For an older project, replace the two sections with the text in `scripts/sections.md`.
- `publisher`: the summary says what the person takes responsibility for; only a "yes" in a later reply signs.
- `planner`: fits the controls to the type of study (for example clustering); a removed control with a valid reason gets `DECISION override: veto Q2 RNN` at the plan and `fail - removed by the person, override <date>`.
- `checker`, `analyze`: a `fail` with `override` does not stop the work.
- `supervisor`: an override entry from the plan counts; it covers the same defect in each question.
- `grilling`: no recommended mark on the options for the useful action.
- `editor`: `report_pdf.sh` writes its temporary `.docx` in a temporary folder, not in the run.
- `analyze`: step 8 is "Summary".
- Repository: `.gitignore` for Python caches.

## 0.9.0 (2026-10-22)
A new flow that protects the decisions of the person. Decision by Kosta after the misuse tests and round 8 (grilling Q1-Q30): `decisions/2026-10-22-flow-v0.9.0.md` in the project files. Closes #8, #9, #11, #12, #13, #15. Part of #19, #25, #38.

What changes for you:
- `/planner` and `/editor` are no longer commands (`user-invocable: false`). Use `/grill-with-plan` (interview, then plan) and `/analyze <RNN>` (the analysis and the brief). `/grill-me` stays for an interview without a plan.
- The agent does not start an analysis without an accepted plan, also when you ask in plain text.
- Each decision line shows `(person)` or `(agent)`. If the agent made more than half of them, you must say "start anyway", and the brief and the title slide show a red warning.
- The judge always runs. Without a verdict there is no release. An override of a veto needs a reason: the defect and why it does not change the decision. A deadline is not a reason.
- Questions are numbered Q1, Q2, ... through the session.

Changes:
- New person skill `grill-with-plan`: calls `grilling`, then `planner`. If a grilling entry for the next run exists, it asks only if the task is still valid.
- New person skill `analyze`: gate (confirmed model, `plan accepted`, override of the start if needed), needs and run time (asks if the controls take more than 10 minutes), packages in `.venv/` with versions in `run.yaml` `env`, input checks, code, a main figure and other figures, controls, then `editor`.
- `planner` is an agent skill. It does not run the analysis. It shows the share of `(agent)` decisions; above 4 of 8 it asks "Start anyway?" and writes `DECISION override: start RNN`. The negative control uses 100 shuffles (1000 only near the pass limit). `done_when` names the main figure.
- `editor` is an agent skill. The person cannot turn off the judge. With `context: forced`, the brief starts with a red warning block (style `Warning` in `reference.docx`).
- `grilling`: marks the 8 decision lines `(person)` or `(agent)` and writes `context: N of 8 (agent)`. The word `assumed` is gone. The model has no `(agent)` part.
- `judge`: question 7 (the grilling entry and the accepted plan exist; the Answer answers the question and serves the decision; the warning is there after a forced start). The judge checks the reason of an override: `pass - override Q<n>`.
- `publisher`: no release without a verdict. An override is a limit of the analysis with a valid reason; the publisher calls `editor` so that the brief names it and the judge checks it. The release copy of the brief ends with `Checked by the judge: <verdict>`, and the terminal shows it.
- `checker`: step 0 stops an analysis without an accepted plan. An `(agent)` answer does not accept a doubt.
- `curator`: shared sections "Who decides" and "Chat style" in `scripts/sections.md`. `curate.py --add-sections` adds them; for an older project the State lists them and the agent asks first. A brief without a verdict is Open.
- `setup-project`: adds the shared sections; `.venv/` in `.gitignore`. `designer`: a red `warning` on the title slide.
- `ask-kosta`: new flow, a row for an analysis asked in plain text, the list of skills that only the person starts.
- Tests: no test round for this version yet. The harness still types `/planner` and `/editor`; update it before the next round.
- Tests: round 8 for 0.8.0 (`tests/results/round-8.md`). New scenarios `s10-vague-model` and `s11-two-runs-rule`. `run_scenario.py` reads an optional `flow.json` and the persona text for a second run. New `harness/check_rules.py`.
- Tests: misuse tests. `tests/misuse/*.json` hold the errors of the person per step. `tests/harness/run_misuse.py` runs them, with `--resume` after a usage limit. Results of round 1 on 0.7.1: `tests/results/misuse-1.md`.

## 0.8.0 (2026-10-21)
Solution model and project rules. Decision by Kosta, without a test failure: `decisions/2026-10-21-model-and-rules.md` in the project files. Closes #2 and #3.
- `grilling`: builds the solution model of the project (useful action, method, plausibility) in `CLAUDE.md` between `model:begin` and `model:end`. The useful action is never `assumed`; when the person cannot name it, the agent proposes 2 to 4 options from the context. Without the person, the model stays `draft`. Each later grilling shows the model and asks if it is still valid. Changes go in `DECISION model`.
- `grilling`: the entry is the task of one run: `run`, `method`, `plausibility`, `inputs` (earlier runs), `rules`. Checks contradictions between the useful action, the data and method, and the resources. Reads the project rules and warns when an answer goes against one; a deviation is a `DECISION deviation RULE-NN` with the words of the person.
- Each new run starts with `/grill-me`. `planner` stops without a grilling entry for the new run or with a `draft` model. `run.yaml` has `inputs` and `rules`.
- Project rules: `curator` holds the steps. After a fixed `fail`, a post-hoc change, a fixed veto cause, an accepted `todo`, or "remember this", the agent proposes `RULE-NN` in one line. After "yes" it adds the line to `## Project rules` in `CLAUDE.md` and a `RULE` entry to `LOG.md`. The agent never changes or deletes a rule; only the person does, by hand. A general rule becomes a proposed issue in this repository.
- `checker` and `editor` call "curator" to propose a rule. `checker` applies the project rules.
- `judge`: question 6 (rules); the judge also reads `## Project rules` in `CLAUDE.md`.
- `setup-project`: the `CLAUDE.md` template has the sections `Solution model` and `Project rules`. `LOG.md` entry types: `DECISION model`, `DECISION deviation`, `RULE`.
- `ask-kosta`: each new run starts at `/grill-me`; new rows for a new run and for a lesson.

## 0.7.1 (2026-10-20)
Fixes from test round 6 (see tests/results/round-6.md).
- `planner`: the positive control size needs a source and is not computed from the predictor. The negative control uses at least 200 shuffles and compares to the shuffled distribution. Robustness variants are named before the data. One figure `out/fig-<what>.png`. After "yes" the agent runs the plan without another command.
- `checker`: a positive or negative control fail stops the work. A robustness fail does not block; it becomes `warn - answer changes when <variant>`, and the Answer says so. Each doubt is accepted by name; a general "use your recommendation" does not accept it.
- `judge`: the verdict carries the checksum of `brief.md`. A defect means "no". A wrong source file, an unnamed robustness warn, an unsupported options cell, or a blanket acceptance of doubts is a "no".
- `curator`: the script shows a verdict whose checksum does not match the brief. Do not run the script by hand after each edit; the hook runs it.
- `editor`: the main agent may change words and layout, not numbers or claims; render the PDF again and run the judge again after each change.
- `publisher`: compares the verdict checksum with `brief.md`.
- `designer`: 4 to 6 slides; the title slide does not count, the appendix does. `reviewer`: brief criteria scored 0/1/2.
- `ask-kosta`: commands with the plugin prefix; 6 steps.
- Tests: scenarios s7-s9 with reference answers, blind grader (`tests/harness/grade.py`), skill-use table (`tests/harness/skill_usage.py`), resume after a usage limit.

## 0.7.0 (2026-10-19)
Roles. Decision by Kosta, based on Yoon et al. 2026 (agent research tasks): `decisions/2026-10-19-roles-v0.7.md` in the project files. The skill `judge` is added by this decision, not after a test failure: in rounds 1-5 the agent judged its own work and knew more than the files showed.
- Renamed: `to-analysis-plan` → `planner`, `sanity-check` → `checker`, `decision-brief` → `editor`, `decision-deck` → `designer`, `deck-review` → `reviewer`, `release` → `publisher`.
- `project-order` and `checkpoint` → `curator`. A script builds the State block in `CLAUDE.md` from `run.yaml`. The plugin runs it with a Claude Code `Stop` hook (`hooks/hooks.json`). The script lists files out of place and never moves or deletes them.
- New: `judge`. A fresh subagent answers 5 yes/no questions from the files only. One "no" is a veto, written in `run.yaml` (`verdict`).
- `planner`: positive, negative (shuffled labels), and robustness controls fixed before the data; the person must approve the plan.
- `checker`: doubts become `todo` lines in `run.yaml`; the word "new" needs a recorded literature search; stop after 3 failed repairs of one check.
- `editor`: a fresh subagent writes the brief from `run.yaml`, `out/`, and `LOG.md`; then `judge` and `reviewer`.
- `publisher`: no release with a veto; only the person can override, with a reason in `LOG.md`; the person signs each release.
- Three points where the person acts: grilling answers, plan approval, release signature.
- `LOG.md` holds only decisions of the person and releases. Review records: `review-brief.csv`, `review-deck.csv`.

## 0.6.0 (2026-10-18)
Fixes from test round 5 (see tests/results/round-5.md).
- decision-brief: 300 words, 1 figure at half width, `scripts/brief_pdf.sh` renders an A4 PDF and counts pages; rule for revising a shipped brief.
- Deck script: table fonts applied and row height from text; big-number size from text length; larger secondary text.
- release: re-release of a shipped run without new numbers; brief.pdf; asks about other candidate runs.
- deck-review: review the rendered brief; replace deck-review.csv per release; source bracket check; space criterion for short bullet slides.
- DECK.md: one figure file for brief and deck, 11 x 5 in, plotting in its own script. Checkpoint and naming fixes.
- Plugin and marketplace manifests (own marketplace `kostachernyshov`); `agents/openai.yaml` in each skill for Codex; install and update commands in README.

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
