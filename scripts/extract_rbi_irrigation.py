#!/usr/bin/env python3
"""Write data/rbi/irrigation-2024.json from Tables 54 and 56 of the RBI Handbook of Statistics on Indian States 2024-25.

    python3 scripts/extract_rbi_irrigation.py [--check]

Source: RBI, Handbook of Statistics on Indian States 2024-25 (11 December 2025), Table 54 (net sown area) and Table 56 (net
irrigated area), thousand hectares, from the Ministry of Agriculture's Land Use Statistics at a Glance. rbidocs.rbi.org.in
sits behind a bot challenge, so the two PDFs were read through Firecrawl on 2026-10-19 and the figures are transcribed
below for 2021-22, 2022-23 and 2023-24(p), with no SHA-256 pinned. Checks: net irrigated never exceeds net sown, and the
all-India rows are 82,416 / 138,992 (2023-24), 79,312 / 140,705 (2022-23) and 77,916 / 141,007 (2021-22).

Three things about the source. 2023-24 is provisional, and it breaks the series in places: Maharashtra's net irrigated
area goes from 3,095 to 6,496 thousand ha in one year, Andhra Pradesh's net sown area falls from 5,725 to 4,955, Manipur's
from 382 to 215 and Jharkhand's from 1,025 to 902. The map therefore uses 2022-23, the latest year not marked provisional,
and keeps 2023-24(p) in the calculation file. Several earlier years carry an asterisk meaning the figure is an estimate or
comes from the Agriculture Census. Ladakh, Chandigarh, Lakshadweep and the Andaman and Nicobar and Dadra islands and
territories are not in the tables.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'rbi', 'irrigation-2024.json')
# state: (net sown 2021-22, 2022-23, 2023-24p), (net irrigated 2021-22, 2022-23, 2023-24p), thousand hectares
T = {
    'Andhra Pradesh': ((6038, 5725, 4955), (2952, 2855, 2603)),
    'Arunachal Pradesh': ((243, 253, 258), (63, 64, 63)),
    'Assam': ((2749, 2744, 2756), (438, 467, 469)),
    'Bihar': ((5070, 5113, 5314), (3082, 3124, 3401)),
    'Chhattisgarh': ((4631, 4592, 4616), (1604, 1535, 1487)),
    'Delhi': ((22, 22, 28), (22, 22, 25)),
    'Goa': ((127, 126, 127), (15, 32, 39)),
    'Gujarat': ((9720, 9748, 9824), (5796, 6186, 6273)),
    'Haryana': ((3611, 3584, 3515), (3579, 3336, 3225)),
    'Himachal Pradesh': ((528, 532, 516), (111, 109, 110)),
    'Jammu and Kashmir': ((733, 733, 738), (315, 311, 311)),
    'Jharkhand': ((1379, 1025, 902), (279, 202, 199)),
    'Karnataka': ((11166, 11161, 10701), (4920, 5038, 4809)),
    'Kerala': ((2029, 1990, 1973), (403, 419, 420)),
    'Madhya Pradesh': ((15823, 15848, 15640), (12903, 12930, 12747)),
    'Maharashtra': ((16590, 16491, 16571), (3103, 3095, 6496)),
    'Manipur': ((393, 382, 215), (62, 57, 57)),
    'Meghalaya': ((269, 274, 274), (102, 105, 105)),
    'Mizoram': ((145, 145, 198), (16, 16, 12)),
    'Nagaland': ((265, 361, 366), (49, 118, 118)),
    'Odisha': ((4322, 4269, 4307), (1238, 1335, 1315)),
    'Puducherry': ((16, 16, 16), (14, 14, 16)),
    'Punjab': ((4113, 4110, 4109), (4113, 4082, 4109)),
    'Rajasthan': ((18130, 18423, 18198), (8924, 9500, 9547)),
    'Sikkim': ((77, 83, 83), (14, 13, 13)),
    'Tamil Nadu': ((4909, 4838, 4756), (2930, 2921, 2885)),
    'Telangana': ((5625, 5897, 5564), (3376, 3866, 3728)),
    'Tripura': ((255, 255, 255), (89, 90, 90)),
    'Uttar Pradesh': ((16096, 16121, 16365), (13941, 14044, 13656)),
    'Uttarakhand': ((594, 568, 551), (315, 313, 310)),
    'West Bengal': ((5281, 5216, 5245), (3127, 3088, 3757)),
}
INDIA = {'net_sown': (141007, 140705, 138992), 'net_irrigated': (77916, 79312, 82416)}
YEARS = ['2021-22', '2022-23', '2023-24(p)']


def main():
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert not set(T) - geo, sorted(set(T) - geo)
    for s, (sown, irr) in T.items():
        for a, b in zip(irr, sown):
            assert a <= b, (s, a, b)
    out = {'source': 'RBI, Handbook of Statistics on Indian States 2024-25, Tables 54 and 56 (Land Use Statistics at a Glance)',
           'url': 'https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=Handbook+of+Statistics+on+Indian+States', 'retrieved': '2026-10-19',
           'unit': 'thousand hectares', 'years': YEARS, 'india': {'net_sown': dict(zip(YEARS, INDIA['net_sown'])), 'net_irrigated': dict(zip(YEARS, INDIA['net_irrigated']))},
           'states': {s: {'net_sown': dict(zip(YEARS, a)), 'net_irrigated': dict(zip(YEARS, b))} for s, (a, b) in sorted(T.items())}}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(T), 'states')


main()
