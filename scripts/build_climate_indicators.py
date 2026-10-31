#!/usr/bin/env python3
"""Add the climate indicators to data/interactive-data.json from data/climate/envstats.json.

    python3 scripts/build_climate_indicators.py          # rewrite them
    python3 scripts/build_climate_indicators.py --check  # fail if out of date

Forest cover is the Forest Survey of India's ISFR 2021 and 2023 as returned by MoSPI's
EnviStats API. The API labels the India total as "Puducherry" in both years (it is the
exact sum of the other rows), so that row is never used as a state. Heat-wave days are the
mean of 2022-2024 for states that report all three years; single years swing from 0 to 26.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(raw):
    f = raw['forest_cover_sq_km']
    skip = {'Puducherry (source row)', 'Dadra and Nagar Haveli (source row)', 'Daman and Diu and Dadra Nagar Haveli (source row)'}
    vals = {s: round(f['isfr_2023'][s] - f['isfr_2021'][s], 2) for s in f['isfr_2023'] if s not in skip and s in f['isfr_2021']}
    # the India total is every row except the one the source mislabels Puducherry (which IS that total)
    rows = [k for k in f['isfr_2023'] if k != 'Puducherry (source row)']
    total = round(sum(f['isfr_2023'][k] for k in rows) - sum(f['isfr_2021'][k] for k in rows), 2)
    assert abs(total - round(f['isfr_2023']['Puducherry (source row)'] - f['isfr_2021']['Puducherry (source row)'], 2)) < 0.05, 'rows do not add to the national row'
    h = raw['heat_wave_days']['values']
    hv = {s: round(sum(v) / 3, 1) for s, v in h.items() if all(x is not None for x in v)}
    return [
        {'id': 'forest_change', 'theme': 'Environment', 'name': 'Change in forest cover', 'unit': 'sq km, ISFR 2021 to 2023',
         'source': 'Forest Survey of India (ISFR 2023, via MoSPI)', 'year': '2021-23',
         'desc': 'Change in forest cover between the 2021 and 2023 Indian State of Forest Reports. Forest cover is satellite-measured tree canopy over one hectare, so plantations count and a gain is not necessarily natural forest.',
         'higherIsBetter': None, 'national': round(total, 2), 'values': dict(sorted(vals.items())),
         'sourceUrl': 'https://fsi.nic.in/forest-report-2023', 'retrieved': '2026-10-19',
         'name_hi': 'वन आच्छादन में बदलाव', 'unit_hi': 'वर्ग किमी, ISFR 2021 से 2023',
         'desc_hi': 'भारत वन स्थिति रिपोर्ट 2021 और 2023 के बीच वन आच्छादन में बदलाव। वन आच्छादन उपग्रह से मापा गया एक हेक्टेयर से बड़ा वृक्ष-आच्छादन है, इसलिए वृक्षारोपण भी गिने जाते हैं और बढ़त का मतलब हमेशा प्राकृतिक वन नहीं।'},
        {'id': 'heat_wave_days', 'theme': 'Environment', 'name': 'Heat-wave days, 2022-24 average', 'unit': 'days a summer',
         'source': 'IMD (via MoSPI EnviStats)', 'year': '2022-24',
         'desc': 'Average number of heat-wave days reported in the summer season, averaged over 2022, 2023 and 2024. Single years swing widely, so only states reporting all three years are shown.',
         'higherIsBetter': False, 'national': None, 'values': dict(sorted(hv.items())),
         'sourceUrl': 'https://mospi.gov.in/', 'retrieved': '2026-10-19',
         'name_hi': 'लू वाले दिन, 2022-24 औसत', 'unit_hi': 'दिन प्रति गर्मी',
         'desc_hi': 'गर्मी के मौसम में दर्ज लू वाले दिनों की औसत संख्या, 2022, 2023 और 2024 का औसत। अलग-अलग वर्षों में भारी उतार-चढ़ाव होता है, इसलिए केवल वे राज्य दिखाए गए हैं जिनके तीनों वर्षों के आँकड़े हैं।'},
    ]


def main():
    raw = json.load(open(os.path.join(ROOT, 'data', 'climate', 'envstats.json')))
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
    if 'EnviStats' not in data['note']:
        data['note'] += (' The forest-cover change and heat-wave indicators come from MoSPI\'s EnviStats API. In that source the row labelled '
                         'Puducherry holds the India total, so Puducherry and the merged Dadra and Nagar Haveli and Daman and Diu are left grey for forest cover. '
                         'Heat-wave days are reported for 24 states and shown for 19 with all three years.')
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    print('wrote', len(new), 'climate indicators;', len(data['indicators']), 'in file')


if __name__ == '__main__':
    main()
