#!/usr/bin/env python3
"""Add the PLFS 2025 unemployment indicators to data/interactive-data.json.

    python3 scripts/build_plfs_indicators.py          # rewrite them
    python3 scripts/build_plfs_indicators.py --check  # fail if out of date

The figures are in data/mospi/plfs-2025.json, as returned by MoSPI's open data API
(see the file for the exact filters). The unemployment rate here is on usual status
(principal plus subsidiary), the same basis as the female participation indicator.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://www.mospi.gov.in/periodic-labour-force-survey-plfs'


def build(raw):
    spec = [
        ('plfs_ur', 'Unemployment Rate', 'of the labour force aged 15 and above',
         'Share of the labour force aged 15 and above who are without work and looking for it, on usual status (principal plus subsidiary).',
         'बेरोज़गारी दर', '% श्रम बल (15 वर्ष और अधिक)',
         '15 वर्ष और अधिक के श्रम बल का वह हिस्सा जो काम से बाहर है और काम खोज रहा है (सामान्य स्थिति: मुख्य और सहायक)।'),
        ('plfs_yur', 'Youth Unemployment Rate', 'of the labour force aged 15-29',
         'Share of the labour force aged 15-29 who are without work and looking for it, on usual status (principal plus subsidiary).',
         'युवा बेरोज़गारी दर', '% श्रम बल (15-29 वर्ष)',
         '15-29 वर्ष के श्रम बल का वह हिस्सा जो काम से बाहर है और काम खोज रहा है (सामान्य स्थिति: मुख्य और सहायक)।'),
    ]
    out = []
    for iid, name, unit, desc, nhi, uhi, dhi in spec:
        s = raw['series'][iid]
        out.append({'id': iid, 'theme': 'Economy', 'name': name, 'unit': '% ' + unit, 'source': 'PLFS (MoSPI)',
                    'year': '2025', 'desc': desc, 'higherIsBetter': False, 'national': s['national'],
                    'values': dict(sorted(s['values'].items())), 'sourceUrl': URL, 'retrieved': raw['retrieved'],
                    'name_hi': nhi, 'desc_hi': dhi, 'unit_hi': uhi})
    return out


def main():
    raw = json.load(open(os.path.join(ROOT, 'data', 'mospi', 'plfs-2025.json')))
    path = os.path.join(ROOT, 'data', 'interactive-data.json')
    data = json.load(open(path))
    new = build(raw)
    ids = {i['id'] for i in new}
    if '--check' in sys.argv:
        have = [i for i in data['indicators'] if i['id'] in ids]
        print('OK' if have == new else 'STALE')
        sys.exit(0 if have == new else 1)
    data['indicators'] = [i for i in data['indicators'] if i['id'] not in ids] + new
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    print('wrote', len(new), 'PLFS indicators;', len(data['indicators']), 'in file')


if __name__ == '__main__':
    main()
