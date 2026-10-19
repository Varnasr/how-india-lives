#!/usr/bin/env python3
"""Add the UDISE+ primary pupil-teacher ratio (2024-25, with 2022-23 beside it) to data/interactive-data.json. --check compares.

Source: data/mospi/udise-ptr.json (scripts/fetch_mospi_ptr.py). All management types together, whole numbers as published.
There is no all-India row in the API, so national is null."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import GEO, load, write_indicators  # noqa: E402


def build(raw):
    t = {}
    for r in raw['rows']:
        if r['level_of_education'] == 'Primary':
            t.setdefault(r['year'], {})[GEO.get(r['state'], r['state'])] = float(r['value'])
    assert len(t['2024-25']) == 36 and len(t['2022-23']) == 36
    return [{
        'id': 'udise_ptr_primary', 'theme': 'Education', 'name': 'Pupil-Teacher Ratio, Primary Schools',
        'unit': 'pupils per teacher (classes 1-5)', 'source': 'UDISE+ via MoSPI', 'year': '2024-25',
        'desc': 'Pupils per teacher in primary schools (classes 1 to 5), all management types together (government, aided and private), UDISE+ 2024-25, as MoSPI publishes it in whole numbers. The Right to Education Act sets 30 pupils per teacher as the norm at primary level. A state average hides small schools with one teacher and large ones with too few, so it says little about any one school.',
        'higherIsBetter': False, 'national': None,
        'values': dict(sorted(t['2024-25'].items())),
        'previous': dict(sorted(t['2022-23'].items())), 'previousYear': '2022-23', 'nationalPrevious': None,
        'sourceUrl': 'https://mospi.gov.in/', 'retrieved': raw['retrieved'],
        'name_hi': 'प्राथमिक विद्यालयों में छात्र-शिक्षक अनुपात', 'unit_hi': 'प्रति शिक्षक छात्र (कक्षा 1-5)',
        'desc_hi': 'प्राथमिक विद्यालयों (कक्षा 1 से 5) में प्रति शिक्षक छात्र, सभी प्रबंधन प्रकार मिलाकर, UDISE+ 2024-25, जैसा MoSPI पूर्ण संख्याओं में प्रकाशित करता है। शिक्षा का अधिकार अधिनियम प्राथमिक स्तर पर 30 छात्र प्रति शिक्षक का मानक तय करता है। राज्य औसत छोटे और एक शिक्षक वाले स्कूलों को छिपा देता है।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/mospi/udise-ptr.json')))
