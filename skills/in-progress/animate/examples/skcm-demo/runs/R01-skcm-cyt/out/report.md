# Demo report: cytotoxic T-cell score and survival in melanoma (TCGA SKCM)

This is a short demo report for the /animate skill. It is not a full analysis and was not checked by the supervisor.

Question: do melanoma patients with a high cytotoxic T-cell score live longer?
Decision: put a prognostic claim in a brochure, put a weaker claim, or no claim.
Reader: head of marketing (no statistics).

Data: TCGA SKCM RNA-seq (UCSC Xena, log2(RSEM + 1)), one tumor sample per patient: 470 patients, 104 primary tumors and 366 metastases.
Score: cytolytic activity (CYT), the mean of log2 GZMA and PRF1 (Rooney et al., Cell 2015).
Groups: split at the median score: high and low.
Outcome: overall survival from diagnosis (TCGA Pan-Cancer clinical data), 453 patients with follow-up, 213 deaths.

Result: patients with a high score lived longer. Hazard ratio high vs low 0.52 (95% CI 0.40 to 0.69), Cox model, p < 0.001.
Median overall survival: 9.8 years (high) and 4.8 years (low).
The high group has more of the T-cell genes (CD8A, GZMA, PRF1, NKG7, LAG3, PDCD1); this follows from how the groups were made.
Primary tumors had a lower score than metastases (median 6.32 vs 7.26).

Limit: most samples are metastases, collected years after diagnosis. A patient had to survive until that time to give a sample. This can make the effect look larger.
Limit: the score is from tumor RNA. It does not show which test the customer sells.

Recommendation: a weaker claim: "a higher T-cell score was linked with longer survival in a public melanoma cohort".
