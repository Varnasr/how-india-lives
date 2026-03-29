# How India Lives

**205 state-level choropleth maps showcasing India's diversity across demography, health, gender, economy, education, environment, and more.**

A visual atlas for understanding why India's states are different — and why it matters for policy. Part of [ImpactMojo](https://impactmojo.in).

> Kerala's life expectancy (77 years) exceeds Chhattisgarh's (64) by 13 years. Bihar's female labour force participation is 10x lower than Himachal Pradesh's. Rajasthan is 60% vegetarian; Bengal is under 5%. India is not one country when it comes to development outcomes.

**Live site:** [howindialives.impactmojo.in](https://howindialives.impactmojo.in)

---

## What This Is

These 205 maps make India's development diversity visible — one indicator at a time, across all 28 states and 8 union territories. Policy debates in India often assume national averages. But an average of Kerala and Bihar is a fiction that helps no one.

This project arms educators, journalists, students, and policymakers with the visual proof that context-specific policy design is not a luxury — it's a necessity.

## Features

- **205 choropleth maps** across 12 themes
- **Dark/light mode** with system preference detection
- **Search and filter** by keyword, data source, or quality flag
- **Detail modal** — click any card to see the full map, key takeaway, policy implication, tags, and download option
- **Ctrl+K overlay** — project explainer accessible via keyboard shortcut
- **Mobile-responsive** — pill-style tab navigation, single-column cards, touch-friendly
- **Map downloads** with CC BY-NC-SA 4.0 license attribution

## Themes

| # | Theme | Maps | Examples |
|---|-------|------|----------|
| 1 | Demography | 13 | Median age, sex ratio, urbanisation |
| 2 | Food & Culture | 15 | Vegetarianism, alcohol, tobacco, newspaper readership |
| 3 | Economy | 42 | Poverty, informal workforce, digital access, MGNREGA |
| 4 | Health | 30 | Life expectancy, stunting, mental health, out-of-pocket spend |
| 5 | Gender | 23 | Female labour, domestic violence, women's autonomy |
| 6 | Caste | 10 | SC/ST population, atrocity rates, reservation |
| 7 | Religion | 10 | Religious composition and diversity |
| 8 | Education | 13 | Literacy, dropout rates, pupil-teacher ratio |
| 9 | Environment | 15 | Forest cover, air quality, groundwater, night lights |
| 10 | Democracy | 13 | Voter turnout, women MLAs, fact-checking coverage |
| 11 | Social Protection | 10 | MGNREGA, Jal Jeevan, PMFBY, ration cards |
| 12 | Reproductive Choices | 11 | Contraception, sterilisation, unmet need |

## Data Sources

| Source | Coverage | Maps |
|--------|----------|------|
| NFHS-5 (2019-21) | Health, demographics, gender, reproductive | ~80 |
| Census of India (2011) | Population, housing, employment | ~45 |
| PLFS (2022-23) | Employment and labour | ~15 |
| NCRB (2022) | Crime statistics | ~10 |
| Government Dashboards | MGNREGA, JJM, PMFBY, UDISE+, DPIIT | ~20 |
| Other | IMD, CGWB, FSI, ECI, ADR, TRAI, RBI, NASA VIIRS, Pew | ~35 |

Full methodology: [methodology.html](https://howindialives.impactmojo.in/methodology.html)

## Project Structure

```
how-india-lives/
├── index.html            # Main gallery (HTML + CSS + JS, single file)
├── methodology.html      # Data sources, quality flags, limitations
├── data/
│   └── maps.json         # Catalog of all 205 maps with metadata
├── maps/
│   ├── demography/       # 13 maps
│   ├── food-and-culture/ # 15 maps
│   ├── economy/          # 42 maps
│   ├── health/           # 30 maps
│   ├── gender/           # 23 maps
│   ├── caste/            # 10 maps
│   ├── religion/         # 10 maps
│   ├── education/        # 13 maps
│   ├── environment/      # 15 maps
│   ├── democracy/        # 13 maps
│   ├── social-protection/# 10 maps
│   └── reproductive-choices/ # 11 maps
├── docs/                 # GitBook-style documentation
├── LICENSE               # CC BY-NC-SA 4.0
├── CONTRIBUTING.md       # Contributor guidelines
└── CNAME                 # Custom domain config
```

## How Maps Were Made

Rendered programmatically with **Python 3 + GeoPandas + Matplotlib** using Natural Earth 10m shapefiles. Each map includes:
- State-level choropleth with two-letter abbreviations
- Northeast India inset panel
- Shock statistic (red box, top right)
- National average marker on colourbar
- Source and year citation

## Roadmap

- [ ] **Translations** — Hindi and regional language support for takeaways
- [ ] **District-level maps** — Move beyond state-level where data permits
- [ ] **Time series** — Show how indicators have changed over time
- [ ] **Comparison mode** — Side-by-side state comparisons
- [ ] **Embed API** — Let others embed individual maps on their sites
- [ ] **Data download** — CSV/JSON exports for each indicator
- [ ] **Interactive maps** — Hover-based tooltips with state values
- [ ] **Community contributions** — Open pipeline for adding new indicators
- [ ] **Accessibility audit** — WCAG 2.1 AA compliance
- [ ] **PWA support** — Offline access for fieldworkers

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding maps, fixing bugs, translating content, and improving documentation.

## Credits

Data work by **Varna**

Part of [ImpactMojo](https://impactmojo.in) — Free development education for South Asia

## License

[CC BY-NC-SA 4.0](LICENSE) — Maps are pedagogical tools designed for facilitated discussion. For policy or academic citation, consult the underlying source publications directly.
