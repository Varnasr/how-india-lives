#!/usr/bin/env python3
"""Add rural tap water coverage (JJM, July 2026) and solid waste generated per person (CPCB, 2023-24) to data/interactive-data.json.
--check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def tap(raw):
    return {s: d['tap_pct'] for s, d in raw['states'].items()}


def waste(raw):
    pop = {s: v['population_lakh'] for s, v in load('data/ncrb/crime-in-india-2024-other.json')['states'].items()}
    v = {s: round(d['generated'] * 1e6 / (pop[s] * 1e5), 0) for s, d in raw['states'].items()}  # tonnes a day -> grams a person a day
    return v, round(raw['india']['generated'] * 1e6 / (sum(pop.values()) * 1e5), 0)


def build():
    j = load('data/jjm/tap-connections-2026-07.json')
    w = load('data/cpcb/solid-waste-2023-24.json')
    wv, wn = waste(w)
    return [{
        'id': 'jjm_tap_pct', 'theme': 'Infrastructure', 'name': 'Rural Households with Tap Water Supply', 'unit': '% of rural households',
        'source': 'Ministry of Jal Shakti, Lok Sabha Starred Question 62 (23 July 2026), Annexure (JJM IMIS)', 'year': 'as on 18 Jul 2026',
        'desc': 'Rural households reported by the state as having tap water supply under the Jal Jeevan Mission, as a share of all rural households, as on 18 July 2026. India: 82.09% (15.89 crore of 19.36 crore households), up from 16.72% in August 2019. The count is of connections reported by states in the Mission\'s own monitoring system, not of supply that runs or water that is safe. Delhi and Chandigarh have no rural population.',
        'higherIsBetter': True, 'national': j['india']['tap_pct'], 'values': tap(j), 'sourceUrl': j['url'], 'retrieved': j['retrieved'],
        'name_hi': 'नल जल आपूर्ति वाले ग्रामीण परिवार', 'unit_hi': 'ग्रामीण परिवारों का %',
        'desc_hi': 'जल जीवन मिशन के अंतर्गत राज्यों द्वारा बताए गए नल जल आपूर्ति वाले ग्रामीण परिवार, सभी ग्रामीण परिवारों के हिस्से के रूप में, 18 जुलाई 2026 तक। भारत: 82.09% (अगस्त 2019 में 16.72%)। यह मिशन की निगरानी प्रणाली में राज्यों द्वारा बताए गए कनेक्शनों की गिनती है, चालू या सुरक्षित आपूर्ति की नहीं।',
    }, {
        'id': 'cpcb_waste_pc', 'theme': 'Environment', 'name': 'Solid Waste Generated per Person', 'unit': 'grams per person per day',
        'source': 'MoEFCC, Lok Sabha Unstarred Question 50 (1 December 2025), Annexure (CPCB, 2023-24), with NCRB 2024 population projections', 'year': '2023-24',
        'desc': 'Solid waste generated in tonnes a day as reported by each State Pollution Control Board or Committee for 2023-24, divided by the state\'s 2024 population projection as printed by NCRB. India: 132 grams a person a day (1,85,195 tonnes a day). The boards report by different methods, some weigh and some estimate, and some report urban waste only, while the denominator is the whole population, so the spread between states reflects reporting as much as waste.',
        'higherIsBetter': None, 'national': wn, 'values': wv, 'sourceUrl': w['url'], 'retrieved': w['retrieved'],
        'name_hi': 'प्रति व्यक्ति उत्पन्न ठोस अपशिष्ट', 'unit_hi': 'ग्राम प्रति व्यक्ति प्रति दिन',
        'desc_hi': '2023-24 में प्रत्येक राज्य प्रदूषण नियंत्रण बोर्ड द्वारा बताया गया ठोस अपशिष्ट (टन प्रतिदिन), NCRB की 2024 जनसंख्या अनुमान से भाग देकर। भारत: 132 ग्राम प्रति व्यक्ति प्रति दिन। बोर्ड अलग-अलग विधियों से और कुछ केवल शहरी अपशिष्ट बताते हैं, इसलिए राज्यों का अंतर रिपोर्टिंग को भी दर्शाता है।',
    }]


if __name__ == '__main__':
    write_indicators(build())
