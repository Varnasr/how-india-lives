#!/usr/bin/env python3
"""Write data/srs/marriage-age-2023.json from Statement 13 of the SRS Statistical Report 2023.

    python3 scripts/extract_srs_marriage_age.py SRS_STAT_2023.pdf [--check]

Source: ORGI, Sample Registration System Statistical Report 2023 (September 2025), Statement 13 (page 53): mean age at effective
marriage of females, 2023, by residence, with the mean for marriages below 18, at 18-20 and at 21 and over, for India and 22
bigger states. The PDF (catalog 46172 on censusindia.gov.in, the owner's Drive copy) is pinned by SHA-256. Checks: the India
figure is 22.9, the all-ages total lies between the rural and urban values wherever both are printed, each total sits within
the range of its three age-band means, and every state name is in the atlas geometry. A dash in the source (no marriages in that
cell in the sample) is left out. Jammu & Kashmir includes Ladakh. This is the mean age at which a marriage took effect for
women whose marriage was recorded in the year, not the age of all married women.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, GEO, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'srs', 'marriage-age-2023.json')
URL = 'https://censusindia.gov.in/nada/index.php/catalog/46172/download/50420/SRS_STAT_2023.pdf'
SHA = '165b70974389015365a836630280366917820afe089d28e748785c0c1e1b5458'
NUM = r'(\d{2}\.\d|-)'


def main():
    pdf = sys.argv[1]
    assert sha256(pdf) == SHA, 'wrong file'
    text = subprocess.run(['pdftotext', '-f', '80', '-l', '80', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    assert 'Statement 13' in text
    rows = {}
    for line in text.splitlines():
        m = re.match(r'^\s*(India|[A-Z][A-Za-z &]+?)\s{2,}((?:%s\s+){11}%s)\s*$' % (NUM, NUM), line)
        if m:
            v = [None if x == '-' else float(x) for x in m.group(2).split()]
            rows[m.group(1).strip()] = {'total': v[0:4], 'rural': v[4:8], 'urban': v[8:12]}
    assert len(rows) == 23, sorted(rows)
    assert rows['India']['total'][3] == 22.9
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    states = {}
    for k, r in sorted(rows.items()):
        if k == 'India':
            continue
        t = r['total']
        assert min(t[:3]) - 0.01 <= t[3] <= max(t[:3]) + 0.01, (k, t)
        if r['rural'][3] and r['urban'][3]:
            lo, hi = sorted((r['rural'][3], r['urban'][3]))
            assert lo - 0.05 <= t[3] <= hi + 0.05, (k, r)
        n = GEO.get(k, k.replace('&', 'and'))
        assert n in geo, n
        states[n] = r
    out = {'source': 'ORGI, SRS Statistical Report 2023, Statement 13', 'url': URL, 'sha256': SHA, 'retrieved': '2026-10-20',
           'unit': 'years; order within each group: below 18, 18-20, 21 and over, all ages', 'india': rows['India'], 'states': states}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(states), 'states')


main()
