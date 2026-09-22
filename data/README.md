# Data files

## `maps.json`
The catalog of all 205 static choropleth maps (metadata + takeaway text). Rendered by the
gallery on `index.html`. No per-state numeric values.

## `india-states.geojson`
Boundaries of India's 36 states and union territories, derived from **Natural Earth** (public
domain) and simplified for the web (~60 KB). Each feature carries `name`, `code`, `type`, `region`.
Used by the interactive map on `explore.html`.

## `interactive-data.json`
The per-state numeric layer that powers the interactive atlas (`explore.html`). This is the file to
extend as more indicators get real state-level values.

### Schema
```json
{
  "note": "Provenance / caveats shown under the map.",
  "indicators": [
    {
      "id": "literacy",              // stable slug; also the deep-link hash (explore.html#literacy)
      "theme": "Education",          // groups the indicator in the picker
      "name": "Literacy Rate",
      "unit": "%",
      "source": "Census of India",
      "year": "2011",
      "desc": "One-line description shown under the selector.",
      "higherIsBetter": true,        // true | false | null — only affects the legend caption
      "national": 74.04,             // India average; drawn as a marker on the legend (optional)
      "mapId": "S07d",               // OPTIONAL: id of the matching map in maps.json
      "retrieved": "2026-09-22",     // OPTIONAL: ISO date the values were pulled from an API
      "values": {                    // keys must match the `name` field in india-states.geojson
        "Kerala": 94.0,
        "Bihar": 61.8
      }
    }
  ]
}
```

### Adding an indicator (promoting a catalog map to interactive)
1. Add an entry to `indicators` with the schema above.
2. Key `values` by the exact state names in `india-states.geojson` (states without a value render
   grey / "no data" — that is fine and honest).
3. Set `mapId` to the corresponding `id` in `maps.json` to cross-link the two views: the interactive
   page shows a **"View the detailed map →"** link, and that map's card on `index.html` shows an
   **"Explore interactively"** button. Both are driven entirely by this field.
4. Bump `CACHE_NAME` in `sw.js`. This file is **precached**, so without the bump a
   returning visitor keeps the copy they already hold and never sees the new indicator.
5. Run `python3 scripts/check_data.py`. It must print `PASS`.

No build step and no framework. Edit the JSON.

## Checking it

```bash
python3 scripts/check_data.py     # both data files, run by CI on every push
```

Every failure it guards against is quiet, which is the reason it exists:

- **A state name the geojson does not know** simply does not colour. There is no
  error and no console warning, and a map of 35 states looks finished.
- **A `national` figure outside the range of its own states** means the two were
  taken in different units or different vintages. Both render.
- **A missing `higherIsBetter`** captions the legend as though more were better.
  `null` is a deliberate third value, for indicators with no normative direction
  (fertility, density, the urban share, decadal growth), so the check accepts
  `true`, `false` and `null` and rejects only absence or a string.
- **A stale `mapId`** renders a cross-link button leading to a 404.
- **A precached path that 404s** rejects `cache.addAll`, which fails the whole
  service worker install and silently leaves the site with no offline layer.
- **Counts written in prose** (205 maps, 16 indicators) go stale the first time
  one is added, in three files.

Four of those were fault-injected against a real failure on 2026-09-22 to confirm
they bite rather than pass vacuously.

CI also re-runs `scripts/build_map_pages.py` and fails if `m/` or `sitemap.xml`
differs from what it generates, so a map cannot be added to the catalogue without
its page.

## Where the MoSPI figures come from

`flfpr` and `litgap` were pulled from the MoSPI open data API (`api.mospi.gov.in`,
`GENDER` dataset) on 2026-09-22 and carry a `retrieved` date for that reason.

Two things to know before refreshing them. The host negotiates TLS in a way
OpenSSL 3 rejects by default: a plain `curl` fails with *unsafe legacy
renegotiation disabled*, and a Python client needs `ctx.options |= 0x4`
(`OP_LEGACY_SERVER_CONNECT`, which is unnamed before Python 3.12) before it will
connect at all. And the REST paths are not published in the portal's own bundle,
so the practical way to re-pull is the MoSPI MCP tooling rather than a script
in this repository. That is why the values are committed here rather than
fetched at build time.

## Localization (Hindi and beyond)

The site ships an English/Hindi toggle in the common header. It uses a light
`data-i18n` system (`assets/common-header.js`): any element with a
`data-i18n="some.key"` attribute is translated from a dictionary, and
`window.IM.setLang('hi'|'en')` flips the language (persisted in `im-lang`,
also sets `<html lang>` and fires an `im:langchange` event).

Currently translated:
- The navigation and the interactive tool's chrome (tabs, labels, headings).
- **All 16 interactive indicators** (`name_hi`, `desc_hi`, `unit_hi`).
- **All 205 maps** — every map has `title_hi` + `takeaway_hi`, and every section
  title has a Hindi form. Numbers, ratios and state names are preserved.

To translate additional content (e.g. per-map static pages, policy notes):

1. Add parallel `_hi` fields to the data, e.g. `"name_hi"`, `"desc_hi"` in
   `interactive-data.json`, or `"title_hi"` / `"takeaway_hi"` in `maps.json`.
2. In the rendering code, pick the field by `window.IM.lang` (fall back to the
   English field when the `_hi` value is missing).
3. For static page copy, add `data-i18n` attributes and register strings via
   `window.IM_I18N` before `common-header.js` loads (see `explore.html`).

This keeps translation incremental — partial coverage degrades gracefully to
English rather than breaking.
