#!/usr/bin/env python3
"""Add the private-school enrolment share (UDISE+) to data/interactive-data.json.

    python3 scripts/build_udise_enrolment_indicators.py          # rewrite it
    python3 scripts/build_udise_enrolment_indicators.py --check  # fail if out of date

Source: data/mospi/udise-enrolment.json (scripts/fetch_mospi_udise.py). Share = enrolment in private unaided
recognised schools / enrolment in all schools, classes 1-12, both sexes, times 100. Government aided schools
are private-managed but publicly funded and are not counted as private here. In every state and year the
management categories must add to the all-management total; a state with no private row whose government row
equals the total (Lakshadweep) has a private share of 0 by that identity. The national figure is the sum over
the 36 states and UTs.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = {'Andaman & Nicobar Islands': 'Andaman and Nicobar', 'Jammu & Kashmir': 'Jammu and Kashmir',
       'Dadra & Nagar Haveli and Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu'}


def tables(raw):
    t = {}
    for r in raw['rows']:
        t.setdefault(r['year'], {}).setdefault(GEO.get(r['state'], r['state']), {})[r['type_of_management']] = float(r['value'])
    for y, st in t.items():
        for s, d in st.items():
            parts = sum(v for k, v in d.items() if k != 'All Management')
            if abs(parts - d['All Management']) > 1e-4 * d['All Management']:
                raise SystemExit('%s %s: management categories sum to %s, all-management is %s' % (s, y, parts, d['All Management']))
    return t


def build(raw):
    t = tables(raw)

    def share(y):
        return {s: round(d.get('Private Unaided Recognized', 0) / d['All Management'] * 100, 1) for s, d in sorted(t[y].items())}

    def nat(y):
        return round(sum(d.get('Private Unaided Recognized', 0) for d in t[y].values()) / sum(d['All Management'] for d in t[y].values()) * 100, 1)
    return [{
        'id': 'udise_private_share', 'theme': 'Education', 'name': 'Private School Enrolment Share', 'unit': '% of enrolment, classes 1-12',
        'source': 'UDISE+ (MoSPI)', 'year': '2024-25',
        'desc': 'Share of students in classes 1-12 enrolled in private unaided recognised schools, 2024-25, with 2022-23 beside it. Government-aided schools are not counted as private here. The national figure is the sum over all states and union territories.',
        'higherIsBetter': None, 'national': nat('2024-25'), 'values': share('2024-25'), 'previous': share('2022-23'), 'previousYear': '2022-23',
        'nationalPrevious': nat('2022-23'), 'sourceUrl': 'https://udiseplus.gov.in/', 'retrieved': raw['retrieved'],
        'name_hi': 'निजी स्कूलों में नामांकन का हिस्सा', 'unit_hi': 'कक्षा 1-12 के नामांकन का %',
        'desc_hi': 'कक्षा 1-12 के उन विद्यार्थियों का हिस्सा जो निजी गैर-सहायता प्राप्त मान्यता प्राप्त स्कूलों में नामांकित हैं, 2024-25, 2022-23 के साथ। सरकारी सहायता प्राप्त स्कूल यहाँ निजी नहीं गिने गए। राष्ट्रीय आँकड़ा सभी राज्यों और केंद्र शासित प्रदेशों का योग है।',
    }]


def main():
    raw = json.load(open(os.path.join(ROOT, 'data', 'mospi', 'udise-enrolment.json')))
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
