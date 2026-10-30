#!/usr/bin/env python3
"""Add three Ministry of Rural Development indicators to data/interactive-data.json: MGNREGA women's share of persondays and
households completing 100 days (State Performance Report 2024-25), and women SHGs per lakh people (Lok Sabha Q.3687, 2026).
--check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402

SPR = 'https://www.dord.gov.in/static/uploads/2025/09/d81193f25cde78b36f36b559ffabbb18.pdf'


def mgnrega(raw):
    """West Bengal had no approved Labour Budget (0 persondays) and Lakshadweep shows 0: both are left out of both series."""
    live = {s: d for s, d in raw['states'].items() if d['persondays'] > 0}
    return ({s: d['women_pct'] for s, d in live.items()}, {s: d['hh_100_days_pct'] for s, d in live.items()})


def shg_rates(raw):
    pop = {s: v['population_lakh'] for s, v in load('data/ncrb/crime-in-india-2024-other.json')['states'].items()}
    return {s: round(n / pop[s], 0) for s, n in raw['states'].items()}, round(raw['india_total'] / sum(pop.values()), 0)


def build():
    m = load('data/mord/mgnrega-2024-25.json')
    women, hh100 = mgnrega(m)
    shg = load('data/mord/nrlm-shgs-2026.json')
    rates, nat = shg_rates(shg)
    common = {'retrieved': m['retrieved']}
    return [{
        'id': 'mgnrega_women_pct', 'theme': 'Gender', 'name': 'Women\'s share of MGNREGA persondays', 'unit': '% of persondays',
        'source': 'Ministry of Rural Development, State Performance Report 2024-25, Annexure II', 'year': '2024-25',
        'desc': 'Share of the persondays of work generated under the Mahatma Gandhi NREGA in 2024-25 that went to women, as printed in whole per cent. West Bengal (no Labour Budget was approved, so no work is recorded) and Lakshadweep (no work recorded) are left out. The Act asks that at least one third of the persondays go to women. India: 58%.',
        'higherIsBetter': None, 'national': m['all_india']['women_pct'], 'values': women, 'sourceUrl': SPR, **common,
        'name_hi': 'मनरेगा कार्य-दिवसों में महिलाओं का हिस्सा', 'unit_hi': 'कार्य-दिवसों का %',
        'desc_hi': '2024-25 में महात्मा गांधी नरेगा के अंतर्गत सृजित कार्य-दिवसों में महिलाओं का हिस्सा, पूर्ण प्रतिशत में। पश्चिम बंगाल (कोई श्रम बजट स्वीकृत नहीं हुआ) और लक्षद्वीप (कोई कार्य दर्ज नहीं) शामिल नहीं हैं। अधिनियम के अनुसार कम से कम एक तिहाई कार्य-दिवस महिलाओं को मिलने चाहिए। भारत: 58%।',
    }, {
        'id': 'mgnrega_100_days_pct', 'theme': 'Economy', 'name': 'Households completing 100 days of MGNREGA work', 'unit': '% of households that worked',
        'source': 'Ministry of Rural Development, State Performance Report 2024-25, Annexure I', 'year': '2024-25',
        'desc': 'Per cent of households that completed 100 days of work under the Mahatma Gandhi NREGA in 2024-25, as printed in whole per cent. The base is households that worked: the report counts 40,66,631 such households against 5.78 crore that worked. West Bengal (no Labour Budget was approved) and Lakshadweep (no work recorded) are left out. India: 7%.',
        'higherIsBetter': None, 'national': m['all_india']['hh_100_days_pct'], 'values': hh100, 'sourceUrl': SPR, **common,
        'name_hi': 'मनरेगा में 100 दिन का काम पूरा करने वाले परिवार', 'unit_hi': 'काम करने वाले परिवारों का %',
        'desc_hi': '2024-25 में महात्मा गांधी नरेगा में 100 दिन का काम पूरा करने वाले परिवारों का प्रतिशत, पूर्ण प्रतिशत में। आधार काम करने वाले परिवार हैं (5.78 करोड़ में से 40,66,631)। पश्चिम बंगाल और लक्षद्वीप शामिल नहीं हैं। भारत: 7%।',
    }, {
        'id': 'nrlm_shg_per_lakh', 'theme': 'Gender', 'name': 'Women self-help groups per lakh people', 'unit': 'groups per lakh people',
        'source': 'Ministry of Rural Development, Lok Sabha Unstarred Question 3687 (11 August 2026), Annexure I, with NCRB 2024 population projections', 'year': 'to August 2026',
        'desc': 'Women self-help groups set up under DAY-NRLM since the Mission began, 92.30 lakh in all, divided by the state\'s 2024 population projection as printed by NCRB (lakh people). The count is of groups and not of members, it is cumulative and includes groups that have since stopped meeting, and the denominator is the whole population and not the rural population the Mission works in, so heavily urban states and territories read low. Delhi and Chandigarh are outside the Mission. India: 657.',
        'higherIsBetter': None, 'national': nat, 'values': rates, 'sourceUrl': shg['url'], 'retrieved': shg['retrieved'],
        'name_hi': 'प्रति लाख लोगों पर महिला स्वयं सहायता समूह', 'unit_hi': 'प्रति लाख लोगों पर समूह',
        'desc_hi': 'DAY-NRLM के अंतर्गत मिशन की शुरुआत से बने महिला स्वयं सहायता समूह (कुल 92.30 लाख), NCRB की 2024 जनसंख्या अनुमान (लाख) से भाग देकर। यह समूहों की गिनती है, सदस्यों की नहीं, और हर में पूरी जनसंख्या है, ग्रामीण नहीं, इसलिए अधिक शहरी राज्य कम दिखते हैं। दिल्ली और चंडीगढ़ मिशन के बाहर हैं। भारत: 657।',
    }]


if __name__ == '__main__':
    write_indicators(build())
