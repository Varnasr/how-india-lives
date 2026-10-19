#!/usr/bin/env python3
"""Read Table 1.43 of TRAI's Yearly Performance Indicators (end of March 2026) into data/trai/internet-2026-03.json.

    python3 scripts/extract_trai_internet.py YIR.pdf [--check]

Table 1.43 gives internet subscribers by state and UT (rural, urban, total, in millions) and subscribers per 100
population (rural, urban, total). A subscription is not a person: one person can hold several, which is why Goa, Delhi
and Haryana exceed 100 per 100 people. Population is TRAI's projection from the Technical Group's 2011-2036 report.
Checks: rural plus urban equals total in each row (0.02 mn), the 36 rows sum to the printed 1,092.79 million (and rural
440.87, urban 651.93), and the table's total per 100 equals 76.59. Rural and urban per-100 cells printed '-' (Delhi,
Chandigarh, Lakshadweep) are left empty. The operators' rural/urban split uses different sources (TRAI's own note), so
only the total per 100 is mapped.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'trai', 'internet-2026-03.json')
URL = 'https://www.trai.gov.in/'
NAMES = {'Chattisgarh': 'Chhattisgarh', 'Andaman & Nicobar Islands': 'Andaman and Nicobar', 'Dadar & Nagar Haweli (incl. Daman & Diu)': 'Dadra and Nagar Haveli and Daman and Diu', 'Jammu & Kashmir': 'Jammu and Kashmir'}
NUM = r'(-|[\d.]+)'


def main():
    t = subprocess.run(['pdftotext', '-layout', sys.argv[1], '-'], capture_output=True, text=True).stdout
    a = t.index('Table 1.43: State/UT wise number of Internet Subscribers per 100')
    seg = t[a:t.index('Top five Telecom Service Areas in terms of internet', a)]
    seg = re.sub(r'\s*\n\s*(Islands|\(incl\. Daman & Diu\))\s*\n', r' \1\n', seg)
    rows = {}
    for ln in seg.splitlines():
        m = re.match(r'^\s*(?:\d+\s+)?([A-Za-z&][A-Za-z&.() ]*?)\s+' + r'\s+'.join([NUM] * 6) + r'\s*$', ln)
        if m and m.group(1).strip() not in ('Total',):
            name = m.group(1).strip()
        elif re.match(r'^\s*Total\s', ln):
            continue
        else:
            m = None
        if m:
            v = [None if m.group(i) == '-' else float(m.group(i)) for i in range(2, 8)]
            rows[name] = v
    # wrapped names (two UTs): the figure line follows a name-only line
    lines = seg.splitlines()
    for i, ln in enumerate(lines):
        if re.match(r'^\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+(-|[\d.]+)\s+(-|[\d.]+)\s+[\d.]+\s*$', ln):
            ctx = ' '.join(x.strip() for x in lines[max(0, i - 3):i])
            nm = 'Andaman and Nicobar' if 'Andaman' in ctx else 'Dadra and Nagar Haveli and Daman and Diu' if 'Dadar' in ctx else None
            if nm:
                v = ln.split()
                rows[nm] = [None if x == '-' else float(x) for x in v]
    out = {}
    for n, v in rows.items():
        n = NAMES.get(n, n)
        out[n] = {'rural_mn': v[0], 'urban_mn': v[1], 'total_mn': v[2], 'rural_per100': v[3], 'urban_per100': v[4], 'total_per100': v[5]}
    assert len(out) == 36, (len(out), sorted(out))
    for n, d in out.items():
        assert abs(d['rural_mn'] + d['urban_mn'] - d['total_mn']) <= 0.02, (n, d)
    for k, tot in (('rural_mn', 440.87), ('urban_mn', 651.93), ('total_mn', 1092.79)):
        assert abs(sum(d[k] for d in out.values()) - tot) <= 0.1, (k, sum(d[k] for d in out.values()), tot)
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert not set(out) - geo, sorted(set(out) - geo)
    res = {'source': 'TRAI, Yearly Performance Indicators of Indian Telecom Services 2025-26, Table 1.43 (end of March 2026)', 'url': URL,
           'sha256': sha256(sys.argv[1]), 'india_total_per100': 76.59, 'india_total_mn': 1092.79, 'states': dict(sorted(out.items()))}
    print(len(out), 'rows; missing from geo:', sorted(geo - set(out)))
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == res, 'stale'
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(res, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')


main()
