#!/usr/bin/env python3
"""Add ASER 2024 children aged 6-14 not in school to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    return [{
        'id': 'aser_oos_6_14', 'theme': 'Education', 'name': 'Children aged 6-14 not in school (rural)',
        'unit': '% of rural children aged 6-14', 'source': 'ASER Centre, ASER (Rural) 2024', 'year': '2024',
        'desc': 'Share of rural children aged 6 to 14 who are not enrolled in any school, from the ASER 2024 household survey (provisional report, 28 January 2025). Rural districts only; 27 states have a published figure, and Delhi, Goa, Manipur and the smaller territories do not. Single-state figures rest on modest samples, so differences of a few tenths of a point are within survey noise.',
        'higherIsBetter': False, 'national': raw['india']['6-14']['not_in_school'],
        'values': {s: x['6-14']['not_in_school'] for s, x in raw['states'].items()},
        'sourceUrl': raw['url'], 'retrieved': '2026-10-19',
        'name_hi': 'स्कूल से बाहर बच्चे, 6-14 वर्ष (ग्रामीण)', 'unit_hi': 'ग्रामीण 6-14 वर्ष के बच्चों का %',
        'desc_hi': 'ग्रामीण क्षेत्रों में 6 से 14 वर्ष के उन बच्चों का हिस्सा जो किसी स्कूल में नामांकित नहीं हैं, ASER 2024 घरेलू सर्वेक्षण से (अनंतिम रिपोर्ट, 28 जनवरी 2025)। केवल ग्रामीण जिले; 27 राज्यों के आँकड़े प्रकाशित हैं।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/aser/not-enrolled-2024.json')))
