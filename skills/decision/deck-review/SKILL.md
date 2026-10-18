---
name: deck-review
description: Review a slide deck or a one-page brief with the eyes of the reader, in two rounds, and fix it. Use after you build or change a deck or a brief, before it goes to a release.
---

# Deck review

The deck is the main product of the analysis. The reader sees the deck, not the code. A correct result that the reader does not understand has no value.

## Process: two rounds

Do the steps below two times. Round 2 starts from the deck that round 1 fixed.

1. **Render.** Convert the deck to images: `pdftoppm -png -r 60 runs/RNN-<slug>/out/deck.pdf scratch/review-R<round>`. Look at each image. Do not judge from the YAML or the code.
2. **Cold read.** If you can start a subagent, give it only the slide images and one line about the reader (from `run.yaml` `decision`). Ask it: "What is the main message? What decision does the deck ask for? Which slide was hard to read, and why?" If you cannot start a subagent, answer these questions yourself from the images only, before you read your notes.
3. **Score each slide** with the criteria in [CRITERIA.md](CRITERIA.md). Each criterion: 2 (good), 1 (weak), 0 (fails).
4. **Compare** the cold-read answer with the answer in the brief. If the main message differs, the deck fails. Fix slide 2 and the deck title first.
5. **Fix** each criterion with a score of 0 or 1. Change the words, cut content, split a slide, or redraw a figure (larger fonts, fewer series, direct labels instead of a legend). Do not add new results.
6. **Rebuild** the deck with the skill "decision-deck" script.
7. **Record** the round in `runs/RNN-<slug>/out/deck-review.csv`: round, slide, criterion, score, issue, fix.

Apply the same two rounds to `brief.md` when it changes: one page, answer first, no term the reader does not know.

## Done when

- `deck-review.csv` has 2 rounds.
- In round 2, no criterion has a score of 0, and the cold-read main message matches the brief.
