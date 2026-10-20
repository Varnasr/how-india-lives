#!/usr/bin/env python3
"""Add the stage of groundwater extraction (CGWB 2024 assessment, 2023 beside it) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    S = raw['states']
    cur = {s: d['2024']['stage'] for s, d in S.items()}
    prev = {s: d['2023']['stage'] for s, d in S.items() if d['2023']['stage'] is not None}
    return [{
        'id': 'cgwb_stage', 'theme': 'Environment', 'name': 'Stage of Groundwater Extraction', 'unit': '% of annual extractable resource',
        'source': 'CGWB 2024 assessment, via RBI Handbook of Statistics on Indian States 2024-25 (Table 107)', 'year': '2024',
        'desc': 'Annual groundwater extraction as a share of the annual extractable resource, from the Central Ground Water Board\'s 2024 assessment as the RBI Handbook prints it. Above 100 per cent more is drawn each year than the assessment counts as recharged. A state average hides block-level over-exploitation and wide differences between aquifers, and Daman and Diu is counted with Dadra and Nagar Haveli in 2024. The 2023 assessment is shown beside it for every state except Dadra and Nagar Haveli and Daman and Diu.',
        'higherIsBetter': False, 'national': round(raw['india']['2024']['stage'], 1),
        'values': cur, 'previous': prev, 'previousYear': '2023', 'nationalPrevious': round(raw['india']['2023']['stage'], 1),
        'sourceUrl': raw['url'], 'retrieved': raw['retrieved'],
        'name_hi': 'भूजल दोहन का स्तर', 'unit_hi': 'वार्षिक निकासी योग्य संसाधन का %',
        'desc_hi': 'केंद्रीय भूजल बोर्ड के 2024 आकलन से वार्षिक भूजल निकासी, वार्षिक निकासी योग्य संसाधन के प्रतिशत के रूप में, जैसा RBI हैंडबुक छापती है। 100 प्रतिशत से ऊपर का अर्थ है कि आकलन की पुनर्भरण मात्रा से अधिक पानी हर साल निकाला जाता है। राज्य का औसत ब्लॉक स्तर की अति-निकासी को छिपा देता है।',
    }]


if __name__ == '__main__':
    write_indicators(build(load('data/rbi/groundwater-2024.json')))
