# Custom scenes for the video "How the skills work": one road from the question to the release.
# The camera moves along the road. Each scene names its part ("part") and the camera ("cam": [from, to]).
# Numbers in the cards come from files (the SKCM demo of /animate) through ctx["fill"] and pixel_kit.story.
# World: x grows to the right (about 1500 px), y is the screen y. The frame shows 480 px of it.

import math
from PIL import ImageDraw
from pixel_kit.palette import *
from pixel_kit.font import text, text_w, title_text
from pixel_kit.timing import clamp, seg, ease, lerp
from pixel_kit import sprites as S, ui, charts, story

W, H = 480, 270
MAIN_Y, R1_Y, R2_Y = 150, 92, 176
ROAD, ROAD_ON = LGREY, NAVY
YOU = LAV                               # the person decides here
QRED = RED                              # the question mark of grilling

# key: (x, y, label, icon, person decides)
ST = {
    "grill": (200, MAIN_Y, "GRILL-ME", "?", True),
    "split": (330, MAIN_Y, "SPLIT", "fork", False),
    "plan1": (440, R1_Y, "PLAN", "datasheet", True),
    "ana1": (550, R1_Y, "ANALYSIS", "computer", False),
    "rep1": (660, R1_Y, "REPORT", "file_doc", False),
    "sup1": (770, R1_Y, "SUPERVISOR", "check_card", False),
    "plan2": (900, R2_Y, "PLAN", "datasheet", True),
    "ana2": (1010, R2_Y, "ANALYSIS", "computer", False),
    "rep2": (1120, R2_Y, "REPORT", "file_doc", False),
    "sup2": (1230, R2_Y, "SUPERVISOR", "check_card", False),
    "show": (1340, R2_Y, "SLIDES, VIDEO", "deck", False),
    "rel": (1450, R2_Y, "RELEASE", "folder", True),
}
OPTIONAL = {"show"}
ORDER = list(ST)
RUN1 = ["plan1", "ana1", "rep1", "sup1"]
EDGES = [("grill", "split"), ("split", "plan1"), ("plan1", "ana1"), ("ana1", "rep1"), ("rep1", "sup1"),
         ("split", "plan2"), ("plan2", "ana2"), ("ana2", "rep2"), ("rep2", "sup2"), ("sup2", "show"),
         ("show", "rel")]
LOCK_X = 760                            # the lock on the lane of the second run
RUN_NAMES = (('RUN "BIOLOGICAL DESCRIPTION"', 605, R1_Y + 32, "c"),
             ('RUN "PREDICT OUTCOMES"', 440, R2_Y - 24, "l"))


# ---------------------------------------------------------------- geometry

def _bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        u = i / n
        a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def edge_points(a, b):
    ax, ay = ST[a][:2]
    bx, by = ST[b][:2]
    if ay == by:
        return [(ax, ay), (bx, by)]
    if b == "plan1":
        return _bez((ax, ay), (ax + 50, ay), (bx - 60, by), (bx, by))
    # split -> lane of the second run: a bend, then a long straight lane
    return _bez((ax, ay), (ax + 45, ay), (ax + 45, by), (ax + 100, by)) + [(bx, by)]


def _part(pts, k):
    """The first part (0..1) of a polyline, by length."""
    if k >= 1:
        return pts
    seglen = [math.dist(p, q) for p, q in zip(pts, pts[1:])]
    goal = sum(seglen) * clamp(k)
    out = [pts[0]]
    for (p, q), L in zip(zip(pts, pts[1:]), seglen):
        if goal <= L:
            u = goal / L if L else 0
            out.append((lerp(p[0], q[0], u), lerp(p[1], q[1], u)))
            return out
        out.append(q)
        goal -= L
    return out


def _line(d, pts, ox, col, w):
    pts = [(int(round(x - ox)), int(round(y))) for x, y in pts]
    if len(pts) > 1:
        d.line(pts, fill=C(col), width=w, joint="curve")


def _dashed(d, pts, ox, col, on=3, off=3):
    for i, (p, q) in enumerate(zip(pts, pts[1:])):
        n = max(1, int(math.dist(p, q) / (on + off)))
        for j in range(n):
            u0, u1 = j / n, (j + on / (on + off)) / n
            d.line([(p[0] + (q[0] - p[0]) * u0 - ox, p[1] + (q[1] - p[1]) * u0),
                    (p[0] + (q[0] - p[0]) * u1 - ox, p[1] + (q[1] - p[1]) * u1)], fill=C(col), width=1)


def _dashed_box(d, x0, y0, x1, y1, col):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    for x in range(x0, x1, 4):
        d.line([(x, y0), (min(x + 1, x1), y0)], fill=C(col))
        d.line([(x, y1), (min(x + 1, x1), y1)], fill=C(col))
    for y in range(y0, y1, 4):
        d.line([(x0, y), (x0, min(y + 1, y1))], fill=C(col))
        d.line([(x1, y), (x1, min(y + 1, y1))], fill=C(col))


# ---------------------------------------------------------------- the road

def diamond(d, x, y, col=YOU, r=3):
    d.polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=C(col), outline=C(INK))


def qmark(img, x, y, scale=1):
    """The red question mark of grilling."""
    text(img, x, y, "?", QRED, scale=scale, align="c")


def fork(d, x, y, col):
    d.line([(x - 7, y), (x - 1, y)], fill=C(col), width=2)
    d.line([(x - 1, y), (x + 6, y - 6)], fill=C(col), width=2)
    d.line([(x - 1, y), (x + 6, y + 6)], fill=C(col), width=2)


def tile(img, x, y, key, hot=False, lit=False, pulse=False):
    d = ImageDraw.Draw(img)
    _, _, label, icon, you = ST[key]
    border = NAVY if hot else (DGREY if lit else LGREY)
    d.rectangle([x - 12, y - 12, x + 12, y + 12], fill=C(PAPER))
    if key in OPTIONAL and not hot:
        _dashed_box(d, x - 12, y - 12, x + 12, y + 12, border)
    else:
        ui.box(d, x - 12, y - 12, x + 12, y + 12, fill=PAPER, border=border, inner=None)
    if hot:
        d.rectangle([x - 13, y - 13, x + 13, y + 13], outline=C(NAVY))
    if icon == "?":
        text(img, x, y - 8, "?", QRED if lit or hot else DGREY, align="c")
    elif icon == "fork":
        fork(d, x, y, NAVY if lit or hot else DGREY)
    else:
        S.draw(img, icon, "idle", 0, x, y)
    if you:
        diamond(d, x + 12, y - 12, YOU if (lit or hot) and not pulse else (PAPER if pulse else LGREY), r=4)
    text(img, x, y + 14, label, INK if (lit or hot) else DGREY, align="c")
    if key in OPTIONAL:
        text(img, x, y + 30, "OPTIONAL", DGREY, align="c")


def world(img, cam, lit=(), hot=None, grow=1.0, locked=False, unlock=None, inform=0.0, veto=0.0, pulse=False,
          names=1.0):
    """Draws the road with the camera centered on world x = cam. lit: stations already passed.
    grow: how much of the edge into hot is drawn. unlock: 0..1 for the lock animation.
    names: how much of the run names is typed (0..1)."""
    ox = cam - W // 2
    d = ImageDraw.Draw(img)
    lit = set(lit)
    for a, b in EDGES:
        _line(d, edge_points(a, b), ox, ROAD, 7)
    for a, b in EDGES:
        if a in lit and (b in lit or b == hot):
            k = grow if b == hot else 1.0
            _line(d, _part(edge_points(a, b), k), ox, ROAD_ON, 3)
    if inform > 0:
        sx, sy = ST["sup1"][:2]
        px, py = ST["plan2"][:2]
        pts = _part(_bez((sx + 14, sy + 6), (sx + 70, sy + 40), (px - 60, py - 60), (px - 6, py - 16)), inform)
        _dashed(d, pts, ox, DGREY)
    for key in ORDER:
        x, y = ST[key][:2]
        if -60 < x - ox < W + 60:
            tile(img, x - ox, y, key, hot=(key == hot), lit=(key in lit), pulse=pulse and key == hot)
    if names > 0:
        for s, x, y, al in RUN_NAMES:
            w = text_w(s)
            x0 = x - w // 2 if al == "c" else x       # the left end stays in place while the name types
            if -w < x0 - ox < W:
                text(img, x0 - ox, y, s[:int(len(s) * clamp(names))], NAVY)
    if locked:
        _dashed(d, edge_points("split", "plan2"), ox, DGREY, on=4, off=4)
    if locked or unlock is not None:
        x = LOCK_X - ox
        if -20 < x < W + 20:
            k = 0 if unlock is None else unlock
            S.draw(img, "lock", "open" if k > 0.5 else "idle", 1.0 if k > 0.5 else 0, x, R2_Y, scale=2)
            if k < 0.5:
                text(img, x, R2_Y + 16, "OUTCOME LOCKED", DGREY, align="c")
    if veto > 0:
        cx, cy = ST["sup2"][:2]
        rx = ST["rep2"][0]
        pts = _part(_bez((cx - 4, cy - 14), (cx - 20, cy - 58), (rx + 20, cy - 58), (rx + 4, cy - 15)), veto)
        _line(d, pts, ox, ORANGE, 2)
        if veto >= 1:
            ex, ey = rx + 4 - ox, cy - 15
            d.polygon([(ex - 4, ey - 6), (ex + 4, ey - 6), (ex, ey)], fill=C(ORANGE))
            text(img, (cx + rx) / 2 - ox, cy - 66, "FIX", BROWN, align="c")
    return ox


def actor(img, ox, name, anim, wx, wy, t, flip=False, scale=2):
    x = wx - ox
    if anim == "idle":
        S.idle(img, name, t, x, wy, flip=flip, scale=scale)
    else:
        S.draw(img, name, anim, t, x, wy, flip=flip, scale=scale)


# ---------------------------------------------------------------- cards, chat, stamps

def card(img, x, y, w, title, lines, t, t0=0.3, cps=60, h=None):
    """A card with a dark header. lines: [(text, color)]. The text types letter by letter."""
    if t < t0:
        return
    d = ImageDraw.Draw(img)
    h = h or 22 + 17 * len(lines)
    ui.box(d, x, y, x + w, y + h, fill=PAPER, border=NAVY, inner=LGREY)
    d.rectangle([x, y, x + w, y + 15], fill=C(NAVY))
    text(img, x + w // 2, y, title, WHITE, align="c")
    n = int((t - t0 - 0.2) * cps)
    for i, (s, col) in enumerate(lines):
        k = clamp(n - sum(len(m) for m, _ in lines[:i]), 0, len(s))
        if k > 0:
            text(img, x + 6, y + 19 + 17 * i, s[:int(k)], col)
    return h


def typed_until(lines, t0=0.3, cps=60):
    return t0 + 0.2 + sum(len(s) for s, _ in lines) / cps


def _typed(lines, n):
    """lines typed with n letters in total."""
    out = []
    for s in lines:
        k = int(clamp(n, 0, len(s)))
        out.append(s[:k])
        n -= len(s)
    return out


def chat(img, x, y, w, questions, answers, t, t0=0.3, cps=60, gap=0.4):
    """The grilling as a chat: the questions of the agent type first (red marks),
    then the answers of the person type on the right, as in a messenger."""
    if t < t0:
        return
    d = ImageDraw.Draw(img)
    qh = 6 + 16 * len(questions)
    ah = 6 + 16 * len(answers)
    h = 15 + 4 + qh + 5 + ah + 4
    ui.box(d, x, y, x + w, y + h, fill=PAPER, border=NAVY, inner=None)
    d.rectangle([x, y, x + w, y + 15], fill=C(NAVY))
    text(img, x + w // 2, y, "/GRILL-ME", WHITE, align="c")
    # the agent: on the left
    by = y + 19
    d.rounded_rectangle([x + 4, by, x + w - 4, by + qh], radius=4, fill=C(PAPER), outline=C(NAVY))
    n = (t - t0 - 0.1) * cps
    for i, s in enumerate(_typed(questions, n)):
        if s:
            qmark(img, x + 13, by + 3 + 16 * i)
            text(img, x + 22, by + 3 + 16 * i, s, INK)
    t1 = t0 + 0.1 + sum(len(s) for s in questions) / cps + gap
    if t < t1:
        return t1
    # the person: on the right
    ay = by + qh + 5
    d.rounded_rectangle([x + 30, ay, x + w - 4, ay + ah], radius=4, fill=C(PAPER), outline=C(YOU))
    for i, s in enumerate(_typed(answers, (t - t1) * cps)):
        if s:
            text(img, x + w - 10, ay + 3 + 16 * i, s, NAVY, align="r")
    return t1


def chat_done(questions, answers, t0=0.3, cps=60, gap=0.4):
    return t0 + 0.1 + sum(len(s) for s in questions) / cps + gap + sum(len(s) for s in answers) / cps


def stamp(img, x, y, label, col, t, t0):
    """A stamp: it lands big and settles (0.2 s)."""
    if t < t0:
        return
    k = ease(seg(t, t0, t0 + 0.2))
    sc = 3 if k < 1 else 2
    w = text_w(label, sc) + 12
    d = ImageDraw.Draw(img)
    d.rectangle([x - w // 2, y - 4, x + w // 2, y + 16 * sc + 2], fill=C(PAPER), outline=C(col), width=2)
    text(img, x, y, label, col, scale=sc, align="c")


def checks(img, t, t0, x=10, y=10):
    """Checks before each result: positive control, negative control, robustness."""
    d = ImageDraw.Draw(img)
    for i, lab in enumerate(("+ CONTROL", "- CONTROL", "ROBUST")):
        if t > t0 + 0.4 * i:
            yy = y + 16 * i
            d.rectangle([x, yy + 3, x + 9, yy + 12], fill=C(XBLUE))
            d.line([(x + 2, yy + 8), (x + 4, yy + 10), (x + 8, yy + 5)], fill=C(WHITE), width=1)
            text(img, x + 14, yy, lab, INK)


# ---------------------------------------------------------------- scene parts

DUR = {}                                # scene id -> length in seconds (filled by draw)


def cam_x(sc, t):
    """The camera moves at an even speed for the whole scene: no stop in the middle of the road."""
    a, b = sc["cam"]
    return lerp(a, b, seg(t, 0.0, DUR.get(sc["id"], 5.0)))


def lit_upto(key):
    """Stations passed up to key, along its run."""
    i = ORDER.index(key)
    out = set(ORDER[:i + 1])
    if key in ORDER[ORDER.index("plan2"):]:
        out |= set(RUN1)
    return out


def faint_world(img, cam):
    """The whole road in light grey, behind the title."""
    ox = cam - W // 2
    d = ImageDraw.Draw(img)
    for a, b in EDGES:
        _line(d, edge_points(a, b), ox, LGREY, 5)
    for key in ORDER:
        x, y = ST[key][:2]
        if -20 < x - ox < W + 20:
            ui.box(d, x - ox - 12, y - 12, x - ox + 12, y + 12, fill=PAPER, border=LGREY, inner=None)


def part_title(img, t, sc, ctx):
    faint_world(img, sc.get("cam", [200])[0])
    title_text(img, W // 2, 40, "KOSTA CHERNYSHOV SKILLS", 3, XBLUE, NAVY, back=LGREY)
    text(img, W // 2, 74, "squeeze analysis", DGREY, scale=2, align="c")


def part_ask(img, t, sc, ctx):
    """The client asks you, the bioinformatician. A red question mark over your head."""
    ox = world(img, cam_x(sc, t), names=0)
    actor(img, ox, "manager", "idle", 60, MAIN_Y - 4, t)
    actor(img, ox, "person", "idle", 120, MAIN_Y - 4, t + 0.4)
    lines = [("DESCRIBE THE IMMUNE CELLS", INK), ("IN MELANOMA.", INK), ("DO THEY PREDICT SURVIVAL?", INK)]
    card(img, 226, 10, 234, "THE CLIENT ASKS YOU", lines, t)
    t1 = typed_until(lines) + 0.2
    if t > t1:
        d = ImageDraw.Draw(img)
        x, y = 120 - ox, MAIN_Y - 66
        k = ease(seg(t, t1, t1 + 0.3))
        y = int(lerp(y + 8, y, k))
        d.rounded_rectangle([x - 9, y - 10, x + 9, y + 9], radius=3, fill=C(PAPER), outline=C(INK))
        d.polygon([(x - 3, y + 9), (x + 3, y + 9), (x, y + 13)], fill=C(INK))
        qmark(img, x, y - 9)


def part_grill(img, t, sc, ctx):
    q = ["WHO ACTS ON THE ANSWER?", "WHY CAN IT WORK?", "WHAT IS ENOUGH?"]
    a = ["THE TRIAL TEAM", "T CELLS KILL THE TUMOR", "A CLEAR PICTURE"]
    ox = world(img, cam_x(sc, t), lit={"grill"}, hot="grill", names=0,
               pulse=int(t * 3) % 2 == 0 and t > chat_done(q, a))
    gx = ST["grill"][0]
    actor(img, ox, "person", "idle", gx - 76, MAIN_Y - 46, t)
    actor(img, ox, "agent", "work" if t < 2.0 else "idle", gx - 34, MAIN_Y - 46, t + 0.5, flip=True)
    chat(img, 236, 4, 238, q, a, t)


def part_split(img, t, sc, ctx):
    q = ["TWO TASKS IN ONE.", "SPLIT INTO TWO RUNS?"]
    a = ["YES"]
    t_yes = chat_done(q, a)
    k = ease(seg(t, t_yes, t_yes + 1.4))
    ox = world(img, cam_x(sc, t), lit={"grill", "split"} | ({"plan1"} if k >= 1 else set()), hot="split",
               locked=k >= 1, names=seg(t, t_yes + 0.6, t_yes + 1.6))
    d = ImageDraw.Draw(img)
    if k < 1:
        _line(d, _part(edge_points("split", "plan1"), k), ox, ROAD_ON, 3)
        _dashed(d, _part(edge_points("split", "plan2"), k), ox, DGREY, on=4, off=4)
    chat(img, 6, 4, 210, q, a, t)


def part_plan(img, t, sc, ctx):
    lines = [("DONE: A FIXED GENE PANEL", INK), ("+ KNOWN T-CELL GENES", XBLUE), ("- SHUFFLED LABELS", BROWN),
             ("~ OTHER CUTOFFS", INK), ("ACCEPT THE PLAN? YES", LAV)]
    t_yes = typed_until(lines, 0.8)
    ox = world(img, cam_x(sc, t), lit={"grill", "split", "plan1"}, hot="plan1", locked=True,
               pulse=t > t_yes and int(t * 3) % 2 == 0)
    px = ST["plan1"][0]
    actor(img, ox, "person", "cheer" if t > t_yes else "idle", px - 40, R1_Y - 46, t)
    card(img, 258, 118, 214, "PLAN", lines, t, t0=0.8)


def part_ana1(img, t, sc, ctx):
    ox = world(img, cam_x(sc, t), lit=lit_upto("ana1") - {"ana1"}, hot="ana1", grow=ease(seg(t, 0, 1.0)),
               locked=True)
    actor(img, ox, "agent", "work", ST["ana1"][0] - 36, R1_Y - 46, t)
    checks(img, t, 0.6)
    if t > 1.6:
        d = ImageDraw.Draw(img)
        dsc = sc["data"]
        if "_hm" not in CACHE:
            CACHE["_hm"] = story._heatmap_data(dsc)
        m, labels, cg = CACHE["_hm"]
        gcols = [story.color(g.get("color", "neutral")) for g in dsc["groups"]]
        x0, y0, x1, y1 = 196, 100, 474, 226
        ui.box(d, x0 - 4, y0 - 18, x1 + 4, y1 + 6, fill=PAPER, border=NAVY, inner=LGREY)
        d.rectangle([x0 - 4, y0 - 18, x1 + 4, y0 - 3], fill=C(NAVY))
        text(img, (x0 + x1) // 2, y0 - 18, sc.get("chart_title", "T-CELL GENES BY SAMPLE"), WHITE, align="c")
        charts.heatmap(img, (x0, y0, x1, y1 - 28), m, labels, cg, gcols, lim=2.0, k=ease(seg(t, 1.6, 3.2)),
                       scale=EXPRESSION)
        lx = x0 + 2
        for gi, g in enumerate(dsc["groups"]):
            lab = f"{ctx['fill'](g['label'])} n={cg.count(gi)}"
            charts._swatch(d, lx, y1 - 6, gcols[gi])
            text(img, lx + 10, y1 - 11, lab, gcols[gi][0])
            lx += text_w(lab) + 22


def part_check1(img, t, sc, ctx):
    """The first run: a fresh agent writes the report, the supervisor checks it, and it passes."""
    t_sup = 2.2
    on_sup = t > t_sup
    ox = world(img, cam_x(sc, t), lit=lit_upto("sup1" if on_sup else "rep1") - ({"sup1"} if not on_sup else set()),
               hot="sup1" if on_sup else "rep1", grow=ease(seg(t, t_sup if on_sup else 0, (t_sup if on_sup else 0) + 0.8)),
               locked=True)
    actor(img, ox, "agent", "idle", ST["rep1"][0] - 30, R1_Y - 46, t)
    actor(img, ox, "supervisor", "alert" if t_sup < t < t_sup + 1.0 else "idle", ST["sup1"][0] + 40, R1_Y - 46, t,
          flip=True)
    lines = [("FRESH AGENT. FILES ONLY.", DGREY), ("T-CELL GENES DIFFER", INK), ("BETWEEN THE SAMPLES.", INK)]
    card(img, 10, 128, 220, "REPORT: BIOLOGY", lines, t, t0=0.4)
    stamp(img, 330, 140, "PASS", XBLUE, t, t_sup + 1.0)


def part_plan2(img, t, sc, ctx):
    lines = [("DONE: THE SCORE SPLITS SURVIVAL", INK), ("+ SCORE FROM RUN ONE", XBLUE), ("- SHUFFLED SURVIVAL", BROWN),
             ("~ OTHER CUTOFFS", INK), ("ACCEPT THE PLAN? YES", LAV)]
    t_yes = typed_until(lines, 1.0)
    unlock = seg(t, t_yes + 0.2, t_yes + 0.8)
    ox = world(img, cam_x(sc, t), lit=lit_upto("plan2") - {"plan2"}, hot="plan2", grow=ease(seg(t, 0.4, 1.4)),
               inform=ease(seg(t, 0, 1.0)), unlock=unlock if t < t_yes + 1.6 else None,
               locked=t < t_yes + 0.2, pulse=t > t_yes and int(t * 3) % 2 == 0)
    actor(img, ox, "person", "cheer" if t > t_yes else "idle", ST["plan2"][0] - 40, R2_Y - 46, t)
    card(img, 222, 6, 252, "PLAN", lines, t, t0=1.0)


def part_ana2(img, t, sc, ctx):
    ox = world(img, cam_x(sc, t), lit=lit_upto("ana2") - {"ana2"}, hot="ana2", grow=ease(seg(t, 0, 1.0)))
    actor(img, ox, "agent", "work", ST["ana2"][0] - 36, R2_Y - 46, t)
    checks(img, t, 0.5)


def part_rep2(img, t, sc, ctx):
    """The report of the second run: the survival curves, from the files."""
    ox = world(img, cam_x(sc, t), lit=lit_upto("rep2") - {"rep2"}, hot="rep2", grow=ease(seg(t, 0, 1.0)))
    rx = ST["rep2"][0]
    actor(img, ox, "agent", "idle", rx + 34, R2_Y - 46, t, flip=True)
    for i in range(3):
        u = seg(t, 0.3 + 0.25 * i, 0.9 + 0.25 * i)
        if 0 < u < 1:
            x = lerp(ST["ana2"][0] - ox, rx - ox, ease(u))
            S.draw(img, "file_doc", "idle", 0, x, R2_Y - 20 - 14 * math.sin(u * math.pi), scale=2)
    if t > 0.8:
        dsc = sc["data"]
        if "_km" not in CACHE:
            CACHE["_km"] = story._km_groups(ctx["plan"], dsc)
        groups = CACHE["_km"]
        d = ImageDraw.Draw(img)
        x0, y0, x1, y1 = 12, 22, 236, 140
        ui.box(d, x0 - 4, y0 - 18, x1 + 4, y1 + 4, fill=PAPER, border=NAVY, inner=LGREY)
        d.rectangle([x0 - 4, y0 - 18, x1 + 4, y0 - 3], fill=C(NAVY))
        text(img, (x0 + x1) // 2, y0 - 18, "REPORT: SURVIVAL", WHITE, align="c")
        k = ease(seg(t, 1.0, 2.6))
        charts.km(img, (x0, y0, x1, y1), groups, k=k, tmax=sc.get("tmax", 20), xlabel="YEARS", ylabel="",
                  time_scale=365.25, legend_xy=(x1 - 96, y0 + 6))
        if k >= 1 and sc.get("key"):
            key = ctx["fill"](sc["key"])
            w = text_w(key) + 10
            ui.box(d, x0 + 26, y1 - 46, x0 + 26 + w, y1 - 26, fill=PAPER, border=NAVY, inner=None)
            text(img, x0 + 31, y1 - 45, key, NAVY)
    lines = [("FRESH AGENT. FILES ONLY.", DGREY), ("DRAFT: MORE T CELLS", BROWN), ("GIVE LONGER LIFE.", BROWN)]
    card(img, 250, 8, 222, "REPORT (DRAFT)", lines, t, t0=2.6)


def part_check2(img, t, sc, ctx):
    t_no, t_veto, t_fix, t_pass = 1.0, 1.8, 3.0, 4.2
    ox = world(img, cam_x(sc, t), lit=lit_upto("sup2"), hot="sup2", veto=ease(seg(t, t_veto, t_veto + 0.8)))
    cx = ST["sup2"][0]
    actor(img, ox, "supervisor", "alert" if t_no < t < t_fix else "idle", cx + 44, R2_Y - 46, t, flip=True)
    lines = [("Q1-Q5  YES", XBLUE), ("Q6     NO: CAUSE, NOT LINK", BROWN if t > t_no else PAPER),
             ("Q7     YES", XBLUE if t > t_no else PAPER)]
    card(img, 10, 8, 232, "SUPERVISOR: YES OR NO", lines, t, t0=0.3)
    if t < t_pass:
        stamp(img, 316, 22, "VETO", BROWN, t, t_veto)
    if t > t_fix:
        d = ImageDraw.Draw(img)
        ui.box(d, 252, 66, 472, 100, fill=PAPER, border=NAVY, inner=None)
        text(img, 258, 68, "FIX:", DGREY)
        s = "LINKED, NOT PROVEN."
        text(img, 258, 83, s[:int((t - t_fix) * 60)], NAVY)
    stamp(img, 316, 22, "PASS", XBLUE, t, t_pass)


def part_show(img, t, sc, ctx):
    ox = world(img, cam_x(sc, t), lit=lit_upto("show"), hot="show", grow=ease(seg(t, 0, 1.0)), veto=1.0)
    d = ImageDraw.Draw(img)
    sx = ST["show"][0] - ox
    if t > 0.8:
        S.draw(img, "deck", "idle", 0, sx - 60, 52, scale=3)
        text(img, sx - 60, 76, "SLIDES", INK, align="c")
    if t > 1.3:
        # a small screen that plays this video: the road and a dot that runs along it
        x0, y0 = sx + 4, 24
        ui.box(d, x0, y0, x0 + 96, y0 + 56, fill=PAPER, border=INK, inner=None)
        d.rectangle([x0 + 2, y0 + 2, x0 + 94, y0 + 54], fill=C(PAPER))
        d.line([(x0 + 8, y0 + 34), (x0 + 30, y0 + 34), (x0 + 40, y0 + 22), (x0 + 88, y0 + 22)], fill=C(LGREY), width=3)
        d.line([(x0 + 30, y0 + 34), (x0 + 40, y0 + 44), (x0 + 88, y0 + 44)], fill=C(LGREY), width=3)
        u = ((t - 1.3) / 3.0) % 1.0
        px = lerp(x0 + 8, x0 + 88, u)
        py = y0 + 34 if px < x0 + 30 else y0 + 44
        d.rectangle([px - 2, py - 2, px + 2, py + 2], fill=C(NAVY))
        d.rectangle([x0 + 40, y0 + 58, x0 + 56, y0 + 62], fill=C(DGREY))
        text(img, x0 + 48, 92, "VIDEO", INK, align="c")


def part_release(img, t, sc, ctx):
    lines = [("REPORT, SLIDES, FILES", INK), ("SIGN THE RELEASE?  YES", LAV), ("RELEASES/V1  FROZEN", DGREY)]
    t_yes = typed_until(lines[:2], 0.5)
    ox = world(img, cam_x(sc, t), lit=lit_upto("rel"), hot="rel", grow=ease(seg(t, 0, 1.0)),
               pulse=t > t_yes and int(t * 3) % 2 == 0)
    rx = ST["rel"][0]
    actor(img, ox, "person", "cheer" if t > t_yes else "idle", rx - 40, R2_Y - 46, t)
    # the files fly into the release folder
    for i, icon in enumerate(("file_doc", "deck", "datasheet")):
        u = seg(t, 0.2 + 0.25 * i, 0.8 + 0.25 * i)
        if 0 < u < 1:
            x = lerp(ST["show"][0] - ox, rx - ox, ease(u))
            S.draw(img, icon, "idle", 0, x, R2_Y - 20 - 14 * math.sin(u * math.pi), scale=1)
    card(img, 228, 10, 244, "THE RELEASE", lines, t, t0=0.5)
    if t > t_yes + 0.6:
        S.draw(img, "lock", "idle", 0, rx - ox + 30, R2_Y - 40, scale=2)


def _mini_tile(img, x, y, icon=None, you=False, col=DGREY):
    d = ImageDraw.Draw(img)
    ui.box(d, x - 8, y - 8, x + 8, y + 8, fill=PAPER, border=col, inner=None)
    if you:
        diamond(d, x + 8, y - 8, YOU)


def part_runs(img, t, sc, ctx):
    d = ImageDraw.Draw(img)
    text(img, 10, 4, "EACH RUN: PLAN, ANALYSIS, REPORT, SUPERVISOR", DGREY)
    gx, gy = 40, 132
    d.line([(4, gy), (gx + 30, gy)], fill=C(ROAD_ON), width=4)
    _mini_tile(img, gx, gy, you=True, col=NAVY)
    text(img, gx, gy - 8, "?", QRED, align="c")
    text(img, gx, gy + 12, "GRILL-ME", INK, align="c")
    names = sc.get("runs") or []
    for i, name in enumerate(names):
        ti = 0.4 + 0.45 * i
        if t < ti:
            continue
        k = ease(seg(t, ti, ti + 0.6))
        y = 42 + 40 * i
        x0 = 110 + 18 * i
        pts = _bez((gx + 30, gy), (gx + 60, gy), (x0 - 40, y), (x0, y)) + [(x0 + 168, y)]
        _line(d, _part(pts, k), 0, ROAD_ON, 2)
        if k >= 1:
            for j, (xx, icon) in enumerate(zip((x0 + 20, x0 + 62, x0 + 104, x0 + 146),
                                                ("datasheet", "computer", "file_doc", "check_card"))):
                _mini_tile(img, xx, y, you=(j == 0), col=NAVY)
                S.draw(img, icon, "idle", 0, xx, y)
            text(img, x0 + 172, y - 8, name, NAVY)
            if i + 1 < len(names) and t > ti + 0.7:
                _dashed(d, _bez((x0 + 146, y + 9), (x0 + 156, y + 24), (x0 + 30, y + 20), (x0 + 38, y + 31)), 0, DGREY)


def part_parallel(img, t, sc, ctx):
    d = ImageDraw.Draw(img)
    ys = (54, 122, 190)
    names = sc.get("tasks") or []
    S.idle(img, "person", t, 26, 128, scale=2)
    done = t > float(sc.get("accept_at", 4.0))
    for i, y in enumerate(ys):
        d.line([(66, y), (470, y)], fill=C(ROAD), width=7)
        d.line([(66, y), (470, y)], fill=C(ROAD_ON), width=2)
        if i < len(names):
            text(img, 66, y - 30, names[i], NAVY)
        for x in (82, 112, 142):
            _mini_tile(img, x, y, you=True, col=NAVY)
        for x in (408, 438):
            _mini_tile(img, x, y, you=done, col=NAVY if done else LGREY)
        # the agent drives along the middle of each road on its own
        u = ((t * 0.18 + i * 0.33) % 1.0)
        S.draw(img, "agent", "work", t, lerp(180, 370, u), y - 4)
        _dashed(d, [(42, 120), (74, y - 6)], 0, YOU)
    if done:
        text(img, 423, 14, "ACCEPT", LAV, align="c")


def _map(p):
    """World point -> point on the small map of the summary."""
    return 24 + (p[0] - ST["grill"][0]) * 0.345, 116 + (p[1] - MAIN_Y) * 0.9


def part_summary(img, t, sc, ctx):
    """The whole road at once, then one clear step for the viewer."""
    d = ImageDraw.Draw(img)
    text(img, W // 2, 4, "FROM A QUESTION TO A DECISION", NAVY, align="c")
    for a, b in EDGES:
        pts = [_map(q) for q in edge_points(a, b)]
        _line(d, pts, 0, ROAD, 6)
        _line(d, pts, 0, ROAD_ON, 2)
    sx, sy = ST["sup1"][:2]
    px, py = ST["plan2"][:2]
    _dashed(d, [_map(q) for q in _bez((sx + 14, sy + 6), (sx + 70, sy + 40), (px - 60, py - 60), (px - 6, py - 16))],
            0, DGREY)
    cx, cy = _map(ST["sup2"][:2])
    qx = _map(ST["rep2"][:2])[0]
    _line(d, _bez((cx - 3, cy - 11), (cx - 10, cy - 40), (qx + 10, cy - 40), (qx + 3, cy - 12)), 0, ORANGE, 2)
    d.polygon([(qx - 1, cy - 17), (qx + 7, cy - 17), (qx + 3, cy - 12)], fill=C(ORANGE))
    text(img, (cx + qx) / 2, cy - 54, "VETO", BROWN, align="c")
    for key in ORDER:
        x, y = (int(v) for v in _map(ST[key][:2]))
        _, _, _, icon, you = ST[key]
        if key in OPTIONAL:
            d.rectangle([x - 11, y - 11, x + 11, y + 11], fill=C(PAPER))
            _dashed_box(d, x - 11, y - 11, x + 11, y + 11, NAVY)
        else:
            ui.box(d, x - 11, y - 11, x + 11, y + 11, fill=PAPER, border=NAVY, inner=None)
        if icon == "?":
            qmark(img, x, y - 8)
        elif icon == "fork":
            fork(d, x, y, NAVY)
        else:
            S.draw(img, icon, "idle", 0, x, y)
        if you:
            diamond(d, x + 11, y - 11, YOU, r=4)
    x, y = _map((605, R1_Y))
    text(img, x, y - 34, RUN_NAMES[0][0], NAVY, align="c")
    x, y = _map((1120, R2_Y))
    text(img, x, y + 14, RUN_NAMES[1][0], NAVY, align="c")
    ui.caption(img, "TYPE /ASK-KOSTA", y=180)
    text(img, W // 2, 218, "GITHUB.COM/KOSTACHERNYSHOV/SKILLS", DGREY, align="c")
    diamond(d, W // 2 - 52, 252, YOU, r=4)
    text(img, W // 2 - 42, 244, "= YOU DECIDE", DGREY)


PARTS = {k[5:]: v for k, v in globals().items() if k.startswith("part_")}
CACHE = {}                              # data for the charts, read once


def draw(img, t, sc, ctx):
    if not DUR:
        for s, (a, b) in zip(ctx["plan"]["scenes"], story.durations(ctx["plan"])):
            DUR[s["id"]] = b - a
    PARTS[sc["part"]](img, t, sc, ctx)
