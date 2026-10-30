#!/usr/bin/env python3
"""Add each state's share of India's inward remittances (RBI survey, 2023-24) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    S = raw['states']
    return [{
        'id': 'rbi_remit_share', 'theme': 'Economy', 'name': "Share of India's inward remittances",
        'unit': "% of India's inward remittances", 'source': "RBI, India's Remittances Survey, sixth round (2023-24)", 'year': '2023-24',
        'desc': "Each state's and UT's share of the US$ 118.7 billion India received in inward remittances in 2023-24, from the sixth round of RBI's Remittances Survey (RBI Bulletin, March 2025, Table 2). The shares add to 100. It says where remittances land in total, which follows both population and how many people from the state work abroad; it is not remittances per person and not how much a state depends on them. The 2020-21 round's share is shown as the previous value where that round listed the state separately.",
        'higherIsBetter': None, 'national': None,
        'values': {s: d['2023-24'] for s, d in S.items()},
        'previous': {s: d['2020-21'] for s, d in S.items() if d['2020-21'] is not None}, 'previousYear': '2020-21', 'nationalPrevious': None,
        'sourceUrl': raw['url'], 'retrieved': '2026-10-19',
        'name_hi': 'भारत के आवक विप्रेषण में हिस्सा', 'unit_hi': 'भारत के आवक विप्रेषण का %',
        'desc_hi': 'RBI के विप्रेषण सर्वेक्षण के छठे दौर (2023-24) के अनुसार 2023-24 में भारत को मिले 118.7 अरब डॉलर के आवक विप्रेषण में प्रत्येक राज्य और केंद्र शासित प्रदेश का हिस्सा। हिस्सों का योग 100 है। यह प्रति व्यक्ति विप्रेषण नहीं है और न ही यह बताता है कि राज्य उन पर कितना निर्भर है।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/rbi/remittances-2023-24.json')))
