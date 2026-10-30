# About the project

## Why How India Lives exists

Policy debates in India often rely on national averages. But national averages mask enormous state-level variation. An "average" of Kerala and Bihar is a fiction that describes neither state and helps no one.

**How India Lives** makes this variation visible through 259 choropleth maps and 10 curated visual stories, so that anyone discussing Indian policy can see how much the states differ.

## The core argument

India's states are so different in development outcomes that they function as separate countries for policy purposes. A policy designed for "India" will fail in most Indian states because "India" doesn't exist as a single development reality.

Examples:
- **Life expectancy**: Kerala (75.1 years) vs Chhattisgarh (64.6 years) in the SRS life tables for 2019-23, a gap of more than 10 years
- **Female labour force participation**: Himachal Pradesh (64.7%) vs Bihar (24.7%) in PLFS 2025
- **Vegetarianism**: Rajasthan (~60%) vs Bengal (<5%)
- **Informal workforce**: Over 90% in Bihar, under 50% in government-heavy states
- **Smartphone access**: 70%+ in metros, under 25% in rural Northeast

## Design principles

1. **Storytelling first, data second**: research question pills and curated stories guide exploration in place of database-style filters
2. **One map, one story**: Each map focuses on a single indicator with a clear takeaway
3. **Shock value**: The "shock statistic" (red box) grabs attention with the most striking data point
4. **Policy connection**: Every map links the data to a policy implication
5. **Source transparency**: Every map cites its data source and year
6. **Mobile first**: Designed for phones, adapted for desktop

## Features

- **10 visual stories**: Scroll-driven narratives like "India's north-south divide" and "The gender gap"
- **State explorer**: Pick any state, see all maps that mention it
- **Compare states**: Kerala vs Bihar side-by-side
- **WhatsApp sharing**: Per map and per story with prefilled context
- **Cite and embed**: Formatted citations and iframe embed codes
- **Offline support**: PWA with service worker caching

## Technical approach

Maps are rendered programmatically with Python 3 + GeoPandas + Matplotlib using Natural Earth 10m shapefiles. The website is a plain HTML/CSS/JS static site with no frameworks, no build process and no dependencies. Data lives in a single `maps.json` catalog.

## Part of ImpactMojo

How India Lives is a project of [ImpactMojo](https://impactmojo.in), which provides free development education for South Asia.
