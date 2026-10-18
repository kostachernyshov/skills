# Rubric

Score each item 0 (no), 1 (partly), 2 (yes). Give the evidence (a path or a quote).

## Grilling
- G1. Questions came in rounds with a recommended option each.
- G2. The agent found facts in the data itself and did not ask the person for them.
- G3. The decision and its owner are written in one sentence.

## Project order
- P1. Layout matches: CLAUDE.md, LOG.md, data/, runs/, releases/, scratch/.
- P2. No extra service files (handoff, summary, notes, extra .md, README in runs).
- P3. Each run has run.yaml with a valid status.
- P4. LOG.md has SETUP, DECISION, RELEASE entries; each sample removal is logged.
- P5. CLAUDE.md State lets a new reader say the next step.
- P6. Release folder has brief.md, SOURCE.txt, only used files; tag vN exists.

## Sanity checks
- C1. Input checks recorded with evidence.
- C2. Each scenario trap was found (see scenario list in README).
- C3. Positive control or prior comparison done with numbers.
- C4. Nothing invented (gene names, weights, references).

## Brief
- B1. Six sections, 400 words or fewer.
- B2. Answer in one sentence in the first 3 lines.
- B3. Options with cost of error and reversibility.
- B4. Warnings from checks appear in limits.
- B5. Each number in the brief exists in a run output.

## Correctness
- R1. Main result agrees with published evidence or the difference is explained.
