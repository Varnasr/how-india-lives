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

## Honour killings, witchcraft murders and crimes against Scheduled Castes (`ncrb_honour`, `ncrb_witchcraft`, `ncrb_sc_crimes`)

Source: NCRB Crime in India 2024, Volume 1 (Tables 2A.1 and 2A.2) and Volume II (Table 7A.1), read by `scripts/extract_ncrb_other.py`. The script refuses a PDF whose SHA-256 differs from the one recorded, and stops unless every column's states and UTs add to NCRB's own printed totals.

- Honour killings and witchcraft are counts of murders by recorded motive (Table 2A.2). The map divides by the population NCRB prints beside the murder counts (Table 2A.1, lakh) and multiplies by 100, giving cases per crore. India has 36 and 54 such murders, so one case moves a small state a long way (Manipur's top rate is one case; so is Nagaland's for witchcraft). A zero means none recorded under that motive.
- Crimes against Scheduled Castes uses NCRB's printed 2024 rate per lakh SC population (2011 Census). It is recomputed from cases and the population NCRB prints to 0.1 lakh and must agree within that rounding. 2023 is 2023 cases over the same population. Ten states and territories with under 1 lakh SC people are left grey.
- These count registrations, not incidence, so the maps claim no direction.

## State output (`gsdp_pc`, `gsva_agri`, `gsva_mfg`, `gsva_services`)

Source: MoSPI National Accounts Statistics, state series, base year 2011-12, current prices, 2024-25 (2022-23 beside it), fetched by `scripts/fetch_mospi_nas.py`.

- GSDP per head is MoSPI's published figure in rupees, as served.
- A sector share is the sector's gross state value added divided by the state's total GSVA, times 100, one decimal. Each state's twelve industry rows must add to its published total within 0.01% or the build stops.
- Services are trade, repair, hotels and restaurants; transport, storage and communication; financial services; real estate, ownership of dwellings and professional services; public administration; other services. Mining, electricity and construction are not services.
- 2024-25 is an estimate that states revise. Nagaland and Ladakh have no 2024-25 figure. The series has no all-India row, so no national figure is shown.

## Private school share (`udise_private_share`) and written contracts (`plfs_no_contract`)

- Private share: UDISE+ enrolment (MoSPI API, indicator 28, both sexes, classes 1-12) in private unaided recognised schools divided by enrolment in all schools, times 100, one decimal. Government-aided schools are not counted as private. In every state and year the management categories must add to the all-management total or the build stops. Lakshadweep lists only government schools, whose enrolment equals the total, so its private share is 0. The national figure is the sum over all states and union territories.
- Written contracts: MoSPI's published PLFS annual figure (indicator 5), the share of regular wage and salaried employees with no written job contract, persons, rural and urban. It is used as published, with the All India row as the national figure. It covers regular employees only.

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

## What is not on the maps

Human trafficking, the old S02j sheet, has no 2024 state table here: it sits in Crime in India 2024 Volume III, which I could not reach from a primary source. PM2.5, rainfall and flood-prone districts have no state-level source in hand either. Their sheets keep their old vintage and say so.

## What the CSVs cannot show

The older static sheets (the 205 made outside this repository) have no per-state numbers here. Those are labelled with their vintage on each page and are not in these CSVs.
