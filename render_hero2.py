#!/usr/bin/env python3
"""Hero render v2: glowing ribbon torus knot + crisp type. Frames -> animated WebP."""
import numpy as np, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = pathlib.Path('/home/yqecea/.hermes/profiles/yqecea/work/github-profile/assets')
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1200, 320

F_TXT = '/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf'
F_SEMI = '/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf'

AX0, AX1, AY0, AY1 = 560, 1176, 8, 312
AW, AH = AX1 - AX0, AY1 - AY0


def knot(n=2600, t=0.0, p=2, q=3):
    u = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 2.0 + np.cos(q * u / p)
    x, y, z = r * np.cos(u), r * np.sin(u), np.sin(q * u / p) * 1.05
    a = t * 2 * np.pi
    xr = x * np.cos(a) - z * np.sin(a)
    zr = x * np.sin(a) + z * np.cos(a)
    yr = y * np.cos(a * 0.6) - zr * np.sin(a * 0.6)
    z2 = y * np.sin(a * 0.6) + zr * np.cos(a * 0.6)
    d = 5.2 + z2 * 0.9
    px = (xr / d) * AW * 1.9 + AW * 0.5
    py = (yr / d) * AH * 2.0 + AH * 0.5
    return px, py, z2


def ribbon(t):
    buf = np.zeros((AH + 8, AW + 8), dtype=np.float32)
    px, py, pz = knot(t=t)
    for i in np.argsort(pz):
        x, y = px[i] + 4, py[i] + 4
        if not (3 < x < AW + 4 and 3 < y < AH + 4):
            continue
        depth = np.clip((pz[i] + 2) / 4, 0, 1)
        inten = 0.16 + 0.84 * depth ** 1.7
        xi, yi = int(x), int(y)
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                d2 = dx * dx + dy * dy
                if d2 > 9:
                    continue
                buf[yi + dy, xi + dx] += inten * (1 - d2 / 10) ** 2 * 0.55
    return np.clip(buf[:AH, :AW], 0, 1.6)


def frame(t, theme='dark'):
    bg = np.array((9, 9, 11), np.float32) if theme == 'dark' else np.array((255, 255, 255), np.float32)
    canvas = np.ones((H, W, 3), np.float32) * bg

    rib = ribbon(t)
    a = Image.fromarray((np.clip(rib, 0, 1) * 255).astype(np.uint8))
    b1 = np.asarray(a.filter(ImageFilter.GaussianBlur(1.6)), np.float32) / 255
    b2 = np.asarray(a.filter(ImageFilter.GaussianBlur(6.0)), np.float32) / 255
    glow = np.clip(rib + b1 * 0.9 + b2 * 1.5, 0, 1)

    accent = np.array((238, 242, 248), np.float32) if theme == 'dark' else np.array((18, 18, 22), np.float32)
    region = canvas[AY0:AY1, AX0:AX1]
    for c in range(3):
        region[:, :, c] = region[:, :, c] * (1 - glow) + accent[c] * glow
    canvas[AY0:AY1, AX0:AX1] = region

    img = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    fg = (238, 238, 240) if theme == 'dark' else (16, 16, 18)
    muted = (150, 153, 160) if theme == 'dark' else (92, 102, 112)

    d.text((48, 76), 'Yusuf Kabiden', font=ImageFont.truetype(F_SEMI, 44), fill=fg)
    d.text((48, 142), 'Frontend engineer and product designer.', font=ImageFont.truetype(F_TXT, 16), fill=muted)
    d.text((48, 164), 'I ship interfaces and prove them.', font=ImageFont.truetype(F_TXT, 16), fill=muted)
    d.text((48, 198), 'Astana, Kazakhstan · UTC+5', font=ImageFont.truetype(F_TXT, 13), fill=muted)

    x = 48
    for num, lab in (('113', 'TESTS FOR OYKASPI'), ('12', 'COMMITS IN TASTECODE'), ('4', 'PRODUCTS SHIPPED')):
        d.text((x, 234), num, font=ImageFont.truetype(F_SEMI, 22), fill=fg)
        d.text((x, 262), lab, font=ImageFont.truetype(F_TXT, 9), fill=muted)
        x += 148
    return img


if __name__ == '__main__':
    frame(0.0, 'dark').save('/tmp/hero_v2.png')
    print('ok')
