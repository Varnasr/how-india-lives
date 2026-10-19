#!/usr/bin/env python3
"""Read two Lok Sabha annexures into data/loksabha/.

    python3 scripts/extract_loksabha_tables.py PMJAY.pdf MUDRA.pdf          # writes the two JSON files
    python3 scripts/extract_loksabha_tables.py PMJAY.pdf MUDRA.pdf --check  # compares only

PMJAY.pdf  Unstarred Question 2518, 13 Feb 2026, Annexure-II: hospital admissions authorised under PM-JAY (lakh) by
           state and financial year, 2022-23 to 2025-26 (to 31 Jan 2026). The table prints no total, so the rows
           are checked for count (35 states and UTs) and format only. Delhi and Odisha joined in April 2025 and print 0.00
           before that, which means not in the scheme, not zero admissions.
MUDRA.pdf  Unstarred Question 5803, 30 Mar 2026, Annexure: PM Mudra Yojana loans to SC and ST entrepreneurs, by state, 1 Apr
           2022 to 31 Mar 2025 (number and Rs crore). The loan counts must add to the printed 3,84,16,963.
Each PDF's SHA-256 is recorded.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, GEO, sha256  # noqa: E402

PM_URL = 'https://sansad.in/getFile/loksabhaquestions/annex/187/AU2518_sNjCWQ.pdf?source=pqals'
MU_URL = 'https://sansad.in/getFile/loksabhaquestions/annex/187/AU5803_fuDmOn.pdf?source=pqals'


def text(pdf):
    return re.sub(r'[ \t]+', ' ', subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout)


def name(n):
    n = n.replace('*', '').strip().title().replace(' And ', ' and ')
    n = {'Pondicherry': 'Puducherry', 'Andaman and Nicobar Islands': 'Andaman and Nicobar', 'Islands': 'Andaman and Nicobar',
         'And Daman and Diu': 'Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu': 'Dadra and Nagar Haveli and Daman and Diu'}.get(n, n)
    return GEO.get(n, n)


def pmjay(pdf):
    t = text(pdf)
    a = t.index('State/UTs wise details of the number of hospital admissions')
    block = t[a:t.index('Annexure-III', a)]
    rows = {}
    for line in block.splitlines():
        m = re.match(r'^\s*([A-Za-z][A-Za-z &*]*?)\s+(\d+\.\d+) (\d+\.\d+) (\d+\.\d+) (\d+\.\d+)\s*$', line)
        if m:
            rows[name(m.group(1))] = [float(m.group(i)) for i in range(2, 6)]
    if len(rows) != 35:
        raise SystemExit('PM-JAY: expected 35 states and UTs, read %d: %s' % (len(rows), sorted(rows)))
    return {'source': 'Lok Sabha Unstarred Question 2518, 13 Feb 2026, Annexure-II (Ministry of Health and Family Welfare)', 'url': PM_URL, 'sha256': sha256(pdf),
            'unit': 'hospital admissions authorised, lakh', 'years': ['2022-23', '2023-24', '2024-25', '2025-26 (to 31 Jan 2026)'],
            'not_in_scheme_until_april_2025': ['Delhi', 'Odisha'], 'states': rows}


def mudra(pdf):
    t = text(pdf)
    block = t[t.index('Pradhan Mantri Mudra Yojana - State/U.T wise'):]
    rows, tot = {}, None
    lines = [l.strip() for l in block.splitlines()]
    for i, line in enumerate(lines):
        if line.startswith('TOTAL'):
            m = re.match(r'TOTAL ([\d,]+) ([\d,.]+)', line)
            tot = (int(m.group(1).replace(',', '')), float(m.group(2).replace(',', '')))
            continue
        m = re.match(r'^(\d{1,2}) ([A-Za-z &]+?) ([\d,]+) ([\d,]+)$', line)
        if m:
            n = m.group(2).strip()
            if n == 'Diu':
                n = 'Dadra and Nagar Haveli and Daman and Diu'
            rows[name(n)] = [int(m.group(3).replace(',', '')), int(m.group(4).replace(',', ''))]
    if len(rows) != 36 or tot is None:
        raise SystemExit('Mudra: expected 36 rows and a total, read %d' % len(rows))
    if sum(v[0] for v in rows.values()) != tot[0]:
        raise SystemExit('Mudra: loans add to %d, printed total is %d' % (sum(v[0] for v in rows.values()), tot[0]))
    return {'source': 'Lok Sabha Unstarred Question 5803, 30 Mar 2026, Annexure (Ministry of Finance); data uploaded by Member Lending Institutions on the Mudra portal', 'url': MU_URL,
            'sha256': sha256(pdf), 'period': '1 April 2022 to 31 March 2025', 'national_loans': tot[0], 'national_amount_rs_crore': tot[1],
            'columns': ['loans_to_sc_and_st_entrepreneurs', 'amount_rs_crore'], 'states': rows}


def main():
    pm, mu = pmjay(sys.argv[1]), mudra(sys.argv[2])
    d = os.path.join(ROOT, 'data', 'loksabha')
    if '--check' in sys.argv:
        ok = json.load(open(os.path.join(d, 'pmjay-admissions.json'))) == pm and json.load(open(os.path.join(d, 'mudra-sc-st.json'))) == mu
        print('OK' if ok else 'STALE')
        return
    os.makedirs(d, exist_ok=True)
    for f, o in (('pmjay-admissions.json', pm), ('mudra-sc-st.json', mu)):
        json.dump(o, open(os.path.join(d, f), 'w'), indent=1, ensure_ascii=False)
        open(os.path.join(d, f), 'a').write('\n')
    print('wrote', len(pm['states']), 'PM-JAY rows and', len(mu['states']), 'Mudra rows')


if __name__ == '__main__':
    main()
