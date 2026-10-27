# Demo: T-cell score and survival in melanoma (TCGA SKCM)

A small project folder to test `/animate`. The report is a short demo, not a full analysis. The repository keeps only the inputs: the code, the voice-over, the plan, and the report. The data and the outputs are not in the repository.

- `runs/R01-skcm-cyt/code/analysis.py` makes the tables in `out/` from public UCSC Xena data (needs pandas, scipy, lifelines).
- `runs/R01-skcm-cyt/code/voiceover.md` and `runs/R01-skcm-cyt/code/animation.yaml` are the inputs of the animation.
- `runs/R01-skcm-cyt/out/report.md` is the report that the scenes point to.

Run from this folder:

```
mkdir -p data
curl -sL -o data/HiSeqV2.gz https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.SKCM.sampleMap%2FHiSeqV2.gz
curl -sL -o data/SKCM_survival.txt https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/survival%2FSKCM_survival.txt
uv run --with pandas --with scipy --with lifelines python3 runs/R01-skcm-cyt/code/analysis.py data runs/R01-skcm-cyt/out

A="uv run --with pillow --with numpy --with pyyaml python3 ../../scripts/animate.py"
P=runs/R01-skcm-cyt/code/animation.yaml
$A check $P
$A board $P runs/R01-skcm-cyt/out/animation-board.png
$A colors $P runs/R01-skcm-cyt/out/animation-colors
$A render $P runs/R01-skcm-cyt/out/animation.mp4 runs/R01-skcm-cyt/out/animation.gif
```
