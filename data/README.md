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
4. Bump the cache version in `sw.js` so returning visitors pick up the change.

No build step, no framework — just edit the JSON.

## Localization (Hindi and beyond)

The site ships an English/Hindi toggle in the common header. It uses a light
`data-i18n` system (`assets/common-header.js`): any element with a
`data-i18n="some.key"` attribute is translated from a dictionary, and
`window.IM.setLang('hi'|'en')` flips the language (persisted in `im-lang`,
also sets `<html lang>` and fires an `im:langchange` event).

Currently translated: the navigation and the interactive tool's chrome
(tabs, labels, headings). **Data content** — indicator names, map titles and
takeaways — is still English. To translate content:

1. Add parallel `_hi` fields to the data, e.g. `"name_hi"`, `"desc_hi"` in
   `interactive-data.json`, or `"title_hi"` / `"takeaway_hi"` in `maps.json`.
2. In the rendering code, pick the field by `window.IM.lang` (fall back to the
   English field when the `_hi` value is missing).
3. For static page copy, add `data-i18n` attributes and register strings via
   `window.IM_I18N` before `common-header.js` loads (see `explore.html`).

This keeps translation incremental — partial coverage degrades gracefully to
English rather than breaking.
