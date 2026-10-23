# Checks by data type

Each check: what to test, how, what result passes. Use `n/a - <reason>` when a check does not apply.

## Any table with samples (input checks)

| Check | How | Pass |
|---|---|---|
| ids-match | Compare sample ids in the expression table and in the clinical table. | All ids match, or the mismatch is listed and explained. |
| one-sample-per-subject | Count samples per patient or subject id. | One sample per subject in the analysis set, or the design is paired on purpose. |
| sample-type | List sample types (tumor, normal, metastasis, cell line). | Only the types that the question needs. |
| missing-values | Count missing values per key column (outcome, group, covariates). | The count is known. The rule is in `LOG.md`, the counts in `run.yaml`. |
| category-labels | List the unique values of each categorical column. | No typos, no mixed case, no "unknown" variants that split one group. |
| duplicate-variables | Find columns that record the same variable (two ER fields, two survival times). Cross-tabulate them. | The reference column is chosen, and the disagreement rate is written. |
| group-sizes | Count samples per group. | Each group has enough samples for the method. Write the counts. |

## Expression data (input checks)

| Check | How | Pass |
|---|---|---|
| scale | Look at min, median, max. Find out if values are counts, log, or z-scores. | The scale fits the method. |
| identifiers | Find the identifier type (symbol, Ensembl, probe). | Annotation exists, or the result uses raw identifiers and says so. |
| sex-genes | If sex is in the clinical data and the data has Y genes (RPS4Y1, DDX3Y, KDM5D, EIF1AY): call sex from the mean of the Y genes. Set the threshold at the gap between the two groups. Do not use XIST: some male tumors express it. | Expression sex matches the recorded sex. List each mismatch. |
| outliers | PCA on the top 2000 variable genes (all genes for a small panel). Distance of each sample from the center on PC1 and PC2 in SD units. | No sample beyond 4 SD, or it is listed with a reason. |
| tissue-composition | If the score measures cells that also live in the sampled tissue (immune cells in lymph nodes, stroma, normal tissue), compare the score across sample sites. | The effect holds within each site, or the model includes the site. |
| batch | Color PCA by batch or plate. If no batch column exists, use the collection site or center (for TCGA: the tissue source site in the barcode). If site and outcome are linked, test site within each outcome group. | The main axes do not follow batch, or the model includes batch. |

## Methylation array data (input checks)

| Check | How | Pass |
|---|---|---|
| meth-scale | Find if values are beta (0 to 1) or M-values. Convert with M = log2(beta / (1 - beta)) when a published model needs M. | The scale fits the model. A model fit on another scale is a `warn`. |
| meth-probes | Check that each probe the analysis needs is present and has few missing values. | All needed probes are present. |
| meth-sex | If a probe manifest with chromosomes is available, compare chrX and chrY probe signal with the recorded sex. | Matches, or `n/a` with the reason. |
| cross-reactive | Check needed probes against published lists of cross-reactive or SNP-affected probes. | None of the needed probes is affected, or it is reported. |

## Expression data (result checks)

| Check | How | Pass |
|---|---|---|
| positive-control | Find a gene or effect that must appear (for example ESR1 high in ER-positive breast tumors). The control must not be the predictor under test: if ESR1 is the predictor, use PGR, GATA3, or FOXA1. If the data has no such gene (small panel), use a named clinical association with a published effect, for example "grade 3 vs grade 1 predicts metastasis". | The control appears with the expected sign and a clear size. |
| p-value-distribution | Histogram of raw p-values. Only for many tests. | Flat with a peak near 0. A peak near 1 or a hill in the middle is a fail. |
| effect-size | Look at the top effects. | Sizes are plausible for the biology (not 20 log2 units). |
| prior | Compare with the published result. | Agrees or the difference is explained. If no prior exists: `n/a`, and the plan controls carry the evidence. |

## Classifier or cut-off

| Check | How | Pass |
|---|---|---|
| split | Choose the cut-off on one part of the data and measure on another part, or use cross-validation. Applies each time the report gives a classification rate. | Agreement is measured on data not used to choose the cut-off. |
| error-location | List the false negatives and false positives. Compare them with the clinically critical subgroup (for example MSI tumors with normal MLH1, which include Lynch cases). | The error rate in the critical subgroup is reported. |
| test-size | Compute the confidence interval of the key rate in the test part. | The interval is narrow enough to tell if the success threshold is met. If not, write `warn`. |
| threshold-uncertainty | Compare the confidence interval of the main result (any data type) with the `success` threshold. | The whole interval is on one side of the threshold. If the interval crosses it, write `warn` and say so in the report. |
| platform-transfer | A cut-off found on one assay (RNA-seq) does not move to another assay (qPCR, IHC, a new lab) without new calibration. | The report says on which assay the cut-off is valid. |
| error-balance | Report both error types (false positive and false negative) with confidence intervals. | The error that costs more for the decision is named and measured. |

## Survival and outcome data

| Check | How | Pass |
|---|---|---|
| endpoint-validation | Test a known strong factor against the outcome. Use a factor measured at the time origin: stage for survival from diagnosis; distant vs regional metastasis for survival from sampling. | The known factor gives the expected effect. This shows that the outcome variable is built correctly. |
| time-origin | Compare the date of the sample with the date of diagnosis. | If samples were taken long after diagnosis, survival starts at sampling, or the analysis corrects for left truncation. |
| treatment-received | A group defined by treatment received after the start of follow-up (for example "patients who got temozolomide") favors patients who lived long enough to get it. | Use a landmark analysis or treat the group as confounded. Do not claim a treatment-specific effect without an interaction test in a fair comparison. |
| follow-up | Median follow-up of patients without an event (reverse Kaplan-Meier). Number at risk at the time horizon of the question. | Follow-up covers the horizon. If not, write `warn` and name the horizon that the data can support. |
| treatment | Find which treatment patients received. Count unknown values. | Treatment is known and in the model, or the missing information is a `warn` in the report. |
| events | Count events. Divide by the number of model terms (events per variable, EPV). | EPV 10 or more: pass. 5 to 10: warn. Below 5: fail. |
| time-units | Find the unit of time (days, months, years). | The unit is known and written in each figure. |
| proportional-hazards | Test or plot Schoenfeld residuals for a Cox model. | No strong violation, or it is reported with a fixed-horizon result. |
| confounding | Check known prognostic variables (age, grade, stage, ER). | The main effect stays after adjustment, or the change is reported. |
| model-fit | Check that each model converged. | No convergence warning in the main models. |

## Published signature or model

| Check | How | Pass |
|---|---|---|
| weights-source | Find the published weights, genes, and cut-off. Record the table and the page. Put the file in `data/ref/`. | The source is cited. Values are checked against the source. |
| signature-platform | Compare the platform and the normalization of these data with the original study. | Same platform, or the effect of the change is stated. |
| cutoff-transfer | Check if the original cut-off can be applied to these data. | The original cut-off is used, or the result uses a continuous score and says why. |
| optimism | A gain in C-index or AUC measured on the same data is optimistic. | The gain is validated (bootstrap optimism correction or a held-out set), or it is reported as in-sample. |
