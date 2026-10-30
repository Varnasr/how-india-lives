#!/usr/bin/env python3
"""Add bank offices per lakh people (RBI Table 152, March 2025) to data/interactive-data.json. --check compares.

Offices at end-March 2025 divided by the 2024 population NCRB prints (the National Commission on Population's projection,
in lakh), so the two are a year apart. The same population divides the 2024 offices for the previous value, so the change
shown is the change in offices alone."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    pop = {s: v['population_lakh'] for s, v in load('data/ncrb/crime-in-india-2024-other.json')['states'].items()}
    S = raw['states']
    assert set(S) == set(pop), sorted(set(S) ^ set(pop))
    cur = {s: round(S[s]['2025'] / pop[s], 2) for s in sorted(S)}
    prev = {s: round(S[s]['2024'] / pop[s], 2) for s in sorted(S)}
    tot = sum(pop.values())
    return [{
        'id': 'rbi_bank_offices', 'theme': 'Economy', 'name': 'Bank offices per lakh people', 'unit': 'offices per lakh population',
        'source': 'RBI Handbook of Statistics on Indian States 2024-25 (Table 152)', 'year': 'Mar 2025',
        'desc': 'Offices of scheduled commercial banks at the end of March 2025 per lakh people, using the 2024 population projection NCRB prints, so numerator and denominator are a year apart. Offices are counted where the branch is, not where its customers live, so small and urban states with head offices read high. Regional rural banks, cooperative banks, post offices and business correspondents are not counted, and in the north-east and the hills much banking reaches people through them. Dadra and Nagar Haveli includes Daman and Diu.',
        'higherIsBetter': None, 'national': round(raw['india']['2025'] / tot, 2),
        'values': cur, 'previous': prev, 'previousYear': 'Mar 2024 (offices only)', 'nationalPrevious': round(raw['india']['2024'] / tot, 2),
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'प्रति लाख लोगों पर बैंक कार्यालय', 'unit_hi': 'प्रति लाख जनसंख्या पर कार्यालय',
        'desc_hi': 'मार्च 2025 के अंत में अनुसूचित वाणिज्यिक बैंकों के कार्यालय प्रति लाख लोगों पर, NCRB की 2024 की जनसंख्या प्रक्षेपण के साथ, इसलिए अंश और हर में एक वर्ष का अंतर है। कार्यालय वहाँ गिने जाते हैं जहाँ शाखा है, ग्राहक जहाँ रहते हैं वहाँ नहीं। क्षेत्रीय ग्रामीण बैंक, सहकारी बैंक, डाकघर और बिज़नेस करेस्पॉन्डेंट शामिल नहीं हैं।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/rbi/bank-offices-2025.json')))
