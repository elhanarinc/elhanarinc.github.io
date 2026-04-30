#!/usr/bin/env python3
"""Regenerate sitemap.xml from all .html files in the repo.

Run after adding/removing/renaming pages. Idempotent: if the resulting
sitemap is byte-identical to the on-disk version, nothing is written.
"""
import os, datetime, sys, pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://elhanarinc.github.io"
TODAY = datetime.date.today().isoformat()

SKIP_DIRS = {".git", ".github", "Scripts", "node_modules"}
SKIP_FILES = {"404.html"}


def collect():
    pages = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".html") or f in SKIP_FILES:
                continue
            rel = pathlib.Path(root, f).relative_to(REPO).as_posix()
            pages.append(rel)
    return sorted(pages)


def url_for(path: str) -> str:
    if path == "index.html":
        return BASE + "/"
    if path.endswith("/index.html"):
        return BASE + "/" + path[: -len("index.html")]
    return BASE + "/" + path


def priority(u: str) -> str:
    if u == BASE + "/":
        return "1.0"
    if u.endswith("/hexora/") or u.endswith("/hexora/tr/") or u.endswith("/packrip-mythos/"):
        return "0.9"
    if any(x in u for x in ("/oracle.html", "/journal.html", "/fal.html",
                             "/pack-opening.html", "/rarity.html")):
        return "0.8"
    if u.endswith("/packrip-mythos/pantheons/"):
        return "0.8"
    if "/hexagram/" in u:
        return "0.7"
    if "/packrip-mythos/pantheons/" in u and u.endswith(".html"):
        return "0.7"
    if u.endswith("/index.html") or u.endswith("/"):
        return "0.6"
    return "0.5"


def hreflang(u: str):
    """Return [(lang, href)] tuples for cross-lang pages."""
    if "/hexora/hexagram/" in u and "/tr/" not in u:
        slug = u.split("/hexora/hexagram/")[-1]
        return [("en", u), ("tr", BASE + "/hexora/tr/hexagram/" + slug), ("x-default", u)]
    if "/hexora/tr/hexagram/" in u:
        slug = u.split("/hexora/tr/hexagram/")[-1]
        en = BASE + "/hexora/hexagram/" + slug
        return [("en", en), ("tr", u), ("x-default", en)]
    if u in (BASE + "/hexora/", BASE + "/hexora/tr/"):
        return [("en", BASE + "/hexora/"), ("tr", BASE + "/hexora/tr/"),
                ("x-default", BASE + "/hexora/")]
    if u == BASE + "/hexora/oracle.html":
        return [("en", u), ("tr", BASE + "/hexora/tr/fal.html"), ("x-default", u)]
    if u == BASE + "/hexora/tr/fal.html":
        en = BASE + "/hexora/oracle.html"
        return [("en", en), ("tr", u), ("x-default", en)]
    return []


def build():
    urls = sorted({url_for(p) for p in collect()})
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for u in urls:
        out.append("  <url>")
        out.append(f"    <loc>{u}</loc>")
        out.append(f"    <lastmod>{TODAY}</lastmod>")
        out.append(f"    <priority>{priority(u)}</priority>")
        for lang, href in hreflang(u):
            out.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>')
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n", len(urls)


def main():
    new, n = build()
    sm = REPO / "sitemap.xml"
    old = sm.read_text() if sm.exists() else ""
    if old == new:
        print(f"sitemap.xml unchanged ({n} URLs)")
        return 0
    sm.write_text(new)
    print(f"sitemap.xml regenerated ({n} URLs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
