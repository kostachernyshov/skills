# Checks by data type

Each check: what to test, how, what result passes.

## Any table with samples (input checks)

| Check | How | Pass |
|---|---|---|
| ids-match | Compare sample ids in the expression table and in the clinical table. | All ids match, or the mismatch is listed and explained. |
| one-sample-per-subject | Count samples per patient or subject id. | One sample per subject in the analysis set, or the design is paired on purpose. |
| sample-type | List sample types (tumor, normal, metastasis, cell line). | Only the types that the question needs. |
| missing-values | Count missing values per key column (outcome, group, covariates). | The count is known and each removal is in `LOG.md`. |
| category-labels | List the unique values of each categorical column. | No typos, no mixed case, no "unknown" variants that split one group. |
| group-sizes | Count samples per group. | Each group has enough samples for the method. Write the counts. |

## Expression data (input checks)

| Check | How | Pass |
|---|---|---|
| scale | Look at min, median, max. Find out if values are counts, log, or z-scores. | The scale fits the method. |
| identifiers | Find the identifier type (symbol, Ensembl, probe). | Annotation exists, or the result uses raw identifiers and says so. |
| sex-genes | If sex is in the clinical data and the data has XIST and Y genes (RPS4Y1, DDX3Y, KDM5D): compare. | Expression sex matches the recorded sex. List each mismatch. |
| outliers | PCA or sample correlation. | No sample is far from all others, or it is listed with a reason. |
| batch | Color PCA by batch, site, or plate if known. | The main axes do not follow batch, or the model includes batch. |

## Expression data (result checks)

| Check | How | Pass |
|---|---|---|
| positive-control | Find a gene or effect that must appear (for example ESR1 high in ER-positive breast tumors). | The control appears with the expected sign and a clear size. |
| p-value-distribution | Histogram of raw p-values. | Flat with a peak near 0. A peak near 1 or a hill in the middle is a fail. |
| effect-size | Look at the top effects. | Sizes are plausible for the biology (not 20 log2 units). |
| prior | Compare with the published result. | Agrees or the difference is explained. |

## Survival and outcome data

| Check | How | Pass |
|---|---|---|
| events | Count events and follow-up time. | Events are enough for the model (about 10 events per variable). |
| time-units | Find the unit of time (days, months, years). | The unit is known and written in each figure. |
| proportional-hazards | Test or plot Schoenfeld residuals for a Cox model. | No strong violation, or it is reported. |
| confounding | Check known prognostic variables (age, grade, stage, ER). | The main effect stays after adjustment, or the change is reported. |
