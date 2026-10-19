# how-india-lives

Shared engineering standard: @.claude/engineering-standards.md. It applies to all work in this repository. This file adds what is specific to the project, and wins where the two disagree.

State-level atlas of India: 205 static choropleths with takeaway and policy
notes, plus a live interactive choropleth over 66 indicators. Static HTML, no
build step for the part that runs, served by Netlify (site `howindialives`,
built from `main`) at howindialives.impactmojo.in. English and Hindi throughout.

## Commands

```bash
python3 scripts/check_data.py       # both data files, run by CI
python3 scripts/check_design.py     # one palette, both themes, run by CI
python3 scripts/build_map_pages.py  # regenerates m/*.html, m/index.html, sitemap.xml, robots.txt
python3 scripts/stage_site.py       # what Netlify publishes; with a directory, copies it there
python3 -m http.server 8000         # then open http://localhost:8000
```

`build_map_pages.py` is deterministic: running it on an unchanged `maps.json`
produces no diff, which is what lets CI use it as a staleness gate.

## Two data files, two completely different jobs

- **`data/maps.json`** is a catalogue of 258 PNGs. It carries no per-state
  numbers at all, only metadata and prose. **205 of them were produced outside
  this repository**, from sources this repository does not hold, and cannot be
  regenerated here.
- **`data/interactive-data.json`** is the numeric layer, 66 indicators keyed by
  state. `explore.html` renders it as a live SVG choropleth from
  `data/india-states.geojson`, with hover, keyboard navigation and a scatterplot.

**The other 51 are generated (X206 to X256), and that is the path a new sheet should take.**
`scripts/render/` renders a sheet from an indicator in `interactive-data.json`,
so the static map and the interactive map of the same indicator are drawing the
same numbers and cannot disagree. X206 to X211 were made this way on
2026-09-23, and X212 to X239 (NFHS-6, PLFS 2025 and UDISE+ 2024-25 sheets) and X240 to X244 (NCRB 2024, from Women on Record) on 2026-10-19. Before that there was no renderer here at all, and this file said
in as many words that a static map could not be made from the repository.

An interactive indicator is still the cheaper artefact, and a new figure should
land there first. What changed is that turning it into a sheet afterwards is
now one line in `scripts/render/sheets.json` rather than a rendering job in
another tool.

`mapId` is the whole of the cross-link between the two views, in both directions.

## NFHS-6 and PLFS 2025 came in October 2026, and how

`data/nfhs6/states.json` holds the NFHS-6 (2023-24) state and UT totals, read
from IIPS's fact-sheet compendium of May 2026 by `scripts/extract_nfhs6.py`.
**Thirteen of that PDF's 36 sheets carry no text layer**, so
`scripts/ocr_nfhs6.py` reads them as images first (`rapidocr-onnxruntime`).
OCR can lose a row label or misread a digit, so the extract was held to three
tests: the NFHS-5 column printed in each sheet matched MoSPI's NFHS-5 values on
every spot check (stunting 17 of 18 sheets, the one miss a row absent in the
source; institutional births and caesarean sections 10 of 10), every state's
total sits between its urban and rural figures, and the largest changes were
read against the page images. A figure the source prints as `*` or leaves blank
is absent, never filled in. Manipur has no NFHS-6 sheet.

`scripts/build_nfhs6_indicators.py` turns 25 of them into `n6_*` indicators
with the NFHS-5 total beside each as `previous`, and the explorer's "Change
since 2019-21" view reads that. `scripts/build_plfs_indicators.py` adds the two
PLFS 2025 unemployment indicators from `data/mospi/plfs-2025.json`. Both are
idempotent and have `--check`. `maps.json` carries `newer` on the 18 NFHS-5
maps whose measure NFHS-6 repeats; the map page and the gallery card link to it.

**NFHS-6 is not a drop-in for NFHS-5.** It reports 101 indicators against 131;
anaemia and the mortality rates are not among them, so those static maps keep
their NFHS-5 figures and say so. Some changes are large (Karnataka's spousal
violence 44.4 to 14.1, Ladakh's 17.7 to 1.9) and are what the sheets print;
quote them with the survey's own caution that NFHS-6 is provisional.

## Crime figures come from Women on Record, and mean registrations

`data/ncrb/crimes-against-women.json` holds NCRB's 2023 and 2024 state and UT
figures for five headings (all crimes, rape, cruelty by husband or relatives,
dowry deaths, acid attacks), pulled by `scripts/extract_ncrb_wor.py` from the
Women on Record dataset, which reads Crime in India Volume 1 table 3A.2 and
checks every row against NCRB's own totals. The source PDF's address and SHA-256
sit beside each figure, with the Women on Record commit. `scripts/build_ncrb_indicators.py`
(`--check` supported) turns them into the `ncrb_*` indicators; X240 to X244 are
drawn from those.

**These count crimes registered, not crimes committed.** A higher figure can mean
more crime, easier reporting, or both, so `higherIsBetter` is null and the sheets
say so. Do not rank states on them. Dowry deaths and acid attacks are derived
from NCRB's case counts over its female population because the printed rate has
one decimal; the derived value rounds to NCRB's printed rate in every state. A
zero means none registered. The trafficking map (S02j) is not refreshed: its 2024 table is in Crime in India
Volume III, which could not be fetched from a primary source. Honour killings,
witchcraft murders and crimes against SCs come from `data/ncrb/crime-in-india-2024-other.json`,
read by `scripts/extract_ncrb_other.py` from Volumes 1 and II (SHA-256 pinned, totals
checked) and turned into `ncrb_honour`, `ncrb_witchcraft` and `ncrb_sc_crimes` by
`scripts/build_ncrb_other_indicators.py`; X249 to X251 are drawn from those.

## Climate and court maps, and the two source faults found

`data/climate/envstats.json` (MoSPI EnviStats) and `data/courts/lok-sabha-3501.json`
(Lok Sabha Unstarred Question 3501, 13 March 2026, Annexures II and IV) feed
`scripts/build_climate_indicators.py` and `scripts/build_court_indicators.py`
(both `--check`), and X245 to X248. Each source had a fault that no check on the
numbers alone would have caught:

- **EnviStats labels the India total as "Puducherry"** in forest cover (715,342.61
  sq km in ISFR 2023). It equals the sum of every other row, so Puducherry has no
  figure and the row is never mapped. The 2023 minus 2021 total, +156.41 sq km, is
  the increase ISFR 2023 reports. The merged Dadra and Nagar Haveli and Daman and
  Diu also has two ambiguous rows and is left out.
- **The court answer is a scan and Meghalaya's pendency row contradicts itself**
  (4,917 + 4,917 is not 16,671). The national columns add up only with the printed
  figures, so the error is in the source. Meghalaya is left off that map. The printed
  national working-judges total (21,026) is 12 above what the state rows add to
  (21,014); the rows are used. The pendency table is NJDG as on 9 March 2026 and the
  judges table is Nyaya Vikas and undated, so cases per judge is a rough guide.

Heat-wave days swing from 0 to 26 between years in one state, so the map uses the
2022-24 mean for the 19 states with all three years.

## State output from MoSPI National Accounts

`scripts/fetch_mospi_nas.py` pulls per-head GSDP and state value added by industry (base 2011-12, current
prices, 2022-23 and 2024-25) from `api.mospi.gov.in/api/nas/getNasData` into `data/mospi/nas-state.json`.
`limit` above 100 returns 400. `scripts/build_nas_indicators.py` builds `gsdp_pc`, `gsva_agri`, `gsva_mfg`
and `gsva_services` (X252 to X255); each state's twelve industry rows must add to its published total.
Services exclude mining, electricity and construction. Nagaland and Ladakh have no 2024-25 figure. There is
no all-India row in these series, so `national` is null. The API can be called directly from Python with
`ctx.options |= 0x4`, which is faster than the MCP tool for many states.

## School enrolment and PLFS contract series

`scripts/fetch_mospi_udise.py` (`/api/udise/getUdiseRecords`, indicator 28) and `scripts/fetch_mospi_plfs.py`
(`/api/plfs/getData`, indicator 5) commit their raw rows under `data/mospi/`; `build_udise_enrolment_indicators.py`
and `build_plfs_contract_indicator.py` turn them into `udise_private_share` (X257) and `plfs_no_contract` (X258).
UDISE management categories must add to the all-management total. PLFS annual data stops at 2023-24, and
indicator 4 (worker distribution) returned nothing for the filters tried, so S10g is not rebuilt.

## CSV exports and the calculations behind the maps

`scripts/export_csv.py` writes `data/csv/` (all indicators, one file per indicator, and
`calculations/` for every derived one) and `data/CALCULATIONS.md` says in words how each figure is
got. The export recomputes each derived value from the source files and stops if it differs from the
indicator, so a calculation file cannot disagree with its map. CI runs it with `--check`. After any
indicator change, run `python3 scripts/export_csv.py` and commit the result.

## Why the checks exist

Before 2026-09-22 `interactive-data.json` was checked by nothing. The workflow
that checked `maps.json` carried `paths: [data/maps.json, maps/**]`, so an edit
to the interactive layer, the geojson, or `sw.js` ran no job at all. That is the
shape of the problem rather than an oversight: the file most likely to be edited
was the one outside the trigger.

Every failure `scripts/check_data.py` guards against is quiet. Nothing in this
repository throws:

- **A state name the geojson does not know** does not colour, and does not warn.
  `Orissa` for `Odisha` leaves one state grey on a map that otherwise looks done.
- **A `national` figure outside the range of its own states** is a unit or
  vintage mismatch, and renders as a legend marker off the end of the scale.
- **`higherIsBetter` absent** captions the legend as though more were better.
  `null` is a deliberate third value for indicators with no normative direction,
  so the check accepts `true`, `false` and `null` and rejects only absence.
- **A stale `mapId`** renders a cross-link button that 404s.
- **A precached path that 404s** rejects `cache.addAll`, which fails the service
  worker install outright and leaves the site with no offline layer, silently.

Four of these were fault-injected against real failures to confirm they bite.

## The palette was written eight times and every copy was failing

`assets/tokens.css` owns it now, and `scripts/check_design.py` holds it there.

It used to live inline in `index.html`, `explore.html`, `methodology.html` and
`stories.html`, twice inside `scripts/build_map_pages.py`, and again in
`assets/common-header.css`, under four naming schemes: `--accent-color`,
`--acc`, `--im-accent`. They had drifted. Only `index.html` defined the status
colours. Only index and explore defined a second accent. The generated
templates carried a shorter dark block holding the failing values, so all 205
map pages shipped `--mut: #64748B` at 2.18:1 on the card it sits on.

The numbers were failing in the light theme too, measured against the surfaces
they are painted on: `--accent-color` #0EA5E9 at **2.53:1**, `--text-muted`
#94A3B8 at 2.34:1, `--success` #10B981 at 2.32:1, `--warning` #F59E0B at
**1.96:1**, `--danger` #EF4444 at 3.44:1, `--secondary-accent` #6366F1 at
4.08:1. That was 106 failing nodes on the home page and more on every other
page, because the same numbers had been copied into each one. Fixing a page
fixed a page.

**Contrast ratio is symmetric**, which is what made the accent fixable at all.
`#0EA5E9` as ink on white and white as ink on a `#0EA5E9` chip are the same
2.77:1 measurement, so darkening the token to clear AA fixed the label and the
chip in one move.

### The accent is a fill too, and that direction was never measured

`--accent-color` is ink on a light page and a **fill** under a light ink on a
dark one, and those pull opposite ways. The check walked ink-on-surface only,
so it reported OK while **white on the dark-theme `#38BDF8` measured 2.14:1** —
every "Open in the interactive atlas" button on all 205 map pages, every filter
pill and every map count on the home page, the cite and share buttons in the
detail panel, and the subscribe button. Ten rules and two inline styles wrote
`color: white` against `var(--accent-color)`.

`--on-accent` is the ink that flips with it: white in the light theme,
`#0F172A` in the dark one, 8.43:1 on the bright accent. `FILLS` in
`scripts/check_design.py` measures that direction now, for all three accents,
and was fault-injected against the real failure.

The generated map pages are the reason this mattered 205 times over: the
template in `scripts/build_map_pages.py` carried `background:var(--acc);
color:#fff`, so one string produced the defect on every page. Changing the
generator and re-running it is the whole fix; the regeneration gate in CI then
holds it.

`docs/index.html` is docsify's own theme and outside the palette entirely. Its
`#d97706` measured 2.97:1 as the site name and 3.18:1 as the link.

### What the token check cannot see

A colour written as a literal in a rule, and a colour composited with opacity,
are invisible to it. Consolidating the tokens left five such cases behind, and
axe over the pages is what found them:

- **The headline gradient is ink, not decoration.** `.hero-text h1 span` paints
  `--gradient-primary` into text with `background-clip: text`. Its sky stop was
  2.77:1, under even the 3:1 large-text threshold, and no automated check reads
  a gradient used as a text colour.
- `explore.html` wrote `#EF4444` and `#10B981` as literals in three rules, and
  those are the ink of the ranking figures a reader came for.
- `methodology.html`'s three data-quality badges were literal ink on literal
  tints. BUILT / NEW / UNCERTAIN is the flag telling a reader whether to trust
  a map.
- `stories.html` put white on WhatsApp's `#25D366` at **1.98:1**. The brand's
  own dark teal `#075E54` is 7.67:1 and still reads as WhatsApp.
- `#collections-scroll` scrolled horizontally and no keyboard could reach it.

Run both when you touch colour. A token check and a browser audit are not
substitutes for each other, and this repository is the argument for that.

## Watch out for

- **`data/interactive-data.json` is precached in `sw.js`.** Adding an indicator
  without bumping `CACHE_NAME` means returning visitors keep the old file and
  never see it. A check pins that both data files are still in `PRECACHE`, so
  removing one has to be deliberate.
- **Counts are written in prose in three places**: `scripts/build_map_pages.py`
  ("All 258 maps" in the page footer), `data/README.md` and `README.md`. All
  three are pinned against the actual lengths. `index.html`, `stories.html`,
  `methodology.html` and `explore.html` carry the number too, in titles, Open
  Graph tags and the JSON-LD block, and nothing pins those.
- **Coverage differs by source and grey is honest.** The SRS and NSS series cover
  22 larger states; PLFS and the Census cover all 36. A state left grey has no
  published figure, not a low one, and the note under the map says so. Do not
  fill a gap by interpolation.
- **Nine maps in `maps.json` are self-flagged `quality: "UNCERTAIN"`** and are
  published anyway. That is a live decision, not a bug, but check the flag before
  quoting a figure from one.
- **The static maps run on old vintages**: 37 on NFHS-5 (2019-21) and 37 on
  Census 2011. The six generated sheets are the exception, and they inherit
  their vintage from the indicator rather than carrying one of their own.
  "The interactive layer is where the recent data is" used to be the whole
  answer and was only half true: eleven of the first sixteen indicators were
  Census 2011 too. The four HCES 2023-24 series are the most recent figures in
  the repository, and X206 to X209 are now the first static sheets carrying
  them.
- **The head of `explore.html` is a two-column grid above 960px** and a plain
  stack below it, with the source order untouched. Wrapping the two columns in
  divs was tried and is worse: the indicator description in a 340px column moves
  the map by up to 75px every time you change indicator, and the mobile stack
  becomes headline, tabs, controls, lead, which reads backwards.

## The renderer

```bash
python3 scripts/render/render.py            # every generated sheet
python3 scripts/render/render.py mpce_r     # one of them
python3 scripts/render/render.py --svg-only # no browser needed
```

`scripts/render/choropleth.py` writes the SVG and needs nothing but the
standard library; `render.py` rasterises it through headless Chromium at
3052x1725, the size of the existing sheets. **Inter is vendored** as
`scripts/render/Inter-latin.woff2` (OFL, licence beside it) and embedded in the
page as a data URI, because a render that quietly falls back to a system face
produces a sheet that looks nearly right and does not match the other 205.

`scripts/render/sheets.json` holds the curatorial half: which indicator, which
section, the takeaway, the policy note, the tags and the Hindi. **No number is
written there.** The palette, the ramp and the layout are sampled from
`maps/education/S07a_*.png` rather than invented, so a generated sheet sits in
the same visual family.

Three things in it are load-bearing:

- **The callout colour follows `higherIsBetter`.** The top of a consumption map
  is good news and the top of a Gini map is not, and a sheet that paints both
  in the same red is asserting something false about one of them.
- **Label ink is chosen by comparing both contrast ratios**, not against a
  fixed luminance cutoff. The cutoff is how white-on-amber at 3.19:1 shipped
  twice in the ImpactMojo diagrams.
- **The min and max annotations are placed by score, not by a fixed offset.**
  A constant offset put the Jharkhand callout on top of the Uttar Pradesh
  label, and the offset that works on one indicator is wrong on the next
  because the extreme state moves.

`scripts/check_data.py` holds the two ends together: every sheet must name a
live indicator, carry a catalogue entry with the same filename, exist on disk,
and be linked back to by that indicator's `mapId`. Both halves were
fault-injected. What it cannot check is whether the rendered sheet *looks*
right, so open the PNG after rendering.

## The MoSPI API, if you refresh the figures

`flfpr` (PLFS 2025) and `litgap` (NSS 75th round, 2017-18) came from
`api.mospi.gov.in`, `GENDER` dataset, on 2026-09-22. `mpce_r`, `mpce_u`,
`gini_r` and `gini_u` came from the `HCES` dataset, indicators 1 and 9, year
2023-24, `imputation_type_code=1`, on 2026-09-23.

Three things about HCES that are easy to get wrong. **There is no combined
rural-and-urban series**: `sector_code=3` returns nothing, which is why these
are four indicators and not two, and why no combined figure is quoted anywhere.
**The "All India" row is a row like any other** and has to be pulled out rather
than mapped onto a state. And the survey publishes **with and without
imputation** of the value of items received free through welfare programmes;
these use *without*, which is the series MoSPI leads with, and the national
figures agree with the published factsheet (rural 4,122, urban 6,996).

The host negotiates TLS in a way OpenSSL 3 rejects by default. A plain `curl`
dies with *unsafe legacy renegotiation disabled*; a Python client needs
`ctx.options |= 0x4` (`OP_LEGACY_SERVER_CONNECT`, unnamed before Python 3.12)
before it connects at all. The REST paths are not in the portal's own JS bundle
either, so the practical way to re-pull is the MoSPI MCP tooling rather than a
fetch script here. The values are therefore committed, with a `retrieved` date,
rather than fetched at build time.

MoSPI spells some states its own way (`Jammu & Kashmir`, `Andaman & Nicobar
Islands` with a double space, `Dadra & Nagar Haveli and Daman & Diu`). Every one
of those resolves to a different string in the geojson, and a mismatch is exactly
the silent failure above, so map the names and let the check confirm it.

## Testing

`.github/workflows/validate.yml` runs `check_data.py`, `check_design.py` and
the regeneration gate on every push and pull request, with no `paths:` filter.
Netlify deploys from `main` and publishes only what `scripts/stage_site.py`
names as published (`netlify.toml`), so `CLAUDE.md`, `scripts/` and the
contributor notes are not served. A new top-level file fails CI until it is
named published or kept back. GitHub Pages served the site until 2026-10-12.
