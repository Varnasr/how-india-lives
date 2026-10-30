#!/usr/bin/env python3
"""Add installed renewable capacity per person to data/interactive-data.json.

    python3 scripts/build_mnre_indicator.py          # rewrite it
    python3 scripts/build_mnre_indicator.py --check  # fail if out of date

Capacity: MoSPI's MNRE series 'Total Power' (solar, wind, hydro including large hydro, bio), MW, July 2026,
data/mospi/mnre-total-2026-07.json. The state rows plus 'Others' must add to the All India row within 1 MW.
Population: the 2024 state populations (lakh) printed beside NCRB's murder table, which NCRB takes from the
National Commission on Population's July 2020 projections (data/ncrb/crime-in-india-2024-other.json). So the
capacity is July 2026 and the population is a projection for 2024; the two years differ.
watts per person = MW x 1,000,000 / (lakh x 100,000) = MW x 10 / lakh. The national figure is All India
capacity (which includes 'Others', capacity not assigned to a state) over the total population.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(cap, pop):
    mw = cap['capacity_mw']
    states = {k: v for k, v in mw.items() if k not in ('All India', 'Others')}
    if abs(sum(states.values()) + mw['Others'] - mw['All India']) > 1:
        raise SystemExit('state capacity plus Others does not add to All India')
    vals = {}
    for s, v in states.items():
        lakh = pop['states'][s]['population_lakh']
        vals[s] = round(v * 10 / lakh)
    nat = round(mw['All India'] * 10 / pop['india']['population_lakh'])
    return [{
        'id': 'mnre_per_person', 'theme': 'Environment', 'name': 'Installed renewable capacity per person', 'unit': 'watts per person',
        'source': 'MNRE (via MoSPI) and NCP population projection', 'year': '2026',
        'desc': 'Installed renewable power capacity (solar, wind, hydro including large hydro, bio) as of July 2026, in watts per person, using 2024 projected populations. It is capacity, not generation, and large hydro is included in the total.',
        'higherIsBetter': None, 'national': nat, 'values': dict(sorted(vals.items())),
        'sourceUrl': 'https://mnre.gov.in/', 'retrieved': cap['retrieved'],
        'name_hi': 'प्रति व्यक्ति स्थापित नवीकरणीय क्षमता', 'unit_hi': 'वाट प्रति व्यक्ति',
        'desc_hi': 'जुलाई 2026 तक स्थापित नवीकरणीय बिजली क्षमता (सौर, पवन, बड़ी पनबिजली सहित जल, जैव), वाट प्रति व्यक्ति, 2024 के अनुमानित जनसंख्या आँकड़ों के साथ। यह क्षमता है, उत्पादन नहीं, और बड़ी पनबिजली के कारण पहाड़ी राज्यों में आँकड़ा ऊँचा है।',
    }]


def main():
    cap = json.load(open(os.path.join(ROOT, 'data', 'mospi', 'mnre-total-2026-07.json')))
    pop = json.load(open(os.path.join(ROOT, 'data', 'ncrb', 'crime-in-india-2024-other.json')))
    path = os.path.join(ROOT, 'data', 'interactive-data.json')
    data = json.load(open(path))
    new = build(cap, pop)
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
