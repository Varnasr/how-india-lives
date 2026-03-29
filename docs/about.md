# About the Project

## Why How India Lives Exists

Policy debates in India often rely on national averages. But national averages mask enormous state-level variation. An "average" of Kerala and Bihar is a fiction that describes neither state and helps no one.

**How India Lives** makes this variation visible through 205 choropleth maps — one indicator at a time — so that anyone discussing Indian policy can see the actual landscape of difference.

## The Core Argument

India's states are so different in development outcomes that they function as separate countries for policy purposes. A policy designed for "India" will fail in most Indian states because "India" doesn't exist as a single development reality.

Examples:
- **Life expectancy**: Kerala (77 years) vs Chhattisgarh (64 years) — a 13-year gap
- **Female labour force participation**: Himachal Pradesh vs Bihar — a 10x difference
- **Vegetarianism**: Rajasthan (~60%) vs Bengal (<5%)
- **Informal workforce**: Over 90% in Bihar, under 50% in government-heavy states
- **Smartphone access**: 70%+ in metros, under 25% in rural Northeast

## Design Principles

1. **One map, one story** — Each map focuses on a single indicator with a clear takeaway
2. **Shock value** — The "shock statistic" (red box) grabs attention with the most striking data point
3. **Policy connection** — Every map links the data to a policy implication
4. **Source transparency** — Every map cites its data source and year
5. **Quality honesty** — Maps are flagged as BUILT, NEW, or UNCERTAIN

## Technical Approach

Maps are rendered programmatically with Python 3 + GeoPandas + Matplotlib using Natural Earth 10m shapefiles. This means:
- Consistent styling across all 205 maps
- Reproducible pipeline (any map can be regenerated)
- Easy to add new indicators
- Northeast India inset panel for readability

## Part of ImpactMojo

How India Lives is a project of [ImpactMojo](https://impactmojo.in), which provides free development education for South Asia.
