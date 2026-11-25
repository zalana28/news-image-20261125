#!/usr/bin/env python3
"""Compose the news-image poster for Wednesday 25 November 2026.

Draws a 1024x1024 newspaper front page with PIL: 4 lead stories with
hand-drawn illustrations, a 12-story grid, a 28-item ALSO list, a
timeline strip, a schematic world map with numbered pins, a BY FIELD
bar and a DATE CHECK box. Also writes assets/hero.png (globe emblem).

Deterministic: no timestamps, no randomness, fixed font paths.
Run:  python3 compose_poster.py   (writes entry.png + assets/hero.png)
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = "/home/hatch/workspace/fonts"
F_SERIF = os.path.join(FONTS, "PlayfairDisplay-Bold.ttf")
F_SANS = os.path.join(FONTS, "PlusJakartaSans-Regular.ttf")
F_SANS_B = os.path.join(FONTS, "PlusJakartaSans-Bold.ttf")
F_SANS_SB = os.path.join(FONTS, "PlusJakartaSans-SemiBold.ttf")
F_SANS_M = os.path.join(FONTS, "PlusJakartaSans-Medium.ttf")

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (26, 26, 26)
MUTED = (107, 98, 87)
RULE = (201, 191, 169)
RED = (179, 38, 30)
BLUE = (29, 78, 137)
GREEN = (30, 122, 52)
AMBER = (138, 109, 0)
LIGHT = (238, 232, 220)

CONF_STYLE = {
    "CONFIRMED": (GREEN, (227, 242, 230)),
    "OFFICIAL": (BLUE, (226, 235, 245)),
    "REPORTED": (AMBER, (251, 243, 208)),
    "CLAIM": (RED, (251, 233, 231)),
}

# ---------------------------------------------------------------- data
# section: lead | grid | also.  field/region drive the masthead counts.
LEADS = [
    dict(n="L1", field="Conflict", region="Middle East",
         kick="STRAIT OF HORMUZ",
         head="MINES IN THE STRAIT: TANKERS ABLAZE OFF HORMUZ",
         body=("IRGC says two tankers hit mines and caught fire in the "
               "strait; a US escort was with the convoy. Oil slides."),
         src="Reuters / IRGC", conf="CONFIRMED", art="tanker"),
    dict(n="L2", field="Markets", region="North America",
         kick="WALL STREET",
         head="NVIDIA SINKS 7% AS HILL QUESTIONS HUANG'S RETURN",
         body=("Shares fell 7% as lawmakers probe Trump's role in "
               "restoring Huang. He admits a conduct breach and faces "
               "the Senate."),
         src="BBC / Guardian", conf="CONFIRMED", art="chart"),
    dict(n="L3", field="Society", region="Latin America",
         kick="CARTAGENA, COLOMBIA",
         head="CARTAGENA SIEGE ENDS: EVERY HOSTAGE FREED",
         body=("Troops stormed a Cartagena supermarket after a day-long "
               "siege; one gunman was killed and every hostage walked "
               "out alive."),
         src="Horizon (3 src)", conf="CONFIRMED", art="store"),
    dict(n="L4", field="Space", region="Asia",
         kick="JIUQUAN, CHINA",
         head="PAKISTAN'S FIRST ASTRONAUT RIDES SHENZHOU-24",
         body=("A Long March 2F lifted Shenzhou-24 from Jiuquan. "
               "Zeeshan Ali is Pakistan's first astronaut \u2014 and "
               "Tiangong's first foreign guest."),
         src="Paris Times", conf="CONFIRMED", art="rocket"),
]

GRID = [
    dict(field="Conflict", region="Middle East",
         head="Houthi strike hits Riyadh tower; 11 hurt \u2014 coalition hits Hodeidah",
         src="Horizon", conf="CONFIRMED"),
    dict(field="Conflict", region="Europe",
         head="Zelenskiy confirms ship strike off Finland; 2 die in Libya raid",
         src="Reuters", conf="CONFIRMED"),
    dict(field="Courts", region="North America",
         head="Huawei guilty on 10 of 12 counts; acquitted of racketeering",
         src="Reuters / WSJ", conf="REPORTED"),
    dict(field="Markets", region="North America",
         head="Nikkei \u22122.8%, Kospi \u22126%; Nasdaq \u22121.5%; VIX 26.4; Brent \u22124.4%",
         src="Horizon", conf="CONFIRMED"),
    dict(field="Politics", region="North America",
         head="Trump plans new tariffs on 16 economies after trade probe",
         src="BBC", conf="REPORTED"),
    dict(field="Politics", region="North America",
         head="Democrats clinch House majority: 259+ seats, best since 1990",
         src="The Hindu", conf="REPORTED"),
    dict(field="Diplomacy", region="Oceania",
         head="Solomons\u2013Australia treaty bars foreign military bases",
         src="One Turn", conf="CONFIRMED"),
    dict(field="Society", region="Asia",
         head="Bangladesh garment wage up 36% after weeks of protests",
         src="Horizon", conf="CONFIRMED"),
    dict(field="Disaster", region="Asia",
         head="Dozens trapped 100m down in Indonesian mine since Sunday",
         src="Horizon", conf="CONFIRMED"),
    dict(field="Health", region="Latin America",
         head="WHO: end US fuel blockade on Cuba; life expectancy falls",
         src="Horizon", conf="OFFICIAL"),
    dict(field="Conflict", region="Africa",
         head="DR Congo plane missing, rebels claim kill; Ebola fuels abuse",
         src="One Turn", conf="REPORTED"),
    dict(field="Politics", region="Europe",
         head="Spain heads for a snap election",
         src="One Turn", conf="REPORTED"),
]

ALSO = [
    ("Politics", "Asia", "China probes Shanghai party chief Chen Jining"),
    ("Courts", "Asia", "Iran flogs singer 74 times over unveiled concert"),
    ("Courts", "Africa", "Zambia indicts opposition leader for treason"),
    ("Society", "Asia", "Hong Kong marks a year since the Tai Po fire"),
    ("Diplomacy", "North America", "Pentagon faults Canada's military spending"),
    ("Migration", "North America", "\u00c1brego Garc\u00eda leaves US voluntarily for Spain"),
    ("Politics", "North America", "Trump pardons turkeys Freedom and Feathers"),
    ("Courts", "North America", "Fort Hood gunman Hasan seeks execution stay"),
    ("Courts", "Europe", "Sarkozy corruption case sent to trial"),
    ("Politics", "Europe", "Sweden to vote on Kristersson staying PM"),
    ("Diplomacy", "Middle East", "Eisenkot seals first coalition pact in Israel"),
    ("Conflict", "Middle East", "Israeli strike kills Hamas security chief"),
    ("Diplomacy", "Middle East", "Netanyahu urges Trump to resume Iran strikes"),
    ("Conflict", "Middle East", "US weighs targeting Iran's top leaders"),
    ("Conflict", "Middle East", "Houthis threaten Jeddah, Saudi Red Sea ports"),
    ("Markets", "Latin America", "Venezuela reveals $237.5bn public debt"),
    ("Markets", "Latin America", "Argentina slips into technical recession"),
    ("Markets", "Oceania", "Australia inflation rises to 4.9%"),
    ("Climate & Energy", "Europe", "UK energy bills to jump 26% in January"),
    ("Markets", "Europe", "BYD picks France for first W. Europe plant"),
    ("Markets", "Asia", "Boeing: China Southern arm orders 50 jets"),
    ("Space", "Latin America", "Ariane 6 lifts 36 Amazon Leo satellites"),
    ("Culture", "North America", "GTA 6 sold 44.9m copies in first weekend"),
    ("Sport", "Europe", "UCL: Real 5\u20131 PSV; Arsenal 1\u20131 Dortmund"),
    ("Sport", "Africa", "Senegal regain AFCON crown on CAS ruling"),
    ("Disaster", "North America", "Cessna crashes in Gulf of Mexico; 6 dead"),
    ("Science", "Oceania", "Deepest volcanic blasts found, Mariana Trench"),
    ("Tech", "North America", "AI staff fear unreleased models too unsafe"),
]

TIMELINE = [
    ("OVERNIGHT", "Mines hit tankers in Hormuz; oil slides"),
    ("MORNING", "Asia markets plunge; Nikkei \u22122.8%"),
    ("MIDDAY", "Cartagena siege ends; all hostages freed"),
    ("AFTERNOON", "Shenzhou-24 lifts off with Pakistan's first astronaut"),
    ("EVENING", "Tariff plan reported; turkeys pardoned in Washington"),
]

DATE_CHECK = [
    "COP31 talks collapsed Sun 22 Nov \u2014 oil states blocked a phase-out.",
    "Huang was reinstated as Nvidia CEO Mon 23 Nov \u2014 not today.",
    "BepiColombo reached Mercury orbit Sat 21 Nov \u2014 not today.",
    "AI Riemann-proof claim was Fri 20 Nov; checks ran 21 Nov.",
    "CAN-2025 final was Jan 2026 \u2014 only the CAS ruling is this week.",
]

# (lon, lat, number) pins for the schematic map.
PINS = [
    (56, 26, "1"), (-75, 10, "2"), (100, 40, "3"), (-77, 39, "4"),
    (47, 25, "5"), (90, 24, "6"), (113, -2, "7"), (160, -9, "8"),
]
PIN_LEGEND = ("1 Hormuz \u00b7 2 Cartagena \u00b7 3 Jiuquan \u00b7 4 Washington \u00b7 "
              "5 Riyadh \u00b7 6 Dhaka \u00b7 7 Indonesia \u00b7 8 Honiara")

# Rough continent outlines as (lon, lat) points, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-85, 70), (-75, 62),
     (-55, 52), (-60, 47), (-70, 44), (-75, 35), (-80, 26), (-90, 21),
     (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60),
     (-155, 58), (-165, 60)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-58, -35), (-65, -42), (-70, -52), (-73, -40),
     (-72, -20), (-80, -5), (-81, 5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29),
     (26, -34), (18, -35), (15, -27), (12, -18), (9, 4), (-8, 4)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 58), (10, 57), (18, 56),
     (21, 55), (28, 60), (30, 70), (40, 68), (60, 70), (80, 73), (100, 77),
     (120, 73), (140, 72), (160, 70), (178, 66), (170, 60), (162, 56),
     (158, 52), (142, 50), (140, 40), (130, 35), (122, 30), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (80, 15), (75, 8), (70, 20),
     (60, 25), (55, 26), (50, 29), (48, 30), (43, 36), (36, 36), (30, 36),
     (22, 38), (15, 40), (10, 44), (3, 43), (-2, 37), (-9, 37)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (137, -35), (140, -38), (147, -39), (150, -37), (153, -27), (153, -24),
     (146, -19), (142, -11), (136, -12), (132, -12), (126, -14), (122, -17),
     (118, -20)],
]

ALL = LEADS + GRID + [dict(field=f, region=r, head=t) for f, r, t in ALSO]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def conf_tag(d, x, y, label):
    """Draw a small confidence pill; returns its right edge."""
    fg, bg = CONF_STYLE[label]
    f = font(F_SANS_B, 8)
    w = int(d.textlength(label, font=f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=6, fill=bg)
    d.text((x + 5, y + 2), label, font=f, fill=fg)
    return x + w


def draw_hero():
    """Globe emblem: navy disc, graticule, red pins, orbit ring."""
    s = 512
    img = Image.new("RGB", (s, s), PAPER)
    d = ImageDraw.Draw(img)
    cx = cy = s // 2
    r = 200
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(23, 68, 120))
    for k in range(-2, 3):
        d.ellipse([cx - r + k * 62, cy - r, cx + r + k * 62, cy + r],
                  outline=(120, 170, 220), width=3)
    for yy in (cy - 100, cy, cy + 100):
        d.ellipse([cx - r, yy - 14, cx + r, yy + 14],
                  outline=(120, 170, 220), width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(15, 45, 90), width=6)
    # orbit ring
    d.ellipse([cx - 236, cy - 236, cx + 236, cy + 236],
              outline=RED, width=5)
    # pins
    for px, py in [(cx - 90, cy - 60), (cx + 70, cy - 110), (cx + 110, cy + 40),
                   (cx - 40, cy + 110)]:
        d.ellipse([px - 13, py - 13, px + 13, py + 13], fill=RED,
                  outline=(255, 255, 255), width=3)
    # headline bars
    for i, wdt in enumerate((300, 240, 270)):
        y = 452 + i * 16
        d.rectangle([106, y, 106 + wdt, y + 8], fill=INK)
    return img


def draw_art(d, kind, x, y, w, h):
    """Small hand-drawn illustration for a lead story."""
    if kind == "tanker":
        d.rectangle([x, y, x + w, y + h], fill=(23, 68, 120))
        d.rectangle([x, y + h - 22, x + w, y + h], fill=(16, 48, 86))
        d.polygon([(x + 20, y + h - 22), (x + 150, y + h - 22),
                   (x + 140, y + h - 8), (x + 30, y + h - 8)], fill=(60, 60, 60))
        d.rectangle([x + 150, y + h - 44, x + 185, y + h - 22], fill=(90, 90, 90))
        d.rectangle([x + 160, y + h - 58, x + 172, y + h - 44], fill=(120, 120, 120))
        cx, cy = x + 195, y + 26
        for dx, dy in [(0, -16), (11, -11), (16, 0), (11, 11), (0, 16),
                       (-11, 11), (-16, 0), (-11, -11)]:
            d.line([cx, cy, cx + dx, cy + dy], fill=(255, 176, 32), width=4)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 120, 40))
        for mx, my in [(x + 60, y + 18), (x + 105, y + 12)]:
            d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(30, 30, 30))
    elif kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(250, 246, 238),
                    outline=RULE, width=1)
        d.rectangle([x + 14, y + 14, x + 52, y + 52], fill=(23, 68, 120))
        d.rectangle([x + 20, y + 20, x + 30, y + 46], fill=(120, 170, 220))
        d.rectangle([x + 34, y + 26, x + 44, y + 46], fill=(120, 170, 220))
        pts = [(x + 62, y + 18), (x + 105, y + 26), (x + 148, y + 22),
               (x + 185, y + 52), (x + 218, y + 68)]
        d.line(pts, fill=RED, width=4)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
        d.text((x + 62, y + 58), "\u22127%", font=font(F_SANS_B, 16), fill=RED)
    elif kind == "store":
        d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
        d.rectangle([x, y, x + w, y + 26], fill=(250, 246, 238))
        for i in range(8):
            col = RED if i % 2 == 0 else PAPER
            sx = x + i * (w // 8)
            d.polygon([(sx, y + 4), (sx + w // 8, y + 4),
                       (sx + w // 8 - 3, y + 26), (sx + 3, y + 26)], fill=col)
        d.rectangle([x + 16, y + 36, x + 86, y + h - 6], fill=(120, 170, 220))
        d.rectangle([x + 16, y + 36, x + 86, y + h - 6], outline=(23, 68, 120),
                    width=2)
        d.line([(x + 51, y + 36), (x + 51, y + h - 6)], fill=(23, 68, 120),
               width=2)
        d.rectangle([x + 108, y + 36, x + 210, y + h - 6], fill=(23, 68, 120))
        d.rectangle([x + 118, y + 44, x + 150, y + h - 14], fill=(120, 170, 220))
        d.rectangle([x + 160, y + 44, x + 192, y + h - 14], fill=(120, 170, 220))
        d.ellipse([x + w - 26, y + h - 26, x + w - 2, y + h - 2], fill=GREEN,
                  outline=(255, 255, 255), width=2)
        d.text((x + w - 20, y + h - 23), "\u2713", font=font(F_SANS_B, 15),
               fill=(255, 255, 255))
    elif kind == "rocket":
        d.rectangle([x, y, x + w, y + h], fill=(12, 20, 40))
        for sx, sy in [(x + 30, y + 16), (x + 90, y + 30), (x + 180, y + 14),
                       (x + 210, y + 60), (x + 50, y + 62)]:
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
        bx, by = x + 105, y + 14
        d.polygon([(bx, by), (bx - 12, by + 26), (bx + 12, by + 26)], fill=RED)
        d.rectangle([bx - 12, by + 26, bx + 12, by + 58], fill=(240, 240, 240))
        d.polygon([(bx - 12, by + 40), (bx - 26, by + 58), (bx - 12, by + 58)],
                  fill=RED)
        d.polygon([(bx + 12, by + 40), (bx + 26, by + 58), (bx + 12, by + 58)],
                  fill=RED)
        d.polygon([(bx - 6, by + 58), (bx + 6, by + 58), (bx, by + 74)],
                  fill=(255, 176, 32))
        d.ellipse([x + 150, y + 44, x + 206, y + 72], outline=(120, 170, 220),
                  width=3)


def main():
    counts_field = {}
    counts_region = {}
    for s in ALL:
        counts_field[s["field"]] = counts_field.get(s["field"], 0) + 1
        counts_region[s["region"]] = counts_region.get(s["region"], 0) + 1
    n_stories = len(ALL)
    n_regions = len(counts_region)
    n_fields = len(counts_field)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 28
    CW = W - 2 * MX

    # ---- masthead
    hero = draw_hero()
    img.paste(hero.resize((76, 76)), (W - MX - 76, 14))
    d.text((MX, 16), "THE WORLD IN ONE DAY", font=font(F_SERIF, 40), fill=INK)
    sub = (f"WEDNESDAY \u00b7 25 NOVEMBER 2026 \u00b7 {n_stories} STORIES \u00b7 "
           f"{n_regions} REGIONS \u00b7 {n_fields} FIELDS")
    d.text((MX, 70), sub, font=font(F_SANS_SB, 13), fill=RED)
    d.line([(MX, 96), (W - MX, 96)], fill=INK, width=2)
    d.line([(MX, 100), (W - MX, 100)], fill=RULE, width=1)

    # ---- leads: 4 across
    gap = 12
    col_w = (CW - 3 * gap) // 4
    ly = 108
    for i, s in enumerate(LEADS):
        x = MX + i * (col_w + gap)
        d.text((x, ly), s["kick"], font=font(F_SANS_B, 9), fill=RED)
        ay = ly + 14
        draw_art(d, s["art"], x, ay, col_w, 76)
        hy = ay + 82
        for j, ln in enumerate(wrap(d, s["head"], font(F_SERIF, 15), col_w)):
            d.text((x, hy + j * 18), ln, font=font(F_SERIF, 15), fill=INK)
        by = hy + 2 * 18 + 4
        for j, ln in enumerate(wrap(d, s["body"], font(F_SANS, 10), col_w)):
            d.text((x, by + j * 13), ln, font=font(F_SANS, 10), fill=(60, 55, 48))
        ty = by + 3 * 13 + 4
        d.text((x, ty), s["src"] + "  \u00b7  " + s["conf"],
               font=font(F_SANS_B, 9),
               fill=CONF_STYLE[s["conf"]][0])
        if i < 3:
            d.line([(x + col_w + 6, ly), (x + col_w + 6, ly + 182)],
                   fill=RULE, width=1)

    # ---- by field bar
    fy = 306
    d.line([(MX, fy), (W - MX, fy)], fill=INK, width=1)
    d.text((MX, fy + 7), "BY FIELD", font=font(F_SANS_B, 10), fill=RED)
    fx = MX + 72
    fnt_f = font(F_SANS, 10)
    order = sorted(counts_field.items(), key=lambda kv: (-kv[1], kv[0]))
    line_y = fy + 7
    for name, cnt in order:
        piece = f"{name} {cnt}"
        pw = d.textlength(piece + "   ", font=fnt_f)
        if fx + pw > W - MX:
            fx = MX + 72
            line_y += 14
        d.text((fx, line_y), piece, font=fnt_f, fill=INK)
        fx += pw

    # ---- grid header + 12 stories
    gy = 342
    d.text((MX, gy), "THE DAY IN BRIEF \u2014 12 MORE",
           font=font(F_SANS_B, 11), fill=INK)
    d.line([(MX, gy + 16), (W - MX, gy + 16)], fill=RULE, width=1)
    gw = (CW - 5 * 10) // 6
    gh, grof = 116, 8
    gy0 = gy + 24
    for i, s in enumerate(GRID):
        r, c = divmod(i, 6)
        x = MX + c * (gw + 10)
        y = gy0 + r * (gh + grof)
        d.text((x, y), s["field"].upper(), font=font(F_SANS_B, 8), fill=RED)
        lines = wrap(d, s["head"], font(F_SANS_B, 11), gw)
        for j, ln in enumerate(lines[:3]):
            d.text((x, y + 12 + j * 13), ln, font=font(F_SANS_B, 11), fill=INK)
        my = y + 12 + min(len(lines), 3) * 13 + 4
        d.text((x, my), s["src"], font=font(F_SANS_M, 8), fill=MUTED)
        conf_tag(d, x, my + 11, s["conf"])
        if c < 5:
            d.line([(x + gw + 5, y), (x + gw + 5, y + gh)], fill=RULE, width=1)

    # ---- ALSO section: 3 columns x 10/9/9
    ay0 = 610
    d.text((MX, ay0), "ALSO ON WEDNESDAY \u2014 28 MORE",
           font=font(F_SANS_B, 11), fill=INK)
    d.line([(MX, ay0 + 16), (W - MX, ay0 + 16)], fill=RULE, width=1)
    cols = [ALSO[0:10], ALSO[10:19], ALSO[19:28]]
    aw = (CW - 2 * 16) // 3
    fnt_a = font(F_SANS, 10)
    ay = ay0 + 24
    for ci, col in enumerate(cols):
        x = MX + ci * (aw + 16)
        for ri, (fld, reg, txt) in enumerate(col):
            yy = ay + ri * 21
            num = str(ci * 10 + ri + 1) if ci < 2 else str(19 + ri + 1)
            d.text((x, yy), num + ".", font=font(F_SANS_B, 10), fill=RED)
            d.text((x + 24, yy), txt, font=fnt_a, fill=INK)
        if ci < 2:
            d.line([(x + aw + 8, ay), (x + aw + 8, ay + 10 * 21)],
                   fill=RULE, width=1)

    # ---- timeline strip
    ty0 = 842
    d.line([(MX, ty0), (W - MX, ty0)], fill=INK, width=1)
    d.text((MX, ty0 + 6), "THE DAY IN FIVE BEATS",
           font=font(F_SANS_B, 10), fill=RED)
    tw = CW // 5
    for i, (part, beat) in enumerate(TIMELINE):
        x = MX + i * tw
        d.text((x, ty0 + 22), part, font=font(F_SANS_B, 10), fill=INK)
        for j, ln in enumerate(wrap(d, beat, font(F_SANS, 10), tw - 12)):
            d.text((x, ty0 + 36 + j * 13), ln, font=font(F_SANS, 10),
                   fill=(60, 55, 48))
        if i < 4:
            d.line([(x + tw - 6, ty0 + 22), (x + tw - 6, ty0 + 62)],
                   fill=RULE, width=1)

    # ---- bottom: map (left) + date check (right)
    by0 = 910
    d.line([(MX, by0), (W - MX, by0)], fill=INK, width=1)
    d.text((MX, by0 + 6), "WHERE IT HAPPENED",
           font=font(F_SANS_B, 10), fill=RED)
    map_x, map_y, map_w, map_h = MX, by0 + 22, 360, 66
    lat_top, lat_bot = 78, -58

    def proj(lon, lat):
        px = map_x + (lon + 180) / 360 * map_w
        py = map_y + (lat_top - lat) / (lat_top - lat_bot) * map_h
        return px, py

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(196, 214, 196),
                  outline=(120, 140, 120))
    for lon, lat, num in PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        fnum = font(F_SANS_B, 8)
        twd = d.textlength(num, font=fnum)
        d.text((px - twd / 2, py - 5), num, font=fnum, fill=(255, 255, 255))
    d.text((MX, by0 + 92), PIN_LEGEND, font=font(F_SANS, 8), fill=MUTED)

    dx = MX + 392
    d.text((dx, by0 + 6), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHY",
           font=font(F_SANS_B, 10), fill=RED)
    for i, line in enumerate(DATE_CHECK):
        yy = by0 + 24 + i * 14
        d.text((dx, yy), "\u2715", font=font(F_SANS_B, 9), fill=RED)
        d.text((dx + 14, yy), line, font=font(F_SANS, 9), fill=(60, 55, 48))

    # ---- footer
    d.text((MX, 1014),
           "Sources: Reuters \u00b7 BBC \u00b7 The Guardian \u00b7 CNN \u00b7 WSJ \u00b7 The Hindu \u00b7 "
           "UEFA \u00b7 One Turn \u00b7 Horizon \u00b7 The Daily Edition \u2014 25 Nov 2026 editions. "
           "Drawn by program; no photograph reproduced.",
           font=font(F_SANS, 8), fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    hero.save(os.path.join(HERE, "assets", "hero.png"), "PNG", optimize=True)
    print(f"stories={n_stories} regions={n_regions} fields={n_fields}")
    print("fields:", dict(sorted(counts_field.items(),
                                 key=lambda kv: -kv[1])))
    print("regions:", counts_region)
    print("entry.png bytes:", os.path.getsize(out))
    print("hero.png bytes:",
          os.path.getsize(os.path.join(HERE, "assets", "hero.png")))


if __name__ == "__main__":
    main()
