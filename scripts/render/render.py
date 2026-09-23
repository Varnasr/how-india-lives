#!/usr/bin/env python3
"""Render the generated sheets in `scripts/render/sheets.json` to PNG.

    python3 scripts/render/render.py            # render every sheet
    python3 scripts/render/render.py mpce_r     # one of them
    python3 scripts/render/render.py --svg-only # no browser needed

Each sheet names an indicator in `data/interactive-data.json` and adds the
prose the atlas carries around a map: the takeaway, the policy note, the
tags, and the Hindi. The numbers are never written here.

Rasterising needs Chromium. The path is taken from PLAYWRIGHT_BROWSERS_PATH
if it is set, which is how the agent sandbox and CI both find one.
"""
import base64
import glob
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import choropleth as ch  # noqa: E402

ROOT = ch.ROOT
SHEETS = os.path.join(HERE, "sheets.json")
FONT = os.path.join(HERE, "Inter-latin.woff2")


def chromium():
    root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    for pat in ("chromium-*/chrome-linux/chrome",
                "chromium_headless_shell-*/chrome-linux/headless_shell"):
        hits = sorted(glob.glob(os.path.join(root, pat)))
        if hits:
            return hits[-1]
    for p in ("/usr/bin/chromium", "/usr/bin/chromium-browser",
              "/usr/bin/google-chrome"):
        if os.path.exists(p):
            return p
    raise SystemExit(
        "No Chromium found. Set PLAYWRIGHT_BROWSERS_PATH, or run with "
        "--svg-only to write the SVG and rasterise elsewhere.")


def page(svg):
    """Wrap the SVG in a page carrying Inter as a data URI.

    The font is embedded rather than linked because a render that silently
    falls back to a system face produces a sheet that looks nearly right and
    does not match the other 205.
    """
    with open(FONT, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return (
        "<!doctype html><meta charset=utf-8><style>"
        "@font-face{font-family:Inter;font-style:normal;font-weight:100 900;"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
        "html,body{margin:0;padding:0}"
        "svg{display:block}svg text{font-family:Inter,sans-serif}"
        "</style>" + svg)


def indicators():
    with open(os.path.join(ROOT, "data", "interactive-data.json"), encoding="utf-8") as f:
        return {i["id"]: i for i in json.load(f)["indicators"]}


def build_spec(sheet, ind):
    return {
        "id": sheet["id"],
        "title": sheet.get("title", ind["name"]),
        "subtitle": sheet["subtitle"],
        "eyebrow": sheet["eyebrow"],
        "unit": ind["unit"],
        "suffix": sheet.get("suffix", ""),
        "source": ind["source"],
        "year": ind["year"],
        "values": ind["values"],
        "national": ind.get("national"),
        "higherIsBetter": ind.get("higherIsBetter"),
        "decimals": sheet.get("decimals", 0),
        "callout_note": sheet["callout_note"],
        "credit": "How India Lives · generated sheet",
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    svg_only = "--svg-only" in sys.argv
    with open(SHEETS, encoding="utf-8") as f:
        sheets = json.load(f)
    inds = indicators()
    if args:
        sheets = [s for s in sheets if s["indicator"] in args or s["id"] in args]
        if not sheets:
            raise SystemExit(f"no sheet matches {args}")

    exe = None if svg_only else chromium()
    for sheet in sheets:
        ind = inds.get(sheet["indicator"])
        if ind is None:
            raise SystemExit(f"{sheet['id']}: no indicator {sheet['indicator']!r} "
                             "in data/interactive-data.json")
        svg = ch.render(build_spec(sheet, ind))
        out = os.path.join(ROOT, "maps", sheet["section"], sheet["file"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if svg_only:
            with open(out.replace(".png", ".svg"), "w", encoding="utf-8") as f:
                f.write(svg)
            print("wrote", out.replace(".png", ".svg"))
            continue
        with tempfile.TemporaryDirectory() as td:
            html = os.path.join(td, "sheet.html")
            with open(html, "w", encoding="utf-8") as f:
                f.write(page(svg))
            subprocess.run(
                [exe, "--headless", "--disable-gpu", "--no-sandbox",
                 "--hide-scrollbars", "--force-color-profile=srgb",
                 f"--screenshot={out}", f"--window-size={ch.W},{ch.H}", html],
                check=True, capture_output=True)
        print(f"wrote {out} ({os.path.getsize(out) // 1024} KB)")


if __name__ == "__main__":
    main()
