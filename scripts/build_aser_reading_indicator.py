#!/usr/bin/env python3
"""Add ASER 2024 Std V reading (government schools, rural) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    d = raw['std5']
    return [{
        'id': 'aser_std5_read', 'theme': 'Education', 'name': 'Std V children who can read a Std II text (government schools)',
        'unit': '% of government-school Std V children (rural)', 'source': 'ASER Centre, ASER (Rural) 2024', 'year': '2024',
        'desc': 'Share of Std V children in rural government schools who can read a Std II level text, from the ASER 2024 household survey (provisional report, 28 January 2025). ASER tests children at home in rural districts only, and its state tables cover government schools only. 27 states are published; Delhi, Goa and the smaller territories have no figure. Subtract from 100 for the share who cannot. State samples are small, so single-state swings of a few points are within survey noise.',
        'higherIsBetter': True, 'national': raw['national_govt']['std5']['2024'],
        'values': {s: x['2024'] for s, x in d.items()},
        'previous': {s: x['2022'] for s, x in d.items()}, 'previousYear': '2022', 'nationalPrevious': raw['national_govt']['std5']['2022'],
        'sourceUrl': raw['url'], 'retrieved': '2026-10-19',
        'name_hi': 'कक्षा 5 के बच्चे जो कक्षा 2 का पाठ पढ़ सकते हैं (सरकारी स्कूल)',
        'unit_hi': 'ग्रामीण सरकारी स्कूल की कक्षा 5 के बच्चों का %',
        'desc_hi': 'ग्रामीण सरकारी स्कूलों में कक्षा 5 के उन बच्चों का हिस्सा जो कक्षा 2 स्तर का पाठ पढ़ सकते हैं, ASER 2024 घरेलू सर्वेक्षण से (अनंतिम रिपोर्ट, 28 जनवरी 2025)। ASER केवल ग्रामीण जिलों में बच्चों को घर पर परखता है और राज्य तालिकाएँ केवल सरकारी स्कूलों की हैं। 27 राज्यों के आँकड़े प्रकाशित हैं।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/aser/reading-2024.json')))
