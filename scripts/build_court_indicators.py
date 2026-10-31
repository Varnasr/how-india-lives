#!/usr/bin/env python3
"""Add the court indicators to data/interactive-data.json from data/courts/lok-sabha-3501.json.

    python3 scripts/build_court_indicators.py          # rewrite them
    python3 scripts/build_court_indicators.py --check  # fail if out of date

Source: Lok Sabha Unstarred Question 3501 (13 March 2026), Annexure II (cases pending in
district and subordinate courts, NJDG as on 9 March 2026) and Annexure IV (sanctioned and
working judicial officers, Nyaya Vikas 2.0 portal). The two tables come from different
sources and the second is undated, so cases per working judge is a rough guide.
Where the judges table merges states (West Bengal with Andaman and Nicobar; the two
Dadra and Nagar Haveli and Daman and Diu rows) the pendency is merged the same way, and the
merged ratio is shown for each. Meghalaya's pendency row is inconsistent in the source and is left out.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(raw):
    pend = raw['pending_cases_district_subordinate_courts']['by_state']
    jud = raw['judicial_officers_subordinate_judiciary']['by_state']
    WBAN = 'West Bengal and Andaman and Nicobar (combined)'
    # (state shown, pending cases, sanctioned, working)
    rows = {}
    for s, p in pend.items():
        if p.get('unreliable'):
            continue
        if s in ('West Bengal', 'Andaman and Nicobar'):
            continue
        j = jud.get(s)
        if s == 'Dadra and Nagar Haveli and Daman and Diu':
            a, b = jud['Dadra and Nagar Haveli (judges)'], jud['Daman and Diu (judges)']
            j = {'sanctioned': a['sanctioned'] + b['sanctioned'], 'working': a['working'] + b['working']}
        if j:
            rows[s] = (p['total'], j['sanctioned'], j['working'])
    merged = (pend['West Bengal']['total'] + pend['Andaman and Nicobar']['total'], jud[WBAN]['sanctioned'], jud[WBAN]['working'])
    rows['West Bengal'] = rows['Andaman and Nicobar'] = merged
    per = {s: round(p / w) for s, (p, a, w) in rows.items() if w}
    # vacancy needs no pendency row, so Meghalaya is included
    vac = {s: round((a - w) / a * 100, 1) for s, (p, a, w) in rows.items()}
    m = jud['Meghalaya']
    vac['Meghalaya'] = round((m['sanctioned'] - m['working']) / m['sanctioned'] * 100, 1)
    tp = sum(v['total'] for v in pend.values())
    tw = sum(v['working'] for v in jud.values())
    ts = sum(v['sanctioned'] for v in jud.values())
    url = raw['document_url']
    return [
        {'id': 'court_pending_per_judge', 'theme': 'Economy', 'name': 'Pending cases per working judge',
         'unit': 'cases per working judicial officer', 'source': 'NJDG and Nyaya Vikas (Lok Sabha, March 2026)', 'year': '2026',
         'desc': 'Cases pending in district and subordinate courts (NJDG, 9 March 2026) divided by working judicial officers in the subordinate judiciary. The two counts come from different sources, so it is a rough guide.',
         'higherIsBetter': False, 'national': round(tp / tw), 'values': dict(sorted(per.items())), 'sourceUrl': url, 'retrieved': '2026-10-19',
         'name_hi': 'प्रति कार्यरत न्यायाधीश लंबित मामले', 'unit_hi': 'मामले प्रति कार्यरत न्यायिक अधिकारी',
         'desc_hi': 'जिला और अधीनस्थ न्यायालयों में लंबित मामले (NJDG, 9 मार्च 2026) को अधीनस्थ न्यायपालिका के कार्यरत न्यायिक अधिकारियों से भाग देकर। दोनों संख्याएँ अलग स्रोतों से हैं, इसलिए यह मोटा अनुमान है।'},
        {'id': 'court_vacancy_pct', 'theme': 'Economy', 'name': 'Vacant judicial posts', 'unit': '% of sanctioned posts in the subordinate judiciary',
         'source': 'Nyaya Vikas (Lok Sabha, March 2026)', 'year': '2026',
         'desc': 'Share of sanctioned judicial posts in the district and subordinate courts that are vacant.',
         'higherIsBetter': False, 'national': round((ts - tw) / ts * 100, 1), 'values': dict(sorted(vac.items())), 'sourceUrl': url, 'retrieved': '2026-10-19',
         'name_hi': 'रिक्त न्यायिक पद', 'unit_hi': 'अधीनस्थ न्यायपालिका में स्वीकृत पदों का %',
         'desc_hi': 'जिला और अधीनस्थ न्यायालयों में स्वीकृत न्यायिक पदों का वह हिस्सा जो रिक्त है।'},
    ]


def main():
    raw = json.load(open(os.path.join(ROOT, 'data', 'courts', 'lok-sabha-3501.json')))
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
    if 'Nyaya Vikas' not in data['note']:
        data['note'] += (' The court indicators divide NJDG pendency in district and subordinate courts (9 March 2026) by working judicial officers '
                         'from the Nyaya Vikas portal, both as printed in Lok Sabha Question 3501. West Bengal and Andaman and Nicobar share one ratio because the judges '
                         'table merges them; Meghalaya\'s pendency row is inconsistent in the source and is left grey.')
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    print('wrote', len(new), 'court indicators;', len(data['indicators']), 'in file')


if __name__ == '__main__':
    main()
