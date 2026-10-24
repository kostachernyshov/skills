# Data for s12

- `HiSeqV2.gz`: UCSC Xena TCGA hub, `TCGA.KIRC.sampleMap/HiSeqV2.gz` (log2(RSEM norm count + 1), 20530 genes, 606 samples: 533 primary tumors 01, 72 normal 11, 1 new primary 05).
- `KIRC_clinicalMatrix.tsv`: UCSC Xena TCGA hub, `TCGA.KIRC.sampleMap/KIRC_clinicalMatrix` (945 rows, 407 of them normal samples, many without RNA).

Download: `https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.KIRC.sampleMap%2FHiSeqV2.gz` and `.../TCGA.KIRC.sampleMap%2FKIRC_clinicalMatrix` (saved as `KIRC_clinicalMatrix.tsv`).
