#!/usr/bin/env python3
"""Fetch UDISE+ enrolment by school management for classes 1-12 from MoSPI.

    python3 scripts/fetch_mospi_udise.py        # writes data/mospi/udise-enrolment.json

Indicator 28 (Enrolment of Students), gender Total, level 'Primary to Higher Secondary (1-12)', for
All Management and for each management type, 2022-23 and 2024-25. Raw rows are committed.
"""
import json
import os
import ssl
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'mospi', 'udise-enrolment.json')
URL = 'https://api.mospi.gov.in/api/udise/getUdiseRecords'
LEVEL = 'Primary to Higher Secondary (1-12)'


def call(params):
    ctx = ssl.create_default_context()
    ctx.options |= 0x4
    rows, page = [], 1
    while True:
        u = URL + '?' + urllib.parse.urlencode(dict(params, page=page, limit=100))
        for attempt in range(4):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), context=ctx, timeout=60))
                break
            except Exception:
                time.sleep(2 ** attempt)
        else:
            raise SystemExit('MoSPI UDISE API did not answer for %s' % params)
        rows += d.get('data', [])
        if page >= d.get('meta_data', {}).get('totalPages', 1):
            return rows
        page += 1


def main():
    rows = []
    for y in ('2022-23', '2024-25'):
        for m in (1, 2, 3, 4, 5):
            rows += [r for r in call(dict(indicator_code=28, year=y, gender_code=3, type_of_management_code=m)) if r['level_of_education'] == LEVEL]
    out = {'source': 'MoSPI open data API, dataset UDISE, indicator 28 (Enrolment of Students), gender Total, level ' + LEVEL,
           'retrieved': time.strftime('%Y-%m-%d'), 'rows': [{k: r[k] for k in ('year', 'state', 'type_of_management', 'value')} for r in rows]}
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT, len(rows), 'rows')


if __name__ == '__main__':
    main()
