# Round 6 (skills v0.7.0), 2026-10-19

Goal: test the roles of v0.7.0 on three new questions with public data. Each scenario ran 3 times. A persona model (Haiku) played the person. A blind grader (Opus, fresh context, copy of the project under a random name) scored each project with `tests/RUBRIC.md`. Projects: `/mnt/project-files/skill-tests/round6/`.

Scenarios:
- s7: can heavy smokers with lung adenocarcinoma skip the EGFR test? (TCGA LUAD, MC3)
- s8: is CLDN18.2 a good target, in which tumors, and is it safe for normal tissue? (TOIL TCGA + GTEx, isoform level)
- s9: does high TMB mean longer survival in 8 cancer types? (MC3 + PanCanAtlas CDR)

Three runs stopped at the account usage limit. The harness cut each session at the limit and resumed it. s7-1 and s9-1 were first resumed without the cut; their later turns are real, but the record of those runs has noise.

## Scores (yes count minus overclaims)

| Run | Score | Items | Overclaims | "No" items |
|---|---|---|---|---|
| s7-1 | 18 | 20 | 0 | H3, O3 (person did not sign) |
| s7-2 | 19 | 20 | 0 | J2 |
| s7-3 | 19 | 20 | 0 | J2 |
| s8-1 | 20 | 22 | 0 | J2, T8 |
| s8-2 | 16 | 22 | 1 | J2, J4, T3, T5, T8 |
| s8-3 | 19 | 22 | 0 | H1, J2, T8 |
| s9-1 | 12 | 22 | 0 | B1, B2, H1, H3, J1, J2, J3, O3, T5, T7 |
| s9-2 | 20 | 22 | 0 | J2, T7 |
| s9-3 | 15 | 22 | 2 | H1, J3, J4, O3, T2 |

| Scenario | min | max |
|---|---|---|
| s7 | 18 | 19 |
| s8 | 16 | 20 |
| s9 | 12 | 20 |

J2 was "no" in 8 of 9 runs. In 6 runs the cause was a robustness `warn` or a control rule changed after the data. The rubric asks for all controls `pass`; the skills (0.7.1) now allow a robustness `warn` that the Answer names. Compare rounds without J2.

## Answers
- s7: all 3 runs answer "No" with 11-12 of 233-248 heavy smokers (4.7-4.8%, upper bound 8.3%). Agrees with the reference.
- s8: all 3 runs find isoform 18.2 and stomach and pancreas as the main tumors (70-78% at 10-15 TPM; s8-2 used a cut-off calibrated to IHC, 38%). No run split esophageal cancer by histology (T8). s8-2 wrote "healthy tissues look safe" while normal stomach is 58% above the cut-off (overclaim).
- s9: s9-1 found that the effect goes away without hypermutated tumors, but gave the client no brief (robustness fail blocked it). s9-2 and s9-3 answer "No" (effect in 2-3 of 8 types). s9-3 wrote "clear benefit" (cause language). No run told the client that TMB and survival is already published (T7).

## Skill use (9 runs)

| Skill | Who started it | Note |
|---|---|---|
| ask-kosta, setup-project, grill-me, planner, editor, designer, publisher | person (command) | When the agent tried the Skill tool for a person skill, the tool refused. 3 agents read the person skill files and followed them without the command. |
| grilling | agent, 9/9 | Called from grill-me. |
| checker | agent 4/9, read only 4/9, never 1/9 | Often read with `cat`, not called. |
| curator | hook 14-21 times per run; agent read or ran the script by hand 8-15 times per run | The agent does not see the hook output, so it ran the script itself. |
| judge | fresh subagent 8/9 (1-3 times per run) | s9-1 had no brief. Vetoes caught a post-hoc rule not named and a wrong source file. |
| reviewer | agent 7/9 | Cold reads of brief and deck by subagents. |
| dataviz (not ours) | agent 3/9 | Before the figure. |

## Failures and fixes in 0.7.1

| # | Failure | Seen in | Fix |
|---|---|---|---|
| F1 | Controls with fixed narrow bands; positive size from memory | s8-1, s9-1 | planner: size needs a source and is not from the predictor; ≥200 shuffles, compare to the shuffled distribution |
| F2 | Robustness fail blocks the brief; client gets nothing | s9-1 | checker: robustness fail becomes `warn - answer changes when ...`; the Answer names it |
| F3 | Main agent edits brief.md | s7-2, s9-2 | editor: words and layout only, not numbers or claims |
| F4 | PDF not rendered again after an edit | s8-1 | editor: render again after each change |
| F5 | Judge passed "Can reverse: yes" with no source; passed with a wrong-file note | s8-1 | QUESTIONS.md: a defect means "no"; new "no" cases |
| F6 | Verdict holds only a date | all | verdict carries `brief <sha256[:8]>`; curator and publisher compare it |
| F7 | "Use your recommendation" turned into a DECISION that closed all doubts | s8-2, s7-3, s9-2 | checker and judge: each doubt accepted by name, with the words of the person |
| F8 | Commands need the plugin prefix `/skills:` | all | ask-kosta writes the prefix |
| F9 | "Run the plan" step was not needed | all | planner runs the plan after "yes" |
| F10 | Agent ran curate.py by hand many times | all | curator: do not run it by hand after each edit |
| F11 | Slide count unclear | s7-2 | DECK.md: title slide does not count, appendix does |
| F12 | Brief criteria had no scale | s7-2 | CRITERIA.md: 0/1/2 |
| F13 | No figure when the brief has none | s8-1 | planner: one figure in done_when |

Not fixed (seen, no clear skill fix yet):
- T7: the client wanted to publish a finding that is already known. The word "new" was not used, so the literature rule did not start.
- T8: a mixed tumor group (esophageal cancer) was not split by histology.
- H1: the persona did not give a success threshold, so the agent assumed one. This is the persona, but the brief must say "assumed" (it did).
