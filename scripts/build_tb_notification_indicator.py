#!/usr/bin/env python3
"""Add the TB case notification rate (India TB Report 2024, data for 2023) to data/interactive-data.json. --check compares.

fewCases lists territories with fewer than 100 notified cases in the year (Lakshadweep: 6)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    S = raw['states']
    return [{
        'id': 'tb_notification_rate', 'theme': 'Health', 'name': 'TB Case Notification Rate',
        'unit': 'notified cases per lakh population', 'source': 'Central TB Division, India TB Report 2024', 'year': '2023',
        'desc': 'TB patients notified (public and private sector) in 2023 per lakh population, India TB Report 2024, Table 1.2. It counts cases the health system found and reported, not cases that exist: a higher rate can mean more TB, better case finding, or both. The report publishes state incidence nowhere (the national modelled incidence is 199 per lakh for 2022), so this is a different measure from incidence. A state or territory is counted where the patient was notified, not where they live.',
        'higherIsBetter': None, 'national': raw['india']['rate'],
        'values': {s: d['rate'] for s, d in S.items()},
        'fewCases': sorted(s for s, d in S.items() if d['notified'] < 100),
        'sourceUrl': raw['url'], 'retrieved': '2026-10-19',
        'name_hi': 'टीबी मामला अधिसूचना दर', 'unit_hi': 'प्रति लाख जनसंख्या अधिसूचित मामले',
        'desc_hi': '2023 में अधिसूचित टीबी रोगी (सार्वजनिक और निजी क्षेत्र) प्रति लाख जनसंख्या, इंडिया टीबी रिपोर्ट 2024, तालिका 1.2। यह उन मामलों की गिनती है जिन्हें स्वास्थ्य व्यवस्था ने खोजा और दर्ज किया, मौजूद मामलों की नहीं: ऊँची दर का अर्थ अधिक टीबी, बेहतर खोज या दोनों हो सकता है। यह राज्यों की घटना दर (इन्सिडेंस) नहीं है।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/ntep/tb-notification-2023.json')))
