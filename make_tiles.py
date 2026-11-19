#!/usr/bin/env python3
"""Project tiles in the same dot-language as the hero: dark card, dotted motif, crisp type."""
import pathlib, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path('/home/yqecea/.hermes/profiles/yqecea/work/github-profile/assets')
W, H = 380, 152
F_TXT = '/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf'
F_SEMI = '/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf'

BG = (11, 11, 13)
BORDER = (38, 38, 42)
FG = (238, 238, 240)
MUTED = (150, 153, 160)
DOT = (214, 210, 202)


def dots(d, pts, r=1.15, alpha=1.0):
    for (x, y), a in pts:
        c = tuple(int(BG[i] + (DOT[i] - BG[i]) * min(1, a * alpha)) for i in range(3))
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)


def motif_bars(w, h):
    """prices stepping down to a floor"""
    pts = []
    for i, x in enumerate(range(8, w - 8, 9)):
        level = h - 10 - (i * 2.1) % (h - 30)
        for y in range(int(level), h - 8, 7):
            pts.append(((x, y), 0.35 + 0.5 * (y / h)))
    return pts


def motif_wave(w, h):
    pts = []
    for x in range(8, w - 8, 6):
        amp = 14 + 16 * math.sin(x * 0.03)
        yc = h / 2 + amp * math.sin(x * 0.09)
        pts.append(((x, yc), 0.9))
        pts.append(((x, yc + 6), 0.35))
    return pts


def motif_grid(w, h):
    pts = []
    for x in range(10, w - 10, 11):
        for y in range(10, h - 10, 11):
            band = abs(y - h * 0.42) < 12
            pts.append(((x, y), 0.95 if band else 0.3))
    return pts


def motif_branch(w, h):
    pts = []
    for x in range(10, w - 10, 5):
        y = h / 2 + 14 * math.sin(x * 0.05)
        pts.append(((x, y), 0.8))
    for bx in (w * 0.35, w * 0.6):
        for y in range(14, int(h - 14), 5):
            pts.append(((bx, y), 0.45))
    return pts


def motif_ring(w, h):
    pts = []
    cx, cy = w / 2, h / 2
    for r in range(8, 60, 5):
        n = int(2 * math.pi * r / 5)
        for k in range(n):
            a = 2 * math.pi * k / n
            pts.append(((cx + r * math.cos(a), cy + r * math.sin(a) * 0.6), 0.25 + 0.7 * (1 - r / 60)))
    return pts


def motif_mesh(w, h):
    pts = []
    for y in range(12, h - 12, 8):
        for x in range(10, w - 10, 8):
            v = math.sin(x * 0.035 + 1.2) * math.cos(y * 0.05)
            pts.append(((x, y + v * 7), 0.15 + 0.85 * (v + 1) / 2))
    return pts


TILES = [
    ('oykaspi', 'OyKaspi', 'Pricing that never crosses the margin floor.', 'TypeScript · 113 tests · 11 gates', motif_bars),
    ('oyvoice', 'OyVoice', 'Dictation that proves what it inserted.', 'Rust · TypeScript · private beta', motif_wave),
    ('mispro', 'MIS Pro', 'Government project in Tajikistan, designed end to end.', 'Design · client work', motif_grid),
    ('tastecode', 'TasteCode', '12 commits merged, plus the Linux packaging line.', 'TypeScript · open source', motif_branch),
    ('oysana', 'Oysana', 'An AI product studio: interfaces and delivery.', 'Studio · oysana-web.vercel.app', motif_ring),
    ('webgl', 'Portfolio', 'WebGL and Three.js, shaders and motion.', 'Three.js · live', motif_mesh),
]


def make(key, title, desc, meta, motif):
    S = 2
    img = Image.new('RGB', (W * S, H * S), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([1 * S, 1 * S, (W - 1) * S, (H - 1) * S], radius=13 * S, outline=BORDER, width=S)

    pts = [((x * S, y * S), a) for (x, y), a in motif(W - 4, H - 4) if x > W * 0.46 and y > 92]
    dots(d, pts, r=1.15 * S, alpha=0.85)

    # fade the motif behind text with a horizontal scrim
    scrim = Image.new('L', (W * S, H * S), 0)
    ds = ImageDraw.Draw(scrim)
    x_start = int(W * S * 0.40)
    for x in range(x_start, int(W * S * 0.62)):
        a = int(255 * (1 - (x - x_start) / (W * S * 0.22)))
        ds.line([(x, 0), (x, H * S)], fill=a)
    ds.rectangle([0, 0, x_start, H * S], fill=255)
    img = Image.composite(Image.new('RGB', img.size, BG), img, scrim)

    d = ImageDraw.Draw(img)
    d.text((18 * S, 16 * S), title, font=ImageFont.truetype(F_SEMI, 15 * S), fill=FG)
    d.text((18 * S, 42 * S), desc, font=ImageFont.truetype(F_TXT, 11 * S), fill=MUTED)
    d.text((18 * S, (H - 22) * S), meta, font=ImageFont.truetype(F_TXT, 9 * S), fill=(120, 123, 130))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == '__main__':
    for key, title, desc, meta, motif in TILES:
        make(key, title, desc, meta, motif).save(OUT / f'tile-{key}.png')
    print('tiles ok')
