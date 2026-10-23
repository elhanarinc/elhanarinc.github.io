#!/usr/bin/env python3
"""Regenerate sitemap.xml from all .html files in the repo.

Run after adding/removing/renaming pages. Idempotent: if the resulting
sitemap is byte-identical to the on-disk version, nothing is written.
"""
import os, datetime, subprocess, sys, pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://elhanarinc.github.io"
TODAY = datetime.date.today().isoformat()


def last_commit_dates() -> dict:
    """Map repo-relative path -> YYYY-MM-DD of its last commit.

    <lastmod> must reflect when a page actually changed. Stamping every URL
    with today's date makes the signal worthless (and rewrites the whole file
    on every run). Needs full history: the CI checkout uses fetch-depth: 0.
    """
    try:
        out = subprocess.run(
            ["git", "log", "--name-only", "--format=%x00%cs", "--", "*.html"],
            cwd=REPO, capture_output=True, text=True, check=True, timeout=120,
        ).stdout
    except (subprocess.SubprocessError, OSError) as exc:
        print(f"WARNING: git log failed ({exc}) — every <lastmod> will fall back to "
              f"today's date, which is the bug this function exists to prevent.",
              file=sys.stderr)
        return {}
    dates, cur = {}, None
    for line in out.splitlines():
        if line.startswith("\x00"):
            cur = line[1:].strip()
        elif line.strip() and cur:
            dates.setdefault(line.strip(), cur)  # first hit = most recent commit
    return dates


LAST_COMMIT = last_commit_dates()



def lastmod_for(path: str) -> str:
    return LAST_COMMIT.get(path, TODAY)

SKIP_DIRS = {".git", ".github", "Scripts", "node_modules", "_preview"}
SKIP_FILES = {"404.html"}


def collect():
    pages = []
    for root, dirs, files in os.walk(REPO):
        # Dot-directories are skipped from the SITEMAP, which is not the same as
        # being unpublishable: this repo ships .nojekyll, so GitHub Pages serves the
        # raw tree and .well-known/ is genuinely reachable. The exclusion exists
        # because tooling directories (.git, .github, .superpowers) contain HTML that
        # must never be indexed, and enumerating them by name silently misses the next
        # one. If a dot-directory ever holds a real page, the warning below fires.
        dropped_dots = [d for d in dirs if d.startswith(".") and d not in SKIP_DIRS]
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for d in dropped_dots:
            stray = sorted(p for p in pathlib.Path(root, d).rglob("*.html"))
            if stray:
                rel = pathlib.Path(root, d).relative_to(REPO).as_posix()
                print(f"WARNING: {rel}/ holds {len(stray)} .html file(s) and was skipped, "
                      f"so they are absent from the sitemap. If any is a real page, move it "
                      f"out of a dot-directory or add an explicit exception. First: "
                      f"{stray[0].relative_to(REPO).as_posix()}", file=sys.stderr)
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
    # Active apps — landing pages.
    if u.endswith(("/packrip-cards/", "/filmoire35/")):
        return "0.9"
    if u.endswith("/rarity.html"):
        return "0.8"
    if u.endswith("/index.html") or u.endswith("/"):
        return "0.6"
    return "0.5"


CM = BASE + "/captain-mittens/"
HREFLANG_GROUPS = [
    {"tr": CM + "tr/", "en": CM + "en/", "x-default": CM},
    {"tr": CM + "tr/kedi-bulmaca-oyunu-iphone.html", "en": CM + "en/cat-match-3-game-iphone.html"},
]


def hreflang(u: str):
    """Return [(lang, href)] alternates for every member of an hreflang group
    (each member lists the whole group, itself included, as Google requires)."""
    for g in HREFLANG_GROUPS:
        if u in g.values():
            return list(g.items())
    return []


def build():
    pages = collect()
    known = sum(1 for p in pages if p in LAST_COMMIT)
    if known < len(pages) * 0.9:
        print(f"WARNING: git history covers only {known}/{len(pages)} pages — this is "
              f"what a shallow clone looks like. The rest will be stamped with today's "
              f"date. Re-run with a full checkout (fetch-depth: 0).", file=sys.stderr)
    lastmods = {}
    for p in pages:
        u = url_for(p)
        lastmods[u] = max(lastmods.get(u, ""), lastmod_for(p))
    urls = sorted(lastmods)
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for u in urls:
        out.append("  <url>")
        out.append(f"    <loc>{u}</loc>")
        out.append(f"    <lastmod>{lastmods[u]}</lastmod>")
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
