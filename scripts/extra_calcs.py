"""Calculation CSVs for the indicators built from PDFs (called by scripts/export_csv.py).

Each function returns {relative path: csv text} and recomputes the mapped value from the committed raw file,
stopping if it differs from the indicator. Add a function here for each new PDF-based indicator.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def calcs(by, load, rows_to_csv, fmt, check_equal):
    files = {}
    # NACO HIV
    raw = load('data/naco/hiv-2024.json')
    check_equal('naco_hiv', raw['values'], by['naco_hiv']['values'])
    files['calculations/naco_hiv.csv'] = rows_to_csv(['state', 'adult_hiv_prevalence_pct_2024 (as printed in Sankalak Figure 2.7)'], [[s, v] for s, v in sorted(raw['values'].items())] + [['India', raw['national']]])
    # NHA 2022-23
    nha = load('data/nha/states-2022-23.json')['states']
    check_equal('nha_ghe_pc', {s: round(v['ghe_pc']) for s, v in nha.items()}, by['nha_ghe_pc']['values'])
    check_equal('nha_oope_share', {s: v['oope_pct_the'] for s, v in nha.items()}, by['nha_oope_share']['values'])
    rows = [[s, v['the_cr'], v['ghe_cr'], v['ghe_pc'], v['oope_cr'], v['oope_pct_the'], v['population_crore']] for s, v in sorted(nha.items())]
    files['calculations/nha_state_health_spending.csv'] = rows_to_csv(
        ['state', 'total_health_expenditure_rs_crore', 'government_health_expenditure_rs_crore', 'government_per_capita_rs (mapped, as printed)',
         'out_of_pocket_rs_crore', 'out_of_pocket_pct_of_total (mapped, as printed)', 'population_crore (as printed)'], rows)
    # Lok Sabha beds, PM-JAY, Mudra
    pop = load('data/ncrb/crime-in-india-2024-other.json')['states']
    beds = load('data/health/public-beds-2023.json')
    rows = []
    for s, r in sorted(beds['states'].items()):
        tot = sum(v or 0 for v in r.values())
        lakh = pop[s]['population_lakh']
        rows.append([s] + ['' if v is None else v for v in r.values()] + [tot, lakh, '' if s in beds['unreliable'] else round(tot / lakh), beds['unreliable'].get(s, '')])
    files['calculations/ls_public_beds.csv'] = rows_to_csv(
        ['state'] + beds['columns'] + ['total_beds (blank = not applicable)', 'population_lakh_2024', 'beds_per_lakh (total / population_lakh, rounded)', 'note'], rows)
    pm = load('data/loksabha/pmjay-admissions.json')
    rows = []
    for s, r in sorted(pm['states'].items()):
        lakh = pop[s]['population_lakh']
        out = s in pm['not_in_scheme_until_april_2025']
        rows.append([s] + r + [lakh, '' if out else round(r[2] / lakh * 1e5), '' if out else round(r[0] / lakh * 1e5), 'joined April 2025, no figure for 2024-25' if out else ''])
    files['calculations/pmjay_admissions.csv'] = rows_to_csv(
        ['state', 'admissions_lakh_2022_23', 'admissions_lakh_2023_24', 'admissions_lakh_2024_25', 'admissions_lakh_2025_26_to_31_jan', 'population_lakh_2024',
         'admissions_per_lakh_people_2024_25 (admissions_lakh / population_lakh x 100,000)', 'admissions_per_lakh_people_2022_23', 'note'], rows)
    mu = load('data/loksabha/mudra-sc-st.json')
    rows = []
    for s, (loans, amt) in sorted(mu['states'].items()):
        sc, st = pop[s]['sc_population_lakh_2011'], pop[s]['st_population_lakh_2011']
        base = sc + st
        rows.append([s, loans, amt, sc, st, round(base, 1), '' if base < 1.0 else round(loans / base), 'excluded: under 1 lakh SC and ST people' if base < 1.0 else ''])
    files['calculations/mudra_sc_st.csv'] = rows_to_csv(
        ['state', 'loans_apr_2022_mar_2025', 'amount_rs_crore', 'sc_population_lakh_2011 (NCRB 7A.1)', 'st_population_lakh_2011 (NCRB 7C.1)', 'sc_plus_st_lakh',
         'loans_per_lakh_sc_and_st (loans / sc_plus_st_lakh, rounded)', 'note'], rows)
    check_equal('ls_public_beds', {s: round(sum(v or 0 for v in r.values()) / pop[s]['population_lakh']) for s, r in beds['states'].items() if s not in beds['unreliable']}, by['ls_public_beds']['values'])
    check_equal('pmjay_admissions', {s: round(r[2] / pop[s]['population_lakh'] * 1e5) for s, r in pm['states'].items() if s not in pm['not_in_scheme_until_april_2025']}, by['pmjay_admissions']['values'])
    check_equal('mudra_sc_st', {s: round(l / (pop[s]['sc_population_lakh_2011'] + pop[s]['st_population_lakh_2011'])) for s, (l, a) in mu['states'].items() if pop[s]['sc_population_lakh_2011'] + pop[s]['st_population_lakh_2011'] >= 1.0}, by['mudra_sc_st']['values'])
    # ADR women MLAs
    adr = load('data/adr/women-mlas-2026.json')['states']
    check_equal('adr_women_mlas', {s: round(r['women'] / r['seats_analysed'] * 100, 1) for s, r in adr.items()}, by['adr_women_mlas']['values'])
    files['calculations/adr_women_mlas.csv'] = rows_to_csv(
        ['state', 'last_election_year', 'seats_analysed', 'women_mlas', 'women_share_pct (women / seats x 100, 1 dp)'],
        [[s, r['election_year'], r['seats_analysed'], r['women'], round(r['women'] / r['seats_analysed'] * 100, 1)] for s, r in sorted(adr.items())])
    # CPCB rivers
    cp = load('data/cpcb/polluted-rivers-2025.json')['states']
    check_equal('cpcb_prs_critical', {s: r['priority_I'] for s, r in cp.items()}, by['cpcb_prs_critical']['values'])
    files['calculations/cpcb_polluted_rivers.csv'] = rows_to_csv(
        ['state', 'priority_I_bod_above_30 (mapped)', 'priority_II_20_to_30', 'priority_III_10_to_20', 'priority_IV_6_to_10', 'priority_V_3_to_6', 'total'],
        [[s, r['priority_I'], r['priority_II'], r['priority_III'], r['priority_IV'], r['priority_V'], r['total']] for s, r in sorted(cp.items())])
    return files
