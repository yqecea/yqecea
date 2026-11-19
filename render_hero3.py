#!/usr/bin/env python3
"""Hero v3: warm glowing ribbon knot, depth, grain, supersampled."""
import numpy as np, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = pathlib.Path('/home/yqecea/.hermes/profiles/yqecea/work/github-profile/assets')
W, H = 1200, 320
F_TXT = '/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf'
F_SEMI = '/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf'
AX0, AX1, AY0, AY1 = 540, 1180, 6, 314
AW, AH = AX1 - AX0, AY1 - AY0
SS = 2  # supersample


def knot_points(n=900, t=0.0, p=2, q=3):
    u = np.linspace(0, 2 * np.pi, n)
    r = 2.0 + np.cos(q * u / p)
    x, y, z = r * np.cos(u), r * np.sin(u), np.sin(q * u / p) * 1.05
    a = t * 2 * np.pi
    xr = x * np.cos(a) - z * np.sin(a)
    zr = x * np.sin(a) + z * np.cos(a)
    yr = y * np.cos(a * 0.62) - zr * np.sin(a * 0.62)
    z2 = y * np.sin(a * 0.62) + zr * np.cos(a * 0.62)
    d = 6.4 + z2 * 0.85
    amp = AH * SS * 0.62
    sx = (xr / d) * amp + AW * SS * 0.52
    sy = (yr / d) * amp + AH * SS * 0.50
    return sx, sy, z2


def art_layer(t):
    """RGBA art layer at SS resolution: core ribbon + glow + rim."""
    w, h = AW * SS, AH * SS
    core = Image.new('L', (w, h), 0)
    dc = ImageDraw.Draw(core)
    px, py, pz = knot_points(t=t)
    for i in range(len(px) - 1):
        depth = np.clip((pz[i] + 2) / 4, 0, 1)
        width = int(5.0 * SS + 4.0 * SS * depth)
        val = int(70 + 185 * depth)
        dc.line([(px[i], py[i]), (px[i + 1], py[i + 1])], fill=val, width=width)

    glow_small = core.filter(ImageFilter.GaussianBlur(3 * SS))
    glow_big = core.filter(ImageFilter.GaussianBlur(9 * SS))

    core_c = np.array((237, 232, 223), dtype=np.float32)     # warm champagne
    rim_c = np.array((154, 180, 255), dtype=np.float32)      # cool rim

    c = np.asarray(core, np.float32) / 255
    g1 = np.asarray(glow_small, np.float32) / 255
    g2 = np.asarray(glow_big, np.float32) / 255

    lum = np.clip(c * 1.0 + g1 * 0.55, 0, 1)
    halo = np.clip(g1 * 0.45 + g2 * 0.55, 0, 1)

    rgb = np.zeros((h, w, 3), np.float32)
    for i in range(3):
        rgb[:, :, i] = core_c[i] * lum + rim_c[i] * halo * 0.55
    return np.clip(rgb, 0, 255)


def frame(t, theme='dark'):
    img = Image.new('RGB', (W, H), (8, 8, 9) if theme == 'dark' else (255, 255, 255))
    # radial depth gradient
    if theme == 'dark':
        yy, xx = np.mgrid[0:H, 0:W]
        cx, cy = W * 0.78, H * 0.5
        r = np.sqrt(((xx - cx) / W) ** 2 + ((yy - cy) / H) ** 2)
        base = np.clip(20 - 12 * (r / 0.6), 8, 20)
        img = Image.fromarray(np.dstack([base] * 3).astype(np.uint8))

    art = Image.fromarray(art_layer(t).astype(np.uint8)).resize((AW, AH), Image.LANCZOS)
    img.paste(Image.blend(img.crop((AX0, AY0, AX1, AY1)), art, 1.0), (AX0, AY0))

    # subtle grain
    if theme == 'dark':
        rng = np.random.default_rng(3)
        arr = np.asarray(img, np.int16)
        noise = rng.integers(-3, 4, size=(H, W, 1))
        img = Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8))

    d = ImageDraw.Draw(img)
    fg = (240, 240, 242) if theme == 'dark' else (16, 16, 18)
    muted = (152, 155, 162) if theme == 'dark' else (92, 102, 112)
    d.text((48, 76), 'Yusuf Kabiden', font=ImageFont.truetype(F_SEMI, 44), fill=fg)
    d.text((48, 142), 'Frontend engineer and product designer.', font=ImageFont.truetype(F_TXT, 16), fill=muted)
    d.text((48, 164), 'I ship interfaces and prove them.', font=ImageFont.truetype(F_TXT, 16), fill=muted)
    d.text((48, 198), 'Astana, Kazakhstan · UTC+5', font=ImageFont.truetype(F_TXT, 13), fill=muted)
    x = 48
    for num, lab in (('113', 'TESTS FOR OYKASPI'), ('12', 'COMMITS IN TASTECODE'), ('4', 'PRODUCTS SHIPPED')):
        d.text((x, 232), num, font=ImageFont.truetype(F_SEMI, 22), fill=fg)
        d.text((x, 260), lab, font=ImageFont.truetype(F_TXT, 9), fill=muted)
        x += 146
    return img


if __name__ == '__main__':
    frame(0.0).save('/tmp/hero_v3.png')
    print('ok')
