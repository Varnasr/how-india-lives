#!/usr/bin/env python3
"""Render a static atlas choropleth from the repository's own data.

Until 2026-09-23 there was no renderer here. The 205 PNGs in `maps/` were
produced somewhere else and committed, so a new static map could not be made
from this repository at all, and the catalogue in `data/maps.json` carried no
per-state numbers to make one from.

This renders from `data/interactive-data.json`, which does carry them. A map
generated this way cannot disagree with the interactive view of the same
indicator, because there is one set of numbers and the cross-link is written
by the same script.

Output is SVG. `render.py` rasterises it through headless Chromium, which is
what puts real type on the page; nothing here needs a browser.
"""
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GEOJSON = os.path.join(ROOT, "data", "india-states.geojson")

W, H = 3052, 1725

# Sampled from maps/education/S07a_*.png so a new sheet sits in the same
# visual family as the 205 that came before it.
BG = "#F8F6F1"
INK = "#1A1A2E"
EYEBROW = "#8B8C9C"
MUTED = "#6E6E7A"
CALLOUT = "#C0392B"
NODATA = "#E0DED8"
HAIRLINE = "#FFFFFF"

# The green ramp of the existing sheets, read off the legend bar at five
# points rather than guessed at.
RAMP = [
    (0.00, (234, 244, 219)),
    (0.25, (193, 215, 165)),
    (0.50, (101, 146, 41)),
    (0.75, (52, 84, 14)),
    (1.00, (23, 42, 4)),
]

# The geojson carries a few superseded two-letter codes. These are display
# only: every join in this repository is on the state name.
CODE_DISPLAY = {"OR": "OD", "UT": "UK", "CT": "CG", "DH": "DNH"}

NORTHEAST = {"AS", "MN", "NL", "ML", "AR", "MZ", "TR", "SK"}

# States whose polygon is too small to hold a label at this scale. The label
# goes outside on a leader line, at (dx, dy) in final pixels from the state.
OUTSIDE = {
    "GA": (-150, 30), "DH": (-185, -10), "LD": (-140, 20),
    "AN": (160, 40), "PY": (150, 25), "CH": (-150, -40),
    "DL": (-330, -60), "KL": (-150, 10),
}

# The same problem inside the north-east inset, where Sikkim and Tripura are
# still smaller than their own labels.
OUTSIDE_INSET = {"SK": (-30, -60), "TR": (-120, 20)}


def load_states():
    with open(GEOJSON, encoding="utf-8") as f:
        gj = json.load(f)
    out = []
    for feat in gj["features"]:
        geom = feat["geometry"]
        if geom["type"] == "Polygon":
            polys = [geom["coordinates"][0]]
        else:
            polys = [p[0] for p in geom["coordinates"]]
        p = feat["properties"]
        out.append({
            "name": p["name"],
            "code": p["code"],
            "label": CODE_DISPLAY.get(p["code"], p["code"]),
            "region": p.get("region", ""),
            "polys": [[(float(x), float(y)) for x, y in ring] for ring in polys],
        })
    return out


def project(lon, lat, lat0=23.0):
    """Equirectangular, scaled by cos(lat0) so India is not stretched.

    A conic would be more correct and would also mean this file could not be
    checked by reading it. At this scale the difference is under a pixel.
    """
    return lon * math.cos(math.radians(lat0)), -lat


def fit(polys, box):
    """Scale and centre projected rings into (x, y, w, h), keeping aspect."""
    pts = [project(x, y) for ring in polys for x, y in ring]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    bx, by, bw, bh = box
    s = min(bw / (x1 - x0), bh / (y1 - y0))
    ox = bx + (bw - (x1 - x0) * s) / 2 - x0 * s
    oy = by + (bh - (y1 - y0) * s) / 2 - y0 * s
    return lambda lon, lat: (
        project(lon, lat)[0] * s + ox,
        project(lon, lat)[1] * s + oy,
    )


def path_d(polys, tx):
    parts = []
    for ring in polys:
        pts = [tx(lon, lat) for lon, lat in ring]
        parts.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    return "".join(parts)


def ring_centroid(ring):
    """Area centroid. The arithmetic mean of the vertices sits outside a
    state with a long coastline, because the coast carries more points."""
    a = cx = cy = 0.0
    for i in range(len(ring)):
        x0, y0 = ring[i]
        x1, y1 = ring[(i + 1) % len(ring)]
        f = x0 * y1 - x1 * y0
        a += f
        cx += (x0 + x1) * f
        cy += (y0 + y1) * f
    if abs(a) < 1e-12:
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        return sum(xs) / len(xs), sum(ys) / len(ys), 0.0
    a *= 0.5
    return cx / (6 * a), cy / (6 * a), abs(a)


def anchor(state, tx):
    """Label point: the centroid of the state's largest ring, in pixels."""
    best = max((ring_centroid(r) for r in state["polys"]), key=lambda c: c[2])
    return tx(best[0], best[1]), best[2]


def ramp(t):
    t = max(0.0, min(1.0, t))
    for (a, ca), (b, cb) in zip(RAMP, RAMP[1:]):
        if t <= b:
            u = 0.0 if b == a else (t - a) / (b - a)
            return "#%02X%02X%02X" % tuple(
                round(ca[i] + (cb[i] - ca[i]) * u) for i in range(3)
            )
    return "#%02X%02X%02X" % RAMP[-1][1]


def ink_on(hexfill):
    """White or dark, whichever clears more contrast against the fill.

    A fixed luminance cutoff is how the same defect shipped twice in the
    ImpactMojo diagrams: white on #d97706 at 3.19:1. Compare both ratios.
    """
    r, g, b = (int(hexfill[i:i + 2], 16) / 255 for i in (1, 3, 5))

    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    L = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    white = 1.05 / (L + 0.05)
    dark = (L + 0.05) / (0.0603 + 0.05)   # #1A1A2E relative luminance
    return "#FFFFFF" if white >= dark else INK


SHORT = {
    "Dadra and Nagar Haveli and Daman and Diu": "D & N Haveli, Daman & Diu",
    "Andaman and Nicobar": "Andaman & Nicobar",
    "Jammu and Kashmir": "Jammu & Kashmir",
    "Arunachal Pradesh": "Arunachal Pradesh",
}


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def fmt(v, dec):
    if dec == 0:
        return f"{v:,.0f}"
    return f"{v:.{dec}f}"


def render(spec):
    """spec: id, title, subtitle, eyebrow, unit, source, year, values{},
    national, higherIsBetter, decimals, callout_note, credit."""
    states = load_states()
    values = spec["values"]
    dec = spec.get("decimals", 0)
    nums = [v for v in values.values() if v is not None]
    lo, hi = min(nums), max(nums)
    span = (hi - lo) or 1.0

    main_box = (250, 280, 1450, 1130)
    inset_box = (1800, 430, 480, 440)
    tx = fit([r for s in states for r in s["polys"]], main_box)
    ne = [s for s in states if s["code"] in NORTHEAST]
    tx_ne = fit([r for s in ne for r in s["polys"]], inset_box)

    o = []
    A = o.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
      f'viewBox="0 0 {W} {H}" role="img" aria-label="{esc(spec["title"])}">')
    A(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    # Masthead
    A(f'<text x="46" y="52" font-size="19" letter-spacing="1.6" fill="{EYEBROW}" '
      f'font-weight="600">{esc(spec.get("eyebrow", "HOW INDIA LIVES"))}</text>')
    A(f'<text x="46" y="132" font-size="46" font-weight="800" letter-spacing="-0.4" '
      f'fill="{INK}">{esc(spec["title"].upper())}</text>')
    for i, line in enumerate(spec.get("subtitle", "").split("\n")):
        A(f'<text x="46" y="{180 + i * 38}" font-size="27" fill="{INK}" '
          f'opacity="0.86">{esc(line)}</text>')

    def draw(group, transform, label_size, show_values, skip=(), inset=False):
        for s in group:
            v = values.get(s["name"])
            fill = NODATA if v is None else ramp((v - lo) / span)
            A(f'<path d="{path_d(s["polys"], transform)}" fill="{fill}" '
              f'stroke="{HAIRLINE}" stroke-width="2" stroke-linejoin="round"/>')
        for s in group:
            if s["code"] in skip:
                continue
            v = values.get(s["name"])
            (cx, cy), _ = anchor(s, transform)
            fill = NODATA if v is None else ramp((v - lo) / span)
            ink = MUTED if v is None else ink_on(fill)
            out = (OUTSIDE if not inset else OUTSIDE_INSET).get(s["code"])
            halo = f' stroke="{BG if out else fill}" stroke-width="5" paint-order="stroke"' 
            if out:
                lx, ly = cx + out[0], cy + out[1]
                A(f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{lx:.0f}" y2="{ly:.0f}" '
                  f'stroke="{MUTED}" stroke-width="1.6" opacity="0.7"/>')
                cx, cy, ink = lx, ly, MUTED
            A(f'<text x="{cx:.0f}" y="{cy:.0f}" font-size="{label_size}" '
              f'font-weight="700" text-anchor="middle" fill="{ink}"{halo}>'
              f'{s["label"]}</text>')
            if show_values and v is not None:
                A(f'<text x="{cx:.0f}" y="{cy + label_size + 2:.0f}" '
                  f'font-size="{label_size}" text-anchor="middle" fill="{ink}"{halo}>'
                  f'{fmt(v, dec)}</text>')

    draw(states, tx, 21, True, skip=NORTHEAST)

    # North-east inset: seven states and Sikkim, too small to read in place.
    ix, iy, iw, ih = inset_box
    A(f'<rect x="{ix - 40}" y="{iy - 40}" width="{iw + 80}" height="{ih + 80}" '
      f'fill="#EFEDE7" stroke="{MUTED}" stroke-width="2" opacity="0.9"/>')
    draw(ne, tx_ne, 20, True, inset=True)
    nx0, ny0 = tx(88.0, 29.6)
    nx1, ny1 = tx(97.4, 21.9)
    A(f'<rect x="{nx0:.0f}" y="{ny0:.0f}" width="{nx1 - nx0:.0f}" '
      f'height="{ny1 - ny0:.0f}" fill="none" stroke="{MUTED}" stroke-width="2.4" '
      f'stroke-dasharray="14 10" opacity="0.8"/>')

    # The two ends of the distribution, named on the map rather than left to
    # the reader to find.
    hi_state = max((s for s in states if values.get(s["name"]) is not None),
                   key=lambda s: values[s["name"]])
    lo_state = min((s for s in states if values.get(s["name"]) is not None),
                   key=lambda s: values[s["name"]])
    # Red marks the end of the scale that is bad news, which depends on the
    # indicator: the top of a consumption map is not the top of a Gini map.
    good = spec.get("higherIsBetter")
    top = CALLOUT if good is False else "#2F6B3C"
    bot = "#2F6B3C" if good is False else CALLOUT
    # Where the annotation goes is not a constant. A fixed offset put the
    # Jharkhand callout on top of the Uttar Pradesh label; the offset that
    # works on one indicator is wrong on the next, because the extreme state
    # moves. Score the candidates against every other label anchor and the
    # canvas edge, and take the emptiest.
    anchors = [anchor(x, tx)[0] for x in states if x["code"] not in NORTHEAST]
    taken = []

    def place(cx, cy):
        best, best_score = (-330, -120), -1
        for dx, dy in ((-330, -120), (-330, 120), (330, -120), (330, 120),
                       (-400, 0), (400, 0), (0, -190), (0, 190)):
            px, py = cx + dx + (95 if dx < 0 else 95), cy + dy
            if not (120 < px < W - 1250) or not (260 < py < 1450):
                continue
            score = min([abs(px - ax) + abs(py - ay) for ax, ay in anchors]
                        + [abs(px - tx_) + abs(py - ty_) for tx_, ty_ in taken]
                        + [9999])
            if score > best_score:
                best, best_score = (dx, dy), score
        taken.append((cx + best[0] + 95, cy + best[1]))
        return best

    for s, colour, mark in ((hi_state, top, "▲"), (lo_state, bot, "▼")):
        if s["code"] in NORTHEAST:
            continue
        (cx, cy), _ = anchor(s, tx)
        dx, dy = place(cx, cy)
        lx, ly = cx + dx, cy + dy
        A(f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{lx + 190:.0f}" y2="{ly:.0f}" '
          f'stroke="{colour}" stroke-width="2"/>')
        A(f'<text x="{lx:.0f}" y="{ly + 10:.0f}" font-size="30" font-weight="700" '
          f'fill="{colour}">{mark} {s["label"]}: {fmt(values[s["name"]], dec)}'
          f'{esc(spec.get("suffix", ""))}</text>')

    # Callout
    cx0, cy0, cw, ch = 2370, 180, 640, 600
    A(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" fill="{top}"/>')
    A(f'<text x="{cx0 + cw / 2:.0f}" y="{cy0 + 290}" font-size="104" font-weight="800" '
      f'text-anchor="middle" fill="#FFFFFF">{fmt(values[hi_state["name"]], dec)}'
      f'{esc(spec.get("suffix", ""))}</text>')
    note = spec.get("callout_note", "").replace("{state}", hi_state["name"])
    for i, line in enumerate(wrap(note, 30)):
        A(f'<text x="{cx0 + cw / 2:.0f}" y="{cy0 + 400 + i * 34}" font-size="25" '
          f'text-anchor="middle" fill="#FFFFFF">{esc(line)}</text>')

    # Legend
    lx0, ly0, lw, lh = 250, 1500, 1450, 28
    A('<defs><linearGradient id="ramp" x1="0" x2="1">'
      + "".join(f'<stop offset="{t}" stop-color="{ramp(t)}"/>' for t, _ in RAMP)
      + "</linearGradient></defs>")
    A(f'<rect x="{lx0}" y="{ly0}" width="{lw}" height="{lh}" fill="url(#ramp)"/>')
    for i in range(6):
        t = i / 5
        A(f'<text x="{lx0 + lw * t:.0f}" y="{ly0 + lh + 32}" font-size="24" '
          f'text-anchor="middle" fill="{MUTED}">{fmt(lo + span * t, dec)}</text>')
    nat = spec.get("national")
    if nat is not None and lo <= nat <= hi:
        mx = lx0 + lw * (nat - lo) / span
        A(f'<rect x="{mx - 2:.0f}" y="{ly0 - 8}" width="4" height="{lh + 16}" '
          f'fill="{CALLOUT}"/>')
        A(f'<text x="{mx:.0f}" y="{ly0 - 18}" font-size="24" font-weight="600" '
          f'text-anchor="middle" fill="{CALLOUT}">India: {fmt(nat, dec)}</text>')
    A(f'<text x="{lx0 + lw / 2:.0f}" y="{ly0 + lh + 70}" font-size="24" '
      f'text-anchor="middle" fill="{MUTED}">{esc(spec["unit"])}</text>')

    # The ranked panel. A choropleth is good at pattern and bad at order:
    # two states a shade apart cannot be told apart by eye, and the reader who
    # wants to know which is third has nowhere to look. This is that list.
    rows = sorted(((v, k) for k, v in values.items() if v is not None),
                  reverse=True)
    px, py, pw = 2370, 860, 640
    A(f'<text x="{px}" y="{py}" font-size="24" font-weight="700" '
      f'letter-spacing="1.2" fill="{MUTED}">HIGHEST AND LOWEST FIVE</text>')
    band = [(rows[i], i + 1) for i in range(5)] + \
           [(rows[-5 + i], len(rows) - 4 + i) for i in range(5)]
    for i, ((v, name), rank) in enumerate(band):
        y = py + 56 + i * 52 + (24 if i >= 5 else 0)
        colour = ramp((v - lo) / span)
        A(f'<rect x="{px}" y="{y - 24}" width="{pw * (v - lo) / span:.0f}" '
          f'height="34" fill="{colour}" opacity="0.55"/>')
        A(f'<text x="{px + 12}" y="{y}" font-size="26" fill="{INK}">'
          f'{rank}. {esc(SHORT.get(name, name))}</text>')
        A(f'<text x="{px + pw}" y="{y}" font-size="26" font-weight="700" '
          f'text-anchor="end" fill="{INK}">{fmt(v, dec)}'
          f'{esc(spec.get("suffix", ""))}</text>')
    A(f'<text x="{px}" y="{py + 56 + 10 * 52 + 46}" font-size="22" '
      f'fill="{MUTED}">{len(rows)} of 36 states and territories carry a '
      f'published figure</text>')

    A(f'<text x="46" y="{H - 34}" font-size="24" fill="{MUTED}">'
      f'Source: {esc(spec["source"])} · {esc(spec["year"])} · '
      f'rendered from data/interactive-data.json</text>')
    A(f'<text x="{W - 46}" y="{H - 34}" font-size="24" text-anchor="end" '
      f'fill="{MUTED}">{esc(spec.get("credit", "How India Lives"))}</text>')
    A("</svg>")
    return "\n".join(o)


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
