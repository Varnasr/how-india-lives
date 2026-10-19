#!/usr/bin/env python3
"""Read women MLAs by state assembly from ADR and NEW's report (as on 2 February 2026) into data/adr/women-mlas-2026.json.

    python3 scripts/extract_adr_women.py REPORT.pdf          # writes the JSON
    python3 scripts/extract_adr_women.py REPORT.pdf --check  # compares only

Source: ADR and National Election Watch, 'Women's Political Participation and Representation in India 2026',
table 'Women MPs and MLAs in the Current Lok Sabha and State Assemblies, Elections Wise'. Each assembly's men plus
women must equal its seats, and the 31 assemblies together must give the 4,123 MLAs and 390 women the report's text
states. Assemblies are shown on the election they last held as of that date, so Assam, Kerala, Puducherry, Tamil
Nadu and West Bengal are on their 2021 results.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT, GEO, sha256  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'adr', 'women-mlas-2026.json')
URL = 'https://adrindia.org/sites/default/files/Womens_Political_Participation_and_Representation_in_India_2026_Eng.pdf'


def main():
    pdf = sys.argv[1]
    t = re.sub(r'[ \t]+', ' ', subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout)
    a = t.index('Women MPs and MLAs in the Current Lok Sabha and State Assemblies – Elections Wise')
    block = t[a:t.index('Table: Women MPs and MLAs in Assembly and Lok Sabha Elections', a)]
    rows = {}
    for m in re.finditer(r'^\s*(\d{1,2}) ([A-Za-z&. ]+?) Assembly (\d{4}) (\d+) (\d+) \d+% (\d+) \d+%\s*$', block, re.M):
        seats, men, women = int(m.group(4)), int(m.group(5)), int(m.group(6))
        if men + women != seats:
            raise SystemExit('%s: men plus women is not the seat count' % m.group(2))
        rows[GEO.get(m.group(2).strip(), m.group(2).strip())] = {'election_year': int(m.group(3)), 'seats_analysed': seats, 'women': women}
    if len(rows) != 31:
        raise SystemExit('expected 31 assemblies, read %d' % len(rows))
    if (sum(r['seats_analysed'] for r in rows.values()), sum(r['women'] for r in rows.values())) != (4123, 390):
        raise SystemExit('assemblies do not add to the 4,123 MLAs and 390 women the report states')
    out = {'source': "ADR and National Election Watch, Women's Political Participation and Representation in India 2026 (as on 2 February 2026)", 'url': URL,
           'sha256': sha256(pdf), 'states': dict(sorted(rows.items()))}
    if '--check' in sys.argv:
        print('OK' if json.load(open(OUT)) == out else 'STALE')
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print('wrote', OUT, len(rows))


if __name__ == '__main__':
    main()
