# How the skills work: source of the promo video

This file is the source of the video in this folder. Each scene of `animation.yaml` points to one line here (`claim: L<n>`). The example numbers come from the SKCM demo of `/animate` (public TCGA data). Commands to build the video are at the end.

The skills take a bioinformatics project from the question of a client to a decision that the client can trust.
A client asks the bioinformatician two things in one request: describe the immune cells in melanoma, and predict survival.
The person types /grill-me. The agent asks its questions first, each with a red question mark: who acts on the answer, why it can work, and what is enough. Then the person answers, as in a chat.
Grilling marks each decision with the one who made it: (person) or (agent).
If the request mixes two types of task, grilling proposes a split into runs: first run "biological description" without the outcome, then run "predict outcomes".
Before any data, the planner writes the plan: the success threshold, a positive control, a negative control, and a robustness check. The person approves the plan.
Run "biological description": the analysis shows T-cell genes in each tumor sample, primary tumors and metastases. The outcome stays locked.
Each run ends with a report from a fresh agent and a supervisor check. The report of the first run passes.
The result of the first run shapes the plan of run "predict outcomes". The person approves this plan, and the outcome opens.
In run "predict outcomes", the agent runs the analysis and checks each result.
A fresh agent writes the report from the files only. The report shows the survival curves: patients with a high T-cell score lived longer.
The supervisor answers seven yes or no questions from the files. One "no" is a veto.
Example of a veto: the draft said that T cells give longer life. The data show a link, not a cause. The report was fixed to "linked, not proven", and the supervisor gave a pass.
If the person wants, the agent makes a short deck (designer) or a short video like this one (animate). This step is optional.
The results go into a release. Only the person signs the release. After the signature, the release does not change.
A big task can split into more runs, for example five. Each run has its own plan, analysis, report, and supervisor.
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
