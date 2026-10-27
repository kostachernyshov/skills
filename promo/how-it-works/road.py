# Custom scenes for the video "How the skills work": one road from the question to the release.
# The camera moves along the road. Each scene names its part ("part") and the camera ("cam": [from, to]).
# Numbers in the cards come from files (the SKCM demo of /animate) through ctx["fill"] and pixel_kit.story.
# World: x grows to the right (about 1400 px), y is the screen y. The frame shows 480 px of it.

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

# key: (x, y, label, icon, person decides)
ST = {
    "ask": (60, MAIN_Y, "ASK", "bulb", False),
    "grill": (190, MAIN_Y, "GRILL", "?", True),
    "split": (320, MAIN_Y, "SPLIT", "fork", False),
    "plan1": (430, R1_Y, "PLAN", "datasheet", True),
    "ana1": (545, R1_Y, "DESCRIBE", "computer", False),
    "rep1": (660, R1_Y, "REPORT", "file_doc", False),
    "plan2": (790, R2_Y, "PLAN", "datasheet", True),
    "ana2": (905, R2_Y, "OUTCOME", "computer", False),
    "rep2": (1020, R2_Y, "REPORT", "file_doc", False),
    "check": (1135, R2_Y, "SUPERVISOR", "check_card", False),
    "sign": (1250, R2_Y, "SIGN", "folder", True),
    "show": (1365, R2_Y, "SHOW", "deck", False),
}
ORDER = list(ST)
EDGES = [("ask", "grill"), ("grill", "split"), ("split", "plan1"), ("plan1", "ana1"), ("ana1", "rep1"),
         ("split", "plan2"), ("plan2", "ana2"), ("ana2", "rep2"), ("rep2", "check"), ("check", "sign"),
         ("sign", "show")]
LOCK_X = 560                            # the lock on the lane of R02


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
    # split -> lane of R02: a bend, then a long straight lane
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


# ---------------------------------------------------------------- the road

def diamond(d, x, y, col=YOU, r=3):
    d.polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=C(col), outline=C(INK))


def tile(img, x, y, key, hot=False, lit=False, pulse=False):
    d = ImageDraw.Draw(img)
    _, _, label, icon, you = ST[key]
    border = NAVY if hot else (DGREY if lit else LGREY)
    ui.box(d, x - 12, y - 12, x + 12, y + 12, fill=PAPER, border=border, inner=None)
    if hot:
        d.rectangle([x - 13, y - 13, x + 13, y + 13], outline=C(NAVY))
    if icon == "?":
        text(img, x, y - 8, "?", NAVY if lit or hot else DGREY, align="c")
    elif icon == "fork":
        col = C(NAVY if lit or hot else DGREY)
        d.line([(x - 7, y), (x - 1, y)], fill=col, width=2)
        d.line([(x - 1, y), (x + 6, y - 6)], fill=col, width=2)
        d.line([(x - 1, y), (x + 6, y + 6)], fill=col, width=2)
    else:
        S.draw(img, icon, "idle", 0, x, y)
    if you:
        diamond(d, x + 12, y - 12, YOU if (lit or hot) and not pulse else (PAPER if pulse else LGREY), r=4)
    text(img, x, y + 14, label, INK if (lit or hot) else DGREY, align="c")


def world(img, cam, lit=(), hot=None, grow=1.0, locked=False, unlock=None, inform=0.0, veto=0.0, pulse=False,
          dim=False):
    """Draws the road with the camera centered on world x = cam. lit: stations already passed.
    grow: how much of the edge into hot is drawn. unlock: 0..1 for the lock animation."""
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
        rx, ry = ST["rep1"][:2]
        px, py = ST["plan2"][:2]
        pts = _part(_bez((rx + 14, ry + 6), (rx + 70, ry + 40), (px - 60, py - 60), (px - 6, py - 16)), inform)
        _dashed(d, pts, ox, DGREY)
    for key in ORDER:
        x, y = ST[key][:2]
        if -40 < x - ox < W + 40:
            tile(img, x - ox, y, key, hot=(key == hot), lit=(key in lit), pulse=pulse and key == hot)
    # lane tags
    for lab, x, y in (("R01", 487, R1_Y - 26), ("R02", 847, R2_Y - 26)):
        if -30 < x - ox < W + 30:
            text(img, x - ox, y, lab, NAVY, align="c")
    if locked:
        _dashed(d, edge_points("split", "plan2"), ox, DGREY, on=4, off=4)
    if locked or unlock is not None:
        x = LOCK_X - ox
        if -20 < x < W + 20:
            k = 0 if unlock is None else unlock
            S.draw(img, "lock", "open" if k > 0.5 else "idle", 1.0 if k > 0.5 else 0, x, R2_Y, scale=2)
            if k < 0.5:
                text(img, x, R2_Y + 16, "SURVIVAL LOCKED", DGREY, align="c")
    if veto > 0:
        cx, cy = ST["check"][:2]
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


# ---------------------------------------------------------------- cards and stamps

def card(img, x, y, w, title, lines, t, t0=0.3, cps=30, h=None):
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


def typed_until(lines, t0=0.3, cps=30):
    return t0 + 0.2 + sum(len(s) for s, _ in lines) / cps


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


# ---------------------------------------------------------------- scene parts

def cam_x(sc, t):
    a, b = sc["cam"]
    return lerp(a, b, ease(seg(t, 0.0, float(sc.get("move", 1.2)))))


def lit_upto(key):
    """Stations passed up to key, along its run."""
    i = ORDER.index(key)
    out = set(ORDER[:i + 1])
    if key in ("plan2", "ana2", "rep2", "check", "sign", "show"):
        out |= {"plan1", "ana1", "rep1"}
    return out


def part_title(img, t, sc, ctx):
    d = ImageDraw.Draw(img)
    _line(d, [(20, 222), (460, 222)], 0, ROAD, 7)
    for i, x in enumerate(range(40, 470, 55)):
        ui.box(d, x - 8, 214, x + 8, 230, fill=PAPER, border=LGREY, inner=None)
    y = int(lerp(-60, 46, ease(seg(t, 0, 0.6))))
    title_text(img, W // 2, y, "KOSTA CHERNYSHOV", 4, XBLUE, NAVY, back=LGREY)
    title_text(img, W // 2, y + 40, "SKILLS", 4, XBLUE, NAVY, back=LGREY)
    if t > 0.7:
        text(img, W // 2, 150, "squeeze analysis", DGREY, scale=2, align="c")


def part_ask(img, t, sc, ctx):
    ox = world(img, cam_x(sc, t), lit={"ask"}, hot="ask")
    actor(img, ox, "manager", "idle", 22, MAIN_Y + 4, t)
    lines = [("DESCRIBE THE IMMUNE CELLS", INK), ("IN MELANOMA.", INK), ("DO THEY PREDICT SURVIVAL?", INK)]
    card(img, 230, 16, 230, "THE CLIENT ASKS", lines, t)
    # the agent wants to jump to a survival curve at once: a ghost curve, crossed out
    t1 = typed_until(lines) + 0.4
    if t > t1:
        ax = ST["grill"][0] - ox
        S.draw(img, "agent", "alert", 0, ax - 92, MAIN_Y - 46, scale=2)
        d = ImageDraw.Draw(img)
        gx, gy = ax - 62, MAIN_Y - 84
        d.rectangle([gx, gy, gx + 44, gy + 30], outline=C(LGREY))
        _dashed(d, [(gx + 2, gy + 3), (gx + 14, gy + 3), (gx + 14, gy + 12), (gx + 28, gy + 12), (gx + 28, gy + 22),
                    (gx + 42, gy + 22)], 0, DGREY)
        if t > t1 + 0.6:
            d.line([(gx - 2, gy - 2), (gx + 46, gy + 32)], fill=C(ORANGE), width=3)
            d.line([(gx + 46, gy - 2), (gx - 2, gy + 32)], fill=C(ORANGE), width=3)


def part_grill(img, t, sc, ctx):
    ox = world(img, cam_x(sc, t), lit={"ask", "grill"}, hot="grill", grow=ease(seg(t, 0, 1.2)),
               pulse=int(t * 3) % 2 == 0 and t > 1.2)
    gx = ST["grill"][0]
    actor(img, ox, "person", "idle", gx - 60, MAIN_Y - 46, t)
    actor(img, ox, "agent", "idle", gx - 22, MAIN_Y - 46, t + 0.5)
    lines = [("Q1 WHO ACTS ON THE ANSWER?", DGREY), ("   TRIAL TEAM     (PERSON)", NAVY),
             ("Q2 WHY CAN IT WORK?", DGREY), ("   T CELLS KILL   (PERSON)", NAVY),
             ("Q3 WHAT IS ENOUGH?", DGREY), ("   A CLEAR PICTURE (AGENT)", DGREY)]
    card(img, 222, 8, 250, "GRILLING", lines, t, t0=0.6, cps=34)


def part_split(img, t, sc, ctx):
    k = ease(seg(t, 0.2, 1.6))
    ox = world(img, cam_x(sc, t), lit={"ask", "grill", "split"} | ({"plan1"} if k >= 1 else set()), hot="split",
               locked=k >= 1)
    d = ImageDraw.Draw(img)
    if k < 1:
        _line(d, _part(edge_points("split", "plan1"), k), ox, ROAD_ON, 3)
        _dashed(d, _part(edge_points("split", "plan2"), k), ox, DGREY, on=4, off=4)
    lines = [("R01  DESCRIBE THE BIOLOGY", NAVY), ("     NO OUTCOME", DGREY), ("R02  WORK WITH THE OUTCOME", NAVY)]
    card(img, 14, 8, 232, "MIXED TASK: TWO RUNS", lines, t, t0=0.8)


def part_plan(img, t, sc, ctx):
    lines = [("DONE: A FIXED GENE PANEL", INK), ("+ KNOWN T-CELL GENES", XBLUE), ("- SHUFFLED LABELS", BROWN),
             ("~ OTHER CUTOFFS", INK), ("ACCEPT THE PLAN? YES", LAV)]
    t_yes = typed_until(lines, 0.8, 34)
    ox = world(img, cam_x(sc, t), lit={"ask", "grill", "split", "plan1"}, hot="plan1", locked=True,
               pulse=t > t_yes and int(t * 3) % 2 == 0)
    px = ST["plan1"][0]
    actor(img, ox, "person", "cheer" if t > t_yes else "idle", px - 40, R1_Y - 46, t)
    card(img, 258, 118, 214, "PLAN R01", lines, t, t0=0.8, cps=34)


def part_r01(img, t, sc, ctx):
    ox = world(img, cam_x(sc, t), lit=lit_upto("rep1") - {"rep1"} | ({"rep1"} if t > 3.5 else set()), hot="ana1",
               locked=True)
    actor(img, ox, "agent", "work", ST["ana1"][0] - 36, R1_Y - 46, t)
    d = ImageDraw.Draw(img)
    # checks before each result
    for i, lab in enumerate(("+ CONTROL", "- CONTROL", "ROBUST")):
        if t > 0.8 + 0.4 * i:
            x, y = 10, 10 + 16 * i
            d.rectangle([x, y + 3, x + 9, y + 12], fill=C(XBLUE))
            d.line([(x + 2, y + 8), (x + 4, y + 10), (x + 8, y + 5)], fill=C(WHITE), width=1)
            text(img, x + 14, y, lab, INK)
    if t > 1.6:
        dsc = sc["data"]
        if "_hm" not in ctx:
            ctx["_hm"] = story._heatmap_data(dsc)
        m, labels, cg = ctx["_hm"]
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


def part_r02(img, t, sc, ctx):
    unlock = seg(t, 2.0, 2.6)
    ox = world(img, cam_x(sc, t), lit=lit_upto("ana2") - {"ana2"} | ({"ana2"} if t > 3 else set()), hot="ana2",
               grow=ease(seg(t, 1.0, 2.0)), inform=ease(seg(t, 0.2, 1.4)), unlock=unlock if t < 3.6 else None)
    actor(img, ox, "agent", "work", ST["ana2"][0] + 40, R2_Y - 46, t, flip=True)
    if t > 2.6:
        dsc = sc["data"]
        if "_km" not in ctx:
            ctx["_km"] = story._km_groups(ctx["plan"], dsc)
        groups = ctx["_km"]
        d = ImageDraw.Draw(img)
        x0, y0, x1, y1 = 12, 22, 236, 140
        ui.box(d, x0 - 4, y0 - 18, x1 + 4, y1 + 4, fill=PAPER, border=NAVY, inner=LGREY)
        d.rectangle([x0 - 4, y0 - 18, x1 + 4, y0 - 3], fill=C(NAVY))
        text(img, (x0 + x1) // 2, y0 - 18, "OVERALL SURVIVAL", WHITE, align="c")
        k = ease(seg(t, 2.8, 4.6))
        charts.km(img, (x0, y0, x1, y1), groups, k=k, tmax=sc.get("tmax", 20), xlabel="YEARS", ylabel="",
                  time_scale=365.25, legend_xy=(x1 - 96, y0 + 6))
        if k >= 1 and sc.get("key"):
            key = ctx["fill"](sc["key"])
            w = text_w(key) + 10
            ui.box(d, x0 + 26, y1 - 46, x0 + 26 + w, y1 - 26, fill=PAPER, border=NAVY, inner=None)
            text(img, x0 + 31, y1 - 45, key, NAVY)


def part_report(img, t, sc, ctx):
    ox = world(img, cam_x(sc, t), lit=lit_upto("rep2"), hot="rep2", grow=ease(seg(t, 0, 1.2)))
    rx = ST["rep2"][0]
    actor(img, ox, "agent", "idle", rx - 30, R2_Y - 46, t)
    d = ImageDraw.Draw(img)
    # files fly in from the run; a chat bubble is crossed out
    for i in range(3):
        u = seg(t, 1.0 + 0.3 * i, 1.6 + 0.3 * i)
        if 0 < u < 1:
            x = lerp(ST["ana2"][0] - ox, rx - ox - 30, ease(u))
            S.draw(img, "file_doc", "idle", 0, x, R2_Y - 20 - 14 * math.sin(u * math.pi), scale=2)
    if t > 1.2:
        bx, by = rx - ox - 124, R2_Y - 80
        ui.box(d, bx, by, bx + 46, by + 22, fill=PAPER, border=DGREY, inner=None)
        d.polygon([(bx + 30, by + 22), (bx + 38, by + 22), (bx + 40, by + 29)], fill=C(DGREY))
        text(img, bx + 23, by + 3, "CHAT", DGREY, align="c")
        if t > 1.8:
            d.line([(bx - 3, by - 3), (bx + 49, by + 25)], fill=C(ORANGE), width=3)
    lines = [("FRESH AGENT. FILES ONLY.", DGREY), ("ANSWER:", INK), ("MORE T CELLS GIVE LONGER LIFE.", BROWN)]
    card(img, 212, 10, 262, "REPORT R02 (DRAFT)", lines, t, t0=1.4)


def part_check(img, t, sc, ctx):
    t_no, t_veto, t_fix, t_pass = 1.6, 2.4, 3.6, 4.8
    ox = world(img, cam_x(sc, t), lit=lit_upto("check"), hot="check", veto=ease(seg(t, t_veto, t_veto + 0.8)))
    cx = ST["check"][0]
    actor(img, ox, "supervisor", "alert" if t_no < t < t_fix else "idle", cx + 44, R2_Y - 46, t, flip=True)
    lines = [("Q1-Q5  YES", XBLUE), ("Q6     NO: CAUSE, NOT LINK", BROWN if t > t_no else PAPER),
             ("Q7     YES", XBLUE if t > t_no else PAPER)]
    card(img, 10, 8, 232, "SUPERVISOR: YES OR NO", lines, t, t0=0.4, cps=40)
    if t < t_pass:
        stamp(img, 316, 22, "VETO", BROWN, t, t_veto)
    if t > t_fix:
        d = ImageDraw.Draw(img)
        ui.box(d, 252, 66, 472, 100, fill=PAPER, border=NAVY, inner=None)
        text(img, 258, 68, "FIX:", DGREY)
        s = "LINKED, NOT PROVEN."
        text(img, 258, 83, s[:int((t - t_fix) * 30)], NAVY)
    stamp(img, 316, 22, "PASS", XBLUE, t, t_pass)


def part_sign(img, t, sc, ctx):
    lines = [("ANSWER, VERDICT, LIMITS", INK), ("SIGN RELEASE V1?  YES", LAV), ("RELEASES/V1  FROZEN", DGREY)]
    t_yes = typed_until(lines[:2], 0.6, 30)
    ox = world(img, cam_x(sc, t), lit=lit_upto("sign"), hot="sign", grow=ease(seg(t, 0, 1.2)),
               pulse=t > t_yes and int(t * 3) % 2 == 0)
    sx = ST["sign"][0]
    actor(img, ox, "person", "cheer" if t > t_yes else "idle", sx - 40, R2_Y - 46, t)
    card(img, 228, 10, 244, "THE RELEASE", lines, t, t0=0.6)
    if t > t_yes + 0.8:
        S.draw(img, "lock", "idle", 0, sx - ox + 30, R2_Y - 40, scale=2)


def part_show(img, t, sc, ctx):
    ox = world(img, cam_x(sc, t), lit=lit_upto("show"), hot="show", grow=ease(seg(t, 0, 1.2)))
    d = ImageDraw.Draw(img)
    sx = ST["show"][0] - ox
    if t > 1.2:
        S.draw(img, "deck", "idle", 0, sx - 60, 52, scale=3)
        text(img, sx - 60, 76, "SLIDES", INK, align="c")
    if t > 1.8:
        # a small screen that plays this video: the road and a dot that runs along it
        x0, y0 = sx + 4, 24
        ui.box(d, x0, y0, x0 + 96, y0 + 56, fill=PAPER, border=INK, inner=None)
        d.rectangle([x0 + 2, y0 + 2, x0 + 94, y0 + 54], fill=C(PAPER))
        d.line([(x0 + 8, y0 + 34), (x0 + 30, y0 + 34), (x0 + 40, y0 + 22), (x0 + 88, y0 + 22)], fill=C(LGREY), width=3)
        d.line([(x0 + 30, y0 + 34), (x0 + 40, y0 + 44), (x0 + 88, y0 + 44)], fill=C(LGREY), width=3)
        u = ((t - 1.8) / 3.0) % 1.0
        px = lerp(x0 + 8, x0 + 88, u)
        py = y0 + 34 if px < x0 + 30 else y0 + 44
        d.rectangle([px - 2, py - 2, px + 2, py + 2], fill=C(NAVY))
        d.rectangle([x0 + 40, y0 + 58, x0 + 56, y0 + 62], fill=C(DGREY))
        text(img, x0 + 48, 92, "VIDEO", INK, align="c")


def _mini_tile(img, x, y, icon=None, you=False, col=DGREY):
    d = ImageDraw.Draw(img)
    ui.box(d, x - 8, y - 8, x + 8, y + 8, fill=PAPER, border=col, inner=None)
    if you:
        diamond(d, x + 8, y - 8, YOU)


def part_runs(img, t, sc, ctx):
    d = ImageDraw.Draw(img)
    gx, gy = 46, 118
    d.line([(10, gy), (gx + 30, gy)], fill=C(ROAD_ON), width=4)
    _mini_tile(img, gx, gy, you=True, col=NAVY)
    text(img, gx, gy - 8, "?", NAVY, align="c")
    text(img, gx, gy + 12, "GRILL", INK, align="c")
    names = sc.get("runs") or []
    for i, name in enumerate(names):
        ti = 0.5 + 0.5 * i
        if t < ti:
            continue
        k = ease(seg(t, ti, ti + 0.6))
        y = 30 + 40 * i
        x0 = 120 + 22 * i
        pts = _bez((gx + 30, gy), (gx + 60, gy), (x0 - 40, y), (x0, y)) + [(x0 + 132, y)]
        _line(d, _part(pts, k), 0, ROAD_ON, 2)
        if k >= 1:
            for j, xx in enumerate((x0 + 22, x0 + 66, x0 + 110)):
                _mini_tile(img, xx, y, you=(j == 0), col=NAVY)
            S.draw(img, "datasheet", "idle", 0, x0 + 22, y)
            S.draw(img, "computer", "idle", 0, x0 + 66, y)
            S.draw(img, "file_doc", "idle", 0, x0 + 110, y)
            text(img, x0 + 136, y - 8, name, NAVY)
            if i + 1 < len(names) and t > ti + 0.8:
                _dashed(d, _bez((x0 + 110, y + 9), (x0 + 120, y + 24), (x0 + 30, y + 20), (x0 + 44, y + 31)), 0, DGREY)


def part_parallel(img, t, sc, ctx):
    d = ImageDraw.Draw(img)
    ys = (54, 122, 190)
    names = sc.get("tasks") or []
    S.idle(img, "person", t, 26, 128, scale=2)
    done = t > float(sc.get("accept_at", 6.0))
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


def part_summary(img, t, sc, ctx):
    d = ImageDraw.Draw(img)
    text(img, W // 2, 6, "FROM A QUESTION TO A DECISION", NAVY, align="c")
    row1 = [("ASK", "bulb", False), ("GRILL", "?", True), ("PLAN", "datasheet", True), ("DESCRIBE", "computer", False),
            ("OUTCOME", "computer", False)]
    row2 = [("REPORT", "file_doc", False), ("SUPERVISOR", "check_card", False), ("SIGN", "folder", True),
            ("SHOW", "deck", False)]
    y1, y2 = 66, 148
    xs1 = [44, 140, 236, 332, 428]
    xs2 = [428, 320, 212, 104]
    d.line([(xs1[0], y1), (xs1[-1], y1)], fill=C(ROAD), width=7)
    d.line([(xs1[0], y1), (xs1[-1], y1)], fill=C(ROAD_ON), width=3)
    d.line([(xs1[-1], y1), (xs2[0], y2)], fill=C(ROAD_ON), width=3)
    d.line([(xs2[0], y2), (xs2[-1], y2)], fill=C(ROAD), width=7)
    d.line([(xs2[0], y2), (xs2[-1], y2)], fill=C(ROAD_ON), width=3)
    pts = _bez((xs2[1] - 2, y2 - 14), (xs2[1] + 6, y2 - 62), (xs2[0] - 6, y2 - 62), (xs2[0] + 2, y2 - 15))
    _line(d, pts, 0, ORANGE, 2)
    d.polygon([(xs2[0] - 2, y2 - 21), (xs2[0] + 6, y2 - 21), (xs2[0] + 2, y2 - 15)], fill=C(ORANGE))
    text(img, (xs2[0] + xs2[1]) // 2, y2 - 38, "VETO, FIX", BROWN, align="c")
    for (lab, icon, you), x, y in [(r, x, y1) for r, x in zip(row1, xs1)] + [(r, x, y2) for r, x in zip(row2, xs2)]:
        ui.box(d, x - 12, y - 12, x + 12, y + 12, fill=PAPER, border=NAVY, inner=None)
        if icon == "?":
            text(img, x, y - 8, "?", NAVY, align="c")
        else:
            S.draw(img, icon, "idle", 0, x, y)
        if you:
            diamond(d, x + 12, y - 12, YOU, r=4)
        text(img, x, y + 14, lab, INK, align="c")
    for lab, x in (("R01", xs1[3]), ("R02", xs1[4])):
        text(img, x, y1 - 32, lab, NAVY, align="c")
    diamond(d, 16, 196, YOU, r=4)
    text(img, 26, 188, "= YOU DECIDE", DGREY)
    if t > 0.8:
        ui.caption(img, "TYPE /ASK-KOSTA", y=212)
        text(img, W // 2, 248, "GITHUB.COM/KOSTACHERNYSHOV/SKILLS", DGREY, align="c")


PARTS = {k[5:]: v for k, v in globals().items() if k.startswith("part_")}


def draw(img, t, sc, ctx):
    PARTS[sc["part"]](img, t, sc, ctx)
