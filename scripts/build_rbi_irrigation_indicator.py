#!/usr/bin/env python3
"""Add net irrigated area as a share of net sown area (RBI Handbook, 2023-24 provisional, 2022-23 beside it) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def share(d, y):
    return {s: round(v['net_irrigated'][y] / v['net_sown'][y] * 100, 1) for s, v in sorted(d['states'].items())}


def build(raw):
    cur, prev = share(raw, '2023-24(p)'), share(raw, '2022-23')
    nat = round(raw['india']['net_irrigated']['2023-24(p)'] / raw['india']['net_sown']['2023-24(p)'] * 100, 1)
    nat0 = round(raw['india']['net_irrigated']['2022-23'] / raw['india']['net_sown']['2022-23'] * 100, 1)
    return [{
        'id': 'rbi_irrigated_share', 'theme': 'Environment', 'name': 'Net irrigated area as % of net sown area', 'unit': '% of net sown area',
        'source': 'RBI Handbook of Statistics on Indian States 2024-25 (Land Use Statistics)', 'year': '2023-24 (provisional)',
        'desc': 'Net irrigated area divided by net sown area, 2023-24 provisional, from the Ministry of Agriculture\'s land use statistics as the RBI Handbook prints them (Tables 54 and 56). The provisional year breaks the series in places: Maharashtra\'s net irrigated area doubles in one year (a rise of 20 points here), Andhra Pradesh\'s net sown area falls 13 per cent, and Manipur\'s and Jharkhand\'s fall sharply, so compare with 2022-23 before relying on a change. Delhi\'s tiny area makes its share unstable. Ladakh and the smaller territories are not in the tables.',
        'higherIsBetter': None, 'national': nat,
        'values': cur, 'previous': prev, 'previousYear': '2022-23', 'nationalPrevious': nat0,
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'शुद्ध बोए गए क्षेत्र का शुद्ध सिंचित क्षेत्र प्रतिशत', 'unit_hi': 'शुद्ध बोए गए क्षेत्र का %',
        'desc_hi': 'शुद्ध सिंचित क्षेत्र को शुद्ध बोए गए क्षेत्र से भाग देकर, 2023-24 (अनंतिम), कृषि मंत्रालय के भूमि उपयोग आँकड़ों से जैसा RBI हैंडबुक (तालिका 54 और 56) छापती है। अनंतिम वर्ष में कुछ राज्यों के आँकड़ों में अचानक बड़ा बदलाव है (महाराष्ट्र में 20 अंक की वृद्धि), इसलिए 2022-23 से तुलना करके ही बदलाव पर भरोसा करें।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/rbi/irrigation-2024.json')))
