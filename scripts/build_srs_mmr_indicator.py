#!/usr/bin/env python3
"""Add the SRS maternal mortality ratio 2022-24 (19 states shown separately) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    S = raw['states']
    return [{
        'id': 'srs_mmr', 'theme': 'Health', 'name': 'Maternal Mortality Ratio', 'unit': 'maternal deaths per 100,000 live births',
        'source': 'ORGI, SRS Special Bulletin on Maternal Mortality 2022-24', 'year': '2022-24',
        'desc': 'Maternal deaths per 100,000 live births, pooled over 2022 to 2024, from the Sample Registration System. Only 19 states are shown separately; the other states and UTs are pooled by SRS as "Other states" (84) and stay grey here. The estimates rest on few deaths, so the 95 per cent confidence intervals are wide (Kerala 0 to 50, Uttar Pradesh 115 to 192) and differences between neighbouring values are usually within the noise.',
        'higherIsBetter': False, 'national': raw['india']['mmr'],
        'values': {s: d['mmr'] for s, d in S.items()},
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'मातृ मृत्यु अनुपात', 'unit_hi': 'प्रति 1,00,000 जीवित जन्म पर मातृ मृत्यु',
        'desc_hi': '2022 से 2024 के पूल किए गए आँकड़ों से प्रति 1,00,000 जीवित जन्म पर मातृ मृत्यु, नमूना पंजीकरण प्रणाली से। केवल 19 राज्य अलग दिखाए गए हैं; बाकी "अन्य राज्य" (84) में समूहित हैं और यहाँ धूसर हैं। अनुमान कम मृत्यु पर आधारित हैं, इसलिए विश्वास अंतराल चौड़े हैं।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/srs/mmr-2022-24.json')))
