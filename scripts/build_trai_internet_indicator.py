#!/usr/bin/env python3
"""Add internet subscriptions per 100 people (TRAI, March 2026) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    return [{
        'id': 'trai_internet_per100', 'theme': 'Economy', 'name': 'Internet subscriptions per 100 people',
        'unit': 'subscriptions per 100 population', 'source': 'TRAI, Yearly Performance Indicators 2025-26 (Table 1.43)', 'year': 'Mar 2026',
        'desc': 'Wired and wireless internet subscriptions per 100 people at the end of March 2026, from operators\' returns to TRAI divided by TRAI\'s population projection for 2026. A subscription is not a person: one person can hold several, so Goa, Delhi and Haryana exceed 100, and a low figure is not the same as a share of people online. The operators\' rural and urban split rests on different sources, so only the total is mapped.',
        'higherIsBetter': True, 'national': raw['india_total_per100'],
        'values': {s: d['total_per100'] for s, d in raw['states'].items()},
        'sourceUrl': raw['url'], 'retrieved': '2026-10-19',
        'name_hi': 'प्रति 100 लोगों पर इंटरनेट कनेक्शन', 'unit_hi': 'प्रति 100 जनसंख्या पर कनेक्शन',
        'desc_hi': 'मार्च 2026 के अंत में प्रति 100 लोगों पर वायर्ड और वायरलेस इंटरनेट कनेक्शन, TRAI को ऑपरेटरों के आँकड़ों और TRAI के जनसंख्या अनुमान से। एक कनेक्शन एक व्यक्ति नहीं है: एक व्यक्ति के कई कनेक्शन हो सकते हैं, इसलिए गोवा, दिल्ली और हरियाणा में आँकड़ा 100 से ऊपर है।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/trai/internet-2026-03.json')))
