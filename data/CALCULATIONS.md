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
- Human trafficking (`ncrb_trafficking`, Crime in India 2024 Volume III, Table 14.1): cases divided by the population NCRB prints with the table (lakh) times 10, giving cases per 10 lakh; 2023 uses the same population. The extractor requires IPC plus BNS to equal each state's total and the states and UTs to add to NCRB's printed totals (2,135 cases in India). States with under 10 cases are flagged as small samples.
- Communal or religious riots (`ncrb_riots`, Crime in India 2024 Volume 1, Table 1A.4, sub-head a of rioting): IPC plus BNS cases in 2024 divided by the printed population (lakh) times 100, cases per crore. One year only; the old map's 2019 to 2024 total cannot be rebuilt from this volume. The states and UTs add to NCRB's printed 349.
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

## Renewable capacity per person (`mnre_per_person`)

Installed renewable capacity is MoSPI's MNRE series `Total Power` (solar, wind, hydro including large hydro, bio) in MW for July 2026; the 36 states and UTs plus 'Others' add to the All India row within 1 MW. Population is the 2024 state figure (lakh) NCRB prints beside its murder table, taken from the National Commission on Population's 2020 projections. Watts per person = MW x 1,000,000 / (lakh x 100,000) = MW x 10 / lakh. The capacity year (2026) and the population year (2024) differ. The national figure is All India capacity over the total population.

## Women workers outside agriculture (`plfs_women_nonagri`)

MoSPI's PLFS calendar-year 2025 distribution of female workers by industry (usual status, rural and urban). The map plots 100 minus the share in agriculture, forestry and fishing, one decimal; the All India row is MoSPI's. PLFS was redesigned for 2025, so earlier rounds are not strictly comparable.

## HIV, health spending, beds, PM-JAY and Mudra (`naco_hiv`, `nha_*`, `ls_public_beds`, `pmjay_admissions`, `mudra_sc_st`)

- **Adult HIV prevalence:** NACO Sankalak (7th edition, 2025) Figure 2.7, estimates for 2024, as printed. It is a model-based estimate. Ladakh and Lakshadweep are not reported.
- **Health spending:** National Health Accounts 2022-23, Table A.6, 21 states. Government spending per person and the out-of-pocket share of total health spending are the table's own figures. Each row is checked: the shares equal the ratios of the crore figures (0.15 point) and each per-person figure equals spending over the printed population (4%). Out-of-pocket spending rests on the NSS 75th round (2017-18).
- **Public beds:** Lok Sabha question 1000 of 25 July 2025, beds at PHC, CHC, sub-district and district hospitals and medical colleges as on 31 March 2023, divided by 2024 projected population (NCRB Table 2A.1) per lakh. The five columns add to 8,18,661, the figure in the answer. The medical-college column adds to 16,998 beds more than its printed total, which is exactly Maharashtra's entry, so Maharashtra is left off. The table lists Uttarakhand as 26 and Uttar Pradesh as 27.
- **PM-JAY:** Lok Sabha question 2518 of 13 February 2026, admissions authorised in FY 2024-25 (lakh) divided by population (lakh) times 100,000. The table prints no total to check. Delhi and Odisha joined in April 2025 and West Bengal is not in the scheme.
- **Mudra:** Lok Sabha question 5803 of 30 March 2026, loans to SC and ST entrepreneurs April 2022 to March 2025, divided by SC plus ST population in lakh (Census 2011, NCRB Tables 7A.1 and 7C.1). The loan counts add to the printed 3,84,16,963. States with under 1 lakh SC and ST people are left off.

## Women MLAs and polluted rivers (`adr_women_mlas`, `cpcb_prs_critical`)

- **Women MLAs:** ADR and National Election Watch, as on 2 February 2026: women divided by seats analysed, times 100. Each assembly's men plus women equal its seats, and the 31 assemblies give the 4,123 MLAs and 390 women the report states. Five assemblies (Assam, Kerala, Puducherry, Tamil Nadu, West Bengal) are on 2021 results.
- **Polluted rivers:** CPCB's Table 1 (September 2025, monitoring 2022-23): the count of Priority I stretches (BOD above 30 mg/L). Each row's classes add to its total and each column to the printed totals (36, 21, 45, 45, 148, 295). The report's summary elsewhere says 279 stretches, against Table 1's 295.

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

PM2.5, rainfall and flood-prone districts have no state-level source in hand either. Their sheets keep their old vintage and say so.

## What the CSVs cannot show

The older static sheets (the 205 made outside this repository) have no per-state numbers here. Those are labelled with their vintage on each page and are not in these CSVs.

## Std V reading, ASER 2024 (`aser_std5_read`)

ASER Centre's Annual Status of Education Report (Rural) 2024, provisional, 28 January 2025: the share of Std V children in rural government schools who can read a Std II level text, 27 states, for 2018, 2022 and 2024. The mapped value is the 2024 figure; the file also gives its complement (children who cannot) and the change since 2022. The all-India rural government-school figure (44.8; 38.5 in 2022) must lie within the state range. ASER tests children at home in rural districts only and its state tables are government schools only. Samples are small in the smaller states.

## Children not in school, ASER 2024 (`aser_oos_6_14`)

Table 1 of each state page of ASER (Rural) 2024: the share of children aged 6 to 14 enrolled in government, private and other schools and not in school. Each row adds to 100 within rounding (0.3) and the all-India figure (1.9; 7.9 for ages 15 and 16, matching the report text) lies in the state range. Rural household survey; 27 states.

## Internet subscriptions per 100 people, TRAI March 2026 (`trai_internet_per100`)

TRAI's Yearly Performance Indicators 2025-26, Table 1.43: internet subscribers (millions) and subscribers per 100 population by state and UT. Rural plus urban equals total in every row (0.02 million) and the 36 rows sum to the printed 1,092.79 million (rural 440.87, urban 651.93); the total per 100 is 76.59. A subscription is not a person, so values above 100 are possible. Where the rural or urban per-100 cell is printed '-' (Delhi, Chandigarh, Lakshadweep) it is left empty. Replaces X168 and S01d.

## TB case notification rate (`tb_notification_rate`)

India TB Report 2024 (Central TB Division, data for 2023), Tables 1.1 (population in lakhs) and 1.2 (patients notified, public and private, and the rate per lakh). Public plus private equals the total in every row, the 36 rows sum exactly to the national 25,52,257, and notified divided by population reproduces each printed rate within 0.5. The rate counts cases notified where the patient was notified, not incidence; the report gives no state incidence. Lakshadweep (6 cases) is flagged as few cases. S03t (a modelled incidence map) links here as the newer map.

## Share of India's inward remittances (`rbi_remit_share`)

RBI Bulletin, 19 March 2025, Table 2 (sixth round of the Remittances Survey, 2023-24): each state's and UT's share of India's inward remittances, with the 2016-17 and 2020-21 rounds beside it. The 36 shares add to 100.0 and the five largest match the article's text (Maharashtra 20.5, Kerala 19.7, Tamil Nadu 10.4, Telangana 8.1, Karnataka 7.7). The calculation file multiplies each share by the US$ 118.7 billion total the article gives, for a rough dollar figure; it is arithmetic on rounded shares, not a published state amount. A dash in an earlier round means the state was not shown separately. S10h (an older dependence map) links here as its newer map; a share is not dependence or per-person receipts.

## Pupil-teacher ratio, primary (`udise_ptr_primary`)

UDISE+ indicator 23 (Pupil Teacher Ratio by level of education) from MoSPI's open data API, 2022-23 and 2024-25, all management types together and whole numbers as published (`scripts/fetch_mospi_ptr.py`). Each state has all four levels in both years (36 x 4 x 2 rows); the primary figure for 2024-25 is mapped and the calculation file lists the other levels. The API has no all-India row and no split by management for this indicator, so the old S07i (government primary schools) is not reproduced; the new map covers all schools. MoSPI does not say whether 2022-23 and 2024-25 are on the same basis, and Bihar's primary ratio goes from 43 to 26, so the change is shown with a warning.

## Rice share of cereal consumption, rural and urban (`hces_rice_r`, `hces_rice_u`)

MoSPI HCES, indicator 5 (average per-capita monthly quantity, kg), 2022-23 and 2023-24, without imputation (`scripts/fetch_mospi_hces_cereals.py`). Rice share = rice kg / total cereals kg x 100, to one decimal. In every row rice + wheat + coarse grains + other cereals equals the total within 1 per cent, where the API's '-' (a negligible or unreported component) counts as 0. The All India row gives the national marker (rural 54.2 = 5.065 / 9.352). A quantity share, not calories or spending, and rural and urban are separate series. S01j links to the rural map as its newer version; the urban map sits beside it.

## Maternal mortality ratio and life expectancy, SRS (`srs_mmr`, `srs_life_exp`)

Both come from Office of the Registrar General publications on censusindia.gov.in, a host that serves an incomplete certificate chain, so the PDFs could not be downloaded here: the figures were read from a text extraction on 2026-10-19 and no SHA-256 is pinned. They are held to internal checks instead.

- **MMR 2022-24** (Special Bulletin on Maternal Mortality, Table 1): maternal deaths per 100,000 live births, three years pooled. Each state's value lies inside its printed 95% confidence interval; the India figure is 87 (78 to 95), 88 for 2021-23. Only 19 states are shown separately and the rest are pooled by SRS as 'Other states' (84), which is not mapped. The intervals are wide (Kerala 0 to 50).
- **Life expectancy at birth 2019-23** (Abridged Life Tables, Statement 3, as corrected by Corrigendum 15/09/2020-VS(SRS), which changes West Bengal's urban female figure to 76.3): the total lies between the male and female figures and between the rural and urban totals in every row, and agrees with the report's Chart 4 and its text. Statement 4 of the same report prints different 2019-23 totals for some states (Andhra Pradesh 70.3, Bihar 69.0, Gujarat 70.1, Haryana 68.6, Himachal Pradesh 73.6, Kerala 74.8) while its male and female columns match Statement 3; Statement 3 is used because every other table agrees with it. Jammu and Kashmir includes Ladakh. S03f and S03s link to these as their newer maps.

## RBI Handbook tables: irrigation, bank offices, groundwater (`rbi_irrigated_share`, `rbi_bank_offices`, `cgwb_stage`)

All three come from the RBI Handbook of Statistics on Indian States 2024-25 (released 11 December 2025). rbidocs.rbi.org.in sits behind a bot challenge, so the PDFs were read through Firecrawl on 2026-10-19 and the figures are transcribed into the extractor scripts, with no SHA-256 pinned. Each is held to the table's own printed totals.

- **Net irrigated share** (Tables 54 and 56, thousand hectares, from the Ministry of Agriculture's land use statistics): net irrigated area over net sown area for 2023-24 (provisional), with 2022-23 beside it. Net irrigated never exceeds net sown. The provisional year breaks the series in places (Maharashtra's irrigated area doubles, and the net sown area falls in Andhra Pradesh, Manipur and Jharkhand), which the map text says. S08b links here.
- **Bank offices per lakh** (Table 152, offices at end-March): the 36 rows add exactly to the printed all-India totals (1,63,216 in 2024 and 1,67,806 in 2025) and each of the six regional subtotals agrees. Offices at March 2025 are divided by the 2024 population NCRB prints, a year apart, and the same population divides the 2024 offices for the previous value. Offices are where the branch stands. S02n links here.
- **Stage of groundwater extraction** (Table 107, billion cubic metres, from the Central Ground Water Board's assessments): the printed stage equals extraction over extractable resource within rounding for every state with a resource of 1 BCM or more, and the all-India 2024 figures give 60.5. Daman and Diu is clubbed with Dadra and Nagar Haveli in 2024, so that territory has no 2023 comparison. S08j (over-exploited blocks) links here as a different measure.

## Rice and sugarcane share of crop area (`rbi_thirsty_share`)

RBI Handbook of Statistics on Indian States 2024-25, Tables 67 (rice), 69 (coarse cereals) and 78 (sugarcane), area in thousand hectares for 2023-24 and 2024-25, read through Firecrawl on 2026-10-20 with no SHA-256 pinned (`scripts/extract_rbi_crop_area.py`). Share = (rice + sugarcane) / (rice + sugarcane + coarse cereals) x 100. For each table and year the state rows sum to the printed ALL INDIA row within 0.5 per cent, and the national marker uses those totals (68.8 in 2024-25). Goa's coarse cereals are a dash in every year, so Goa is left out. Delhi and Sikkim are absent from the sugarcane table, and Jharkhand's 2023-24 dash, and all count as 0. Coarse cereals include maize and barley as well as millets, and the three groups leave out wheat, pulses, oilseeds, cotton, fruit, vegetables and plantation crops, which is why Kerala reads 99.8. The calculation file also gives the ratio form (hectares of rice and sugarcane per hectare of coarse cereals), which runs from 0.06 in Rajasthan to 589 in Kerala and is not mapped. S08f (the old 10x claim) links here as its newer map.

## Sex ratio at birth (`srs_sex_ratio_birth`)

ORGI, Sample Registration System Statistical Report 2023, Table 16 (page 315) and Statement 16 (page 66): females per 1,000 males at birth, three-year averages from 2017-19 to 2021-23, for India and 22 larger states. The PDF is pinned by SHA-256 in `scripts/extract_srs_sex_ratio_birth.py`. Table 16's 2021-23 columns equal Statement 16 row for row, the India figure is 917, and the highest and lowest states match the report's text. The map shows the 2021-23 total with 2020-22 beside it; the calculation file gives all five periods, rural and urban, and the change since 2017-19. Jammu and Kashmir includes Ladakh. A low figure can reflect sex-selective practice or unreported girls' births, and the data cannot separate them. X184, the older map labelled as a proxy for sex-selective abortion, links here as its newer map.

## Startups per lakh people (`dpiit_startups`)

DPIIT, Lok Sabha Unstarred Question 1446 of 28 July 2026, Annexure I: entities recognised as startups as on 30 June 2026, by state and UT (`scripts/extract_dpiit_startups.py`). The 36 rows add to the 2,40,092 the answer gives for India, and Odisha and Karnataka match the figures in its text. Startups per lakh = startups / population (NCRB's 2024 projection in lakh). A startup is counted at its registered address, which concentrates in Delhi, Karnataka and Maharashtra, and recognition does not say the business still trades. S10i links here as its newer map.

## Mean age at effective marriage of females (`srs_marriage_age`)

ORGI, SRS Statistical Report 2023, Statement 13 (page 53): the mean age at which a marriage took effect among females whose marriages were recorded in 2023, for India and 22 larger states, with the means for marriages below 18, at 18 to 20 and at 21 and over, in rural and urban areas (`scripts/extract_srs_marriage_age.py`; the PDF is pinned by SHA-256). India is 22.9, each total lies between its rural and urban values, and the mapped figure is the all-ages total. It is an average over recorded marriages, not the share of women married below 18. S01f links here as its newer map.

## Over-exploited groundwater units (`cgwb_oe_share`)

CGWB and Ministry of Jal Shakti, National Compilation on Dynamic Ground Water Resources of India, 2025, table "Categorization of blocks/mandals/talukas in India (2025)" (page 187). Over-exploited units / units assessed x 100. Each state's categories add to its total and the 36 rows add to the printed Grand Total (6,762 units, 730 over-exploited). Units are blocks, taluks, mandals or districts by state, so they differ in size. The 2024 national figure (751 of 6,746) is from the same compilation's trend table. S08j links here; the stage-of-extraction map (X285) is a different measure.

## Annual rainfall, 2024 (`rain_2024`)

State-wise rainfall tables in the same CGWB compilation (pages 39 and 40), from IMD data: normal rainfall and rainfall in calendar year 2024, in millimetres, for 36 states and UTs (`scripts/extract_cgwb_rainfall.py`). The report's own text agrees on the extremes (Ladakh 50.9 mm normal and 79.3 mm in 2024, Meghalaya 3,751.5 mm normal, Goa 4,906.6 mm in 2024) and on 18 states and UTs being below normal. The calculation file adds each state's departure from normal. S08a links here as its newer map.

## Udyam MSME registrations per lakh people (`udyam_per_lakh`)

Ministry of MSME, Lok Sabha Unstarred Question 755 of 4 December 2025, Annexure I: registrations on the Udyam Registration Portal and the Udyam Assist Platform (informal micro enterprises) by state and financial year, 1 July 2020 to 30 November 2025 (`scripts/extract_udyam_msme.py`; the PDF is pinned). In each year the state rows add to the printed Total and the six years give 7,22,32,207 registrations. Registrations per lakh = total registrations / population (NCRB 2024 projection). It counts registrations at the registered address, includes informal enterprises added since January 2023, and moves with registration drives, so it is not comparable with the earlier Udyam map. S10a links here as its newer map.

## MGNREGA women's share and households completing 100 days (`mgnrega_women_pct`, `mgnrega_100_days_pct`)

Ministry of Rural Development, State Performance Report 2024-25, Annexures I to III (`scripts/extract_mgnrega_spr.py`; the PDF is pinned). The shares are printed in whole per cent and are mapped as printed. The persondays by state add to the printed total, 29,06,505,713, and the persondays-weighted mean of the state women's shares is 58.08 per cent against the 58.1 the report gives for India, which checks the Annexure II column against Annexure III. The 100-day share is of households that worked: 40,66,631 of 5.78 crore, or 7.0 per cent, the 7 printed for India. West Bengal (no Labour Budget approved) and Lakshadweep show 0 persondays and are left out of both maps, since a printed 0% there means no work and not no women. S11b and S02e link here as their newer maps; S02e showed average days per household, which this report gives only for India (50.21), so the new map shows the 100-day share instead.

## Women self-help groups per lakh people (`nrlm_shg_per_lakh`)

Ministry of Rural Development, Lok Sabha Unstarred Question 3687 of 11 August 2026, Annexure I (`scripts/extract_nrlm_shg.py`; the PDF is pinned): women SHGs set up under DAY-NRLM by state. The 34 rows add to the printed 92,30,743. Groups per lakh = groups / population (NCRB 2024 projection). It counts groups, not members, is cumulative, and divides by the whole population though the Mission works in rural areas. X179 linked here shows membership, which this table does not give.

## Rural power supply hours (`power_hours_rural`)

Ministry of Power, Rajya Sabha Unstarred Question 3185 of 28 March 2023, Annexure I (`scripts/extract_power_hours.py`; the PDF is pinned): average hours of supply a day on 11 kV feeders as reported by utilities, 2018-19 to 2022-23 (to December 2022). The table leaves cells blank where a state reported nothing, so each number is placed in its column by the position of its right edge from the printed All India row, and five printed values are asserted. 2021-22 is mapped because it is the last full year and 20 states report a rural figure; the unweighted mean of those 20 is 20.49 against the printed all-India 20.53. S02m links here as its newer map.

## Rural tap water supply (`jjm_tap_pct`)

Ministry of Jal Shakti, Lok Sabha Starred Question 62 of 23 July 2026, annexure (Jal Jeevan Mission IMIS, as on 18 July 2026) (`scripts/extract_jjm_tap.py`; the PDF is pinned). The 34 rows add to the printed totals of 19,35.54 lakh rural households and 15,88.96 lakh with tap supply, and each printed per cent lies within the range its lakh figures give once rounding to 0.01 lakh is allowed for. The printed per cent is mapped. It counts connections the states report, not supply that runs or water that is safe. Delhi and Chandigarh have no rural population. S02l links here as its newer map.

## Solid waste generated per person (`cpcb_waste_pc`)

Ministry of Environment, Forest and Climate Change, Lok Sabha Unstarred Question 50 of 1 December 2025, annexure (State Pollution Control Board reports to CPCB for 2023-24) (`scripts/extract_cpcb_msw.py`; the PDF is pinned). The 36 rows add to the printed totals of 1,85,195 tonnes a day generated, 1,79,479 collected and 1,14,110 treated. Grams per person per day = tonnes a day x 1,000,000 / population (NCRB 2024 projection, 36 states and territories). The boards use different methods and some report urban waste only, so the spread reflects reporting as well as waste. S08h links here as its newer map.
