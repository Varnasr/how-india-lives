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
