---
name: reviewer
description: Review a slide deck or a one-page report with the eyes of the reader, in two rounds, and fix it. Use after you build or change a deck or a report, before it goes to a release.
---

# Reviewer

The deck is the main product of the analysis. The reader sees the deck, not the code. A correct result that the reader does not understand has no value.

The reviewer asks "can the reader understand this?". The skill "supervisor" asks "can the reader trust this?". Do not change a number or a claim here. If a number or a claim is wrong, tell the agent that called you: the supervisor must run again.

## Process: two rounds

Do the steps below two times. Round 2 starts from the deck that round 1 fixed.

1. **Render.** Convert the deck to images: `pdftoppm -png -r 100 runs/RNN-<slug>/out/deck.pdf scratch/review-R<round>`. Look at each image. Do not supervisor from the YAML or the code.
2. **Cold read.** If you can start a subagent, give it only the slide images and one line about the reader (from `run.yaml` `decision`). Ask it: "What is the main message? What decision does the deck ask for? Which slide was hard to read, and why?" If you cannot start a subagent, do the titles test: write the slide titles in order, without the slides. They must tell the full story: question, answer, evidence, limit, decision. Then look at each image for 5 seconds and write the one thing a reader remembers. Write these lines before you score. Mark the cold read `self` in the record.
3. **Score each slide** with the criteria in [CRITERIA.md](CRITERIA.md). Each criterion: 2 (good), 1 (weak), 0 (fails).
4. **Compare** the cold-read answer with the answer in the report. If the main message differs, the deck fails. Fix slide 2 and the deck title first.
5. **Fix** each criterion with a score of 0 or 1. Change the words, cut content, split a slide, or redraw a figure (larger fonts, fewer series, direct labels instead of a legend). Do not add new results.
6. **Rebuild** the deck with the script of the skill "designer".
7. **Record** the round in `runs/RNN-<slug>/out/review-deck.csv` (or `review-report.csv` for the report): round, slide, criterion, score, issue, fix. For a new release, replace the file. The tag of the last release keeps the old review.

8. **Verify.** After the round 2 fixes, render again and look at each changed slide. Fix any new problem before you finish.

Apply the same two rounds to `report.md` when it changes, with the report criteria in [CRITERIA.md](CRITERIA.md). Review the rendered `report.pdf`, not the Markdown. After the report changes, check the deck against it again.

## Done when

- `review-deck.csv` (and `review-report.csv` for a report) has 2 rounds.
- In round 2, no criterion has a score of 0, and the cold-read main message matches the report.
- The final render was checked after the last fix.
