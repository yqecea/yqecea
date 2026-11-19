#!/usr/bin/env python3
"""Hero v4: the initials YK built from a field of dots, drifting. Reads instantly, no ambiguous shapes."""
import numpy as np, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = pathlib.Path('/home/yqecea/.hermes/profiles/yqecea/work/github-profile/assets')
W, H = 1200, 320
F_TXT = '/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf'
F_SEMI = '/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf'
F_ART = '/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf'

AX0, AX1, AY0, AY1 = 520, 1180, 0, 320
AW, AH = AX1 - AX0, AY1 - AY0
SS = 3


def dot_field(t):
    # mask of the initials at high res
    m = Image.new('L', (AW * SS, AH * SS), 0)
    dm = ImageDraw.Draw(m)
    font = ImageFont.truetype(F_ART, int(AH * SS * 0.94))
    text = 'YK'
    bbox = dm.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # tighter optical spacing between the two letters
    x0 = (AW * SS - tw) / 2 - bbox[0]
    y0 = (AH * SS - th) / 2 - bbox[1] - 6 * SS
    dm.text((x0, y0), 'Y', font=font, fill=255)
    kb = dm.textbbox((0, 0), 'K', font=font)
    dk = dm.textlength('Y', font=font)
    dm.text((x0 + dk - 0.06 * th, y0), 'K', font=font, fill=255)
    mask = np.asarray(m, np.float32) / 255

    out = Image.new('RGB', (AW * SS, AH * SS), (10, 10, 11))
    d = ImageDraw.Draw(out)

    step = 4 * SS
    rng = np.random.default_rng(11)
    ys, xs = np.mgrid[0:AH * SS:step, 0:AW * SS:step]
    for y, x in zip(ys.ravel(), xs.ravel()):
        v = mask[min(y, AH * SS - 1), min(x, AW * SS - 1)]
        if v < 0.35:
            continue
        phase = (x * 0.02 + y * 0.015) + t * 6.283
        dx = np.sin(phase) * 1.6 * SS
        dy = np.cos(phase * 0.8) * 1.6 * SS
        r = (0.9 + 0.9 * v) * SS * (0.7 + 0.3 * np.sin(t * 6.283 + x * 0.01))
        shade = 0.45 + 0.55 * v
        c = (int(232 * shade), int(228 * shade), int(220 * shade))
        d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=c)

    glow = out.filter(ImageFilter.GaussianBlur(2 * SS))
    base = np.asarray(out, np.float32)
    g = np.asarray(glow, np.float32)
    merged = np.clip(base * 0.92 + g * 0.35, 0, 255)
    return Image.fromarray(merged.astype(np.uint8)).resize((AW, AH), Image.LANCZOS)


def frame(t):
    img = Image.new('RGB', (W, H), (10, 10, 11))
    art = dot_field(t)
    img.paste(art, (AX0, AY0))

    d = ImageDraw.Draw(img)
    fg, muted = (240, 240, 242), (152, 155, 162)
    d.text((48, 76), 'Yusuf Kabiden', font=ImageFont.truetype(F_SEMI, 44), fill=fg)
    d.text((48, 142), 'Frontend engineer and product designer.', font=ImageFont.truetype(F_TXT, 16), fill=muted)
    d.text((48, 164), 'I ship interfaces and prove them.', font=ImageFont.truetype(F_TXT, 16), fill=muted)
    d.text((48, 198), 'Astana, Kazakhstan · UTC+5', font=ImageFont.truetype(F_TXT, 13), fill=muted)
    x = 48
    for num, lab in (('113', 'TESTS BEHIND OYKASPI'), ('150', 'COMMITS IN TASTECODE'), ('4', 'PRODUCTS SHIPPED')):
        d.text((x, 232), num, font=ImageFont.truetype(F_SEMI, 22), fill=fg)
        d.text((x, 260), lab, font=ImageFont.truetype(F_TXT, 9), fill=muted)
        x += 146
    return img


if __name__ == '__main__':
    frame(0.0).save('/tmp/hero_v4.png')
    print('ok')
