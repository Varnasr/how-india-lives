#!/usr/bin/env python3
"""Write data/cgwb/assessment-units-2025.json from the categorisation table of the CGWB National Compilation 2025.

    python3 scripts/extract_cgwb_units.py [--check]

Source: Central Ground Water Board and Ministry of Jal Shakti, National Compilation on Dynamic Ground Water Resources of India,
2025 (November 2025), "Categorization of blocks/mandals/talukas in India (2025)" (printed page 187, PDF page 213). The PDF was
downloaded from jalshakti-dowr.gov.in on 2026-10-20 (SHA-256 below) and the table transcribed. Columns: units assessed, safe,
semi-critical, critical, over-exploited, saline. A blank in the table is a zero. Checks: each row's categories add to its total,
and the 36 rows add to the printed Grand Total (6,762 units: 4,946 safe, 758 semi-critical, 201 critical, 730 over-exploited,
127 saline). A unit is a block, taluk, mandal or district depending on the state, so units differ widely in size.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'cgwb', 'assessment-units-2025.json')
SHA = 'f2453ccf635761707926610e5d96300ae0ab1abf748a860bc3b3a998a32f7b8a'
URL = 'https://www.jalshakti-dowr.gov.in/static/uploads/2025/11/711d8d476bbf498cd90f8038e7371227.pdf'
# state: (assessed, safe, semi-critical, critical, over-exploited, saline)
T = {
    'Andhra Pradesh': (679, 601, 24, 3, 12, 39),
    'Arunachal Pradesh': (42, 42, 0, 0, 0, 0),
    'Assam': (245, 244, 1, 0, 0, 0),
    'Bihar': (535, 471, 49, 12, 3, 0),
    'Chhattisgarh': (146, 120, 21, 5, 0, 0),
    'Goa': (12, 12, 0, 0, 0, 0),
    'Gujarat': (252, 181, 31, 3, 25, 12),
    'Haryana': (143, 31, 15, 6, 91, 0),
    'Himachal Pradesh': (26, 26, 0, 0, 0, 0),
    'Jharkhand': (263, 240, 12, 5, 6, 0),
    'Karnataka': (237, 145, 36, 11, 45, 0),
    'Kerala': (152, 123, 27, 2, 0, 0),
    'Madhya Pradesh': (317, 221, 64, 6, 26, 0),
    'Maharashtra': (359, 306, 40, 5, 7, 1),
    'Manipur': (9, 9, 0, 0, 0, 0),
    'Meghalaya': (40, 40, 0, 0, 0, 0),
    'Mizoram': (26, 26, 0, 0, 0, 0),
    'Nagaland': (52, 52, 0, 0, 0, 0),
    'Odisha': (314, 298, 10, 0, 0, 6),
    'Punjab': (153, 17, 15, 10, 111, 0),
    'Rajasthan': (302, 36, 27, 23, 213, 3),
    'Sikkim': (38, 38, 0, 0, 0, 0),
    'Tamil Nadu': (313, 121, 61, 23, 103, 5),
    'Telangana': (620, 473, 105, 19, 23, 0),
    'Tripura': (59, 59, 0, 0, 0, 0),
    'Uttar Pradesh': (836, 563, 171, 48, 54, 0),
    'Uttarakhand': (20, 16, 4, 0, 0, 0),
    'West Bengal': (345, 242, 34, 9, 0, 60),
    'Andaman and Nicobar': (9, 9, 0, 0, 0, 0),
    'Chandigarh': (1, 1, 0, 0, 0, 0),
    'Dadra and Nagar Haveli and Daman and Diu': (3, 3, 0, 0, 0, 0),
    'Delhi': (34, 7, 6, 11, 10, 0),
    'Jammu and Kashmir': (149, 149, 0, 0, 0, 0),
    'Ladakh': (18, 17, 1, 0, 0, 0),
    'Lakshadweep': (5, 4, 1, 0, 0, 0),
    'Puducherry': (8, 3, 3, 0, 1, 1),
}
GRAND = (6762, 4946, 758, 201, 730, 127)
# over-exploited units nationally: 2024 assessment, printed in the same compilation (751 of 6,746 units, 11.13 per cent)
PREV_OE = (751, 11.13)


def main():
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert set(T) == geo, sorted(set(T) ^ geo)
    for s, v in T.items():
        assert sum(v[1:]) == v[0], (s, v)
    for i in range(6):
        assert sum(v[i] for v in T.values()) == GRAND[i], (i, sum(v[i] for v in T.values()))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    keys = ('assessed', 'safe', 'semi_critical', 'critical', 'over_exploited', 'saline')
    out = {'source': 'CGWB / Ministry of Jal Shakti, National Compilation on Dynamic Ground Water Resources of India, 2025', 'url': URL,
           'sha256': SHA, 'retrieved': '2026-10-20', 'unit': 'assessment units (blocks, taluks or mandals)',
           'india': dict(zip(keys, GRAND)), 'states': {s: dict(zip(keys, v)) for s, v in sorted(T.items())}}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(T), 'states')


main()
