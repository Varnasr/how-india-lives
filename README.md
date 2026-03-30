# How India Lives

**205 state-level choropleth maps and 10 visual stories showcasing India's diversity across demography, health, gender, economy, education, environment, and more.**

A storytelling-first visual atlas for understanding why India's states are different — and why it matters for policy. Part of [ImpactMojo](https://impactmojo.in).

> Kerala's life expectancy (77 years) exceeds Chhattisgarh's (64) by 13 years. Bihar's female labour force participation is 10x lower than Himachal Pradesh's. Rajasthan is 60% vegetarian; Bengal is under 5%. India is not one country when it comes to development outcomes.

**Live site:** [howindialives.impactmojo.in](https://howindialives.impactmojo.in)

---

## What This Is

These 205 maps make India's development diversity visible — one indicator at a time, across all 28 states and 8 union territories. Policy debates in India often assume national averages. But an average of Kerala and Bihar is a fiction that helps no one.

This project arms educators, journalists, students, and policymakers with the visual proof that context-specific policy design is not a luxury — it's a necessity.

## Features

### Discovery & Navigation
- **Featured rotating map spotlight** in hero — curated maps auto-rotate every 8s
- **Research question pills** — "Why are states so different?", "Where do women have least autonomy?" etc. instead of database-style filters
- **Search autocomplete** — type 2+ characters to see matching maps in a dropdown; searches titles, tags, sources, and takeaway statistics
- **"Surprise Me" button** — opens a random map
- **Deep links** — share any map directly via `#map/S00a` URL
- **Keyboard navigation** — arrow keys to browse maps in detail modal

### Storytelling
- **10 curated visual stories** — scroll-driven narratives like "India's North-South Divide in 7 Maps", "The Gender Gap", "What India Eats"
- **6 story thread collections** on the main page with editorial framing
- **Map of the Week** — deterministic weekly rotation with featured banner
- **Editorial section layout** — lead card + supporting grid per section, not flat database dump
- **Show fewer / expand** — 3 cards per section by default, "Show all" to reveal the rest

### State Explorer
- **State profile view** — pick any of 37 states/UTs, see maps that mention that state prioritised
- **Compare two states** — "Kerala vs Bihar" style comparison, maps mentioning both states surfaced first

### Sharing & Citation
- **WhatsApp share** — per map and per story, with prefilled context
- **Shareable story cards** — generates branded 1200x630 PNG for social media using Canvas API
- **Cite this map** — one-click formatted citation (title, source, year, URL, access date)
- **Embed widget** — copies iframe embed code to clipboard
- **Map annotations** — add a personal note and share annotated text + link

### Technical
- **Dark/light mode** with system preference detection and localStorage persistence
- **Mobile-first responsive** — compact hero, swipe gestures, touch-friendly throughout
- **PWA / offline support** — service worker caches HTML, JSON, and fonts
- **Print stylesheet** — clean 2-column layout for classroom printing
- **No dependencies** — pure vanilla HTML/CSS/JS, no build process, no frameworks
- **Newsletter signup** — email capture in footer (ready for Mailchimp/Buttondown integration)

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

## Stories

| # | Story | Maps |
|---|-------|------|
| 1 | India's North-South Divide | 7 |
| 2 | The Gender Gap: What It Means to Be a Woman | 7 |
| 3 | Where Bihar Falls Behind — and Why | 6 |
| 4 | What India Eats: Food as Cultural Geography | 6 |
| 5 | Does Caste Still Shape Life Outcomes? | 6 |
| 6 | India's Climate Map: Heat, Water, Vulnerability | 6 |
| 7 | Is India's Democracy Equally Healthy? | 6 |
| 8 | The Digital Divide | 5 |
| 9 | Who Gets the Safety Net? | 5 |
| 10 | How Faith Maps Onto Geography | 5 |

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
├── stories.html          # 10 scroll-driven visual stories
├── methodology.html      # Data sources, quality flags, limitations
├── manifest.json         # PWA manifest
├── sw.js                 # Service worker for offline support
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
- [ ] **Interactive maps** — Hover-based tooltips with state values
- [ ] **Data download** — CSV/JSON exports for each indicator
- [ ] **Community contributions** — Open pipeline for adding new indicators
- [ ] **Accessibility audit** — WCAG 2.1 AA compliance
- [x] ~~Comparison mode~~ — Compare two states side by side
- [x] ~~Embed API~~ — Embed individual maps via iframe
- [x] ~~PWA support~~ — Offline access for fieldworkers

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding maps, fixing bugs, translating content, and improving documentation.

## Credits

Data work by **Varna**

Part of [ImpactMojo](https://impactmojo.in) — Free development education for South Asia

## License

[CC BY-NC-SA 4.0](LICENSE) — Maps are pedagogical tools designed for facilitated discussion. For policy or academic citation, consult the underlying source publications directly.
