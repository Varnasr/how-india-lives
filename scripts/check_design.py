#!/usr/bin/env python3
"""
check_design.py - one palette, and every colour in it readable.

    python3 scripts/check_design.py
    python3 scripts/check_design.py --all    # print the passing pairs too

WHY THIS EXISTS

The palette used to be written out eight times: inline in index.html,
explore.html, methodology.html and stories.html, twice inside
build_map_pages.py, and again in assets/common-header.css, under four
different naming schemes (--accent-color, --acc, --im-accent). They had
drifted. Only index.html defined the status colours. Only index and explore
defined a second accent. Neither generated template had a dark theme at all,
so the 205 map pages under m/ rendered light-theme ink whatever the reader
had chosen.

And the numbers were failing. Measured on the surfaces they are painted on:
--accent-color #0EA5E9 at 2.53:1, --text-muted #94A3B8 at 2.34:1, --success
#10B981 at 2.32:1, --warning #F59E0B at 1.96:1. That was 106 failing nodes on
the home page and more on every other page, because the same numbers had been
copied into each one. Fixing a page fixed a page.

So: assets/tokens.css owns the palette, every page links it, and this check
holds both halves.

WHAT IT CANNOT SEE, stated plainly. A colour written as a literal in a rule,
and a colour composited with opacity, are invisible here. Consolidating the
tokens left three such rules behind in explore.html (#EF4444, #10B981 as
ranking figures), three badge rules in methodology.html, and white on
WhatsApp's #25D366 in stories.html at 1.98:1. axe over the built pages is
what found those, and the two are not substitutes for each other.
"""
import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, "assets", "tokens.css")
AA = 4.5

INK = ["--text-primary", "--text-secondary", "--text-muted",
       "--accent-color", "--accent-hover", "--secondary-accent",
       "--success-color", "--warning-color", "--danger-color"]
SURFACE = ["--primary-bg", "--secondary-bg", "--card-bg", "--hover-bg"]

# Tokens assets/tokens.css owns. A page redeclaring one of these is the drift
# this check exists to stop.
OWNED = set(INK + SURFACE + ["--border-color", "--gradient-primary",
                             "--bg", "--sec", "--card", "--tx", "--tx2",
                             "--mut", "--acc", "--bd"])

# Pages that legitimately do not link the palette, each with a reason. A stale
# exemption fails too, so the list cannot rot into a blindfold.
EXEMPT_PAGES = {}


def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def declarations(css, selector):
    """Custom properties a selector declares, merged across every block."""
    out, at = {}, css.find(selector)
    if at == -1:
        return None
    while at != -1:
        open_at = css.index("{", at)
        depth, end = 0, open_at
        for i in range(open_at, len(css)):
            if css[i] == "{":
                depth += 1
            elif css[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        out.update(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", css[open_at + 1:end]))
        at = css.find(selector, end)
    return out


def resolve(tokens, value, seen=None):
    seen = seen or set()
    m = re.fullmatch(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)", (value or "").strip())
    if not m:
        return (value or "").strip()
    if m.group(1) in seen:
        return None
    seen.add(m.group(1))
    if m.group(1) in tokens:
        return resolve(tokens, tokens[m.group(1)], seen)
    return resolve(tokens, m.group(2), seen) if m.group(2) else None


def pages():
    found = [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "*.html"))]
    # One generated map page is enough to prove the template; all 205 come from
    # the same two strings in build_map_pages.py.
    for p in ("m/index.html", "m/S00a.html"):
        if os.path.exists(os.path.join(ROOT, p)):
            found.append(p)
    return sorted(found)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    failures, passes, checks = [], [], 0

    if not os.path.exists(TOKENS):
        print("FAIL: assets/tokens.css is missing. It owns the palette.", file=sys.stderr)
        return 1
    css = open(TOKENS, encoding="utf-8").read()

    light = declarations(css, ":root")
    dark = declarations(css, 'html[data-theme="dark"]')
    if not light or not dark:
        failures.append("assets/tokens.css: could not find both theme blocks")
        light, dark = light or {}, dark or {}

    for theme_name, block in (("light", light), ("dark", dark)):
        merged = dict(light)
        merged.update(block)
        for ink in INK:
            fg = resolve(merged, merged.get(ink, ""))
            if not fg or not fg.startswith("#"):
                failures.append(f"{theme_name}: {ink} is missing or unresolvable")
                continue
            for surface in SURFACE:
                bg = resolve(merged, merged.get(surface, ""))
                if not bg or not bg.startswith("#"):
                    failures.append(f"{theme_name}: {surface} is missing or unresolvable")
                    continue
                checks += 1
                r = ratio(fg, bg)
                row = f"{theme_name:5s} {ink} ({fg}) on {surface} ({bg})  {r:.2f}:1"
                (failures if r < AA else passes).append(row)

    # Every page links the palette, and no page redeclares it.
    owned_re = re.compile(r"(" + "|".join(re.escape(t) for t in sorted(OWNED)) + r")\s*:")
    for page in pages():
        text = open(os.path.join(ROOT, page), encoding="utf-8").read()
        checks += 1
        if page in EXEMPT_PAGES:
            if "assets/tokens.css" in text:
                failures.append(f"{page}: exempted as {EXEMPT_PAGES[page]}, but it links "
                                f"tokens.css now. Remove the exemption.")
            continue
        if "assets/tokens.css" not in text:
            failures.append(f"{page}: does not link /assets/tokens.css")
        # Only look inside <style> blocks; a hex in page copy is not a token.
        for style in re.findall(r"<style[^>]*>(.*?)</style>", text, re.S):
            for m in owned_re.finditer(style):
                line = style[:m.start()].count("\n") + 1
                failures.append(f"{page}: redeclares {m.group(1)} in a <style> block "
                                f"(line {line} of that block). The palette lives in "
                                f"assets/tokens.css.")
                break

    for page, why in EXEMPT_PAGES.items():
        if page not in pages():
            failures.append(f"stale exemption: {page} ({why}) is not a page any more")

    print(f"Design: {checks} check(s) over {len(pages())} page(s), against {AA}:1.")
    if args.all:
        for p in passes:
            print(f"  ok   {p}")

    if failures:
        print("")
        for f in failures:
            print(f"  {f}")
        print(f"\nFAIL: {len(failures)} problem(s).", file=sys.stderr)
        return 1
    print(f"OK: one palette, linked everywhere, every ink clears {AA}:1 in its own theme.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
