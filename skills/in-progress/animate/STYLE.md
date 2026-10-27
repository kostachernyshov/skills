# Style

Pixel art like an old video game, on a very light background. Frame 480x270, scaled x4 to 1920x1080 with nearest neighbor, 30 frames a second. No transparency, no smoothing.

## Palette

PICO-8: 16 main colors for sprites, and 16 extra ("secret") colors only for charts and scales. Names are in `scripts/pixel_kit/palette.py`.

- Background `PAPER` = #FBFAF7, near white and a little cool, with a faint dotted grid. It is outside the palette and only the background uses it. Text and axes `INK` = black.
- Sprite bodies stay PICO-8 white (#FFF1E8). The outline separates them from `PAPER`.
- Backgrounds can use muted tints outside the palette. Their texture stays near the fill color.

## Meaning of colors

| Meaning | Colors | Use |
|---|---|---|
| Better outcome, response, no side effects | shades of blue (`favorable`) | the group that does better |
| Worse outcome, no response | shades of orange (`unfavorable`) | the group that does worse |
| No direction (subtypes, phenotypes, sample types) | grey, lavender, brown (`neutral`) | when "better" and "worse" are not known |
| Expression level in a heatmap | purple to yellow (`EXPRESSION`) | levels have no "better" or "worse" |

Blue and orange, not green and red: people with red-green color vision deficiency can tell them apart. The color must not say "good" or "bad" when the data does not.

## Contrast

- A line or a mark on `PAPER` has a contrast of 3:1 or more (WCAG 1.4.11). The first color of each pair in `palette.py` passes this.
- Inside one scene, the group colors differ by Delta E 20 or more for normal vision, deuteranopia, and protanopia. `animate.py colors` checks this and saves each key frame in four views.
- In greyscale, blue and orange can have the same lightness. Then label each group directly (the legend, the label under the group, the label next to the curve). Do not rely on color only.
- Sprites have a 1 px black outline, so white bodies read on `PAPER`.

## Text in the frame

- English only. The voice explains.
- The last frame is the summary (graphical abstract). It holds still for 10 s so that the reader can read it.
- A caption has 2 or 3 words, large, on a dark plate, and stays on screen for 2 s or more. It names the idea; it does not repeat the voice.
- A typed number is not allowed. Numbers come from `numbers` in the plan, and `animation-numbers.tsv` shows their source.
- n for each group shows in each chart.
- Without statistics: one key number in a frame (for example `HR 0.52`). With statistics: axes, HR, CI, p.
- Fonts: Unifont (`font.text`, GPL-2+ with the font exception, see `scripts/fonts/LICENSE_unifont.txt`), the 5x7 title font (`font.title_text`), and the 3x5 mini font for axis ticks (`font.mini_text`).

## Characters (bio cast)

The cast comes from an oncology and immunology series. Use it only when the story is about these cells.

| Group | Look | Sprites |
|---|---|---|
| Immune cells | white body, color rim, firm eyes | `nk`, `killer_t`, `helper_t`, `treg`, `car_t`, `b_cell`, `dendritic`, `macrophage` |
| Tumor cells | dark plum lumpy body, red rim, angry brows | `tumor`, `tumor_mhc_low`, `tumor_no_mhc`, `tumor_pdl1`, `tumor_stress`, `blast` |
| Normal body cells | soft colors, dot eyes, no brows | `epithelial`, `stem`, `mutant`, `clone_a`..`clone_d`, `senescent`, `granulocyte` |
| People | human scale, draw at x2 or x3 | `patient_a`, `patient_b`, `patient_c`, `clinician`, `scientist`, `manager`, `person` (the one who decides: young, black T-shirt, jeans) |
| Agents | robot with a screen face, human scale | `agent` (`idle`, `work`, `alert`), `supervisor` (with a magnifier) |
| Props | lab and data objects | `tube`, `tube_orange`, `plate`, `sequencer`, `datasheet`, `lock`, `deck`, `dish`, `mouse_top`, `mouse_side`, `syringe`, `vial_drug`, `pill`, `dna`, `file_doc`, `computer`, `check_card`, `bulb`, ... |
| Molecules | 5x5 badges | `badge_mhc`, `badge_pd1`, `badge_pdl1`, `badge_ctla4`, `badge_tcr`, `badge_stress` |

`animate.py sheet <out.png>` draws all sprites. Rules for the cast:

- Yellow is only for MHC-I on cells. Red is only for tumor cells.
- A mutant cell is not a tumor cell. It has no tumor features.
- An immune cell kills by apoptosis of the target: "!" (`fx.alert`), a shot (`fx.shot`), a hit (`fx.hit_flash`), then the `death` animation of the target.
- A blocked immune cell is grey (`blocked`) with `fx.zzz`.
- A metaphor must not claim more than the report. For example, a PD-L1 molecule appears after the T cells arrive, not before.

## Redraw

The sprites will be redrawn in a less cartoon style. The source of each sprite is code (`cast.py`, `props.py`, `people.py`, `office.py`, animations in `library.py`). `tools/build_sprites.py <name>` builds one sheet. A sheet that a person edited in Aseprite must not be built again in full: build only the named sprites. Use only palette colors. Check each new sprite with `animate.py sheet` and `animate.py colors`.
