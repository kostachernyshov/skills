# How the skills work: source of the promo video

This file is the source of the video in this folder. Each scene of `animation.yaml` points to one line here (`claim: L<n>`). The example numbers come from the SKCM demo of `/animate` (public TCGA data). Commands to build the video are at the end.

The skills take a bioinformatics project from the question of a client to a decision that the client can trust.
A client often asks for two kinds of work in one request: describe the immune cells in melanoma, and predict survival.
Grilling asks questions before any work: who acts on the answer, why it can work, and what is enough.
Grilling marks each decision with the one who made it: (person) or (agent).
If the request mixes two types of task, grilling proposes a split into runs: first describe the biological system without the outcome, then work with the outcome.
Before any data, the planner writes the plan: the success threshold, a positive control, a negative control, and a robustness check. The person approves the plan.
Run R01 describes the biology: T-cell genes in each tumor sample, primary tumors and metastases. Survival data stay closed.
The result of R01 shapes the plan of R02.
Run R02 works with the outcome: patients with a high T-cell score lived longer.
A fresh agent writes a one-page report from the files only. It does not read the chat.
The supervisor answers seven yes or no questions from the files. One "no" is a veto.
Example of a veto: the draft said that T cells give longer life. The data show a link, not a cause. The report was fixed to "linked, not proven", and the supervisor gave a pass.
Only the person signs the release. After the signature, the release does not change.
From the report, the agent makes a short deck for the meeting (designer) or a short video like this one (animate).
A big task can split into more runs, for example five. Each run has its own plan, its own checks, and its own report.
A person can run several tasks at the same time. The work of the person is to state each task well, answer the grilling, and accept the result.
To start, type /ask-kosta in a project.

## Build

From the repository root, with the SKCM demo tables in `skills/in-progress/animate/examples/skcm-demo/runs/R01-skcm-cyt/out/` (see the README of the demo):

```
A="uv run --with pillow --with numpy --with pyyaml python3 skills/in-progress/animate/scripts/animate.py"
P=promo/how-it-works/animation.yaml
$A check $P
$A board $P promo/how-it-works/out/animation-board.png
$A render $P promo/how-it-works/out/animation.mp4 promo/how-it-works/out/animation.gif
```
