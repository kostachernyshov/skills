# Round 5 (skills v0.5.0), 2026-10-18

Goal: test the deck as the main product. Two agents rebuilt the brief and the deck of s4 (MGMT) and s6 (MSI) from round 4 with v0.5.0, then made release v2. No analysis was redone. Projects: `/mnt/project-files/skill-tests/round5/`.

## What the grader saw (slide images v1 vs v2)
- v2 is better in both decks: big numbers on the answer slide, full-width figure with direct labels, the recommended option highlighted, 26 pt bullet slides, missed tumors circled (s6).
- Both v1 briefs broke the skill rules (no Next steps, s4 482 words). Both v2 briefs follow the template. s4 v2 fixed a factual mismatch (11-39 vs 6-11 in 100) between the table and the limits slide.
- Left after v2: table text about 14 pt (the script set the font on the paragraph; LibreOffice ignores it in tables), small text under big numbers and above figures, long big numbers wrap ("32% vs 10%").
- "One page" was not testable: both briefs rendered to 2 pages. Two agents improvised two renderers.

## Failures and fixes in 0.6.0
| # | Failure | Seen in | Fix |
|---|---|---|---|
| 1 | Table font not applied, fixed row height | grader | Font on each run; row height from text length; 20 pt |
| 2 | Big numbers overflow | s4 | Font size from text length (54/44/36 pt) |
| 3 | Small text under big numbers and figures, small subtitle | s4, s6 | 22 pt ink instead of 20 pt grey; subtitle 24 pt; bullet slides 28 pt |
| 4 | One page cannot be checked | s4, s6 | `brief_pdf.sh` (pandoc + LibreOffice, A4, compact reference.docx) prints the page count; limit 300 words; 1 figure at half width; brief.pdf in release |
| 5 | Unclear if source brackets count | s6 | They do not count |
| 6 | Re-release of a shipped run not allowed | s4, s6 | Allowed if the numbers do not change |
| 7 | Old candidate run not marked superseded | s6 | Release asks about other candidate runs |
| 8 | deck-review.csv replace or append | s4, s6 | Replace; the release tag keeps the old one |
| 9 | Slide vs brief figure file, plotting code in a check script | s4, s6 | One figure file for both; plotting in `code/NN-figures.py`; 11 x 5 in |
| 10 | "Space" criterion fails short bullet slides | s4, s6 | Space under 3-4 short bullets is acceptable |
| 11 | Self cold read missed a dropped source bracket | s4 | Brief criterion: each number has its source bracket; write the 5-second lines before scoring |
| 12 | "owner: to be named" twice in Owner column; no date | s4 | Write `to be named by X`; event in When column |
| 13 | rm with a shell variable blocked by safety check | s6 | Literal absolute path |
| 14 | Names rule vs Python file names | s4 | Keep the project style for importable Python files |

Verified by the grader: both v2 decks rebuilt with the 0.6.0 script and inspected as images (tables 20 pt, rows fit text); the s4 v2 brief renders to 1 page with `brief_pdf.sh`, the s6 v2 brief to 2 pages (full-width figure, 335 words), which the new rules would cut.

## Not fixed
- Cold read by a subagent: test agents cannot start one. The self cold read stays weak. A real user session can start subagents.
