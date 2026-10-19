"""Shared plumbing for the scripts/build_*_indicator.py builders.

    from indicator_io import ROOT, GEO, load, sha256, write_indicators

write_indicators(new) rewrites the given indicators in data/interactive-data.json, keeps each one's mapId,
and with --check on the command line compares instead of writing (a mapId is ignored in that comparison).
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Names in the sources -> names in data/india-states.geojson
GEO = {'A&N Islands': 'Andaman and Nicobar', 'A & N Islands': 'Andaman and Nicobar', 'Andaman & Nicobar Islands': 'Andaman and Nicobar',
       'Andaman and Nicobar Islands': 'Andaman and Nicobar', 'Jammu & Kashmir': 'Jammu and Kashmir', 'J&K': 'Jammu and Kashmir',
       'DNH & DD': 'Dadra and Nagar Haveli and Daman and Diu', 'D&N Haveli and Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu',
       'DNH and Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu', 'Dadra & Nagar Haveli and Daman & Diu': 'Dadra and Nagar Haveli and Daman and Diu',
       'Dadra and Nagar Haveli and Daman and Diu': 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi UT': 'Delhi', 'NCT of Delhi': 'Delhi',
       'Orissa': 'Odisha', 'Uttaranchal': 'Uttarakhand'}


def load(path):
    return json.load(open(os.path.join(ROOT, path), encoding='utf-8'))


def sha256(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def write_indicators(new):
    path = os.path.join(ROOT, 'data', 'interactive-data.json')
    data = json.load(open(path))
    ids = {i['id'] for i in new}
    keep = {i['id']: i.get('mapId') for i in data['indicators'] if i['id'] in ids}
    for i in new:
        if keep.get(i['id']):
            i['mapId'] = keep[i['id']]
    if '--check' in sys.argv:
        strip = lambda L: [{k: v for k, v in i.items() if k != 'mapId'} for i in L]
        ok = strip([i for i in data['indicators'] if i['id'] in ids]) == strip(new)
        print('OK' if ok else 'STALE')
        sys.exit(0 if ok else 1)
    data['indicators'] = [i for i in data['indicators'] if i['id'] not in ids] + new
    json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
    open(path, 'a').write('\n')
    print('wrote %d indicator(s); %d in file' % (len(new), len(data['indicators'])))
