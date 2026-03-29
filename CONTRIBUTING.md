# Contributing to How India Lives

Thank you for your interest in contributing! This project aims to make India's state-level development diversity visible through data and maps.

## How You Can Help

### Add New Maps
- Identify an indicator with reliable state-level data
- Add it to `data/maps.json` following the existing schema
- Generate the choropleth PNG using the Python pipeline (GeoPandas + Matplotlib)
- Place the image in the appropriate `maps/<theme>/` directory

### Improve Data Quality
- Flag inaccurate takeaways or outdated sources by opening an issue
- Suggest better data sources for existing maps
- Help verify quality flags (`BUILT`, `NEW`, `UNCERTAIN`)

### Fix Bugs & Improve UX
- Mobile responsiveness issues
- Accessibility improvements
- Performance optimizations
- Browser compatibility

### Translate
- Help translate takeaways and policy notes into Hindi and regional languages
- Suggest multilingual UI support improvements

### Write Documentation
- Improve methodology explanations
- Add context to specific themes
- Help build out the docs/ site

## Map Data Schema

Each map entry in `data/maps.json` follows this structure:

```json
{
  "id": "S01a",
  "title": "Indicator Name",
  "file": "S01a_Indicator_Name.png",
  "section": "theme-slug",
  "source": "Data Source",
  "year": "2021",
  "quality": "BUILT",
  "takeaway": "One-line insight about what the map reveals.",
  "policy": "Why this matters for policy.",
  "tags": ["keyword1", "keyword2"]
}
```

### Quality Flags
- **BUILT** — Well-established, reliable data from official surveys
- **NEW** — Recently added; data is sound but map is new to the catalog
- **UNCERTAIN** — Data quality concerns, limited coverage, or proxy indicators

### Section Slugs
`demography`, `food-and-culture`, `economy`, `health`, `gender`, `caste`, `religion`, `education`, `environment`, `democracy`, `social-protection`, `reproductive-choices`

## Development Setup

This is a static site — no build step required.

1. Clone the repo: `git clone https://github.com/Varnasr/how-india-lives.git`
2. Open `index.html` in a browser (or use a local server)
3. Edit files directly — HTML, CSS, and JS are all in `index.html`
4. Map data lives in `data/maps.json`

## Pull Request Guidelines

1. One feature or fix per PR
2. Test on mobile (Chrome DevTools device mode is fine)
3. If adding a map, include the PNG and the JSON entry
4. Write a clear PR description explaining *why* not just *what*

## Code of Conduct

Be respectful. This is a pedagogical project for public good. We welcome contributors of all backgrounds and experience levels.

## Questions?

Open a [GitHub Discussion](https://github.com/Varnasr/how-india-lives/discussions) or file an issue.
