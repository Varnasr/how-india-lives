#!/usr/bin/env python3
"""Add mean age at effective marriage of females (SRS 2023, 22 states) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    return [{
        'id': 'srs_marriage_age', 'theme': 'Gender', 'name': 'Mean Age at Effective Marriage of Females', 'unit': 'years',
        'source': 'ORGI, SRS Statistical Report 2023 (Statement 13)', 'year': '2023',
        'desc': 'Mean age at which a marriage took effect for women whose marriage was recorded in the Sample Registration System in 2023. It is the average age at marriage in the sample, not the age at which women in the population first married, and it is not the share married below 18. Only India and the 22 larger states are published, and Jammu and Kashmir includes Ladakh.',
        'higherIsBetter': True, 'national': raw['india']['total'][3],
        'values': {s: d['total'][3] for s, d in raw['states'].items()},
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'महिलाओं की प्रभावी विवाह की औसत आयु', 'unit_hi': 'वर्ष',
        'desc_hi': 'नमूना पंजीकरण प्रणाली में 2023 में दर्ज विवाहों में महिलाओं की औसत आयु जब विवाह प्रभावी हुआ। यह नमूने में विवाह के समय की औसत आयु है, 18 से कम आयु में विवाहित का हिस्सा नहीं। केवल भारत और 22 बड़े राज्य प्रकाशित हैं।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/srs/marriage-age-2023.json')))
