#!/usr/bin/env python3
"""Read Tables 1.1 and 1.2 of the India TB Report 2024 into data/ntep/tb-notification-2023.json.

    python3 scripts/extract_tb_notification.py INDIA_TB_REPORT_2024.pdf [--check]

Source: Central TB Division, MoHFW, India TB Report 2024 (data for 2023). Table 1.2 gives the TB patients notified in 2023
(public, private, total) and the notification rate per lakh population by state and UT; Table 1.1 gives the 2023
population in lakhs. Checks: public plus private equals total in every row, the 36 rows sum to the INDIA row, and
notified / population x 1,00,000 reproduces the printed total rate within 0.5 per lakh. A notification rate counts
cases the health system found and reported, not cases that exist: a high rate can mean more TB, better case finding,
or both. The report does not publish state-level incidence (its modelled incidence is national only: 199 per lakh).
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'ntep', 'tb-notification-2023.json')
URL = 'https://tbcindia.gov.in/'
DNH = 'Dadra and Nagar Haveli and Daman and Diu'


def rows(seg):
    out = {}
    for ln in seg.splitlines():
        t = re.sub(r'\(\s*[\d.]+\s*\)', '', ln)
        m = re.match(r'^\s*([A-Za-z][A-Za-z ]*?)\s+((?:[\d.]+(?:%)?\s+|NA\s+){5,}[\d.NA%]+)\s*$', t)
        if m:
            nm = m.group(1).strip()
            nm = 'Andaman and Nicobar' if nm == 'Andaman and Nicobar Islands' else nm
            nm = DNH if nm.startswith('Dadra and Nagar Haveli') else nm
            out[nm] = [None if x == 'NA' else float(x.rstrip('%')) for x in m.group(2).split()]
    return out


def main():
    t = subprocess.run(['pdftotext', '-layout', sys.argv[1], '-'], capture_output=True, text=True).stdout
    a = t.index('1.1. Presumptive TB cases examination', t.index('153 India TB Report 2024') - 200)
    b = t.index('1.2. TB case notification', a)
    c = t.index('1.3. Notified TB patients', b)
    pop = {k: v[0] for k, v in rows(t[a:b]).items()}
    n = rows(t[b:c])
    out = {}
    for k, v in n.items():
        if k == 'INDIA':
            continue
        # numbers: target pub, priv, total, notified pub, priv, total, rate pub, priv, total
        assert len(v) == 9, (k, v)
        out[k] = {'target': v[2], 'notified_public': v[3], 'notified_private': v[4], 'notified': v[5],
                  'rate_public': v[6], 'rate_private': v[7], 'rate': v[8], 'population_lakh': pop[k]}
    ind = n['INDIA']
    assert len(out) == 36, (len(out), sorted(out))
    for k, d in out.items():
        assert abs(d['notified_public'] + (d['notified_private'] or 0) - d['notified']) <= 1, k
        calc = d['notified'] / (d['population_lakh'] * 1e5) * 1e5
        assert abs(calc - d['rate']) <= 0.5, (k, calc, d['rate'])
    assert sum(d['notified'] for d in out.values()) == ind[5], (sum(d['notified'] for d in out.values()), ind[5])
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    bad = sorted(set(out) - geo)
    assert not bad, bad
    res = {'source': 'Central TB Division, India TB Report 2024, Tables 1.1 and 1.2 (2023)', 'url': URL, 'sha256': sha256(sys.argv[1]),
           'india': {'notified': ind[5], 'rate': ind[8], 'rate_public': ind[6], 'rate_private': ind[7], 'population_lakh': pop['INDIA']}, 'states': dict(sorted(out.items()))}
    print(len(out), 'states; missing:', sorted(geo - set(out)))
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == res, 'stale'
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(res, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')


main()
