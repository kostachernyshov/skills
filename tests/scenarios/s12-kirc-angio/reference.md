# Reference answer (grader only)

Score = mean z-score of the six genes over the 533 primary tumors (01). OS from `days_to_death` or `days_to_last_followup`, event `vital_status == DECEASED`; 531 patients with time > 0, 175 deaths. No duplicate patients in 01.

Cox OS:
- Score, continuous, per 1 SD of the mean z: HR 0.76 (0.65-0.89), p = 0.0005. With stage, grade, and age: HR 0.74 (0.61-0.90), n = 520.
- Above vs below the median: HR 0.63 (0.47-0.85). With stage, grade, and age: HR 0.83 (0.60-1.14), p = 0.24.
- Shuffled score, 100 shuffles: median HR 0.99 (95% range 0.84-1.20).
- Score falls with grade (G1 0.36, G4 -0.37 mean z).

Answer: TCGA shows that a high angiogenesis score is prognostic: it goes with longer survival after nephrectomy, and this agrees with the ccA/ccB subtypes. TCGA cannot show that the score predicts benefit from a VEGFR inhibitor: the patients were not treated with one (`targeted_molecular_therapy` YES in 12 of 945 rows), and there is no untreated control arm. The predictive claim needs trial data with a treatment interaction (for example IMmotion150, McDermott et al. 2018, Nat Med, where Angio-high went with longer PFS on sunitinib). The median cut-off is not stable after adjustment. Recommendation: do not use the score as an enrollment criterion on TCGA evidence; at most a stratification factor, with the cut-off fixed before the trial.

Traps: prognostic vs predictive; normal samples (72 RNA, 407 clinical rows); median split vs continuous; stage and grade confounding; survival built from two day columns; the score is already published (Angio signature, IMmotion150).
