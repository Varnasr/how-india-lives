#!/usr/bin/env python3
"""Add the PLFS 'no written job contract' share to data/interactive-data.json.

    python3 scripts/build_plfs_contract_indicator.py          # rewrite it
    python3 scripts/build_plfs_contract_indicator.py --check  # fail if out of date

Source: data/mospi/plfs-contract.json (scripts/fetch_mospi_plfs.py). The figure is MoSPI's published share of
regular wage and salaried employees with no written job contract, persons, rural and urban, 2023-24 with
2022-23 beside it. The All India row is the published national figure. It covers regular wage and salaried
employees only, not every informal worker.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = {'Andaman & Nicobar Islands': 'Andaman and Nicobar', 'Jammu & Kashmir': 'Jammu and Kashmir',
       'Dadra & Nagar Haveli & Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu'}


def build(raw):
    def tab(y):
        return {GEO.get(r['state'], r['state']): float(r['value']) for r in raw['rows'] if r['year'] == y}
    a, b = tab('2023-24'), tab('2022-23')
    nat, natp = a.pop('All India'), b.pop('All India')
    return [{
        'id': 'plfs_no_contract', 'theme': 'Economy', 'name': 'Regular Employees with No Written Contract', 'unit': '% of regular wage and salaried employees',
        'source': 'PLFS annual (MoSPI)', 'year': '2023-24',
        'desc': 'Share of regular wage and salaried employees who have no written job contract, persons, rural and urban, 2023-24, with 2022-23 beside it. It covers regular employees only, not casual workers or the self-employed.',
        'higherIsBetter': False, 'national': nat, 'values': dict(sorted(a.items())), 'previous': dict(sorted(b.items())), 'previousYear': '2022-23',
        'nationalPrevious': natp, 'sourceUrl': 'https://mospi.gov.in/', 'retrieved': raw['retrieved'],
        'name_hi': 'बिना लिखित अनुबंध वाले नियमित कर्मचारी', 'unit_hi': 'नियमित वेतनभोगी कर्मचारियों का %',
        'desc_hi': 'नियमित वेतनभोगी कर्मचारियों का वह हिस्सा जिनके पास कोई लिखित नौकरी अनुबंध नहीं है, व्यक्ति, ग्रामीण और शहरी, 2023-24, 2022-23 के साथ। इसमें केवल नियमित कर्मचारी हैं, अस्थायी मज़दूर या स्वरोज़गार वाले नहीं।',
    }]


def main():
    raw = json.load(open(os.path.join(ROOT, 'data', 'mospi', 'plfs-contract.json')))
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
