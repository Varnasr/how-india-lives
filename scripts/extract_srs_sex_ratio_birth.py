#!/usr/bin/env python3
"""Write data/srs/sex-ratio-birth-2021-23.json from Table 16 of the SRS Statistical Report 2023.

    python3 scripts/extract_srs_sex_ratio_birth.py SRS_STAT_2023.pdf [--check]

Source: ORGI, Sample Registration System Statistical Report 2023 (September 2025), Table 16 (page 315) and Statement 16
(page 66): sex ratio at birth, females per 1000 males, three-year averages 2017-19 to 2021-23, total, rural and urban, for
India and 22 bigger states. The PDF came from the owner's Drive copy of the file on censusindia.gov.in (catalog 46172) and its
SHA-256 is pinned below. Checks: Table 16's 2021-23 columns equal Statement 16 row for row, the India row is 917, the highest
and lowest states match the report's text (Chhattisgarh 974 and Kerala 971, Uttarakhand 868), and each state total lies
between its rural and urban values or within 12 of them (SRS weights births, so the total can sit outside by rounding).
Jammu & Kashmir includes Ladakh. Only the 22 bigger states are covered; the rest are grey.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, GEO, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'srs', 'sex-ratio-birth-2021-23.json')
URL = 'https://censusindia.gov.in/nada/index.php/catalog/46172/download/50420/SRS_STAT_2023.pdf'
SHA = '165b70974389015365a836630280366917820afe089d28e748785c0c1e1b5458'
PERIODS = ['2017-19', '2018-20', '2019-21', '2020-22', '2021-23']


def page(pdf, n):
    return subprocess.run(['pdftotext', '-f', str(n), '-l', str(n), '-layout', pdf, '-'], capture_output=True, text=True).stdout


def main():
    pdf = sys.argv[1]
    assert sha256(pdf) == SHA, 'wrong file'
    t16 = page(pdf, 343)
    assert 'Table 16: Sex Ratio at Birth' in t16
    rows = {}
    for line in t16.splitlines():
        m = re.match(r'^(India|[A-Z][A-Za-z &]+?)\s{2,}((?:\d{3}\s+){14}\d{3})\s*$', line.strip())
        if m:
            v = [int(x) for x in m.group(2).split()]
            rows[m.group(1).strip()] = {'total': v[0:5], 'rural': v[5:10], 'urban': v[10:15]}
    assert len(rows) == 23, sorted(rows)
    s16 = {}
    for line in page(pdf, 93).splitlines():
        m = re.match(r'^\s*(India|[A-Z][A-Za-z &]+?)\s{2,}(\d{3})\s+(\d{3})\s+(\d{3})\s*$', line)
        if m:
            s16[m.group(1).strip()] = [int(m.group(i)) for i in (2, 3, 4)]
    assert len(s16) == 23, sorted(s16)
    for k, r in rows.items():
        assert [r['total'][4], r['rural'][4], r['urban'][4]] == s16[k], (k, s16[k])
    assert rows['India']['total'][4] == 917
    st = {k: v for k, v in rows.items() if k != 'India'}
    assert max(st, key=lambda k: st[k]['total'][4]) == 'Chhattisgarh' and min(st, key=lambda k: st[k]['total'][4]) == 'Uttarakhand'
    assert st['Kerala']['total'][4] == 971 and st['Uttarakhand']['total'][4] == 868
    for k, r in st.items():
        lo, hi = sorted((r['rural'][4], r['urban'][4]))
        assert lo - 12 <= r['total'][4] <= hi + 12, (k, r)
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    states = {}
    for k, r in sorted(st.items()):
        n = GEO.get(k, k.replace('&', 'and'))
        assert n in geo, n
        states[n] = r
    out = {'source': 'ORGI, SRS Statistical Report 2023, Table 16 and Statement 16', 'url': URL, 'sha256': SHA, 'retrieved': '2026-10-20',
           'unit': 'females per 1000 males at birth, three-year average', 'periods': PERIODS, 'india': rows['India'], 'states': states}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(states), 'states')


main()
