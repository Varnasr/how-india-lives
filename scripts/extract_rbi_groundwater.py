#!/usr/bin/env python3
"""Write data/rbi/groundwater-2024.json from Table 107 of the RBI Handbook of Statistics on Indian States 2024-25.

    python3 scripts/extract_rbi_groundwater.py [--check]

Source: RBI, Handbook of Statistics on Indian States 2024-25 (11 December 2025), Table 107, from the Central Ground Water
Board's National Compilation on Dynamic Ground Water Resources. Billion cubic metres a year. rbidocs.rbi.org.in sits behind
a bot challenge, so the PDF was read through Firecrawl on 2026-10-19 and the 2023 and 2024 assessments are transcribed
below, with no SHA-256 pinned. Stage of extraction is extraction over extractable resource. Checks: the stage printed for
every state with an extractable resource of 1 BCM or more equals extraction over resource within 2 per cent of itself or the
rounding of the two-decimal BCM figures, whichever is larger (smaller states cannot be recomputed), the all-India 2024 figures give 60.5 per
cent, and 36 states and territories carry a 2024 stage once Daman and Diu, clubbed with Dadra and Nagar Haveli in 2024,
is dropped. A stage above 100 means more is drawn than the assessment counts as recharged each year.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'rbi', 'groundwater-2024.json')
DNH = 'Dadra and Nagar Haveli and Daman and Diu'
# state: (resource 2023, extraction 2023, stage 2023, resource 2024, extraction 2024, stage 2024); None where not assessed
T = {
    'Andaman and Nicobar': (0.557, 0.008, 1.37, 0.34, 0.01, 2.08),
    'Andhra Pradesh': (26.45, 7.48, 28.3, 26.41, 7.88, 29.83),
    'Arunachal Pradesh': (4.16, 0.02, 0.42, 3.46, 0.01, 0.39),
    'Assam': (20.93, 2.63, 12.54, 20.89, 2.64, 12.61),
    'Bihar': (30.72, 13.75, 44.76, 30.95, 14.10, 45.54),
    'Chandigarh': (0.048, 0.037, 75.41, 0.05, 0.03, 66.13),
    'Chhattisgarh': (12.18, 5.75, 47.17, 12.93, 6.12, 47.32),
    DNH: (None, None, None, 0.12, 0.16, 142.17),
    'Delhi': (0.34, 0.34, 99.13, 0.34, 0.34, 100.77),
    'Goa': (0.317, 0.068, 21.37, 0.31, 0.07, 22.91),
    'Gujarat': (25.41, 13.13, 51.68, 25.58, 13.86, 54.21),
    'Haryana': (8.69, 11.8, 135.74, 9.36, 12.72, 135.96),
    'Himachal Pradesh': (1.01, 0.35, 34.95, 1.01, 0.36, 35.48),
    'Jammu and Kashmir': (4.46, 1.08, 24.20, 2.3, 0.51, 22.28),
    'Jharkhand': (5.73, 1.8, 31.38, 5.76, 1.81, 31.43),
    'Karnataka': (17.08, 11.32, 66.26, 16.88, 11.55, 68.44),
    'Kerala': (5.01, 2.73, 54.55, 5.13, 2.76, 53.78),
    'Ladakh': (0.08, 0.03, 37.05, 0.06, 0.02, 30.93),
    'Lakshadweep': (0.005, 0.003, 61.723, 0.01, 0.00, 61.32),
    'Madhya Pradesh': (32.85, 19.3, 58.75, 33.99, 19.85, 58.40),
    'Maharashtra': (30.95, 16.66, 53.83, 31.15, 16.50, 52.99),
    'Manipur': (0.47, 0.04, 7.99, 0.47, 0.04, 8.00),
    'Meghalaya': (1.51, 0.07, 4.58, 1.53, 0.07, 4.60),
    'Mizoram': (0.2, 0.01, 3.70, 0.19, 0.01, 3.95),
    'Nagaland': (0.54, 0.02, 3.76, 0.56, 0.03, 4.72),
    'Odisha': (15.94, 7.39, 46.33, 16.04, 7.74, 48.23),
    'Puducherry': (0.18, 0.13, 70.27, 0.17, 0.13, 75.91),
    'Punjab': (16.98, 27.8, 163.76, 17.63, 27.66, 156.87),
    'Rajasthan': (11.25, 16.74, 148.77, 11.37, 17.05, 149.86),
    'Sikkim': (0.219, 0.012, 5.54, 0.22, 0.01, 5.85),
    'Tamil Nadu': (19.51, 14.42, 73.91, 19.46, 14.45, 74.26),
    'Telangana': (20.92, 8.09, 38.65, 18.44, 8.47, 45.91),
    'Tripura': (1.09, 0.11, 9.92, 1.18, 0.11, 9.48),
    'Uttar Pradesh': (65.57, 46.4, 70.76, 66.38, 46.76, 70.45),
    'Uttarakhand': (1.85, 0.95, 51.69, 1.96, 1.05, 53.54),
    'West Bengal': (23.9, 10.71, 44.81, 23.56, 10.75, 45.63),
}
INDIA = {'2023': (407.21, 241.34, 59.26), '2024': (406.194, 245.646, 60.475)}


def main():
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert not set(T) - geo, sorted(set(T) - geo)
    assert len(T) == 36
    for s, (r3, e3, s3, r4, e4, s4) in T.items():
        for r, e, st in ((r3, e3, s3), (r4, e4, s4)):
            if r is not None and r >= 1:
                assert abs(e / r * 100 - st) <= max(0.02 * st, 0.5 / r + 0.5 * st * 0.01), (s, e / r * 100, st)
    assert abs(INDIA['2024'][1] / INDIA['2024'][0] * 100 - INDIA['2024'][2]) < 0.05
    out = {'source': 'RBI, Handbook of Statistics on Indian States 2024-25, Table 107 (CGWB National Compilation on Dynamic Ground Water Resources)',
           'url': 'https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=Handbook+of+Statistics+on+Indian+States', 'retrieved': '2026-10-19',
           'unit': 'billion cubic metres a year; stage in per cent', 'india': {k: dict(zip(('resource', 'extraction', 'stage'), v)) for k, v in INDIA.items()},
           'states': {s: {'2023': dict(zip(('resource', 'extraction', 'stage'), v[:3])), '2024': dict(zip(('resource', 'extraction', 'stage'), v[3:]))} for s, v in sorted(T.items())}}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(T), 'states')


main()
