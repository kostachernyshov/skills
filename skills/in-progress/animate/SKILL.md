---
name: animate
description: Make a short pixel-art animation (20 to 45 s and a 10 s summary frame) that explains the design and the result of a run, from the accepted report, with numbers read only from the result files. Experimental.
disable-model-invocation: true
---

# Animate

The animation tells the story of the report to a person who does not read reports: the question, the design, the result, what it means for the decision, and one main limit. It adds no new result. Each number on screen comes from a result file. Each scene points to a line of the report.

The tool is in `scripts/`: the `pixel_kit` library (sprites, charts, light theme) and `animate.py`. Run each command from the project root:

```
uv run --with pillow --with numpy --with pyyaml python3 <this skill>/scripts/animate.py <command> ...
```

The tool also needs `ffmpeg`. If `ffmpeg -version` fails, tell the person to install it (`brew install ffmpeg` on a Mac). Stop.

```
0 gate → 1 read → 2 voice-over [person] → 3 plan → 4 check
       → 5 storyboard and colors [person] → 6 voice (optional) → 7 render → 8 summary
```

## Steps

0. **Gate.** Find `runs/RNN-<slug>/out/report.md`. If it does not exist, tell the person to run `/analyze` first. Stop. If `run.yaml` has no supervisor verdict `pass`, say in one line: "The report has no supervisor pass. The animation can show a wrong result." Continue.
1. **Read.** Read the report, the tables in `out/`, and `run.yaml`. Find the reader (the `Reader` line). A reader without statistics gets one key number in a frame. A reader with statistics can get axes, HR, CI, and p.
2. **Voice-over.** Write `runs/RNN-<slug>/code/voiceover.md`: one `## S01` heading for each scene and the English text below it. Use one idea in each scene. Use 50 to 110 words in total (20 to 45 s at 2.5 words a second). Use the words of the reader, as in the report. Show the text to the person and ask: "Accept the voice-over? yes / changes". Do not continue without "yes".
3. **Plan.** Write `runs/RNN-<slug>/code/animation.yaml` in the format of [SCENES.md](SCENES.md). Use the scene ids of the voice-over. Follow [STYLE.md](STYLE.md) for colors, captions, and characters.
   - Put each number in `numbers`, with its file, column, and row. Write `{name}` in the text. Never type a number into the plan.
   - Give each scene except the title a `claim`: the report line that the scene shows (`L14`).
   - Use the colors of the outcome: blue for the better group, orange for the worse group. If the data has no "better" or "worse", use the neutral colors.
   - End with a `summary` scene: the question, the design, the result chart, the key number, and the conclusion in 1 or 2 lines. It holds for 10 s.
   - Use a scene type from SCENES.md. If no type fits, write a `custom` scene. Tell the person that the scene is a candidate for the library.
4. **Check.** Run `animate.py check <plan>`. Fix the plan until the output is `CHECK PASSED`.
5. **Storyboard and colors.** Run `animate.py board <plan> runs/RNN-<slug>/out/animation-board.png` and `animate.py colors <plan> runs/RNN-<slug>/out/animation-colors`. Look at the board yourself: text does not overlap, labels are not cut, each chart reads in one second. Fix and run again. Then show the board to the person and ask: "Accept the storyboard? yes / changes". Do not render without "yes".
6. **Voice (optional).** Use this step only if the person gives a recording of the voice-over. The person records it in a tool of their choice (for example VoiceStudio) and gives a WAV file and a transcript with times (SRT, VTT, or Whisper JSON). Copy both into `code/`. Add `voice` to the plan. Run `animate.py cues <plan>`, then add `cues: [C01, ...]` to each scene. Use `at: <word>` when a chart must start on a word. Run `animate.py animatic <plan> runs/RNN-<slug>/out/animation-animatic.mp4` and check that each scene starts with its words.
7. **Render.** Run `animate.py render <plan> runs/RNN-<slug>/out/animation.mp4 runs/RNN-<slug>/out/animation.gif`. With a voice, also run `animate.py preview <plan> runs/RNN-<slug>/out/animation.mp4 runs/RNN-<slug>/out/animation-preview.mp4`.
8. **Summary.** Tell the person the paths of the video, the GIF, the board, and `animation-numbers.tsv`. Name the decisions that you made without the person in one line each.

## Rules

- The animation shows only what the report says. A scene without a report line is not allowed.
- A caption has 2 or 3 English words and stays on screen for 2 s or more. The voice explains; the caption names.
- No invented numbers, percents, or meters. Use `ui.pips` and `ui.meter` only for "more" or "less".
- A hypothesis goes in a `limit` frame with the title `HYPOTHESIS`, not in a result scene.
- Cell death is apoptosis (shrink and break up), not an explosion.
- Do not draw new sprites in the plan. A new character goes into `pixel_kit` (`cast.py`, `library.py`, `tools/build_sprites.py <name>`), and the person sees the cast sheet first (`animate.py sheet <out.png>`).
- Do not show a real person, a logo, or a brand.

## Done when

- The person accepted `code/voiceover.md` and `out/animation-board.png`.
- `animate.py check` prints `CHECK PASSED`.
- `out/animation-numbers.tsv` lists each number on screen with its file, column, and row.
- `out/animation-colors/colors.tsv` ends with `OVERALL PASS`: contrast 3:1 or more on the background, and the group colors differ for normal vision, deuteranopia, and protanopia.
- The last scene is a `summary` that holds still for 10 s or more.
- `out/animation.mp4` (1920x1080), `out/animation.gif`, and `out/animation-board.png` exist.
- With a voice: `out/animation-preview.mp4` exists, and each scene starts with its words.
