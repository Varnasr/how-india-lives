#!/usr/bin/env python3
"""Fetch PLFS annual employment-condition shares for regular wage and salaried employees from MoSPI.

    python3 scripts/fetch_mospi_plfs.py        # writes data/mospi/plfs-contract.json

Annual series (frequency_code 1), indicator 5, employee_contract 1 'with no written job contract', all
states, persons, rural and urban combined, 2022-23 and 2023-24. Raw rows are committed.
"""
import json
import os
import ssl
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'mospi', 'plfs-contract.json')
OUT_AGRI = os.path.join(ROOT, 'data', 'mospi', 'plfs-female-agriculture-2025.json')
URL = 'https://api.mospi.gov.in/api/plfs/getData'


def call(params):
    ctx = ssl.create_default_context()
    ctx.options |= 0x4
    rows, page = [], 1
    while True:
        u = URL + '?' + urllib.parse.urlencode(dict(params, page=page, limit=100, Format='JSON'))
        for attempt in range(4):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), context=ctx, timeout=90))
                break
            except Exception:
                time.sleep(2 ** attempt)
        else:
            raise SystemExit('MoSPI PLFS API did not answer for %s' % params)
        rows += d.get('data', [])
        if page >= d.get('meta_data', {}).get('totalPages', 1):
            return rows
        page += 1


def main():
    rows = []
    for y in ('2022-23', '2023-24'):
        rows += call(dict(indicator_code=5, frequency_code=1, year=y, gender_code=3, sector_code=3, employee_contract_code=1))
    out = {'source': 'MoSPI open data API, dataset PLFS (annual), indicator 5, employee_contract 1 (with no written job contract), persons, rural + urban',
           'retrieved': time.strftime('%Y-%m-%d'),
           'rows': [{k: r[k] for k in ('year', 'state', 'value', 'employee_contract', 'gender', 'sector')} for r in rows]}
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT, len(rows), 'rows')
    # indicator 4, calendar year 2025: percentage distribution of female workers by industry section A (agriculture, forestry and fishing)
    ag = call(dict(indicator_code=4, frequency_code=1, year='2025', year_type_code=2, gender_code=2, sector_code=3, weekly_status_code=1, industry_section_code=2))
    ag = [r for r in ag if r['industry_section'].startswith('A_')]
    out2 = {'source': 'MoSPI open data API, dataset PLFS (annual, calendar year 2025), indicator 4, female workers, rural + urban, usual status (PS+SS), industry section A (agriculture, forestry and fishing)',
            'retrieved': time.strftime('%Y-%m-%d'), 'rows': [{k: r[k] for k in ('year', 'state', 'value', 'industry_section', 'gender', 'sector', 'weekly_status')} for r in ag]}
    json.dump(out2, open(OUT_AGRI, 'w'), indent=1, ensure_ascii=False)
    open(OUT_AGRI, 'a').write('\n')
    print('wrote', OUT_AGRI, len(ag), 'rows')


if __name__ == '__main__':
    main()
