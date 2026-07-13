#!/usr/bin/env python3
"""
Generate static, crawlable, shareable pages for each map plus a sitemap.

Reads:  data/maps.json, data/interactive-data.json
Writes: m/<id>.html (one per map), m/index.html (crawlable index),
        sitemap.xml, robots.txt

Each per-map page carries its own <title>, meta description, canonical URL and
Open Graph / Twitter image (the map PNG) so it previews and indexes on its own,
while linking back into the single-page interactive atlas.

Run from the repo root:  python3 scripts/build_map_pages.py
No dependencies. Re-run whenever data/maps.json changes.
"""
import json, os, html
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://howindialives.impactmojo.in"
SECTION_TITLES = {
    'demography': 'Demography', 'food-and-culture': 'Food & Culture', 'economy': 'Economy',
    'health': 'Health', 'gender': 'Gender', 'caste': 'Caste', 'religion': 'Religion',
    'education': 'Education', 'environment': 'Environment', 'democracy': 'Democracy',
    'social-protection': 'Social Protection', 'reproductive-choices': 'Reproductive Choices',
}

def esc(s):
    return html.escape(str(s or ''), quote=True)

def img_url(m, absolute=False):
    path = "/maps/%s/%s" % (m['section'], quote(m['file']))
    return (BASE + path) if absolute else path

def page(m, interactive_id):
    title = m['title']
    desc = m.get('takeaway') or ('%s across India\'s states.' % title)
    sect = SECTION_TITLES.get(m['section'], m['section'])
    canonical = "%s/m/%s.html" % (BASE, m['id'])
    og_img = img_url(m, absolute=True)
    interactive_btn = ''
    if interactive_id:
        interactive_btn = ('<a class="btn" href="/explore.html#%s">Explore interactively '
                           '<span aria-hidden="true">&rarr;</span></a>' % esc(interactive_id))
    policy = ''
    if m.get('policy'):
        policy = '<div class="policy"><strong>Policy implication</strong><br>%s</div>' % esc(m['policy'])
    tags = ''
    if m.get('tags'):
        tags = ''.join('<span class="tag">%s</span>' % esc(t) for t in m['tags'])
    schema = {
        "@context": "https://schema.org", "@type": "ImageObject",
        "name": title, "caption": desc, "contentUrl": og_img,
        "creditText": "%s (%s)" % (m.get('source', ''), m.get('year', '')),
        "isPartOf": {"@type": "WebSite", "name": "How India Lives", "url": BASE},
        "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    }
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} &mdash; How India Lives | ImpactMojo</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title} &mdash; How India Lives">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#0EA5E9">
<link href="https://www.impactmojo.in/assets/images/favicon.png" rel="icon" type="image/png">
<link href="https://fonts.googleapis.com/css2?family=Amaranth:wght@400;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link href="/assets/common-header.css" rel="stylesheet">
<script>(function(){{var s=localStorage.getItem('im-theme');if(s==='dark'||(!s&&window.matchMedia('(prefers-color-scheme:dark)').matches))document.documentElement.setAttribute('data-theme','dark');}})();</script>
<script type="application/ld+json">{schema}</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#fff;--sec:#F8FAFC;--tx:#0F172A;--tx2:#475569;--mut:#94A3B8;--acc:#0EA5E9;--bd:#E2E8F0;--card:#fff}}
html[data-theme="dark"]{{--bg:#0F172A;--sec:#1E293B;--tx:#F1F5F9;--tx2:#CBD5E1;--mut:#64748B;--acc:#38BDF8;--bd:#334155;--card:#1E293B}}
body{{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--tx);line-height:1.6}}
.wrap{{max-width:820px;margin:0 auto;padding:84px 20px 60px}}
.crumb{{font-size:.78rem;color:var(--mut);margin-bottom:6px}}
.crumb a{{color:var(--acc);text-decoration:none}}
h1{{font-family:'Amaranth',sans-serif;font-size:clamp(1.5rem,5vw,2rem);margin:6px 0 14px}}
.mapimg{{width:100%;border:1px solid var(--bd);border-radius:14px;background:var(--card);display:block}}
.takeaway{{border-left:3px solid var(--acc);background:var(--sec);padding:14px 18px;border-radius:0 10px 10px 0;margin:20px 0;font-size:1.05rem}}
.policy{{background:var(--sec);border:1px solid var(--bd);border-radius:10px;padding:14px 18px;margin:14px 0;color:var(--tx2);font-size:.92rem}}
.meta{{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}}
.tag{{font-size:.74rem;font-weight:600;color:var(--tx2);background:var(--sec);border:1px solid var(--bd);border-radius:999px;padding:3px 11px}}
.btns{{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 10px}}
.btn{{font-weight:600;font-size:.9rem;text-decoration:none;padding:11px 18px;border-radius:10px;background:var(--acc);color:#fff}}
.btn.ghost{{background:var(--card);color:var(--tx2);border:1px solid var(--bd)}}
.src{{font-size:.82rem;color:var(--mut);margin-top:10px}}
.credit{{font-size:.72rem;color:var(--mut);margin-top:26px;border-top:1px solid var(--bd);padding-top:14px}}
.credit a{{color:var(--acc)}}
</style>
</head>
<body>
<div id="im-common-header"></div>
<div class="wrap">
  <nav class="crumb"><a href="/index.html">Atlas</a> &rsaquo; <a href="/index.html#{section}">{sect}</a></nav>
  <h1>{title}</h1>
  <img class="mapimg" src="{img}" alt="Choropleth map of India by state: {title}. {desc}" width="1200" height="900">
  {takeaway}
  {policy}
  <div class="meta"><span class="tag">{source} {year}</span><span class="tag">{sect}</span>{tags}</div>
  <div class="btns">
    <a class="btn" href="/index.html#map/{id}">Open in the interactive atlas <span aria-hidden="true">&rarr;</span></a>
    {interactive_btn}
    <a class="btn ghost" href="/m/index.html">All 205 maps</a>
  </div>
  <p class="src">Source: {source}{year_paren}. See the <a href="/methodology.html" style="color:var(--acc)">methodology</a> for notes and limitations.</p>
  <p class="credit">Part of <a href="https://www.impactmojo.in">ImpactMojo</a>. Maps are pedagogical tools for facilitated discussion, not standalone data references. <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>.</p>
</div>
<script src="/assets/common-header.js" defer></script>
</body>
</html>
""".format(
        title=esc(title), desc=esc(desc), canonical=canonical, og_img=og_img,
        schema=json.dumps(schema), section=esc(m['section']), sect=esc(sect),
        img=img_url(m),
        takeaway=('<div class="takeaway">%s</div>' % esc(m['takeaway'])) if m.get('takeaway') else '',
        policy=policy, source=esc(m.get('source', '')), year=esc(m.get('year', '')),
        year_paren=(' (%s)' % esc(m['year'])) if m.get('year') else '', tags=tags,
        id=esc(m['id']), interactive_btn=interactive_btn,
    )

def index_page(maps):
    by_sec = {}
    for m in maps:
        by_sec.setdefault(m['section'], []).append(m)
    blocks = []
    for sec, title in SECTION_TITLES.items():
        items = by_sec.get(sec, [])
        if not items:
            continue
        lis = ''.join('<li><a href="/m/%s.html">%s</a></li>' % (esc(m['id']), esc(m['title'])) for m in items)
        blocks.append('<section id="%s"><h2>%s <small>(%d)</small></h2><ul>%s</ul></section>' % (esc(sec), esc(title), len(items), lis))
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>All 205 maps &mdash; How India Lives | ImpactMojo</title>
<meta name="description" content="A complete, browsable index of all 205 state-level maps of India across demography, health, gender, economy, education, environment and more.">
<link rel="canonical" href="{base}/m/index.html">
<meta name="theme-color" content="#0EA5E9">
<link href="https://www.impactmojo.in/assets/images/favicon.png" rel="icon" type="image/png">
<link href="https://fonts.googleapis.com/css2?family=Amaranth:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="/assets/common-header.css" rel="stylesheet">
<script>(function(){{var s=localStorage.getItem('im-theme');if(s==='dark'||(!s&&window.matchMedia('(prefers-color-scheme:dark)').matches))document.documentElement.setAttribute('data-theme','dark');}})();</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#fff;--tx:#0F172A;--tx2:#475569;--mut:#94A3B8;--acc:#0EA5E9;--bd:#E2E8F0}}
html[data-theme="dark"]{{--bg:#0F172A;--tx:#F1F5F9;--tx2:#CBD5E1;--mut:#64748B;--acc:#38BDF8;--bd:#334155}}
body{{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--tx);line-height:1.6}}
.wrap{{max-width:900px;margin:0 auto;padding:84px 20px 60px}}
h1{{font-family:'Amaranth',sans-serif;font-size:2rem;margin-bottom:6px}}
.lead{{color:var(--tx2);margin-bottom:24px}}
section{{margin:26px 0}}
h2{{font-size:1.15rem;border-bottom:1px solid var(--bd);padding-bottom:8px;margin-bottom:10px}}
h2 small{{color:var(--mut);font-weight:500}}
ul{{list-style:none;columns:2;column-gap:28px}}
@media(max-width:600px){{ul{{columns:1}}}}
li{{margin:5px 0;break-inside:avoid}}
li a{{color:var(--tx2);text-decoration:none;font-size:.9rem}}
li a:hover{{color:var(--acc)}}
</style></head>
<body>
<div id="im-common-header"></div>
<div class="wrap">
  <h1>All 205 maps</h1>
  <p class="lead">Every state-level map in the atlas, by theme. Open the <a href="/index.html" style="color:var(--acc)">interactive gallery</a> to search and filter.</p>
  {blocks}
</div>
<script src="/assets/common-header.js" defer></script>
</body></html>
""".format(base=BASE, blocks='\n'.join(blocks))

def main():
    maps = json.load(open(os.path.join(ROOT, 'data', 'maps.json')))
    inter = {}
    try:
        idata = json.load(open(os.path.join(ROOT, 'data', 'interactive-data.json')))
        for ind in idata.get('indicators', []):
            if ind.get('mapId'):
                inter[ind['mapId']] = ind['id']
    except FileNotFoundError:
        pass

    outdir = os.path.join(ROOT, 'm')
    os.makedirs(outdir, exist_ok=True)
    written = 0
    for m in maps:
        if not m.get('file'):
            continue
        with open(os.path.join(outdir, '%s.html' % m['id']), 'w') as f:
            f.write(page(m, inter.get(m['id'])))
        written += 1
    with open(os.path.join(outdir, 'index.html'), 'w') as f:
        f.write(index_page([m for m in maps if m.get('file')]))

    # sitemap
    urls = ['/', '/explore.html', '/stories.html', '/methodology.html', '/m/index.html']
    urls += ['/m/%s.html' % m['id'] for m in maps if m.get('file')]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append('  <url><loc>%s%s</loc></url>' % (BASE, u))
    sm.append('</urlset>')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
        f.write('\n'.join(sm) + '\n')
    with open(os.path.join(ROOT, 'robots.txt'), 'w') as f:
        f.write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE)

    print("Wrote %d map pages + m/index.html + sitemap.xml (%d urls) + robots.txt" % (written, len(urls)))

if __name__ == '__main__':
    main()
