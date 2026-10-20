#!/usr/bin/env python3
"""Add the sex ratio at birth (SRS 2021-23, 2020-22 beside it, 22 states) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    S = raw['states']
    return [{
        'id': 'srs_sex_ratio_birth', 'theme': 'Gender', 'name': 'Sex Ratio at Birth', 'unit': 'girls per 1,000 boys',
        'source': 'ORGI, SRS Statistical Report 2023 (Table 16)', 'year': '2021-23',
        'desc': 'Female births per 1,000 male births, a three-year average from the Sample Registration System for 2021-23, with 2020-22 beside it. A typical biological ratio is about 105 boys for 100 girls, roughly 952 girls per 1,000 boys, so a figure well below that points to sex-selective practices or to girls\' births going unreported, and the data cannot say which. Only India and the 22 larger states are published, and Jammu and Kashmir includes Ladakh. State samples are small, so single-period changes of a few points are within noise.',
        'higherIsBetter': True, 'national': raw['india']['total'][4],
        'values': {s: d['total'][4] for s, d in S.items()},
        'previous': {s: d['total'][3] for s, d in S.items()}, 'previousYear': '2020-22', 'nationalPrevious': raw['india']['total'][3],
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'जन्म के समय लिंगानुपात', 'unit_hi': 'प्रति 1,000 लड़कों पर लड़कियां',
        'desc_hi': 'नमूना पंजीकरण प्रणाली के 2021-23 के तीन वर्षीय औसत के अनुसार प्रति 1,000 पुरुष जन्म पर महिला जन्म, 2020-22 के साथ। जैविक रूप से सामान्य अनुपात लगभग 952 लड़कियां प्रति 1,000 लड़के है। केवल भारत और 22 बड़े राज्य प्रकाशित हैं।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/srs/sex-ratio-birth-2021-23.json')))
