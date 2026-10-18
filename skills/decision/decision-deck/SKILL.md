---
name: decision-deck
description: Make a short slide deck (a title slide and 4 to 6 slides) from the decision brief, for the person who asked the question and the people who decide with them.
disable-model-invocation: true
---

# Decision deck

The deck tells the same story as the brief, in a form that a group can discuss in 10 minutes. It adds no new result.

## Steps

1. Read `runs/RNN-<slug>/out/brief.md`. If it does not exist, tell the person to run `/decision-brief` first. Stop.
2. Write the slide plan in `runs/RNN-<slug>/code/deck.yaml`. Use the structure in [DECK.md](DECK.md). Use only numbers, figures, and tables that the brief uses. The script needs `python-pptx` and `pyyaml`.
3. Build the deck: `python3 <this skill>/scripts/make_deck.py runs/RNN-<slug>/code/deck.yaml runs/RNN-<slug>/out/deck.pptx`. The script also writes `deck.pdf` if LibreOffice is installed.
4. Check the deck yourself. Convert the PDF to images (`pdftoppm -png -r 50 runs/RNN-<slug>/out/deck.pdf scratch/slide`). Look at each image. Fix text that is cut, overlaps, or is too small, and build again.
5. Check against the brief: the answer, the numbers, and the recommended option are the same on the slides and in the brief.

## Rules

- A title slide and 4 to 6 slides. One message per slide. The slide title is that message as a full sentence ("ESR1 alone misses 1 in 15 ER-negative tumors"), not a topic ("Results").
- 3 to 5 bullets per slide, 15 words or fewer each.
- A bioinformatics figure (PCA, volcano, heatmap) goes in only if the decision needs it. Most decks need one result figure and no method figures.
- The last main slide is the decision: options, the recommended option, and the next steps with an owner.
- Methods and data go on one appendix slide at the end.
- Use the words of the reader, as in the brief.

## Done when

- `out/deck.pptx` exists with a title slide and 4 to 6 slides, and `out/deck.pdf` if LibreOffice exists.
- You looked at each slide image and nothing is cut or overlaps.
- Each number on a slide is in the brief.
