#!/usr/bin/env python3
"""Read three more NCRB tables, 2024, into data/ncrb/crime-in-india-2024-other.json.

    python3 scripts/extract_ncrb_other.py VOL1.pdf VOL2.pdf          # writes the JSON
    python3 scripts/extract_ncrb_other.py VOL1.pdf VOL2.pdf --check  # compares only

Crime in India 2024 Volume 1 (Table 2A.1 murder with population, Table 2A.2 motives of murder) and
Volume 2 (Table 7A.1 crimes against Scheduled Castes). The PDFs are not committed; their SHA-256 is
recorded and must match, so a different edition is refused. Each row is read by serial number, and
the state rows must add to NCRB's own printed 'TOTAL STATE(S)', 'TOTAL UT(S)' and 'TOTAL ALL INDIA'
or the extract stops. The 36 serial numbers are the same in every table.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'ncrb', 'crime-in-india-2024-other.json')
SRC = {
    'vol1': ('https://data.opencity.in/dataset/7d883875-921a-4820-b298-713c6219bd90/resource/46f760f4-dcf4-4f95-85c9-2225e2f7bbe8/download/vol1-crimeinindia2024.pdf',
             '75b827bdcfcd5e641984d7fb549aaa2f3cdf030caace2d93853e450ee236bb4c', 'Crime in India 2024, Volume 1 (NCRB, Ministry of Home Affairs), via OpenCity'),
    'vol2': ('https://data.opencity.in/dataset/7d883875-921a-4820-b298-713c6219bd90/resource/27025829-5e66-49be-9c80-e2a4d1a1b1b8/download/2crimeinindia2024-volumeii.pdf',
             '423af46b6704338d9241fc95411fbca706b70662e79becdd4dc8f7ab0c16ae50', 'Crime in India 2024, Volume II (NCRB, Ministry of Home Affairs), via OpenCity'),
}
NAMES = {1: 'Andhra Pradesh', 2: 'Arunachal Pradesh', 3: 'Assam', 4: 'Bihar', 5: 'Chhattisgarh', 6: 'Goa', 7: 'Gujarat', 8: 'Haryana',
         9: 'Himachal Pradesh', 10: 'Jharkhand', 11: 'Karnataka', 12: 'Kerala', 13: 'Madhya Pradesh', 14: 'Maharashtra', 15: 'Manipur',
         16: 'Meghalaya', 17: 'Mizoram', 18: 'Nagaland', 19: 'Odisha', 20: 'Punjab', 21: 'Rajasthan', 22: 'Sikkim', 23: 'Tamil Nadu',
         24: 'Telangana', 25: 'Tripura', 26: 'Uttar Pradesh', 27: 'Uttarakhand', 28: 'West Bengal', 29: 'Andaman and Nicobar',
         30: 'Chandigarh', 31: 'Dadra and Nagar Haveli and Daman and Diu', 32: 'Delhi', 33: 'Jammu and Kashmir', 34: 'Ladakh',
         35: 'Lakshadweep', 36: 'Puducherry'}
NUM = r'(?:-?\d+(?:\.\d+)?|-)'


def text(pdf):
    return subprocess.run(['pdftotext', '-layout', pdf, '-'], check=True, capture_output=True, text=True).stdout


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def rows(block, ncols):
    """{serial: [cells]} and {'states','uts','india': [cells]} from one printed page of a table."""
    out, tot = {}, {}
    for line in block.splitlines():
        m = re.match(r'^\s*(\d{1,2})\s+(.*?)\s*((?:' + NUM + r'\s+){%d}' % (ncols - 1) + NUM + r')\s*$', line)
        if m and 1 <= int(m.group(1)) <= 36 and not re.search(r'\d\s*$', m.group(2)):
            out[int(m.group(1))] = m.group(3).split()
            continue
        m = re.match(r'^\s*(TOTAL STATE\(S\)|TOTAL UT\(S\)|TOTAL ALL INDIA)\s+((?:' + NUM + r'\s+){%d}' % (ncols - 1) + NUM + r')\s*$', line)
        if m:
            tot[{'TOTAL STATE(S)': 'states', 'TOTAL UT(S)': 'uts', 'TOTAL ALL INDIA': 'india'}[m.group(1)]] = m.group(2).split()
    return out, tot


def num(c):
    return None if c == '-' else (float(c) if '.' in c else int(c))


def check_totals(label, r, tot, cols):
    """Counts must add to NCRB's printed totals. Rates (non-count columns) are not summed."""
    for k, rng in (('states', range(1, 29)), ('uts', range(29, 37))):
        for c in cols:
            s = sum(num(r[i][c]) or 0 for i in rng)
            want = num(tot[k][c])
            tol = 0.5 if any('.' in x for x in (tot[k][c],)) else 1e-6   # one-decimal columns carry rounding
            if abs(s - want) > tol:
                raise SystemExit('%s: column %d %s sums to %s, NCRB prints %s' % (label, c, k, s, want))
    for c in cols:
        if abs(sum(num(tot[k][c]) for k in ('states', 'uts')) - num(tot['india'][c])) > (0.5 if '.' in tot['india'][c] else 1e-6):
            raise SystemExit('%s: column %d states + UTs differ from All India' % (label, c))


def main():
    v1, v2 = sys.argv[1], sys.argv[2]
    for k, p in (('vol1', v1), ('vol2', v2)):
        if sha(p) != SRC[k][1]:
            raise SystemExit('%s: SHA-256 differs from the edition this script was written for' % p)
    t1, t2 = text(v1), text(v2)
    # Table 2A.1: cases 2022, 2023, 2024, population (lakh), rate, chargesheeting rate
    a = t1.rindex('STATES:', 0, t1.index('TABLE 2A.1 Page 1 of 1'))
    r21, tot21 = rows(t1[a:t1.index('TABLE 2A.1 Page 1 of 1')], 6)
    # Table 2A.2 page 1 (cols 3-9) and page 2 (cols 10-16)
    i = t1.index('Motives of Murder - 2024')
    p1 = t1[i:t1.index('TABLE 2A.2 Page 1 of 4', i)]
    p2s = t1.index('Motives of Murder - 2024 (Continued)', i)
    p2 = t1[p2s:t1.index('TABLE 2A.2 Page 2 of 4', p2s)]
    r221, tot221 = rows(p1, 7)
    r222, tot222 = rows(p2, 7)
    # Table 7A.1: 2022, 2023, 2024, SC population lakh (2011), rate 2024, chargesheeting rate 2024
    j = t2.index('Crime/Atrocities against Scheduled Caste(s) - 2022-2024')
    r71, tot71 = rows(t2[j:t2.index('TABLE 7A.1 Page 1 of 1', j)], 6)
    for name, r in (('2A.1', r21), ('2A.2 p1', r221), ('2A.2 p2', r222), ('7A.1', r71)):
        if sorted(r) != list(range(1, 37)):
            raise SystemExit('%s: expected 36 rows, got serials %s' % (name, sorted(r)))
    check_totals('2A.1', r21, tot21, [0, 1, 2, 3])
    check_totals('2A.2 p1', r221, tot221, range(7))
    check_totals('2A.2 p2', r222, tot222, range(7))
    check_totals('7A.1', r71, tot71, [0, 1, 2, 3])
    out = {'source': {k: {'title': v[2], 'url': v[0], 'sha256': v[1]} for k, v in SRC.items()},
           'note': 'Counts are crimes registered with the police in 2024. Murder motives are cases of murder (Table 2A.2) by motive recorded. '
                   'SC population is the 2011 Census figure NCRB prints. Totals were checked against NCRB TOTAL STATE(S), TOTAL UT(S) and TOTAL ALL INDIA.',
           'states': {}, 'india': {}}
    for sl in range(1, 37):
        n = NAMES[sl]
        out['states'][n] = {
            'murder_2022': num(r21[sl][0]), 'murder_2023': num(r21[sl][1]), 'murder_2024': num(r21[sl][2]),
            'population_lakh': num(r21[sl][3]), 'murder_rate_2024': num(r21[sl][4]),
            'murder_witchcraft_2024': num(r221[sl][3]), 'murder_honour_2024': num(r222[sl][2]),
            'sc_crimes_2022': num(r71[sl][0]), 'sc_crimes_2023': num(r71[sl][1]), 'sc_crimes_2024': num(r71[sl][2]),
            'sc_population_lakh_2011': num(r71[sl][3]), 'sc_rate_2024': num(r71[sl][4]),
        }
    out['india'] = {'murder_2024': num(tot21['india'][2]), 'population_lakh': num(tot21['india'][3]),
                    'murder_witchcraft_2024': num(tot221['india'][3]), 'murder_honour_2024': num(tot222['india'][2]),
                    'sc_crimes_2022': num(tot71['india'][0]), 'sc_crimes_2023': num(tot71['india'][1]), 'sc_crimes_2024': num(tot71['india'][2]),
                    'sc_population_lakh_2011': num(tot71['india'][3]), 'sc_rate_2024': num(tot71['india'][4])}
    if '--check' in sys.argv:
        print('OK' if json.load(open(OUT)) == json.loads(json.dumps(out)) else 'STALE')
        return
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT)


if __name__ == '__main__':
    main()
