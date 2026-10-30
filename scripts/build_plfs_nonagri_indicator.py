#!/usr/bin/env python3
"""Add the share of women workers outside agriculture (PLFS 2025) to data/interactive-data.json.

    python3 scripts/build_plfs_nonagri_indicator.py          # rewrite it
    python3 scripts/build_plfs_nonagri_indicator.py --check  # fail if out of date

Source: data/mospi/plfs-female-agriculture-2025.json (scripts/fetch_mospi_plfs.py): the share of female workers,
usual status (principal plus subsidiary), rural and urban, calendar year 2025, whose industry is agriculture,
forestry and fishing. The mapped value is 100 minus that share, one decimal. The All India row is MoSPI's.
PLFS was redesigned for 2025, so these figures are not a like-for-like continuation of earlier annual rounds.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = {'Andaman & Nicobar Islands': 'Andaman and Nicobar', 'Jammu & Kashmir': 'Jammu and Kashmir',
       'Dadra & Nagar Haveli & Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu'}


def build(raw):
    a = {GEO.get(r['state'], r['state']): float(r['value']) for r in raw['rows']}
    nat = round(100 - a.pop('All India'), 1)
    return [{
        'id': 'plfs_women_nonagri', 'theme': 'Gender', 'name': 'Women workers outside agriculture', 'unit': '% of women workers',
        'source': 'PLFS 2025 (MoSPI)', 'year': '2025',
        'desc': 'Share of women workers (usual status, rural and urban) whose work is outside agriculture, forestry and fishing, calendar year 2025. It is 100 minus the agriculture share. PLFS was redesigned for 2025, so earlier rounds are not strictly comparable.',
        'higherIsBetter': None, 'national': nat, 'values': {s: round(100 - v, 1) for s, v in sorted(a.items())},
        'sourceUrl': 'https://mospi.gov.in/', 'retrieved': raw['retrieved'],
        'name_hi': 'कृषि के बाहर काम करने वाली महिला श्रमिक', 'unit_hi': 'महिला श्रमिकों का %',
        'desc_hi': 'उन महिला श्रमिकों का हिस्सा (सामान्य स्थिति, ग्रामीण और शहरी) जिनका काम कृषि, वानिकी और मत्स्य पालन से बाहर है, कैलेंडर वर्ष 2025। यह 100 में से कृषि का हिस्सा घटाने पर मिलता है। PLFS का 2025 के लिए नया ढाँचा है, इसलिए पिछले दौर से सीधी तुलना नहीं हो सकती।',
    }]


def main():
    raw = json.load(open(os.path.join(ROOT, 'data', 'mospi', 'plfs-female-agriculture-2025.json')))
    path = os.path.join(ROOT, 'data', 'interactive-data.json')
    data = json.load(open(path))
    new = build(raw)
    ids = {i['id'] for i in new}
    keep = {i['id']: i.get('mapId') for i in data['indicators'] if i['id'] in ids}
    for i in new:
        if keep.get(i['id']):
            i['mapId'] = keep[i['id']]
    if '--check' in sys.argv:
        ok = [i for i in data['indicators'] if i['id'] in ids] == new
        print('OK' if ok else 'STALE')
        sys.exit(0 if ok else 1)
    data['indicators'] = [i for i in data['indicators'] if i['id'] not in ids] + new
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    print('wrote', len(new), 'indicator;', len(data['indicators']), 'in file')


if __name__ == '__main__':
    main()
