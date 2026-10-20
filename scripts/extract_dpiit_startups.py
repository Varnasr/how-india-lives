#!/usr/bin/env python3
"""Write data/dpiit/startups-2026-06.json from Annexure I of Lok Sabha Unstarred Question 1446 (28 July 2026).

    python3 scripts/extract_dpiit_startups.py [--check]

Source: Department for Promotion of Industry and Internal Trade, reply to Lok Sabha Unstarred Question 1446 of 28 July 2026,
Annexure I: entities recognised as startups by DPIIT as on 30 June 2026, by State and UT. The annexure was read from sansad.in
through Firecrawl on 2026-10-20 and is transcribed below, with no SHA-256 pinned. Check: the 36 rows add to the 2,40,092 the
answer states for the whole country, and Odisha (4,123) and Karnataka (24,026) match the figures the answer gives in its text.
A recognised startup is counted at its registered address, which concentrates in Delhi, Karnataka and Maharashtra.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'dpiit', 'startups-2026-06.json')
T = {
    'Andaman and Nicobar': 108,
    'Andhra Pradesh': 4707,
    'Arunachal Pradesh': 102,
    'Assam': 2351,
    'Bihar': 5527,
    'Chandigarh': 740,
    'Chhattisgarh': 2587,
    'Dadra and Nagar Haveli and Daman and Diu': 102,
    'Delhi': 22336,
    'Goa': 861,
    'Gujarat': 21019,
    'Haryana': 12482,
    'Himachal Pradesh': 898,
    'Jammu and Kashmir': 1628,
    'Jharkhand': 2304,
    'Karnataka': 24026,
    'Kerala': 9092,
    'Ladakh': 25,
    'Lakshadweep': 3,
    'Madhya Pradesh': 8194,
    'Maharashtra': 41440,
    'Manipur': 295,
    'Meghalaya': 106,
    'Mizoram': 78,
    'Nagaland': 131,
    'Odisha': 4123,
    'Puducherry': 263,
    'Punjab': 2708,
    'Rajasthan': 8783,
    'Sikkim': 21,
    'Tamil Nadu': 15774,
    'Telangana': 13622,
    'Tripura': 233,
    'Uttar Pradesh': 23678,
    'Uttarakhand': 1970,
    'West Bengal': 7775,
}
TOTAL = 240092


def main():
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert set(T) == geo, sorted(set(T) ^ geo)
    assert sum(T.values()) == TOTAL, sum(T.values())
    assert T['Odisha'] == 4123 and T['Karnataka'] == 24026
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out = {'source': 'DPIIT, Lok Sabha Unstarred Question 1446, 28 July 2026, Annexure I',
           'url': 'https://sansad.in/getFile/lsapps/loksabhaquestions/annex/188/AU1446_N4i3CT.pdf?source=lsapps', 'retrieved': '2026-10-20',
           'as_on': '30 June 2026', 'unit': 'entities recognised as startups', 'india': TOTAL, 'states': T}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(T), 'states')


main()
