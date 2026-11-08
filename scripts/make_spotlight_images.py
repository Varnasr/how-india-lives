#!/usr/bin/env python3
"""Write the smaller WebP copies of the first home-page spotlight map.

The home page paints this map first and it is the largest thing on the screen
(a 3052 px, 416 KB PNG shown 356 to 600 px wide). The PNG stays as the file the
map's own page and every other view uses; this writes two WebP copies beside it,
720 px for phones and 1200 px for wider screens and 2x displays, and index.html
offers them through srcset. Quality 85 was chosen by comparing crops of the map
labels against the PNG at 390 px and 1280 px: 80 already looked the same, 85
leaves margin for the small state codes.

    python3 scripts/make_spotlight_images.py

Needs Pillow. scripts/check_data.py checks the files exist and match the markup.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'maps', 'demography', 'S00a_Median_Age_by_State.png')
WIDTHS = (720, 1200)
QUALITY = 85


def main():
    im = Image.open(SRC).convert('RGB')
    for w in WIDTHS:
        h = round(im.height * w / im.width)
        out = SRC[:-4] + '-%d.webp' % w
        im.resize((w, h), Image.LANCZOS).save(out, 'WEBP', quality=QUALITY, method=6)
        print('%s  %dx%d  %d bytes' % (os.path.relpath(out, ROOT), w, h, os.path.getsize(out)))


if __name__ == '__main__':
    main()
