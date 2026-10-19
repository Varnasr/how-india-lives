#!/usr/bin/env python3
"""Read Table 1 of CPCB's 'Polluted River Stretches for Restoration of Water Quality 2025' into data/cpcb/polluted-rivers-2025.json.

    python3 scripts/extract_cpcb_rivers.py REPORT.pdf          # writes the JSON
    python3 scripts/extract_cpcb_rivers.py REPORT.pdf --check  # compares only

Source: Central Pollution Control Board, September 2025 (monitoring of 2022 and 2023). Table 1 counts polluted river
stretches and locations by state and priority class: I (BOD above 30 mg/L), II (20.1 to 30), III (10.1 to 20), IV (6.1 to
10), V (3.1 to 6). Each row's classes must add to its total and each column to the printed total row (36, 21, 45, 45,
148, 295). The 32 listed states and UTs are those with a polluted stretch identified; the rest are not in the table.
The report's own summary also speaks of 279 stretches, which does not match Table 1's 295; Table 1 is used.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, GEO, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'cpcb', 'polluted-rivers-2025.json')
URL = 'https://dste.py.gov.in/ppcc/pdf/Laboratory/PRS-2025.pdf'
COLS = ['priority_I', 'priority_II', 'priority_III', 'priority_IV', 'priority_V', 'total']
PRINTED = [36, 21, 45, 45, 148, 295]


def main():
    pdf = sys.argv[1]
    t = re.sub(r'[ \t]+', ' ', subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout)
    a = t.index('Table – 1: State-wise no. of polluted river locations')
    block = t[a:t.index('The 295 polluted river stretches/locations identified on 271 rivers include', a)]
    rows = {}
    for line in block.splitlines():
        m = re.match(r'^\s*(\d{1,2}) (?:([A-Za-z&. ]+?) )?(\d+) (\d+) (\d+) (\d+) (\d+) (\d+)\s*$', line)
        if not m:
            continue
        name = m.group(2) or ('Dadra and Nagar Haveli and Daman and Diu' if m.group(1) == '6' else None)
        if name is None:
            raise SystemExit('row %s has no state name' % m.group(1))
        vals = [int(m.group(i)) for i in range(3, 9)]
        if sum(vals[:5]) != vals[5]:
            raise SystemExit('%s: classes do not add to the row total' % name)
        rows[GEO.get(name.strip(), name.strip())] = dict(zip(COLS, vals))
    if len(rows) != 32:
        raise SystemExit('expected 32 states and UTs, read %d: %s' % (len(rows), sorted(rows)))
    for i, c in enumerate(COLS):
        if sum(r[c] for r in rows.values()) != PRINTED[i]:
            raise SystemExit('column %s does not add to the printed total %d' % (c, PRINTED[i]))
    out = {'source': 'Central Pollution Control Board, Polluted River Stretches for Restoration of Water Quality, September 2025 (monitoring 2022 and 2023), Table 1',
           'url': URL, 'sha256': sha256(pdf), 'classes': {'priority_I': 'BOD above 30 mg/L', 'priority_II': '20.1 to 30', 'priority_III': '10.1 to 20', 'priority_IV': '6.1 to 10', 'priority_V': '3.1 to 6'},
           'states': dict(sorted(rows.items()))}
    if '--check' in sys.argv:
        print('OK' if json.load(open(OUT)) == out else 'STALE')
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT, len(rows))


if __name__ == '__main__':
    main()
