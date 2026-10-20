#!/usr/bin/env python3
"""Write data/rbi/bank-offices-2025.json from Table 152 of the RBI Handbook of Statistics on Indian States 2024-25.

    python3 scripts/extract_rbi_bank_offices.py [--check]

Source: RBI, Handbook of Statistics on Indian States 2024-25 (11 December 2025), Table 152, offices of scheduled commercial
banks as at end-March, from RBI's Basic Statistical Returns. rbidocs.rbi.org.in sits behind a bot challenge, so the PDF was
read through Firecrawl on 2026-10-19 and the 2024 and 2025 columns are transcribed below, with no SHA-256 pinned. Checks:
the 36 rows add to the printed all-India totals (1,63,216 for 2024 and 1,67,806 for 2025) and the five regional subtotals
printed in the table agree with their states. Offices are bank branches of every kind, counted where the office is, not
where its customers live. Dadra and Nagar Haveli includes Daman and Diu since 2020 (the source's own footnote).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'rbi', 'bank-offices-2025.json')
DNH = 'Dadra and Nagar Haveli and Daman and Diu'
# state: (2024, 2025) offices at end-March
T = {
    'Chandigarh': (466, 461), 'Delhi': (3894, 3981), 'Haryana': (5515, 5683), 'Himachal Pradesh': (1774, 1819),
    'Jammu and Kashmir': (1933, 1996), 'Ladakh': (100, 103), 'Punjab': (6784, 6952), 'Rajasthan': (8552, 8786),
    'Arunachal Pradesh': (206, 229), 'Assam': (3190, 3236), 'Manipur': (250, 261), 'Meghalaya': (388, 394),
    'Mizoram': (235, 241), 'Nagaland': (209, 231), 'Tripura': (634, 646),
    'Andaman and Nicobar': (74, 76), 'Bihar': (7979, 8226), 'Jharkhand': (3399, 3518), 'Odisha': (5712, 5920),
    'Sikkim': (176, 185), 'West Bengal': (9948, 10159),
    'Chhattisgarh': (3092, 3187), 'Madhya Pradesh': (7703, 7949), 'Uttarakhand': (2280, 2343), 'Uttar Pradesh': (18883, 19436),
    DNH: (108, 113), 'Goa': (680, 690), 'Gujarat': (9191, 9513), 'Maharashtra': (14410, 14832),
    'Andhra Pradesh': (7898, 8087), 'Karnataka': (11236, 11395), 'Kerala': (7130, 7380), 'Lakshadweep': (23, 17),
    'Puducherry': (285, 288), 'Tamil Nadu': (12832, 13204), 'Telangana': (6047, 6269),
}
REGIONS = {
    'Northern': (['Chandigarh', 'Delhi', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Ladakh', 'Punjab', 'Rajasthan'], (29018, 29781)),
    'North-Eastern': (['Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Tripura'], (5112, 5238)),
    'Eastern': (['Andaman and Nicobar', 'Bihar', 'Jharkhand', 'Odisha', 'Sikkim', 'West Bengal'], (27288, 28084)),
    'Central': (['Chhattisgarh', 'Madhya Pradesh', 'Uttarakhand', 'Uttar Pradesh'], (31958, 32915)),
    'Western': ([DNH, 'Goa', 'Gujarat', 'Maharashtra'], (24389, 25148)),
    'Southern': (['Andhra Pradesh', 'Karnataka', 'Kerala', 'Lakshadweep', 'Puducherry', 'Tamil Nadu', 'Telangana'], (45451, 46640)),
}
INDIA = (163216, 167806)


def main():
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert not set(T) - geo, sorted(set(T) - geo)
    assert len(T) == 36
    for i in (0, 1):
        assert sum(v[i] for v in T.values()) == INDIA[i], (i, sum(v[i] for v in T.values()), INDIA[i])
        for r, (names, tot) in REGIONS.items():
            assert sum(T[n][i] for n in names) == tot[i], (r, i, sum(T[n][i] for n in names), tot[i])
    out = {'source': 'RBI, Handbook of Statistics on Indian States 2024-25, Table 152 (Basic Statistical Returns of Scheduled Commercial Banks)',
           'url': 'https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=Handbook+of+Statistics+on+Indian+States', 'retrieved': '2026-10-19',
           'unit': 'offices at end-March', 'india': {'2024': INDIA[0], '2025': INDIA[1]},
           'states': {s: {'2024': a, '2025': b} for s, (a, b) in sorted(T.items())}}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(T), 'states, sums and regional subtotals agree')


main()
