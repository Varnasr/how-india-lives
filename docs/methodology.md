# Data Sources & Methodology

## Primary Data Sources

### NFHS-5 (2019-21) — ~80 maps
The National Family Health Survey is India's most comprehensive household survey, covering health, demographics, gender, nutrition, and reproductive health across all states and districts.

### Census of India (2011) — ~45 maps
The decennial census provides the most complete picture of India's population, housing, employment, and social composition. While dated, it remains the only source for many indicators at full geographic resolution.

### PLFS (2022-23) — ~15 maps
The Periodic Labour Force Survey by NSSO provides the most current employment and labour statistics, including workforce participation, informality, and sectoral composition.

### NCRB Crime in India (2022) — ~10 maps
The National Crime Records Bureau publishes annual crime statistics by state, including crimes against women, SC/ST atrocities, and cybercrime.

### Government Dashboards — ~20 maps
Official dashboards for flagship schemes provide near-real-time data:
- MGNREGA (employment guarantee)
- Jal Jeevan Mission (tap water)
- PMFBY (crop insurance)
- UDISE+ (school education)
- DPIIT (industrial investment)

### Other Sources — ~35 maps
- **IMD** — India Meteorological Department (climate)
- **CGWB** — Central Ground Water Board (groundwater)
- **FSI** — Forest Survey of India (forest cover)
- **ECI** — Election Commission of India (voter data)
- **ADR** — Association for Democratic Reforms (candidate data)
- **TRAI** — Telecom Regulatory Authority (digital access)
- **RBI** — Reserve Bank of India (financial data)
- **NASA VIIRS** — Night light satellite imagery
- **Pew Research** — Religious composition surveys
- **NACO** — National AIDS Control Organisation

## Quality Flags

Each map carries one of three quality flags:

| Flag | Meaning |
|------|---------|
| **BUILT** | Well-established, reliable data from official large-sample surveys |
| **NEW** | Recently added to the catalog; data is sound but the map is new |
| **UNCERTAIN** | Data quality concerns, limited sample, proxy indicators, or dated source |

## Map Rendering Pipeline

1. Data is compiled into a state-level CSV for each indicator
2. GeoPandas reads Natural Earth 10m shapefiles for India's boundaries
3. Matplotlib renders the choropleth with a sequential or diverging colormap
4. Each map includes:
   - State-level colour shading
   - Two-letter state abbreviations
   - Northeast India inset panel (for readability)
   - "Shock statistic" (red box, top right corner)
   - National average marker on the colourbar
   - Source, year, and data citation

## Limitations

- **Temporal mismatch**: Maps combine data from 2011 (Census) to 2024 (dashboards). Comparisons across maps with different years should be made cautiously.
- **State boundaries**: Some indicators predate the creation of newer states/UTs (e.g., Ladakh, J&K reorganisation).
- **Small states/UTs**: Sample sizes for small UTs (Lakshadweep, D&NH, etc.) may be unreliable even in NFHS.
- **No district data**: All maps are state-level. District-level variation (often larger) is not captured.
- **Static snapshots**: Maps show a single point in time. Trends and trajectories are not visible.
