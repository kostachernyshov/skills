# Tests

Each test round runs a fresh agent on a scenario. Rounds 1-5 used a subagent that read the skills. From round 6 the agent is a real Claude Code session with the plugin. The agent uses the skills as a user would. A grader scores the project with `RUBRIC.md`. Each failure becomes a change in a skill or a new check.

## Protocol

1. Make an empty project folder outside this repository. Copy the data into it.
2. Give the agent: the path to `skills/`, the path to `persona.md`, the project folder. Do not give it `RUBRIC.md`.
3. From 0.7.0 the test runs in real Claude Code with the plugin installed (`harness/run_scenario.py`). A driver types the person commands in this order: `/ask-kosta`, `/setup-project`, `/grill-with-plan`, `/analyze`, `/designer`, `/publisher`. The agent skills and the curator hook start by themselves.
   A scenario can set its own command order in `flow.json` (for example two runs in one project). `harness/check_rules.py` prints the solution model, the project rules, and the turn of each rule write.
4. A persona model answers the questions of the agent from `persona.md`. A question without an answer gets "use your recommendation". The persona signs a release only without a supervisor veto.
5. At the end the agent reports the skills it used and each point where a skill was unclear or wrong (friction).
6. `harness/skill_usage.py` makes the table "skill → called → when" from the session logs.
7. A blind grader (`harness/grade.py`) scores each project copy with `RUBRIC.md`. It does not know the run number or the version.
8. Report min–max per item over the replicates. A change to a skill is accepted only if the gain is larger than the spread.

## Cost

A full round costs about 60 M tokens. Use the smallest test that can show the failure.

- For a fix: 1 short run of the scenario that showed the failure. If the fix is in grilling or the planner, stop after the plan (`--stop-after`, or a `flow.json` like s10).
- Before the release of a version: a full round with 2 replicates per scenario.
- Write the budget of the round (tokens or USD) in the results file before the start. `harness/cost.py` gives the real cost after the round.
- If the agent or the persona hits a usage limit, the harness stops. Run it again with `--resume`.

## Misuse tests

A misuse test gives the person wrong behavior: wrong decisions, skipped steps, a forbidden supervisor, commands in the wrong order. Each spec in `misuse/` names a scenario and, for each step, the error that it injects. Run it with `harness/run_misuse.py --spec misuse/<id>.json`. Score each injected error by the expected reaction in the text of the skills.

## Scenarios

| Id | Data | Question | Traps |
|---|---|---|---|
| s1-tcga-esr1 | TCGA-BRCA from UCSC Xena: log2(RSEM+1) RNA-seq, clinical matrix | Can ESR1 mRNA replace IHC ER status for trial screening? | normal tissue, metastases, male patients, two ER columns, indeterminate values |
| s3-luad-mki67 | TCGA-LUAD from UCSC Xena | Does high MKI67 predict worse overall survival in stage I, beyond age and sex? | overall survival must be built from two day columns, `[Discrepancy]` and unspecified stage labels, normal and recurrent samples, both sexes (sex-gene check applies) |
| s4-gbm-mgmt | TCGA-GBM 27k methylation (beta values) and clinical | Can array data call MGMT status, and does methylated MGMT go with longer survival on temozolomide? | no reference MGMT test in the data, G-CIMP confounding, treatment fields, recurrent and normal samples |
| s5-skcm-immune | TCGA-SKCM RNA-seq and clinical | Does a high cytotoxic T-cell score predict longer survival in melanoma? | most samples are metastases collected long after diagnosis (survival time origin, left truncation), primary vs metastatic, no fixed gene list |
| s6-crc-msi | TCGA-COADREAD RNA-seq and clinical | Can RNA expression flag MSI-high tumors and replace the MSI test? | three MSI columns, MSI-L grouping, class imbalance, sporadic (MLH1 silencing) vs Lynch |
| s7-luad-egfr-smoking | TCGA-LUAD clinical matrix and MC3 mutation calls | Can the lab skip EGFR testing in heavy smokers? | samples without mutation calls are not wild-type; sensitizing vs other EGFR variants (exon 20 insertions, T790M alone, variants of unknown effect); two smoking fields and missing pack-years; clinical EGFR fields vs MC3 calls; answer as missed patients with an interval, not "rarer in smokers"; research exome vs clinical assay and ancestry |
| s8-cldn18-target | TOIL TCGA + GTEx TPM: 20-gene panel, CLDN18 transcripts, phenotype | In which tumors is Claudin 18.2 expressed, and is it absent from normal tissue? | gene level mixes 18.1 (lung) and 18.2 (stomach); which transcript is which must come from the data or a cited source, not from coordinates; normal stomach expresses 18.2 (on-target, off-tumor); lung signal is 18.1; mRNA level does not give IHC eligibility; log2(TPM+0.001) scale; TCGA adjacent normal vs GTEx normal; esophageal set mixes squamous and adenocarcinoma |
| s9-tmb-prognosis | MC3 calls for 8 TCGA types and the TCGA-CDR survival table | Is TMB-high a favorable prognosis in all cancers, and is it new? | pooled estimate confounded by cancer type; TCGA patients did not get immunotherapy (prognostic, not predictive); exome TMB vs panel TMB cut-off; MSI/POLE hypermutators in UCEC, COAD, STAD; OS vs PFI (CDR advice); metastatic samples (SKCM 06) and duplicates; "new" needs a literature search; effect differs by type |
| s10-vague-model | TCGA-BRCA from UCSC Xena (same files as s1) | "Find something useful about ESR1" (vague) | the person does not know who gets the benefit; two days and an independent cohort that does not exist; the run stops after the plan |
| s11-two-runs-rule | TCGA-LUAD from UCSC Xena (same files as s3) | R01: MKI67 and survival in stage I; R02: TOP2A in stage I and II | "remember this: radiation patients are out" must become a rule; in R02 the person asks to keep them; two radiation fields |
| s2-gse7390-signature | GEO GSE7390 (TRANSBIG), 198 patients, 76 probes, clinical | Does the 76-gene signature predict distant metastasis beyond clinical factors? | probe ids without symbols, signature weights not in data, time in days, label typo, ER-specific signature |
