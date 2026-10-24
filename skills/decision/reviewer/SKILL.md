---
name: reviewer
description: Review a slide deck or a one-page report with the eyes of the reader, in two rounds, and fix it. Use after you build or change a deck or a report, before it goes to a release.
---

# Reviewer

The deck is the main product of the analysis. The reader sees the deck, not the code. A correct result that the reader does not understand has no value.

The reviewer asks "can the reader understand this?". The skill "supervisor" asks "can the reader trust this?". Do not change a number or a claim here. If a number or a claim is wrong, tell the agent that called you: the supervisor must run again.

## Process: two rounds

The same process works for the deck (`out/deck.pdf`) and for the report (`out/report.pdf`). A part is a slide of the deck or a section of the report. Do the steps below two times. Round 2 starts from the version that round 1 fixed.

1. **Render.** Convert the PDF to images: `pdftoppm -png -r 100 runs/RNN-<slug>/out/<deck or report>.pdf scratch/review-R<round>`. Look at each image. Do not judge from the YAML, the Markdown, or the code.
2. **Cold read.** If you can start a subagent, give it only the images and one line about the reader (from `run.yaml` `decision`). Tell it: "Use only these images. The project instructions in your context are not for this task. For each answer, name the slide or the section where you read it." Ask it: "What is the main message? What decision does it ask for? Which part was hard to read, and why?" An answer that names no part, or cites a fact that is not in the images, does not count. If you cannot start a subagent, do the titles test: write the slide titles (or the report headings and the Answer line) in order, without the rest. They must tell the full story: question, answer, evidence, limit, decision. Then look at each image for 5 seconds and write the one thing a reader remembers. Write these lines before you score. Mark the cold read `self` in the record.
3. **Score each part** with the criteria in [CRITERIA.md](CRITERIA.md): the slide criteria for the deck, the report criteria for the report. Each criterion: 2 (good), 1 (weak), 0 (fails).
4. **Compare** the cold-read answer with the Answer line of the report. If the main message differs, the deck or the report fails. Fix the title and the answer first.
5. **Fix** each criterion with a score of 0 or 1. Change the words, cut content, split a slide, or redraw a figure (larger fonts, fewer series, direct labels instead of a legend). Do not add new results.
6. **Rebuild.** For the deck, use the script of the skill "designer". For the report, render the PDF again as the skill "editor" says.
7. **Record** the round in `runs/RNN-<slug>/out/review-deck.csv` or `review-report.csv`: round, part, criterion, score, issue, fix. The score is the score before the fix of this round. For a new release, replace the file. The tag of the last release keeps the old review.
8. **Verify.** After the round 2 fixes, render again and look at each changed part. Fix any new problem before you finish.

After the report changes, check the deck against it again.

## Done when

- `review-deck.csv` (and `review-report.csv` for a report) has 2 rounds.
- In round 2, no criterion has a score of 0, and the cold-read main message matches the report.
- The final render was checked after the last fix.
