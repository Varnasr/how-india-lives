#!/usr/bin/env python3
"""Add life expectancy at birth (SRS abridged life tables 2019-23, 22 states) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    S = raw['states']
    return [{
        'id': 'srs_life_exp', 'theme': 'Health', 'name': 'Life expectancy at birth', 'unit': 'years',
        'source': 'ORGI, SRS Abridged Life Tables 2019-23', 'year': '2019-23',
        'desc': 'Expected years of life at birth for both sexes, from the Sample Registration System abridged life tables for 2019-23, a five-year moving average. Only India and the 22 larger states and UTs are published (those with a population of 10 million or more, plus Himachal Pradesh); the rest stay grey. Jammu and Kashmir includes Ladakh. Female life expectancy is higher than male in every state shown.',
        'higherIsBetter': True, 'national': raw['india']['total'],
        'values': {s: d['total'] for s, d in S.items()},
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'जन्म पर जीवन प्रत्याशा', 'unit_hi': 'वर्ष',
        'desc_hi': 'नमूना पंजीकरण प्रणाली की 2019-23 की संक्षिप्त जीवन तालिकाओं से दोनों लिंगों के लिए जन्म पर जीवन प्रत्याशा, पाँच वर्ष का चलता औसत। केवल भारत और 22 बड़े राज्य और केंद्र शासित प्रदेश प्रकाशित हैं; शेष धूसर हैं। जम्मू-कश्मीर में लद्दाख शामिल है।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/srs/life-expectancy-2019-23.json')))
