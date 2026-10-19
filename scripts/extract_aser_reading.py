#!/usr/bin/env python3
"""Read ASER 2024 (rural) state tables of government-school reading into data/aser/reading-2024.json.

    python3 scripts/extract_aser_reading.py ASER2024.pdf [--check]

Source: ASER Centre, Annual Status of Education Report (Rural) 2024, provisional, 28 January 2025. The state tables give
the share of government-school children in Std III and in Std V who can read a Std II level text, for 2018, 2022 and 2024.
ASER's state tables cover government schools only and rural districts only. Checks: every state's three values lie in
0 to 100, the state names all map to the atlas geojson, and the all-India rural government-school figure in Table 1 of
the report (Std III 23.4, Std V 44.8 in 2024; 16.3 and 38.5 in 2022; 20.9 and 44.2 in 2018) lies inside the range of the
state values. States absent from a table (Delhi, Goa, the smaller UTs) had no published figure and stay grey.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, GEO, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'aser', 'reading-2024.json')
URL = 'https://asercentre.org/wp-content/uploads/2022/12/ASER_2024_Final-Report_13_2_24-1.pdf'
NAT = {'std3': {'2018': 20.9, '2022': 16.3, '2024': 23.4}, 'std5': {'2018': 44.2, '2022': 38.5, '2024': 44.8}}
ROW = re.compile(r'([A-Z][A-Za-z ]+?)\s+(\d{1,2}\.\d)\s+(\d{1,2}\.\d)\s*(\d{1,2}\.\d)?\s*$')


def table(text, head, tail):
    a = text.index(head)
    b = text.index(tail, a)
    rows = {}
    for line in text[a:b].splitlines():
        right = line[100:] if len(line) > 100 else ''
        m = ROW.search(right.strip()) or ROW.search(line.strip())
        if m and m.group(4):
            name = m.group(1).strip()
            if name in ('State',):
                continue
            rows[name] = [float(m.group(2)), float(m.group(3)), float(m.group(4))]
    return rows


def main():
    pdf = sys.argv[1]
    raw = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    out = {'source': 'ASER Centre, ASER (Rural) 2024, provisional, 28 Jan 2025', 'url': URL, 'sha256': sha256(pdf),
           'years': ['2018', '2022', '2024'], 'national_govt': NAT}
    for key, head in (('std3', 'children in Std III who can read Std II level text, 2024'),
                      ('std5', 'children in Std V who can read Std II level text, 2024')):
        a = raw.index(head)
        seg = raw[a:a + 12000]
        end = seg.index('Annual Status of Education Report 2024') if 'Annual Status of Education Report 2024' in seg else len(seg)
        rows = {}
        for line in seg[:end].splitlines():
            m = re.search(r'(?:^|\s{2,})([A-Z][a-z]+(?: [A-Za-z]+)*)\s+(\d{1,2}\.\d)\s+(\d{1,2}\.\d)\s+(\d{1,2}\.\d)\s*$', line)
            if m:
                rows[m.group(1).strip()] = [float(m.group(i)) for i in (2, 3, 4)]
        geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
        bad = sorted(set(rows) - geo)
        assert not bad, bad
        for n, v in rows.items():
            assert all(0 <= x <= 100 for x in v), (n, v)
        for y, i in (('2018', 0), ('2022', 1), ('2024', 2)):
            vals = [v[i] for v in rows.values()]
            assert min(vals) <= NAT[key][y] <= max(vals), (key, y, NAT[key][y], min(vals), max(vals))
        out[key] = {n: dict(zip(out['years'], v)) for n, v in sorted(rows.items())}
        print(key, len(rows), 'states')
    assert len(out['std5']) == 27 and len(out['std3']) >= 27, (len(out['std5']), len(out['std3']))
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
        print('ok')
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')


main()
