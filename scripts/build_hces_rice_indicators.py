#!/usr/bin/env python3
"""Add the rice share of cereal consumption (HCES 2023-24, rural and urban) to data/interactive-data.json. --check compares.

Source: data/mospi/hces-cereals.json (scripts/fetch_mospi_hces_cereals.py). Share = per-capita monthly rice (kg) / total
cereals (kg) x 100, in quantity, not calories or money. A '-' in the API for wheat, coarse grains or other cereals means a
negligible or unreported component; in every row rice + wheat + coarse + other (with '-' as 0) equals the total cereals
within 1 per cent, which is checked. There is no combined rural-urban series, so there are two indicators."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import GEO, load, write_indicators  # noqa: E402


def tables(raw):
    t = {}
    for r in raw['rows']:
        v = 0.0 if r['value'].strip() == '-' else float(r['value'])
        t.setdefault((r['year'], r['sector']), {}).setdefault(GEO.get(r['state'], r['state']), {})[r['cereal']] = v
    for k, st in t.items():
        for s, d in st.items():
            parts = d['Rice'] + d['Wheat'] + d['Coarse Grains'] + d['Other Cereals']
            assert abs(parts - d['Total Cereals']) <= 0.01 * d['Total Cereals'] + 0.005, (k, s, parts, d['Total Cereals'])
            assert d['Rice'] > 0 and d['Total Cereals'] > 0
    return t


def share(t, key):
    return {s: round(d['Rice'] / d['Total Cereals'] * 100, 1) for s, d in sorted(t[key].items())}


def build(raw):
    t = tables(raw)
    out = []
    for sec, i, hi in (('Rural', 'hces_rice_r', 'ग्रामीण'), ('Urban', 'hces_rice_u', 'शहरी')):
        cur, prev = share(t, ('2023-24', sec)), share(t, ('2022-23', sec))
        nat, nat0 = cur.pop('All India'), prev.pop('All India')
        out.append({
            'id': i, 'theme': 'Economy', 'name': 'Rice share of cereal consumption (%s)' % sec.lower(), 'unit': '% of per-capita cereal quantity',
            'source': 'MoSPI HCES 2023-24', 'year': '2023-24',
            'desc': 'Rice as a share of all cereals eaten per person per month, in kilograms, %s households, HCES 2023-24 (without imputation). A quantity share, not calories or rupees. The rest is wheat, coarse grains (millets and maize) and other cereals. Rural and urban are separate series because HCES publishes no combined one.' % sec.lower(),
            'higherIsBetter': None, 'national': nat, 'values': cur, 'previous': prev, 'previousYear': '2022-23', 'nationalPrevious': nat0,
            'sourceUrl': 'https://mospi.gov.in/', 'retrieved': raw['retrieved'],
            'name_hi': 'अनाज उपभोग में चावल का हिस्सा (%s)' % hi, 'unit_hi': 'प्रति व्यक्ति अनाज मात्रा का %',
            'desc_hi': 'प्रति व्यक्ति प्रति माह खाए गए सभी अनाजों में चावल का हिस्सा, किलोग्राम में, %s परिवार, HCES 2023-24 (बिना आरोपण)। यह मात्रा का हिस्सा है, कैलोरी या रुपये का नहीं।' % hi,
        })
    return out


if __name__ == '__main__':
    write_indicators(build(load('data/mospi/hces-cereals.json')))
