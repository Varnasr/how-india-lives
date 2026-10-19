#!/usr/bin/env python3
"""Pull NCRB crimes-against-women figures for 2023 and 2024 out of Women on Record.

    python3 scripts/extract_ncrb_wor.py path/to/WomenOnRecord/data/womenonrecord.csv

Writes data/ncrb/crimes-against-women.json. Women on Record reads NCRB's Crime in
India, Volume 1 (table 3A.2 for state and UT counts and rates, table 3A.1 for the
female population) and checks every row against NCRB's own totals; the source file,
its address and its SHA-256 travel with each figure. Only the five headings the atlas
maps are kept: all crimes, rape, cruelty by husband or relatives, dowry deaths and
acid attacks.
"""
import csv
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'ncrb', 'crimes-against-women.json')
CODES = ('TOTAL', 'RAPE', 'CRUELTY', 'DOWRY_DEATH', 'ACID')
YEARS = ('2023', '2024')


def main():
    src = sys.argv[1]
    rows = list(csv.DictReader(open(src, encoding='utf-8')))
    commit = subprocess.run(['git', '-C', os.path.dirname(src), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    out = {'source': 'NCRB, Crime in India 2023 and 2024, Volume 1, as read and checked by Women on Record (womenonrecord.net)',
           'women_on_record_commit': commit, 'years': {}}
    for y in YEARS:
        d = out['years'][y] = {'population_lakh': {}, 'codes': {c: {} for c in CODES}, 'provenance': {}}
        for r in rows:
            if r['year'] != y or r['kind'] not in ('state', 'ut', 'total') or r['state'] in ('Total states', 'Total UTs'):
                continue
            s = r['state']
            if r['crime_code'] == 'FEMALE_POP' and r['measure'] == 'population_lakh':
                d['population_lakh'][s] = float(r['value'])
            elif r['crime_code'] in CODES and r['measure'] in ('cases', 'rate') and r['value'] not in ('', 'NA'):
                d['codes'][r['crime_code']].setdefault(s, {})[r['measure']] = float(r['value'])
                d['provenance'][r['crime_code'] + ':' + r['measure']] = {
                    'table': r['table_no'], 'edition': r['source_edition'], 'url': r['source_url'], 'sha256': r['source_sha256']}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT, {y: {c: len(v) for c, v in d['codes'].items()} for y, d in out['years'].items()})


if __name__ == '__main__':
    main()
