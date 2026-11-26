"""Build the 26 November 2026 world-news front page (1024x1024 PNG).

Draws a dense one-page newspaper from the day's verified stories:
masthead, key-numbers strip, three big stories, a ten-story brief grid,
a numbered world map, a further-stories list, and a date-check box.
Runs with Pillow locally; the submitted entry (main.py) only copies the
finished image, so the sandbox program needs no third-party library.
"""

import hashlib
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
RED = (157, 27, 27)
FAINT = (90, 84, 70)
OCEAN = (216, 228, 232)
LAND = (226, 214, 174)
LAND_EDGE = (138, 127, 92)
PANEL = (240, 234, 218)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

NUMBERS = [
    ("250M", "AMERICANS IN STORM PATH"),
    ("60 MPH", "WIND GUSTS, NEW YORK"),
    ("31", "KILLED, CAIRO FIRE"),
    ("100TH", "MACY'S PARADE"),
    ("1,220", "IPL AUCTION ENTRIES"),
    ("500,000", "RUSSIA'S WAR DEAD"),
]

LEAD = {
    "kicker": "THANKSGIVING  ·  NEW YORK",
    "headline": "NO PARADE TODAY",
    "body": (
        "Macy's 100th Thanksgiving Day Parade, due to step off at 8:30 this "
        "morning, has been postponed to Saturday as a nor'easter bears down "
        "on New York \u2014 the first weather postponement in the parade's "
        "100-year history. The National Weather Service warns of gusts to "
        "60 mph. NBC will re-air last year's parade instead."
    ),
    "source": "USA TODAY  ·  AP",
    "pin": (-74.0, 40.7),
}

SECOND = {
    "headline": "STORM SWALLOWS THANKSGIVING",
    "body": (
        "More than 250 million Americans face holiday storms: heavy rain "
        "and flooding in the East, and King Tides flooding California, "
        "where La Jolla set a record 8.11-foot tide."
    ),
    "source": "FOX WEATHER",
    "pin": (-75.0, 40.0),
}

THIRD = {
    "headline": "FIREBALL ON THE CAIRO RING ROAD",
    "body": (
        "A fuel tanker crash ignited a huge fire on a highway ringing "
        "Cairo, killing at least 31 people in one of Egypt's deadliest "
        "road crashes this year."
    ),
    "source": "AP",
    "pin": (31.2, 30.0),
}

# (number, headline, body, source, lon, lat)
GRID = [
    (4, "HOUTHIS HIT SAUDI REFINERY",
     "Yemen's Houthis say they attacked the Ras Tanura refinery, starting fires.",
     "REUTERS", 50.0, 26.6),
    (5, "MINES HIT TWO TANKERS",
     "Two tankers struck naval mines in the Strait of Hormuz, hitting Gulf shipping.",
     "AP", 56.5, 26.5),
    (6, "ISRAEL KILLS HAMAS COLONEL",
     "An Israeli strike killed Hamas security chief Abuelouf in Gaza; truce strained.",
     "AP", 34.5, 31.5),
    (7, "UKRAINE HITS TWO REFINERIES",
     "Ukrainian forces struck two Russian refineries overnight; Putin vowed revenge.",
     "AP", 30.5, 50.4),
    (8, "RUSSIA COUNTS ITS WAR DEAD",
     "Moscow's own figures show nearly 500,000 people lost in the Ukraine war.",
     "BBC", 37.6, 55.7),
    (9, "US TO HIKE TARIFFS",
     "Washington will unveil broad new tariffs on China, the EU, Brazil and others.",
     "AP", -77.0, 38.9),
    (10, "ARMY BLOWS UP POISON STOCK",
     "The US Army destroyed the nation's entire stockpile of lead azide in Iowa.",
     "AP", -93.0, 41.6),
    (11, "VANCE: NO PARDON FOR HUANG",
     "Vance said Nvidia chief Jensen Huang will not need a pardon as scrutiny builds.",
     "AP", -80.0, 37.0),
    (12, "COLOMBIA FREES 20 HOSTAGES",
     "Police stormed a supermarket and freed 20 hostages held for 17 hours.",
     "BBC", -74.0, 4.7),
    (13, "PAKISTAN'S FIRST ASTRONAUT",
     "Muhammad Zeeshan Ali will fly on Shenzhou-24 \u2014 the first foreign astronaut there.",
     "AP", 116.4, 39.9),
]

MORE = [
    "INDIA MARKS CONSTITUTION DAY \u2014 18th since 26/11",
    "HASINA SEEKS RETURN \u2014 ex-PM eyes 16 Dec trip",
    "DHAKA RAISES GARMENT PAY \u2014 wage up 36%",
    "PYONGYANG EXPELS SWISS \u2014 office ordered shut",
    "IPL AUCTION DRAWS 1,220 \u2014 entries for 2027",
    "TEEN SMASHES 204 OFF 53 \u2014 Sooryavanshi, 15",
    "GUKESH DRAWS GAME 2 \u2014 held in 20 moves",
    "FLIPKART CHIEF TO GO \u2014 CEO exits in Dec",
    "INDIA PLEDGES \u20b915,000 CRORE \u2014 aid for Nepal",
    "INDIA: HUMANS MUST RULE AI ARMS",
    "IITs ADD 6,000 TECH SEATS \u2014 AI, space",
    "SIX DIE IN PLANE CRASH \u2014 two children lost",
    "DURAN DURAN'S TAYLOR DIES \u2014 guitarist, 65",
    "ASTEROID TEST'S NEW CRATER \u2014 close-up images",
    "XI'S GRAFT PROBE SHAKES CHINA",
    "SOLOMONS SIGN SECURITY PACT \u2014 with Australia",
    "BRAZIL MOSQUITOES CUT VIRUS 68%",
    "FED SPLIT ON INFLATION \u2014 at odds on causes",
    "TEMPUS BUYS PERSONALIS \u2014 $600M deal",
    "META MEETS CONGRESS \u2014 quizzed on suspensions",
    "RIYADH ATTACK VICTIMS GO HOME",
    "LIBYAN OFFICERS KILLED \u2014 strike on warship",
    "BIOVAC TO SCALE UP VACCINES \u2014 EU loan",
    "EMIRATES TOPS AIRLINE RANKING",
    "TOP PROSECUTOR DUCKS NVIDIA QUERY",
]

DATE_CHECK = (
    "DATE CHECK \u2014 WHAT WE LEFT OUT: the missile that landed in Poland (20 Nov)  ·  "
    "the 2008 Mumbai attacks themselves \u2014 today marks their 18th anniversary, the attacks are "
    "not today's news  ·  the 2025 Macy's parade \u2014 re-aired today, but last year's event."
)

FOOTER = (
    "SOURCES: AP  ·  REUTERS  ·  BBC  ·  USA TODAY  ·  FOX WEATHER  ·  PEOPLE  ·  INVESTING.COM"
    "      THE WORLD IN ONE DAY \u2014 THURSDAY 26 NOVEMBER 2026"
)

# Rough equirectangular continent outlines (lon, lat).
CONTINENTS = [
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-110, 73), (-95, 80),
     (-85, 80), (-78, 73), (-65, 62), (-55, 52), (-60, 46), (-70, 42),
     (-76, 35), (-81, 26), (-86, 21), (-91, 19), (-97, 16), (-104, 21),
     (-112, 28), (-120, 34), (-125, 42), (-125, 49), (-135, 58),
     (-150, 60), (-162, 58), (-168, 66)],
    [(-80, 9), (-77, 4), (-72, 0), (-62, -3), (-52, -4), (-42, -8),
     (-35, -9), (-38, -15), (-40, -22), (-48, -28), (-55, -34),
     (-65, -41), (-70, -50), (-73, -54), (-72, -44), (-73, -30),
     (-78, -18), (-81, -6), (-80, 9)],
    [(-17, 15), (-15, 27), (-9, 32), (-2, 35), (8, 37), (12, 34),
     (20, 32), (30, 31), (34, 28), (38, 20), (43, 12), (48, 11),
     (44, 2), (40, -8), (36, -18), (33, -26), (28, -33), (19, -35),
     (15, -28), (13, -18), (10, -4), (8, 4), (0, 6), (-8, 5), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 55), (8, 58),
     (12, 60), (20, 62), (28, 65), (35, 62), (40, 58), (38, 50),
     (30, 46), (24, 42), (19, 40), (12, 38), (4, 37), (-2, 36), (-10, 36)],
    [(40, 62), (50, 68), (68, 72), (90, 75), (110, 74), (130, 72),
     (150, 70), (168, 66), (162, 60), (156, 52), (142, 46), (135, 40),
     (127, 36), (120, 32), (112, 22), (108, 12), (102, 8), (96, 10),
     (90, 14), (84, 18), (78, 10), (72, 20), (66, 25), (60, 25),
     (54, 27), (48, 30), (44, 36), (40, 44), (36, 52), (40, 62)],
    [(113, -22), (120, -16), (128, -14), (136, -12), (142, -11),
     (146, -18), (150, -23), (153, -28), (150, -37), (144, -38),
     (138, -35), (132, -32), (126, -32), (120, -34), (114, -32),
     (113, -22)],
]


def wrap(text, fnt, width, draw):
    """Greedy word wrap; returns a list of lines fitting `width` pixels."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = word if not line else line + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 4], fill=INK)
    fnt = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=fnt)
    draw.text(((W - tw) / 2, 12), title, font=fnt, fill=INK)
    draw.line([24, 84, W - 24, 84], fill=INK, width=2)
    fnt = font(SANS_B, 15)
    left = "THURSDAY 26 NOVEMBER 2026"
    right = "DAY 330 OF 2026"
    draw.text((24, 92), left, font=fnt, fill=INK)
    rw = draw.textlength(right, font=fnt)
    draw.text((W - 24 - rw, 92), right, font=fnt, fill=INK)
    fnt = font(SANS, 11)
    mid = "EVERY STORY HERE HAPPENED, OR WAS FIRST REPORTED, TODAY"
    mw = draw.textlength(mid, font=fnt)
    draw.text(((W - mw) / 2, 94), mid, font=fnt, fill=FAINT)
    draw.line([24, 112, W - 24, 112], fill=INK, width=1)


def draw_numbers(draw):
    y0 = 118
    cell = (W - 48) / 6
    for i, (num, label) in enumerate(NUMBERS):
        x = 24 + i * cell
        if i:
            draw.line([x, y0 + 4, x, y0 + 32], fill=FAINT, width=1)
        fnt = font(SERIF_B, 22)
        nw = draw.textlength(num, font=fnt)
        draw.text((x + (cell - nw) / 2, y0), num, font=fnt, fill=RED)
        fnt = font(SANS_B, 9)
        lw = draw.textlength(label, font=fnt)
        draw.text((x + (cell - lw) / 2, y0 + 27), label, font=fnt, fill=INK)
    draw.line([24, 156, W - 24, 156], fill=INK, width=2)


def draw_balloon_scene(draw, x0, y0, x1, y1):
    """Schematic grounded parade balloon over a skyline, in a ruled box."""
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    draw.rectangle([x0 + 2, y0 + 2, x1 - 2, y1 - 2], fill=(223, 232, 236))
    for i in range(26):
        rx = x0 + 12 + (i * 37) % (x1 - x0 - 24)
        ry = y0 + 10 + (i * 53) % (y1 - y0 - 90)
        draw.line([rx, ry, rx - 6, ry + 14], fill=(120, 140, 150), width=1)
    base = y1 - 34
    bx = x0 + 14
    for bw, bh in [(34, 52), (26, 78), (40, 44), (30, 92), (36, 60), (28, 84),
                   (38, 48), (30, 70), (34, 56)]:
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(96, 104, 112))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(bx + 5, bx + bw - 4, 10):
                draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(240, 220, 130))
        bx += bw + 6
        if bx > x1 - 40:
            break
    draw.rectangle([x0 + 2, base, x1 - 2, y1 - 2], fill=(70, 78, 86))
    cx, cy = (x0 + x1) // 2, y0 + 74
    draw.ellipse([cx - 88, cy - 46, cx + 88, cy + 46], fill=(178, 44, 44),
                 outline=INK, width=2)
    draw.arc([cx - 88, cy - 46, cx + 88, cy + 46], 200, 340,
             fill=(255, 255, 255), width=2)
    for dx in (-52, -18, 18, 52):
        draw.line([cx + dx, cy + 40, cx + dx // 3, y1 - 40], fill=INK, width=2)
    draw.rectangle([cx - 26, y1 - 44, cx + 26, y1 - 34], fill=(120, 84, 40),
                   outline=INK, width=1)
    for sx, sy in [(x0 + 30, y0 + 28), (x1 - 60, y0 + 42), (x0 + 44, y0 + 116)]:
        draw.arc([sx, sy, sx + 34, sy + 16], 180, 20, fill=INK, width=2)
    fnt = font(SANS, 10)
    cap = "A century of parades, grounded by weather. \u2014 Illustration"
    draw.text((x0 + 8, y1 - 16), cap, font=fnt, fill=INK)


def draw_lead(draw):
    y = 164
    x, w = 24, 620
    fnt = font(SANS_B, 13)
    draw.text((x, y), LEAD["kicker"], font=fnt, fill=RED)
    y += 20
    fnt = font(SERIF_B, 47)
    for ln in wrap(LEAD["headline"], fnt, w, draw):
        draw.text((x, y), ln, font=fnt, fill=INK)
        y += 52
    y += 2
    draw.line([x, y, x + w, y], fill=INK, width=1)
    y += 8
    fnt = font(SERIF, 16)
    y = draw_wrapped(draw, x, y, wrap(LEAD["body"], fnt, w, draw), fnt,
                     leading=21)
    y += 4
    fnt = font(SANS_B, 11)
    draw.text((x, y), LEAD["source"], font=fnt, fill=FAINT)
    draw_balloon_scene(draw, 668, 164, 1000, 388)


def draw_row2(draw):
    y = 396
    cols = [(24, 480, SECOND), (520, 480, THIRD)]
    for x, w, story in cols:
        fnt = font(SERIF_B, 22)
        yy = y
        for ln in wrap(story["headline"], fnt, w, draw):
            draw.text((x, yy), ln, font=fnt, fill=INK)
            yy += 25
        yy += 2
        draw.line([x, yy, x + w, yy], fill=INK, width=1)
        yy += 6
        fnt = font(SERIF, 14)
        yy = draw_wrapped(draw, x, yy, wrap(story["body"], fnt, w, draw),
                          fnt, leading=17)
        yy += 3
        fnt = font(SANS_B, 10)
        draw.text((x, yy), story["source"], font=fnt, fill=FAINT)
    draw.line([24, 520, W - 24, 520], fill=INK, width=1)
    return 526


def draw_grid(draw, y0):
    fnt = font(SANS_B, 13)
    draw.text((24, y0), "THE WORLD IN BRIEF", font=fnt, fill=INK)
    fnt = font(SANS, 10)
    note = "Numbered stories are pinned on the map below"
    nw = draw.textlength(note, font=fnt)
    draw.text((W - 24 - nw, y0 + 2), note, font=fnt, fill=FAINT)
    y = y0 + 20
    draw.line([24, y, W - 24, y], fill=INK, width=1)
    y += 6
    cols, rows = 5, 2
    cw = (W - 48) / cols
    ch = 88
    for idx, item in enumerate(GRID):
        num, head, body, src, _lon, _lat = item
        col, row = idx % cols, idx // cols
        x = 24 + col * cw
        yy = y + row * ch
        # numbered badge
        draw.ellipse([x, yy, x + 18, yy + 18], fill=RED, outline=INK, width=1)
        fnt = font(SANS_B, 10)
        tw = draw.textlength(str(num), font=fnt)
        draw.text((x + 9 - tw / 2, yy + 3), str(num), font=fnt,
                  fill=(255, 255, 255))
        hx = x + 24
        hw = cw - 32
        fnt = font(SERIF_B, 13)
        hy = yy
        for ln in wrap(head, fnt, hw, draw)[:2]:
            draw.text((hx, hy), ln, font=fnt, fill=INK)
            hy += 16
        fnt = font(SERIF, 11)
        hy = draw_wrapped(draw, hx, hy + 1, wrap(body, fnt, hw, draw)[:3],
                          fnt, leading=12)
        fnt = font(SANS_B, 9)
        draw.text((hx, yy + 76), src, font=fnt, fill=FAINT)
        if col < cols - 1:
            draw.line([x + cw - 6, yy, x + cw - 6, yy + ch - 8],
                      fill=(200, 192, 170), width=1)
    return y + rows * ch + 4


def project(lon, lat, x0, y0, x1, y1):
    x = x0 + (lon + 170) / 360.0 * (x1 - x0)
    yy = y0 + (75 - lat) / 133.0 * (y1 - y0)
    return x, yy


def draw_map(draw, y0):
    fnt = font(SANS_B, 13)
    draw.text((24, y0), "WHERE IT HAPPENED", font=fnt, fill=INK)
    my0 = y0 + 18
    my1 = my0 + 76
    draw.rectangle([24, my0, W - 24, my1], fill=OCEAN, outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, 24, my0, W - 24, my1) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    pins = [(1, LEAD["pin"]), (2, SECOND["pin"]), (3, THIRD["pin"])]
    for item in GRID:
        pins.append((item[0], (item[4], item[5])))
    nudges = {1: (-11, -7), 2: (9, 8), 9: (0, -8), 11: (10, 6), 5: (8, 6),
              4: (-8, -6), 6: (7, 7), 3: (-7, 7)}
    for num, (lon, lat) in pins:
        px, py = project(lon, lat, 24, my0, W - 24, my1)
        dx, dy = nudges.get(num, (0, 0))
        px, py = px + dx, py + dy
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=INK,
                     width=1)
        fnt = font(SANS_B, 10)
        tw = draw.textlength(str(num), font=fnt)
        draw.text((px - tw / 2, py - 7), str(num), font=fnt,
                  fill=(255, 255, 255))
    return my1 + 6


def draw_more(draw, y0):
    fnt = font(SANS_B, 13)
    draw.text((24, y0), "AND 25 MORE STORIES", font=fnt, fill=INK)
    draw.line([24, y0 + 18, W - 24, y0 + 18], fill=INK, width=1)
    y = y0 + 24
    fnt = font(SERIF, 10)
    colw = (W - 48 - 2 * 16) / 3
    per_col = 9
    for i, item in enumerate(MORE):
        col, row = i // per_col, i % per_col
        x = 24 + col * (colw + 16)
        yy = y + row * 12
        line = wrap(item, fnt, colw, draw)[0]
        draw.text((x, yy), "\u25aa  " + line, font=fnt, fill=INK)
    return y + per_col * 12 + 4


def draw_datecheck(draw, y):
    draw.rectangle([24, y, W - 24, y + 32], fill=PANEL, outline=INK, width=1)
    fnt = font(SERIF, 10)
    lines = wrap(DATE_CHECK, fnt, W - 48 - 16, draw)
    yy = y + 3
    for ln in lines[:2]:
        draw.text((32, yy), ln, font=fnt, fill=INK)
        yy += 13
    fnt = font(SANS, 10)
    fw = draw.textlength(FOOTER, font=fnt)
    draw.text(((W - fw) / 2, y + 36), FOOTER, font=fnt, fill=FAINT)


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_numbers(draw)
    draw_lead(draw)
    y = draw_row2(draw)
    y = draw_grid(draw, y)
    y = draw_map(draw, y)
    y = draw_more(draw, y)
    draw_datecheck(draw, y)
    img.save(out_path, "PNG", optimize=True)
    data = open(out_path, "rb").read()
    return len(data), hashlib.sha256(data).hexdigest()


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    size, digest = build(target)
    print("wrote", target, size, "bytes sha256", digest)
