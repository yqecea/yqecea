#!/usr/bin/env python3
"""Render a shader-style ASCII hero (torus knot + starfield) for the GitHub profile."""
import numpy as np, pathlib, math
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path('/home/yqecea/.hermes/profiles/yqecea/work/github-profile/assets')
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1200, 320
CELL_W, CELL_H = 6, 9

CHARS = np.array(list(' .:-=+*#%@'))
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
FONT_TXT = '/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf'
FONT_SEMI = '/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf'
FONT_TC = '/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf'

TEXT_X, TEXT_Y = 48, 0
ART_X0, ART_X1 = 566, 1168
ART_Y0, ART_Y1 = 16, 304
GW = (ART_X1 - ART_X0) // CELL_W
GH = (ART_Y1 - ART_Y0) // CELL_H


def torus_knot(n=1400, t=0.0, p=2, q=3, scale=1.0):
    u = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 2 + np.cos(q * u / p)
    x = r * np.cos(u)
    y = r * np.sin(u)
    z = np.sin(q * u / p) * 1.1
    a = t * 2 * np.pi
    # rotate around Y then X
    xr = x * np.cos(a) - z * np.sin(a)
    zr = x * np.sin(a) + z * np.cos(a)
    yr = y * np.cos(a * 0.55) - zr * np.sin(a * 0.55)
    z2 = y * np.sin(a * 0.55) + zr * np.cos(a * 0.55)
    return xr * scale, yr * scale, z2 * scale


def splat(grid, depth, xs, ys, zs):
    order = np.argsort(zs)
    for i in order:
        gx, gy = xs[i], ys[i]
        if 0 <= gx < grid.shape[1] and 0 <= gy < grid.shape[0]:
            val = np.clip((zs[i] + 3.2) / 6.4, 0, 1)
            grid[gy, gx] = max(grid[gy, gx], 0.25 + val * 0.75)
            depth[gy, gx] = zs[i]


def render_frame(t, stars, theme='dark'):
    bg = (10, 10, 12) if theme == 'dark' else (255, 255, 255)
    fg = (238, 238, 238) if theme == 'dark' else (24, 24, 24)
    muted = (150, 152, 158) if theme == 'dark' else (95, 107, 118)

    img = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(img)

    # starfield
    for (sx, sy, sa) in stars:
        c = tuple(int(v) for v in (np.array(bg) * (1 - sa) + np.array(fg) * sa))
        d.point((sx, sy), fill=c)

    grid = np.zeros((GH, GW))
    depth = np.full((GH, GW), 1e9)
    xs3, ys3, zs3 = torus_knot(t=t)
    span = 5.6
    gx = ((xs3 / span + 0.5) * GW).astype(int)
    gy = ((ys3 / span + 0.5) * GH).astype(int)
    splat(grid, depth, gx, gy, zs3)

    font = ImageFont.truetype(MONO, CELL_H + 2)
    for row in range(GH):
        for col in range(GW):
            v = grid[row, col]
            if v <= 0:
                continue
            ch = CHARS[min(len(CHARS) - 1, int(v * (len(CHARS) - 1)))]
            if ch == ' ':
                continue
            a = 0.25 + 0.75 * v
            c = tuple(int(f * a + b * (1 - a)) for f, b in zip(fg, bg))
            d.text((ART_X0 + col * CELL_W, ART_Y0 + row * CELL_H - 2), ch, font=font, fill=c)

    # text block
    f_name = ImageFont.truetype(FONT_SEMI, 44)
    f_tag = ImageFont.truetype(FONT_TXT, 16)
    f_meta = ImageFont.truetype(FONT_TXT, 13)
    d.text((TEXT_X, 74), 'Yusuf Kabiden', font=f_name, fill=fg)
    d.text((TEXT_X, 140), 'Frontend engineer and product designer.', font=f_tag, fill=muted)
    d.text((TEXT_X, 162), 'I ship interfaces and prove them.', font=f_tag, fill=muted)
    d.text((TEXT_X, 196), 'Astana, Kazakhstan · UTC+5', font=f_meta, fill=muted)

    # stats at bottom left
    f_num = ImageFont.truetype(FONT_SEMI, 22)
    f_lab = ImageFont.truetype(FONT_TXT, 9)
    x = TEXT_X
    for num, lab in (('113', 'TESTS FOR OYKASPI'), ('12', 'COMMITS IN TASTECODE'), ('4', 'PRODUCTS SHIPPED')):
        d.text((x, 236), num, font=f_num, fill=fg)
        d.text((x, 264), lab, font=f_lab, fill=muted)
        x += 148
    return img


if __name__ == '__main__':
    rng = np.random.default_rng(7)
    stars = [(int(rng.integers(ART_X0, ART_X1)), int(rng.integers(ART_Y0, ART_Y1)), float(rng.uniform(0.05, 0.35)))
             for _ in range(260)]
    img = render_frame(0.0, stars, 'dark')
    img.save('/tmp/hero_frame.png')
    print('frame ok')
