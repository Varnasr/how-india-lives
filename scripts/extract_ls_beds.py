#!/usr/bin/env python3
"""Read Annexure-I of Lok Sabha Unstarred Question 1000 (25 July 2025): public hospital beds by state, 31 March 2023.

    python3 scripts/extract_ls_beds.py ANNEXURE.pdf          # writes data/health/public-beds-2023.json
    python3 scripts/extract_ls_beds.py ANNEXURE.pdf --check  # compares only

Source: Ministry of Health and Family Welfare, from Health Dynamics of India 2022-23. Beds at PHC, CHC,
sub-district hospital, district hospital and medical college, 36 states and UTs. 'N App' (not applicable) is
kept as null, not zero. Every column must add to the printed All India/Total row and the five columns together
to the 8,18,661 beds the answer's text quotes.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, sha256  # noqa: E402
from extract_ncrb_other import NAMES as NCRB_NAMES  # noqa: E402

# This table numbers Uttarakhand 26 and Uttar Pradesh 27, the reverse of NCRB's order, so the NCRB list cannot be used as is.
NAMES = dict(NCRB_NAMES)
NAMES[26], NAMES[27] = 'Uttarakhand', 'Uttar Pradesh'

OUT = os.path.join(ROOT, 'data', 'health', 'public-beds-2023.json')
URL = 'https://sansad.in/getFile/loksabhaquestions/annex/185/AU1000_LIR76k.pdf?source=pqals'
COLS = ['phc', 'chc', 'sub_divisional_hospital', 'district_hospital', 'medical_college']
V = r'(?:\d+|N App)'


def val(x):
    return None if x == 'N App' else int(x)


def main():
    pdf = sys.argv[1]
    t = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    t = re.sub(r'[ \t]+', ' ', t)
    block = t[t.index('NUMBER OF BEDS AT PHC, CHC, SDH'):]
    rows, pending, total = {}, None, None
    tail = re.compile(r'((?:%s ){4}%s)\s*$' % (V, V))
    for line in block.splitlines():
        line = line.strip()
        if re.fullmatch(r'\d{1,2}', line):
            pending = int(line)
            continue
        m = tail.search(line)
        if not m:
            continue
        cells = m.group(1).split(' ')
        cells = re.findall(V, m.group(1))
        s = re.match(r'(\d{1,2}) ', line)
        if line.startswith('All India'):
            total = [val(c) for c in cells]
        elif s and not line.startswith('All'):
            rows[int(s.group(1))] = [val(c) for c in cells]
            pending = None
        elif pending is not None:
            rows[pending] = [val(c) for c in cells]
            pending = None
    if sorted(rows) != list(range(1, 37)) or total is None:
        raise SystemExit('expected 36 rows and a total, got %s' % sorted(rows))
    for i, c in enumerate(COLS):
        gap = sum(r[i] or 0 for r in rows.values()) - total[i]
        if gap and not (c == 'medical_college' and gap == rows[14][4]):
            raise SystemExit('column %s does not add to the printed total (off by %d)' % (c, gap))
    if sum(total) != 818661:
        raise SystemExit('total beds %d is not the 8,18,661 the answer quotes' % sum(total))
    # Source fault, pinned so a different one fails: the medical-college column adds to 16,998 more than its printed
    # total, which is exactly Maharashtra's own entry, and the printed totals are the ones that match the answer's text
    # (8,18,661). Either the total omits Maharashtra's medical-college beds or that entry is wrong, so Maharashtra is
    # not mapped.
    unreliable = {'Maharashtra': 'The medical-college column adds to 16,998 beds more than its printed total, which is exactly this state\'s entry. The source does not say which is wrong, so the state is left off the map.'}
    # A mapping by serial is only safe if each state's name is printed on its line, so check the two that differ.
    for k in (26, 27):
        line = next(l for l in block.splitlines() if re.match(r'%d ' % k, l.strip()))
        if NAMES[k] not in line:
            raise SystemExit('serial %d is not %s in this table' % (k, NAMES[k]))
    out = {'source': 'Lok Sabha Unstarred Question 1000, 25 July 2025, Annexure-I (Health Dynamics of India 2022-23), beds as on 31 March 2023', 'url': URL,
           'sha256': sha256(pdf), 'national_total': sum(total), 'columns': COLS, 'unreliable': unreliable,
           'states': {NAMES[k]: dict(zip(COLS, rows[k])) for k in range(1, 37)}}
    if '--check' in sys.argv:
        print('OK' if json.load(open(OUT)) == out else 'STALE')
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT)


if __name__ == '__main__':
    main()
