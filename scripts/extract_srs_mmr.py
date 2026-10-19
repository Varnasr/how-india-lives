#!/usr/bin/env python3
"""Write data/srs/mmr-2022-24.json from Table 1 of the SRS Special Bulletin on Maternal Mortality in India 2022-24.

    python3 scripts/extract_srs_mmr.py [--check]

Source: Office of the Registrar General, India, Sample Registration System, Special Bulletin on Maternal Mortality in India
2022-24, Table 1 (https://censusindia.gov.in/nada/index.php/catalog/47151). censusindia.gov.in serves an incomplete
certificate chain, so the PDF could not be downloaded here and no SHA-256 is pinned; the table text below was read from a
text extraction of the PDF on 2026-10-19 and is held to these checks instead: each state's MMR lies inside its printed 95%
confidence interval, the India figure is 87 (78 to 95), the bulletin text agrees (87 for 2022-24, 88 for 2021-23), and
19 states are shown separately, the other states and UTs being pooled as 'Other states' (84), which is never mapped.
Estimates pool three years of births and rest on few deaths, so the intervals are wide (Kerala 0 to 50) and a
difference between two states is usually inside the noise. MMR is maternal deaths per 100,000 live births.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'srs', 'mmr-2022-24.json')
TABLE = """
INDIA | 87 | (78,95) | 5 | 0.18%
Assam | 84 | (35,134) | 5 | 0.17%
Bihar | 96 | (62,130) | 9 | 0.32%
Jharkhand | 82 | (29,136) | 6 | 0.20%
Madhya Pradesh | 135 | (93,176) | 11 | 0.38%
Chhattisgarh | 124 | (48,199) | 9 | 0.31%
Odisha | 124 | (74,175) | 7 | 0.24%
Rajasthan | 87 | (51,124) | 7 | 0.25%
Uttar Pradesh | 154 | (115,192) | 13 | 0.44%
Uttarakhand | 99 | (52,146) | 6 | 0.21%
Andhra Pradesh | 39 | (9,69) | 2 | 0.07%
Telangana | 48 | (8,89) | 3 | 0.09%
Karnataka | 73 | (37,108) | 3 | 0.12%
Kerala | 24 | (0,50) | 1 | 0.04%
Tamil Nadu | 25 | (3,46) | 1 | 0.04%
Gujarat | 64 | (33,95) | 4 | 0.14%
Haryana | 94 | (47,141) | 6 | 0.22%
Maharashtra | 37 | (14,61) | 2 | 0.07%
Punjab | 77 | (23,132) | 4 | 0.13%
West Bengal | 94 | (56,132) | 4 | 0.15%
Other states | 84 | (62,107) | 4 | 0.14%
"""


def main():
    rows = {}
    for ln in TABLE.strip().splitlines():
        n, mmr, ci, rate, risk = [x.strip() for x in ln.split('|')]
        lo, hi = map(int, re.findall(r'\d+', ci))
        assert lo <= int(mmr) <= hi, (n, mmr, ci)
        rows[n] = {'mmr': int(mmr), 'ci_low': lo, 'ci_high': hi, 'mortality_rate': int(rate), 'lifetime_risk': risk}
    india = rows.pop('INDIA')
    other = rows.pop('Other states')
    assert india['mmr'] == 87 and len(rows) == 19
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert not set(rows) - geo, sorted(set(rows) - geo)
    assert min(r['mmr'] for r in rows.values()) <= 87 <= max(r['mmr'] for r in rows.values())
    out = {'source': 'ORGI, SRS Special Bulletin on Maternal Mortality in India 2022-24, Table 1', 'url': 'https://censusindia.gov.in/nada/index.php/catalog/47151',
           'retrieved': '2026-10-19', 'unit': 'maternal deaths per 100,000 live births', 'india': india, 'other_states_pooled': other, 'previous_india_2021_23': 88,
           'states': rows}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(rows), 'states')


main()
