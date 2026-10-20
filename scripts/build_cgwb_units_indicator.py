#!/usr/bin/env python3
"""Add the share of over-exploited groundwater assessment units (CGWB 2025) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def share(raw):
    return {s: round(d['over_exploited'] / d['assessed'] * 100, 1) for s, d in raw['states'].items()}


def build(raw):
    return [{
        'id': 'cgwb_oe_share', 'theme': 'Environment', 'name': 'Over-Exploited Groundwater Units', 'unit': '% of assessed blocks, taluks or mandals',
        'source': 'CGWB, National Compilation on Dynamic Ground Water Resources of India, 2025', 'year': '2025',
        'desc': 'Share of assessment units (blocks, taluks or mandals) categorised over-exploited in the 2025 groundwater assessment, meaning yearly extraction exceeds the yearly replenishable recharge. The unit differs by state, so a state with few large units (Uttarakhand has 20, Delhi 34) can swing sharply on one unit, and a state average hides which parts of it are depleted. India: 730 of 6,762 units, against 751 of 6,746 in 2024. Saline units are counted in the total and are not over-exploited.',
        'higherIsBetter': False, 'national': round(raw['india']['over_exploited'] / raw['india']['assessed'] * 100, 1),
        'values': share(raw), 'nationalPrevious': 11.1, 'previousYear': '2024',
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'अति-दोहित भूजल इकाइयां', 'unit_hi': 'आकलित ब्लॉक, तालुका या मंडल का %',
        'desc_hi': '2025 के भूजल आकलन में अति-दोहित श्रेणी की आकलन इकाइयों (ब्लॉक, तालुका या मंडल) का हिस्सा, यानी वार्षिक निकासी वार्षिक पुनर्भरण से अधिक है। भारत में 6,762 में से 730 इकाइयां, 2024 में 6,746 में से 751। इकाई का आकार राज्य के अनुसार भिन्न है।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/cgwb/assessment-units-2025.json')))
