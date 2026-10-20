#!/usr/bin/env python3
"""Add rural hours of power supply, 2021-22, to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402

Y = '2021-22'


def hours(raw):
    return {s: d[Y]['rural'] for s, d in raw['states'].items() if d[Y]['rural']}


def build():
    raw = load('data/power/supply-hours-2022.json')
    return [{
        'id': 'power_hours_rural', 'theme': 'Infrastructure', 'name': 'Rural Power Supply, Hours a Day', 'unit': 'average hours a day',
        'source': 'Ministry of Power, Rajya Sabha Unstarred Question 3185 (28 March 2023), Annexure I', 'year': Y,
        'desc': 'Average hours of power supply a day on rural 11 kV feeders in 2021-22, as reported by distribution utilities to the National Power Portal. Only 20 states and Puducherry report a rural figure for the year, and the rest are left grey. The figure is the utility\'s own reporting on feeders, not what a household measures. India: 20.5 hours.',
        'higherIsBetter': True, 'national': raw['all_india'][Y]['rural'], 'values': hours(raw), 'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'ग्रामीण बिजली आपूर्ति, घंटे प्रतिदिन', 'unit_hi': 'औसत घंटे प्रतिदिन',
        'desc_hi': '2021-22 में ग्रामीण 11 केवी फीडरों पर प्रतिदिन बिजली आपूर्ति के औसत घंटे, जैसा वितरण कंपनियों ने राष्ट्रीय विद्युत पोर्टल पर बताया। केवल 20 राज्य और पुडुचेरी ग्रामीण आंकड़ा देते हैं, बाकी धूसर हैं। यह कंपनी की अपनी रिपोर्टिंग है, घरों में मापी गई आपूर्ति नहीं। भारत: 20.5 घंटे।',
    }]


if __name__ == '__main__':
    write_indicators(build())
