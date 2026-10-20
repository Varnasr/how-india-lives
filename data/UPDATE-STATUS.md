# Which maps can be updated, and which cannot

Status as of 19 October 2026 for the older static maps. Three research agents searched official sources for each map, tested whether the files can be reached from this sandbox, and reported a verdict. **Only the first group was checked by me.** Everything else is a lead: the release, year and caveat are the agent's reading, and a few figures were read from PDFs by a model and need checking against the PDF before use.

## Counts

| Status | Maps |
|---|---|
| built in this work | 3 |
| updatable now | 24 |
| updatable if user supplies file | 30 |
| no newer state data | 25 |
| unclear | 21 |
| not a state series | 3 |
| Census 2011, labelled with a data note (no later count exists) | 36 |
| NFHS-5, labelled with a data note (NFHS-6 does not repeat the measure) | 27 |

## Built in this work

Rebuilt from a source I read myself. The new sheet is named.

| Map | Title | Newest release found | Caveat |
|---|---|---|---|
| S02j | Human Trafficking Cases per 10 lakh populatio | X262 (see data/CALCULATIONS.md) | Verified in the Volume I PDF text that Tables 14.1-8 are in Volume III, which neither the mirror nor ncrb.gov.in's year page gave me; the repo's CLAUDE.md says the same. Counts are registrations, not prevalence. |
| S08l | Renewable Energy Capacity per Capita | X260 (see data/CALCULATIONS.md) | Needs a state population projection for the denominator. Latest API month was July 2026; Sept 2026 figures exist only in secondary reports. |
| S10g | Women in Non-Agricultural Employment | X261 (see data/CALCULATIONS.md) | Compute as 100 minus the agriculture share (industry_section A); shares shift sharply between years because PLFS 2025 changed its sample design, so note the break. |

## Updatable now

A research agent found a newer state-level release it could read. I have not yet checked these myself, so treat the release, year and caveat as leads.

| Map | Title | Newest release found | Caveat |
|---|---|---|---|
| S01d | Mobile Internet Penetration | TRAI Performance Indicators Report Apr-Jun 2026, released 12 Oct 2026, Table 1.42 | TRAI reports by Licensed Service Area, not state: UP East/West, Mumbai, Delhi, Kolkata and Maharashtra-ex-Mumbai must be merged or approximated. Source label 'DFPD' on the map looks wrong. |
| S01j | Rice as Primary Cereal % of total cere | MoSPI HCES 2023-24 (and 2022-23), indicator 5, by state and rural/urban | Rural and urban are separate series: combine with population or household weights for a state figure. The repo already uses the same API for HCES MPCE. |
| S03f | Maternal Mortality Ratio | SRS Special Bulletin on Maternal Mortality in India 2022-24 (ORGI, listed 20 May 2026): India 87; also 2021-23 bulletin (3 Sep 2025, India 8 | Only 20 states are shown separately and all others are pooled as 'Other states' (84), so the map has grey for the rest; confidence intervals are wide (e.g. Kerala 24, CI 0 to 50). Extraction was model-assisted (one CI looked garbled), so check values against t |
| S03h | Government Health Expenditure per Capita | National Health Accounts Estimates for India 2022-23 (MoHFW/NHSRC, released May 2026), Annexure Tables A.6 and A.7 | Table A.7 covers all states/UTs with legislature for government spending; the existing takeaway (Bihar under Rs 500) does not match NHA 2022-23, which lists Bihar at Rs 1,056 per capita, so the old map's source is doubtful. Spending is on an RBI state-finance  |
| S03p | Hospital Beds per Lakh Population | LS USQ 1000, 25.07.2025: Annexure-I beds at PHC, CHC, sub-district, district hospitals and medical colleges by state, as on 31.03.2023 (Heal | Only three months newer than the NHP basis and it covers public facilities only (8,18,661 beds), so it gains little; private beds are not in any state series found. |
| S03q | PM-JAY Ayushman Bharat Hospital Admissions pe | LS USQ 2518, 13.02.2026: Annexure-II state/UT-wise admissions (lakh) for FY 2022-23, 2023-24, 2024-25 and FY 2025-26 to 31.01.2026 | Use full-year FY 2024-25; FY 2025-26 is part-year and Delhi joined only in 2025-26 (0.24 lakh). Per-lakh needs a population denominator (projected 2024 or Census 2011). |
| S03r | Out-of-Pocket Health Expenditure | NHA 2022-23, Table A.6 (21 select states: THE, GHE and OOPE per capita and as % of THE) | Only 21 'select states' are given; north-east states except Assam, Goa and all UTs are missing, so the map will be sparser. NHA 2022-23 shows UP at 66.1% and Bihar at 47.7%, which contradicts the existing 'over 70% in UP and Bihar' takeaway. |
| S03s | Life Expectancy at Birth | SRS Abridged Life Tables 2019-2023 (ORGI, 1 Jun 2026), Statement 3: India 70.3 and 22 states/UTs; corrigendum published | Apply Corrigendum_SRS_ABL_2019-23.pdf (catalog/46175/download/51399) before using values; my extraction was model-assisted. Only 22 states/UTs; Kerala is 75.1 and Chhattisgarh 64.6, not 77 and 64 as the old takeaway says. |
| S03t | TB Incidence per Lakh Population | India TB Report 2024 (data 2023) is the newest report on tbcindia.mohfw.gov.in; MoSPI GENDER indicator 159 holds state-wise TB cases notifie | Official state tables are notification rates (cases notified), not incidence, and a newer India TB Report (2025) was not found. 2024 counts need a population denominator to become a per-lakh rate; Ni-kshay (reports.nikshay.in) may offer 2025. |
| S03u | HIV Prevalence Among Adults 15-49 | NACO Sankalak (7th ed., 2025) Figure 2.7: state-wise adult prevalence 2024 (India 0.20%); India HIV Estimates 2023 state table (Mizoram 2.73 | J&K and Ladakh are reported together and 2024 values differ slightly from 2023 (e.g. Mizoram 2.75 vs 2.73), so keep the year consistent. Values are estimates with wide uncertainty bounds in small states. |
| S04m | Women MLAs as % of Total MLAs | ADR/NEW 'Women's Political Participation and Representation in India 2026' (sitting MLAs as on 2 Feb 2026): 32 assemblies with counts and %, | Assam, Kerala, Tamil Nadu, West Bengal and Puducherry still show their 2021 assemblies, though they voted in 2026 (secondary reports: TN 9.8%, WB 12.6%); update those five from ECI results. MoSPI GENDER indicator 126 is older (UP shows 2022). |
| S06e | Communal Riots by State 2019-2024 | NCRB Crime in India 2024 Vol II (released Apr-May 2026), Chapter 1A state-wise head 'Communal/Religious' (37.1); earlier years in CII 2019-2 | The map's '2019-2024' label predates CII 2024 (published 2026), so its provenance is doubtful; CII records cases registered, not riot incidents or casualties, and 2019-2021 need the older editions. CSSS counts (59 riots in 2024) are press-based, not official. |
| S07a | ASER Class 5 Children Who Cannot Read Class 2 | ASER 2024 (Pratham, Jan 2025): state table of government-school Std V children reading Std II text for 2018, 2022, 2024 | Table is government-school children in rural India only; confirm the old map used the same base (all schools would differ). Published ASER summaries disagree on a few top-state values (Mizoram 65.9 vs 64.9), so check the final PDF. |
| S07h | Out-of-School Children 6-14 Years | ASER 2024 state tables (% not enrolled by age group); UDISE+ publishes enrolment, not out-of-school counts | ASER is a rural household survey; confirm the exact age band and base against the old map. Page location of the 6-14 table was not pinned down. |
| S07i | Pupil-Teacher Ratio in Government Primary Sch | UDISE+ 2024-25 via MoSPI API: PTR all management (indicator 7) and by level (indicator 23); 2024-25 newest | The API returns all-management PTR; government-only PTR (indicator 23 with management filter returned nothing) would need the UDISE+ 2024-25 report. Repo already holds UDISE 2024-25 dropout data. |
| S08e | Critically Polluted River Stretches | CPCB 'Polluted River Stretches for Restoration of Water Quality', Sept 2025, based on 2022-23 monitoring; 295/296 stretches, Maharashtra 54 | The copy is on a Puducherry government site, not cpcb.nic.in; headline counts differ slightly between reports (295 vs 296). Decide which priority classes count as 'critical'. |
| S09e | Internet Shutdowns Cumulative 2012-2024 | SFLC.in tracker, 913 events through 2026 (state and year filters) | Scrape and count by state; 'Jammu & Kashmir' and 'Jammu and Kashmir' appear as separate labels. These are recorded events, not days or population-weighted. |
| S10h | Remittance-Dependent States | RBI sixth Remittances Survey 2023-24 (RBI Bulletin, 19 Mar 2025), Table 2: all states/UTs, 2016-17, 2020-21 and 2023-24 (Maharashtra 20.5, K | These are shares of the national total, not remittances relative to a state's economy; 2023-24 shares include all states that were 'Others' earlier, and Telangana is shown separately. |
| S12k | HIV Prevalence Among Adults 15-49 | Same as S03u: NACO Sankalak (7th ed., 2025), state-wise adult prevalence 2024 | Duplicate of S03u (same title, source and year), so one extraction serves both; consider merging the two maps. |
| X168 | Smartphone + Internet Access Digital Access P | TRAI Yearly Performance Indicators 2025-26, released 5 Oct 2026, Table 1.43 (state/UT internet subscribers per 100 population, 31 Mar 2026); | Table 1.43 lists 28 states and 8 UTs with rural/urban/total per 100; values exceed 100 in places (Goa 150, Delhi 173) because it counts subscriptions (SIMs), not people, so it is not smartphone ownership. If the map means households with internet, use NSS80 in |
| X172 | Average Monthly Per Capita Consumption Expend | HCES 2023-24 (MoSPI factsheet Dec 2024; state-level rural and urban via API; the API lists only 2022-23 and 2023-24) | The repo already carries HCES 2023-24 as X206/X207 (rural/urban MPCE), so this is a duplicate of existing data; the API has no combined rural+urban series, so a single-number map is not possible. |
| X178 | Mudra Loans to SC ST per Lakh SC ST Populatio | Lok Sabha USQ 5803, 30.03.2026 (Ministry of Finance): State/UT-wise number of loans and disbursed amount to SC & ST entrepreneurs, 1 Apr 202 | SC and ST are combined and the window is a three-year cumulative, so it will not match the existing map's basis; denominator needs Census 2011 SC+ST population. Related: LS USQ 2415 and 2407 (3 Aug 2026) give state-wise totals but not SC/ST splits (not checked |
| X184 | Sex-Selective Abortion Proxy Unnatural Sex Ra | SRS Statistical Report 2024 (ORGI, released 2026): SRB table for India and 22 bigger states/UTs (India 918); SRS 2023 report also exists (91 | The 22-state values were read by a language-model query over the PDF and the reference period was not labelled in the output (Delhi rural/urban also looks inconsistent), so verify every figure against the table before use. Small states and UTs are not covered. |
| X189 | Households Using Improved Drinking Water Sour | NFHS-6 (2023-24) fact sheets, May 2026, indicator 5, already in data/nfhs6/states.json; JJM dashboard reports tap connections, a different m | Use the NFHS-6 indicator already in the repo: JJM measures functional household tap connections in rural homes, not improved sources, so the map title and source would need changing. Manipur has no NFHS-6 sheet. |

## Updatable if user supplies file

A newer release exists but the file could not be fetched from this sandbox (blocked site, scanned answer, browser-only download). It needs the file from you.

| Map | Title | Newest release found | Caveat |
|---|---|---|---|
| S01f | Average Age of Women at First Marriage | SRS Statistical Report 2022 (RGI); NFHS-6 (May 2026) gives % women 20-24 married before 18 instead | Secondary summary cites 2022 SRS national 22.7 years but I did not retrieve the state table. NFHS-6 child marriage is a different measure and is already in the repo (n6_child_marriage). |
| S02d | Income Tax Filers as % of Population | Income Tax Return Statistics AY 2023-24 (CBDT, June 2024; AY 2024-25 and 2025-26 also filed); Dataful (secondary) holds a state, month, year | Returns are counted by filing state, and many returns are zero-tax, so 'filers' is not taxpayers; state tables in the official PDF were not confirmed. |
| S02e | MGNREGA Average Days of Work per Household | MGNREGA MIS for FY2025-26 (complete year); MGNREGA was repealed and replaced by VB-G RAM G from 1 Jul 2026 | The MIS excludes Kerala and Maharashtra (technical upgrade note on the page), so two states would be blank; nreganarep.nic.in resets connections. |
| S02f | Night-time Light Radiance Economic Activity P | Annual VIIRS Nighttime Lights composites from Colorado School of Mines EOG (versions to at least 2024); ISRO NRSC NTL Atlas for context | This is a computed raster aggregate, not a published state series; results depend on version, masking and boundary file, so the map would not match the old one exactly. |
| S02l | Households with Piped Water Tap Connection | JJM live dashboard: 81.57% of rural households nationally on 29 Jan 2026 (Ministry statement via humanprogress.org, secondary); state-wise d | Data is live and shifts daily, so pin a date; the page's disclaimer says household totals were revised for UP and AP, which affects percentages. |
| S02m | Average Daily Electricity Supply Rural Hours | Ministry of Power data in Lok Sabha/Rajya Sabha replies: FY2023-24 (RS 3 Feb 2025) and FY2024-25/2025-26 (press: national rural average 22:3 | The 2025-26 state numbers appear only in a press report that I could not tie to a document; state annexures were not readable from the sandbox. |
| S02n | Bank Branches per Lakh Population | RBI Handbook of Statistics on Indian States 2024-25 (10th edition, released 11 Dec 2025; banking section) and RBI BSR-2 March 2025 branch-ba | The Handbook dropped Census 2011 tables, so population denominators come from the NCP projection; branch counts by state need the right table downloaded in a normal browser. |
| S02o | Post Offices per Lakh Population | India Post circle-wise counts: rural post offices as on 31 Mar 2023 (Lok Sabha Dec 2023) and a 12 Mar 2025 Lok Sabha question (USQ 2156); In | India Post reports by postal circle, and circles do not match states (for example Maharashtra includes Goa), so a state map needs an allocation rule. |
| S03g | Annual Mean PM2.5 Concentration | No official state-wise annual PM2.5 table found. CPCB station data exist to 2024 (NAMP/CAAQMS portal); third-party Princeton dashboard holds | State means must be derived by aggregating station or city data, and a mean of monitored cities is not a state mean; the existing 2023 figures have no traceable published table. cpcb.nic.in also showed relay failures in some requests. |
| S04p | Female Domestic Workers as % of All Workers | PLFS Annual Report 2025 (MoSPI, 29 May 2026) exists; no published state-wise table of domestic workers by sex was found | Domestic work is a 2- or 3-digit industry code that needs unit-level PLFS microdata and survey weights, and state-level sample sizes may be thin; I did not confirm that the report prints it. |
| S07j | Mid-Day Meal Coverage vs Enrolment | PM POSHAN dashboard/Lok Sabha replies; PAB minutes give 2023-24 to 2024-25 changes only | UDISE+ API has no mid-day-meal coverage item. State-wise children covered for 2024-25 was not found as a single table, and coverage vs enrolment depends on matching two sources. |
| S08a | Annual Rainfall | IMD Annual Report 2025 / IMD rainfall statistics 2025; IMD reports by 36 meteorological subdivisions | IMD publishes subdivision, not state, rainfall; a subdivision-to-state mapping is needed and I did not find a ready state table. ENVSTATS rainfall is all-India only. |
| S08b | Net Irrigated Area as % of Net Sown Area | RBI Handbook of Statistics on Indian States 2024-25, Tables 54 and 56 (2023-24 provisional) | Search results quote 2023-24 values (Gujarat 6,273/9,824 thousand ha = 64%), but the file itself did not download from this sandbox. Values are provisional. |
| S08f | Water-Intensive Crops vs Millet Area Ratio | DoAFW state crop area 2023-24 or 2024-25 advance estimates; not retrieved | No ready state-wise machine-readable crop-area file located from here; the RBI Handbook crop-area tables are a possible route. |
| S08h | Municipal Solid Waste Per Capita | CPCB Annual Report on SWM Rules 2022-23 exists (national 170,939 TPD per a Scribd copy); state table not retrieved. ENVSTATS has 2021-22 | If the map's 2022 means the 2021-22 report, a 2022-23 report may be newer, but I could not open it. Per-capita also needs urban population. |
| S08j | Groundwater Over-Exploited Blocks | CGWB Dynamic Ground Water Resources 2025 (released Dec 2025: 730 of 6,762 units over-exploited nationally); ENVSTATS has state stage of extr | Only the national headline of the 2025 assessment was found; state counts of over-exploited blocks need the CGWB report or its annexure. Stage of extraction (%) is available now for 2024 but is a different measure. |
| S08k | PM Fasal Bima Crop Insurance Coverage | Rajya Sabha reply Aug 2024 has state-wise 2019-20 to 2023-24; PIB Aug 2026 doc gives national 2024-25 only | No 2024-25 state-wise table located; pmfby.gov.in unreachable. Coverage as a share of farmers also needs a denominator. |
| S09d | Police per Lakh Population | BPR&D Data on Police Organisations as on 1 Jan 2024 (Dataful lists All-India 197.44 per lakh); 2025 edition not confirmed | Could not reach BPR&D or Dataful from here. Secondary 2025 tables show implausible values (Nagaland 1,136), so use only the BPR&D PDF. |
| S09i | Old Age Pension Coverage % of Eligible | NSAP FY 2024-25 beneficiary abstract (data.gov.in); Lok Sabha Q.1159 of 11 Feb 2025 with state annexure | Beneficiaries are available, but 'eligible' needs a denominator (BPL list or 60+ BPL population) that the map's method must define. Sandbox could not open any of the source hosts. |
| S10a | MSME Density per Lakh Population | Lok Sabha USQ 1883 (11 Dec 2025): 7.22 crore MSMEs on Udyam as on 30 Nov 2025 with a state-wise annexure; ASUSE 2025 (MoSPI, May 2026) is a  | Udyam registrations jumped from 2.13 crore (Dec 2023) to 7.22 crore (Nov 2025) largely through informal-unit registration, so the new map will not be comparable with the 2024 one. |
| S10i | DPIIT-Recognised Startups per Lakh Population | Ministry statement: over 2.23 lakh startups at 31 Mar 2026 (Maharashtra 38,660, Karnataka 22,600, UP 21,960); Lok Sabha Dec 2025 had 1,97,69 | Startups are counted at the registered address, which concentrates in Delhi, Karnataka and Maharashtra; do not mix the Oct 2025 and Mar 2026 cut-offs. |
| S11a | PM-JAY Hospital Admissions per Lakh Beneficia | Rajya Sabha/Lok Sabha state-wise admissions to Oct-Nov 2024 (Tamil Nadu about 96.8 lakh, Karnataka 76.4 lakh); data.gov.in resource carries  | Need a beneficiary denominator by state that moves over time; state admissions are cumulative or yearly depending on the answer, so check the basis before dividing. |
| S11b | MGNREGA Women as % of Total Person-Days | MGNREGA MIS for FY2025-26; scheme replaced by VB-G RAM G from 1 Jul 2026 | Same MIS limits as S02e: Kerala and Maharashtra are missing from the dashboard. |
| S11c | PDS Ration Card Coverage vs Actual Offtake | DFPD data in Lok Sabha replies (USQ 2732 of 7 Aug 2024; USQ 525 of 2025-26) and the NFSA portal (nfsa.gov.in) with monthly allocation/offtak | The map's own definition is vague (coverage vs offtake); NFSA coverage ratios are fixed by the 2011 population, so the 'coverage' half barely changes. |
| S11d | Anganwadi Centres per 1000 Children 0-6 | Poshan Tracker figures in Lok Sabha replies (USQ 2174 of 1 Aug 2025: UP 1,89,373 AWCs at June 2025; annexure of 29 Nov 2024 lists all states | The only state denominator for children 0-6 is Census 2011 or a projection, so the ratio mixes years; sanctioned and operational counts differ. |
| X175 | Fertiliser Consumption per Hectare | State-wise nutrient consumption: ENVSTATS indicator 55 only 2021-22; indicator 54 (2023-24) is all-India only | Source label 'CIC' looks wrong (CIC = Central Information Commission). Need state-wise 2023-24 consumption plus net sown/gross cropped area for the denominator. |
| X176 | Crop Diversification Index | DoAFW area under crops by state 2023-24 (Agricultural Statistics / Advance Estimates 2024-25); not retrieved | ENVSTATS crop-area series (indicator 50, to 2024-25*) is all-India only, so state shares need the DoAFW or RBI Handbook tables. |
| X179 | Women SHG Membership per Lakh Women | Only national figures found in a newer release: 10.05 crore households in 92 lakh SHGs (LS USQ 309, 21.07.2026). No state-wise membership ta | The state-wise SHG/household table sits on the NRLM dashboard, unreachable from here; a proxy exists in MoSPI GENDER indicators 116/117/177 (bank-linked SHGs, NABARD, as on 31.03.2025) but that counts SHGs, not women members. |
| X197 | Air Passengers per Lakh Population | AAI monthly/annual traffic by airport, FY2024-25 and FY2025-26 (also via Dataful, secondary) | Passengers are counted where they board, so per-capita-by-state rewards states with hub airports (Delhi, Maharashtra); the old map has the same flaw. Not verified that AAI files are reachable. |
| X199 | Degree Attainment Gap Urban vs Rural | PLFS Annual Report calendar year 2025 (press note 23 Mar 2026); full report tables not retrieved | Annual reports normally carry state education tables by sector, but I have not seen the 2025 ones. Map year is 2022-23, so 2023-24, 2024 and 2025 reports are all newer. |

## No newer state data

The source has not published anything newer at state level, or the map already uses the latest release.

| Map | Title | Newest release found | Caveat |
|---|---|---|---|
| S00k | Projected State Population in 2036 | Technical Group on Population Projections 2011-2036 (NCP/MoHFW, July 2020) remains the latest; TRAI still uses it for its 2026 tele-density. | Same vintage as the map; no Census 2027 based projections exist yet. |
| S01e | Hindu Temple Density per 100 sq. km | Temples of India (IIT-B) 2022 survey, 648,907 temples; no newer release found | State counts disagree between sources (Tamil Nadu 79,157 vs 89,154) and no official temple census exists. Density needs area, which the repo already holds. |
| S02b | Multidimensional Poverty Index MPI | NITI Aayog National MPI: Progress Review 2023 (NFHS-4 vs NFHS-5, 2019-21); I found no NFHS-6 based update (NFHS-6 fact sheets of May 2026 ex | An NFHS-6 recomputation is possible by the repo but would be unofficial and NFHS-6 reports fewer indicators than NFHS-5, so it would not be the NITI index. |
| S03o | Doctors per Lakh Population | National Health Profile 2023 (CBHI) Table 5.1, registered doctors up to 31.12.2022, 35 councils. No NHP 2024 found; only a national total (1 | NHP 2023 has the same 2022 reference year as the map, so it is probably the existing source. Registration counts include doctors who have moved, emigrated or died; the existing 'Delhi 14+ per lakh' takeaway could not be matched to any source. |
| S05d | Inter-Caste Marriages | No newer state-level survey found; IHDS-II (2011-12) remains the source and NFHS does not record spouse's caste. An IHDS-3 was not found (un | State estimates from IHDS-II rest on a small sample per state, so the 'highest in Kerala' takeaway is shaky. Census 2027 will include caste enumeration but results are not due yet. |
| S06d | Muslim Total Fertility Rate | NFHS-6 (2023-24) state fact sheets give TFR for all women only; secondary reports cite a national Muslim TFR of about 2.36 vs Hindu 1.94 (fr | No state-level TFR by religion is published from NFHS-6 or SRS (SRS has no religion field); only microdata analysis could produce it. The 'CIC' source named in the map could not be identified. |
| S08g | Forest Cover Change 2001-2023 | ISFR 2023 (FSI, Dec 2024) is the latest; no ISFR 2025 found | Already built from ISFR 2021/2023 (forest_change indicator in repo). The next ISFR is not yet out per my searches. |
| S08i | Flood-Prone Districts | No newer official state release found (Rashtriya Barh Ayog / NDMA / IMD) | IMD does not publish 'flood-prone districts'; the source label is likely loose. Nothing newer located. |
| S09a | Voter Turnout 2024 Lok Sabha | ECI 2024 statistical reports / Atlas 2024 (already latest) | Map already uses the 2024 general election, the newest. The next Lok Sabha election is 2029. |
| S09b | Lok Sabha Seats Held by Same Party Since 1984 | ECI results through 2024 (already latest) | Already includes 2024; no newer general election. Derived series, not a fresh release. |
| S09c | Elected MPs with Criminal Cases | ADR analysis of 2024 winners (251 of 543, 46%) | Already 2024. The ADR state-wise breakdown I found for 2024 was for sitting MPs (March 2024), so do not mix the two. |
| S09h | Youth 18-25 vs Elderly 65+ Voter Turnout Gap | No ECI age-wise turnout; likely CSDS-Lokniti post-poll survey 2024 | ECI does not publish turnout by age, so the source is a sample survey with small state samples. Nothing newer than 2024 exists. |
| S09k | Newspaper Readership per 1000 Population | IRS 2019 is the last (MRUC pilot approved Sept 2025) | No newer readership survey exists. ABC circulation per 1000 would be a different measure. |
| S09l | Ever Voted as % of Eligible Adults | Not an ECI series; likely CSDS-Lokniti survey | ECI publishes turnout, not 'ever voted'. Map is 2024 and no newer source exists. |
| S10d | Marginal Farmers Holdings Under 1 Hectare | Agri Census 2015-16 is still the latest; 2021-22 results unpublished as of PIB 21 Jul 2026. NSS 77th (2019) is older than the map's labelled | The map's source label (PLFS) is wrong for holdings data; PLFS has no land-holding size. |
| S10f | Child Labour Working Children 5-14 | PLFS covers age 15 and over only, so no 2022-23 child series exists; latest state-wise 5-14 data is Census 2011 (43.53 lakh main workers, pe | The existing map's PLFS 2022-23 label cannot be right for ages 5-14; check what it actually plots before refreshing anything. |
| S12g | Men Who Believe Family Planning Is Women's Re | NFHS-5 (2019-21) is the last source; NFHS-6 state fact sheets (101 indicators) dropped this indicator (it is not in data/nfhs6/states.json) | 'Multiple sources' hints at a mixed series; verify the original numbers against NFHS-5 state fact sheets before keeping the map. |
| S12j | Psychiatrist Density per Lakh Population | No newer state-wise count found. Latest official state figures cited by the Ministry are from NMHS 2015-16 (12 states, 0.05 to 1.2 per lakh) | NMC does not publish state-wise psychiatrist counts that I could find, and NMHS covers only 12 states. The map's 2022 year and its '0.3 per lakh' figure (the Ministry's own national estimate is about 0.75) could not be traced. |
| X166 | Hindi vs English Newspaper Readership Ratio | IRS 2019 (MRUC) is the last full survey; revival pilot only approved Sept 2025 | No IRS after 2019 found and no state tables located. ABC circulation is not readership, so it is not a like-for-like substitute. |
| X174 | Agricultural Mechanisation Tractors per 1000 | No newer source: the 11th Agriculture Census (2021-22) has not published results as of the PIB note of 21 Jul 2026 (field work only). A Feb  | State tractor registrations (Vahan, dealer data) exist but need a denominator the Agri Census would supply; nothing official gives tractors per 1000 farmers by state. |
| X183 | Missing Women Sen Methodology | No newer input: Census 2011 remains the latest enumeration (Census 2027 not yet published). SRS sex ratio at birth to 2022-24 exists but is  | A computed measure, not a published series; the '63 million' headline could not be verified. Recomputing needs Census population by sex and a reference ratio, with no newer census to apply it to. |
| X193 | Road Density km per 100 sq. km | Basic Road Statistics of India 2020-22 (MoRTH, roads as on 31 Mar 2022, state-wise tables); no later edition found | The edition is as on 31.03.2022, the same vintage as the map; MoRTH's year-end review gives a 66.71 lakh km national total for 2023 but I found no state table for it. |
| X196 | Passport Holders as % of Population | Lok Sabha USQ 1334 (9 Feb 2024) has state-wise passports issued 2019-2023 (same year as the map). I found no state-wise 2024 or 2025 table;  | Passports issued in a year is not 'holders as % of population' (that stock is not published by state); a later state annexure may exist in 2025-26 replies but I could not find it. |
| X202 | Households with Computer or Laptop | No newer state survey found. NSS 80th CMS Telecom 2025 lists internet, phone and fibre indicators but none for household computers; NFHS-6 e | Last survey with household computers by state was NSS 75th (2017-18) and NFHS-5; the 'RBI/MoSPI 2022-23' source on the map could not be traced. |
| X205 | Indebted Agricultural Households | NABARD NAFIS 2021-22 (released 10 Oct 2024) is the latest; the map already uses it (year 2022) | No newer round exists; NSS 77th (2019) is older. The state table is only in the full NAFIS report. |

## Unclear

The measure behind the map could not be pinned down, or the source label looks wrong. These need a decision on what the map should show.

| Map | Title | Newest release found | Caveat |
|---|---|---|---|
| S01h | Beef and Buffalo Meat Consuming Househol | No newer household-share release found; HCES 2023-24 API gives only a combined 'egg, fish & meat' category | NFHS-6 fact sheets (in repo) carry no meat/egg/fish frequency items and HCES API item detail is cereals only. A beef-specific state series is not published in a machine-readable form that I could find. |
| S01i | Egg-Consuming Households | No newer household-share release found; HCES 2023-24 combined 'egg, fish & meat' expenditure only | Egg-only state data is not in the HCES API; the HCES 2023-24 report tables may have it but I did not verify them. |
| S01k | Fish-Consuming Households | No newer household-share release found; HCES combined 'egg, fish & meat' only | Same gap as eggs: no fish-only state series in the API or NFHS-6 sheets. |
| S02a | Households Earning Above Rs 25000 Month | No official state series for household income. HCES 2023-24 gives per capita consumption only | No survey publishes household income by state; a threshold on MPCE x household size would be a derived, non-official figure. |
| S02i | Bonded Labour Identified and Released cumulat | Latest state-wise table I found is a Lok Sabha reply of 24 Jun 2019 (to 31 Mar 2019); national total of 315,302 to Jan 2023 (via IDR). No st | Cumulative state counts change slowly and may be updated in a 2025-26 Rajya Sabha reply I did not find. |
| S05b | SC Households Owning Agricultural Land | Unverified. 11th Agriculture Census 2021-22 fieldwork is reported complete (Jul 2026) but final SC holdings tables were not found; 10th Cens | 'Multiple sources' means the map mixes measures (operational holdings vs households owning land), so no single refresh exists. The Agriculture Census counts holdings operated, not households owning land. |
| S05f | Manual Scavenging States Where It Persists | LS USQ 1599 (July 2026): NAMASTE validated 89,915 sewer/septic tank workers and 2,85,165 waste pickers by state as on 20 Jul 2026; identifie | The government's position is that manual scavenging is not reported, so a 'where it persists' map has no official state series; NAMASTE validation counts measure sanitation workers, a different thing. The Lok Sabha annexure itself still has to be fetched. |
| S06c | Muslim Multidimensional Poverty Rate | No official religion-wise MPI by state found. NITI Aayog MPI (NFHS-5 base) is not disaggregated by religion; NFHS-6 fact sheets carry no rel | 'Multiple sources' means the original is a custom analysis, probably of NFHS-5 microdata; a refresh would need NFHS-6 unit-level data, whose release was not verified. |
| S06j | Hindu Denominational Diversity Vaishnavism vs | Could not identify a 'Dharmaviki/IIT-B' dataset; no official state series exists (Census has no sect question) | Not an official statistic and the source could not be located, so there is nothing to refresh; treat the existing map as unverified. |
| S07e | Teacher Vacancy Rate in Government Schools | No official state series; PAB minutes via Careers360 (3.58 lakh vacant, 18 states/UTs) | UDISE+ reports teachers in position, not sanctioned posts, and the Ministry says vacancy data sits with states, so any rate is built from PAB minutes and covers only some states. |
| S07g | Internet Used for Information or Knowledge | NFHS-6 (2023-24) women who have used the internet is already in repo (n6_women_internet); NSS 80 CMSE/CMST 2025 are candidates | The map title does not say which survey it used, so a like-for-like refresh is not possible. 'Used the internet' is not the same as 'for information or knowledge'. |
| S08c | Mean June Temperature | IMD monthly climate summaries (maps and subdivision text), no state table found | IMD does not publish a state-wise mean temperature table; it would need gridded data (IMD Pune) averaged over state polygons. |
| S08d | Extreme Heat Days Above 40C per Year | Not published by IMD; ENVSTATS indicator 87 has heat-wave days by state for 2024 (a different measure) | Heat-wave days (IMD criteria) are not days above 40C. The repo already carries heat_wave_days, so this map's measure would need redefining. |
| S09f | RTI Applications per Lakh Population | CIC Annual Report 2024-25 covers Union public authorities only; state commissions report separately | CIC is not a state series. State application counts are scattered across state information commissions; SNS reports cover appeals and complaints, not applications. |
| X173 | Gig Workers as % of Workforce | No official state series. PLFS has no gig/platform code (confirmed in 2025 reporting; MoSPI reviewing it in Sep 2026). Only e-Shram platform | The map's stated source (PLFS 2022-23) cannot give a gig share, so the existing map is itself suspect; e-Shram counts are registrations, not a share of the workforce, and are not comparable. |
| X177 | Landless Agricultural Labourers | Agri Census 2015-16 is still the latest (2021-22 not released) but it does not count landless people; NSS 77th round (Jan-Dec 2019) has hous | NSS77 measures landless households, not landless agricultural labourers, so a rebuild would change the definition; Census 2011 agricultural-labour counts are older. |
| X181 | Marital Rape Experience vs Reporting Gap | NFHS-6 (2023-24, May 2026) spousal violence (indicator 95) is already in the repo; NCRB Crime in India 2024 has no marital-rape head (not an | Mixed measure with no official 'marital rape reported' series, so a reporting-gap ratio can only be built from cruelty-by-husband cases vs NFHS spousal violence, which is a different construct. The map's claim of near-zero reporting could not be traced to a so |
| X194 | Railway Stations per 1000 sq. km | No state-wise station count found; Dataful (secondary) shows only the national figure, 7,469 stations in 2024-25. Indian Railways reports by | Zones cross state lines, so a state count needs station-level data (Railway Board) that I could not reach (railwayboard.indianrailways.gov.in returns 502). |
| X195 | Telecom Tower Density per 1000 sq. km | No state stock series found. TRAI's 2025-26 yearly report has none. DoT publishes monthly state-wise 5G BTS counts only; a Lok Sabha answer  | 5G BTS and 'installed in 3 years' are not total towers, so a like-for-like rebuild is not possible; tarangsanchar.gov.in is not reachable from the sandbox. |
| X198 | Income Threshold Top 10% by State | HCES 2023-24 gives average MPCE for 12 fractile classes by state and sector (e.g. Bihar rural 90-95: Rs 5,642; 95-100: Rs 7,562) | HCES gives class averages, not the decile threshold, and measures consumption not income; a rebuild would be a proxy (e.g. mean of the top 10%) and the map label would need changing. |
| X203 | Distance to Nearest Bank Branch Rural km | Nothing located. Village-level distance sits in Census 2011 village directory and Mission Antyodaya data, neither has a recent state series  | I could not trace the map's source (RBI/DoP 2023) to any published state table, so I cannot vouch for the existing map either. |

## Not a state series

The source does not give a state breakdown.

| Map | Title | Newest release found | Caveat |
|---|---|---|---|
| S05g | SC Representation in IAS vs Population Share | RS reply of 12 Feb 2025 gave total IAS strength (5,577) and 2020-24 direct recruits (SC 135) but no current category-wise strength or cadre- | This is a service-level (all-India) proportion; the Union withheld cadre-wise and category-wise strength, so no state series exists. Cadres are not the same as states either. |
| S06i | People Who Say Religion Is Very Important in | Pew 'Religion in India: Tolerance and Segregation' (survey Nov 2019 to Mar 2020, published Jun 2021) is the only edition found; national fig | Pew reports by region and religion, not state, so the map's 20-point state spread cannot be sourced; the existing '90%+' headline also differs from Pew's 84%. |
| X169 | IFCN-Registered Fact-Check Organisations per | IFCN signatories directory (Poynter), country level | IFCN lists organisations by country/language, not by state; a state split would be our own geocoding of organisation HQs. Title is truncated so the denominator is a guess. |

## Other things the research found

- Several older takeaways disagree with the newest official data, which suggests weak original sources. Examples reported: National Health Accounts 2022-23 puts Bihar government health spending at Rs 1,056 per head against the old "under Rs 500"; S06i quotes "90%+" where Pew reports 84% nationally; S06e is labelled 2019-2024 though Crime in India 2024 appeared in 2026.
- Source labels on some maps look wrong (for example X175 says CIC, S01d says DFPD, S08i says IMD, S10f cites PLFS for children aged 5-14, and PLFS covers age 15 and over). Check what these maps plot before refreshing them.
- The Agriculture Census 2021-22 had not been released by July 2026, so the three maps built on it have no newer data.
- MGNREGA was replaced by a new scheme on 1 July 2026 according to the agent, which breaks continuity for S02e and S11b. Unverified by me.
- Sites unreachable from this sandbox: data.gov.in, eparlib (Lok Sabha answers), the RBI Handbook table files, ECI statistical reports, cgwb.gov.in, bprd.nic.in, the Income Tax Department and Udyam portals. A file from you would unlock the "needs a file" group.

## Built from this list, 2026-10-19

Each of these now has a generated sheet and an indicator in the explorer, with its source and checks described in `data/CALCULATIONS.md`. The old map keeps its place in the catalogue and links to the new one as its newer version.

| old map | new map | source |
|---|---|---|
| S07a | X272 | ASER 2024, Std V reading, government schools |
| S07h | X273 | ASER 2024, children 6-14 not in school |
| X168, S01d | X274 | TRAI Table 1.43, internet subscriptions per 100, March 2026 |
| S03t | X275 | India TB Report 2024, case notification rate (not incidence) |
| S10h | X276 | RBI remittances survey 2023-24, share of inward remittances (not dependence) |
| S07i | X277 | UDISE+ 2024-25 via MoSPI, primary pupil-teacher ratio, all management |
| S01j | X278, X279 | HCES 2023-24, rice share of cereals, rural and urban |
| S03f | X280 | SRS maternal mortality 2022-24 (19 states) |
| S03s | X281 | SRS abridged life tables 2019-23 (22 states) |
| X189 | X282 | NFHS-6, improved drinking-water source |

Still open: X184 (sex ratio at birth) needs Table 16 on page 315 of the 363-page SRS 2024 Statistical Report, and censusindia.gov.in cannot be downloaded from here (incomplete certificate chain) and the text extractor reads about 20 pages at a time, so it needs the PDF or the table supplied; S09e (SFLC internet shutdowns, a scrape of a tracker that counts recorded events, not days); X172 (to be retired in favour of X206 and X207, HCES consumption). Everything else on the list above that needs a file nobody has supplied stays as a vintage-labelled map.

## Quality pass, 2026-10-19

Read all 77 generated sheets and ran axe (WCAG 2.1 AA) over the explorer, the home page, the index, the methodology and stories pages and six map pages in both themes at 390x844 and 1280x900. Found and fixed:

- **Every map page stretched the sheet.** The page template gave the image `width="1200" height="900"` and `width:100%` with no `height:auto`, but every sheet is 3052x1725, so on a phone the map was squashed to a fraction of its width. The template now carries the real size and `height:auto`, and each page links to the full-size image.
- **Leader lines ran through the highest and lowest labels** on every sheet, and a callout could land on top of another state's label (the Rajasthan callout sat on Delhi). The line now stops at the label, and placement scores against where each label really is, including those on leader lines, and keeps leader lines off other labels.
- **Ranking bars ran under their values.** Bars now stop short of the value column, and the lowest five show a sliver instead of nothing.
- **Indicators with no good or bad end** (crimes registered, notification rates, shares) were painted green at the top and red at the bottom, which read the top as good news. They now use a neutral slate. This affects 24 sheets.
- **Home page banner** still described the 25 NFHS-6 indicators; it now describes the 77 rebuilt maps.

Not found: any serious or critical axe violation, any horizontal overflow, or any explorer error across all 90 indicators. Every number in the sheet text that does not come straight from the data (source counts, definitions, derived ratios) was spot checked against the files. `data/hindi-review.csv` lists the 424 Hindi strings written for the new sheets and indicators. No native reader review is planned (owner's decision, 2026-10-20), so the Hindi is machine-written and the English governs.

## Built from the RBI Handbook, 2026-10-20

Firecrawl read the RBI Handbook of Statistics on Indian States 2024-25 tables (the files sit behind a bot challenge that blocks curl). About 20 credits for these three maps, at about one credit a page.

| old map | new map | table |
|---|---|---|
| S08b | X283 | 54 and 56, net irrigated area over net sown area, 2023-24 provisional |
| S02n | X284 | 152, offices of scheduled commercial banks, March 2025, per lakh people |
| S08j | X285 | 107, stage of groundwater extraction, CGWB 2024 assessment (a different measure from over-exploited blocks) |

The Handbook has 182 tables, so it is the cheapest route for several other maps on the waiting list; the crop-area maps (S08f, X176) use Tables 67 to 79.

## S08f rebuilt as X286 (2026-10-20)

Rice and sugarcane share of rice, sugarcane and coarse-cereal area, 2024-25, from RBI Handbook Tables 67, 69 and 78 (30 states; Goa has no coarse-cereal area). The old "10x for Punjab and Haryana" claim holds for Punjab (36 to 1) and not for Haryana (2.7 to 1). X176 (crop diversification) is not buildable from the Handbook's crop groups.

## Closed out, 2026-10-20

- **X172** is superseded by X206 and X207 (it links to X206 as its newer map).
- **S09e** (SFLC shutdowns): the tracker returned 502 and no primary state table exists, so the map keeps its figures and carries a data note with the sourced headline counts.
- **X184** (sex ratio at birth): Statement 16 of the SRS 2023 report (2021-23) is at printed page 66, about PDF page 97, and Firecrawl would not return more than about 90 pages per call from this host. A PDF of that page would settle it. The map carries a data note with the published top and bottom states.
- **Waiting and unclear lists:** not worked through. The MoSPI API has no PLFS education table (X199) and its RBI dataset covers trade and exchange rates, not states. The 21 unclear maps need a decision on what each should show, not more data.
