#!/usr/bin/env python3
"""Add government and out-of-pocket health spending (NHA 2022-23) to data/interactive-data.json. --check compares."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import load, write_indicators  # noqa: E402


def build(raw):
    S = raw['states']
    common = dict(theme='Health', source='National Health Accounts 2022-23 (MoHFW/NHSRC)', year='2022-23', sourceUrl=raw['url'], retrieved='2026-10-19', national=None)
    return [
        dict(common, id='nha_ghe_pc', name='Government health spending per person', unit='Rs per person',
             desc='Health spending by all government agencies (Union, state and local) in the state, per person, 2022-23. Only 21 states are covered because the survey behind the estimate is too small for the rest.',
             higherIsBetter=True, values={s: round(v['ghe_pc']) for s, v in S.items()},
             name_hi='प्रति व्यक्ति सरकारी स्वास्थ्य व्यय', unit_hi='रुपये प्रति व्यक्ति',
             desc_hi='राज्य में सभी सरकारी एजेंसियों (केंद्र, राज्य और स्थानीय) का स्वास्थ्य व्यय, प्रति व्यक्ति, 2022-23। केवल 21 राज्य शामिल हैं क्योंकि शेष के लिए अनुमान का आधार सर्वेक्षण बहुत छोटा है।'),
        dict(common, id='nha_oope_share', name='Out-of-pocket share of health spending', unit='% of total health expenditure',
             desc='Households\' own payments at the point of care as a share of all health spending in the state, 2022-23. It rests on the NSS 75th round (2017-18) for household spending. Only 21 states are covered.',
             higherIsBetter=False, values={s: v['oope_pct_the'] for s, v in S.items()},
             name_hi='स्वास्थ्य व्यय में जेब से भुगतान का हिस्सा', unit_hi='कुल स्वास्थ्य व्यय का %',
             desc_hi='राज्य के कुल स्वास्थ्य व्यय में परिवारों के अपने जेब से भुगतान का हिस्सा, 2022-23। घरेलू खर्च का आधार NSS का 75वाँ दौर (2017-18) है। केवल 21 राज्य शामिल हैं।'),
    ]


if __name__ == '__main__':
    write_indicators(build(load('data/nha/states-2022-23.json')))
