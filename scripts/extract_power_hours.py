#!/usr/bin/env python3
"""Write data/power/supply-hours-2022.json from Annexure I of Rajya Sabha Unstarred Question 3185 (28 March 2023).

    python3 scripts/extract_power_hours.py AU3185.pdf [--check]

Source: Ministry of Power, reply to Rajya Sabha Unstarred Question 3185 of 28 March 2023, Annexure I: state-wise average hours of
power supply in a day on 11 kV feeders, rural and urban, for 2018-19 to 2022-23 (to December 2022), for the states that report on
the National Power Portal. The PDF is from sansad.in (SHA-256 pinned below). The table has blank cells where a state reported
nothing, so each number is assigned to a column by the position of its right edge, taken from the printed All India row, and
five printed rural values are asserted to land in the right column. Kept: rural 2021-22, the last full year and the one the most
states report. States with no rural figure are left grey.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'power', 'supply-hours-2022.json')
SHA = '2e371ba6b8ed38c28b41a3cadc722f26d54112046f64f3af002077f8027e734d'
URL = 'https://sansad.in/getFile/annex/259/AU3185.pdf?source=pqars'
NAMES = {1: 'Andhra Pradesh', 2: 'Arunachal Pradesh', 3: 'Assam', 4: 'Bihar', 5: 'Chhattisgarh', 6: 'Delhi', 7: 'Goa', 8: 'Gujarat',
         9: 'Haryana', 10: 'Himachal Pradesh', 11: 'Jammu and Kashmir', 12: 'Karnataka', 13: 'Kerala', 14: 'Madhya Pradesh',
         15: 'Maharashtra', 16: 'Meghalaya', 17: 'Manipur', 18: 'Mizoram', 19: 'Nagaland', 20: 'Odisha', 21: 'Puducherry',
         22: 'Punjab', 23: 'Rajasthan', 24: 'Tamil Nadu', 25: 'Telangana', 26: 'Tripura', 27: 'Uttar Pradesh', 28: 'Uttarakhand',
         29: 'West Bengal'}
YEARS = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23 (to Dec)']
SPOT = {('Bihar', 3): 20.34, ('Haryana', 3): 16.26, ('Uttar Pradesh', 3): 15.99, ('Himachal Pradesh', 3): 13.27, ('West Bengal', 3): 23.48}


def main():
    pdf = sys.argv[1]
    assert sha256(pdf) == SHA, 'wrong file'
    t = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    seg = t[t.index('ANNEXURE-I\n'):t.index('ANNEXURE-II')].splitlines()
    tot = next(l for l in seg if re.match(r'^\s*TOTAL\s', l))
    ends = [m.end() for m in re.finditer(r'\d+\.\d+', tot)]
    assert len(ends) == 10
    rows = {}
    for l in seg:
        m = re.match(r'^\s*(\d{1,2})\s', l)
        toks = [(x.end(), x.group()) for x in re.finditer(r'\d+\.\d+', l)]
        if not m or not toks:
            continue
        cols = [None] * 10
        for e, v in toks:
            i = min(range(10), key=lambda j: abs(ends[j] - e))
            assert abs(ends[i] - e) <= 3, (l, e)
            cols[i] = float(v)
        rows[int(m.group(1))] = cols
    assert sorted(rows) == list(range(1, 30))
    states = {}
    for k, c in rows.items():
        states[NAMES[k]] = {y: {'rural': c[2 * i], 'urban': c[2 * i + 1]} for i, y in enumerate(YEARS)}
    for (s, i), v in SPOT.items():
        assert states[s][YEARS[i]]['rural'] == v, (s, i)
    allind = {y: {'rural': float(re.findall(r'\d+\.?\d*', tot)[2 * i]), 'urban': float(re.findall(r'\d+\.?\d*', tot)[2 * i + 1])} for i, y in enumerate(YEARS)}
    out = {'source': 'Ministry of Power, Rajya Sabha Unstarred Question 3185 (28 March 2023), Annexure I', 'url': URL, 'sha256': SHA,
           'retrieved': '2026-10-20', 'unit': 'average hours of supply a day on 11 kV feeders', 'all_india': allind, 'states': states}
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert set(states) <= geo
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(sum(1 for s in states.values() if s['2021-22']['rural']), 'states with rural 2021-22')


main()
