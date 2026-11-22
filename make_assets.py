#!/usr/bin/env python3
"""Generate GitHub profile assets: hero + project tiles, light and dark."""
import pathlib
from xml.sax.saxutils import escape

OUT = pathlib.Path('assets')
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
 'light': dict(bg='#ffffff', border='#e3e3e3', text='#111111', muted='#5f6b76', soft='#f6f6f6', accent='#111111'),
 'dark':  dict(bg='#0d0d0d', border='#272727', text='#f4f4f4', muted='#a8a8a8', soft='#161616', accent='#f4f4f4'),
}
FONT = "'Inter','SF Pro Text',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

def hero(theme):
    t = THEMES[theme]
    stats = [('12', 'COMMITS MERGED UPSTREAM'), ('20', 'AGENTS IN GEM-SWARM'), ('69', 'DESIGN COMPONENTS')]
    parts = []
    col_w, gap = 150, 34
    total = col_w * 3 + gap * 2
    x0 = 1200 - 48 - total
    for i, (v, label) in enumerate(stats):
        x = x0 + i * (col_w + gap)
        parts.append(f'<text x="{x}" y="152" font-family="{FONT}" font-size="31" font-weight="600" fill="{t["text"]}" style="font-variant-numeric:tabular-nums">{v}</text>')
        parts.append(f'<text x="{x}" y="174" font-family="{FONT}" font-size="9.5" letter-spacing="1.1" fill="{t["muted"]}">{escape(label)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="272" viewBox="0 0 1200 272" role="img" aria-label="Yusuf Kabiden, AI and design engineer in Astana.">
<rect width="1200" height="272" rx="14" fill="{t['bg']}" stroke="{t['border']}"/>
<text x="48" y="104" font-family="{FONT}" font-size="44" font-weight="600" letter-spacing="-1" fill="{t['text']}">Yusuf Kabiden</text>
<text x="48" y="140" font-family="{FONT}" font-size="16.5" fill="{t['muted']}">AI &amp; Design Engineer. Multi-agent setups and product UI.</text>
<text x="48" y="190" font-family="{FONT}" font-size="13" fill="{t['muted']}">Astana, Kazakhstan · UTC+5 · TypeScript, Flutter, design systems</text>
<line x1="48" y1="216" x2="1152" y2="216" stroke="{t['border']}"/>
{''.join(parts)}
</svg>'''

TILES = [
 ('tastecode', 'TasteCode', 'Open source: 12 commits merged upstream, plus the Linux line that ships .deb and .AppImage.', 'TypeScript · Electron · Linux'),
 ('webgl', 'Portfolio', 'WebGL and Three.js: shaders, scroll choreography, live at yqecea-portfolio.web.app.', 'Three.js · live'),
]

def tile(key, title, desc, meta, theme, w=380, h=132):
    t = THEMES[theme]
    # wrap description into two lines of ~52 chars
    words, lines, cur = desc.split(), [], ''
    for word in words:
        if len(cur) + len(word) + 1 <= 52:
            cur = (cur + ' ' + word).strip()
        else:
            lines.append(cur); cur = word
    if cur: lines.append(cur)
    lines = lines[:3]
    body = ''.join(f'<text x="24" y="{78 + i*17}" font-family="{FONT}" font-size="12.5" fill="{t["muted"]}">{escape(l)}</text>' for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}: {escape(desc)}">
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="{t['bg']}" stroke="{t['border']}"/>
<circle cx="26" cy="30" r="4" fill="{t['text']}"/>
<text x="40" y="35" font-family="{FONT}" font-size="15" font-weight="600" fill="{t['text']}">{escape(title)}</text>
{body}
<text x="24" y="{h-14}" font-family="{FONT}" font-size="11" fill="{t['muted']}">{escape(meta)}</text>
</svg>'''

for theme in THEMES:
    (OUT / f'hero-{theme}.svg').write_text(hero(theme))
    for key, title, desc, meta in TILES:
        (OUT / f'tile-{key}-{theme}.svg').write_text(tile(key, title, desc, meta, theme))
print('generated', len(list(OUT.glob('*.svg'))), 'files')
