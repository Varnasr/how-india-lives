# How the figures on the maps are calculated

Every number on a generated map is in `data/csv/`. This note says what each file holds and how each derived figure is got. Regenerate with `python3 scripts/export_csv.py`; CI runs it with `--check`.

## Files

- `data/csv/all-indicators.csv` has one row per state per indicator: value, unit, year, previous value and year where the source gives one, change, source, source address, retrieval date. The last row of each indicator is the India figure.
- `data/csv/indicators/<id>.csv` is the same, one indicator per file.
- `data/csv/calculations/<id>.csv` holds the inputs and the arithmetic for every indicator that is derived or assembled from several source rows.

The export recomputes each derived value from the source files in `data/` and stops if the result differs from the indicator on the map by more than 1e-9. A calculation file therefore cannot disagree with the map it documents.

## NFHS-6 indicators (`n6_*`)

Source: IIPS, NFHS-6 (2023-24) state and UT fact sheets, May 2026. Each row carries urban, rural and total for NFHS-6 and the NFHS-5 total printed in the same sheet.

- Mapped value is the NFHS-6 total as printed. Nothing is weighted or re-estimated here.
- Change is NFHS-6 total minus the NFHS-5 total printed beside it, in percentage points.
- A figure in parentheses (25 to 49 unweighted cases) is kept and flagged `small_sample`. An asterisk or NA is blank and the state stays grey. No value is interpolated.
- Thirteen sheets had no text layer and were read by OCR. Check any figure you intend to quote against the PDF.

## Crimes against women (`ncrb_*`)

Source: NCRB Crime in India, Volume 1, 2024 (2023 beside it), through the Women on Record dataset.

- `ncrb_total`, `ncrb_rape`, `ncrb_cruelty`: NCRB's printed rate, cases per lakh female population.
- `ncrb_dowry_death`: cases divided by female population in lakh, because the printed rate has one decimal and rounds small counts to zero.
- `ncrb_acid`: cases divided by female population in lakh, times 100, giving cases per crore women.
- Cities, districts of Delhi and rows in brackets are skipped. These are registrations. A higher figure can mean more crime, easier reporting, or both, so the maps do not say higher is better or worse.

## Courts

Source: Ministry of Law and Justice, Lok Sabha unstarred question 3501, with NJDG pendency of 9 March 2026.

- Pending per working judge is civil plus criminal cases pending in district and subordinate courts, divided by working judicial officers, rounded to a whole number.
- Vacancy is (sanctioned minus working) divided by sanctioned, times 100, one decimal.
- The judges table gives West Bengal and Andaman and Nicobar as one row. Their pendency is added and the same ratio shown for both. Dadra and Nagar Haveli and Daman and Diu are two judge rows, added.
- Meghalaya's row is self-contradictory in the source, so it is left off the pendency map and kept on the vacancy map. The printed national judges total (21,026) also differs from the sum of rows (21,014); both are recorded in the data file.

## Climate

Source: MoSPI ENVSTATS, from the India State of Forest Report and IMD.

- Forest change is forest cover in ISFR 2023 minus ISFR 2021, square kilometres.
- One source row labelled Puducherry is the India total and is excluded. The national change is the sum of the states and equals that row's own difference. Merged-UT rows that cannot be assigned with confidence are excluded.
- Heat-wave days is the mean of 2022, 2023 and 2024, one decimal, only for states with all three years.

## What the CSVs cannot show

The older static sheets (the 205 made outside this repository) have no per-state numbers here. Those are labelled with their vintage on each page and are not in these CSVs.
