#!/usr/bin/env python3
"""Build a 16:9 deck from deck.yaml. Usage: make_deck.py deck.yaml out/deck.pptx

Slide keys: title (required), bullets, figure, table, highlight_row, kpis, note.
Layout is chosen from the content:
- kpis only (with optional bullets): 2-3 big numbers across the slide.
- figure or table with 0-2 bullets: full width, bullets as one line under the title.
- figure or table with 3+ bullets: bullets left (40%), figure or table right (60%).
- bullets only: large text, full width.
"""
import os, shutil, subprocess, sys
import yaml
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

INK = RGBColor(0x15, 0x20, 0x2B)
MUTED = RGBColor(0x5A, 0x68, 0x76)
ACCENT = RGBColor(0x0F, 0x7F, 0x86)
SOFT = RGBColor(0xE6, 0xF2, 0xF3)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
W, H = Inches(13.333), Inches(7.5)
M = Inches(0.6)
TOP = Inches(1.9)


def box(slide, x, y, w, h, s, size, color=INK, bold=False, align=None, anchor=None):
    tf = slide.shapes.add_textbox(x, y, w, h).text_frame
    tf.word_wrap = True
    if anchor:
        tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.text, p.font.size, p.font.bold, p.font.color.rgb = str(s), Pt(size), bold, color
    if align:
        p.alignment = align
    return tf


def title_lines(s, width_in, size):
    chars = max(1, int(width_in * 72 / (size * 0.5)))
    return max(1, -(-len(s) // chars))


def bullets(slide, x, y, w, h, items, size):
    tf = slide.shapes.add_textbox(x, y, w, h).text_frame
    tf.word_wrap = True
    for i, b in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text, p.font.size, p.font.color.rgb = "• " + str(b), Pt(size), INK
        p.space_after = Pt(size * 0.6)


def table(slide, x, y, w, rows, highlight=None, size=18):
    n, m = len(rows), len(rows[0])
    row_h = Inches(0.62)
    t = slide.shapes.add_table(n, m, x, y, w, row_h * n).table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = t.cell(i, j)
            c.text = str(v)
            c.fill.solid()
            c.fill.fore_color.rgb = ACCENT if i == 0 else (SOFT if i == highlight else WHITE)
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(size)
                p.font.bold = i == 0 or i == highlight
                p.font.color.rgb = WHITE if i == 0 else INK


def figure(slide, path, x, y, w, h):
    from PIL import Image
    iw, ih = Image.open(path).size
    s = min(w / iw, h / ih)
    pw, ph = int(iw * s), int(ih * s)
    slide.shapes.add_picture(path, x + int((w - pw) / 2), y + int((h - ph) / 2), pw, ph)


def kpis(slide, items, y, h):
    n = len(items)
    gap = Inches(0.4)
    w = int((W - 2 * M - gap * (n - 1)) / n)
    for i, k in enumerate(items):
        x = M + i * (w + gap)
        shp = slide.shapes.add_shape(1, x, y, w, h)
        shp.fill.solid(); shp.fill.fore_color.rgb = SOFT; shp.line.fill.background()
        box(slide, x, y + Inches(0.3), w, Inches(1.4), k["value"], 54, ACCENT, True, PP_ALIGN.CENTER)
        box(slide, x + Inches(0.2), y + Inches(1.8), w - Inches(0.4), h - Inches(2.0), k["label"], 20, INK, False, PP_ALIGN.CENTER)


def main(spec_path, out_path):
    spec = yaml.safe_load(open(spec_path))
    root = os.getcwd()
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    blank = prs.slide_layouts[6]
    cw = W - 2 * M

    s = prs.slides.add_slide(blank)
    n = title_lines(spec["title"], 12.1, 40)
    box(s, M, Inches(2.0), cw, Inches(0.75 * n), spec["title"], 40, bold=True)
    box(s, M, Inches(2.0) + Inches(0.75 * n) + Inches(0.4), cw, Inches(0.8), spec.get("subtitle", ""), 20, MUTED)

    for sl in spec["slides"]:
        s = prs.slides.add_slide(blank)
        box(s, M, Inches(0.3), cw, Inches(1.3), sl["title"], 28, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        s.shapes.add_connector(1, M, Inches(1.7), W - M, Inches(1.7)).line.color.rgb = ACCENT
        bl = sl.get("bullets") or []
        body_h = H - TOP - Inches(0.5)
        side = sl.get("figure") or sl.get("table")
        if sl.get("kpis"):
            kpis(s, sl["kpis"], TOP + Inches(0.2), Inches(3.2))
            if bl:
                bullets(s, M, TOP + Inches(3.7), cw, Inches(1.6), bl, 20)
        elif side and len(bl) <= 2:
            y = TOP
            if sl.get("figure"):
                for b in bl:
                    box(s, M, y, cw, Inches(0.5), b, 20, MUTED)
                    y += Inches(0.5)
                figure(s, os.path.join(root, sl["figure"]), M, y, cw, H - y - Inches(0.3))
            else:
                rows = sl["table"]
                table(s, M, y, cw, rows, sl.get("highlight_row"))
                y += Inches(0.62) * len(rows) + Inches(0.4)
                if bl:
                    bullets(s, M, y, cw, H - y - Inches(0.3), bl, 22)
        elif side:
            bw = int(cw * 0.4)
            bullets(s, M, TOP, bw, body_h, bl, 20)
            sx, sw = M + bw + Inches(0.3), cw - bw - Inches(0.3)
            if sl.get("figure"):
                figure(s, os.path.join(root, sl["figure"]), sx, TOP, sw, body_h)
            else:
                table(s, sx, TOP, sw, sl["table"], sl.get("highlight_row"), 16)
        else:
            bullets(s, M, TOP + Inches(0.2), cw, body_h, bl, 26)
        if sl.get("note"):
            s.notes_slide.notes_text_frame.text = sl["note"]

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    prs.save(out_path)
    print("saved", out_path, "slides:", len(prs.slides))
    office = shutil.which("soffice") or shutil.which("libreoffice")
    if office:
        subprocess.run([office, "--headless", "--convert-to", "pdf", "--outdir",
                        os.path.dirname(out_path) or ".", out_path],
                       check=False, capture_output=True, timeout=180)
        print("pdf", os.path.splitext(out_path)[0] + ".pdf")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
