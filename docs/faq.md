# Frequently Asked Questions

## Can I use these maps in my presentation/article/report?

Yes! Maps are licensed under CC BY-NC-SA 4.0. You can use them for non-commercial purposes with attribution. Credit "How India Lives / ImpactMojo" and link to the site.

For academic or policy citations, always cite the **original data source** (NFHS-5, Census, etc.), not our maps.

## Why state-level? Districts would be more useful.

Agreed. District-level maps are on the [roadmap](roadmap.md). We started with states because:
- More data sources are available at the state level
- The state-level story is already under-told
- It's a manageable starting point for 205 indicators

## Why is some data old (Census 2011)?

India's Census happens every 10 years. The 2021 Census was delayed indefinitely. For indicators like urbanisation, migration, and housing, Census 2011 remains the most recent comprehensive source.

## What do the quality flags mean?

- **BUILT**: Reliable data from large-sample official surveys
- **NEW**: Sound data, but the map was recently added — less peer review
- **UNCERTAIN**: Data quality concerns — small samples, proxy indicators, or dated sources

## How were the maps rendered?

Python 3 + GeoPandas + Matplotlib with Natural Earth 10m shapefiles. The pipeline is programmatic — each map is generated from a CSV of state-level data using a standardised script.

## Can I download the underlying data?

Not yet. Data downloads (CSV/JSON) are on the roadmap. For now, consult the original source publications listed on each map.

## How can I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md). You can add new maps, improve takeaways, translate content, fix bugs, or improve documentation.

## Why is the Northeast shown as an inset?

India's Northeastern states are geographically small but developmentally crucial. The inset panel makes them readable without requiring users to zoom in.

## Who made this?

Data work by Varna. Part of [ImpactMojo](https://impactmojo.in) — free development education for South Asia.
