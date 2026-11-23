#!/usr/bin/env python3
"""Build-time poster renderer for the news-image-20261123 entry.

Draws the 1024x1024 "The World Today" poster for Monday 23 November 2026
with Pillow and saves it as a PNG. This script is only used at build time;
the graded entrypoint (main.py) needs nothing but the standard library.

Usage: python3 build_poster.py <output.png>
"""

import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 48
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 243, 234)
INK = (22, 22, 24)
MUTED = (92, 88, 80)
RED = (168, 32, 24)
RULE = (22, 22, 24)
CELL_LINE = (196, 189, 172)

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap against pixel width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, text, y, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def story_block(draw, x, y, width, tag, headline, summary):
    """One grid story: tag, headline, summary. Returns the y after it."""
    tag_f = font(SANS_BOLD, 20)
    head_f = font(SERIF_BOLD, 30)
    sum_f = font(SANS, 22)
    draw.text((x, y), tag, font=tag_f, fill=RED)
    y += 27
    y = draw_lines(draw, wrap(draw, headline, head_f, width), x, y, head_f, INK, 36)
    y += 3
    y = draw_lines(draw, wrap(draw, summary, sum_f, width), x, y, sum_f, MUTED, 28)
    return y


def main():
    out_path = sys.argv[1]
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ------------------------------------------------------
    y = 28
    centered(draw, "T H E   W O R L D   I N   O N E   I M A G E", y, font(SANS_BOLD, 20), MUTED)
    y += 30
    centered(draw, "THE WORLD TODAY", y, font(SERIF_BOLD, 78), INK)
    y += 92
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=5)
    y += 9
    centered(draw, "MONDAY  ·  23 NOVEMBER 2026", y, font(SANS_BOLD, 31), RED)
    y += 44
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 22

    # ---- Lead story -----------------------------------------------------
    draw.text((MARGIN, y), "LEAD STORY — UKRAINE", font=font(SANS_BOLD, 21), fill=RED)
    y += 29
    lead_head_f = font(SERIF_BOLD, 52)
    y = draw_lines(
        draw,
        wrap(draw, "Russian Strikes Kill 11 Near Kyiv", lead_head_f, CONTENT_W),
        MARGIN, y, lead_head_f, INK, 60,
    )
    y += 5
    lead_sum_f = font(SANS, 25)
    y = draw_lines(
        draw,
        wrap(
            draw,
            "Rescuers pulled survivors from a collapsed block of flats in Dymer "
            "as the regional death toll climbed to 11.",
            lead_sum_f, CONTENT_W,
        ),
        MARGIN, y, lead_sum_f, MUTED, 34,
    )
    y += 14
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 20

    # ---- Grid of six ----------------------------------------------------
    stories = [
        ("MIDDLE EAST",
         "Tankers Hit Near Hormuz, Bahrain Blames Iran",
         "Bahrain blames Iran for a plant strike as tankers burn near "
         "Hormuz; Trump leans to strikes if no deal by New Year."),
        ("INDONESIA",
         "24 Dead in Banten Candy Factory Fire",
         "The toll is confirmed as rescuers search the Cikande plant ruins "
         "for about 30 workers still missing."),
        ("UNITED STATES",
         "Democrats Win 258 House Seats",
         "The largest majority for either party since 1992, sealed by a "
         "North Carolina recount in the midterms."),
        ("MARKETS",
         "AI Sell-Off Routs Asian Markets",
         "Tokyo's Nikkei sank about 5% as AI valuation fears spread; the "
         "Nasdaq had its worst week since 2020."),
        ("LIBYA",
         "Ukraine Sinks Russian Corvette at Benghazi",
         "Zelensky says seven sea drones sank the corvette Merkury and hit "
         "a ship Moscow used to carry weapons."),
        ("SPORT",
         "Liverpool Thrash Man United 4-0",
         "Ten-man United collapsed at Anfield in a nightmare first match "
         "in charge for manager Mauricio Pochettino."),
    ]
    col_gap = 36
    col_w = (CONTENT_W - col_gap) // 2
    row_h = 186
    grid_top = y
    for i, (tag, head, summ) in enumerate(stories):
        row, col = divmod(i, 2)
        x = MARGIN + col * (col_w + col_gap)
        top = grid_top + row * row_h
        if col == 1:
            draw.line([(x - col_gap // 2, top), (x - col_gap // 2, top + row_h - 26)],
                      fill=CELL_LINE, width=2)
        story_block(draw, x, top, col_w, tag, head, summ)
    y = grid_top + 3 * row_h + 4

    # ---- Footer ---------------------------------------------------------
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=3)
    y += 13
    centered(
        draw,
        "23 NOVEMBER 2026 · REPORTED BY REUTERS · AP · AFP · CNN · WSJ · SKY SPORTS",
        y, font(SANS_BOLD, 19), MUTED,
    )

    img.save(out_path, format="PNG", optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
