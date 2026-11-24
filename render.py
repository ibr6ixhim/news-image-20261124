#!/usr/bin/env python3
"""Render the news-image-20261124 front page: one image summing up the
world news of Tuesday 24 November 2026.

Draws a dense newspaper front page (1024x1024 PNG) with PIL only:
banner, masthead, deck, region chips, UTC timeline, numbers strip,
3 illustrated heroes, a 10-story grid, a 25-story ALSO list, a world
map with pins, a DATE CHECK box and a legend. Deterministic: same
input always writes the same bytes (fixed fonts, fixed layout, no
timestamps, no randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 22
CW = W - 2 * MARGIN  # 980

CREAM = (245, 239, 226)
NAVY = (27, 42, 74)
NAVY_LIGHT = (36, 54, 94)
RED = (139, 30, 30)
INK = (26, 26, 26)
MUTED = (90, 83, 72)
RULE = (180, 172, 156)
WHITE = (255, 255, 255)
SEA = (64, 110, 150)
SKY = (214, 228, 238)

REGION_COLORS = {
    "AMERICA": (43, 108, 176),
    "EUROPE": (47, 133, 90),
    "ASIA": (192, 86, 33),
    "MIDDLE EAST": (107, 70, 193),
    "AFRICA": (141, 90, 43),
    "OCEANIA": (15, 118, 110),
    "LATIN AMERICA": (179, 64, 42),
}
REGION_SHORT = {
    "AMERICA": "AM", "EUROPE": "EU", "ASIA": "AS", "MIDDLE EAST": "ME",
    "AFRICA": "AF", "OCEANIA": "OC", "LATIN AMERICA": "LA",
    "SCIENCE": "SC",
}
TAG_COLORS = {
    "CONFIRMED": (47, 133, 90),
    "REPORTED": (43, 108, 176),
    "CLAIM": (192, 86, 33),
    "OFFICIAL": (27, 42, 74),
    "ONGOING": (107, 70, 193),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def wrap(draw, text, f, max_w):
    """Wrap text to a list of lines fitting max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_tag(draw, x, y, tag, size=9):
    """Draw a small filled tag chip; returns its right edge."""
    f = SANS_B(size)
    w = int(draw.textlength(tag, font=f)) + 10
    h = size + 7
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3,
                           fill=TAG_COLORS[tag])
    draw.text((x + 5, y + 3), tag, font=f, fill=WHITE)
    return x + w


def hline(draw, y, color=RULE, width=1, x0=None, x1=None):
    draw.line([(x0 if x0 is not None else MARGIN, y),
               (x1 if x1 is not None else W - MARGIN, y)],
              fill=color, width=width)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    y = 0

    # ---------- Banner ----------
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((MARGIN, 6), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=WHITE)
    right = "38 STORIES  ·  7 REGIONS  ·  TUESDAY 24 NOVEMBER 2026"
    d.text((W - MARGIN - d.textlength(right, font=SANS_B(12)), 7),
           right, font=SANS_B(12), fill=(200, 210, 230))
    y = 26

    # ---------- Masthead ----------
    head = "TUESDAY 24 NOVEMBER 2026"
    hf = SERIF_B(40)
    d.text(((W - d.textlength(head, font=hf)) / 2, y + 4),
           head, font=hf, fill=NAVY)
    sub = "Summing up the day's world news — every story happened or was first reported today"
    sf = SERIF(12)
    d.text(((W - d.textlength(sub, font=sf)) / 2, y + 44),
           sub, font=sf, fill=MUTED)
    y += 60
    hline(d, y, color=NAVY, width=2)
    y += 6

    # ---------- Deck (3 hero lines, red serif) ----------
    deck = [
        "Iran says four tankers hit mines in the Strait of Hormuz",
        "Houthis strike Riyadh's tallest tower again; 11 injured",
        "Nvidia gives back 7% Tuesday after Monday's 31% surge",
    ]
    df = SERIF(14)
    for line in deck:
        d.text(((W - d.textlength(line, font=df)) / 2, y),
               line, font=df, fill=RED)
        y += 16
    y += 2

    # ---------- Region chips ----------
    chips = [("AMERICA", 5), ("EUROPE", 10), ("ASIA", 7),
             ("MIDDLE EAST", 7), ("AFRICA", 3), ("OCEANIA", 2),
             ("LATIN AMERICA", 4)]
    cf = SANS_B(10)
    total_w = sum(int(d.textlength(f"{n} {c}", font=cf)) + 16
                  for n, c in chips) + 6 * 8
    x = (W - total_w) / 2
    for name, count in chips:
        label = f"{name} {count}"
        w = int(d.textlength(label, font=cf)) + 16
        d.rounded_rectangle([x, y, x + w, y + 20], radius=4,
                            fill=REGION_COLORS[name])
        d.text((x + 8, y + 5), label, font=cf, fill=WHITE)
        x += w + 8
    y += 26

    # ---------- Timeline ----------
    d.text((MARGIN, y), "THE DAY · UTC", font=SANS_B(10), fill=NAVY)
    tl = [("00:00", "Hormuz mines"), ("01:04", "Korea ADIZ"),
          ("05:54", "Malaysia returns"), ("08:16", "Hanoi blast"),
          ("11:40", "Hamas chief killed"), ("12:55", "UK sanctions"),
          ("15:47", "CAS: Senegal"), ("17:00", "Trump tariffs")]
    tf = SANS_B(10)
    lf = SANS(9)
    x0, x1 = 150, W - MARGIN
    step = (x1 - x0) / (len(tl) - 1)
    d.line([(x0, y + 8), (x1, y + 8)], fill=RULE, width=1)
    for i, (t, label) in enumerate(tl):
        cx = x0 + i * step
        d.ellipse([cx - 3, y + 5, cx + 3, y + 11], fill=NAVY)
        tw = d.textlength(t, font=tf)
        d.text((cx - tw / 2, y + 13), t, font=tf, fill=INK)
        lw = d.textlength(label, font=lf)
        lx = min(max(cx - lw / 2, x0), x1 - lw)
        d.text((lx, y + 24), label, font=lf, fill=MUTED)
    y += 38

    # ---------- The day in numbers ----------
    d.text((MARGIN, y), "THE DAY IN NUMBERS", font=SANS_B(10), fill=NAVY)
    d.text((W - MARGIN - d.textlength("*RFE/RL analysis of Russian deaths",
                                      font=SANS(8)), y + 1),
           "*RFE/RL analysis of Russian deaths", font=SANS(8), fill=MUTED)
    y += 15
    nums = [
        ("4", "TANKERS HIT IN HORMUZ"),
        ("11", "INJURED IN RIYADH"),
        ("-7%", "NVIDIA ON TUESDAY"),
        ("23", "INJURED IN COLOMBIA"),
        ("25", "KILLED/MISSING IN YEMEN"),
        ("96", "DRONES AT UKRAINE"),
        ("700,000+", "RUSSIAN TROOPS KILLED*"),
    ]
    col_w = CW / len(nums)
    nf = SERIF_B(24)
    nlf = SANS_B(8)
    for i, (num, label) in enumerate(nums):
        cx = MARGIN + i * col_w
        if i:
            d.line([(cx - 4, y), (cx - 4, y + 34)], fill=RULE, width=1)
        d.text((cx + 4, y), num, font=nf, fill=RED)
        for j, ln in enumerate(wrap(d, label, nlf, col_w - 12)):
            d.text((cx + 4, y + 26 + j * 9), ln, font=nlf, fill=INK)
    y += 40
    hline(d, y, color=NAVY, width=2)
    y += 6

    return img, d, y


def draw_hormuz(d, x, y, w, h):
    """Tanker on a narrow strait with sea mines; stamp '4 TANKERS'."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # cliffs of the strait
    d.polygon([(x, y), (x + 26, y), (x + 14, y + h), (x, y + h)],
              fill=(120, 110, 92))
    d.polygon([(x + w, y), (x + w - 26, y), (x + w - 14, y + h),
               (x + w, y + h)], fill=(120, 110, 92))
    # sea
    d.rectangle([x + 14, y + h - 26, x + w - 14, y + h], fill=SEA)
    # tanker hull + containers
    d.rectangle([x + 34, y + h - 34, x + w - 34, y + h - 22], fill=(60, 60, 66))
    d.rectangle([x + 44, y + h - 44, x + w - 44, y + h - 34], fill=RED)
    d.rectangle([x + 52, y + h - 52, x + 64, y + h - 44], fill=(200, 200, 200))
    d.rectangle([x + 70, y + h - 52, x + 82, y + h - 44], fill=(230, 200, 120))
    # mines: spiked circles
    for mx, my in [(x + 30, y + 16), (x + w - 34, y + 12), (x + w - 58, y + 22)]:
        for dx, dy in [(0, -6), (0, 6), (-6, 0), (6, 0),
                       (-4, -4), (4, -4), (-4, 4), (4, 4)]:
            d.line([(mx, my), (mx + dx, my + dy)], fill=INK, width=2)
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=INK)
    # stamp
    sf = SANS_B(10)
    label = "4 TANKERS"
    sw = int(d.textlength(label, font=sf)) + 10
    d.rectangle([x + w - sw - 4, y + h - 18, x + w - 4, y + h - 6],
                outline=RED, width=2)
    d.text((x + w - sw + 1, y + h - 17), label, font=sf, fill=RED)


def draw_riyadh(d, x, y, w, h):
    """PIF Tower: tall skyscraper with a damage burst mid-facade."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # small skyline
    for bx, bh in [(x + 6, 22), (x + 118, 30), (x + 128, 18)]:
        d.rectangle([bx, y + h - bh, bx + 12, y + h], fill=(150, 160, 175))
    # tower
    tx, tw = x + 52, 44
    d.rectangle([tx, y + 4, tx + tw, y + h], fill=NAVY)
    d.polygon([(tx, y + 4), (tx + tw // 2, y - 2), (tx + tw, y + 4)],
              fill=NAVY_LIGHT)
    for row in range(6):
        for col in range(3):
            wx = tx + 6 + col * 14
            wy = y + 12 + row * 9
            d.rectangle([wx, wy, wx + 8, wy + 5], fill=(180, 200, 220))
    # damage burst
    cx, cy = tx + tw // 2, y + 34
    for ang in range(0, 360, 30):
        import math
        r = 14
        ex = cx + r * math.cos(math.radians(ang))
        ey = cy + r * math.sin(math.radians(ang))
        d.line([(cx, cy), (ex, ey)], fill=(230, 120, 40), width=2)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(230, 120, 40))
    # stamp
    sf = SANS_B(9)
    for j, ln in enumerate(["2ND TIME", "IN 5 DAYS"]):
        lw = int(d.textlength(ln, font=sf)) + 8
        d.rectangle([x + w - lw - 4, y + h - 26 + j * 11,
                     x + w - 4, y + h - 16 + j * 11],
                    outline=RED, width=2)
        d.text((x + w - lw + 0, y + h - 26 + j * 11), ln, font=sf, fill=RED)


def draw_nvidia(d, x, y, w, h):
    """Stock chart: steep rise then a sharp fall; big -7% label."""
    d.rectangle([x, y, x + w, y + h], fill=(235, 240, 232))
    # axes
    d.line([(x + 10, y + h - 12), (x + w - 8, y + h - 12)],
           fill=MUTED, width=1)
    d.line([(x + 10, y + 8), (x + 10, y + h - 12)], fill=MUTED, width=1)
    # chart line: rise then fall
    pts = [(x + 12, y + h - 22), (x + 34, y + h - 34), (x + 56, y + 22),
           (x + 78, y + 14), (x + 104, y + h - 26), (x + w - 12, y + h - 20)]
    d.line(pts, fill=(47, 133, 90), width=3)
    d.polygon([(x + 56, y + 22), (x + 66, y + 16), (x + 56, y + 30)],
              fill=(47, 133, 90))
    # falling arrow
    d.line([(x + 96, y + h - 44), (x + w - 16, y + h - 16)],
           fill=RED, width=3)
    d.polygon([(x + w - 16, y + h - 16), (x + w - 28, y + h - 18),
               (x + w - 18, y + h - 28)], fill=RED)
    # -7% label
    bf = SERIF_B(24)
    d.text((x + 12, y + 6), "-7%", font=bf, fill=RED)


HEROES = [
    {
        "num": "1", "loc": "STRAIT OF HORMUZ", "cat": "WAR",
        "tag": "CLAIM", "region": "MIDDLE EAST",
        "headline": "Iran says four tankers hit mines in the Strait of Hormuz",
        "summary": ("The IRGC claims three oil tankers struck sea mines and caught "
                    "fire, then a fourth — and orders the strait closed further "
                    "until Washington meets Tehran's terms."),
        "source": "Sources: dailysummaryof · wires · India Bytes",
        "art": "hormuz",
    },
    {
        "num": "2", "loc": "RIYADH, SAUDI ARABIA", "cat": "WAR",
        "tag": "CONFIRMED", "region": "MIDDLE EAST",
        "headline": "Houthis strike Riyadh's tallest tower again; 11 injured",
        "summary": ("A projectile hit the 385 m PIF Tower in the financial district — "
                    "the second strike in five days. Saudi civil defence reports "
                    "11 people injured."),
        "source": "Sources: WSJ · Reuters · Saudi Civil Defence",
        "art": "riyadh",
    },
    {
        "num": "3", "loc": "NEW YORK — MARKETS", "cat": "BUSINESS",
        "tag": "CONFIRMED", "region": "AMERICA",
        "headline": "Nvidia gives back ~7% Tuesday after Monday's +31% surge",
        "summary": ("Shares fell about 7% as investors took profits after Monday's "
                    "record jump on Huang's return as CEO. The Nasdaq slid 2.2% "
                    "by midday."),
        "source": "Sources: Finnhub · Motley Fool · Reuters",
        "art": "nvidia",
    },
]

ART = {"hormuz": draw_hormuz, "riyadh": draw_riyadh, "nvidia": draw_nvidia}


def draw_heroes(d, y):
    """Three hero rows, each 68 px tall with a 150 px illustration."""
    hero_h = 68
    art_w = 150
    for hero in HEROES:
        d.rectangle([MARGIN, y, MARGIN + art_w, y + hero_h],
                    outline=RULE, width=1)
        ART[hero["art"]](d, MARGIN + 1, y + 1, art_w - 2, hero_h - 2)
        tx = MARGIN + art_w + 10
        tw = W - MARGIN - tx
        # kicker line
        kf = SANS_B(10)
        kicker = f"{hero['num']} · {hero['loc']} — {hero['cat']}"
        d.text((tx, y + 2), kicker, font=kf, fill=REGION_COLORS[hero["region"]])
        draw_tag(d, W - MARGIN - 74, y + 1, hero["tag"], size=9)
        # headline (serif bold, 1 line)
        hf = SERIF_B(16)
        d.text((tx, y + 15), hero["headline"], font=hf, fill=INK)
        # summary (2 lines max)
        sf = SANS(11)
        lines = wrap(d, hero["summary"], sf, tw)[:2]
        for j, ln in enumerate(lines):
            d.text((tx, y + 34 + j * 13), ln, font=sf, fill=(50, 48, 44))
        # source line
        d.text((tx, y + 59), hero["source"], font=SANS(9), fill=MUTED)
        y += hero_h + 4
    return y - 4

GRID = [
    ("MIDDLE EAST", "Hamas chief killed in Gaza strike", "CONFIRMED",
     "Israel kills Hamas internal security chief Naeem Abu Nahel, two months "
     "in the job, despite the ceasefire. — Gaza ministry · IDF"),
    ("EUROPE", "Russian attack on Zaporizhzhia kills 2, wounds 22+", "CONFIRMED",
     "A night strike hit a 5-storey block in the Kosmichnyi district; "
     "children among the wounded. — Kyiv Independent"),
    ("AMERICA", "Trump to unveil new tariffs: China up to 20%", "REPORTED",
     "USTR Greer to announce Section 301 findings as soon as Tuesday night; "
     "the EU capped near 15%. — WSJ"),
    ("ASIA", "China probes Politburo member Chen Jining", "CONFIRMED",
     "The Shanghai party chief faces a corruption probe — the fourth "
     "Politburo member investigated in a year. — Xinhua · NYT"),
    ("AFRICA", "CAS restores Senegal as AFCON champions", "CONFIRMED",
     "The sports court overturns CAF's ruling: Senegal keep the 2025 title "
     "won 1–0 over Morocco. — TSN · AP"),
    ("EUROPE", "Ukraine hits Kerch Bridge again", "REPORTED",
     "Road and rail spans damaged; Moscow's mayor reports hundreds of drones "
     "intercepted over the capital. — wires"),
    ("EUROPE", "Abu Dhabi talks end with no breakthrough", "REPORTED",
     "Two days of trilateral talks stall; US envoys head to Moscow, then "
     "Dublin to meet Zelenskyy. — NBC"),
    ("EUROPE", "UK sanctions Houthis + 4 senior officials", "OFFICIAL",
     "Asset freezes and travel bans over rights abuses and attacks in the "
     "Bab al-Mandeb strait. — UK government"),
    ("LATIN AMERICA", "Car bomb in Villavicencio, Colombia injures 23", "CONFIRMED",
     "The blast outside regional government offices is blamed on "
     "'narcoterrorism' by the president. — wires"),
    ("MIDDLE EAST", "Iraq orders federal control of Kurdish oilfields", "OFFICIAL",
     "Baghdad moves to run fields in four provinces; the Kurdish PM calls it "
     "'completely unacceptable'. — Reuters"),
]

ALSO = [
    ("AMERICA", "US blacklists Megaspeed over Nvidia scandal", "REPORTED"),
    ("AMERICA", "Oregon & Virginia sue SpaceX over Grok CSAM images", "REPORTED"),
    ("AMERICA", "Pentagon delays ~60 Patriot interceptors for Ukraine", "REPORTED"),
    ("EUROPE", "96 drones launched at Ukraine overnight; 73 downed", "CONFIRMED"),
    ("EUROPE", "Dymer toll rises to 12 as rescued woman dies", "CONFIRMED"),
    ("EUROPE", "Hungary's Magyar meets Zelensky in Uzhhorod", "OFFICIAL"),
    ("EUROPE", "Moldova: 7 Russian drones entered its airspace", "OFFICIAL"),
    ("EUROPE", "Russia warns Estonia over border crossing closures", "CLAIM"),
    ("EUROPE", "Putin admits pressure on oil market", "REPORTED"),
    ("ASIA", "Russian jets enter South Korea's air defence zone", "OFFICIAL"),
    ("ASIA", "S. Korea offers $375,000 bounty for AI exam cheats", "OFFICIAL"),
    ("ASIA", "Hanoi hot pot blast kills at least 6", "REPORTED"),
    ("ASIA", "Malaysia to repatriate thousands to Myanmar", "OFFICIAL"),
    ("ASIA", "Indonesia names two candidates to replace VP Gibran", "OFFICIAL"),
    ("ASIA", "Shenzhou 24 crew named; Pakistani astronaut first", "CONFIRMED"),
    ("MIDDLE EAST", "Saudi strikes in Yemen: 25 killed or missing", "REPORTED"),
    ("MIDDLE EAST", "Gaza meningitis warning: 272 cases in October", "OFFICIAL"),
    ("MIDDLE EAST", "Haftar visits Turkey for the first time", "OFFICIAL"),
    ("AFRICA", "Ebola fight in Ituri, DRC: 11,000+ cases", "REPORTED"),
    ("AFRICA", "Bayelsa boat toll rises to 29", "REPORTED"),
    ("OCEANIA", "PNG parliament votes on Bougainville independence", "REPORTED"),
    ("OCEANIA", "Severe heatwave in Cape York, Queensland", "REPORTED"),
    ("LATIN AMERICA", "Mexico: 4 soldiers, 7 gunmen killed in Sinaloa raid", "OFFICIAL"),
    ("LATIN AMERICA", "Brazil cuts 2027 growth forecast to 1.8%", "OFFICIAL"),
    ("LATIN AMERICA", "Argentina asks Congress to delay PASO primaries", "REPORTED"),
]

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 72), (-60, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26),
     (-90, 20), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-165, 60)],
    # Greenland
    [(-58, 64), (-45, 60), (-40, 70), (-55, 76), (-65, 74)],
    # South America
    [(-80, 10), (-70, 12), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-50, -30), (-60, -38), (-70, -50), (-75, -40),
     (-75, -25), (-80, -15), (-80, 5)],
    # Europe
    [(-10, 36), (-5, 44), (0, 50), (5, 55), (10, 58), (20, 60), (30, 70),
     (40, 68), (30, 60), (25, 55), (20, 45), (15, 40), (10, 38), (0, 38),
     (-5, 36)],
    # Africa
    [(-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
     (50, 10), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35),
     (15, -30), (10, -20), (8, -5), (0, 5), (-10, 15), (-15, 25)],
    # Asia
    [(40, 70), (60, 72), (90, 75), (120, 73), (150, 70), (170, 66),
     (180, 65), (160, 60), (140, 55), (130, 45), (120, 35), (110, 20),
     (105, 10), (100, 8), (90, 15), (80, 10), (75, 20), (70, 25),
     (60, 25), (50, 30), (45, 30), (40, 35)],
    # Australia
    [(113, -22), (120, -15), (130, -12), (140, -15), (150, -20),
     (150, -28), (145, -38), (135, -35), (125, -32), (115, -30)],
]

PINS = [  # (lon, lat, number or None)
    (56, 26, "1"), (46.7, 24.6, "2"), (-122, 37.4, "3"),
    (34.5, 31.5, None), (35.2, 47.8, None), (36.5, 45.3, None),
    (54.4, 24.5, None), (-0.1, 51.5, None), (-73.6, 4.15, None),
    (44.4, 33.3, None), (116.4, 39.9, None), (-17.4, 14.7, None),
    (105.8, 21, None), (101.7, 3.1, None), (106.8, -6.2, None),
    (15.3, -4.3, None), (6.3, 4.9, None), (147.2, -9.5, None),
    (153, -27.5, None), (-99.1, 19.4, None), (-47.9, -15.8, None),
    (-58.4, -34.6, None), (127, 37.5, None), (22.3, 48.6, None),
    (28.8, 47, None), (24.7, 59.4, None), (37.6, 55.8, None),
    (77.2, 28.6, None), (51.4, 35.7, None), (45, 12.8, None),
    (32.9, 39.9, None), (45.3, 2.05, None), (20.1, 32.1, None),
    (32.5, 15.6, None), (44.2, 15.3, None),
]


def draw_grid(d, y):
    d.text((MARGIN, y), "MORE OF THE DAY", font=SANS_B(11), fill=NAVY)
    y += 16
    row_h, col_w, gap = 44, 482, 16
    hf, sf = SANS_B(12), SANS(10)
    for i, (region, headline, tag, summary) in enumerate(GRID):
        col, row = i % 2, i // 2
        x = MARGIN + col * (col_w + gap)
        cy = y + row * row_h
        d.rectangle([x, cy + 2, x + 3, cy + row_h - 4],
                    fill=REGION_COLORS[region])
        d.text((x + 8, cy + 1), headline, font=hf, fill=INK)
        tw = int(d.textlength(tag, font=SANS_B(8))) + 10
        d.rounded_rectangle([x + col_w - tw, cy + 1,
                             x + col_w, cy + 12], radius=3,
                            fill=TAG_COLORS[tag])
        d.text((x + col_w - tw + 5, cy + 3), tag, font=SANS_B(8), fill=WHITE)
        lines = wrap(d, summary, sf, col_w - 10)[:2]
        for j, ln in enumerate(lines):
            d.text((x + 8, cy + 16 + j * 11), ln, font=sf, fill=(50, 48, 44))
    return y + 5 * row_h


def draw_also(d, y):
    d.text((MARGIN, y), "ALSO ON TUESDAY 24 NOVEMBER",
           font=SANS_B(11), fill=NAVY)
    y += 15
    row_h, col_w, gap = 12, 482, 16
    hf, cf, tf = SANS(11), SANS_B(10), SANS_B(8)
    half = 13
    for i, (region, headline, tag) in enumerate(ALSO):
        col, row = (0, i) if i < half else (1, i - half)
        x = MARGIN + col * (col_w + gap)
        cy = y + row * row_h
        code = REGION_SHORT[region]
        d.text((x, cy), code, font=cf, fill=REGION_COLORS[region])
        d.text((x + 24, cy), headline, font=hf, fill=INK)
        tw = d.textlength(tag, font=tf)
        d.text((x + col_w - tw, cy + 1), tag, font=tf,
               fill=TAG_COLORS[tag])
    return y + half * row_h


def draw_map(d, y):
    d.text((MARGIN, y), "WHERE IT HAPPENED — pins 1–3 are the heroes",
           font=SANS_B(10), fill=NAVY)
    y += 13
    map_h = 52
    d.rectangle([MARGIN, y, W - MARGIN, y + map_h], fill=(232, 226, 210))

    def px(lon, lat):
        cx = MARGIN + (lon + 180) / 360 * CW
        cy = y + (72 - lat) / 114 * map_h
        return (cx, min(max(cy, y), y + map_h))

    for poly in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in poly], fill=NAVY)
    for lon, lat, num in PINS:
        cx, cy = px(lon, lat)
        if num:
            d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                      outline=WHITE, width=1)
            nf = SANS_B(10)
            d.text((cx - d.textlength(num, font=nf) / 2, cy - 7),
                   num, font=nf, fill=WHITE)
        else:
            d.ellipse([cx - 2.5, cy - 2.5, cx + 2.5, cy + 2.5], fill=RED)
    return y + map_h


def draw_datecheck(d, y):
    body = ("DATE CHECK — WHAT WE LEFT OUT, AND WHY: The ICJ's Myanmar "
            "genocide verdict was 19 Nov, not 24 Nov. COP31 collapsed "
            "without a deal on 22 Nov. Puigdemont's amnesty was 23 Nov. "
            "The Merkury sinking was Sunday; Tuesday's news is the "
            "follow-up. Monday night's NBA results belong to 23 Nov.")
    bf = SANS(11)
    lines = wrap(d, body, bf, CW - 20)
    h = 6 + len(lines) * 13 + 6
    d.rectangle([MARGIN, y, W - MARGIN, y + h], outline=RED, width=2)
    for j, ln in enumerate(lines):
        d.text((MARGIN + 10, y + 5 + j * 13), ln, font=bf, fill=INK)
    return y + h


def draw_footer(d, y):
    f1 = ("CONFIRMED = reported by two or more outlets  ·  OFFICIAL = on the "
          "record  ·  REPORTED = named wires  ·  CLAIM = one side only")
    f2 = ("Sources: AP, Reuters, WSJ, BBC, Al Jazeera, Kyiv Independent, TSN, "
          "Motley Fool, Finnhub. All events happened or were first reported on "
          "Tuesday 24 November 2026, any time zone.")
    for j, ln in enumerate([f1, f2]):
        f = SANS(9)
        d.text(((W - d.textlength(ln, font=f)) / 2, y + j * 12),
               ln, font=f, fill=MUTED)
    return y + 23


def build():
    img, d, y = main()
    y = draw_heroes(d, y)
    y = draw_grid(d, y)
    y = draw_also(d, y)
    y += 4
    y = draw_map(d, y)
    y += 4
    y = draw_datecheck(d, y)
    y += 4
    y = draw_footer(d, y)
    assert y <= H, f"layout overflow: final y={y} > {H}"
    img.save(OUT, format="PNG")
    print(f"saved {OUT} final_y={y} size={os.path.getsize(OUT)} bytes")
    return y


if __name__ == "__main__":
    build()
