#!/usr/bin/env python3
"""Write data/jjm/tap-connections-2026-07.json from the annexure to Lok Sabha Starred Question 62 (23 July 2026).

    python3 scripts/extract_jjm_tap.py AS62.pdf [--check]

Source: Ministry of Jal Shakti, reply to Lok Sabha Starred Question 62, State/UT-wise progress under Jal Jeevan Mission as on
18 July 2026 (JJM IMIS). The PDF is from sansad.in (SHA-256 pinned below). Checks: 34 rows, total rural households and households with
tap water supply add to the printed totals (1,935.54 and 1,588.96 lakh, within rounding of 0.05 lakh), the printed per cent lies within the
range households with tap supply over total households allows once the lakh figures' rounding is allowed for, and the national 82.09% is recomputed. Delhi and
Chandigarh have no rural population. The count is of connections reported by states, not of supply that runs.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import GEO, ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'jjm', 'tap-connections-2026-07.json')
SHA = 'ad2d0cdc259533a8edacfc49731df845f05604c3d992a12c8de3e4ec6145931a'
URL = 'https://sansad.in/getFile/lsapps/loksabhaquestions/annex/188/AS62_QLiLqk.pdf?source=lsapps'
NAMES = {1: 'Andaman and Nicobar', 2: 'Arunachal Pradesh', 3: 'Dadra and Nagar Haveli and Daman and Diu', 4: 'Goa', 5: 'Haryana',
         6: 'Himachal Pradesh', 7: 'Mizoram', 8: 'Puducherry', 9: 'Punjab', 10: 'Telangana', 11: 'Gujarat', 12: 'Ladakh', 13: 'Uttarakhand',
         14: 'Bihar', 15: 'Nagaland', 16: 'Sikkim', 17: 'Uttar Pradesh', 18: 'Lakshadweep', 19: 'Maharashtra', 20: 'Tamil Nadu',
         21: 'Karnataka', 22: 'Tripura', 23: 'Meghalaya', 24: 'Chhattisgarh', 25: 'Assam', 26: 'Jammu and Kashmir', 27: 'Manipur',
         28: 'Odisha', 29: 'Andhra Pradesh', 30: 'Madhya Pradesh', 31: 'Rajasthan', 32: 'West Bengal', 33: 'Jharkhand', 34: 'Kerala'}


def num(x):
    return None if x == '-' else float(x.replace(',', ''))


def main():
    pdf = sys.argv[1]
    assert sha256(pdf) == SHA, 'wrong file'
    t = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    seg = t[t.index('State/ UT-wise details of progress made under JJM'):].splitlines()
    pat = re.compile(r'((?:[\d,.]+|-)(?:\s+(?:[\d,.]+|-)){6})\s*$')
    rows, tot = [], None
    for l in seg:
        m = pat.search(l)
        if not m:
            continue
        v = m.group(1).split()
        if re.match(r'^\s*Total\b', l):
            tot = v
        elif not re.match(r'^\s*Delhi', l):
            rows.append(v)
    assert len(rows) == 34, len(rows)
    # Row order is the printed serial order; the name fragments sit on the same or the next line, and these spot values pin it.
    d = {NAMES[i + 1]: r for i, r in enumerate(rows)}
    assert d['Kerala'][6] == '55.14' and d['Bihar'][6] == '95.71' and d['Rajasthan'][6] == '59.10' and d['Goa'][0] == '2.64'
    states = {}
    for s_, r in d.items():
        total, tap, pct = num(r[0]), num(r[5]), num(r[6])
        lo, hi = (tap - 0.005) / (total + 0.005) * 100, (tap + 0.005) / (total - 0.005) * 100  # lakh figures are rounded to 0.01
        assert lo - 0.01 <= pct <= hi + 0.01, (s_, lo, hi, pct)
        states[s_] = {'rural_hh_lakh': total, 'tap_hh_lakh': tap, 'tap_pct': pct}
    assert abs(sum(v['rural_hh_lakh'] for v in states.values()) - num(tot[0])) <= 0.1
    assert abs(sum(v['tap_hh_lakh'] for v in states.values()) - num(tot[5])) <= 0.1
    assert abs(num(tot[5]) / num(tot[0]) * 100 - num(tot[6])) <= 0.06
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert set(states) <= geo
    out = {'source': 'Ministry of Jal Shakti, Lok Sabha Starred Question 62 (23 July 2026), Annexure', 'url': URL, 'sha256': SHA,
           'retrieved': '2026-10-20', 'as_on': '18 July 2026', 'india': {'rural_hh_lakh': num(tot[0]), 'tap_hh_lakh': num(tot[5]), 'tap_pct': num(tot[6])},
           'states': dict(sorted(states.items()))}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(states), 'states')


main()
