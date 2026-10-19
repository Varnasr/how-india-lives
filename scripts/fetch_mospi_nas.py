#!/usr/bin/env python3
"""Fetch state GSDP per head and state value added by industry from MoSPI's National Accounts API.

    python3 scripts/fetch_mospi_nas.py        # writes data/mospi/nas-state.json

Base year 2011-12, current series, annual, 2022-23 and 2024-25, every state code 01 to 37.
The host negotiates TLS in a way OpenSSL 3 rejects, hence OP_LEGACY_SERVER_CONNECT. The raw rows are
committed so the indicators build without a network. Values are as MoSPI serves them on the retrieval
date; the latest year is an estimate that states revise.
"""
import json
import os
import ssl
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'mospi', 'nas-state.json')
BASE = 'https://api.mospi.gov.in/api/nas/getNasData'
YEARS = ['2022-23', '2024-25']
STATES = ','.join('%02d' % i for i in range(1, 38))


def call(params):
    ctx = ssl.create_default_context()
    ctx.options |= 0x4
    rows, page = [], 1
    while True:
        q = dict(params, page=page, limit=100, Format='JSON')
        u = BASE + '?' + urllib.parse.urlencode(q)
        for attempt in range(4):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), context=ctx, timeout=60))
                break
            except Exception:
                time.sleep(2 ** attempt)
        else:
            raise SystemExit('MoSPI NAS API did not answer for %s' % params)
        rows += d.get('data', [])
        if page >= d.get('meta_data', {}).get('totalPages', 1):
            return rows
        page += 1


def main():
    out = {'source': 'MoSPI, National Accounts Statistics, state series (api.mospi.gov.in), base year 2011-12, current series',
           'retrieved': time.strftime('%Y-%m-%d'), 'per_capita_gsdp': [], 'gsva': []}
    for y in YEARS:
        base = dict(base_year='2011-12', series='Current', frequency_code='Annually', state_code=STATES, year=y)
        out['per_capita_gsdp'] += call(dict(base, indicator_code=31))
        out['gsva'] += call(dict(base, indicator_code=29))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT, len(out['per_capita_gsdp']), 'per-capita rows,', len(out['gsva']), 'GSVA rows')


if __name__ == '__main__':
    main()
