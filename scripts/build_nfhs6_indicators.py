#!/usr/bin/env python3
"""Add NFHS-6 (2023-24) indicators to data/interactive-data.json from data/nfhs6/states.json.

    python3 scripts/build_nfhs6_indicators.py          # rewrite the n6_* indicators
    python3 scripts/build_nfhs6_indicators.py --check  # fail if the file is out of date

Every indicator is the state or UT total printed in the NFHS-6 fact sheets, with the
NFHS-5 total printed beside it in the same sheet carried as `previous`, so a change is
always between two figures the survey itself put side by side. A state with no printed
figure (Manipur has no NFHS-6 sheet; small samples are left blank) has no value, and
no value is ever filled in. `fewCases` lists states whose figure is in parentheses in
the source, meaning it rests on 25 to 49 unweighted cases.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RETRIEVED = '2026-10-19'
URL = 'https://www.nfhsiips.in/'
GEO = {'Andaman & Nicobar Islands': 'Andaman and Nicobar'}

# number in the fact sheet, id, theme, English name, description, higherIsBetter, Hindi name, Hindi description
SPEC = [
    (69, 'stunting', 'Health', 'Children under 5 who are stunted',
     'Share of children under 5 whose height for age is more than two standard deviations below the WHO standard.',
     False, '5 वर्ष से कम उम्र के बौने बच्चे',
     '5 वर्ष से कम उम्र के उन बच्चों का हिस्सा जिनका कद उम्र के हिसाब से WHO मानक से दो मानक विचलन से अधिक कम है।'),
    (70, 'wasting', 'Health', 'Children under 5 who are wasted',
     'Share of children under 5 whose weight for height is more than two standard deviations below the WHO standard.',
     False, '5 वर्ष से कम उम्र के दुबले (वेस्टेड) बच्चे',
     '5 वर्ष से कम उम्र के उन बच्चों का हिस्सा जिनका वज़न कद के हिसाब से WHO मानक से दो मानक विचलन से अधिक कम है।'),
    (72, 'underweight', 'Health', 'Children under 5 who are underweight',
     'Share of children under 5 whose weight for age is more than two standard deviations below the WHO standard.',
     False, '5 वर्ष से कम उम्र के कम वज़न वाले बच्चे',
     '5 वर्ष से कम उम्र के उन बच्चों का हिस्सा जिनका वज़न उम्र के हिसाब से WHO मानक से दो मानक विचलन से अधिक कम है।'),
    (62, 'ebf', 'Health', 'Exclusive breastfeeding under 6 months',
     'Share of children under 6 months who are exclusively breastfed.',
     True, '6 महीने से कम उम्र के बच्चे जिन्हें केवल स्तनपान मिलता है',
     '6 महीने से कम उम्र के उन बच्चों का हिस्सा जिन्हें केवल माँ का दूध मिलता है।'),
    (35, 'inst_births', 'Health', 'Institutional births',
     'Share of births in the five years before the survey that took place in a health facility.',
     True, 'संस्थागत प्रसव', 'सर्वेक्षण से पहले के पाँच वर्षों में स्वास्थ्य संस्थान में हुए प्रसवों का हिस्सा।'),
    (44, 'full_vacc', 'Health', 'Children fully vaccinated, 12-23 months',
     'Share of children aged 12-23 months fully vaccinated, from a vaccination card or the mother\'s recall.',
     True, 'पूर्ण टीकाकृत बच्चे, 12-23 महीने',
     '12-23 महीने के उन बच्चों का हिस्सा जिनका पूर्ण टीकाकरण टीकाकरण कार्ड या माँ की याददाश्त के अनुसार हुआ।'),
    (38, 'csection', 'Health', 'Births delivered by caesarean section',
     'Share of births in the five years before the survey delivered by caesarean section.',
     None, 'सिज़ेरियन प्रसव', 'सर्वेक्षण से पहले के पाँच वर्षों में सिज़ेरियन से हुए प्रसवों का हिस्सा।'),
    (74, 'women_thin', 'Health', 'Women with BMI below 18.5',
     'Share of women aged 15-49 whose body mass index is below normal.',
     False, 'BMI 18.5 से कम वाली महिलाएँ', '15-49 वर्ष की उन महिलाओं का हिस्सा जिनका बॉडी मास इंडेक्स सामान्य से कम है।'),
    (76, 'women_overweight', 'Health', 'Women who are overweight or obese',
     'Share of women aged 15-49 with a body mass index of 25.0 or more.',
     False, 'अधिक वज़न या मोटापे वाली महिलाएँ', '15-49 वर्ष की उन महिलाओं का हिस्सा जिनका BMI 25.0 या उससे अधिक है।'),
    (77, 'men_overweight', 'Health', 'Men who are overweight or obese',
     'Share of men with a body mass index of 25.0 or more.',
     False, 'अधिक वज़न या मोटापे वाले पुरुष', 'उन पुरुषों का हिस्सा जिनका बॉडी मास इंडेक्स 25.0 या अधिक है।'),
    (80, 'women_sugar', 'Health', 'Women with high blood sugar',
     'Share of women aged 15 and over with blood sugar above 140 mg/dl, or taking medicine to control it.',
     False, 'उच्च रक्त शर्करा वाली महिलाएँ',
     '15 वर्ष और अधिक की उन महिलाओं का हिस्सा जिनकी रक्त शर्करा 140 mg/dl से ऊपर है या जो उसके लिए दवा ले रही हैं।'),
    (86, 'women_bp', 'Health', 'Women with elevated blood pressure',
     'Share of women aged 15 and over with systolic of 140 or more or diastolic of 90 or more, or taking medicine for it.',
     False, 'उच्च रक्तचाप वाली महिलाएँ',
     '15 वर्ष और अधिक की उन महिलाओं का हिस्सा जिनका रक्तचाप 140/90 या उससे अधिक है या जो इसके लिए दवा ले रही हैं।'),
    (89, 'men_bp', 'Health', 'Men with elevated blood pressure',
     'Share of men aged 15 and over with systolic of 140 or more or diastolic of 90 or more, or taking medicine for it.',
     False, 'उच्च रक्तचाप वाले पुरुष',
     '15 वर्ष और अधिक के उन पुरुषों का हिस्सा जिनका रक्तचाप 140/90 या उससे अधिक है या जो इसके लिए दवा ले रहे हैं।'),
    (98, 'tobacco_w', 'Health', 'Women who use tobacco',
     'Share of women aged 15 and over who use any kind of tobacco.',
     False, 'तंबाकू सेवन करने वाली महिलाएँ', '15 वर्ष और अधिक की उन महिलाओं का हिस्सा जो किसी भी रूप में तंबाकू का सेवन करती हैं।'),
    (99, 'tobacco_m', 'Health', 'Men who use tobacco',
     'Share of men aged 15 and over who use any kind of tobacco.',
     False, 'तंबाकू सेवन करने वाले पुरुष', '15 वर्ष और अधिक के उन पुरुषों का हिस्सा जो किसी भी रूप में तंबाकू का सेवन करते हैं।'),
    (101, 'alcohol_m', 'Health', 'Men who drink alcohol',
     'Share of men aged 15 and over who consume alcohol.',
     False, 'शराब पीने वाले पुरुष', '15 वर्ष और अधिक के उन पुरुषों का हिस्सा जो शराब पीते हैं।'),
    (92, 'bank_w', 'Gender', 'Women with a bank account they use',
     'Share of women aged 15-49 who have a bank or savings account that they themselves use.',
     True, 'स्वयं उपयोग किए जाने वाले बैंक खाते वाली महिलाएँ',
     '15-49 वर्ष की उन महिलाओं का हिस्सा जिनके पास अपना बैंक या बचत खाता है जिसका वे स्वयं उपयोग करती हैं।'),
    (93, 'mobile_w', 'Gender', 'Women with a mobile phone they use',
     'Share of women aged 15-49 who have a mobile phone that they themselves use.',
     True, 'स्वयं उपयोग किए जाने वाला मोबाइल फ़ोन रखने वाली महिलाएँ',
     '15-49 वर्ष की उन महिलाओं का हिस्सा जिनके पास अपना मोबाइल फ़ोन है जिसका वे स्वयं उपयोग करती हैं।'),
    (90, 'decisions_w', 'Gender', 'Married women in household decisions',
     'Share of currently married women aged 15-49 who usually take part in all three household decisions asked about.',
     True, 'घरेलू निर्णयों में भाग लेने वाली विवाहित महिलाएँ',
     'वर्तमान में विवाहित 15-49 वर्ष की उन महिलाओं का हिस्सा जो पूछे गए तीनों घरेलू निर्णयों में सामान्यतः भाग लेती हैं।'),
    (95, 'spousal_violence', 'Gender', 'Ever-married women who experienced spousal violence',
     'Share of ever-married women aged 18-49 who have ever experienced spousal violence.',
     False, 'पति द्वारा हिंसा झेलने वाली विवाहित महिलाएँ',
     '18-49 वर्ष की कभी विवाहित उन महिलाओं का हिस्सा जिन्होंने कभी पति की हिंसा का सामना किया है।'),
    (60, 'ari_care', 'Health', 'Children with fever or ARI symptoms taken to a health facility',
     'Share of children under 5 with fever or symptoms of acute respiratory infection in the two weeks before the survey who were taken to a health facility or provider.',
     True, 'बुखार या ARI लक्षण वाले बच्चे जिन्हें स्वास्थ्य केंद्र ले जाया गया',
     'सर्वेक्षण से पहले दो सप्ताह में बुखार या तीव्र श्वसन संक्रमण (ARI) के लक्षण वाले 5 वर्ष से कम बच्चों का हिस्सा जिन्हें स्वास्थ्य केंद्र या प्रदाता के पास ले जाया गया।'),
    (16, 'child_marriage', 'Gender', 'Women married before 18',
     'Share of women aged 20-24 who were married before age 18.',
     False, '18 से पहले विवाहित महिलाएँ', '20-24 वर्ष की उन महिलाओं का हिस्सा जिनका विवाह 18 वर्ष से पहले हुआ।'),
    (19, 'teen_mothers', 'Reproductive', 'Girls 15-19 already mothers or pregnant',
     'Share of women aged 15-19 who were already mothers or pregnant at the time of the survey.',
     False, '15-19 वर्ष की माँ या गर्भवती किशोरियाँ',
     '15-19 वर्ष की उन किशोरियों का हिस्सा जो सर्वेक्षण के समय माँ थीं या गर्भवती थीं।'),
    (25, 'unmet_need', 'Reproductive', 'Unmet need for family planning',
     'Share of currently married women aged 15-49 with an unmet need for family planning.',
     False, 'परिवार नियोजन की अपूर्ण आवश्यकता',
     'वर्तमान में विवाहित 15-49 वर्ष की उन महिलाओं का हिस्सा जिनकी परिवार नियोजन की आवश्यकता पूरी नहीं हुई।'),
    (6, 'iodised_salt', 'Health', 'Households using iodized salt',
     'Share of households using iodized salt.',
     True, 'आयोडीनयुक्त नमक इस्तेमाल करने वाले परिवार', 'आयोडीनयुक्त नमक इस्तेमाल करने वाले परिवारों का हिस्सा।'),
    (12, 'women_school', 'Education', 'Women with 10 or more years of schooling',
     'Share of women aged 15-49 with 10 or more years of schooling.',
     True, '10 या अधिक वर्ष की स्कूली शिक्षा वाली महिलाएँ',
     '15-49 वर्ष की उन महिलाओं का हिस्सा जिन्होंने 10 या अधिक वर्ष स्कूली शिक्षा पाई है।'),
    (14, 'women_internet', 'Education', 'Women who have ever used the internet',
     'Share of women aged 15-49 who have ever used the internet.',
     True, 'कभी इंटरनेट इस्तेमाल करने वाली महिलाएँ', '15-49 वर्ष की उन महिलाओं का हिस्सा जिन्होंने कभी इंटरनेट इस्तेमाल किया है।'),
    (5, 'improved_water', 'Health', 'Population in households with an improved drinking-water source',
     'Share of the household population living in households with an improved source of drinking water (piped water, tube well or borehole, protected well or spring, rainwater, tanker truck or bottled water), as NFHS defines it. An improved source is not the same as safe water: it says nothing about contamination, regular supply or distance.',
     True, 'बेहतर पेयजल स्रोत वाले परिवारों में रहने वाली आबादी',
     'बेहतर पेयजल स्रोत (नल का पानी, ट्यूबवेल या बोरवेल, संरक्षित कुआँ या झरना, वर्षा जल, टैंकर या बोतलबंद पानी) वाले परिवारों में रहने वाली आबादी का हिस्सा, NFHS की परिभाषा के अनुसार। बेहतर स्रोत का अर्थ सुरक्षित पानी नहीं है।'),
]


def build(n):
    india = n['states']['India']
    out = []
    for num, slug, theme, name, desc, hib, name_hi, desc_hi in SPEC:
        k = str(num)
        values, prev, few = {}, {}, []
        for s, rows in n['states'].items():
            if s == 'India' or k not in rows:
                continue
            g = GEO.get(s, s.replace('&', 'and'))
            r = rows[k]
            if r['total'] is not None:
                values[g] = r['total']
                if r['flag'] == 'few':
                    few.append(g)
            if r['nfhs5'] is not None:
                prev[g] = r['nfhs5']
        ind = {
            'id': 'n6_' + slug, 'theme': theme, 'name': name, 'unit': '%', 'source': 'NFHS-6 (2023-24)',
            'year': '2023-24', 'desc': desc, 'higherIsBetter': hib, 'national': india[k]['total'],
            'values': dict(sorted(values.items())), 'previous': dict(sorted(prev.items())),
            'previousYear': '2019-21', 'nationalPrevious': india[k]['nfhs5'],
            'sourceUrl': URL, 'retrieved': RETRIEVED,
            'name_hi': name_hi, 'desc_hi': desc_hi, 'unit_hi': '%',
        }
        if few:
            ind['fewCases'] = sorted(few)
        out.append(ind)
    return out


def main():
    n = json.load(open(os.path.join(ROOT, 'data', 'nfhs6', 'states.json')))
    path = os.path.join(ROOT, 'data', 'interactive-data.json')
    data = json.load(open(path))
    keep = [i for i in data['indicators'] if not i['id'].startswith('n6_')]
    new = build(n)
    maps = {i['id']: i.get('mapId') for i in data['indicators'] if i['id'].startswith('n6_')}
    for i in new:
        if maps.get(i['id']):
            i['mapId'] = maps[i['id']]
    merged = keep + new
    if '--check' in sys.argv:
        strip = lambda L: [{k: v for k, v in i.items() if k != 'mapId'} for i in L]
        ok = strip([i for i in data['indicators'] if i['id'].startswith('n6_')]) == strip(new)
        print('OK' if ok else 'STALE: run scripts/build_nfhs6_indicators.py')
        sys.exit(0 if ok else 1)
    data['indicators'] = merged
    note = data['note']
    if 'NFHS-6' not in note:
        data['note'] = note + (' NFHS-6 (2023-24) indicators, added in October 2026, are the state and UT totals printed in the '
                               'IIPS fact sheets of May 2026, each with the NFHS-5 total printed beside it. Manipur has no NFHS-6 '
                               'sheet and a state whose figure was left blank for a small sample is shown grey.')
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    print('wrote %d NFHS-6 indicators; file now has %d' % (len(new), len(merged)))


if __name__ == '__main__':
    main()
