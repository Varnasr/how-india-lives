#!/usr/bin/env python3
"""Add state GSDP per head and sector shares of value added to data/interactive-data.json.

    python3 scripts/build_nas_indicators.py          # rewrite the indicators
    python3 scripts/build_nas_indicators.py --check  # fail if out of date

Source: data/mospi/nas-state.json (scripts/fetch_mospi_nas.py), MoSPI National Accounts, base 2011-12,
current prices, 2024-25 with 2022-23 beside it.

gsdp_pc          per capita GSDP at current prices, Rs, as published (indicator 31)
gsva_agri        agriculture, livestock, forestry and fishing, % of total gross state value added
gsva_mfg         manufacturing, % of total GSVA
gsva_services    services, % of total GSVA. Services = trade, repair, hotels and restaurants; transport, storage and
                 communication; financial services; real estate, dwellings and professional services; public
                 administration; other services. Mining, electricity and construction are not services.
Each state's 12 industry rows must add to its published Total (within 0.01%) or the build stops. There is no
all-India row for these series, so no national figure is given. Nagaland and Ladakh have 2022-23 but no
2024-25 figure and stay grey.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = {'Andaman & Nicobar Islands': 'Andaman and Nicobar', 'Jammu & Kashmir': 'Jammu and Kashmir'}
AGRI = 'Agriculture, Livestock, Forestry and Fishing'
MFG = 'Manufacturing'
TOTAL = 'Total Gross State Value Added'
OTHER = ['Mining and Quarrying', 'Electricity, Gas, Water Supply & Other Utility Services', 'Construction']
SERV = ['Trade, Repair, Hotels and Restaurants', 'Transport, Storage, Communication & Services Related to Broadcasting', 'Financial Services',
        'Real Estate, Ownership of Dwelling & Professional Services', 'Public Administration', 'Other Services']


def gva(raw):
    """{year: {state: {industry: Rs lakh}}} from the top-level industry rows only."""
    out = {}
    for r in raw['gsva']:
        if r['subindustry'] is not None:
            continue
        out.setdefault(r['year'], {}).setdefault(GEO.get(r['state'], r['state']), {})[r['industry']] = float(r['current_price'])
    for y, st in out.items():
        for s, d in st.items():
            parts = sum(d[k] for k in [AGRI, MFG] + OTHER + SERV)
            if abs(parts - d[TOTAL]) > 1e-4 * d[TOTAL]:
                raise SystemExit('%s %s: industries sum to %s, total is %s' % (s, y, parts, d[TOTAL]))
    return out


def build(raw):
    g = gva(raw)
    pc = {}
    for r in raw['per_capita_gsdp']:
        pc.setdefault(r['year'], {})[GEO.get(r['state'], r['state'])] = float(r['current_price'])
    url = 'https://mospi.gov.in/national-accounts-statistics'
    common = dict(theme='Economy', source='MoSPI (National Accounts, state series)', year='2024-25', previousYear='2022-23', sourceUrl=url,
                  retrieved=raw['retrieved'], national=None)
    out = [dict(common, id='gsdp_pc', name='GSDP per Head', unit='Rs per person, current prices',
                desc='Gross state domestic product per head of population, at current prices, 2024-25 (an estimate that states revise), with 2022-23 beside it. A state with a small, rich or enclave economy ranks high without that meaning its residents are better off.',
                higherIsBetter=True, values={s: round(v) for s, v in sorted(pc['2024-25'].items())},
                previous={s: round(v) for s, v in sorted(pc['2022-23'].items())},
                name_hi='प्रति व्यक्ति राज्य सकल घरेलू उत्पाद', unit_hi='रुपये प्रति व्यक्ति, वर्तमान मूल्य',
                desc_hi='राज्य के सकल घरेलू उत्पाद को जनसंख्या से भाग देने पर प्रति व्यक्ति आँकड़ा, वर्तमान मूल्यों पर, 2024-25 (अनुमान, जिसे राज्य संशोधित करते हैं), 2022-23 के साथ।')]
    for iid, name, hi, parts, desc, dhi in (
        ('gsva_agri', 'Agriculture Share of State Output', 'राज्य उत्पादन में कृषि का हिस्सा', [AGRI],
         'Agriculture, livestock, forestry and fishing as a share of gross state value added, at current prices.', 'वर्तमान मूल्यों पर राज्य सकल मूल्य वर्धन में कृषि, पशुपालन, वानिकी और मत्स्य पालन का हिस्सा।'),
        ('gsva_mfg', 'Manufacturing Share of State Output', 'राज्य उत्पादन में विनिर्माण का हिस्सा', [MFG],
         'Manufacturing as a share of gross state value added, at current prices.', 'वर्तमान मूल्यों पर राज्य सकल मूल्य वर्धन में विनिर्माण का हिस्सा।'),
        ('gsva_services', 'Services Share of State Output', 'राज्य उत्पादन में सेवाओं का हिस्सा', SERV,
         'Services (trade and hotels, transport and communication, finance, real estate and professional services, public administration, other services) as a share of gross state value added, at current prices. Mining, electricity and construction are not counted as services.',
         'वर्तमान मूल्यों पर राज्य सकल मूल्य वर्धन में सेवाओं (व्यापार और होटल, परिवहन और संचार, वित्त, रियल एस्टेट और पेशेवर सेवाएँ, लोक प्रशासन, अन्य सेवाएँ) का हिस्सा। खनन, बिजली और निर्माण सेवाओं में नहीं गिने गए।')):
        def share(y):
            return {s: round(sum(d[p] for p in parts) / d[TOTAL] * 100, 1) for s, d in sorted(g[y].items())}
        out.append(dict(common, id=iid, name=name, unit='% of gross state value added', desc=desc, higherIsBetter=None,
                        values=share('2024-25'), previous=share('2022-23'), name_hi=hi, unit_hi='राज्य सकल मूल्य वर्धन का %', desc_hi=dhi))
    return out


def main():
    raw = json.load(open(os.path.join(ROOT, 'data', 'mospi', 'nas-state.json')))
    path = os.path.join(ROOT, 'data', 'interactive-data.json')
    data = json.load(open(path))
    new = build(raw)
    ids = {i['id'] for i in new}
    keep = {i['id']: i.get('mapId') for i in data['indicators'] if i['id'] in ids}
    for i in new:
        if keep.get(i['id']):
            i['mapId'] = keep[i['id']]
    if '--check' in sys.argv:
        ok = [i for i in data['indicators'] if i['id'] in ids] == new
        print('OK' if ok else 'STALE')
        sys.exit(0 if ok else 1)
    data['indicators'] = [i for i in data['indicators'] if i['id'] not in ids] + new
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    print('wrote', len(new), 'indicators;', len(data['indicators']), 'in file')


if __name__ == '__main__':
    main()
