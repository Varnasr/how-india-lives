#!/usr/bin/env python3
"""Fetch HCES per-capita monthly cereal quantities (rice, wheat, coarse grains, other cereals, total) from MoSPI.

    python3 scripts/fetch_mospi_hces_cereals.py     # writes data/mospi/hces-cereals.json

Dataset HCES, indicator 5 (Average Per Capita Monthly Quantity Consumption, kg), rural (sector 1) and urban (sector 2),
2022-23 and 2023-24, without imputation. Raw rows are committed.
"""
import json
import os
import ssl
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'mospi', 'hces-cereals.json')
URL = 'https://api.mospi.gov.in/api/hces/getHcesRecords'


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
            raise SystemExit('MoSPI HCES API did not answer for %s' % params)
        rows += d.get('data', [])
        if page >= d.get('meta_data', {}).get('totalPages', 1):
            return rows
        page += 1


def main():
    rows = []
    for y in ('2022-23', '2023-24'):
        for sec in (1, 2):
            rows += call(dict(indicator_code=5, year=y, sector_code=sec, imputation_type_code=1))
    out = {'source': 'MoSPI open data API, dataset HCES, indicator 5 (Average Per Capita Monthly Quantity Consumption), without imputation',
           'retrieved': time.strftime('%Y-%m-%d'),
           'rows': [{k: r[k] for k in ('year', 'state', 'sector', 'cereal', 'value')} for r in rows]}
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT, len(rows), 'rows')


if __name__ == '__main__':
    main()
