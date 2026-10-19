#!/usr/bin/env python3
"""OCR the NFHS-6 fact-sheet pages that have no text layer, into text extract_nfhs6.py can read.

In the May 2026 compendium, 13 of the 36 sheets (Andaman and Nicobar, Andhra Pradesh,
Dadra and Nagar Haveli and Daman and Diu, Ladakh, Lakshadweep, Rajasthan, Sikkim,
Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal) draw their
figures with no extractable text. They render correctly, so this reads them as images.

    pip install rapidocr-onnxruntime pdfplumber
    python3 scripts/ocr_nfhs6.py compendium.pdf compendium.txt out_ocr.txt

Arguments: the PDF, the `pdftotext -layout` text, and where to write the merged text.
OCR can misread a digit, so extract_nfhs6.py is not the last word: scripts/check_nfhs6.py
compares the NFHS-5 column of every OCR'd sheet with the published NFHS-5 values.
"""
import re
import subprocess
import sys
import tempfile
import os

from rapidocr_onnxruntime import RapidOCR


def line_text(items, tol=9):
    """Group OCR boxes into text lines by y, ordered by x; the four figures stay 3+ spaces apart."""
    boxes = []
    for pts, txt, _ in items:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        boxes.append((sum(ys) / 4, min(xs), max(xs), txt))
    boxes.sort()
    lines, cur, cy = [], [], None
    for y, x0, x1, t in boxes:
        if cy is None or abs(y - cy) <= tol:
            cur.append((x0, x1, t))
            cy = y if cy is None else (cy + y) / 2
        else:
            lines.append(cur)
            cur, cy = [(x0, x1, t)], y
    if cur:
        lines.append(cur)
    out = []
    for ln in lines:
        ln.sort()
        s = ''
        for x0, x1, t in ln:
            s += ('   ' if s else '') + t
        out.append(s)
    return out


def main():
    pdf, txt, dest = sys.argv[1:4]
    pages = open(txt).read().split('\f')
    todo = []
    for i, p in enumerate(pages, 1):
        h = re.search(r'(\S.*?) - Key Indicators', p)
        # a sheet page with a header but no numbered rows has no text layer
        if h and len(re.findall(r'\n\s*\d{1,3}\.\s', p)) == 0:
            todo.append((i, h.group(1).strip()))
    ocr = RapidOCR()
    chunks = []
    with tempfile.TemporaryDirectory() as d:
        for i, name in todo:
            subprocess.run(['pdftoppm', '-f', str(i), '-l', str(i), '-r', '220', '-png', pdf, os.path.join(d, 'pg')], check=True)
            png = [f for f in os.listdir(d) if f.startswith('pg')][0]
            res, _ = ocr(os.path.join(d, png))
            os.remove(os.path.join(d, png))
            body = '\n'.join(line_text(res or []))
            chunks.append('\n%s - Key Indicators\n%s\n' % (name, body))
            print('page', i, name, len(res or []), 'boxes', file=sys.stderr)
    keep = '\f'.join(p for p in pages if not (re.search(r' - Key Indicators', p) and len(re.findall(r'\n\s*\d{1,3}\.\s', p)) == 0))
    open(dest, 'w').write(keep + '\n' + ''.join(chunks))


if __name__ == '__main__':
    main()
