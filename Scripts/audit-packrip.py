#!/usr/bin/env python3
"""Audit the PackRip iOS hub against the locked product facts.

Usage:
    python3 Scripts/audit-packrip.py                          # pages + corpus
    python3 Scripts/audit-packrip.py --page packrip-cards/index.html
    python3 Scripts/audit-packrip.py --corpus                 # repo-wide scan only

Exit 0 = clean, 1 = at least one finding. Python stdlib only, no network.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlparse

REPO = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://elhanarinc.github.io"
HUB = "/packrip-cards/"

APP_ID = "6763404045"
APP_STORE_HOST = "apps.apple.com"
APP_STORE_BASE = f"https://apps.apple.com/us/app/packrip-tcg-card-packs/id{APP_ID}"
PROVIDER_TOKEN = "127914124"
PRODUCT_NAME = "PackRip: TCG Card Packs"

ALLOWED_CT = {
    "packrip_ios_github_hero",
    "packrip_ios_github_cta",
    "packrip_ios_github_footer",
    "packrip_ios_github_support",
    "packrip_ios_github_rates",
}
ALLOWED_UTM_CONTENT = {
    "hero_play_web",
    "era_archive",
    "rates_explore",
    "support_web",
    "footer_web",
}
UTM_FIXED = {
    "utm_source": "elhanarinc_github",
    "utm_medium": "referral",
    "utm_campaign": "packrip_ios_hub",
}

PAGES = [
    "packrip-cards/index.html",
    "packrip-cards/rarity.html",
    "packrip-cards/support.html",
    "packrip-cards/privacy.html",
    "packrip-cards/terms.html",
]

# Pages that must carry both an App Store CTA and a packrip.co link.
LINK_CONTRACT_PAGES = {
    "packrip-cards/index.html",
    "packrip-cards/rarity.html",
    "packrip-cards/support.html",
}

STALE_TERMS = [
    r"\bMythos\b",
    r"\bmytholog\w*",
    r"\bmythic\w*",
    r"\bpantheon\b",
    r"\bdeit(?:y|ies)\b",
    r"packrip-mythos",
    r"PackRip:\s*Cards\b",
    r"\bGreek, Norse\b",
]

# Volatile or config-contradicted numbers that must never be published.
FORBIDDEN_NUMERIC_CLAIMS = [
    r"five free daily packs",
    r"\b5 free packs\b",
    r"\b8 total\b",
    r"\bseven rarity\b",
    r"\b7 rarity tiers\b",
    r"\b80 packs\b",
    r"\b200 packs\b",
    r"1\.5\s*(?:×|x)\s*XP",
    r"\+25%\s*sell",
    r"\$\d",
    r"\bno ads\b",
    r"\bno analytics\b",
    r"\bno third-party tracking\b",
    r"\bno leaderboards\b",
]

SYNC_CLAIMS = [
    r"syncs? with the web",
    r"carries over",
    r"shared progress",
    r"same collection on (?:web|iPhone|iOS)",
    r"transfer your (?:collection|progress|save)",
]

FORBIDDEN_JSONLD_KEYS = {
    "aggregateRating",
    "ratingCount",
    "reviewCount",
    "softwareVersion",
    "version",
    "price",
    "priceCurrency",
    "offers",
}

CANONICAL_FOR = {
    "packrip-cards/index.html": f"{SITE}{HUB}",
    "packrip-cards/rarity.html": f"{SITE}{HUB}rarity.html",
    "packrip-cards/support.html": f"{SITE}{HUB}support.html",
    "packrip-cards/privacy.html": f"{SITE}{HUB}privacy.html",
    "packrip-cards/terms.html": f"{SITE}{HUB}terms.html",
}

CORPUS_GLOBS = ["*.html", "*.md", "*.txt", "packrip-cards/*"]
CORPUS_SKIP_PARTS = {".git", "docs", ".github", "hexora", "warranty-pad",
                     "roadshow", "glance", "typesuggest", "wifi-checker",
                     "filmoire35", ".superpowers"}


class PageParser(HTMLParser):
    """Collect the elements the audit reasons about."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.imgs: list[dict] = []
        self.anchors: list[dict] = []
        self.metas: list[dict] = []
        self.links: list[dict] = []
        self.jsonld: list[str] = []
        self.landmarks: list[str] = []
        self._in_ld = False
        self._ld_buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "img":
            self.imgs.append(a)
        elif tag == "a":
            self.anchors.append(a)
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag in ("main", "header", "footer", "nav"):
            self.landmarks.append(tag)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
            self._ld_buf = []

    def handle_endtag(self, tag):
        if tag == "script" and self._in_ld:
            self.jsonld.append("".join(self._ld_buf))
            self._in_ld = False

    def handle_data(self, data):
        if self._in_ld:
            self._ld_buf.append(data)


def meta_value(metas: list[dict], *, name: str = "", prop: str = "") -> str | None:
    for m in metas:
        if name and m.get("name") == name:
            return m.get("content", "")
        if prop and m.get("property") == prop:
            return m.get("content", "")
    return None


def iter_jsonld_keys(node):
    if isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from iter_jsonld_keys(v)
    elif isinstance(node, list):
        for v in node:
            yield from iter_jsonld_keys(v)


def audit_page(rel: str, findings: list[str]) -> None:
    path = REPO / rel
    if not path.exists():
        findings.append(f"{rel}: file missing")
        return
    raw = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(raw)

    def fail(msg: str) -> None:
        findings.append(f"{rel}: {msg}")

    # A. stale Mythos-era vocabulary
    for pat in STALE_TERMS:
        for m in re.finditer(pat, raw, re.IGNORECASE):
            fail(f"stale term {m.group(0)!r} at offset {m.start()}")

    # B. volatile or contradicted numeric claims
    for pat in FORBIDDEN_NUMERIC_CLAIMS:
        for m in re.finditer(pat, raw, re.IGNORECASE):
            fail(f"forbidden claim {m.group(0)!r} at offset {m.start()}")

    # C. wording that implies shared web/iOS progress
    for pat in SYNC_CLAIMS:
        for m in re.finditer(pat, raw, re.IGNORECASE):
            fail(f"sync-implying copy {m.group(0)!r} at offset {m.start()}")

    # D. product name is always the full listing name
    for m in re.finditer(r"PackRip:\s*([A-Za-z][^<.,\n]*)", raw):
        if not m.group(0).startswith(PRODUCT_NAME):
            fail(f"partial product name {m.group(0)[:40]!r}")

    # E. canonical + og:url agree with the page's own address
    want = CANONICAL_FOR.get(rel)
    canonical = next((l.get("href") for l in parser.links
                      if l.get("rel") == "canonical"), None)
    if want and canonical != want:
        fail(f"canonical is {canonical!r}, expected {want!r}")
    og_url = meta_value(parser.metas, prop="og:url")
    if want and og_url != want:
        fail(f"og:url is {og_url!r}, expected {want!r}")

    # F. required head metadata
    if not meta_value(parser.metas, name="description"):
        fail("missing meta description")
    for prop in ("og:type", "og:title", "og:description", "og:image", "og:site_name"):
        if not meta_value(parser.metas, prop=prop):
            fail(f"missing {prop}")
    for name in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
        if not meta_value(parser.metas, name=name):
            fail(f"missing {name}")
    if not meta_value(parser.metas, name="robots"):
        fail("missing robots directive")
    banner = meta_value(parser.metas, name="apple-itunes-app") or ""
    if f"app-id={APP_ID}" not in banner:
        fail(f"smart app banner missing app-id={APP_ID}: {banner!r}")
    if not any(l.get("rel") == "icon" for l in parser.links):
        fail("missing favicon link")
    if not any(l.get("rel") == "apple-touch-icon" for l in parser.links):
        fail("missing apple-touch-icon link")

    # G. og:site_name is the product name
    if meta_value(parser.metas, prop="og:site_name") != PRODUCT_NAME:
        fail("og:site_name is not the full product name")

    # H. App Store anchors carry the full attribution contract
    store_links = [a for a in parser.anchors
                   if APP_STORE_HOST in a.get("href", "")]
    for a in store_links:
        href = a["href"]
        u = urlparse(href)
        q = parse_qs(u.query)
        if f"id{APP_ID}" not in u.path:
            fail(f"App Store link without id{APP_ID}: {href}")
        if not href.startswith(APP_STORE_BASE):
            fail(f"App Store link off canonical base: {href}")
        if q.get("pt", [""])[0] != PROVIDER_TOKEN:
            fail(f"App Store link missing pt={PROVIDER_TOKEN}: {href}")
        if q.get("mt", [""])[0] != "8":
            fail(f"App Store link missing mt=8: {href}")
        ct = q.get("ct", [""])[0]
        if ct not in ALLOWED_CT:
            fail(f"App Store link ct={ct!r} not in the allowed placement set: {href}")

    # I. packrip.co anchors carry the full UTM contract
    web_links = [a for a in parser.anchors
                 if "packrip.co" in a.get("href", "")]
    for a in web_links:
        href = a["href"]
        u = urlparse(href)
        if u.scheme != "https":
            fail(f"packrip.co link is not https: {href}")
        q = parse_qs(u.query)
        for key, val in UTM_FIXED.items():
            if q.get(key, [""])[0] != val:
                fail(f"packrip.co link missing {key}={val}: {href}")
        content = q.get("utm_content", [""])[0]
        if content not in ALLOWED_UTM_CONTENT:
            fail(f"packrip.co link utm_content={content!r} not in the allowed set: {href}")

    # J. the link contract itself
    if rel in LINK_CONTRACT_PAGES:
        if not store_links:
            fail("no App Store CTA on a conversion page")
        if not web_links:
            fail("no packrip.co link on a conversion page")

    # K. new-tab links are safe
    for a in parser.anchors:
        if a.get("target") == "_blank" and "noopener" not in a.get("rel", ""):
            fail(f"target=_blank without rel=noopener: {a.get('href')}")

    # L. images: alt, explicit box, local only
    for img in parser.imgs:
        src = img.get("src", "")
        if "alt" not in img:
            fail(f"img without alt attribute: {src}")
        if not img.get("width") or not img.get("height"):
            fail(f"img without explicit width/height: {src}")
        if src.startswith("http"):
            fail(f"remote image hotlinked: {src}")

    # M. local hub assets exist on disk
    for attr_holder, key in ([(i, "src") for i in parser.imgs]
                             + [(l, "href") for l in parser.links]):
        val = attr_holder.get(key, "")
        if val.startswith(HUB):
            if not (REPO / val.lstrip("/")).exists():
                fail(f"local asset does not exist: {val}")

    # N. internal hub links resolve
    for a in parser.anchors:
        href = a.get("href", "")
        if href.startswith(HUB):
            target = href.split("#", 1)[0]
            candidate = REPO / target.lstrip("/")
            if target.endswith("/"):
                candidate = candidate / "index.html"
            if not candidate.exists():
                fail(f"internal link target missing: {href}")

    # O. JSON-LD parses and stays clear of volatile fields
    for i, block in enumerate(parser.jsonld, start=1):
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError as exc:
            fail(f"JSON-LD block #{i} does not parse: {exc}")
            continue
        for key in iter_jsonld_keys(data):
            if key in FORBIDDEN_JSONLD_KEYS:
                fail(f"JSON-LD block #{i} contains forbidden key {key!r}")

    # P. landmarks and skip link
    for tag in ("header", "main", "footer"):
        if tag not in parser.landmarks:
            fail(f"missing <{tag}> landmark")
    if not any(a.get("href") == "#main" for a in parser.anchors):
        fail("missing skip link to #main")

    # Q. reduced motion is honoured by the shared stylesheet, not inline motion
    if re.search(r"style=\"[^\"]*(?:transition|animation)", raw, re.IGNORECASE):
        fail("inline transition/animation cannot be disabled by reduced-motion")


def audit_corpus(findings: list[str]) -> None:
    """Repo-wide scan of the discovery surfaces for stale PackRip vocabulary."""
    targets = ["index.html", "404.html", "README.md", "llms.txt",
               "llms-full.txt", "packrip-cards/llms.txt"]
    for rel in targets:
        path = REPO / rel
        if not path.exists():
            findings.append(f"{rel}: file missing")
            continue
        raw = path.read_text(encoding="utf-8")
        # Only the PackRip-relevant lines: other products legitimately mention
        # mythology-free vocabulary and are out of scope for this plan.
        for lineno, line in enumerate(raw.splitlines(), start=1):
            if "packrip" not in line.lower() and "PackRip" not in line:
                continue
            for pat in STALE_TERMS + FORBIDDEN_NUMERIC_CLAIMS + SYNC_CLAIMS:
                m = re.search(pat, line, re.IGNORECASE)
                if m:
                    findings.append(
                        f"{rel}:{lineno}: PackRip line carries {m.group(0)!r}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", action="append", default=[],
                    help="repo-relative HTML page to audit; repeatable")
    ap.add_argument("--corpus", action="store_true",
                    help="run only the repo-wide discovery-surface scan")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    findings: list[str] = []
    if args.corpus and not args.page:
        audit_corpus(findings)
    else:
        pages = args.page or PAGES
        for rel in pages:
            audit_page(rel, findings)
        if not args.page:
            audit_corpus(findings)

    if findings:
        for f in findings:
            print(f"FAIL {f}")
        print(f"\n{len(findings)} finding(s)")
        return 1
    if not args.quiet:
        print("audit-packrip: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
