# Tests

Each test round runs a fresh agent on a scenario. The agent uses the skills as a user would. A grader scores the project with `RUBRIC.md`. Each failure becomes a change in a skill or a new check.

## Protocol

1. Make an empty project folder outside this repository. Copy the data into it.
2. Give the agent: the path to `skills/`, the path to `persona.md`, the project folder. Do not give it `RUBRIC.md`.
3. The agent simulates the person who types the person skills in this order: `/ask-kosta`, `/setup-project`, `/grill-me`, `/to-analysis-plan`, analysis, `/decision-brief`, `/decision-deck`, `/release`, `/checkpoint`. The agent skills start when their description fits.
4. The persona file answers the grilling questions. A question without an answer gets "use your recommendation".
5. The agent reports: the grilling rounds, the result, and each point where a skill was unclear or wrong (friction).
6. The grader scores the project folder with `RUBRIC.md` and writes `results/round-N.md`.

## Scenarios

| Id | Data | Question | Traps |
|---|---|---|---|
| s1-tcga-esr1 | TCGA-BRCA from UCSC Xena: log2(RSEM+1) RNA-seq, clinical matrix | Can ESR1 mRNA replace IHC ER status for trial screening? | normal tissue, metastases, male patients, two ER columns, indeterminate values |
| s3-luad-mki67 | TCGA-LUAD from UCSC Xena | Does high MKI67 predict worse overall survival in stage I, beyond age and sex? | overall survival must be built from two day columns, `[Discrepancy]` and unspecified stage labels, normal and recurrent samples, both sexes (sex-gene check applies) |
| s4-gbm-mgmt | TCGA-GBM 27k methylation (beta values) and clinical | Can array data call MGMT status, and does methylated MGMT go with longer survival on temozolomide? | no reference MGMT test in the data, G-CIMP confounding, treatment fields, recurrent and normal samples |
| s5-skcm-immune | TCGA-SKCM RNA-seq and clinical | Does a high cytotoxic T-cell score predict longer survival in melanoma? | most samples are metastases collected long after diagnosis (survival time origin, left truncation), primary vs metastatic, no fixed gene list |
| s6-crc-msi | TCGA-COADREAD RNA-seq and clinical | Can RNA expression flag MSI-high tumors and replace the MSI test? | three MSI columns, MSI-L grouping, class imbalance, sporadic (MLH1 silencing) vs Lynch |
| s2-gse7390-signature | GEO GSE7390 (TRANSBIG), 198 patients, 76 probes, clinical | Does the 76-gene signature predict distant metastasis beyond clinical factors? | probe ids without symbols, signature weights not in data, time in days, label typo, ER-specific signature |
