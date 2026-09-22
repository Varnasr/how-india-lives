# how-india-lives

State-level atlas of India: 205 static choropleths with takeaway and policy
notes, plus a live interactive choropleth over 16 indicators. Static HTML, no
build step for the part that runs, deployed to GitHub Pages at
howindialives.impactmojo.in. English and Hindi throughout.

## Commands

```bash
python3 scripts/check_data.py       # both data files, run by CI
python3 scripts/build_map_pages.py  # regenerates m/*.html, m/index.html, sitemap.xml, robots.txt
python3 -m http.server 8000         # then open http://localhost:8000
```

`build_map_pages.py` is deterministic: running it on an unchanged `maps.json`
produces no diff, which is what lets CI use it as a staleness gate.

## Two data files, two completely different jobs

- **`data/maps.json`** is a catalogue of 205 pre-rendered PNGs. It carries no
  per-state numbers at all, only metadata and prose. The PNGs were produced
  outside this repository and **there is no renderer here**, so a new static map
  cannot be generated from the repository as it stands.
- **`data/interactive-data.json`** is the numeric layer, 16 indicators keyed by
  state. `explore.html` renders it as a live SVG choropleth from
  `data/india-states.geojson`, with hover, keyboard navigation and a scatterplot.

That asymmetry decides where new work goes. **Adding an indicator to the
interactive layer is the cheap path and the better artefact**: a live, comparable,
accessible, deep-linkable map with no image to render and nothing to keep in
step. Adding a static map means producing a PNG somewhere else and committing it.

`mapId` is the whole of the cross-link between the two views, in both directions.

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

## Watch out for

- **`data/interactive-data.json` is precached in `sw.js`.** Adding an indicator
  without bumping `CACHE_NAME` means returning visitors keep the old file and
  never see it. A check pins that both data files are still in `PRECACHE`, so
  removing one has to be deliberate.
- **Counts are written in prose in three places**: `scripts/build_map_pages.py`
  ("All 205 maps" in the page footer), `data/README.md` and `README.md`. All
  three are pinned against the actual lengths.
- **Coverage differs by source and grey is honest.** The SRS and NSS series cover
  22 larger states; PLFS and the Census cover all 36. A state left grey has no
  published figure, not a low one, and the note under the map says so. Do not
  fill a gap by interpolation.
- **Nine maps in `maps.json` are self-flagged `quality: "UNCERTAIN"`** and are
  published anyway. That is a live decision, not a bug, but check the flag before
  quoting a figure from one.
- **The static maps run on old vintages**: 37 on NFHS-5 (2019-21) and 37 on
  Census 2011. The interactive layer is where the recent data is.

## The MoSPI API, if you refresh the figures

`flfpr` (PLFS 2025) and `litgap` (NSS 75th round, 2017-18) came from
`api.mospi.gov.in`, `GENDER` dataset, on 2026-09-22.

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

`.github/workflows/validate.yml` runs `check_data.py` and the regeneration gate
on every push and pull request, with no `paths:` filter. `pages.yml` deploys and
validates nothing.
