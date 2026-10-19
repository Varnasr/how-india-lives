#!/usr/bin/env python3
"""Add NCRB 2024 honour-killing, witchcraft-murder and crimes-against-SC indicators.

    python3 scripts/build_ncrb_other_indicators.py          # rewrite the indicators
    python3 scripts/build_ncrb_other_indicators.py --check  # fail if out of date

Source: data/ncrb/crime-in-india-2024-other.json (scripts/extract_ncrb_other.py). All three count
crimes REGISTERED, so no direction is claimed (higherIsBetter is null).

ncrb_sc_crimes     cases of crime against Scheduled Castes / lakh SC population (2011 Census, as NCRB prints it).
                   The printed 2024 rate is used; it is recomputed here and must agree within rounding of the population NCRB prints to 0.1 lakh. 2023 is cases over the same population. A state or UT whose SC
                   population is under 1 lakh is left grey: one case would swing its rate by more than 100.
ncrb_honour        murders recorded with 'honour killing' as the motive, per crore population (cases / population_lakh x 100)
ncrb_witchcraft    murders recorded with 'witchcraft' as the motive, per crore population
Trafficking is cases / population_lakh x 10 per 10 lakh (population as NCRB prints it with Table 14.1), with fewCases below 10 cases.
Honour and witchcraft counts are tiny (36 and 54 in India), so a single case moves a small state a long way; the text on the maps says so rather than flagging 30 states.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'data', 'ncrb', 'crime-in-india-2024-other.json')
MIN_SC_LAKH = 1.0


def build(raw):
    S, I = raw['states'], raw['india']
    pv1, pv2 = raw['source']['vol1']['url'], raw['source']['vol2']['url']
    sc, scp, few = {}, {}, []
    for s, r in S.items():
        pop = r['sc_population_lakh_2011']
        if pop is None or pop < MIN_SC_LAKH or r['sc_crimes_2024'] is None:
            continue
        v = r['sc_rate_2024'] if r['sc_rate_2024'] is not None else round(r['sc_crimes_2024'] / pop, 1)
        # NCRB divides by the unrounded 2011 population; we only have it to 0.1 lakh, so allow a rounding gap
        if abs(round(r['sc_crimes_2024'] / pop, 1) - v) > max(0.15, 0.01 * v):
            raise SystemExit('SC rate for %s: computed %s, NCRB prints %s' % (s, round(r['sc_crimes_2024'] / pop, 1), v))
        sc[s] = v
        scp[s] = round(r['sc_crimes_2023'] / pop, 1)
        if r['sc_crimes_2024'] < 10:
            few.append(s)
    nat = round(I['sc_crimes_2024'] / I['sc_population_lakh_2011'], 1)
    out = [{
        'id': 'ncrb_sc_crimes', 'theme': 'Caste', 'name': 'Crimes Against Scheduled Castes Recorded', 'unit': 'cases per lakh SC population',
        'source': 'NCRB (Crime in India 2024, Volume II)', 'year': '2024',
        'desc': 'Crime and atrocity cases against Scheduled Castes registered by the police, per lakh Scheduled Caste population (Census 2011). It counts registrations, not incidence. States and territories with under 1 lakh Scheduled Caste people are left grey.',
        'higherIsBetter': None, 'national': nat, 'values': dict(sorted(sc.items())), 'previous': dict(sorted(scp.items())), 'previousYear': '2023',
        'nationalPrevious': round(I['sc_crimes_2023'] / I['sc_population_lakh_2011'], 1), 'fewCases': sorted(few),
        'sourceUrl': pv2, 'retrieved': '2026-10-19',
        'name_hi': 'अनुसूचित जातियों के विरुद्ध दर्ज अपराध', 'unit_hi': 'मामले प्रति लाख अनुसूचित जाति आबादी',
        'desc_hi': 'पुलिस में दर्ज अनुसूचित जातियों के विरुद्ध अपराध और अत्याचार के मामले, प्रति लाख अनुसूचित जाति आबादी (जनगणना 2011)। यह दर्ज मामलों की गिनती है, घटनाओं की नहीं। जिन राज्यों में अनुसूचित जाति आबादी 1 लाख से कम है, वे ग्रे हैं।',
    }]
    for key, iid, name, desc, nhi, dhi in (
        ('murder_honour_2024', 'ncrb_honour', 'Honour Killings Recorded',
         'Murders registered with honour killing as the recorded motive, per crore population. A zero means none recorded as such, which is not the same as none occurring.',
         'दर्ज ऑनर किलिंग', 'हत्या के वे मामले जिनमें दर्ज उद्देश्य ऑनर किलिंग है, प्रति करोड़ आबादी। शून्य का अर्थ है इस रूप में कोई मामला दर्ज नहीं हुआ, यह नहीं कि कोई घटना हुई ही नहीं।'),
        ('murder_witchcraft_2024', 'ncrb_witchcraft', 'Murders Linked to Witchcraft Recorded',
         'Murders registered with witchcraft as the recorded motive, per crore population. A zero means none recorded as such, which is not the same as none occurring.',
         'डायन-शिकार से जुड़ी दर्ज हत्याएँ', 'हत्या के वे मामले जिनमें दर्ज उद्देश्य डायन/जादू-टोना है, प्रति करोड़ आबादी। शून्य का अर्थ है इस रूप में कोई मामला दर्ज नहीं हुआ, यह नहीं कि कोई घटना हुई ही नहीं।')):
        vals = {}
        for s, r in S.items():
            if r[key] is None or not r['population_lakh']:
                continue
            vals[s] = round(r[key] / r['population_lakh'] * 100, 2)
        out.append({
            'id': iid, 'theme': 'Gender', 'name': name, 'unit': 'cases per crore population',
            'source': 'NCRB (Crime in India 2024, Volume 1)', 'year': '2024', 'desc': desc, 'higherIsBetter': None,
            'national': round(I[key] / I['population_lakh'] * 100, 2), 'values': dict(sorted(vals.items())), 
            'sourceUrl': pv1, 'retrieved': '2026-10-19', 'name_hi': nhi, 'unit_hi': 'मामले प्रति करोड़ आबादी', 'desc_hi': dhi,
        })
    tp, tprev, tfew = {}, {}, []
    for s, r in S.items():
        if r['trafficking_2024'] is None or not r['population_lakh']:
            continue
        tp[s] = round(r['trafficking_2024'] / r['population_lakh'] * 10, 2)
        tprev[s] = round(r['trafficking_2023'] / r['population_lakh'] * 10, 2)
        if r['trafficking_2024'] < 10:
            tfew.append(s)
    out.append({
        'id': 'ncrb_trafficking', 'theme': 'Economy', 'name': 'Human Trafficking Cases Recorded', 'unit': 'cases per 10 lakh population',
        'source': 'NCRB (Crime in India 2024, Volume III)', 'year': '2024',
        'desc': 'Human trafficking cases registered by the police (from their Anti Human Trafficking Units), per 10 lakh population, 2024, with 2023 beside it. It counts registrations, not incidence, and a state with few cases moves a long way on one case.',
        'higherIsBetter': None, 'national': round(I['trafficking_2024'] / I['population_lakh'] * 10, 2), 'values': dict(sorted(tp.items())),
        'previous': dict(sorted(tprev.items())), 'previousYear': '2023', 'nationalPrevious': round(I['trafficking_2023'] / I['population_lakh'] * 10, 2),
        'fewCases': sorted(tfew), 'sourceUrl': raw['source']['vol3']['url'], 'retrieved': '2026-10-19',
        'name_hi': 'दर्ज मानव तस्करी के मामले', 'unit_hi': 'मामले प्रति 10 लाख आबादी',
        'desc_hi': 'पुलिस (उनकी मानव तस्करी निरोधक इकाइयों) में दर्ज मानव तस्करी के मामले, प्रति 10 लाख आबादी, 2024, 2023 के साथ। यह दर्ज मामलों की गिनती है, घटनाओं की नहीं, और कम मामलों वाले राज्य में एक मामला आँकड़े को बहुत बदल देता है।',
    })
    return out


def main():
    raw = json.load(open(SRC))
    path = os.path.join(ROOT, 'data', 'interactive-data.json')
    data = json.load(open(path))
    new = build(raw)
    ids = {i['id'] for i in new}
    keepmap = {i['id']: i.get('mapId') for i in data['indicators'] if i['id'] in ids}
    for i in new:
        if keepmap.get(i['id']):
            i['mapId'] = keepmap[i['id']]
    if '--check' in sys.argv:
        have = [i for i in data['indicators'] if i['id'] in ids]
        ok = have == new
        print('OK' if ok else 'STALE')
        sys.exit(0 if ok else 1)
    data['indicators'] = [i for i in data['indicators'] if i['id'] not in ids] + new
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    print('wrote', len(new), 'indicators;', len(data['indicators']), 'in file')


if __name__ == '__main__':
    main()
