# animation.yaml -> Timeline. The agent writes the plan; this module draws it.
# The format is in SCENES.md of the skill. Paths in the plan are relative to the project root.
#
#   from pixel_kit import story
#   plan = story.load("runs/R01-x/code/animation.yaml")
#   problems = story.check(plan)          # rules of the skill (captions, numbers, claims, timing)
#   tl, marks = story.timeline(plan)      # marks: key times for the storyboard
#
# Scene types: title, question, cast, cohort, flow, km, strip, distribution, heatmap, volcano,
# takeaway, limit, summary, custom.

import importlib.util, math, os, re
from PIL import Image, ImageDraw
from .palette import *
from .font import text, text_w, title_text, mini_text, mini_w, TITLE_GLYPHS
from .timing import clamp, seg, ease, lerp
from . import sprites as S, fx, ui, bg, charts, data, voice
from .scene import Timeline, W, H

WORDS_PER_S = 2.5        # English voice-over pace
MIN_SCENE = 2.5          # a caption must stay >= 2 s; the scene is a bit longer
REVEAL_START = 0.4       # s: the chart starts to grow
COLOR_NAMES = {
    "favorable": FAVORABLE[0], "favorable2": FAVORABLE[1], "favorable3": FAVORABLE[2],
    "unfavorable": UNFAVORABLE[0], "unfavorable2": UNFAVORABLE[1], "unfavorable3": UNFAVORABLE[2],
    "neutral": NEUTRAL[0], "neutral2": NEUTRAL[1], "neutral3": NEUTRAL[2],
}
TEXT_FIELDS = ("title", "sub", "caption", "text", "label", "key", "xlabel", "ylabel")
PLACEHOLDER = re.compile(r"\{(\w+)\}")
CHART_TYPES = ("km", "strip", "distribution", "heatmap", "volcano")


# ---------------------------------------------------------------- plan, numbers, voice

def load(path):
    import yaml
    plan = yaml.safe_load(open(path, encoding="utf-8"))
    plan["_path"] = path
    plan.setdefault("scenes", [])
    plan.setdefault("numbers", {})
    plan.setdefault("reader", "no-stats")
    return plan


def numbers(plan):
    """Reads each named number from its file once. Returns {name: formatted text}."""
    if "_numbers" in plan:
        return plan["_numbers"]
    out = {}
    for name, ref in (plan.get("numbers") or {}).items():
        before = len(data.LOG)
        if "count" in ref:
            v = data.count(ref["count"])
        else:
            v = data.value(ref)
        for e in data.LOG[before:]:
            e["name"] = name
        out[name] = data.fmt(v, ref.get("fmt"))
    plan["_numbers"] = out
    return out


def fill(plan, s):
    """Puts the named numbers into a text: "HR {hr}" -> "HR 0.62". Records the use."""
    if s is None:
        return None
    nums = numbers(plan)
    used = PLACEHOLDER.findall(s)
    out = PLACEHOLDER.sub(lambda m: nums[m.group(1)], s)
    if used:
        data.note_text(out, used)
    return out


def voiceover(plan):
    """Scene texts from voiceover.md: '## S01' headings, the text below each heading."""
    path = plan.get("voiceover")
    if not path or not os.path.exists(path):
        return {}
    out, cur = {}, None
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^##\s+(\S+)", line)
        if m:
            cur = m.group(1)
            out[cur] = ""
        elif cur and line.strip() and not line.startswith("<!--"):
            out[cur] += " " + line.strip()
    return {k: v.strip() for k, v in out.items()}


def cues(plan):
    v = plan.get("voice") or {}
    if v.get("transcript") and os.path.exists(v["transcript"]):
        return voice.load(v["transcript"], float(v.get("start", 0.0)), v.get("end"))
    return []


def durations(plan):
    """Start and end of each scene. With a transcript: from the cues of each scene ("cues: [C01, C02]").
    Without: from the words of the voice-over text (2.5 words/s), or "dur" in the scene."""
    scenes = plan["scenes"]
    cs = cues(plan)
    vo = voiceover(plan)
    times = []
    if cs:
        by_id = {c.id: c for c in cs}
        starts = []
        for i, sc in enumerate(scenes):
            ids = sc.get("cues") or []
            starts.append(by_id[ids[0]].start if ids else None)
        starts[0] = 0.0
        for i in range(len(scenes)):
            if starts[i] is None:
                starts[i] = (starts[i - 1] + float(scenes[i - 1].get("dur", MIN_SCENE)))
        last_ids = scenes[-1].get("cues") or []
        end = (by_id[last_ids[-1]].end if last_ids else cs[-1].end) + 0.8
        for i in range(len(scenes)):
            times.append((starts[i], starts[i + 1] if i + 1 < len(scenes) else end))
        if scenes[-1].get("type") == "summary":
            a, b = times[-1]
            times[-1] = (a, max(b, a + float(scenes[-1].get("dur", SUMMARY_HOLD))))
        return times
    t = 0.0
    for sc in scenes:
        words = len(vo.get(sc["id"], "").split())
        d = float(sc.get("dur", max(MIN_SCENE, words / WORDS_PER_S + 0.8)))
        if sc.get("type") == "summary" and "dur" not in sc:
            d = max(d, SUMMARY_HOLD)
        times.append((t, t + d))
        t += d
    return times


def color(name):
    if isinstance(name, (list, tuple)):
        return tuple(name)
    if name not in COLOR_NAMES:
        raise KeyError(f"unknown color {name!r}; use one of {', '.join(COLOR_NAMES)}")
    return COLOR_NAMES[name]


# ---------------------------------------------------------------- checks

def _texts(sc):
    for f in TEXT_FIELDS:
        v = sc.get(f)
        if isinstance(v, str):
            yield f, v
        elif isinstance(v, list):
            for x in v:
                if isinstance(x, str):
                    yield f, x
    for part in ("question", "design"):
        if isinstance(sc.get(part), dict):
            for x in sc[part].get("text") or []:
                yield part, x
    for key in ("groups", "steps", "items"):
        for g in sc.get(key) or sc.get("data", {}).get(key, []) or []:
            if isinstance(g, dict) and isinstance(g.get("label"), str):
                yield "label", g["label"]


def _claim_ok(plan, claim):
    """claim: "L12" (a line of the report), "<file>:12", or "<file.yaml>:key"."""
    report = plan.get("report")
    m = re.match(r"^L(\d+)$", str(claim))
    if m:
        path, line = report, int(m.group(1))
    else:
        path, _, rest = str(claim).rpartition(":")
        if not path:
            return False, f"claim {claim!r}: use L<line> or <file>:<line>"
        if path.endswith((".yaml", ".yml")):
            try:
                data._yaml_value(path, rest)
                return True, ""
            except Exception as e:
                return False, f"claim {claim}: {e}"
        line = int(rest) if rest.isdigit() else -1
    if not path or not os.path.exists(path):
        return False, f"claim {claim}: file {path} not found"
    lines = open(path, encoding="utf-8").read().split("\n")
    if not (1 <= line <= len(lines)) or not lines[line - 1].strip():
        return False, f"claim {claim}: line {line} is empty or out of range"
    return True, ""


def check(plan):
    """Rules of the skill. Returns a list of problems (empty: all pass)."""
    out = []
    if not plan.get("report") or not os.path.exists(plan["report"]):
        out.append(f"report not found: {plan.get('report')}")
    try:
        nums = numbers(plan)
    except Exception as e:
        out.append(f"numbers: {e}")
        nums = {}
    times = durations(plan)
    seen = set()
    for sc, (a, b) in zip(plan["scenes"], times):
        sid = sc.get("id", "?")
        if sid in seen:
            out.append(f"{sid}: id is not unique")
        seen.add(sid)
        if sc.get("type") == "summary" and not sc.get("module"):
            ids = {r.get("id"): r for r in plan["scenes"]}
            ref = ids.get(sc.get("result"))
            if not ref or ref.get("type") not in SUMMARY_CHARTS:
                out.append(f"{sid}: result must be the id of a {', '.join(SUMMARY_CHARTS)} scene")
            for part in ("question", "design"):
                for x in (sc.get(part) or {}).get("text") or []:
                    if len(fill(plan, x) if nums else x) > 15:
                        out.append(f"{sid}: {part} line is longer than 15 characters: {x!r}")
            for x in sc.get("text") or []:
                if len(fill(plan, x) if nums else x) > 28:
                    out.append(f"{sid}: text line is longer than 28 characters: {x!r}")
            if len(sc.get("text") or []) > 2:
                out.append(f"{sid}: text has more than 2 lines")
        if sc.get("type") not in ("title", "question", "cast", "cohort", "flow", "takeaway", "limit", "summary", "custom") + CHART_TYPES:
            out.append(f"{sid}: unknown type {sc.get('type')!r}")
        if sc.get("type") != "title" and not sc.get("claim"):
            out.append(f"{sid}: no claim (a line of the report that the scene shows)")
        if sc.get("claim"):
            ok, msg = _claim_ok(plan, sc["claim"])
            if not ok:
                out.append(f"{sid}: {msg}")
        cap = sc.get("caption")
        if cap and sc.get("type") == "heatmap":
            out.append(f"{sid}: a heatmap has no caption (the group legend is at the bottom)")
        if cap and len(cap.split()) > 3:
            out.append(f"{sid}: caption has {len(cap.split())} words (max 3): {cap!r}")
        if cap and b - a < 2.0:
            out.append(f"{sid}: caption is on screen {b - a:.1f} s (min 2 s)")
        used = set()
        for f, s in _texts(sc):
            if not s.isascii():
                out.append(f"{sid}: {f} is not plain English text: {s!r}")
            names = PLACEHOLDER.findall(s)
            for n in names:
                if n not in nums:
                    out.append(f"{sid}: {f} uses {{{n}}}, but numbers has no {n!r}")
            used |= set(names)
            if data.has_digit(PLACEHOLDER.sub("", s)):
                out.append(f"{sid}: {f} has a typed number: {s!r}. Put the number in 'numbers' and use {{name}}")
        if plan.get("reader") == "no-stats" and len(used) > 1:
            out.append(f"{sid}: {len(used)} numbers in the frame; a reader without statistics gets one key number")
        if sc.get("type") == "title":
            for ch in (sc.get("title") or "").upper():
                if ch not in TITLE_GLYPHS:
                    out.append(f"{sid}: title character {ch!r} is not in the title font")
    if not plan["scenes"] or plan["scenes"][-1].get("type") != "summary":
        out.append("the last scene must be a summary (graphical abstract)")
    if sum(1 for sc in plan["scenes"] if sc.get("type") == "summary") > 1:
        out.append("only one summary scene is allowed")
    # the summary hold is not counted
    story_end = times[-2][1] if len(times) > 1 and plan["scenes"][-1].get("type") == "summary" else (times[-1][1] if times else 0)
    limit = float(plan.get("max_s", 60))
    if story_end > limit:
        out.append(f"length before the summary {story_end:.0f} s: keep it at 20-45 s ({limit:.0f} s at most)")
    return out


# ---------------------------------------------------------------- scene painters

def _frame(sc):
    img = bg.ALL.get(sc.get("bg", "paper"), bg.paper)()
    return img


def _heading(img, s):
    if s:
        text(img, 12, 8, s, NAVY, scale=1)
        ImageDraw.Draw(img).line([12, 26, 12 + text_w(s), 26], fill=C(NAVY))


def _caption(img, plan, sc, t):
    cap = fill(plan, sc.get("caption"))
    if cap and t >= 0.3:
        ui.caption(img, cap, y=238)


def _key(img, plan, sc, t, t0, x=None, y=None):
    """Key number box (for example "HR 0.62"). Appears at t0."""
    keys = sc.get("key")
    if not keys or t < t0:
        return
    keys = [keys] if isinstance(keys, str) else keys
    lines = [fill(plan, k) for k in keys]
    w = max(text_w(s, 2) for s in lines) + 16
    h = 8 + 34 * len(lines)
    x = x if x is not None else W - w - 12
    y = y if y is not None else 34
    d = ImageDraw.Draw(img)
    ui.box(d, x, y, x + w, y + h, fill=PAPER, border=NAVY, inner=LGREY)
    for i, s in enumerate(lines):
        text(img, x + 8, y + 6 + 34 * i, s, NAVY, scale=2)


def _reveal(sc, t, dur, ctx):
    t0 = ctx.get("reveal_at", REVEAL_START)
    span = float(sc.get("reveal", max(1.0, min(2.5, (dur - t0) * 0.55))))
    return ease(seg(t, t0, t0 + span)), t0 + span


def p_title(plan, sc, t, dur, ctx):
    img = bg.paper()
    ui.title_screen(img, t, fill(plan, sc.get("title", "")).upper(), fill(plan, sc.get("sub")),
                    fill(plan, sc.get("credit")))
    return img


def p_question(plan, sc, t, dur, ctx):
    img = _frame(sc)
    spr = sc.get("sprite", "clinician")
    S.idle(img, spr, t, 90, 130, scale=3)
    lines = [fill(plan, s) for s in (sc.get("text") or [])]
    n = int(max(0, t - 0.3) * 40)
    for i, s in enumerate(lines):
        k = clamp(n - sum(len(m) for m in lines[:i]), 0, len(s))
        text(img, 170, 70 + 40 * i, s[:int(k)], INK, scale=2)
    if t > 0.3 + sum(len(s) for s in lines) / 40 and int(t * 3) % 2 == 0:
        text(img, 170 + text_w(lines[-1], 2) + 6 if lines else 170, 70 + 40 * (len(lines) - 1), "?", BROWN, scale=2)
    _caption(img, plan, sc, t)
    return img


def p_cast(plan, sc, t, dur, ctx):
    img = _frame(sc)
    _heading(img, fill(plan, sc.get("title")))
    items = sc.get("items") or []
    n = len(items)
    for i, it in enumerate(items):
        if t < 0.3 + 0.35 * i:
            continue
        x = int(W * (i + 1) / (n + 1))
        anim = it.get("anim", "idle")
        if anim == "idle":
            S.idle(img, it["sprite"], t, x, 118, seed=i, scale=int(it.get("scale", 3)))
        else:
            S.draw(img, it["sprite"], anim, t - 0.3 - 0.35 * i, x, 118, scale=int(it.get("scale", 3)))
        if it.get("label"):
            text(img, x, 170, fill(plan, it["label"]), color(it.get("color", "neutral"))[0], align="c")
    _caption(img, plan, sc, t)
    return img


def _person(d, x, y, col):
    """Pictogram 5x9 for icon grids."""
    line, fillc = C(col[0]), C(col[1])
    d.rectangle([x + 1, y, x + 3, y + 2], fill=line)
    d.rectangle([x, y + 3, x + 4, y + 6], fill=line)
    d.rectangle([x + 1, y + 7, x + 1, y + 8], fill=line)
    d.rectangle([x + 3, y + 7, x + 3, y + 8], fill=line)


def p_cohort(plan, sc, t, dur, ctx):
    """Icon grid: one pictogram = per_icon people, in group colors. groups: [{label, n: name, color}]."""
    img = _frame(sc)
    _heading(img, fill(plan, sc.get("title")))
    nums = numbers(plan)
    groups = sc.get("groups") or []
    counts = [float(nums[g["n"]]) for g in groups]
    total = sum(counts)
    per = int(sc.get("per_icon") or max(1, math.ceil(total / 300)))
    icons = [max(1, round(c / per)) for c in counts]
    d = ImageDraw.Draw(img)
    cols = 30
    k, _ = _reveal(sc, t, dur, ctx)
    shown = int(sum(icons) * k)
    i = 0
    x0, y0 = 40, 44
    for gi, g in enumerate(groups):
        col = color(g.get("color", "neutral"))
        for _ in range(icons[gi]):
            if i >= shown:
                break
            x, y = x0 + (i % cols) * 9, y0 + (i // cols) * 13
            _person(d, x, y, col)
            i += 1
    ly = 52
    for gi, g in enumerate(groups):
        if k >= 1 or shown > sum(icons[:gi]):
            col = color(g.get("color", "neutral"))
            text(img, 330, ly, fill(plan, g["label"]), col[0])
            text(img, 330, ly + 16, f"n={nums[g['n']]}", DGREY)
            ly += 40
    if per > 1 and k >= 1:
        text(img, 330, ly + 6, f"1 ICON = {per}", DGREY)
    _caption(img, plan, sc, t)
    return img


def _arrow(d, x0, y, x1, col):
    d.line([x0, y, x1 - 3, y], fill=C(col), width=2)
    d.polygon([(x1, y), (x1 - 5, y - 4), (x1 - 5, y + 4)], fill=C(col))


def p_flow(plan, sc, t, dur, ctx):
    """Design as a flow: steps [{sprite, anim?, label}] with arrows."""
    img = _frame(sc)
    _heading(img, fill(plan, sc.get("title")))
    steps = sc.get("steps") or []
    n = len(steps)
    d = ImageDraw.Draw(img)
    step_t = max(0.35, min(0.9, (dur - 1.0) / max(1, n)))
    xs = [int(W * (i + 0.5) / n) for i in range(n)]
    for i, st in enumerate(steps):
        ti = 0.3 + step_t * i
        if t < ti:
            continue
        x = xs[i]
        anim = st.get("anim", "idle")
        sc_ = int(st.get("scale", 3 if n <= 4 else 2))
        if anim == "idle":
            S.idle(img, st["sprite"], t, x, 118, seed=i, scale=sc_)
        else:
            S.draw(img, st["sprite"], anim, t - ti, x, 118, scale=sc_)
        lab = fill(plan, st.get("label", ""))
        text(img, x, 170, lab, INK, align="c")
        if st.get("sub"):
            text(img, x, 188, fill(plan, st["sub"]), DGREY, align="c")
        if i + 1 < n and t > ti + step_t * 0.6:
            _arrow(d, x + 28, 118, xs[i + 1] - 28, DGREY)
    _caption(img, plan, sc, t)
    return img


def _groups_from(dsc, value_col):
    out = []
    for g in dsc["groups"]:
        where = dict(dsc.get("where") or {})
        where[dsc["group"]] = g["value"]
        vals = data.column(dsc["file"], value_col, where=where)
        data.shown(f"{g['label']} n={len(vals)}", len(vals), dsc["file"], value_col, where)
        out.append(dict(label=g["label"], values=vals, col=color(g.get("color", "neutral"))))
    return out


def _chart_cache(ctx, key, make):
    c = ctx.setdefault("_cache", {})
    if key not in c:
        c[key] = make()
    return c[key]


BOX = (8, 32, W - 8, 228)


def _km_groups(plan, dsc):
    out = []
    for g in dsc["groups"]:
        where = dict(dsc.get("where") or {})
        where[dsc["group"]] = g["value"]
        tt = data.column(dsc["file"], dsc["time"], where=where, dropna=False)
        ev = data.column(dsc["file"], dsc["event"], where=where, dropna=False)
        pairs = [(a, b) for a, b in zip(tt, ev) if a == a and b == b]
        lab = fill(plan, g["label"])
        data.shown(f"{lab} n={len(pairs)}", len(pairs), dsc["file"], f"{dsc['time']}+{dsc['event']}", where)
        out.append(dict(label=lab, times=[a for a, _ in pairs], events=[int(b) for _, b in pairs],
                        col=color(g.get("color", "neutral"))))
    return out


def p_km(plan, sc, t, dur, ctx):
    img = bg.plain()
    _heading(img, fill(plan, sc.get("title")))
    groups = _chart_cache(ctx, sc["id"], lambda: _km_groups(plan, sc["data"]))
    k, tk = _reveal(sc, t, dur, ctx)
    charts.km(img, BOX, groups, k=k, tmax=sc.get("tmax"), xlabel=sc.get("xlabel", "YEARS"),
              ylabel=sc.get("ylabel", "ALIVE"), time_scale=float(sc.get("time_scale", 1.0)),
              legend_xy=tuple(sc["legend_xy"]) if sc.get("legend_xy") else None)
    # key box: bottom left of the plot is usually empty (curves start at the top)
    _key(img, plan, sc, t, tk + 0.2, x=sc.get("key_x", 44), y=sc.get("key_y", 150))
    _caption(img, plan, sc, t)
    return img


def p_strip(plan, sc, t, dur, ctx):
    img = bg.plain()
    _heading(img, fill(plan, sc.get("title")))
    dsc = sc["data"]
    groups = _chart_cache(ctx, sc["id"], lambda: _groups_from(dsc, dsc["value"]))
    for g in groups:
        g["label"] = fill(plan, g["label"])
    k, tk = _reveal(sc, t, dur, ctx)
    charts.strip(img, (8, 32, W - 150 if sc.get("key") else W - 8, 228), groups, k=k, ylabel=sc.get("ylabel"))
    _key(img, plan, sc, t, tk + 0.2)
    _caption(img, plan, sc, t)
    return img


def p_distribution(plan, sc, t, dur, ctx):
    img = bg.plain()
    _heading(img, fill(plan, sc.get("title")))
    dsc = sc["data"]
    groups = _chart_cache(ctx, sc["id"], lambda: _groups_from(dsc, dsc["value"]))
    k, tk = _reveal(sc, t, dur, ctx)
    charts.distribution(img, (8, 34, W - 8, 228), groups, k=k, bins=int(sc.get("bins", 24)), xlabel=sc.get("xlabel"))
    _key(img, plan, sc, t, tk + 0.2)
    _caption(img, plan, sc, t)
    return img


def _heatmap_data(dsc):
    rows = data.table(dsc["file"])
    feat = dsc.get("feature", list(rows[0].keys())[0])
    sample_groups = {r[dsc["samples"]["id"]]: r[dsc["samples"]["group"]] for r in data.table(dsc["samples"]["file"])}
    gvals = [g["value"] for g in dsc["groups"]]
    cols = [c for c in rows[0].keys() if c != feat and sample_groups.get(c) in gvals]
    cols.sort(key=lambda c: gvals.index(sample_groups[c]))
    keep = dsc.get("features")
    rows = [r for r in rows if not keep or r[feat] in keep]
    if keep:
        rows.sort(key=lambda r: keep.index(r[feat]))
    m = []
    for r in rows:
        v = [float(r[c]) if r[c] not in ("", "NA") else float("nan") for c in cols]
        if dsc.get("center", "row-z") == "row-z":
            good = [x for x in v if x == x]
            mu = sum(good) / len(good)
            sd = (sum((x - mu) ** 2 for x in good) / max(1, len(good) - 1)) ** 0.5 or 1
            v = [(x - mu) / sd for x in v]
        m.append(v)
    data.LOG.append(dict(value=f"matrix {len(m)}x{len(cols)}", file=dsc["file"], column="(matrix)", row="", text=""))
    for g in dsc["groups"]:
        n = sum(1 for c in cols if sample_groups[c] == g["value"])
        data.shown(f"{g['label']} n={n}", n, dsc["samples"]["file"], dsc["samples"]["group"], {dsc["samples"]["group"]: g["value"]})
    return m, [r[feat] for r in rows], [gvals.index(sample_groups[c]) for c in cols]


def p_heatmap(plan, sc, t, dur, ctx):
    img = bg.plain()
    _heading(img, fill(plan, sc.get("title")))
    dsc = sc["data"]
    m, labels, cg = _chart_cache(ctx, sc["id"], lambda: _heatmap_data(dsc))
    gcols = [color(g.get("color", "neutral")) for g in dsc["groups"]]
    k, tk = _reveal(sc, t, dur, ctx)
    scale = {"expression": EXPRESSION, "diverging": DIVERGING}[sc.get("scale", "expression")]
    x0, y0, x1, y1 = charts.heatmap(img, (8, 36, W - 8, 228), m, labels, cg, gcols, lim=float(sc.get("lim", 2.0)),
                                    k=k, scale=scale)
    if k >= 1:
        lx = 12
        for gi, g in enumerate(dsc["groups"]):
            lab = f"{fill(plan, g['label'])} n={cg.count(gi)}"
            charts._swatch(ImageDraw.Draw(img), lx, 236, gcols[gi])
            text(img, lx + 12, 232, lab, gcols[gi][0])
            lx += text_w(lab) + 28
    return img


def p_volcano(plan, sc, t, dur, ctx):
    img = bg.plain()
    _heading(img, fill(plan, sc.get("title")))
    dsc = sc["data"]

    def make():
        fc = data.column(dsc["file"], dsc["fc"], dropna=False)
        if "logp" in dsc:
            lp = data.column(dsc["file"], dsc["logp"], dropna=False)
        else:
            p = data.column(dsc["file"], dsc["p"], dropna=False)
            lp = [-math.log10(max(x, 1e-300)) if x == x else float("nan") for x in p]
        labels = data.strings(dsc["file"], dsc["label"]) if dsc.get("label") else None
        keep = [i for i in range(len(fc)) if fc[i] == fc[i] and lp[i] == lp[i]]
        return [fc[i] for i in keep], [lp[i] for i in keep], ([labels[i] for i in keep] if labels else None)
    fc, lp, labels = _chart_cache(ctx, sc["id"], make)
    direction = sc.get("direction", "none")
    if direction == "up_favorable":
        cols = (UNFAVORABLE[0], FAVORABLE[0])
    elif direction == "down_favorable":
        cols = (FAVORABLE[0], UNFAVORABLE[0])
    else:
        cols = (NEUTRAL[0], NEUTRAL[1])
    k, tk = _reveal(sc, t, dur, ctx)
    charts.volcano(img, BOX, fc, lp, labels, fc_thr=float(sc.get("fc_thr", 1.0)),
                   p_thr=-math.log10(float(sc.get("p_thr", 0.01))), k=k, colors=cols, top_n=int(sc.get("top_n", 5)),
                   xlabel=sc.get("xlabel", "LOG2 FC"), ylabel=sc.get("ylabel", "-LOG10 P"))
    _key(img, plan, sc, t, tk + 0.2, x=sc.get("key_x", 16), y=sc.get("key_y", 34))
    _caption(img, plan, sc, t)
    return img


def p_takeaway(plan, sc, t, dur, ctx):
    img = _frame(sc)
    spr = sc.get("sprite", "check_card")
    S.idle(img, spr, t, 80, 120, scale=4)
    lines = [fill(plan, s) for s in (sc.get("text") or [])]
    for i, s in enumerate(lines):
        if t > 0.3 + 0.5 * i:
            text(img, 150, 70 + 40 * i, s, NAVY, scale=2)
    _key(img, plan, sc, t, 0.3 + 0.5 * len(lines), x=150, y=74 + 40 * len(lines))
    _caption(img, plan, sc, t)
    return img


def p_limit(plan, sc, t, dur, ctx):
    img = _frame(sc)
    lines = [fill(plan, s) for s in (sc.get("text") or [])]
    ui.hypothesis(img, t - 0.2, 60, fill(plan, sc.get("title", "LIMIT")), lines, x0=40, x1=W - 41)
    _caption(img, plan, sc, t)
    return img


SUMMARY_HOLD = 10.0      # s: the last frame stays so that the reader can read it
SUMMARY_CHARTS = ("km", "strip", "distribution")


def _mini_chart(img, plan, ref, box, ctx):
    """The chart of an earlier scene, small and fully drawn. Returns the km groups (the caller draws
    their legend under the plot), or None (strip and distribution label their groups)."""
    dsc = ref["data"]
    if ref["type"] == "km":
        groups = _chart_cache(ctx, "km", lambda: _km_groups(plan, dsc))
        charts.km(img, box, groups, tmax=ref.get("tmax"), xlabel=ref.get("xlabel", "YEARS"), ylabel="",
                  time_scale=float(ref.get("time_scale", 1.0)), show_legend=False)
        return groups
    groups = _chart_cache(ctx, "groups", lambda: _groups_from(dsc, dsc["value"]))
    for g in groups:
        g["label"] = fill(plan, g["label"])
    if ref["type"] == "strip":
        charts.strip(img, box, groups, ylabel=None)
    else:
        charts.distribution(img, box, groups, bins=int(ref.get("bins", 24)))
    return None


def p_summary(plan, sc, t, dur, ctx):
    """Graphical abstract at the end: question, design, result, and the takeaway. It appears in about
    1.5 s and then holds still (SUMMARY_HOLD s), so that the reader can read it.
    With "module", a custom function draws the summary (for example a map of a process)."""
    if sc.get("module"):
        return p_custom(plan, sc, t, dur, ctx)
    img = bg.plain()
    _heading(img, fill(plan, sc.get("title") or plan.get("title")))
    d = ImageDraw.Draw(img)
    y0, ph = 38, 140
    panels = (("question", "QUESTION", 8, 120), ("design", "DESIGN", 136, 120), ("result", "RESULT", 264, 208))
    for i, (part, label, x0, pw) in enumerate(panels):
        if t < 0.2 + 0.3 * i:
            continue
        ui.panel_frame(img, x0, y0, pw, ph, label, NAVY)
        if part == "result":
            ref = next(r for r in plan["scenes"] if r["id"] == sc["result"])
            km_groups = _mini_chart(img, plan, ref, (x0 + 2, y0 + 20, x0 + pw - 4, y0 + ph - (18 if ref["type"] == "km" else 2)), ctx)
            lx, ly = x0 + 6, y0 + ph - 18
            for g in km_groups or []:
                charts._swatch(d, lx, ly + 4, g["col"])
                text(img, lx + 12, ly, g["label"], g["col"][0])
                n = f"n={len(g['times'])}"
                mini_text(img, lx + 14 + text_w(g["label"]), ly + 7, n, g["col"][0])
                lx += 26 + text_w(g["label"]) + mini_w(n)
            if sc.get("key"):
                k = fill(plan, sc["key"])
                kw = text_w(k) + 8
                ui.box(d, x0 + pw - kw - 6, y0 + 22, x0 + pw - 6, y0 + 40, fill=PAPER, border=NAVY, inner=LGREY)
                text(img, x0 + pw - kw - 2, y0 + 23, k, NAVY)
            continue
        p = sc.get(part) or {}
        if p.get("sprite"):
            S.idle(img, p["sprite"], 0.0, x0 + pw // 2, y0 + 70, scale=2)
        for j, s in enumerate(p.get("text") or []):
            text(img, x0 + pw // 2, y0 + ph - 38 + 17 * j, fill(plan, s), INK, align="c")
    if t >= 1.2:
        for j, s in enumerate(sc.get("text") or []):
            text(img, W // 2, 190 + 34 * j, fill(plan, s), NAVY if j == 0 else INK, scale=2, align="c")
    return img


def p_custom(plan, sc, t, dur, ctx):
    fn = ctx.get("_custom_" + sc["id"])
    if fn is None:
        spec = importlib.util.spec_from_file_location("custom_" + sc["id"], sc["module"])
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        fn = getattr(mod, sc.get("function", "draw"))
        ctx["_custom_" + sc["id"]] = fn
    img = _frame(sc)
    fn(img, t, sc, dict(ctx, plan=plan, fill=lambda s: fill(plan, s)))
    _caption(img, plan, sc, t)
    return img


PAINTERS = {k[2:]: v for k, v in globals().items() if k.startswith("p_")}


# ---------------------------------------------------------------- timeline

def timeline(plan):
    """Builds the Timeline. Returns (timeline, marks): marks are (time, label) for the storyboard."""
    numbers(plan)
    times = durations(plan)
    cs = cues(plan)
    scenes, marks = [], []
    for sc, (a, b) in zip(plan["scenes"], times):
        ctx = {}
        if cs and sc.get("at"):
            ctx["reveal_at"] = max(0.0, voice.at(cs, sc["at"]) - a)
        painter = PAINTERS[sc["type"]]
        dur = b - a
        scenes.append((a, b, lambda t, sc=sc, dur=dur, ctx=ctx, painter=painter: painter(plan, sc, t, dur, ctx),
                       sc.get("fade", True)))
        key = a + min(dur - 0.3, max(1.2, dur * 0.75))
        marks.append((key, f"{sc['id']} {sc['type']} {a:.1f}-{b:.1f}s"))
    return Timeline(scenes), marks
