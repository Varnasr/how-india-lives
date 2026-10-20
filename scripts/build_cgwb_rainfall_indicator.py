#!/usr/bin/env python3
"""Add state rainfall in calendar year 2024 (via the CGWB 2025 compilation, IMD data) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    S = raw['states']
    return [{
        'id': 'rain_2024', 'theme': 'Environment', 'name': 'Annual Rainfall, 2024', 'unit': 'mm in calendar year 2024',
        'source': 'IMD rainfall as tabulated in the CGWB National Compilation on Dynamic Ground Water Resources of India, 2025', 'year': '2024',
        'desc': 'Rainfall in calendar year 2024 for each state and territory, in millimetres, as the Central Ground Water Board tabulates it from India Meteorological Department data. The state figure is an average over the state, so it hides the difference between wet and dry districts, and one year is weather, not climate: 18 states and territories were below their normal in 2024 and 18 above. Normal rainfall is in the calculation file.',
        'higherIsBetter': None, 'national': None, 'values': {s: d['rain_2024'] for s, d in S.items()},
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'वार्षिक वर्षा, 2024', 'unit_hi': 'कैलेंडर वर्ष 2024 में मिमी',
        'desc_hi': 'भारत मौसम विज्ञान विभाग के आंकड़ों से केंद्रीय भूजल बोर्ड द्वारा संकलित, कैलेंडर वर्ष 2024 में प्रत्येक राज्य और केंद्रशासित प्रदेश की वर्षा, मिलीमीटर में। राज्य का आंकड़ा औसत है और एक वर्ष मौसम है, जलवायु नहीं। सामान्य वर्षा गणना फ़ाइल में है।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/cgwb/rainfall-2024.json')))
