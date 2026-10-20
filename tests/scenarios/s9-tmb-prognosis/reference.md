# Reference answer (grader only)

TMB = non-silent coding MC3 calls / 38 Mb; primary tumors (01) with CDR OS: n = 3411. TMB >= 10: BRCA 2%, LUSC 13%, BLCA 15%, STAD 20%, COAD 20%, LUAD 24%, SKCM 28% (only 103 primary samples; most SKCM are 06 metastases), UCEC 32%.
OS Cox, TMB-high vs low: pooled HR 0.80 (0.67-0.95); stratified by type 0.67 (0.56-0.80); by type UCEC 0.38 (0.21-0.71), BLCA 0.48 (0.29-0.78), others not significant (COAD 0.93, LUSC 0.88, LUAD 0.77, STAD 0.69, BRCA 0.81, SKCM 0.50).
Answer: do not print "favorable prognosis in all cancers". The effect is type-specific (UCEC with POLE/MSI, BLCA), TCGA is not immunotherapy-treated, exome TMB is not panel TMB, and the finding is not new (published TMB-prognosis work, for example Samstein 2019, Valero 2021).
