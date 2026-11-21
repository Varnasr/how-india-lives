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
    'demography': 'Demography', 'food-and-culture': 'Food & culture', 'economy': 'Economy',
    'health': 'Health', 'gender': 'Gender', 'caste': 'Caste', 'religion': 'Religion',
    'education': 'Education', 'environment': 'Environment', 'democracy': 'Democracy',
    'social-protection': 'Social protection', 'reproductive-choices': 'Reproductive choices',
}
SECTION_TITLES_HI = {
    'demography': 'जनसांख्यिकी', 'food-and-culture': 'भोजन और संस्कृति', 'economy': 'अर्थव्यवस्था',
    'health': 'स्वास्थ्य', 'gender': 'लैंगिक', 'caste': 'जाति', 'religion': 'धर्म',
    'education': 'शिक्षा', 'environment': 'पर्यावरण', 'democracy': 'लोकतंत्र',
    'social-protection': 'सामाजिक सुरक्षा', 'reproductive-choices': 'प्रजनन विकल्प',
}

def esc(s):
    return html.escape(str(s or ''), quote=True)

def img_url(m, absolute=False):
    path = "/maps/%s/%s" % (m['section'], quote(m['file']))
    return (BASE + path) if absolute else path

def served_url(map_id):
    """The address that answers 200. Netlify pretty URLs 301 /m/X166.html to
    /m/x166 (lowercase), so the canonical and the sitemap use that form."""
    return "%s/m/%s" % (BASE, map_id.lower())


# The look of these pages lives in assets/site.css (the .mp rules), shared with
# the rest of the site. The template carries structure only, so a change to the
# design is one stylesheet and no regeneration of 259 files.
HEAD_COMMON = """<meta name="theme-color" content="#F8F6F1">
<link href="https://www.impactmojo.in/assets/images/favicon.png" rel="icon" type="image/png">
<link href="https://fonts.googleapis.com" rel="preconnect">
<link crossorigin href="https://fonts.gstatic.com" rel="preconnect">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="/assets/tokens.css" rel="stylesheet">
<link href="/assets/common-header.css" rel="stylesheet">
<script>(function(){{var s=localStorage.getItem('im-theme');if(s==='dark'||(!s&&window.matchMedia('(prefers-color-scheme:dark)').matches))document.documentElement.setAttribute('data-theme','dark');}})();</script>"""

FOOT = """<footer class="site-footer">
  <p>Need help setting out your story, what sets your work apart, the context, the return on investment and the projections? Pinpoint Ventures can help. Write to <a href="mailto:hello@pinpointventures.in?subject=Enquiry%20from%20howindialives.impactmojo.in">hello@pinpointventures.in</a> or message on <a href="https://wa.me/919871777110?text=Hi%20Pinpoint%20Ventures%2C%20I%20found%20you%20through%20howindialives.impactmojo.in.%20I%27d%20like%20to%20discuss%20a%20research%20or%20advisory%20engagement." target="_blank" rel="noopener">WhatsApp</a>.</p>
</footer>
<script src="/assets/common-header.js" defer></script>
<script src="/assets/dyslexia-font.js" data-accent="var(--im-accent)" data-radius="2px" defer></script>"""


def pager_link(m, label, cls):
    if not m:
        return '<span></span>'
    return '<a class="%s" href="/m/%s.html"><small>%s</small><b>%s</b></a>' % (cls, esc(m['id']), label, esc(m['title']))


def page(m, interactive_id, prev=None, nxt=None):
    title = m['title']
    desc = m.get('takeaway') or ('%s across India\'s states.' % title)
    sect = SECTION_TITLES.get(m['section'], m['section'])
    canonical = served_url(m['id'])
    og_img = img_url(m, absolute=True)
    interactive_btn = ''
    if interactive_id:
        interactive_btn = ('<a class="mp-btn" href="/explore.html#%s">Explore interactively '
                           '<span aria-hidden="true">&rarr;</span></a>' % esc(interactive_id))
    policy = ''
    if m.get('policy'):
        policy = '<section class="mp-block"><h2>Policy implication</h2><p>%s</p></section>' % esc(m['policy'])
    tags = ''
    if m.get('tags'):
        tags = '<div><dt>Tags</dt><dd>%s</dd></div>' % ' &middot; '.join(esc(t) for t in m['tags'])
    schema = {
        "@context": "https://schema.org", "@type": "ImageObject",
        "name": title, "caption": desc, "contentUrl": og_img,
        "creditText": "%s (%s)" % (m.get('source', ''), m.get('year', '')),
        "isPartOf": {"@type": "WebSite", "name": "How India Lives", "url": BASE},
        "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    }
    # Bilingual: swap the visible title/takeaway/section to Hindi when IM.lang === 'hi'
    swap_script = ''
    if m.get('title_hi') or m.get('takeaway_hi'):
        hi = json.dumps({
            'title': m.get('title_hi', ''),
            'takeaway': m.get('takeaway_hi', ''),
            'section': SECTION_TITLES_HI.get(m['section'], ''),
        }, ensure_ascii=False).replace('</', '<\\/')
        swap_script = (
            '<script>(function(){var HI=' + hi + ';'
            'function a(){var h=window.IM&&IM.lang==="hi";'
            '["title","takeaway","section"].forEach(function(k){'
            'var e=document.getElementById("pm-"+k);if(!e||!HI[k])return;'
            'e.textContent=h?HI[k]:e.getAttribute("data-en");});'
            'document.documentElement.lang=h?"hi":"en";}'
            'window.addEventListener("im:langchange",a);'
            'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",a);else a();'
            '})();</script>'
        )
    srcyear_ = esc(m.get('source', '') if str(m.get('year', '')) in m.get('source', '') else (m.get('source', '') + ' ' + str(m.get('year', ''))).strip())
    return ("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | How India Lives | ImpactMojo</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title} | How India Lives">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
""" + HEAD_COMMON + """
<script type="application/ld+json">{schema}</script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}</style>
<link href="/assets/site.css" rel="stylesheet">
</head>
<body>
<div id="im-common-header"></div>
<main class="mp">
  <nav class="crumb" aria-label="Breadcrumb"><a href="/index.html">Atlas</a> <span aria-hidden="true">/</span> <a id="pm-section" data-en="{sect}" href="/index.html#{section}">{sect}</a></nav>
  <h1 id="pm-title" data-en="{title}">{title}</h1>
  {takeaway}
  <figure class="mp-figure">
    <a href="{img}"><img src="{img}" alt="Choropleth map of India by state: {title}. {desc}" width="3052" height="1725" fetchpriority="high"></a>
    <figcaption><span>{srcyear}</span><a href="{img}">Open the full-size image</a></figcaption>
  </figure>
  <div class="mp-cols">
    <div>
      {policy}
      <section class="mp-block">
        <h2>Go further</h2>
        <div class="mp-actions">
          <a class="mp-btn primary" href="/index.html#map/{id}">Open in the interactive atlas <span aria-hidden="true">&rarr;</span></a>
          {interactive_btn}
          <a class="mp-btn" href="/m/index.html">All 259 maps</a>
        </div>
      </section>
    </div>
    <section class="mp-block">
      <h2>About this map</h2>
      <dl class="mp-facts">
        <div><dt>Source</dt><dd>{source}{year_paren}</dd></div>
        <div><dt>Theme</dt><dd>{sect}</dd></div>
        <div><dt>Data vintage</dt><dd>{vintage}{newer}</dd></div>
        {data_note}
        {tags}
      </dl>
      <p class="mp-credit src">See the <a href="/methodology.html">methodology</a> for notes and limitations.</p>
    </section>
  </div>
  <nav class="mp-pager" aria-label="More maps">
    {prev}
    {next}
  </nav>
  <p class="mp-credit">Part of <a href="https://www.impactmojo.in">ImpactMojo</a>. Maps are pedagogical tools for facilitated discussion. For figures to cite, use the source publications. <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>.</p>
</main>
""" + FOOT + """
{swap_script}
</body>
</html>
""").format(
        title=esc(title), desc=esc(desc), canonical=canonical, og_img=og_img,
        schema=json.dumps(schema), section=esc(m['section']), sect=esc(sect),
        img=img_url(m),
        takeaway=('<p class="mp-lead" id="pm-takeaway" data-en="%s">%s</p>' % (esc(m['takeaway']), esc(m['takeaway']))) if m.get('takeaway') else '',
        policy=policy, source=esc(m.get('source', '')), srcyear=srcyear_,
        year_paren=(' (%s)' % esc(m['year'])) if m.get('year') else '', tags=tags,
        swap_script=swap_script, vintage=esc(vintage(m)[1]),
        data_note=('<div><dt>Data note</dt><dd>%s</dd></div>' % esc(m['data_note'])) if m.get('data_note') else '',
        newer=(' <a href="/explore.html#%s">See the newer figures for this measure in the interactive atlas.</a>' % m['newer']) if m.get('newer') else '',
        id=esc(m['id']), interactive_btn=interactive_btn,
        prev=pager_link(prev, 'Previous map', 'prev'), next=pager_link(nxt, 'Next map', 'next'),
    )


def vintage(m):
    """(short label, sentence) saying how current the data behind a map is."""
    src, yr = m.get('source', ''), m.get('year', '')
    if 'NFHS' in src:
        return ('NFHS-5, 2019-21',
                'This map uses NFHS-5 (2019-21). NFHS-6 (2023-24) state fact sheets were released in May 2026, '
                'but they are provisional and report fewer indicators, so the figures here have not been replaced.')
    if 'Census' in src:
        return ('Census 2011',
                'This map uses the 2011 Census, the latest published count by state and district. '
                'Populations and shares will have changed since.')
    note = 'The figures are for %s and have not been refreshed since this map was made.' % yr if yr else \
        'The data year is not recorded for this map.'
    if m.get('quality') == 'UNCERTAIN':
        note += ' It is flagged UNCERTAIN, so check the source before quoting a figure.'
    return ('Data year %s' % yr if yr else 'Data year not recorded', note)

def index_page(maps):
    by_sec = {}
    for m in maps:
        by_sec.setdefault(m['section'], []).append(m)
    blocks = []
    for sec, title in SECTION_TITLES.items():
        items = by_sec.get(sec, [])
        if not items:
            continue
        lis = ''.join('<li><a href="/m/%s.html"><span class="t">%s</span> <span class="vt">%s%s</span></a></li>' % (esc(m['id']), esc(m['title']), esc(vintage(m)[0]), ', newer figures in atlas' if m.get('newer') else (', latest available' if m.get('data_note') else '')) for m in items)
        blocks.append('<section id="%s"><h2>%s <small>%d maps</small></h2><ul>%s</ul></section>' % (esc(sec), esc(title), len(items), lis))
    return ("""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>All 259 maps | How India Lives | ImpactMojo</title>
<meta name="description" content="A complete, browsable index of all 259 state-level maps of India across demography, health, gender, economy, education, environment and more.">
<link rel="canonical" href="{base}/m/index.html">
""" + HEAD_COMMON + """
<style>*{{margin:0;padding:0;box-sizing:border-box}}</style>
<link href="/assets/site.css" rel="stylesheet">
</head>
<body>
<div id="im-common-header"></div>
<main class="mp mp-index">
  <h1>All 259 maps</h1>
  <p class="mp-lead lead">Every state-level map in the atlas, by theme. Open the <a href="/index.html">interactive gallery</a> to search and filter.</p>
  {blocks}
</main>
""" + FOOT + """
</body></html>
""").format(base=BASE, blocks='\n'.join(blocks))

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
    # Previous and next follow the order of data/maps.json, which is the order
    # of the atlas and of m/index.html. The first and last pages have one link.
    filed = [m for m in maps if m.get('file')]
    for i, m in enumerate(filed):
        prev = filed[i - 1] if i > 0 else None
        nxt = filed[i + 1] if i + 1 < len(filed) else None
        with open(os.path.join(outdir, '%s.html' % m['id']), 'w') as f:
            f.write(page(m, inter.get(m['id']), prev, nxt))
        written += 1
    with open(os.path.join(outdir, 'index.html'), 'w') as f:
        f.write(index_page([m for m in maps if m.get('file')]))

    # sitemap
    urls = ['/', '/explore.html', '/stories.html', '/methodology.html', '/m/index.html']
    urls += ['/m/%s' % m['id'].lower() for m in maps if m.get('file')]
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
