#!/usr/bin/env python3
"""Add adult HIV prevalence (NACO 2024) to data/interactive-data.json. --check compares instead of writing."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    return [{
        'id': 'naco_hiv', 'theme': 'Health', 'name': 'Adult HIV Prevalence', 'unit': '% of adults aged 15-49', 'source': 'NACO Sankalak 2025 (estimates for 2024)',
        'year': '2024', 'desc': 'Estimated HIV prevalence among adults, 2024, from the National AIDS Control Organisation. These are modelled estimates, not a count, and Ladakh and Lakshadweep are not reported.',
        'higherIsBetter': False, 'national': raw['national'], 'values': raw['values'], 'sourceUrl': raw['url'], 'retrieved': '2026-10-19',
        'name_hi': 'वयस्कों में एचआईवी का प्रसार', 'unit_hi': '15-49 वर्ष के वयस्कों का %',
        'desc_hi': 'राष्ट्रीय एड्स नियंत्रण संगठन (NACO) के अनुसार वयस्कों में एचआईवी का अनुमानित प्रसार, 2024। ये मॉडल पर आधारित अनुमान हैं, गिनती नहीं, और लद्दाख तथा लक्षद्वीप के आँकड़े नहीं दिए गए।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/naco/hiv-2024.json')))
