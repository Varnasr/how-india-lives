#!/usr/bin/env python3
"""Write data/mord/mgnrega-2024-25.json from the Ministry of Rural Development's State Performance Report 2024-25.

    python3 scripts/extract_mgnrega_spr.py "State Performance Report 2024-25.pdf" [--check]

Source: Department of Rural Development, State Performance Report 2024-25, Annexure I (percentage of households that completed
100 days of work in FY 2024-25), Annexure II (share of SCs, STs and women in the persondays generated) and Annexure III (total
persondays). The PDF is from dord.gov.in (SHA-256 pinned below). Checks: each annexure lists the same 34 states and UTs in the
same order, the persondays add to the printed total (29,06,505,713), and the printed all-India figures are kept beside the rows.
West Bengal had no approved Labour Budget and shows 0 persondays, and Lakshadweep shows 0, so a 0% there means no data and
both are left out. Percentages are printed as whole numbers.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import GEO, ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'mord', 'mgnrega-2024-25.json')
SHA = '78b1d4527933ce3a74bdd241191c1b2b4c11813eabe65cdf31ee35132822c20f'
URL = 'https://www.dord.gov.in/static/uploads/2025/09/d81193f25cde78b36f36b559ffabbb18.pdf'
FIX = {'DN HAVELI AND DD': 'Dadra and Nagar Haveli and Daman and Diu', 'ANDAMAN AND NICOBAR': 'Andaman and Nicobar'}
TOTAL_PD = 2906505713


def seg(text, a, b):
    i = text.index(a)
    return text[i:text.index(b, i)].splitlines()


def name(raw):
    raw = raw.strip()
    if raw in FIX:
        return FIX[raw]
    t = raw.rstrip('*').title().replace(' And ', ' and ')
    return GEO.get(t, t)


def main():
    pdf = sys.argv[1]
    assert sha256(pdf) == SHA, 'wrong file'
    text = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    pct = lambda s: int(s.rstrip('%'))
    a1, a2, a3 = {}, {}, {}
    for line in seg(text, 'Percentage of Households completed 100 Days of Work in FY 2024-25\n', 'Annexure II'):
        m = re.match(r'^\s*(\d{1,2})\s+([A-Z][A-Z ]+?)\s{2,}(\d+%)\s*$', line)
        if m:
            a1[int(m.group(1))] = (name(m.group(2)), pct(m.group(3)))
        elif 'ALL INDIA' in line:
            all1 = pct(re.search(r'(\d+%)', line).group(1))
    for line in seg(text, 'Share of Vulnerable Segments', 'Annexure III'):
        m = re.match(r'^\s*(\d{1,2})\s+([A-Z][A-Z ]+?)\s{2,}(\d+%)\s+(\d+%)\s+(\d+%)\s*$', line)
        if m:
            a2[int(m.group(1))] = (name(m.group(2)), pct(m.group(3)), pct(m.group(4)), pct(m.group(5)))
        elif 'ALL INDIA' in line:
            all2 = [pct(x) for x in re.findall(r'(\d+%)', line)]
    for line in seg(text, 'Total Persondays generated under Mahatma', 'Annexure IV'):
        m = re.match(r'^\s*(\d{1,2})\s+([A-Z][A-Z ]+?\*?)\s{2,}([\d,]+)\s*$', line)
        if m:
            a3[int(m.group(1))] = (name(m.group(2)), int(m.group(3).replace(',', '')))
        elif re.match(r'^\s*TOTAL\s', line):
            tot = int(re.search(r'([\d,]{6,})', line).group(1).replace(',', ''))
    assert sorted(a1) == sorted(a2) == sorted(a3) == list(range(1, 35)), (len(a1), len(a2), len(a3))
    for k in a1:
        assert a1[k][0] == a2[k][0] == a3[k][0], (k, a1[k][0], a2[k][0], a3[k][0])
    assert sum(v[1] for v in a3.values()) == tot == TOTAL_PD
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    states = {}
    for k in sorted(a1):
        s = a1[k][0]
        assert s in geo, s
        states[s] = {'hh_100_days_pct': a1[k][1], 'sc_pct': a2[k][1], 'st_pct': a2[k][2], 'women_pct': a2[k][3], 'persondays': a3[k][1]}
    out = {'source': 'Ministry of Rural Development, State Performance Report 2024-25, Annexures I to III', 'url': URL, 'sha256': SHA,
           'retrieved': '2026-10-20', 'year': '2024-25', 'persondays_total': tot,
           'all_india': {'hh_100_days_pct': all1, 'sc_pct': all2[0], 'st_pct': all2[1], 'women_pct': all2[2]}, 'states': states}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(states), 'states; persondays', tot)


main()
