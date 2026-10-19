#!/usr/bin/env python3
"""Read the state pages of ASER (Rural) 2024 for children not in school into data/aser/not-enrolled-2024.json.

    python3 scripts/extract_aser_enrolment.py ASER2024.pdf [--check]

Each state (and the India) page opens with Table 1, the share of children enrolled in government, private and other
schools and not in school, by age group. The rows used are 'Age 6-14: All' and 'Age 15-16: All' (where printed). Every
row must add to 100 within 0.3 (the printed values are rounded) and the India row must read 1.9 for 6-14. ASER marks
'data is not presented where sample size is insufficient'; a state with no figure stays grey. Household survey, rural
districts only, so the figures say nothing about cities.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'aser', 'not-enrolled-2024.json')
URL = 'https://asercentre.org/wp-content/uploads/2022/12/ASER_2024_Final-Report_13_2_24-1.pdf'


def main():
    pdf = sys.argv[1]
    lines = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.splitlines()
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    alias = {'Jammu & Kashmir': 'Jammu and Kashmir', 'Dadra & Nagar Haveli': 'Dadra and Nagar Haveli and Daman and Diu'}
    res, cur = {}, None
    for i, ln in enumerate(lines):
        m = re.match(r'^\s*([A-Za-z&][A-Za-z& ]+?) RURAL\s', ln)
        if m and any('School enrollment' in x for x in lines[i + 1:i + 8]):
            cur = alias.get(m.group(1).strip(), m.group(1).strip())
            res.setdefault(cur, {})
            continue
        if cur:
            r = re.match(r'^\s*Age (6-14|15-16): All\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(?:100)', ln)
            if r and r.group(1) not in res[cur]:
                v = [float(r.group(k)) for k in (2, 3, 4, 5)]
                assert abs(sum(v) - 100) <= 0.3, (cur, r.group(1), v)
                res[cur][r.group(1)] = {'govt': v[0], 'private': v[1], 'other': v[2], 'not_in_school': v[3]}
    india = res.pop('India')
    assert india['6-14']['not_in_school'] == 1.9, india
    res = {s: d for s, d in res.items() if '6-14' in d}
    bad = sorted(set(res) - geo)
    assert not bad, bad
    vals = [d['6-14']['not_in_school'] for d in res.values()]
    assert min(vals) <= 1.9 <= max(vals)
    out = {'source': 'ASER Centre, ASER (Rural) 2024, provisional, 28 Jan 2025', 'url': URL, 'sha256': sha256(pdf), 'india': india, 'states': dict(sorted(res.items()))}
    print(len(res), 'states', sorted(geo - set(res)))
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')


main()
