#!/usr/bin/env python3
"""Write data/msme/udyam-registrations-2025-11.json from Annexure I of Lok Sabha Unstarred Question 755 (4 December 2025).

    python3 scripts/extract_udyam_msme.py AU755.pdf [--check]

Source: Ministry of Micro, Small and Medium Enterprises, reply to Lok Sabha Unstarred Question 755 of 4 December 2025, Annexure I:
MSMEs registered on the Udyam Registration Portal and the Udyam Assist Platform (informal micro enterprises) by state and
financial year, 1 July 2020 to 30 November 2025. The PDF is from sansad.in (SHA-256 pinned below). Only the "MSMEs Registered"
columns are read. Check: in each of the six years the 36 state rows add to the printed Total row, and the six years together
give 7,22,32,207 registrations, the 7.22 crore the Ministry quoted for November 2025. This counts registrations at the registered
address, including informal micro enterprises onboarded since January 2023, so it is not a count of working firms.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'msme', 'udyam-registrations-2025-11.json')
SHA = '134f146652ff669a54e2c48d76c0ca1ddcb08a39cd93ddf25df0d3ff8d341f95'
URL = 'https://sansad.in/getFile/loksabhaquestions/annex/186/AU755_oHVS7d.pdf?source=pqals'
YEARS = ['2020-21', '2021-22', '2022-23', '2023-24', '2024-25', '2025-26 (to 30 Nov)']
NAMES = {1: 'Andaman and Nicobar', 2: 'Andhra Pradesh', 3: 'Arunachal Pradesh', 4: 'Assam', 5: 'Bihar', 6: 'Chandigarh', 7: 'Chhattisgarh',
         8: 'Delhi', 9: 'Goa', 10: 'Gujarat', 11: 'Haryana', 12: 'Himachal Pradesh', 13: 'Jammu and Kashmir', 14: 'Jharkhand',
         15: 'Karnataka', 16: 'Kerala', 17: 'Ladakh', 18: 'Lakshadweep', 19: 'Madhya Pradesh', 20: 'Maharashtra', 21: 'Manipur',
         22: 'Meghalaya', 23: 'Mizoram', 24: 'Nagaland', 25: 'Odisha', 26: 'Puducherry', 27: 'Punjab', 28: 'Rajasthan', 29: 'Sikkim',
         30: 'Tamil Nadu', 31: 'Telangana', 32: 'Dadra and Nagar Haveli and Daman and Diu', 33: 'Tripura', 34: 'Uttar Pradesh',
         35: 'Uttarakhand', 36: 'West Bengal'}
TOTAL_YEARS = 72232207


def main():
    pdf = sys.argv[1]
    assert sha256(pdf) == SHA, 'wrong file'
    text = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    a = text.index('Annexure referred to in reply to part (a)')
    seg = text[a:text.index('Annexure-II', a)].splitlines()
    ints = lambda toks: [int(x.replace(',', '')) for x in toks[0::2]]
    rows, total = {}, None
    for line in seg:
        if 'Total:-' in line:
            total = ints(re.findall(r'\d[\d,]*', line))
            continue
        m = re.match(r'^\s*(\d{1,2})\s+([A-Z][A-Z ,&]*?)\s{2,}(.*)$', line)
        if m and re.search(r'\d', m.group(3)):
            rows[int(m.group(1))] = ints(re.findall(r'\d[\d,]*', m.group(3)))
    assert sorted(rows) == list(range(1, 37)) and all(len(v) == 6 for v in rows.values())
    for i in range(6):
        assert sum(v[i] for v in rows.values()) == total[i], (i, sum(v[i] for v in rows.values()), total[i])
    assert sum(total) == TOTAL_YEARS
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert set(NAMES.values()) == geo
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out = {'source': 'Ministry of MSME, Lok Sabha Unstarred Question 755 (4 December 2025), Annexure I', 'url': URL, 'sha256': SHA,
           'retrieved': '2026-10-20', 'as_on': '30 November 2025', 'years': YEARS, 'unit': 'registrations on Udyam and Udyam Assist',
           'india_total': TOTAL_YEARS, 'states': {NAMES[k]: v for k, v in sorted(rows.items(), key=lambda kv: NAMES[kv[0]])}}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(rows), 'states')


main()
