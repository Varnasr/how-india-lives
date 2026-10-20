#!/usr/bin/env python3
"""Add Udyam registrations per lakh people (to 30 November 2025) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def rates(raw):
    pop = {s: v['population_lakh'] for s, v in load('data/ncrb/crime-in-india-2024-other.json')['states'].items()}
    return {s: round(sum(v) / pop[s], 0) for s, v in raw['states'].items()}, round(raw['india_total'] / sum(pop.values()), 0)


def build(raw):
    v, nat = rates(raw)
    return [{
        'id': 'udyam_per_lakh', 'theme': 'Economy', 'name': 'Udyam MSME Registrations per Lakh People', 'unit': 'registrations per lakh people',
        'source': 'Ministry of MSME, Lok Sabha Unstarred Question 755 (4 December 2025), with NCRB 2024 population projections', 'year': 'to 30 Nov 2025',
        'desc': 'Registrations on the Udyam Registration Portal and the Udyam Assist Platform from 1 July 2020 to 30 November 2025, divided by the state\'s 2024 population projection as printed by NCRB (lakh people). Udyam registration is free and self-declared, and since January 2023 informal micro enterprises have been onboarded through Udyam Assist, so the figure counts registrations at the registered address and not working firms, and it moves with registration drives. India: 7.22 crore registrations.',
        'higherIsBetter': None, 'national': nat, 'values': v,
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'प्रति लाख लोगों पर उद्यम MSME पंजीकरण', 'unit_hi': 'प्रति लाख लोगों पर पंजीकरण',
        'desc_hi': '1 जुलाई 2020 से 30 नवंबर 2025 तक उद्यम पंजीकरण पोर्टल और उद्यम असिस्ट प्लेटफॉर्म पर पंजीकरण, NCRB की 2024 जनसंख्या अनुमान (लाख) से भाग देकर। यह पंजीकृत पते पर पंजीकरण की गिनती है, चालू इकाइयों की नहीं।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/msme/udyam-registrations-2025-11.json')))
