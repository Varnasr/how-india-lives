#!/usr/bin/env python3
"""Write data/cgwb/rainfall-2024.json from the state-wise rainfall table of the CGWB National Compilation 2025.

    python3 scripts/extract_cgwb_rainfall.py CGWB_2025.pdf [--check]

Source: Central Ground Water Board and Ministry of Jal Shakti, National Compilation on Dynamic Ground Water Resources of India,
2025 (November 2025), "State-wise Monthly Rainfall (mm)" tables (printed pages 39 and 40, PDF pages 65 and 66), which give each
state's normal rainfall and its rainfall in calendar year 2024, from India Meteorological Department data. The PDF is pinned by
SHA-256. Rows whose name wraps in the layout text (Arunachal Pradesh, Jammu and Kashmir, Dadra and Nagar Haveli and Daman and Diu,
Lakshadweep) are placed by serial number. Checks: 36 rows; the report's own text agrees (Ladakh the lowest normal at 50.9 mm and
Meghalaya the highest at 3,751.5 mm; for 2024 Goa 4,906.6, Meghalaya 3,446.4, Dadra and Nagar Haveli and Daman and Diu 2,996.6 and
Ladakh 79.3 mm), and 18 states and UTs are below normal, the count the report states.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'cgwb', 'rainfall-2024.json')
SHA = 'f2453ccf635761707926610e5d96300ae0ab1abf748a860bc3b3a998a32f7b8a'
URL = 'https://www.jalshakti-dowr.gov.in/static/uploads/2025/11/711d8d476bbf498cd90f8038e7371227.pdf'
NAMES = {1: 'Arunachal Pradesh', 2: 'Assam', 3: 'Meghalaya', 4: 'Nagaland', 5: 'Manipur', 6: 'Mizoram', 7: 'Tripura', 8: 'Sikkim',
         9: 'West Bengal', 10: 'Jharkhand', 11: 'Bihar', 12: 'Uttar Pradesh', 13: 'Uttarakhand', 14: 'Haryana', 15: 'Chandigarh',
         16: 'Delhi', 17: 'Punjab', 18: 'Himachal Pradesh', 19: 'Jammu and Kashmir', 20: 'Ladakh', 21: 'Rajasthan', 22: 'Odisha',
         23: 'Madhya Pradesh', 24: 'Gujarat', 25: 'Dadra and Nagar Haveli and Daman and Diu', 26: 'Goa', 27: 'Maharashtra',
         28: 'Chhattisgarh', 29: 'Andaman and Nicobar', 30: 'Andhra Pradesh', 31: 'Telangana', 32: 'Tamil Nadu', 33: 'Puducherry',
         34: 'Karnataka', 35: 'Kerala', 36: 'Lakshadweep'}
ROW = re.compile(r'^\s*(\d{1,2})\s+(.*?)\s{2,}((?:-?\d+\.\d\s+){21}-?\d+\.\d)\s*$')


def main():
    pdf = sys.argv[1]
    assert sha256(pdf) == SHA, 'wrong file'
    rows = {}
    for n in (65, 66):
        text = subprocess.run(['pdftotext', '-f', str(n), '-l', str(n), '-layout', pdf, '-'], capture_output=True, text=True).stdout
        for line in text.splitlines():
            m = ROW.match(line)
            if m:
                v = [float(x) for x in m.group(3).split()]
                rows[int(m.group(1))] = {'normal': v[17], 'rain_2024': v[18]}
    assert sorted(rows) == list(range(1, 37)), sorted(rows)
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert set(NAMES.values()) == geo
    st = {NAMES[k]: v for k, v in rows.items()}
    assert min(v['normal'] for v in st.values()) == st['Ladakh']['normal'] == 50.9 and max(v['normal'] for v in st.values()) == st['Meghalaya']['normal'] == 3751.5
    assert st['Goa']['rain_2024'] == 4906.6 and st['Meghalaya']['rain_2024'] == 3446.4 and st['Ladakh']['rain_2024'] == 79.3
    assert st['Dadra and Nagar Haveli and Daman and Diu']['rain_2024'] == 2996.6
    assert sum(1 for v in st.values() if v['rain_2024'] < v['normal']) == 18
    out = {'source': 'CGWB / Ministry of Jal Shakti, National Compilation on Dynamic Ground Water Resources of India, 2025 (rainfall from IMD)', 'url': URL,
           'sha256': SHA, 'retrieved': '2026-10-20', 'unit': 'mm', 'states': dict(sorted(st.items()))}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(st), 'states')


main()
