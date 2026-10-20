"""Draws the extension icons (icons/icon16/32/48/128.png) as a little LED board showing "M" in the board's 5x5 font.
Run once:  python make_icons.py   (needs Pillow:  pip install pillow). The PNGs are checked in, so buyers never need this."""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "icons")
os.makedirs(OUT, exist_ok=True)

M = ['#...#', '##.##', '#.#.#', '#...#', '#...#']   # same glyph as the board's font (pixfont.js)
GRID = 9                                             # 9x9 LED grid, "M" centered (cols 2-6, rows 2-6)
AMBER = (255, 170, 0)
OFF = (26, 26, 33)
BG = (11, 11, 13)


def draw(size):
    S = 8  # supersample for smooth dots
    px = size * S
    img = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = px * 0.16
    d.rounded_rectangle([0, 0, px - 1, px - 1], radius=r, fill=BG + (255,))
    cell = px / (GRID + 1.0)
    margin = cell / 2
    dot = cell * 0.78 if size >= 48 else cell * 0.9
    for row in range(GRID):
        for col in range(GRID):
            lit = 2 <= row <= 6 and 2 <= col <= 6 and M[row - 2][col - 2] == '#'
            if not lit and size < 32:
                continue  # tiny sizes: only lit dots, otherwise it turns to mud
            cx = margin + cell * col + cell / 2
            cy = margin + cell * row + cell / 2
            color = AMBER if lit else OFF
            if lit and size >= 48:  # soft glow
                g = dot * 1.6
                d.ellipse([cx - g / 2, cy - g / 2, cx + g / 2, cy + g / 2], fill=(255, 170, 0, 60))
            d.ellipse([cx - dot / 2, cy - dot / 2, cx + dot / 2, cy + dot / 2], fill=color + (255,))
    return img.resize((size, size), Image.LANCZOS)


for s in (16, 32, 48, 128):
    draw(s).save(os.path.join(OUT, f"icon{s}.png"))
    print("wrote", f"icons/icon{s}.png")
