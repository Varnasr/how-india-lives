#!/usr/bin/env python3
"""Write every indicator, and every calculation behind a derived one, to CSV.

    python3 scripts/export_csv.py          # write data/csv/
    python3 scripts/export_csv.py --check  # fail if any file is missing or stale

data/csv/all-indicators.csv         one row per state per indicator (long format)
data/csv/indicators/<id>.csv        the same, one file per indicator
data/csv/calculations/<id>.csv      the inputs and the arithmetic, for indicators that are
                                    derived from other figures or built from several rows
data/CALCULATIONS.md explains each formula in words.

The CSVs are built from data/interactive-data.json and the source files beside it, never typed.
Where an indicator is derived, its inputs are recomputed here independently and compared with the
indicator's own values; a mismatch stops the export, so a calculation file cannot disagree with
the map it documents.
"""
import csv
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import build_nfhs6_indicators as n6  # noqa: E402
import build_ncrb_indicators as ncrb  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'csv')


def load(p):
    return json.load(open(os.path.join(ROOT, p), encoding='utf-8'))


def rows_to_csv(header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(header)
    w.writerows(rows)
    return buf.getvalue()


def fmt(v):
    if v is None:
        return ''
    if isinstance(v, float) and v == int(v) and abs(v) < 1e15:
        return str(int(v)) if abs(v) >= 100 else repr(v)
    return str(v)


def indicator_files(inds):
    files = {}
    hdr = ['indicator_id', 'indicator', 'state', 'value', 'unit', 'year', 'previous_value', 'previous_year', 'change',
           'small_sample', 'source', 'source_url', 'retrieved']
    allrows = []
    for i in inds:
        rows = []
        prev = i.get('previous', {})
        few = set(i.get('fewCases', []))
        for s, v in sorted(i['values'].items()):
            p = prev.get(s)
            rows.append([i['id'], i['name'], s, fmt(v), i['unit'], i['year'], fmt(p), i.get('previousYear', '') if p is not None else '',
                         fmt(round(v - p, 4)) if p is not None else '', 'yes' if s in few else '', i['source'], i.get('sourceUrl', ''), i.get('retrieved', '')])
        if i.get('national') is not None:
            p = i.get('nationalPrevious')
            rows.append([i['id'], i['name'], 'India (national figure as published or computed)', fmt(i['national']), i['unit'], i['year'],
                         fmt(p), i.get('previousYear', '') if p is not None else '', fmt(round(i['national'] - p, 4)) if p is not None else '',
                         '', i['source'], i.get('sourceUrl', ''), i.get('retrieved', '')])
        files['indicators/%s.csv' % i['id']] = rows_to_csv(hdr, rows)
        allrows += rows
    files['all-indicators.csv'] = rows_to_csv(hdr, allrows)
    return files


def check_equal(label, got, want, tol=1e-9):
    bad = sorted(k for k in set(got) | set(want) if k not in got or k not in want or abs(got[k] - want[k]) > tol)
    if bad:
        raise SystemExit('%s: calculation does not reproduce the indicator for %s' % (label, bad[:6]))


def nfhs6_calcs(by):
    nf = load('data/nfhs6/states.json')
    files = {}
    for num, slug, *_ in n6.SPEC:
        iid = 'n6_' + slug
        rows, got = [], {}
        for s, sheet in sorted(nf['states'].items()):
            r = sheet.get(str(num))
            if s == 'India' or not r:
                continue
            g = n6.GEO.get(s, s.replace('&', 'and'))
            rows.append([g, num, fmt(r['urban']), fmt(r['rural']), fmt(r['total']), fmt(r['nfhs5']),
                         fmt(round(r['total'] - r['nfhs5'], 4)) if r['total'] is not None and r['nfhs5'] is not None else '',
                         'yes' if r['flag'] == 'few' else ''])
            if r['total'] is not None:
                got[g] = r['total']
        check_equal(iid, got, by[iid]['values'])
        files['calculations/%s.csv' % iid] = rows_to_csv(
            ['state', 'fact_sheet_indicator_no', 'nfhs6_urban', 'nfhs6_rural', 'nfhs6_total', 'nfhs5_total_printed_in_same_sheet',
             'change_points (nfhs6_total - nfhs5_total)', 'small_sample_25_to_49_cases'], rows)
    return files


def ncrb_calcs(by):
    raw = load('data/ncrb/crimes-against-women.json')
    y24, y23 = raw['years']['2024'], raw['years']['2023']
    files = {}
    for code, iid, _n, _u, _d, fac, dec, *_ in ncrb.SPEC:
        rows, got = [], {}
        for s in sorted(y24['codes'][code]):
            if s in ncrb.SKIP or s.endswith(')') or s == 'Delhi City':
                continue
            c24, c23 = y24['codes'][code][s], y23['codes'][code].get(s, {})
            g = ncrb.GEO.get(s, s.replace('&', 'and'))
            pop = y24['population_lakh'].get(s)
            v = ncrb.value(y24, code, s, fac, dec)
            if v is not None:
                got[g] = v
            rows.append([g, fmt(c24.get('cases')), fmt(pop), fmt(c24.get('rate')), fmt(v),
                         'printed NCRB rate' if fac is None else 'cases / female_population_lakh x %d' % fac,
                         fmt(c23.get('cases')), fmt(c23.get('rate'))])
        check_equal(iid, got, by[iid]['values'])
        files['calculations/%s.csv' % iid] = rows_to_csv(
            ['state', 'cases_2024', 'female_population_lakh_2024', 'ncrb_printed_rate_per_lakh_2024', 'mapped_value_2024', 'how_mapped_value_is_got',
             'cases_2023', 'ncrb_printed_rate_per_lakh_2023'], rows)
    return files


def ncrb_other_calcs(by):
    raw = load('data/ncrb/crime-in-india-2024-other.json')
    S = raw['states']
    files = {}
    rows, got = [], {}
    for s, r in sorted(S.items()):
        pop = r['sc_population_lakh_2011']
        if pop < 1.0:
            rows.append([s, r['sc_crimes_2024'], pop, fmt(r['sc_rate_2024']), '', r['sc_crimes_2023'], '', 'excluded: under 1 lakh Scheduled Caste population'])
            continue
        got[s] = r['sc_rate_2024']
        rows.append([s, r['sc_crimes_2024'], pop, fmt(r['sc_rate_2024']), fmt(round(r['sc_crimes_2024'] / pop, 1)),
                     r['sc_crimes_2023'], fmt(round(r['sc_crimes_2023'] / pop, 1)), ''])
    check_equal('ncrb_sc_crimes', got, by['ncrb_sc_crimes']['values'])
    files['calculations/ncrb_sc_crimes.csv'] = rows_to_csv(
        ['state', 'cases_2024', 'sc_population_lakh_2011', 'ncrb_printed_rate_2024 (mapped value)', 'recomputed_rate_2024 (cases / population)',
         'cases_2023', 'rate_2023 (cases_2023 / population)', 'note'], rows)
    for key, iid in (('murder_honour_2024', 'ncrb_honour'), ('murder_witchcraft_2024', 'ncrb_witchcraft')):
        rows, got = [], {}
        for s, r in sorted(S.items()):
            v = round(r[key] / r['population_lakh'] * 100, 2)
            got[s] = v
            rows.append([s, r[key], r['population_lakh'], v, r['murder_2024']])
        check_equal(iid, got, by[iid]['values'])
        files['calculations/%s.csv' % iid] = rows_to_csv(
            ['state', 'murders_with_this_motive_2024', 'population_lakh (as printed with Table 2A.1)', 'cases_per_crore_population (cases / population_lakh x 100)',
             'all_murders_2024'], rows)
    return files


def nas_calcs(by):
    import build_nas_indicators as nas
    raw = load('data/mospi/nas-state.json')
    g = nas.gva(raw)
    files = {}
    pc = {}
    for r in raw['per_capita_gsdp']:
        pc.setdefault(r['year'], {})[nas.GEO.get(r['state'], r['state'])] = r['current_price']
    check_equal('gsdp_pc', {s: float(v) for s, v in pc['2024-25'].items()}, by['gsdp_pc']['values'], tol=0.5)
    files['calculations/gsdp_pc.csv'] = rows_to_csv(
        ['state', 'per_capita_gsdp_rs_2022_23', 'per_capita_gsdp_rs_2024_25 (mapped value)'],
        [[s, pc['2022-23'].get(s, ''), pc['2024-25'].get(s, '')] for s in sorted(set(pc['2022-23']) | set(pc['2024-25']))])
    for iid, parts in (('gsva_agri', [nas.AGRI]), ('gsva_mfg', [nas.MFG]), ('gsva_services', nas.SERV)):
        rows, got = [], {}
        for s in sorted(g['2024-25']):
            d, d0 = g['2024-25'][s], g['2022-23'].get(s)
            num = sum(d[p] for p in parts)
            v = round(num / d[nas.TOTAL] * 100, 1)
            got[s] = v
            rows.append([s, fmt(num), fmt(d[nas.TOTAL]), v, fmt(round(sum(d0[p] for p in parts) / d0[nas.TOTAL] * 100, 1)) if d0 else ''])
        check_equal(iid, got, by[iid]['values'])
        files['calculations/%s.csv' % iid] = rows_to_csv(
            ['state', 'sector_gsva_2024_25_rs_lakh (' + ' + '.join(parts) + ')', 'total_gsva_2024_25_rs_lakh', 'share_pct_2024_25 (sector / total x 100, 1 dp)', 'share_pct_2022_23'], rows)
    return files


def court_calcs(by):
    raw = load('data/courts/lok-sabha-3501.json')
    pend = raw['pending_cases_district_subordinate_courts']['by_state']
    jud = raw['judicial_officers_subordinate_judiciary']['by_state']
    WBAN = 'West Bengal and Andaman and Nicobar (combined)'
    rows, got, vrows, vgot = [], {}, [], {}
    for s in sorted(pend):
        p = pend[s]
        note, jname = '', s
        if s == 'Dadra and Nagar Haveli and Daman and Diu':
            a, b = jud['Dadra and Nagar Haveli (judges)'], jud['Daman and Diu (judges)']
            sanc, work = a['sanctioned'] + b['sanctioned'], a['working'] + b['working']
            note = 'judges are two rows in the source (Dadra and Nagar Haveli; Daman and Diu) and are added'
        elif s in ('West Bengal', 'Andaman and Nicobar'):
            sanc, work = jud[WBAN]['sanctioned'], jud[WBAN]['working']
            note = 'the judges table merges West Bengal with Andaman and Nicobar; pendency of both is added and one ratio is shown for each'
        else:
            sanc, work = jud[s]['sanctioned'], jud[s]['working']
        if p.get('unreliable'):
            rows.append([s, fmt(p['total']), sanc, work, '', 'excluded: ' + p['unreliable']])
        else:
            tot = p['total']
            if s in ('West Bengal', 'Andaman and Nicobar'):
                tot = pend['West Bengal']['total'] + pend['Andaman and Nicobar']['total']
            v = round(tot / work)
            got[s] = v
            rows.append([s, tot, sanc, work, v, note])
        vac = round((sanc - work) / sanc * 100, 1)
        vgot[s] = vac
        vrows.append([s, sanc, work, sanc - work, vac, note])
    check_equal('court_pending_per_judge', got, by['court_pending_per_judge']['values'])
    check_equal('court_vacancy_pct', vgot, by['court_vacancy_pct']['values'])
    return {
        'calculations/court_pending_per_judge.csv': rows_to_csv(
            ['state', 'pending_cases_used (NJDG 2026-03-09, civil+criminal)', 'sanctioned_judicial_officers', 'working_judicial_officers',
             'pending_per_working_judge (pending / working, rounded)', 'note'], rows),
        'calculations/court_vacancy_pct.csv': rows_to_csv(
            ['state', 'sanctioned', 'working', 'vacant (sanctioned - working)', 'vacancy_pct (vacant / sanctioned x 100, 1 dp)', 'note'], vrows),
    }


def climate_calcs(by):
    raw = load('data/climate/envstats.json')
    f = raw['forest_cover_sq_km']
    skip = {'Puducherry (source row)', 'Dadra and Nagar Haveli (source row)', 'Daman and Diu and Dadra Nagar Haveli (source row)'}
    rows, got = [], {}
    for s in sorted(f['isfr_2023']):
        a, b = f['isfr_2021'].get(s), f['isfr_2023'][s]
        if s in skip:
            why = {'Puducherry (source row)': 'excluded: this row is the India total in the source, not Puducherry'}.get(s, 'excluded: row cannot be assigned to the merged UT with confidence')
            rows.append([s, fmt(a), fmt(b), '', why])
        else:
            c = round(b - a, 2)
            got[s] = c
            rows.append([s, fmt(a), fmt(b), fmt(c), ''])
    check_equal('forest_change', got, by['forest_change']['values'])
    h = raw['heat_wave_days']['values']
    hrows, hgot = [], {}
    for s in sorted(h):
        v = h[s]
        if all(x is not None for x in v):
            m = round(sum(v) / 3, 1)
            hgot[s] = m
            hrows.append([s, v[0], v[1], v[2], m, ''])
        else:
            hrows.append([s, *['' if x is None else x for x in v], '', 'excluded: a year is missing in the source'])
    check_equal('heat_wave_days', hgot, by['heat_wave_days']['values'])
    return {
        'calculations/forest_change.csv': rows_to_csv(['source_row', 'forest_cover_sq_km_isfr_2021', 'forest_cover_sq_km_isfr_2023', 'change_sq_km (2023 - 2021)', 'note'], rows),
        'calculations/heat_wave_days.csv': rows_to_csv(['state', 'days_2022', 'days_2023', 'days_2024', 'mean_2022_24 (sum / 3, 1 dp)', 'note'], hrows),
    }


def main():
    inds = load('data/interactive-data.json')['indicators']
    by = {i['id']: i for i in inds}
    files = indicator_files(inds)
    files.update(nfhs6_calcs(by))
    files.update(ncrb_calcs(by))
    files.update(ncrb_other_calcs(by))
    files.update(nas_calcs(by))
    files.update(court_calcs(by))
    files.update(climate_calcs(by))
    for mod in ('extra_calcs',):
        try:
            m = __import__(mod)
        except ImportError:
            continue
        files.update(m.calcs(by, load, rows_to_csv, fmt, check_equal))
    check = '--check' in sys.argv
    bad = []
    for rel, text in sorted(files.items()):
        path = os.path.join(OUT, rel)
        if check:
            if not os.path.exists(path) or open(path, encoding='utf-8').read() != text:
                bad.append(rel)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w', encoding='utf-8').write(text)
    if check:
        extra = []
        for dp, _dn, fn in os.walk(OUT):
            for f in fn:
                rel = os.path.relpath(os.path.join(dp, f), OUT)
                if rel not in files:
                    extra.append(rel)
        if bad or extra:
            print('STALE:', bad[:5], 'unexpected:', extra[:5])
            sys.exit(1)
        print('OK: %d CSV files current' % len(files))
    else:
        print('wrote %d CSV files to data/csv/' % len(files))


if __name__ == '__main__':
    main()
