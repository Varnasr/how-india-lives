#!/usr/bin/env python3
"""Add the NCRB crimes-against-women indicators to data/interactive-data.json.

    python3 scripts/build_ncrb_indicators.py          # rewrite the ncrb_* indicators
    python3 scripts/build_ncrb_indicators.py --check  # fail if out of date

Source: data/ncrb/crimes-against-women.json (see scripts/extract_ncrb_wor.py). These are
crimes REGISTERED with the police, not crimes committed. A higher rate can mean more
crime, easier reporting, or both, so no direction is claimed (`higherIsBetter` is null).
Rape and cruelty use NCRB's printed rate per lakh women. Dowry deaths and acid attacks
are counts too small for one decimal, so they are cases over the female population NCRB
prints, which agrees with NCRB's own rate to its printed precision in every state.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = {'A&N Islands': 'Andaman and Nicobar', 'D&N Haveli and Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu'}
SKIP = {'All India', 'Total states', 'Total UTs'}

# code, id, name, unit, desc, derived factor (None = printed rate), decimals, Hindi name, Hindi unit, Hindi desc
SPEC = [
    ('TOTAL', 'ncrb_total', 'Crimes against women recorded', 'cases per lakh women',
     'All crimes against women registered by the police under the IPC/BNS and special laws, per lakh women. It counts registrations, not incidence.',
     None, 1, 'दर्ज महिला-विरोधी अपराध', 'मामले प्रति लाख महिलाएँ',
     'IPC/BNS और विशेष कानूनों के तहत पुलिस में दर्ज महिलाओं के विरुद्ध सभी अपराध, प्रति लाख महिलाएँ। यह दर्ज मामलों की गिनती है, घटनाओं की नहीं।'),
    ('RAPE', 'ncrb_rape', 'Rape cases recorded', 'cases per lakh women',
     'Rape cases registered by the police under the IPC/BNS, per lakh women. It counts registrations, not incidence.',
     None, 1, 'दर्ज बलात्कार के मामले', 'मामले प्रति लाख महिलाएँ',
     'IPC/BNS के तहत पुलिस में दर्ज बलात्कार के मामले, प्रति लाख महिलाएँ। यह दर्ज मामलों की गिनती है, घटनाओं की नहीं।'),
    ('CRUELTY', 'ncrb_cruelty', 'Cruelty by husband or relatives recorded', 'cases per lakh women',
     'Cases of cruelty by a husband or his relatives registered by the police, per lakh women. It counts registrations, not incidence.',
     None, 1, 'पति या रिश्तेदारों द्वारा क्रूरता, दर्ज मामले', 'मामले प्रति लाख महिलाएँ',
     'पुलिस में दर्ज पति या उसके रिश्तेदारों द्वारा क्रूरता के मामले, प्रति लाख महिलाएँ। यह दर्ज मामलों की गिनती है, घटनाओं की नहीं।'),
    ('DOWRY_DEATH', 'ncrb_dowry_death', 'Dowry deaths recorded', 'cases per lakh women',
     'Dowry death cases registered by the police, per lakh women. It counts registrations, not incidence.',
     1, 2, 'दर्ज दहेज मृत्यु', 'मामले प्रति लाख महिलाएँ',
     'पुलिस में दर्ज दहेज मृत्यु के मामले, प्रति लाख महिलाएँ। यह दर्ज मामलों की गिनती है, घटनाओं की नहीं।'),
    ('ACID', 'ncrb_acid', 'Acid attack cases recorded', 'cases per crore women',
     'Acid attack cases registered by the police, per crore women. Counts are small, so a single case moves a small state a long way.',
     100, 2, 'दर्ज एसिड हमले के मामले', 'मामले प्रति करोड़ महिलाएँ',
     'पुलिस में दर्ज एसिड हमले के मामले, प्रति करोड़ महिलाएँ। संख्या छोटी है, इसलिए एक मामला छोटे राज्य का आँकड़ा काफ़ी बदल देता है।'),
]


def value(year, code, s, factor, dec):
    c = year['codes'][code].get(s)
    if not c:
        return None
    if factor is None:
        return c.get('rate')
    pop = year['population_lakh'].get(s)
    if c.get('cases') is None or not pop:
        return None
    return round(c['cases'] / pop * factor, dec)


def build(raw):
    y24, y23 = raw['years']['2024'], raw['years']['2023']
    out = []
    for code, iid, name, unit, desc, fac, dec, nhi, uhi, dhi in SPEC:
        vals, prev = {}, {}
        for s in y24['codes'][code]:
            if s in SKIP or s.endswith(')') or s == 'Delhi City':
                continue
            g = GEO.get(s, s.replace('&', 'and'))
            v, p = value(y24, code, s, fac, dec), value(y23, code, s, fac, dec)
            if v is not None:
                vals[g] = v
            if p is not None:
                prev[g] = p
        prov = y24['provenance'][code + (':rate' if fac is None else ':cases')]
        out.append({
            'id': iid, 'theme': 'Gender', 'name': name, 'unit': unit, 'source': 'NCRB (Crime in India 2024)', 'year': '2024',
            'desc': desc, 'higherIsBetter': None, 'national': value(y24, code, 'All India', fac, dec),
            'values': dict(sorted(vals.items())), 'previous': dict(sorted(prev.items())), 'previousYear': '2023',
            'nationalPrevious': value(y23, code, 'All India', fac, dec), 'sourceUrl': prov['url'], 'retrieved': '2026-10-19',
            'name_hi': nhi, 'desc_hi': dhi, 'unit_hi': uhi,
        })
    return out


def main():
    raw = json.load(open(os.path.join(ROOT, 'data', 'ncrb', 'crimes-against-women.json')))
    path = os.path.join(ROOT, 'data', 'interactive-data.json')
    data = json.load(open(path))
    new = build(raw)
    ids = {i['id'] for i in new}
    keepmap = {i['id']: i.get('mapId') for i in data['indicators'] if i['id'] in ids}
    for i in new:                      # a sheet that points back at an indicator survives a rebuild
        if keepmap.get(i['id']):
            i['mapId'] = keepmap[i['id']]
    if '--check' in sys.argv:
        have = [i for i in data['indicators'] if i['id'] in ids]
        ok = [{k: v for k, v in i.items()} for i in have] == new
        print('OK' if ok else 'STALE')
        sys.exit(0 if ok else 1)
    data['indicators'] = [i for i in data['indicators'] if i['id'] not in ids] + new
    if 'NCRB' not in data['note']:
        data['note'] += (' The NCRB indicators are crimes registered with the police in 2024 and 2023, per lakh women, read '
                         'from Crime in India Volume 1 by Women on Record. They count registrations, not incidence: a higher figure can mean '
                         'more crime, easier reporting, or both, so the maps claim no direction.')
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    print('wrote', len(new), 'NCRB indicators;', len(data['indicators']), 'in file')


if __name__ == '__main__':
    main()
