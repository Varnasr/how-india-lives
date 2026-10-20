#!/usr/bin/env python3
"""Write data/mord/nrlm-shgs-2026.json from Annexure I of Lok Sabha Unstarred Question 3687 (11 August 2026).

    python3 scripts/extract_nrlm_shg.py AU3687.pdf [--check]

Source: Ministry of Rural Development, reply to Lok Sabha Unstarred Question 3687 of 11 August 2026 ("Rural schemes implemented
for SHGs"), Annexure I: women self-help groups set up under DAY-NRLM, by state and UT. The PDF is from sansad.in (SHA-256
pinned below). Check: the 34 rows add to the printed total, 92,30,743, the 92.30 lakh the answer quotes. Delhi and Chandigarh
are outside the Mission and have no row. The count is of groups, cumulative since the Mission began, and not of members.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import GEO, ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'mord', 'nrlm-shgs-2026.json')
SHA = '54f0f67d1c8ed9f7e897e59043b9582a58180b48cbd77aec937bb3885b62370d'
URL = 'https://sansad.in/getFile/lsapps/loksabhaquestions/annex/188/AU3687_XtpT52.pdf?source=lsapps'
TOTAL = 9230743


def main():
    pdf = sys.argv[1]
    assert sha256(pdf) == SHA, 'wrong file'
    text = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    seg = text[text.index('Detail of Women Self Help Groups'):].splitlines()
    rows, pend = {}, ''
    for line in seg:
        m = re.match(r'^\s*(\d{1,2})\s+([A-Za-z][A-Za-z &]*?)\s{2,}([\d,]+)\s*$', line)
        if m:
            nm = m.group(2).strip()
            rows[int(m.group(1))] = (nm, int(m.group(3).replace(',', '')))
            pend = ''
            continue
        m = re.match(r'^\s*(\d{1,2})\s+([A-Za-z][A-Za-z &]*?)\s*$', line)
        if m and 'S.No' not in line:
            rows[int(m.group(1))] = [m.group(2).strip(), None]
            pend = int(m.group(1))
            continue
        m = re.match(r'^\s*([A-Za-z][A-Za-z &]*?)\s{2,}([\d,]+)\s*$', line)
        if m and pend:
            rows[pend] = (rows[pend][0] + ' ' + m.group(1).strip(), int(m.group(2).replace(',', '')))
            pend = ''
    if rows.get(7) and rows[7][1] is None:
        rows[7] = (rows[7][0], 1823)  # printed on the line above the label: the wrapped row
    assert sorted(rows) == list(range(1, 35)), sorted(rows)
    names = {1: 'Andaman and Nicobar', 7: 'Dadra and Nagar Haveli and Daman and Diu'}
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    states = {}
    for k, (nm, v) in rows.items():
        nm = names.get(k, GEO.get(nm.title(), nm.title().replace(' And ', ' and ')))
        assert nm in geo and v, (k, nm, v)
        states[nm] = v
    assert sum(states.values()) == TOTAL, sum(states.values())
    out = {'source': 'Ministry of Rural Development, Lok Sabha Unstarred Question 3687 (11 August 2026), Annexure I', 'url': URL, 'sha256': SHA,
           'retrieved': '2026-10-20', 'as_on': 'August 2026', 'india_total': TOTAL, 'states': dict(sorted(states.items()))}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(states), 'states')


main()
