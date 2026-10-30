# Frequently asked questions

## Can I use these maps in my presentation/article/report?

Yes! Maps are licensed under CC BY-NC-SA 4.0. You can use them for non-commercial purposes with attribution. Credit "How India Lives / ImpactMojo" and link to the site.

For academic or policy citations, use the **Cite button** in the detail modal, which copies a formatted citation. Always cite the **original data source** (NFHS-5, Census, etc.) for academic work.

## Can I embed a map on my website?

Yes. Open any map, click the **Embed** button, and paste the iframe code into your HTML. The embed auto-attributes and links back.

## Can I share a specific map?

Yes, three ways:
1. **Direct link**: every map has a URL like `howindialives.impactmojo.in/#map/S00a`
2. **WhatsApp**: use the green WhatsApp button in the detail modal
3. **Story card**: the "Share story card" button generates a branded 1200x630 PNG for social media

## What are the stories?

[Stories](https://howindialives.impactmojo.in/stories.html) are curated narratives that thread 5-7 maps into a scroll-driven visual essay. There are currently 10 stories covering topics like the North-South divide, gender gap, Bihar's development challenge, and food as cultural geography.

## How do I explore a specific state?

Click **"Explore a state"** in the hero section. Pick any of the 36 states and UTs. Maps that mention your state are prioritised. You can also compare two states using the **"Compare with..."** button.

## Why state-level? Districts would be more useful.

Agreed. District-level maps are on the [roadmap](roadmap.md). We started with states because:
- More data sources are available at the state level
- The state-level story is already under-told
- It's a manageable starting point for 259 maps

## Why is some data old (Census 2011)?

India's Census happens every 10 years. The 2021 Census was delayed indefinitely. For indicators like urbanisation, migration, and housing, Census 2011 remains the most recent comprehensive source.

## Does it work offline?

Yes. The site is a Progressive Web App (PWA). After your first visit, pages and data are cached for offline use. Useful for classrooms and fieldwork with limited connectivity.

## How were the maps rendered?

Python 3 + GeoPandas + Matplotlib with Natural Earth 10m shapefiles. The pipeline is programmatic. Each map is generated from a CSV of state-level data using a standardised script.

## Can I download the underlying data?

Yes, for the interactive atlas. Every indicator there can be downloaded as CSV or JSON, and the calculations behind derived figures are in `data/csv/`. For the static maps, consult the original source publications listed on each map.

## Can I print the maps?

Yes. Use your browser's print function (Ctrl+P). A print stylesheet strips navigation and shows all maps in a clean 2-column layout suitable for classroom handouts.

## How can I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md). You can add new maps, improve takeaways, translate content, fix bugs, or improve documentation.

## Why is the Northeast shown as an inset?

India's Northeastern states are geographically small, and their polygons are too small to label at national scale. The inset panel makes them readable without requiring users to zoom in.

## Who made this?

Data work by Varna. Part of [ImpactMojo](https://impactmojo.in), free development education for South Asia.
