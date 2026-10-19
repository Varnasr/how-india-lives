#!/usr/bin/env python3
"""Write data/srs/life-expectancy-2019-23.json from Statement 3 of SRS Abridged Life Tables 2019-23.

    python3 scripts/extract_srs_life_tables.py [--check]

Source: ORGI, SRS based Abridged Life Tables 2019-23 (September 2025), Statement 3, as re-uploaded after Corrigendum
No. 15/09/2020-VS(SRS), which corrects West Bengal's urban female figure to 76.3 (the table below carries 76.3).
censusindia.gov.in serves an incomplete certificate chain, so the PDF could not be downloaded here and no SHA-256 is
pinned; the figures were read from a text extraction on 2026-10-19 and are held to these checks: the total lies between
the male and female figures in every row, between the rural and urban totals (or equals one), agrees with the report's
Chart 4 and Statement 5 (age 0) and its summary text (India 70.3, Kerala 75.1 highest, Chhattisgarh 64.6 lowest). Note that
Statement 4 of the same report prints a different 2019-23 total for some states (Andhra Pradesh 70.3, Bihar 69.0,
Gujarat 70.1, Haryana 68.6, Himachal Pradesh 73.6, Kerala 74.8) while its male and female columns match Statement 3;
Statement 3 agrees with every other table and with the text, so it is used. Jammu & Kashmir includes Ladakh. Columns:
total, male, female, rural total, rural male, rural female, urban total, urban male, urban female.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicator_io import ROOT  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'srs', 'life-expectancy-2019-23.json')
TABLE = """
India | 70.3 | 68.5 | 72.5 | 69.1 | 67.1 | 71.4 | 73.1 | 71.4 | 75.0
Andhra Pradesh | 70.7 | 68.5 | 73.3 | 69.8 | 67.4 | 72.5 | 72.8 | 71.0 | 74.9
Assam | 68.6 | 66.9 | 70.7 | 67.7 | 66.0 | 69.9 | 73.5 | 72.1 | 75.1
Bihar | 69.3 | 68.9 | 69.7 | 69.0 | 68.5 | 69.4 | 71.5 | 71.4 | 71.5
Chhattisgarh | 64.6 | 62.4 | 67.1 | 64.1 | 62.0 | 66.3 | 66.4 | 63.7 | 69.7
Delhi | 74.2 | 72.3 | 76.8 | 72.1 | 68.6 | 76.6 | 74.3 | 72.4 | 76.8
Gujarat | 70.4 | 67.6 | 73.9 | 68.6 | 65.2 | 72.9 | 72.7 | 70.6 | 75.2
Haryana | 68.8 | 65.9 | 72.2 | 67.9 | 64.8 | 71.8 | 70.1 | 67.8 | 72.9
Himachal Pradesh | 74.4 | 71.0 | 78.1 | 74.2 | 70.6 | 78.1 | 76.1 | 74.5 | 77.9
Jammu and Kashmir | 74.4 | 73.4 | 75.5 | 73.4 | 72.6 | 74.3 | 76.7 | 75.6 | 78.0
Jharkhand | 69.5 | 68.7 | 70.5 | 68.8 | 67.9 | 69.8 | 71.5 | 70.8 | 72.4
Karnataka | 70.0 | 67.8 | 72.4 | 68.5 | 65.5 | 71.8 | 72.6 | 71.9 | 73.4
Kerala | 75.1 | 71.9 | 78.4 | 75.7 | 72.5 | 78.9 | 74.6 | 71.4 | 77.8
Madhya Pradesh | 67.6 | 65.4 | 70.3 | 66.8 | 64.5 | 69.4 | 70.5 | 68.2 | 73.0
Maharashtra | 72.8 | 70.7 | 75.2 | 71.3 | 68.9 | 74.0 | 75.0 | 73.3 | 77.0
Odisha | 70.5 | 69.4 | 71.8 | 70.2 | 69.1 | 71.5 | 72.1 | 70.7 | 73.5
Punjab | 70.8 | 68.8 | 73.1 | 69.2 | 66.9 | 72.0 | 73.2 | 72.0 | 74.7
Rajasthan | 70.4 | 67.8 | 73.3 | 69.7 | 67.0 | 72.7 | 72.7 | 70.3 | 75.5
Tamil Nadu | 73.4 | 71.4 | 75.6 | 70.3 | 67.8 | 73.1 | 76.3 | 74.8 | 77.9
Telangana | 70.8 | 68.6 | 73.2 | 69.8 | 67.0 | 72.9 | 71.9 | 70.7 | 73.5
Uttar Pradesh | 68.0 | 66.5 | 69.8 | 67.4 | 65.8 | 69.3 | 70.1 | 68.7 | 71.6
Uttarakhand | 71.3 | 68.1 | 74.8 | 71.4 | 67.8 | 75.3 | 71.0 | 68.8 | 73.4
West Bengal | 72.5 | 71.1 | 74.0 | 71.4 | 69.9 | 73.1 | 74.8 | 73.5 | 76.3
"""
KEYS = ['total', 'male', 'female', 'rural_total', 'rural_male', 'rural_female', 'urban_total', 'urban_male', 'urban_female']
CHART4 = {'Kerala': 75.1, 'Jammu and Kashmir': 74.4, 'Himachal Pradesh': 74.4, 'Delhi': 74.2, 'Tamil Nadu': 73.4, 'Maharashtra': 72.8, 'West Bengal': 72.5,
          'Uttarakhand': 71.3, 'Punjab': 70.8, 'Telangana': 70.8, 'Andhra Pradesh': 70.7, 'Odisha': 70.5, 'Gujarat': 70.4, 'Rajasthan': 70.4, 'Karnataka': 70.0,
          'Jharkhand': 69.5, 'Bihar': 69.3, 'Haryana': 68.8, 'Assam': 68.6, 'Uttar Pradesh': 68.0, 'Madhya Pradesh': 67.6, 'Chhattisgarh': 64.6}


def main():
    rows = {}
    for ln in TABLE.strip().splitlines():
        p = [x.strip() for x in ln.split('|')]
        rows[p[0]] = dict(zip(KEYS, map(float, p[1:])))
    india = rows.pop('India')
    assert len(rows) == 22
    for n, d in rows.items():
        assert d['male'] <= d['total'] <= d['female'], n
        assert min(d['rural_total'], d['urban_total']) <= d['total'] <= max(d['rural_total'], d['urban_total']), n
        assert CHART4[n] == d['total'], n
    assert max(rows, key=lambda n: rows[n]['total']) == 'Kerala' and min(rows, key=lambda n: rows[n]['total']) == 'Chhattisgarh'
    assert india['total'] == 70.3 and rows['West Bengal']['urban_female'] == 76.3
    geo = {f['properties']['name'] for f in json.load(open(os.path.join(ROOT, 'data', 'india-states.geojson')))['features']}
    assert not set(rows) - geo, sorted(set(rows) - geo)
    out = {'source': 'ORGI, SRS based Abridged Life Tables 2019-23, Statement 3 (as corrected by Corrigendum 15/09/2020-VS(SRS))',
           'url': 'https://censusindia.gov.in/nada/index.php/catalog/46175', 'retrieved': '2026-10-19', 'unit': 'years', 'india': india,
           'note': 'Jammu and Kashmir includes Ladakh. Statement 4 of the report prints different totals for some states; Statement 3 is used.', 'states': rows}
    if '--check' in sys.argv:
        assert json.load(open(OUT)) == out, 'stale'
    else:
        json.dump(out, open(OUT, 'w'), indent=1, ensure_ascii=False)
        open(OUT, 'a').write('\n')
    print(len(rows), 'states')


main()
