#!/usr/bin/env python3
"""Add public hospital beds, PM-JAY admissions and Mudra loans to SC and ST borrowers to data/interactive-data.json.

    python3 scripts/build_loksabha_indicators.py          # rewrite them
    python3 scripts/build_loksabha_indicators.py --check  # fail if out of date

Beds (data/health/public-beds-2023.json): beds at PHC, CHC, sub-district and district hospitals and medical colleges, 31 March 2023, per lakh
  people, on NCRB's 2024 projected state populations. Maharashtra is left off (the source's medical-college column does not add to its total by
  exactly Maharashtra's entry). No national figure: the printed total may omit Maharashtra's medical-college beds.
PM-JAY (data/loksabha/pmjay-admissions.json): admissions authorised in FY 2024-25 per lakh people, with FY 2022-23 beside it. Delhi and Odisha joined in
  April 2025 and West Bengal is not in the scheme, so they have no figure. No national figure for the same reason.
Mudra (data/loksabha/mudra-sc-st.json): loans to SC and ST entrepreneurs, April 2022 to March 2025, per lakh SC plus ST population (Census 2011, from
  NCRB Tables 7A.1 and 7C.1). A state with under 1 lakh SC plus ST people is left off.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build():
    pop = load('data/ncrb/crime-in-india-2024-other.json')
    P = pop['states']
    beds, pm, mu = load('data/health/public-beds-2023.json'), load('data/loksabha/pmjay-admissions.json'), load('data/loksabha/mudra-sc-st.json')
    bv = {}
    for s, r in beds['states'].items():
        if s in beds['unreliable']:
            continue
        bv[s] = round(sum(v or 0 for v in r.values()) / P[s]['population_lakh'])
    pv, pp, notin = {}, {}, set(pm['not_in_scheme_until_april_2025'])
    for s, r in pm['states'].items():
        if s in notin:
            continue
        pv[s] = round(r[2] / P[s]['population_lakh'] * 1e5)
        pp[s] = round(r[0] / P[s]['population_lakh'] * 1e5)
    mv, few = {}, []
    for s, (loans, amt) in mu['states'].items():
        base = P[s]['sc_population_lakh_2011'] + P[s]['st_population_lakh_2011']
        if base < 1.0:
            continue
        mv[s] = round(loans / base)
    nat_mu = round(mu['national_loans'] / (pop['india']['sc_population_lakh_2011'] + pop['india']['st_population_lakh_2011']))
    return [
        {'id': 'ls_public_beds', 'theme': 'Health', 'name': 'Public Hospital Beds per Lakh People', 'unit': 'beds per lakh population',
         'source': 'Lok Sabha answer 1000 of 25 July 2025 (Health Dynamics of India 2022-23)', 'year': '2023', 'national': None,
         'desc': 'Beds in government facilities (primary and community health centres, sub-district and district hospitals, and medical colleges) as on 31 March 2023, per lakh people on 2024 projected populations. It counts public beds only. Maharashtra is left off because the source\'s medical-college column does not add up.',
         'higherIsBetter': True, 'values': dict(sorted(bv.items())), 'sourceUrl': beds['url'], 'retrieved': '2026-10-19',
         'name_hi': 'प्रति लाख आबादी पर सरकारी अस्पताल के बिस्तर', 'unit_hi': 'बिस्तर प्रति लाख आबादी',
         'desc_hi': '31 मार्च 2023 तक सरकारी सुविधाओं (प्राथमिक और सामुदायिक स्वास्थ्य केंद्र, उप-जिला और जिला अस्पताल, और मेडिकल कॉलेज) में बिस्तर, 2024 के अनुमानित जनसंख्या आँकड़ों पर प्रति लाख आबादी। इसमें केवल सरकारी बिस्तर हैं। महाराष्ट्र छोड़ा गया है क्योंकि स्रोत का मेडिकल कॉलेज स्तंभ जुड़ता नहीं।'},
        {'id': 'pmjay_admissions', 'theme': 'Health', 'name': 'PM-JAY Hospital Admissions per Lakh People', 'unit': 'admissions per lakh population',
         'source': 'Lok Sabha answer 2518 of 13 Feb 2026 (PM-JAY)', 'year': '2024-25', 'previousYear': '2022-23', 'national': None,
         'desc': 'Hospital admissions authorised under PM-JAY in FY 2024-25, per lakh people on 2024 projected populations, with FY 2022-23 beside it. Delhi and Odisha joined in April 2025 and West Bengal is not in the scheme, so they are grey.',
         'higherIsBetter': None, 'values': dict(sorted(pv.items())), 'previous': dict(sorted(pp.items())), 'sourceUrl': pm['url'], 'retrieved': '2026-10-19',
         'name_hi': 'प्रति लाख आबादी पर PM-JAY अस्पताल भर्ती', 'unit_hi': 'भर्ती प्रति लाख आबादी',
         'desc_hi': 'वित्त वर्ष 2024-25 में PM-JAY के तहत स्वीकृत अस्पताल भर्ती, 2024 के अनुमानित जनसंख्या आँकड़ों पर प्रति लाख आबादी, वित्त वर्ष 2022-23 के साथ। दिल्ली और ओडिशा अप्रैल 2025 में जुड़े और पश्चिम बंगाल योजना में नहीं है, इसलिए वे ग्रे हैं।'},
        {'id': 'mudra_sc_st', 'theme': 'Economy', 'name': 'Mudra Loans to SC and ST Entrepreneurs', 'unit': 'loans per lakh SC and ST people, three years',
         'source': 'Lok Sabha answer 5803 of 30 Mar 2026 (PM Mudra Yojana)', 'year': '2022-25', 'national': nat_mu,
         'desc': 'Number of PM Mudra Yojana loans to SC and ST entrepreneurs, April 2022 to March 2025, per lakh Scheduled Caste and Scheduled Tribe people (Census 2011). It counts loans, not borrowers, and SC and ST are reported together. States with under 1 lakh SC and ST people are grey.',
         'higherIsBetter': None, 'values': dict(sorted(mv.items())), 'sourceUrl': mu['url'], 'retrieved': '2026-10-19',
         'name_hi': 'SC और ST उद्यमियों को मुद्रा ऋण', 'unit_hi': 'ऋण प्रति लाख SC और ST आबादी, तीन वर्ष',
         'desc_hi': 'अप्रैल 2022 से मार्च 2025 तक SC और ST उद्यमियों को प्रधानमंत्री मुद्रा योजना के ऋणों की संख्या, प्रति लाख अनुसूचित जाति और जनजाति आबादी (जनगणना 2011)। यह ऋणों की गिनती है, उधारकर्ताओं की नहीं, और SC और ST साथ में दिए गए हैं। जिन राज्यों में SC और ST आबादी 1 लाख से कम है, वे ग्रे हैं।'},
    ]


if __name__ == '__main__':
    write_indicators(build())
