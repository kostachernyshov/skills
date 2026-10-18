# Deck structure

| # | Slide | Content |
|---|---|---|
| 1 | Question and decision | Title: a statement, not a question ("You must decide whether ..."). The question in the reader's words. The decision it serves. Who decides. |
| 2 | Answer | The answer in one sentence as the title. 2 or 3 key numbers as `kpis` (big numbers). If the threshold was assumed, say so. |
| 3 | Evidence | One result figure, or one small table. The title states what the figure shows. |
| 4 | Confidence and limits | What the data can and cannot show. Warnings that can change the decision. |
| 5 | Decision and next steps | Options table (what happens, cost if wrong, can reverse). Recommended option. Next steps with owner. |
| 6 | Appendix: data and methods | Data source, sample counts, method, checks summary, release version. |

Slides 3 and 4 can merge if the result is simple. Use 4 slides minimum.

## deck.yaml format

```yaml
title: "<deck title: the answer as a short statement>"
subtitle: "<client, date, release vN>"
slides:
  - title: "<the message of the slide, a full sentence>"
    bullets:
      - "<15 words or fewer>"
    figure: "runs/R01-x/out/fig-x.png"     # optional, path from the project root
    table:                                  # optional, first row is the header
      - ["Option", "What happens", "Cost if wrong", "Can reverse"]
      - ["A", "...", "...", "yes"]
    highlight_row: 2                        # optional, the table row of the recommended option
    kpis:                                   # optional, 2 or 3 big numbers instead of a figure or table
      - {value: "0.63", label: "<what the number means, 10 words or fewer>"}
    note: "<speaker note, optional>"
```

A slide has one of `kpis`, `figure`, or `table`, with 0 to 3 bullets, or bullets only.

Layout: with 0 to 2 bullets, a figure or a table takes the full width. Prefer this. Make figures for slides at 10 x 5.5 inches with fonts of 16 pt or more. The appendix slide may show counts and the release version that are not in the brief.

Run the script from the project root: figure paths are relative to it.
