---
name: designer
description: Make a short slide deck (a title slide and 4 to 6 slides) from the decision report, for the person who asked the question and the people who decide with them.
disable-model-invocation: true
---

# Designer

The deck tells the same story as the report, in a form that a group can discuss in 10 minutes. It adds no new result.

## Steps

1. Read `runs/RNN-<slug>/out/report.md`. If it does not exist, tell the person to run `/analyze` first. Stop.
2. Write the slide plan in `runs/RNN-<slug>/code/deck.yaml`. In the subtitle, write the next release number with `(planned)`. If the report starts with the warning block, copy its sentence into `warning`. Use the structure in [DECK.md](DECK.md). Use only numbers, figures, and tables that the report uses. The script needs `python-pptx` and `pyyaml`.
3. Build the deck: `python3 <this skill>/scripts/make_deck.py runs/RNN-<slug>/code/deck.yaml runs/RNN-<slug>/out/deck.pptx`. The script also writes `deck.pdf` if LibreOffice is installed.
4. Call the Skill tool with "reviewer". It reviews the deck in two rounds with the eyes of the reader and fixes it.
5. Check against the report: the answer, the numbers, and the recommended option are the same on the slides and in the report.

## Rules

- A title slide and 4 to 6 slides. One message per slide. The slide title is that message as a full sentence ("ESR1 alone misses 1 in 15 ER-negative tumors"), not a topic ("Results").
- 3 to 5 bullets per slide, 15 words or fewer each.
- A bioinformatics figure (PCA, volcano, heatmap) goes in only if the decision needs it. Most decks need one result figure and no method figures.
- The last main slide is the decision: options, the recommended option, and the next steps with an owner.
- Methods and data go on one appendix slide at the end.
- Use the words of the reader, as in the report.

## Done when

- `out/deck.pptx` exists with a title slide and 4 to 6 slides, and `out/deck.pdf` if LibreOffice exists.
- `out/review-deck.csv` has 2 rounds, and round 2 has no score of 0.
- Each number on a slide is in the report.
- If the report starts with the warning block, the title slide shows the same warning in red.
