#!/usr/bin/env python3
"""Add the UDISE+ 2024-25 secondary dropout indicator to data/interactive-data.json.

    python3 scripts/build_udise_indicators.py          # rewrite it
    python3 scripts/build_udise_indicators.py --check  # fail if out of date

Figures are in data/mospi/udise-2024-25.json as returned by MoSPI's open data API.
A state the API reports as exactly 0 where that cannot be a measurement (Bihar) is
listed under `unreported` in that file and is left off, never plotted as zero. The API
returns no All India row, so `national` is null rather than a figure of our own.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(raw):
    return [{
        'id': 'udise_dropout_sec', 'theme': 'Education', 'name': 'Secondary school dropout rate',
        'unit': '% of students in classes 9-10', 'source': 'UDISE+ (MoSPI)', 'year': '2024-25',
        'desc': 'Share of students in secondary school (classes 9-10) who dropped out, all school management types, boys and girls together.',
        'higherIsBetter': False, 'national': None, 'values': dict(sorted(raw['values'].items())),
        'sourceUrl': 'https://udiseplus.gov.in/', 'retrieved': raw['retrieved'],
        'name_hi': 'माध्यमिक स्तर पर स्कूल छोड़ने की दर', 'unit_hi': '% छात्र (कक्षा 9-10)',
        'desc_hi': 'माध्यमिक विद्यालय (कक्षा 9-10) के उन छात्रों का हिस्सा जिन्होंने पढ़ाई छोड़ दी, सभी प्रबंधन प्रकारों के लड़के और लड़कियाँ मिलाकर।',
    }]


def main():
    raw = json.load(open(os.path.join(ROOT, 'data', 'mospi', 'udise-2024-25.json')))
    path = os.path.join(ROOT, 'data', 'interactive-data.json')
    data = json.load(open(path))
    new = build(raw)
    ids = {i['id'] for i in new}
    if '--check' in sys.argv:
        ok = [i for i in data['indicators'] if i['id'] in ids] == new
        print('OK' if ok else 'STALE')
        sys.exit(0 if ok else 1)
    data['indicators'] = [i for i in data['indicators'] if i['id'] not in ids] + new
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    print('wrote', len(new), 'UDISE indicator;', len(data['indicators']), 'in file')


if __name__ == '__main__':
    main()
