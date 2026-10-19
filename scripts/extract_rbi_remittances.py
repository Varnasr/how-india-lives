#!/usr/bin/env python3
"""Read Table 2 of the RBI Bulletin article on India's Remittances Survey (sixth round, 2023-24) into data/rbi/remittances-2023-24.json.

    python3 scripts/extract_rbi_remittances.py BULLETIN.html [--check]

Source: Gajbhiye et al., 'Changing Dynamics of India's Remittances: Insights from the Sixth Round of India's Remittances
Survey', RBI Bulletin, 19 March 2025 (https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=23260). Table 2 gives each
state's and UT's share of India's inward remittances for 2016-17, 2020-21 and 2023-24. The shares are of remittances
received (family maintenance, savings and withdrawals from non-resident deposits), in per cent, and a dash means the
state was not shown separately in that round. Checks: 36 states and UTs in 2023-24, shares add to 100 within 0.5 (the
printed values are rounded), and the article's text (Maharashtra 20.5, Kerala 19.7, Tamil Nadu 10.4, Telangana 8.1,
Karnataka 7.7) matches the table. A share is not remittances per person: it says where remittances land in total, which
follows population and migration together.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'rbi', 'remittances-2023-24.json')
URL = 'https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=23260'
NAMES = {'Delhi NCT': 'Delhi', 'Dadra & Nagar Haveli and Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu',
         'Lakshwadeep': 'Lakshadweep', 'Andaman & Nicobar': 'Andaman and Nicobar'}


def main():
    t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', open(sys.argv[1], errors='ignore').read()))
    a = t.index('Table 2: State-wise/UT-wise Share of India')
    seg = t[a:t.index('Note: (i) For 2023-24', a)]
    seg = seg[seg.index('2023-24 Destination State 2016-17 2020-21 2023-24') + len('2023-24 Destination State 2016-17 2020-21 2023-24'):]
    rows = {}
    for m in re.finditer(r'([A-Za-z][A-Za-z&. ]*?) (–|[\d.]+) (–|[\d.]+) ([\d.]+)(?= [A-Z]|$)', seg.strip()):
        n = NAMES.get(m.group(1).strip(), m.group(1).strip())
        f = lambda x: None if x == '–' else float(x)
        rows[n] = {'2016-17': f(m.group(2)), '2020-21': f(m.group(3)), '2023-24': f(m.group(4))}
    assert len(rows) == 36, (len(rows), sorted(rows))
    tot = sum(r['2023-24'] for r in rows.values())
    assert abs(tot - 100) <= 0.5, tot
    for k, v in (('Maharashtra', 20.5), ('Kerala', 19.7), ('Tamil Nadu', 10.4), ('Telangana', 8.1), ('Karnataka', 7.7)):
        assert rows[k]['2023-24'] == v, k
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert not set(rows) - geo, sorted(set(rows) - geo)
    out = {'source': "RBI Bulletin, March 2025, 'Changing Dynamics of India's Remittances', Table 2 (sixth round of the Remittances Survey, 2023-24)",
           'url': URL, 'sha256_of_saved_page': sha256(sys.argv[1]), 'total_usd_bn_2023_24': 118.7, 'sum_of_shares_2023_24': round(tot, 2), 'states': dict(sorted(rows.items()))}
    print(len(rows), 'rows, shares sum', round(tot, 2), 'missing', sorted(geo - set(rows)))
    if '--check' in sys.argv:
        o = json.load(open(OUT)); o.pop('sha256_of_saved_page'); out.pop('sha256_of_saved_page')
        assert o == out, 'stale'
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')


main()
