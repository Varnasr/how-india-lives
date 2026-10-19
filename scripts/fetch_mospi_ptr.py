#!/usr/bin/env python3
"""Fetch the UDISE+ pupil-teacher ratio by level of education from MoSPI into data/mospi/udise-ptr.json.

    python3 scripts/fetch_mospi_ptr.py

Indicator 23 (Pupil Teacher Ratio by level of education), 2022-23 and 2024-25, all management types together
(the API offers no split by management for this indicator), levels Primary, Upper Primary, Secondary and Higher Secondary.
Values are whole numbers as MoSPI publishes them.
"""
import json
import os
import ssl
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'mospi', 'udise-ptr.json')
URL = 'https://api.mospi.gov.in/api/udise/getUdiseRecords'


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
        rows += call(dict(indicator_code=23, year=y))
    out = {'source': 'MoSPI open data API, dataset UDISE, indicator 23 (Pupil Teacher Ratio by level of education)',
           'retrieved': time.strftime('%Y-%m-%d'), 'rows': [{k: r[k] for k in ('year', 'state', 'level_of_education', 'value')} for r in rows]}
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT, len(rows), 'rows')


if __name__ == '__main__':
    main()
