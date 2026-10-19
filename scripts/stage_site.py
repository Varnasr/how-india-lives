#!/usr/bin/env python3
"""
What the site publishes, and what it must not.

Netlify used to publish the whole repository, so CLAUDE.md, the build scripts
and the contributor notes were served at guessable addresses, linked from
nothing. The build now copies only the published entries into _site.

Every top-level entry in the repository has to be named here, as published or
as kept back. A new one fails the build until somebody decides which it is.

    python3 scripts/stage_site.py           # check only
    python3 scripts/stage_site.py _site     # check, then copy the site there
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PUBLISHED = {
    "index.html", "explore.html", "methodology.html", "stories.html",
    "m", "maps", "data", "assets", "fonts", "docs",
    "sw.js", "manifest.json", "robots.txt", "sitemap.xml", "LICENSE",
}
KEPT_BACK = {
    ".github", ".gitignore", ".gitattributes", ".editorconfig", ".claude", "CLAUDE.md", "CONTRIBUTING.md",
    "README.md", "scripts", "netlify.toml", "_site",
}


def main():
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                             text=True, check=True).stdout.split("\n")
    top = {p.split("/")[0] for p in tracked if p}
    errors = []
    unnamed = sorted(top - PUBLISHED - KEPT_BACK)
    if unnamed:
        errors.append("named neither published nor kept back: " + ", ".join(unnamed))
    missing = sorted(p for p in PUBLISHED if not os.path.exists(os.path.join(ROOT, p)))
    if missing:
        errors.append("named as published but absent: " + ", ".join(missing))
    if errors:
        for e in errors:
            print("FAIL:", e)
        sys.exit(1)
    if len(sys.argv) > 1:
        dest = os.path.abspath(sys.argv[1])
        if os.path.exists(dest):
            shutil.rmtree(dest)
        os.makedirs(dest)
        for name in sorted(PUBLISHED):
            src = os.path.join(ROOT, name)
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(dest, name),
                                ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
            else:
                shutil.copy2(src, os.path.join(dest, name))
        print(f"staged {len(PUBLISHED)} entries in {dest}")
    print(f"PASS: {len(PUBLISHED)} published, {len(KEPT_BACK)} kept back")


if __name__ == "__main__":
    main()
