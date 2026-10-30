#!/usr/bin/env python3
"""Add women's share of MLAs (ADR, as on 2 Feb 2026) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    S = raw['states']
    seats, women = sum(r['seats_analysed'] for r in S.values()), sum(r['women'] for r in S.values())
    return [{
        'id': 'adr_women_mlas', 'theme': 'Democracy', 'name': 'Women among MLAs', 'unit': '% of assembly seats', 'source': 'ADR and National Election Watch (as on 2 Feb 2026)', 'year': '2026',
        'desc': 'Women as a share of sitting MLAs in each state assembly as on 2 February 2026, on the results of the last election held there. Assam, Kerala, Puducherry, Tamil Nadu and West Bengal are on their 2021 results. Ladakh has no assembly and is not shown.',
        'higherIsBetter': True, 'national': round(women / seats * 100, 1), 'values': {s: round(r['women'] / r['seats_analysed'] * 100, 1) for s, r in S.items()},
        'sourceUrl': raw['url'], 'retrieved': '2026-10-19',
        'name_hi': 'विधायकों में महिलाएँ', 'unit_hi': 'विधानसभा सीटों का %',
        'desc_hi': '2 फरवरी 2026 तक प्रत्येक विधानसभा के मौजूदा विधायकों में महिलाओं का हिस्सा, वहाँ हुए पिछले चुनाव के नतीजों पर। असम, केरल, पुदुचेरी, तमिलनाडु और पश्चिम बंगाल 2021 के नतीजों पर हैं। लद्दाख में विधानसभा नहीं है।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/adr/women-mlas-2026.json')))
