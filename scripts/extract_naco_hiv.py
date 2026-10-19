#!/usr/bin/env python3
"""Read adult HIV prevalence by state, 2024, from NACO's Sankalak (7th edition, 2025) into data/naco/hiv-2024.json.

    python3 scripts/extract_naco_hiv.py SANKALAK.pdf          # writes the JSON
    python3 scripts/extract_naco_hiv.py SANKALAK.pdf --check  # compares only

Figure 2.7 'Adult HIV prevalence (%), 2024' prints one bar per state and UT with its value. The PDF's SHA-256
is pinned. The India bar must read 0.20, and Mizoram, Nagaland and Manipur must read the 2.75, 1.37 and 0.81
the report's own text quotes. Ladakh and Lakshadweep are not in the figure.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, GEO, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'naco', 'hiv-2024.json')
URL = 'https://naco.mohfw.gov.in/files/Sankalak%20Booklet_Seventh%20Edition.pdf'
SHA = None  # set on first run from the downloaded copy; pinned in the JSON thereafter


def main():
    pdf = sys.argv[1]
    t = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    a = t.index('Figure 2.7. Adult HIV prevalence (%), 2024', t.index('Figure 2.7.', t.index('Status of the epidemic')))
    block = t[a:t.index('0.00           0.50', a)]
    vals = {}
    for m in re.finditer(r'^\s*([A-Za-z&][A-Za-z&. ]+?)\s+(\d\.\d\d)\s*$', block, re.M):
        vals[m.group(1).strip()] = float(m.group(2))
    nat = vals.pop('India')
    if nat != 0.20 or (vals['Mizoram'], vals['Nagaland'], vals['Manipur']) != (2.75, 1.37, 0.81):
        raise SystemExit('Figure 2.7 does not match the values quoted in the report text')
    out = {'source': 'NACO, Sankalak: Status of National AIDS & STD Response, 7th edition (2025), Figure 2.7', 'url': URL, 'sha256': sha256(pdf),
           'national': nat, 'values': {GEO.get(k, k): v for k, v in sorted(vals.items())}}
    if len(out['values']) != 34:
        raise SystemExit('expected 34 states and UTs, got %d' % len(out['values']))
    if '--check' in sys.argv:
        print('OK' if json.load(open(OUT)) == out else 'STALE')
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT, len(out['values']))


if __name__ == '__main__':
    main()
