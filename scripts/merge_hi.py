#!/usr/bin/env python3
"""Merge subagent Hindi translation outputs (xl_*_out.json) into data/maps.json."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SD = sys.argv[1] if len(sys.argv) > 1 else '.'

merged = {}
for batch in ['A', 'B', 'C', 'D']:
    path = os.path.join(SD, f'xl_{batch}_out.json')
    d = json.load(open(path))
    for k, v in d.items():
        merged[k] = v
    print(f'batch {batch}: {len(d)} entries')

maps = json.load(open(os.path.join(ROOT, 'data', 'maps.json')))
applied = 0
for m in maps:
    t = merged.get(m['id'])
    if t and t.get('title_hi') and t.get('takeaway_hi'):
        m['title_hi'] = t['title_hi']
        m['takeaway_hi'] = t['takeaway_hi']
        applied += 1

json.dump(maps, open(os.path.join(ROOT, 'data', 'maps.json'), 'w'), ensure_ascii=False, indent=2)
total = sum(1 for m in maps if m.get('title_hi'))
have_take = sum(1 for m in maps if m.get('takeaway'))
print(f'merged this run: {applied} | total maps with title_hi: {total} / {have_take} with takeaways')
