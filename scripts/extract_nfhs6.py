#!/usr/bin/env python3
"""Read the NFHS-6 (2023-24) India and State/UT fact sheets into data/nfhs6/states.json.

Source: IIPS, National Family Health Survey (NFHS-6), 2023-24: India and State/UT
Fact Sheets, May 2026 (Ministry of Health and Family Welfare). The compendium PDF is
not committed (about 49 MB); pass its path, or the text from `pdftotext -layout`.

    python3 scripts/extract_nfhs6.py path/to/compendium.pdf          # writes the JSON
    python3 scripts/extract_nfhs6.py path/to/compendium.pdf --check  # compares only

Each fact-sheet row carries four figures: urban, rural and total for NFHS-6, then the
NFHS-5 total beside them. Three things are kept as printed and never filled in:
a figure in parentheses (based on 25 to 49 unweighted cases) is kept with a flag, and
an asterisk (suppressed, under 25 cases) or NA is null. Manipur has no NFHS-6 sheet.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'nfhs6', 'states.json')

# Name in the compendium -> name used by data/interactive-data.json and the geojson.
NAMES = {
    'India': 'India',
    'Andaman and Nicobar Islands': 'Andaman & Nicobar Islands',
    'Jammu and Kashmir': 'Jammu & Kashmir',
    'NCT of Delhi': 'Delhi',
}

VAL = r'(?:\(?-?\d+(?:\.\d+)?\)?|\*|NA|na|-)'
HEAD = re.compile(r'^\s*(.+?) - Key Indicators\s*$')
ROW = re.compile(r'^\s*(\d{1,3})\.?\s+(.*?)\s*(' + VAL + r')\s+(' + VAL + r')\s+(' + VAL + r')\s+(' + VAL + r')\s*$')
NUMLINE = re.compile(r'^\s*(\d{1,3})\.?\s+(\S.*)$')
TAIL = re.compile(r'^\s*([A-Za-z\)].*?)\s{2,}(' + VAL + r')\s+(' + VAL + r')\s+(' + VAL + r')\s+(' + VAL + r')\s*$')
VALS = re.compile(r'^\s*(' + VAL + r')\s+(' + VAL + r')\s+(' + VAL + r')\s+(' + VAL + r')\s*$')


def num(tok):
    """(value, flag) for one printed cell."""
    t = tok.strip()
    if t in ('*', 'NA', 'na', '-'):
        return None, t
    paren = t.startswith('(')
    return float(t.strip('()')), ('few' if paren else '')


def blocks(text):
    cur, buf = None, []
    for line in text.splitlines():
        h = HEAD.match(line)
        if h:
            if cur and buf:
                yield cur, buf
            cur, buf = h.group(1).strip(), []
        elif cur:
            buf.append(line)
    if cur and buf:
        yield cur, buf


def parse_block(lines):
    rows, pending, last = {}, None, 0
    for line in lines:
        m = ROW.match(line)
        if m and 1 <= int(m.group(1)) <= 130:
            n = int(m.group(1))
            rows.setdefault(n, (m.group(2).strip(), m.groups()[2:]))
            pending, last = None, n
            continue
        v = VALS.match(line)
        if v and pending is not None:
            rows.setdefault(pending[0], (pending[1], v.groups()))
            pending, last = None, pending[0]
            continue
        t = TAIL.match(line)
        if t and pending is not None:
            # the second half of a wrapped label shares a line with the figures
            rows.setdefault(pending[0], (pending[1], t.groups()[1:]))
            pending, last = None, pending[0]
            continue
        if v and last:
            # the numbered label line was lost (OCR merged it away): take the next number
            rows.setdefault(last + 1, ('', v.groups()))
            last += 1
            continue
        p = NUMLINE.match(line)
        pending = (int(p.group(1)), p.group(2).strip()) if p and int(p.group(1)) <= 130 else pending
    return rows


def main():
    src = sys.argv[1]
    text = src if src.endswith('.txt') else None
    if text:
        text = open(src).read()
    else:
        text = subprocess.run(['pdftotext', '-layout', src, '-'], check=True, capture_output=True, text=True).stdout
    seen, votes, states = set(), {}, {}
    for name, lines in blocks(text):
        # each sheet header appears on two pages; merge both halves
        rows = parse_block(lines)
        key = NAMES.get(name, name)
        d = states.setdefault(key, {})
        for n, (label, cells) in rows.items():
            if label:
                votes.setdefault(n, {}).setdefault(label, 0)
                votes[n][label] += 1
            if n not in d:
                d[n] = [num(c) for c in cells]
        seen.add(key)
    # a label is whatever most sheets print for that number; OCR'd sheets can garble one
    labels = {n: max(v, key=lambda k: (v[k], len(k))) for n, v in votes.items()}
    out = {'source': 'IIPS, NFHS-6 (2023-24) India and State/UT Fact Sheets, May 2026 (MoHFW). Manipur has no sheet.',
           'columns': ['urban', 'rural', 'total', 'nfhs5_total'],
           'indicators': {str(n): labels.get(n, '') for n in sorted(labels)},
           'states': {s: {str(n): {'urban': c[0][0], 'rural': c[1][0], 'total': c[2][0], 'nfhs5': c[3][0],
                                   'flag': c[2][1], 'flag5': c[3][1]} for n, c in sorted(r.items())}
                      for s, r in sorted(states.items())}}
    if '--check' in sys.argv:
        print(len(out['states']), 'sheets;', {s: len(r) for s, r in out['states'].items()})
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    print('wrote', OUT, len(out['states']), 'sheets')


if __name__ == '__main__':
    main()
