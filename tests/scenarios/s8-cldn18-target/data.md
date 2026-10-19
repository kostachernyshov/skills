# Data for s8

UCSC Xena TOIL hub (TCGA, TARGET, and GTEx re-processed with one pipeline), `https://toil-xena-hub.s3.us-east-1.amazonaws.com/download/`.

- `gene_tpm_panel.tsv`: rows of `TcgaTargetGtex_rsem_gene_tpm.gz` for 20 genes (CLDN18 and lineage, housekeeping, and control genes). Values: log2(TPM + 0.001). Ensembl gene ids with version.
- `cldn18_isoform_tpm.tsv`: rows of `TcgaTargetGtex_rsem_isoform_tpm.gz` for the 3 CLDN18 transcripts. Values: log2(TPM + 0.001).
- `TcgaTargetGTEX_phenotype.txt.gz`: sample, study, tissue, sample type, sex.
- `gencode.v23.annotation.gene.probemap`, `gencode.v23.annotation.transcript.probemap`: id to gene symbol and coordinates.

The rows were cut from the full files with `awk` on the id column. No other change.
