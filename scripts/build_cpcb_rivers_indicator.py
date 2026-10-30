#!/usr/bin/env python3
"""Add critically polluted river stretches (CPCB 2025, Priority I) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    S = raw['states']
    return [{
        'id': 'cpcb_prs_critical', 'theme': 'Environment', 'name': 'Critically polluted river stretches', 'unit': 'stretches with BOD above 30 mg/L',
        'source': 'CPCB, Polluted River Stretches 2025', 'year': '2025',
        'desc': 'Number of river stretches or locations in the most polluted class (Priority I, biochemical oxygen demand above 30 mg/L), from monitoring in 2022 and 2023, published September 2025. A count, not a rate: states differ in river length and in how many locations are monitored. The 32 states and UTs in the CPCB table are shown; the rest had no polluted stretch listed.',
        'higherIsBetter': False, 'national': None, 'values': {s: r['priority_I'] for s, r in S.items()},
        'sourceUrl': raw['url'], 'retrieved': '2026-10-19',
        'name_hi': 'अत्यधिक प्रदूषित नदी खंड', 'unit_hi': 'BOD 30 mg/L से अधिक वाले खंड',
        'desc_hi': 'सबसे प्रदूषित वर्ग (प्राथमिकता I, जैव-रासायनिक ऑक्सीजन माँग 30 mg/L से अधिक) में नदी खंडों या स्थानों की संख्या, 2022 और 2023 की निगरानी से, सितंबर 2025 में प्रकाशित। यह गिनती है, दर नहीं: राज्यों में नदी की लंबाई और निगरानी के स्थान अलग हैं। CPCB तालिका के 32 राज्य और केंद्र शासित प्रदेश दिखाए गए हैं।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/cpcb/polluted-rivers-2025.json')))
