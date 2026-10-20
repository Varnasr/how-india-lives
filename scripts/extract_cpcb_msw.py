#!/usr/bin/env python3
"""Write data/cpcb/solid-waste-2023-24.json from the annexure to Lok Sabha Unstarred Question 50 (1 December 2025).

    python3 scripts/extract_cpcb_msw.py AU50.pdf [--check]

Source: Ministry of Environment, Forest and Climate Change, reply to Lok Sabha Unstarred Question 50 of 1 December 2025,
Annexure: solid waste generated, collected and treated in tonnes a day in 2023-24 as submitted by 36 State Pollution Control Boards
and Pollution Control Committees under the Solid Waste Management Rules, 2016 (CPCB annual reports). The PDF is from sansad.in
(SHA-256 pinned below). Checks: 36 rows in the printed order, and each column adds to the printed total (1,85,195 generated,
1,79,479 collected, 1,14,110 treated tonnes a day). The A&N Islands row wraps onto the line above its name in the PDF and is read
by order. Figures are the boards' own reports, produced by different methods (weighbridge or estimate), and some states report
urban waste only, so they are not strictly comparable.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'cpcb', 'solid-waste-2023-24.json')
SHA = '1cad0928216b3879e201f305037f92e376341f8f61e7a02f3326aa54be9a9ed2'
URL = 'https://sansad.in/getFile/loksabhaquestions/annex/186/AU50_IQkGYW.pdf?source=pqals'
NAMES = ['Andhra Pradesh', 'Andaman and Nicobar', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
         'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir',
         'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
         'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
         'Uttarakhand', 'West Bengal']
TOTALS = (185195, 179479, 114110)


def main():
    pdf = sys.argv[1]
    assert sha256(pdf) == SHA, 'wrong file'
    t = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    seg = t[t.index('Overall Solid Waste Management Status'):].splitlines()
    num = r'(\d[\d,]*\.?\d*)\*?'
    trip = re.compile(r'^(?:\s*\d{1,2}\s+(?:[A-Za-z&. ]+?)|\s*Total)?\s+' + num + r'\s+' + num + r'\s+' + num + r'\s*$')
    rows, tot = [], None
    for l in seg:
        m = trip.match(l)
        if not m:
            continue
        v = [float(x.replace(',', '')) for x in m.groups()]
        if re.match(r'^\s*Total', l):
            tot = v
        else:
            rows.append(v)
    assert len(rows) == 36, len(rows)
    d = dict(zip(NAMES, rows))
    assert d['Maharashtra'][0] == 24299.43 and d['West Bengal'][0] == 14072.04 and d['Andaman and Nicobar'][0] == 77.3 and d['Delhi'][0] == 11342
    for i in range(3):
        assert round(sum(r[i] for r in rows)) == TOTALS[i] == tot[i], (i, sum(r[i] for r in rows))
    out = {'source': 'Ministry of Environment, Forest and Climate Change, Lok Sabha Unstarred Question 50 (1 December 2025), Annexure (CPCB, 2023-24)',
           'url': URL, 'sha256': SHA, 'retrieved': '2026-10-20', 'year': '2023-24', 'unit': 'tonnes a day',
           'india': {'generated': TOTALS[0], 'collected': TOTALS[1], 'treated': TOTALS[2]},
           'states': {s: {'generated': r[0], 'collected': r[1], 'treated': r[2]} for s, r in sorted(d.items())}}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(d), 'states')


main()
