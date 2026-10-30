#!/usr/bin/env python3
"""Add DPIIT-recognised startups per lakh people (30 June 2026) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def rates(raw):
    pop = {s: v['population_lakh'] for s, v in load('data/ncrb/crime-in-india-2024-other.json')['states'].items()}
    return {s: round(n / pop[s], 2) for s, n in raw['states'].items()}, round(raw['india'] / sum(pop.values()), 2)


def build(raw):
    v, nat = rates(raw)
    return [{
        'id': 'dpiit_startups', 'theme': 'Economy', 'name': 'DPIIT-recognised startups per lakh people', 'unit': 'startups per lakh people',
        'source': 'DPIIT, Lok Sabha Unstarred Question 1446 (28 July 2026), with NCRB 2024 population projections', 'year': '30 June 2026',
        'desc': 'Entities recognised as startups by the Department for Promotion of Industry and Internal Trade as on 30 June 2026, divided by the state\'s 2024 population projection as printed by NCRB (lakh people). A startup is counted at its registered address, so the figure measures where companies register, which concentrates in Delhi, Karnataka and Maharashtra, and not where their work or jobs are. Recognition is voluntary and does not say the business is still trading.',
        'higherIsBetter': None, 'national': nat, 'values': v,
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'प्रति लाख लोगों पर DPIIT-मान्यता प्राप्त स्टार्टअप', 'unit_hi': 'प्रति लाख लोगों पर स्टार्टअप',
        'desc_hi': 'उद्योग संवर्धन और आंतरिक व्यापार विभाग (DPIIT) द्वारा 30 जून 2026 तक मान्यता प्राप्त स्टार्टअप, NCRB की 2024 जनसंख्या अनुमान (लाख) से भाग देकर। स्टार्टअप उसके पंजीकृत पते पर गिना जाता है, इसलिए यह आंकड़ा बताता है कि कंपनियां कहां पंजीकृत हैं, काम कहां होता है यह नहीं।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/dpiit/startups-2026-06.json')))
