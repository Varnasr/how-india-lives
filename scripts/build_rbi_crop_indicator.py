#!/usr/bin/env python3
"""Add the rice-and-sugarcane share of rice, sugarcane and coarse-cereal area (RBI Handbook 2024-25) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def share(raw, i):
    out = {}
    for s in raw['rice']:
        if s == 'ALL INDIA':
            continue
        c = raw['coarse_cereals'].get(s, [None, None])[i]
        if c is None:
            continue
        r = raw['rice'][s][i]
        g = (raw['sugarcane'].get(s, [0, 0])[i]) or 0
        out[s] = round((r + g) / (r + g + c) * 100, 1)
    return out


def national(raw, i):
    r, c, g = raw['rice']['ALL INDIA'][i], raw['coarse_cereals']['ALL INDIA'][i], raw['sugarcane']['ALL INDIA'][i]
    return round((r + g) / (r + g + c) * 100, 1)


def build(raw):
    return [{
        'id': 'rbi_thirsty_share', 'theme': 'Environment', 'name': 'Rice and Sugarcane Share of Rice, Sugarcane and Coarse Cereal Area',
        'unit': '% of the three crops\' area',
        'source': 'Ministry of Agriculture area statistics, via RBI Handbook of Statistics on Indian States 2024-25 (Tables 67, 69, 78)', 'year': '2024-25',
        'desc': 'Area under rice and sugarcane as a share of the combined area under rice, sugarcane and coarse cereals (millets, maize and barley), 2024-25. Rice and sugarcane are the two crops that draw most irrigation water; coarse cereals are the dryland alternative. It compares three crop groups only: plantation crops, fodder, wheat, pulses and oilseeds are outside it, so Kerala\'s high share reflects that coconut and rubber are not counted. Goa has no coarse-cereal area in the source and is left out. Sugarcane area missing from the table (Delhi, Sikkim) counts as zero.',
        'higherIsBetter': None, 'national': national(raw, 1),
        'values': share(raw, 1), 'previous': share(raw, 0), 'previousYear': '2023-24', 'nationalPrevious': national(raw, 0),
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'चावल और गन्ने का हिस्सा (चावल, गन्ना और मोटे अनाज के क्षेत्र में)', 'unit_hi': 'तीनों फसलों के क्षेत्र का %',
        'desc_hi': 'चावल, गन्ना और मोटे अनाज (बाजरा, मक्का, जौ) के कुल क्षेत्र में चावल और गन्ने का हिस्सा, 2024-25। चावल और गन्ना सबसे अधिक सिंचाई का पानी लेते हैं। यह केवल तीन फसल समूहों की तुलना है; बागान फसलें, चारा, गेहूं, दालें और तिलहन इसमें नहीं हैं। गोवा में स्रोत में मोटे अनाज का क्षेत्र नहीं है, इसलिए छोड़ा गया है।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/rbi/crop-area-2024.json')))
