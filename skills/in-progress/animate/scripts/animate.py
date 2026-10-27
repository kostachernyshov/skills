#!/usr/bin/env python3
# Pixel animation from a plan. Run from the project root (paths in the plan are relative to it).
#
#   uv run --with pillow --with numpy --with pyyaml python3 animate.py <command> ...
#
#   check     PLAN                       rules: captions, numbers from files, claims, timing
#   cues      PLAN                       voice cues with times (needs voice.transcript in the plan)
#   board     PLAN OUT.png               storyboard: one key frame per scene, with scene id and time
#   colors    PLAN OUTDIR                color check: table + each key frame in 4 views
#   frames    PLAN OUTDIR [t ...]        single frames (x4 PNG); default: the key frames
#   animatic  PLAN OUT.mp4               key frames held under the voice (fast)
#   render    PLAN OUT.mp4 [OUT.gif]     full video (1920x1080), and a GIF loop if asked
#   preview   PLAN VIDEO.mp4 OUT.mp4     video + voice, to check sync
#   sheet     OUT.png                    cast sheet: all sprites of the library on PAPER
#
# Each command that draws also writes <OUT dir>/animation-numbers.tsv: each number on screen,
# with its file, column, and row.

import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pixel_kit import story, data, voice, colorcheck as CC
from pixel_kit.palette import NAMES


def _plan(path):
    return story.load(path)


def _log(out_path):
    d = os.path.dirname(os.path.abspath(out_path)) if not os.path.isdir(out_path) else out_path
    p = data.write_log(os.path.join(d, "animation-numbers.tsv"))
    print("numbers ->", p)


def _stop_on_problems(plan):
    problems = story.check(plan)
    if problems:
        print("CHECK FAILED:")
        for p in problems:
            print(" -", p)
        sys.exit(1)


def cmd_check(a):
    plan = _plan(a[0])
    problems = story.check(plan)
    times = story.durations(plan)
    for sc, (s, e) in zip(plan["scenes"], times):
        print(f"{sc['id']:5} {sc['type']:12} {s:6.1f}-{e:6.1f} s  {sc.get('caption', '')}")
    print(f"total {times[-1][1]:.1f} s" if times else "no scenes")
    if problems:
        print("CHECK FAILED:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("CHECK PASSED")


def cmd_cues(a):
    plan = _plan(a[0])
    cs = story.cues(plan)
    if not cs:
        print("no transcript: set voice.transcript in the plan")
        sys.exit(1)
    voice.table(cs)


def cmd_board(a):
    plan = _plan(a[0])
    _stop_on_problems(plan)
    tl, marks = story.timeline(plan)
    tl.storyboard(a[1], [t for t, _ in marks], labels=[m for _, m in marks])
    print("board ->", a[1])
    _log(a[1])


def _used_colors(plan):
    out = []
    for sc in plan["scenes"]:
        names = [g.get("color", "neutral") for g in (sc.get("groups") or sc.get("data", {}).get("groups") or [])]
        if sc["type"] == "volcano":
            d = sc.get("direction", "none")
            names = ["favorable", "unfavorable"] if d != "none" else ["neutral", "neutral2"]
        if len(set(names)) > 1:
            out.append((sc["id"], sorted(set(names))))
    return out


def cmd_colors(a):
    import numpy as np
    plan = _plan(a[0])
    outdir = a[1]
    os.makedirs(outdir, exist_ok=True)
    ok_all = True
    lines = []
    for sid, names in _used_colors(plan):
        rows, ok = CC.check([(n, story.color(n)[0]) for n in names])
        ok_all &= ok
        lines.append(f"# scene {sid}")
        lines.append(CC.report(rows, ok))
    tl, marks = story.timeline(plan)
    for t, lab in marks:
        sid = lab.split()[0]
        CC.panel(tl.frame(t), os.path.join(outdir, f"colors-{sid}.png"))
    txt = "\n".join(lines) + f"\nOVERALL\t{'PASS' if ok_all else 'FAIL'}\n"
    open(os.path.join(outdir, "colors.tsv"), "w").write(txt)
    print(txt)
    print("4-view frames ->", outdir)
    if not ok_all:
        sys.exit(1)


def cmd_frames(a):
    plan = _plan(a[0])
    tl, marks = story.timeline(plan)
    times = [float(x) for x in a[2:]] or [t for t, _ in marks]
    for p in tl.export_frames(a[1], times):
        print(p)
    _log(a[1])


def cmd_animatic(a):
    plan = _plan(a[0])
    _stop_on_problems(plan)
    tl, marks = story.timeline(plan)
    audio = (plan.get("voice") or {}).get("audio")
    voice.animatic(tl, [0.0] + [t for t, _ in marks], audio if audio and os.path.exists(audio) else None, a[1])
    print("animatic ->", a[1])
    _log(a[1])


def cmd_render(a):
    plan = _plan(a[0])
    _stop_on_problems(plan)
    tl, _ = story.timeline(plan)
    tl.render(a[1])
    print("video ->", a[1])
    if len(a) > 2:
        tl.gif(a[2])
        print("gif ->", a[2])
    _log(a[1])


def cmd_preview(a):
    plan = _plan(a[0])
    audio = (plan.get("voice") or {}).get("audio")
    if not audio:
        print("no voice.audio in the plan")
        sys.exit(1)
    print(voice.mux(a[1], audio, a[2]))


def cmd_sheet(a):
    import runpy
    sys.argv = ["make_sheet.py", a[0]]
    runpy.run_path(os.path.join(HERE, "tools", "make_sheet.py"), run_name="__main__")


COMMANDS = {k[4:]: v for k, v in globals().items() if k.startswith("cmd_")}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(open(__file__).read().split("\n\n")[0])
        sys.exit(2)
    COMMANDS[sys.argv[1]](sys.argv[2:])
