# animation.yaml format

All paths are relative to the project root. A full example is in `examples/skcm-demo/`.

```yaml
title: "<name of the animation>"
reader: no-stats                     # no-stats: one key number in a frame; stats: more numbers are allowed
report: runs/R01-x/out/report.md     # claims point to lines of this file
voiceover: runs/R01-x/code/voiceover.md
voice:                               # optional: only with a recording
  audio: runs/R01-x/code/voice.wav
  transcript: runs/R01-x/code/voice.srt   # SRT, VTT, Whisper JSON, or "0:12 text" lines

numbers:                             # each number on screen; the text uses {name}
  hr: {file: runs/R01-x/out/cox.tsv, column: HR, where: {term: score_high}, fmt: "{:.2f}"}
  n_high: {count: {file: runs/R01-x/out/scores.tsv, where: {group: high}}}
  auc: {file: runs/R01-x/run.yaml, key: result.auc, fmt: "{:.2f}"}

scenes:
  - id: S01                          # the same id as the heading in voiceover.md
    type: title
    ...
```

## Timing

- Without a voice: a scene lasts (words of its voice-over) / 2.5 + 0.8 s, and at least 2.5 s. `dur: 4` sets it by hand.
- With a voice: `cues: [C03, C04]` puts the start of the scene at the start of its first cue. Get the cue ids from `animate.py cues`. `at: "survival"` starts the chart reveal on that word.
- The whole video before the summary: 20 to 45 s. More than 60 s fails the check.
- The summary holds for 10 s (`dur` sets more), with or without a voice. It is not counted in the limit above.

## Fields of all scenes

| Field | Meaning |
|---|---|
| `id` | Unique id, the same as in `voiceover.md`. |
| `type` | One of the types below. The last scene is a `summary`. |
| `claim` | The report line that the scene shows: `L14`, `<file>:<line>`, or `<file.yaml>:<key>`. Not needed for `title`. |
| `caption` | 2 or 3 English words at the bottom. No caption on a heatmap. |
| `title` | Short heading at the top left (charts, cohort, flow, cast). |
| `bg` | Background: `paper` (default), `plain`, `tissue`, `epithelium`, `bloodstream`, `lymph_node`, `tme`, `dishes`. |

A text field can use `{name}` from `numbers`. A typed number fails the check. Names with digits (`CD8A`, `PRF1`, `MHC-I`) are allowed.

## Colors

Write a color by name: `favorable`, `favorable2`, `favorable3` (blue), `unfavorable`, `unfavorable2`, `unfavorable3` (orange), `neutral`, `neutral2`, `neutral3` (grey, lavender, brown). See STYLE.md.

## Scene types

### title
`title` (letters A-Z, digits, `- ! . ? :`), `sub`, `credit`.

### question
`sprite` (a person: `clinician`, `scientist`, `manager`, `patient_a`), `text` (1 to 3 lines, short), `caption`.

### cast
`items`: up to 5 of `{sprite, anim, label, color, scale}`. Shows the characters of the story in a row. Animations: see `animate.py sheet`.

### cohort
`groups`: `{label, n, color}`, where `n` is a name in `numbers`. Draws one person icon for each `per_icon` people (default: so that the grid has 300 icons or fewer).

### flow
`steps`: up to 5 of `{sprite, label, sub, anim, scale}`, with arrows between them. Use it for the design: sample, assay, table, score, groups.

### distribution
`data: {file, value, group, groups: [{value, label, color}], where}`, `bins` (default 24), `xlabel`. One histogram for each group on one x axis.

### strip
`data: {file, value, group, groups, where}`, `ylabel`, `key`. Dots for each group and a median bar, with n under each group.

### km
`data: {file, time, event, group, groups, where}`, `time_scale` (365.25 for days to years), `tmax`, `xlabel`, `ylabel`, `key` (for example `"HR {hr}"`), `key_x`, `key_y`, `legend_xy`. Kaplan-Meier curves from the raw times and events. The legend shows n.

### heatmap
`data: {file, feature, features, samples: {file, id, group}, groups, center}`. `file` is wide: one row for each feature, one column for each sample. `center: row-z` (default) or `none`. `scale: expression` (default, purple to yellow, no "better" or "worse") or `diverging` (blue to orange, only when low is better). `lim` (default 2). Columns are sorted by group. Row labels show when each row has 9 px or more (12 rows or fewer).

### volcano
`data: {file, fc, p or logp, label}`, `fc_thr` (default 1), `p_thr` (default 0.01), `top_n` labels, `direction`: `none` (default, neutral colors), `up_favorable`, or `down_favorable`.

### limit
`title` (`LIMIT` or `HYPOTHESIS`), `text` (1 to 4 lines). A frame that the eye reads as "careful".

### takeaway
`sprite` (default `check_card`), `text` (1 to 3 lines), `key`. The answer for the decision.

### summary
The last scene. It must be in each plan, and only once. A graphical abstract that holds still for 10 s:
- `question: {sprite, text}`: 1 or 2 lines of 15 characters or fewer.
- `design: {sprite, text}`: 1 or 2 lines of 15 characters or fewer.
- `result`: the id of a `km`, `strip`, or `distribution` scene. Its chart is drawn small, with n for each group.
- `key`: the key number (for example `"HR {hr}"`).
- `text`: the conclusion, 1 or 2 lines of 28 characters or fewer.
- `title`: default is the title of the plan.

### custom
`module` (path to a Python file), `function` (default `draw`). The function gets `(img, t, scene, ctx)`. `ctx["fill"]` puts numbers into text. Use the library: `from pixel_kit import sprites, charts, fx, ui`. A custom scene that is used a second time moves into the library.

## Outputs

| File | Command |
|---|---|
| `out/animation-board.png` | `board` |
| `out/animation-colors/` (`colors.tsv` and 4-view frames) | `colors` |
| `out/animation-animatic.mp4` | `animatic` (with a voice) |
| `out/animation.mp4`, `out/animation.gif` | `render` |
| `out/animation-preview.mp4` | `preview` (with a voice) |
| `out/animation-numbers.tsv` | each command that draws |
