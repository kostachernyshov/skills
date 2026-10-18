# Checks by data type

Each check: what to test, how, what result passes. Use `n/a - <reason>` when a check does not apply.

## Any table with samples (input checks)

| Check | How | Pass |
|---|---|---|
| ids-match | Compare sample ids in the expression table and in the clinical table. | All ids match, or the mismatch is listed and explained. |
| one-sample-per-subject | Count samples per patient or subject id. | One sample per subject in the analysis set, or the design is paired on purpose. |
| sample-type | List sample types (tumor, normal, metastasis, cell line). | Only the types that the question needs. |
| missing-values | Count missing values per key column (outcome, group, covariates). | The count is known and each removal is in `LOG.md`. |
| category-labels | List the unique values of each categorical column. | No typos, no mixed case, no "unknown" variants that split one group. |
| duplicate-variables | Find columns that record the same variable (two ER fields, two survival times). Cross-tabulate them. | The reference column is chosen, and the disagreement rate is written. |
| group-sizes | Count samples per group. | Each group has enough samples for the method. Write the counts. |

## Expression data (input checks)

| Check | How | Pass |
|---|---|---|
| scale | Look at min, median, max. Find out if values are counts, log, or z-scores. | The scale fits the method. |
| identifiers | Find the identifier type (symbol, Ensembl, probe). | Annotation exists, or the result uses raw identifiers and says so. |
| sex-genes | If sex is in the clinical data and the data has XIST and Y genes (RPS4Y1, DDX3Y, KDM5D): compare. | Expression sex matches the recorded sex. List each mismatch. |
| outliers | PCA or sample correlation. | No sample is far from all others, or it is listed with a reason. |
| batch | Color PCA by batch or plate. If no batch column exists, use the collection site or center (for TCGA: the tissue source site in the barcode). | The main axes do not follow batch, or the model includes batch. |

## Expression data (result checks)

| Check | How | Pass |
|---|---|---|
| positive-control | Find a gene or effect that must appear (for example ESR1 high in ER-positive breast tumors). If the data has no such gene, use a known clinical association instead. | The control appears with the expected sign and a clear size. |
| p-value-distribution | Histogram of raw p-values. Only for many tests. | Flat with a peak near 0. A peak near 1 or a hill in the middle is a fail. |
| effect-size | Look at the top effects. | Sizes are plausible for the biology (not 20 log2 units). |
| prior | Compare with the published result. | Agrees or the difference is explained. |

## Classifier or cut-off

| Check | How | Pass |
|---|---|---|
| split | Choose the cut-off on one part of the data and measure on another part, or use cross-validation. | Agreement is measured on data not used to choose the cut-off. |
| error-balance | Report both error types (false positive and false negative) with confidence intervals. | The error that costs more for the decision is named and measured. |

## Survival and outcome data

| Check | How | Pass |
|---|---|---|
| events | Count events. Divide by the number of model terms (events per variable, EPV). | EPV 10 or more: pass. 5 to 10: warn. Below 5: fail. |
| time-units | Find the unit of time (days, months, years). | The unit is known and written in each figure. |
| proportional-hazards | Test or plot Schoenfeld residuals for a Cox model. | No strong violation, or it is reported with a fixed-horizon result. |
| confounding | Check known prognostic variables (age, grade, stage, ER). | The main effect stays after adjustment, or the change is reported. |
| model-fit | Check that each model converged. | No convergence warning in the main models. |

## Published signature or model

| Check | How | Pass |
|---|---|---|
| weights-source | Find the published weights, genes, and cut-off. Record the table and the page. Put the file in `data/ref/`. | The source is cited. Values are checked against the source. |
| platform-transfer | Compare the platform and the normalization of these data with the original study. | Same platform, or the effect of the change is stated. |
| cutoff-transfer | Check if the original cut-off can be applied to these data. | The original cut-off is used, or the result uses a continuous score and says why. |
| optimism | A gain in C-index or AUC measured on the same data is optimistic. | The gain is validated (bootstrap optimism correction or a held-out set), or it is reported as in-sample. |
