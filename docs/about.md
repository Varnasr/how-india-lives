# About the Project

## Why How India Lives Exists

Policy debates in India often rely on national averages. But national averages mask enormous state-level variation. An "average" of Kerala and Bihar is a fiction that describes neither state and helps no one.

**How India Lives** makes this variation visible through 205 choropleth maps and 10 curated visual stories — so that anyone discussing Indian policy can see the actual landscape of difference.

## The Core Argument

India's states are so different in development outcomes that they function as separate countries for policy purposes. A policy designed for "India" will fail in most Indian states because "India" doesn't exist as a single development reality.

Examples:
- **Life expectancy**: Kerala (77 years) vs Chhattisgarh (64 years) — a 13-year gap
- **Female labour force participation**: Himachal Pradesh vs Bihar — a 10x difference
- **Vegetarianism**: Rajasthan (~60%) vs Bengal (<5%)
- **Informal workforce**: Over 90% in Bihar, under 50% in government-heavy states
- **Smartphone access**: 70%+ in metros, under 25% in rural Northeast

## Design Principles

1. **Storytelling first, data second** — Research question pills and curated stories guide exploration, not database-style filters
2. **One map, one story** — Each map focuses on a single indicator with a clear takeaway
3. **Shock value** — The "shock statistic" (red box) grabs attention with the most striking data point
4. **Policy connection** — Every map links the data to a policy implication
5. **Source transparency** — Every map cites its data source and year
6. **Mobile first** — Designed for phones, enhanced for desktop

## Key Features

- **10 visual stories** — Scroll-driven narratives like "India's North-South Divide" and "The Gender Gap"
- **State explorer** — Pick any state, see all maps that mention it
- **Compare states** — Kerala vs Bihar side-by-side
- **WhatsApp sharing** — Per map and per story with prefilled context
- **Cite and embed** — Formatted citations and iframe embed codes
- **Offline support** — PWA with service worker caching

## Technical Approach

Maps are rendered programmatically with Python 3 + GeoPandas + Matplotlib using Natural Earth 10m shapefiles. The website is a pure vanilla HTML/CSS/JS static site — no frameworks, no build process, no dependencies. Data lives in a single `maps.json` catalog.

## Part of ImpactMojo

How India Lives is a project of [ImpactMojo](https://impactmojo.in), which provides free development education for South Asia.
