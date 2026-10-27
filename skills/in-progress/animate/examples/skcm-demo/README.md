# Demo: T-cell score and survival in melanoma (TCGA SKCM)

A small project folder to test `/animate`. The report is a short demo, not a full analysis.

- Data: UCSC Xena TCGA hub, `TCGA.SKCM.sampleMap/HiSeqV2.gz` and `survival/SKCM_survival.txt` (public).
- `runs/R01-skcm-cyt/code/analysis.py <data dir> <out dir>` makes the tables in `out/` (needs pandas, scipy, lifelines).
- `code/voiceover.md` and `code/animation.yaml` are the inputs of the animation.
- `out/animation-board.png`, `out/animation.gif`, `out/animation-numbers.tsv`, and `out/animation-colors/colors.tsv` are the outputs.

Run from this folder:

```
A=../../scripts/animate.py
uv run --with pillow --with numpy --with pyyaml python3 $A check runs/R01-skcm-cyt/code/animation.yaml
uv run --with pillow --with numpy --with pyyaml python3 $A render runs/R01-skcm-cyt/code/animation.yaml /tmp/animation.mp4
```
