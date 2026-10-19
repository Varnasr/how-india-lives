#!/usr/bin/env python3
"""Read Table A.6 (key health financing indicators, select states) of National Health Accounts 2022-23.

    python3 scripts/extract_nha_states.py NHA_2022-23.pdf          # writes data/nha/states-2022-23.json
    python3 scripts/extract_nha_states.py NHA_2022-23.pdf --check  # compares only

Source: MoHFW / NHSRC, National Health Accounts Estimates for India 2022-23 (May 2026), Annexure A.2. 21 states
(no UTs, and no small or north-eastern states beyond Assam, because the out-of-pocket estimate rests on a survey too
small to give them). Each row has 16 figures after the state name. Every row is checked against itself: the
share of total health expenditure that is government and out of pocket must equal the ratio of the crore figures
(to 0.15 point), and each per-capita figure must equal expenditure over the printed population (population is
printed to 0.1 crore, so 4%). Out-of-pocket spending is estimated from the NSS 75th round (2017-18), as the report says.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, GEO, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'nha', 'states-2022-23.json')
URL = 'https://nhsrcindia.org/sites/default/files/2026-05/NHA%202022-23%20Report.pdf'
FIELDS = ['the_cr', 'the_pct_gsdp', 'the_pc', 'ghe_cr', 'ghe_pct_the', 'ghe_pct_gsdp', 'ghe_pct_gge', 'ghe_pc',
          'oope_cr', 'oope_pct_the', 'oope_pct_gsdp', 'oope_pct_gge', 'oope_pc', 'population_crore', 'gsdp_rs_lakh_or_cr', 'gge']
NUM = r'\d[\d,]*(?:\.\d+)?'


def f(x):
    return float(x.replace(',', ''))


def main():
    pdf = sys.argv[1]
    t = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    a = t.index('Table A. 6: Key Health Financing Indicators for select States')
    block = t[a:t.index('Table A.6 presents key health financing indicators', a)]
    rows = {}
    for m in re.finditer(r'^\s*(\d{1,2})\s+([A-Za-z][A-Za-z ]+?)\s{2,}((?:' + NUM + r'\s+){15}' + NUM + r')\s*$', block, re.M):
        rows[m.group(2).strip()] = dict(zip(FIELDS, [f(x) for x in m.group(3).split()]))
    if len(rows) != 21:
        raise SystemExit('expected 21 states, read %d: %s' % (len(rows), sorted(rows)))
    for s, r in rows.items():
        for share, part in (('ghe_pct_the', 'ghe_cr'), ('oope_pct_the', 'oope_cr')):
            if abs(r[part] / r['the_cr'] * 100 - r[share]) > 0.15:
                raise SystemExit('%s: %s does not equal %s / total health expenditure' % (s, share, part))
        for pc, cr in (('the_pc', 'the_cr'), ('ghe_pc', 'ghe_cr'), ('oope_pc', 'oope_cr')):
            if abs(r[cr] * 1e7 / (r['population_crore'] * 1e7) - r[pc]) > 0.04 * r[pc]:
                raise SystemExit('%s: %s does not equal %s over population' % (s, pc, cr))
    out = {'source': 'MoHFW / NHSRC, National Health Accounts Estimates for India 2022-23, Annexure A.2, Table A.6', 'url': URL, 'sha256': sha256(pdf),
           'states': {GEO.get(k, k): v for k, v in sorted(rows.items())}}
    if '--check' in sys.argv:
        print('OK' if json.load(open(OUT)) == out else 'STALE')
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT, len(rows))


if __name__ == '__main__':
    main()
