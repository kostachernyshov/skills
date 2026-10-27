# People and objects of the work world: manager, scientist, clinician, file, folder,
# computer, check card, bulb. These are not cells: the bio cast colors do not apply.
# Palette rules hold: no yellow (MHC-I), no red (tumor).
# Human scale, as in people.py: height 30 px, draw at x2 or x3.
#

import numpy as np
from .palette import *
from .pixdraw import Spr, mask_circle, mask_superellipse, outline


# ---------------------------------------------------------------- people

def worker(hair=BROWN, top=DGREY, pants=NAVY, shoes=BLACK, tie=None, coat=False, glasses=False,
           arms="down", laptop=False, blink=False):
    """Person, front view, 20x30. arms: down / up (panic) / point (right arm forward).
    tie: necktie (manager); coat: white coat over a shirt of color top (scientist); laptop: in the hands."""
    w, h = 20, 30
    s = Spr(w, h)
    ys, xs = np.mgrid[0:h, 0:w]
    cx = 9.5
    body = (ys >= 16) & (ys <= 24) & (np.abs(xs - cx) <= 4.5 + (ys - 16) * 0.1)
    s.a[body] = WHITE if coat else top
    if coat:
        s.a[body & (np.abs(xs - cx) <= 1.0) & (ys <= 21)] = top
        s.put(7, 22, LGREY); s.put(12, 22, LGREY)
    if tie is not None:
        for y in range(17, 22):
            s.put(9, y, tie); s.put(10, y, tie)
        s.put(9, 16, WHITE); s.put(10, 16, WHITE)
    sleeve = WHITE if coat else top
    skin = PEACH
    if arms == "down":
        for ax in (4, 15):
            s.rect(ax, 17, ax, 22, sleeve); s.put(ax, 23, skin)
    elif arms == "up":
        for ax, dx in ((4, -1), (15, 1)):
            s.rect(ax, 13, ax, 17, sleeve); s.put(ax + dx, 11, skin); s.put(ax, 12, skin)
    elif arms == "point":
        s.rect(4, 17, 4, 22, sleeve); s.put(4, 23, skin)
        s.rect(15, 17, 18, 17, sleeve); s.put(19, 17, skin)
    if laptop:
        s.rect(5, 20, 14, 21, LGREY); s.rect(6, 19, 13, 19, BLUE)
    s.rect(6, 25, 8, 28, pants); s.rect(11, 25, 13, 28, pants)
    s.rect(5, 29, 8, 29, shoes); s.rect(11, 29, 14, 29, shoes)
    s.rect(8, 14, 11, 16, skin)
    s.a[mask_superellipse(w, h, cx, 9.0, 5.4, 5.8, n=2.4)] = skin
    s.a[mask_circle(w, h, cx, 8.4, 6.4) & (ys <= 6)] = hair
    for (x, y) in ((4, 6), (15, 6), (4, 7), (15, 7)):
        s.put(x, y, hair)
    for ex in (7, 12):
        if blink:
            s.put(ex, 10, BLACK); s.put(ex + (1 if ex > 9 else -1), 10, BLACK)
        else:
            s.put(ex, 9, BLACK); s.put(ex, 10, BLACK)
    if glasses:
        for ex in (7, 12):
            s.put(ex - 1, 9, LGREY); s.put(ex + 1, 9, LGREY)
        s.put(9, 9, LGREY); s.put(10, 9, LGREY)
    s.put(9, 13, BROWN); s.put(10, 13, BROWN)
    outline(s, BLACK)
    return s


def manager(arms="down", laptop=False, blink=False):
    """Manager: dark suit, blue tie, short grey hair."""
    return worker(hair=DGREY, top=DGREY, pants=NAVY, tie=BLUE, arms=arms, laptop=laptop, blink=blink)


def scientist(arms="down", blink=False):
    """Scientist: white coat over a light blue shirt, glasses, light hair."""
    return worker(hair=LGREY, top=BLUE, pants=DGREY, coat=True, glasses=True, arms=arms, blink=blink)


def clinician(arms="down", blink=False):
    """Clinician: white coat over a dark green scrub, short dark hair."""
    return worker(hair=XBROWN, top=DGREEN, pants=DGREEN, coat=True, arms=arms, blink=blink)


# ---------------------------------------------------------------- objects

def file_doc():
    """Document with a folded corner, 9x11."""
    s = Spr(9, 11)
    s.rect(0, 0, 8, 10, WHITE)
    s.put(7, 0, -1); s.put(8, 0, -1); s.put(8, 1, -1)
    s.put(7, 1, LGREY); s.put(6, 0, LGREY)
    for y in (3, 5, 7):
        s.rect(1, y, 6 if y != 7 else 4, y, LGREY)
    outline(s, BLACK)
    return s


def folder():
    """Folder, 13x10."""
    s = Spr(13, 10)
    s.rect(0, 1, 4, 2, BROWN); s.rect(0, 2, 12, 9, PEACH); s.rect(0, 2, 12, 2, ORANGE)
    s.rect(0, 9, 12, 9, BROWN)
    outline(s, BLACK)
    return s


def computer(on=True):
    """Monitor on a stand, 15x14; on=False: dark screen."""
    s = Spr(15, 14)
    s.rect(0, 0, 14, 9, LGREY); s.rect(1, 1, 13, 8, NAVY)
    if on:
        for y, ln in ((2, 7), (4, 10), (6, 5)):
            s.rect(2, y, 2 + ln, y, BLUE if y != 4 else GREEN)
    s.rect(6, 10, 8, 11, LGREY); s.rect(3, 12, 11, 12, DGREY)
    outline(s, BLACK)
    return s


def check_card():
    """Check card: done, clear. 13x13."""
    s = Spr(13, 13)
    s.rect(0, 0, 12, 12, DGREEN); s.rect(1, 1, 11, 11, GREEN)
    s.rect(1, 1, 11, 1, WHITE)
    for (x, y) in ((3, 6), (4, 7), (5, 8), (6, 7), (7, 6), (8, 5), (9, 4)):
        s.put(x, y, WHITE); s.put(x, y + 1, WHITE)
    outline(s, BLACK)
    return s


def bulb(lit=True):
    """Idea bulb, 13x17. Orange filament: yellow is for MHC-I."""
    s = Spr(13, 17)
    m = mask_circle(13, 17, 6.5, 6.0, 5.2)
    s.a[m] = WHITE if lit else LGREY
    s.a[m & ~mask_circle(13, 17, 6.5, 6.0, 4.0)] = PEACH if lit else DGREY
    if lit:
        s.rect(5, 6, 7, 9, ORANGE); s.put(6, 5, ORANGE)
    else:
        s.rect(6, 7, 6, 9, DGREY)
    s.rect(4, 11, 8, 12, LGREY); s.rect(4, 13, 8, 13, DGREY); s.rect(5, 14, 7, 14, LGREY)
    outline(s, BLACK)
    return s
