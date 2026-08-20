# PackRip iOS Pokémon Hub Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the obsolete Mythos-facing `/packrip-cards/` microsite into the official `PackRip: TCG Card Packs` Pokémon TCG iPhone product, legal, and support hub, with measurable reciprocal links to the playable web product at `packrip.co`.

**Architecture:** Five hand-written static HTML pages plus one shared stylesheet in the `elhanarinc.github.io` repository, served by GitHub Pages with no build step, no JavaScript dependency, and no backend. A new stdlib-only Python auditor (`Scripts/audit-packrip.py`) encodes the product facts and the link/attribution contract as executable assertions, so every task has a real failing check before its content is written. The `pokemon-pack-opening` repository receives one deliberately narrow reverse-backlink change on the `/ios` surface only.

**Tech Stack:** Static HTML5, hand-written CSS with custom properties, Google Fonts (Bodoni Moda + Archivo), schema.org JSON-LD, Python 3 stdlib (`Scripts/audit-packrip.py`, `Scripts/regen-sitemap.py`), GitHub Actions, and on the web side React 19 + TypeScript + Vite + `scripts/prerender.mjs`.

**Spec:** `docs/superpowers/specs/2026-08-20-packrip-ios-pokemon-hub-design.md`

---

## Global Constraints

Every task's requirements implicitly include this section. Values are copied verbatim from the spec or from the live evidence gathered in Task 1.

### Identity

- Public product name, everywhere, with no abbreviation: `PackRip: TCG Card Packs`
- App Store ID: `6763404045`
- Canonical App Store URL base: `https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045`
- Provider token: `127914124`
- Platform: iPhone. Minimum OS: iOS 17.0. Language: English.
- Web product: `https://packrip.co`
- Hub base URL: `https://elhanarinc.github.io/packrip-cards/` — this path never changes and is never redirected.
- Contact e-mail on every hub page: `elhanarinc@gmail.com` (the web product's `arinc@packrip.co` is not used on the hub).
- Publisher/author name in structured data and footers: `Arinc Elhan`.

### Attribution contract

Every App Store anchor on the hub is exactly `https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?pt=127914124&ct=<TAG>&mt=8` (written `&amp;` in HTML), where `<TAG>` is one of exactly these six placement tags and nothing else:

- `packrip_ios_github_hero` — landing hero CTA
- `packrip_ios_github_bridge` — landing web/iOS bridge column CTA
- `packrip_ios_github_cta` — landing final conversion block
- `packrip_ios_github_footer` — the shared footer on all five pages
- `packrip_ios_github_support` — Support page CTAs
- `packrip_ios_github_rates` — Pull Rates page CTAs

Every web anchor on the hub points at `https://www.packrip.co/...` — `www` is the host the web product itself declares canonical (17 occurrences in `pokemon-pack-opening`, none for the bare host), and the bare host answers with a 301 to it. Each carries all four parameters `utm_source=elhanarinc_github`, `utm_medium=referral`, `utm_campaign=packrip_ios_hub`, and `utm_content=<PLACEMENT>`, where `<PLACEMENT>` is one of exactly these eight and nothing else:

- `nav_play_web` — landing header nav "Play in browser"
- `hero_play_web` — landing hero secondary CTA
- `era_archive` — landing era-archive section
- `bridge_web` — landing web/iOS bridge column CTA
- `cta_play_web` — landing final conversion block secondary CTA
- `rates_explore` — Pull Rates page outbound link
- `support_web` — Support page outbound link
- `footer_web` — the shared footer on all five pages

Every placement gets its own tag. Spec section 7.1 justifies placement-specific tags because the diagnostic value outweighs the maintenance cost, so one tag covering several positions defeats the point — Task 4's review caught three placements sharing `hero_play_web` and two sharing both `footer_web` and `packrip_ios_github_cta`.

### Facts that may be published

Verified against the live App Store listing (`packrip-ios/ASC/metadata/1.2.5/version/1.2.5/en-US.json`, `ASC/metadata/app-info/en-US.json`) and the live server config (`packrip-ios/Worker/config/gameplay.json`):

- Subtitle, verbatim: `Booster Pack Opening Simulator`
- Every set is unlocked from the start.
- Nine rarity tiers, named exactly: Common, Uncommon, Rare, Holo Rare, Holo EX, Rare Secret, Shining, Gold Star, Crystal.
- Foil variants roll independently on every card and sell for more than the base card.
- Free packs arrive every day.
- Pity guarantees exist and expose a visible counter in the app.
- The Forge scraps duplicates into shards and crafts missing cards.
- Binder view, nine cards a page.
- Wishlist hearts feed Hunt Packs, which target a specific missing card.
- Set checklists with Owned / Missing / Foils filters, completion bars, and milestone coin rewards.
- 16 collectible Seals, each granting a permanent gameplay perk.
- Daily, weekly, and Super quests with coin rewards.
- Daily challenge leaderboard and trainer identity (title, name colour).
- One-tap portrait PNG share of a pack rip.
- Cloud sync with no signup, no account, and no e-mail.
- Server-driven content: new sets arrive without an app update.
- Pull rates are shown in the app before any purchase, and the in-app view is authoritative.
- Web and iOS progress do not synchronize. They are separate saves.

### Facts that must NOT be published

These are either volatile, unverified in this repository, or contradicted by the live server config. Publishing any of them is a task failure.

- Any numeric daily-free-pack count. The listing states only that Plus grants "4 extra daily packs (7 total)"; the baseline is a derived number and may be retuned from KV without a release.
- Any numeric pity threshold. `Worker/config/gameplay.json` carries thresholds only for `holo`, `holoEx`, `shining`, and `goldStar` — the retired site's "Rare Secret after 80 packs" and "Crystal after 200 packs" are fabrications.
- Any Plus multiplier. The listing says 1.5× XP while the live config says 1.75, and sell/streak values disagree too. Describe Plus perks qualitatively and point to the in-app paywall.
- Any IAP price, currency amount, or `offers` block in JSON-LD. Prices vary by territory and are not evidenced in this repository.
- `aggregateRating`, `ratingCount`, `reviewCount`, `softwareVersion`, current app version, catalog set count, or card count.
- Any claim that the app has no ads, no analytics, no tracking, or no leaderboards. All four are contradicted by shipped releases.
- Any wording that implies web and iOS progress are shared, synced, transferable, or the same collection.
- Any claim that the iOS app contains licensed Pokémon cards, or that it is official, endorsed, or affiliated.

### Copy coherence rule for Pokémon context

The live App Store description states "All card art is AI-generated and original to PackRip." The hub therefore attributes Pokémon-era imagery to its real source and never to the iOS binary:

- Pokémon booster-wrapper art on the hub is always introduced as era artwork from the PackRip web archive at `packrip.co`, and its `alt` text names the set, not the app.
- iOS screenshots are always labelled as the iOS app.
- The hero positions PackRip as one Pokémon TCG pack-opening brand across two products: the browser simulator and the iPhone app.
- Every page footer carries the fan-made and trademark disclosure defined in Task 3.

Never write a sentence that claims the iOS app ships licensed Pokémon cards.

### Design system

- Ground: deep navy ink. Primary accent: brass gold. Era accents: restrained blue, red, green, violet.
- Display face: `Bodoni Moda`. Body, UI, and data face: `Archivo`. No third family.
- Structural device: binder-divider tabs labelled with era name and year range. Years carry real chronological information; decorative `01 / 02 / 03` numbering is forbidden.
- Signature element: the era archive rail — real sealed booster wrappers in chronological order, each behind a binder tab, lifting on hover and focus. This is the only animated element on the site.
- Field Guide variant for Pull Rates, Support, Privacy, and Terms: same tokens and chrome, narrower measure, higher text contrast, anchored sections, `<dl>` instead of wide tables on narrow screens.

### Accessibility and robustness floor

- Fully usable at 320 CSS px. Primary controls at least 44×44 CSS px.
- Body copy at least 16 px on reading pages; no text below 12 px anywhere.
- Visible keyboard focus on every interactive element. Skip link and semantic landmarks on every page.
- Decorative images use `alt=""`; informational images use specific `alt`.
- Every `<img>` carries explicit `width` and `height`.
- Readable with CSS, images, or JavaScript unavailable. No page runs any JavaScript.
- `prefers-reduced-motion: reduce` removes every transform and transition.
- Colour is never the only carrier of rarity or state.
- External links that open a new tab carry `rel="noopener"`. Internal and legal navigation never forces a new tab.

### Out of scope — do not do these

- Do not change or redirect the `/packrip-cards/` path.
- Do not change, recaption, or re-render the App Store screenshots at `packrip-cards/images/screens/01.jpg`–`07.jpg`.
- Do not add a backend, account system, newsletter, e-mail capture, social channel, paid acquisition surface, or save synchronization.
- Do not refactor gameplay or broad design in `pokemon-pack-opening`; the only change there is the reverse backlink and its required cache bump.
- Do not edit anything under `pokemon-pack-opening/dist/` by hand.
- Do not change `pokemon-pack-opening/src/config/iosLaunch.ts`, including its `packrip-cards` slug. Task 1 records the slug question as evidence only.
- Do not `git push` and do not deploy. Task 12 ends at a checkpoint.
- Do not hand-edit any brain `MEMORY.md` and do not run `reindex.mjs`.
- Do not change a commit message's Conventional Commit type. The repository's
  `commit-msg` hook accepts only `build|ci|docs|feat|fix|perf|refactor|style|test` and
  rejects `chore`. Every commit message in this plan already uses an accepted type
  (`docs`, `feat`, `fix`, `test`); Task 1 discovered the hook the hard way.

---

## File Structure

### `elhanarinc.github.io` (primary)

- Create `docs/superpowers/evidence/2026-08-20-packrip-live-facts.md` — frozen snapshot of live App Store, config, and web evidence with the commands that produced it.
- Create `Scripts/audit-packrip.py` — executable product-fact, identity, attribution, asset, and JSON-LD contract for the hub.
- Create `packrip-cards/images/eras/*.webp` — seven repository-owned era booster wrappers copied from the web repo.
- Rewrite `packrip-cards/_shared.css` — Collector Archive tokens, chrome, era rail, Field Guide variant.
- Rewrite `packrip-cards/index.html` — landing page, nine fixed sections.
- Rewrite `packrip-cards/rarity.html` — Pull Rates field guide.
- Rewrite `packrip-cards/support.html` — support answers plus a matching `FAQPage`.
- Rewrite `packrip-cards/privacy.html` — privacy reconciled with the 1.2.5 analytics change.
- Rewrite `packrip-cards/terms.html` — terms reconciled with the fan-made framing and price-free billing text.
- Rewrite `packrip-cards/llms.txt` — per-product atomic facts.
- Modify `index.html` — portfolio `Now` bullet, featured card copy, app card copy, `ItemList` entry.
- Modify `404.html` — product name in the link row.
- Modify `README.md` — replace the Mythos PackRip section.
- Modify `llms.txt` — PackRip section and editorial note.
- Modify `llms-full.txt` — PackRip atomic facts.
- Regenerate `sitemap.xml` — `lastmod` refresh, after the HTML commits.
- Modify `.github/workflows/seo-checks.yml` — add the auditor to `validate-html`; add the three missing hub URLs to the PSI matrix.

### `pokemon-pack-opening` (secondary, backlink only)

- Modify `src/components/screens/IosLaunchScreen.tsx` — visible crawlable "Official iPhone app details & support" link.
- Modify `scripts/prerender.mjs` — the same link inside the `/ios` prerendered `noscript` block.
- Modify `public/sw.js` — `CACHE_NAME` bump, required by repo rules for any shipped source change.

---

## Task 1: Evidence snapshot and the executable fact contract

Builds the auditor first so every later task has a real failing check, and freezes the live facts the copy will be written against.

**Files:**
- Create: `docs/superpowers/evidence/2026-08-20-packrip-live-facts.md`
- Create: `Scripts/audit-packrip.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `python3 Scripts/audit-packrip.py [--page PATH ...] [--corpus] [--quiet]`, exit `0` clean / `1` findings. Module-level constants other tasks read but never change: `APP_STORE_BASE`, `PROVIDER_TOKEN`, `ALLOWED_CT`, `ALLOWED_UTM_CONTENT`, `UTM_FIXED`, `PAGES`, `STALE_TERMS`, `FORBIDDEN_NUMERIC_CLAIMS`, `SYNC_CLAIMS`, `FORBIDDEN_JSONLD_KEYS`.

- [ ] **Step 1: Capture the live App Store facts**

Run, from the repo root:

```bash
mkdir -p docs/superpowers/evidence
curl -s 'https://itunes.apple.com/lookup?id=6763404045&country=us' \
  | python3 -c 'import json,sys; r=json.load(sys.stdin)["results"][0]; print(json.dumps({k:r.get(k) for k in ("trackName","trackViewUrl","sellerName","minimumOsVersion","trackContentRating","contentAdvisoryRating","primaryGenreName","genres","languageCodesISO2A","supportedDevices","currentVersionReleaseDate","formattedPrice","artistViewUrl")}, indent=2, ensure_ascii=False))'
```

Expected: a JSON object whose `trackName` is `PackRip: TCG Card Packs`. Record `trackViewUrl` (it settles the `packrip-tcg-card-packs` vs `packrip-cards` slug question), `minimumOsVersion`, `trackContentRating`, and `contentAdvisoryRating` verbatim.

If the endpoint is unreachable or returns `resultCount: 0`, write `UNMEASURED` for every field, and for the rest of the plan treat the spec's locked values as authoritative: name `PackRip: TCG Card Packs`, canonical slug `packrip-tcg-card-packs`, minimum OS `iOS 17.0`. Do not invent an age rating — in that case Task 7 omits the numeric rating sentence entirely.

- [ ] **Step 2: Capture the live server-config facts**

```bash
python3 -c "
import json
d=json.load(open('../packrip-ios/Worker/config/gameplay.json'))
print('pity thresholds :', d['pity']['thresholds'])
print('foil rates      :', d['foil']['rates'])
print('foil multiplier :', d['foil']['sellMultiplier'])
print('pull rates      :', d['pullRates'])
print('hunt rates      :', d['huntRates'])
print('plus perks      :', d['plusPerks'])
print('forge enabled   :', d['forge']['enabled'])
print('setCompletion   :', d['setCompletion']['milestones'])
"
```

Expected output includes exactly:

```
pity thresholds : {'holo': 20, 'holoEx': 50, 'shining': 150, 'goldStar': 150}
plus perks      : {'xpMultiplier': 1.75, 'dailyPackBonus': 4, 'sellRateMultiplier': 1.5, 'streakCoinMultiplier': 2.5}
```

The absent `rareSecret` and `crystal` pity keys, and the `1.75` versus listing `1.5×` XP disagreement, are the reason the Global Constraints forbid publishing those numbers.

- [ ] **Step 3: Capture the web-product link targets**

```bash
for p in / /sets /faq /pull-rate/base1/holo-rare; do
  printf '%s -> ' "$p"
  curl -s -o /dev/null -w '%{http_code}\n' "https://packrip.co${p}"
done
```

Expected: `301` for each bare-host path, with a `location` header that preserves the query string, and `200` when the same path is requested on `https://www.packrip.co/`. Verified 2026-08-20: the redirect does preserve UTM parameters, and all four `www` paths return 200. Because `www` is canonical for that site, every hub anchor targets `www` directly rather than eating the hop. If a `www` path itself returns anything other than 200, drop that target from the link plan and fall back to `https://www.packrip.co/` with the same `utm_content`.

- [ ] **Step 4: Write the evidence snapshot**

Create `docs/superpowers/evidence/2026-08-20-packrip-live-facts.md` with these exact section headings, filling each from the command output above: `## Command log`, `## Live App Store listing`, `## Live gameplay config`, `## Frozen App Store screenshots`, `## Web-product link targets`, `## Known conflicts carried into the copy`, `## Re-check trigger`.

Under `## Frozen App Store screenshots`, record verbatim that `packrip-ios/ASC/screenshot-captions.json` captions the shipped screenshots "Open Mythology Booster Packs" and "Greek, Norse, Egyptian & Beyond", that the screenshots are frozen by owner decision, and that the hub therefore labels them as iOS-app screenshots without repeating their captions.

Under `## Known conflicts carried into the copy`, record all four: the Mythos screenshot captions against the Pokémon hub framing; the listing's "all card art is original to PackRip" against the Pokémon era wrappers, resolved by the Global Constraints copy coherence rule; the `1.5×` versus `1.75` XP disagreement; and the `iosLaunch.ts` slug mismatch that is deliberately left untouched.

Under `## Re-check trigger`, write: "This snapshot is void if the App Store listing name, subtitle, or description changes, if `Worker/config/gameplay.json` pity or plusPerks values change, or if the App Store screenshots are re-rendered."

- [ ] **Step 5: Write the failing audit — the script**

Create `Scripts/audit-packrip.py`:

```python
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
```

- [ ] **Step 6: Run the audit to verify it fails against the current site**

Run: `python3 Scripts/audit-packrip.py`

Expected: FAIL. The output must include, among many others, findings of the shape:

```
FAIL packrip-cards/index.html: stale term 'PackRip: Cards' at offset ...
FAIL packrip-cards/index.html: forbidden claim 'five free daily packs' at offset ...
FAIL packrip-cards/index.html: App Store link missing pt=127914124: https://apps.apple.com/us/app/id6763404045
FAIL packrip-cards/index.html: img without explicit width/height: /packrip-cards/images/screens/01.jpg
FAIL packrip-cards/index.html: missing skip link to #main
FAIL packrip-cards/index.html: no packrip.co link on a conversion page
FAIL packrip-cards/rarity.html: forbidden claim '200 packs' at offset ...
FAIL README.md:29: PackRip line carries 'Mythology'
```

and a non-zero exit. Confirm with `python3 Scripts/audit-packrip.py; echo "exit=$?"` printing `exit=1`.

- [ ] **Step 7: Verify the auditor is self-consistent on a page it should pass**

The auditor must not be trivially broken. Prove its parsing works by checking it produces zero findings for a minimal synthetic page:

```bash
mkdir -p /tmp/audit-probe/packrip-cards && cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io && python3 - <<'PY'
import pathlib, sys
sys.path.insert(0, "Scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("aud", "Scripts/audit-packrip.py")
aud = importlib.util.module_from_spec(spec); spec.loader.exec_module(aud)
probe = """<!doctype html><html lang="en"><head>
<meta name="description" content="d"><meta name="robots" content="index,follow">
<meta name="apple-itunes-app" content="app-id=6763404045">
<meta property="og:type" content="website"><meta property="og:title" content="t">
<meta property="og:description" content="d"><meta property="og:image" content="i">
<meta property="og:site_name" content="PackRip: TCG Card Packs">
<meta property="og:url" content="https://elhanarinc.github.io/packrip-cards/terms.html">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="t">
<meta name="twitter:description" content="d"><meta name="twitter:image" content="i">
<link rel="canonical" href="https://elhanarinc.github.io/packrip-cards/terms.html">
<link rel="icon" href="/packrip-cards/images/app-icon.png">
<link rel="apple-touch-icon" href="/packrip-cards/images/app-icon.png">
</head><body><a href="#main">Skip</a><header></header><main id="main"></main><footer></footer></body></html>"""
p = pathlib.Path("packrip-cards/_probe.html"); p.write_text(probe)
f = []
aud.audit_page("packrip-cards/_probe.html", f)
p.unlink()
print("probe findings:", f or "none")
sys.exit(1 if f else 0)
PY
```

Expected: `probe findings: none` and exit 0. If the probe reports findings, the auditor has a false positive — fix the auditor, not the probe.

- [ ] **Step 8: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add Scripts/audit-packrip.py docs/superpowers/evidence/2026-08-20-packrip-live-facts.md
git commit -m "test(packrip): Add the iOS hub fact and attribution auditor

The auditor fails against the current Mythos-era pages by design; the
following commits make it pass. Evidence snapshot records the live App
Store listing and gameplay config the copy is written against."
```

---
## Task 2: Repository-owned era assets and the social card

Copies seven era booster wrappers out of the sibling web repo and generates one Open Graph card, so no page ever hotlinks a third-party image and every image has a known intrinsic box.

**Files:**
- Create: `packrip-cards/images/eras/era-1999-wotc.webp`
- Create: `packrip-cards/images/eras/era-2000-neo.webp`
- Create: `packrip-cards/images/eras/era-2002-ecard.webp`
- Create: `packrip-cards/images/eras/era-2003-ex.webp`
- Create: `packrip-cards/images/eras/era-2007-dp.webp`
- Create: `packrip-cards/images/eras/era-2011-bw.webp`
- Create: `packrip-cards/images/eras/era-2017-modern.webp`
- Create: `packrip-cards/images/og-cover.png`
- Read only, never modified: `packrip-cards/images/app-icon.png` (1024×1024), `packrip-cards/images/screens/01.jpg`–`07.jpg` (607×1320 each)

**Interfaces:**
- Consumes: nothing from Task 1.
- Produces: the seven era files with the exact intrinsic dimensions listed in Step 2, consumed verbatim as `width`/`height` attributes by Task 4; and `og-cover.png` at 1200×630, consumed as `og:image` by Tasks 4–8.

- [ ] **Step 1: Verify every source asset exists before copying**

```bash
cd /Users/appsamurai/Desktop/personal-projects/pokemon-pack-opening/public/images/packs
for f in base1-charizard.webp neo1-1stedition.webp ecard3-ho-oh.webp \
         ex1-lairon.webp dp1-dialga.webp bw1-reshiram.webp sv1-koraidon.webp; do
  [ -f "$f" ] && echo "OK   $f" || echo "MISS $f"
done
```

Expected: seven `OK` lines. A `MISS` line means the web repo's asset set moved; pick the largest remaining `.webp` with the same set-id prefix and record the substitution in the evidence file.

- [ ] **Step 2: Copy the seven era wrappers**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
mkdir -p packrip-cards/images/eras
SRC=../pokemon-pack-opening/public/images/packs
cp "$SRC/base1-charizard.webp"  packrip-cards/images/eras/era-1999-wotc.webp
cp "$SRC/neo1-1stedition.webp"  packrip-cards/images/eras/era-2000-neo.webp
cp "$SRC/ecard3-ho-oh.webp"     packrip-cards/images/eras/era-2002-ecard.webp
cp "$SRC/ex1-lairon.webp"       packrip-cards/images/eras/era-2003-ex.webp
cp "$SRC/dp1-dialga.webp"       packrip-cards/images/eras/era-2007-dp.webp
cp "$SRC/bw1-reshiram.webp"     packrip-cards/images/eras/era-2011-bw.webp
cp "$SRC/sv1-koraidon.webp"     packrip-cards/images/eras/era-2017-modern.webp
ls -la packrip-cards/images/eras/
```

These files are already WebP and already size-appropriate, so they are copied byte-for-byte and never re-encoded. Their intrinsic dimensions, which Task 4 writes into the `width`/`height` attributes, are exactly:

- `era-1999-wotc.webp` — 696 × 1204
- `era-2000-neo.webp` — 906 × 1514
- `era-2002-ecard.webp` — 451 × 800
- `era-2003-ex.webp` — 451 × 800
- `era-2007-dp.webp` — 242 × 412
- `era-2011-bw.webp` — 563 × 1072
- `era-2017-modern.webp` — 780 × 1429

- [ ] **Step 3: Verify the copied dimensions match**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
import struct, pathlib
EXPECT = {
    "era-1999-wotc.webp":   (696, 1204),
    "era-2000-neo.webp":    (906, 1514),
    "era-2002-ecard.webp":  (451, 800),
    "era-2003-ex.webp":     (451, 800),
    "era-2007-dp.webp":     (242, 412),
    "era-2011-bw.webp":     (563, 1072),
    "era-2017-modern.webp": (780, 1429),
}
def dims(p):
    d = p.read_bytes()
    if d[12:16] == b"VP8X":
        return 1 + int.from_bytes(d[24:27], "little"), 1 + int.from_bytes(d[27:30], "little")
    if d[12:16] == b"VP8 ":
        return struct.unpack("<H", d[26:28])[0] & 0x3FFF, struct.unpack("<H", d[28:30])[0] & 0x3FFF
    if d[12:16] == b"VP8L":
        b = int.from_bytes(d[21:25], "little")
        return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
    raise SystemExit(f"{p}: not a recognised WebP")
bad = 0
base = pathlib.Path("packrip-cards/images/eras")
for name, want in EXPECT.items():
    got = dims(base / name)
    flag = "OK " if got == want else "BAD"
    if got != want:
        bad += 1
    print(f"{flag} {name} {got[0]}x{got[1]} (want {want[0]}x{want[1]})")
raise SystemExit(1 if bad else 0)
PY
```

Expected: seven `OK` lines and exit 0. Any `BAD` line means the plan's baked dimensions are stale — update the `width`/`height` values used in Task 4 to the measured values and note the change in the evidence file.

- [ ] **Step 4: Generate the 1200×630 Open Graph card**

The retired pages used the portrait 607×1320 screenshot as `og:image` while declaring `og:image:width` 1320 and `og:image:height` 2868 — wrong on both axes and the wrong aspect for a social card. This step produces a correct one from repository-owned material only.

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
INK, PANEL, VELLUM, BRASS, MUTED = (11, 18, 32), (22, 34, 58), (242, 237, 225), (201, 162, 39), (169, 180, 201)

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# Archive drawer: a brass hairline frame inset from the edge.
d.rectangle([28, 28, W - 29, H - 29], outline=BRASS, width=2)
d.rectangle([40, 40, W - 41, H - 41], outline=(30, 44, 73), width=1)

# App icon, left, on a raised panel.
icon = Image.open("packrip-cards/images/app-icon.png").convert("RGB").resize((196, 196), Image.LANCZOS)
d.rectangle([84, 210, 84 + 216, 210 + 216], fill=PANEL)
img.paste(icon, (94, 220))

didot = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 74)
helv_b = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 27, index=1)
helv = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 25)
helv_s = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20, index=1)

x = 350
d.text((x, 196), "T H E   A R C H I V E", font=helv_s, fill=BRASS)
d.text((x, 236), "PackRip:", font=didot, fill=VELLUM)
d.text((x, 316), "TCG Card Packs", font=didot, fill=VELLUM)
d.text((x, 416), "Booster Pack Opening Simulator", font=helv_b, fill=MUTED)
d.line([x, 466, x + 470, 466], fill=(30, 44, 73), width=1)
d.text((x, 484), "Every era. One fresh binder.  ·  iPhone", font=helv, fill=MUTED)

img.save("packrip-cards/images/og-cover.png", optimize=True)
print("wrote packrip-cards/images/og-cover.png", img.size)
PY
```

Expected: `wrote packrip-cards/images/og-cover.png (1200, 630)`.

If PIL, `Didot.ttc`, or `HelveticaNeue.ttc` is unavailable in the execution environment, do not substitute a fabricated card and do not hotlink anything: instead set `og:image` on every page to `https://elhanarinc.github.io/packrip-cards/images/app-icon.png` with `og:image:width` 1024 and `og:image:height` 1024, change `twitter:card` from `summary_large_image` to `summary` on all five pages, and record the fallback in the evidence file.

- [ ] **Step 5: Verify the card and confirm no third-party imagery entered the tree**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 -c "
from PIL import Image
im = Image.open('packrip-cards/images/og-cover.png')
print('og-cover:', im.size, im.mode)
assert im.size == (1200, 630), im.size
"
du -sh packrip-cards/images/eras packrip-cards/images/og-cover.png
grep -rhoE '(src|content)="https?://[^"]+' packrip-cards/ \
  | grep -vE '^(src|content)="https://elhanarinc\.github\.io/' \
  || echo "no remote image or asset references"
```

Expected: `og-cover: (1200, 630) RGB`, the era directory around 500K, and `no remote image or asset references`.

The grep is narrow on purpose, and both narrowings were learned from a false failure:

- It matches only `src=` and `content=`, never `href=`. Every page legitimately carries remote `href` values — the Google Fonts stylesheet, Apple's EULA, RevenueCat's privacy policy — and including `href` makes this check fail on correct work.
- It matches attributes, not hostnames in prose. Task 7's privacy page legitimately names `cdn4.buysellads.net` in its disclosure text, so a hostname-based grep would false-fail once that task lands.
- Self-referential absolute URLs are excluded, because `og:image` and `twitter:image` must be absolute and point at this site.

What remains is exactly the thing that must never happen: an `<img>`, or an `og:image`/`twitter:image`, pointing at somebody else's host. Verified 2026-08-20 that this form reports clean on the current tree and still catches a planted `src="https://images.pokemontcg.io/..."` hotlink. Note that `Scripts/audit-packrip.py` independently fails any `<img src>` on a remote host, so this grep is a second net over the `og:image`/`twitter:image` surface the auditor does not parse.

- [ ] **Step 6: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add packrip-cards/images/eras packrip-cards/images/og-cover.png
git commit -m "feat(packrip): Add repository-owned era wrappers and a real OG card

Seven era booster wrappers copied byte-for-byte from the web repo's own
asset set, plus a 1200x630 social card built from the app icon. The old
pages used a 607x1320 screenshot as og:image while declaring 1320x2868."
```

---

## Task 3: Collector Archive stylesheet

Replaces the shared stylesheet with the approved visual system, including the Field Guide variant the four reading pages use and the reduced-motion contract every later task depends on.

**Files:**
- Rewrite: `packrip-cards/_shared.css` (currently 101 lines)

**Interfaces:**
- Consumes: the era files from Task 2 (referenced only from HTML, never from CSS).
- Produces the class contract every later task writes markup against, and nothing may invent a class outside it:
  - Chrome: `.skip`, `.site-head`, `.brand`, `.nav-links`, `.wrap`, `.site-foot`, `.foot-nav`, `.legal`
  - Buttons: `.cta`, `.cta--primary`, `.cta--ghost`, `.cta-row`
  - Landing: `.hero`, `.hero-grid`, `.hero-copy`, `.hero-shot`, `.kicker`, `.lede`, `.ledger`, `.block`, `.block-head`, `.block-sub`, `.rail`, `.era`, `.era--wotc`, `.era--neo`, `.era--ecard`, `.era--ex`, `.era--dp`, `.era--bw`, `.era--modern`, `.era-tab`, `.era-name`, `.era-year`, `.era-wrap`, `.era-cap`, `.cards`, `.card`, `.card-label`, `.shots`, `.bridge`, `.bridge-col`
  - Field Guide: `body.field-guide`, `.prose`, `.anchor`, `.note`, `.odds`, `.odds-row`, `.tier-mark`, plus tier-mark modifiers `.tier-mark--common`, `--rare`, `--holo`, `--holoex`, `--secret`, `--shining`, `--goldstar`, `--crystal`, `--foil`

  There is no visually-hidden or tabular-numeral utility class, because nothing in Tasks 4–8 needs one: tier swatches use `aria-hidden`, permalinks use `aria-label`, and the two places that want lining figures set `font-variant-numeric` directly. Do not add a class that no page uses.

  Note that the `tag` class appearing in Task 9's root-portfolio markup belongs to the root page's own stylesheet, not to this contract — Task 9 edits `index.html`, which never loads `packrip-cards/_shared.css`.

- [ ] **Step 1: Write the failing check**

The stylesheet has no test runner, so its contract is checked by assertion over the file itself. Create nothing new — run this check now, before writing the CSS, to confirm it fails:

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
import pathlib, re, sys
css = pathlib.Path("packrip-cards/_shared.css").read_text()
required_tokens = ["--ink:", "--brass:", "--vellum:", "--era-wotc:", "--era-modern:",
                   "--measure-read:"]
required_rules = [r"prefers-reduced-motion:\s*reduce", r":focus-visible",
                  r"\.skip", r"\.era-tab", r"\.rail", r"\.odds-row",
                  r"body\.field-guide", r"min-height:\s*44px",
                  r"Bodoni Moda", r"Archivo"]
# "Inter" is checked as a bare substring on purpose: the retired stylesheet named the
# family directly, and the replacement must not reintroduce it. Verified not to collide
# with any word in the new sheet.
missing = [t for t in required_tokens if t not in css]
missing += [r for r in required_rules if not re.search(r, css)]
forbidden = [f for f in ("Cormorant Garamond", "Inter", "background-clip: text",
                         "border-radius: 999px", "999px") if f in css]
for m in missing:
    print("FAIL missing:", m)
for f in forbidden:
    print("FAIL retired token still present:", f)
sys.exit(1 if (missing or forbidden) else 0)
PY
```

Expected: FAIL, listing every required token as missing and `Cormorant Garamond`, `Inter`, `background-clip: text`, and `999px` as retired tokens still present. Exit code 1.

- [ ] **Step 2: Write the stylesheet**

Replace the entire contents of `packrip-cards/_shared.css` with:

```css
/* PackRip: TCG Card Packs — Collector Archive
   One stylesheet for all five hub pages. No page on this site runs JavaScript.
   The four reading pages add `field-guide` to <body> for the narrower,
   higher-contrast variant of the same system. */

:root {
  /* Ground: the navy drawer the archive lives in. */
  --ink:        #0b1220;
  --ink-2:      #101a2c;
  --panel:      #16223a;
  --panel-lift: #1d2c49;

  /* Paper and type. */
  --vellum:     #f2ede1;
  --read:       #e6e0d2;
  --muted:      #a9b4c9;
  --subtle:     #7d89a1;

  /* Brass: the single conversion and rarity accent. */
  --brass:      #c9a227;
  --brass-lift: #e8c86a;
  --brass-dim:  rgba(201, 162, 39, 0.26);

  /* Era accents, in chronological order. Restrained on purpose. */
  --era-wotc:   #3f7cac;
  --era-neo:    #4f8f6c;
  --era-ecard:  #7b5ea7;
  --era-ex:     #b4534a;
  --era-dp:     #4a80a8;
  --era-bw:     #6f7f96;
  --era-modern: #b08a3e;

  --rule:       rgba(242, 237, 225, 0.10);
  --rule-firm:  rgba(242, 237, 225, 0.20);

  --measure:      74ch;
  --measure-read: 64ch;
  --radius:       4px;

  --display: 'Bodoni Moda', 'Didot', 'Times New Roman', serif;
  --ui:      'Archivo', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }
* { margin: 0; padding: 0; }

html {
  color-scheme: dark;
  -webkit-text-size-adjust: 100%;
}

body {
  min-height: 100vh;
  background: var(--ink);
  color: var(--vellum);
  font: 400 17px/1.65 var(--ui);
  -webkit-font-smoothing: antialiased;
}

/* One quiet atmospheric layer: brass light entering the drawer from
   above-right. Sits behind everything and never animates. */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background:
    radial-gradient(1100px 520px at 82% -14%, rgba(201, 162, 39, 0.10), transparent 62%),
    radial-gradient(760px 480px at -8% 22%, rgba(63, 124, 172, 0.08), transparent 62%);
}

a { color: inherit; text-decoration: none; }

img { max-width: 100%; }

.wrap { width: min(1080px, calc(100% - 40px)); margin-inline: auto; }

/* ---------- Focus and skip link ---------- */

/* Focus ring. `:where()` holds this at zero specificity on purpose, so a
   page-level rule can intentionally restyle one control's focus. The cost is
   that ANY later rule touching `outline` on a focused control wins silently —
   if you add one, restate the ring there. Nothing in this file overrides it. */
:where(a, button, summary, [tabindex]):focus-visible {
  outline: 2px solid var(--brass-lift);
  outline-offset: 3px;
  border-radius: 2px;
}

.skip {
  position: absolute;
  left: 12px; top: -60px;
  z-index: 20;
  background: var(--brass);
  color: #0b1220;
  font: 600 15px/1 var(--ui);
  padding: 14px 18px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  border-radius: var(--radius);
  transition: top 160ms ease;
}
.skip:focus { top: 12px; }

/* ---------- Header ---------- */

.site-head {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(11, 18, 32, 0.92);
  border-bottom: 1px solid var(--rule);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.site-head .wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
  padding: 10px 0;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-height: 44px;
  font: 600 16px/1.15 var(--display);
  letter-spacing: 0.01em;
}
.brand img { width: 30px; height: 30px; border-radius: 7px; }

.nav-links {
  display: flex;
  align-items: center;
  gap: 2px;
  overflow-x: auto;
  scrollbar-width: none;
  -webkit-overflow-scrolling: touch;
}
.nav-links::-webkit-scrollbar { display: none; }

.nav-links a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding: 0 12px;
  color: var(--muted);
  font: 600 12px/1 var(--ui);
  text-transform: uppercase;
  letter-spacing: 0.13em;
  white-space: nowrap;
  border-bottom: 2px solid transparent;
}
.nav-links a:hover { color: var(--vellum); border-bottom-color: var(--brass); }
.nav-links a[aria-current='page'] { color: var(--vellum); border-bottom-color: var(--brass); }

/* ---------- Calls to action ---------- */

.cta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  min-height: 44px;
  padding: 12px 22px;
  border-radius: var(--radius);
  font: 600 16px/1.1 var(--ui);
  border: 1px solid var(--brass);
}

.cta--primary {
  background: var(--brass);
  color: #0b1220;
}
.cta--primary:hover { background: var(--brass-lift); }

.cta--ghost {
  background: transparent;
  color: var(--vellum);
  border-color: var(--rule-firm);
}
.cta--ghost:hover { border-color: var(--brass); }

/* ---------- Landing: hero ---------- */

main { display: block; }

.hero { padding: 58px 0 0; }

.hero-grid {
  display: grid;
  grid-template-columns: 1.08fr 0.92fr;
  gap: 52px;
  align-items: center;
}

.kicker {
  font: 600 12px/1 var(--ui);
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--brass);
}

.hero-copy h1 {
  margin-top: 16px;
  font: 600 clamp(36px, 6vw, 62px) / 1.02 var(--display);
  letter-spacing: -0.015em;
}

.lede {
  margin-top: 20px;
  max-width: 48ch;
  color: var(--muted);
  font-size: 18px;
}

.hero-copy .cta-row { margin-top: 28px; }

.hero-shot {
  position: relative;
  justify-self: center;
  width: min(320px, 100%);
  padding: 14px;
  background: var(--ink-2);
  border: 1px solid var(--rule-firm);
  border-radius: var(--radius);
}
.hero-shot img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 2px;
}
.hero-shot figcaption {
  margin-top: 12px;
  color: var(--subtle);
  font: 600 12px/1.4 var(--ui);
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

/* ---------- Landing: truth ledger ---------- */

.ledger {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  margin-top: 52px;
  border-top: 1px solid var(--rule-firm);
}
.ledger > div {
  padding: 18px 20px 20px 0;
  border-right: 1px solid var(--rule);
}
.ledger > div:last-child { border-right: none; padding-right: 0; }
.ledger dt {
  font: 600 12px/1.3 var(--ui);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--brass);
}
.ledger dd { margin-top: 8px; font-size: 16px; color: var(--vellum); }

/* ---------- Landing: sections ---------- */

.block { margin-top: 76px; }

.block-head {
  font: 600 clamp(26px, 3.6vw, 37px) / 1.1 var(--display);
  letter-spacing: -0.01em;
}
.block-sub {
  margin-top: 10px;
  max-width: var(--measure);
  color: var(--muted);
}

/* ---------- Signature: the era archive rail ---------- */

.rail {
  display: flex;
  gap: 16px;
  margin-top: 28px;
  padding-bottom: 12px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.era {
  flex: 0 0 auto;
  width: 176px;
  scroll-snap-align: start;
  --era: var(--brass);
}
.era--wotc   { --era: var(--era-wotc); }
.era--neo    { --era: var(--era-neo); }
.era--ecard  { --era: var(--era-ecard); }
.era--ex     { --era: var(--era-ex); }
.era--dp     { --era: var(--era-dp); }
.era--bw     { --era: var(--era-bw); }
.era--modern { --era: var(--era-modern); }

/* Binder divider tab. The colour band is decoration; the era name and the
   year range carry the information. */
.era-tab {
  border: 1px solid var(--rule-firm);
  border-bottom: none;
  border-top: 3px solid var(--era);
  border-radius: 3px 3px 0 0;
  background: var(--panel);
  padding: 9px 11px 8px;
}
.era-name {
  display: block;
  font: 600 12px/1.25 var(--ui);
  text-transform: uppercase;
  letter-spacing: 0.13em;
  color: var(--vellum);
}
.era-year {
  display: block;
  margin-top: 3px;
  font: 400 12px/1.2 var(--ui);
  letter-spacing: 0.08em;
  color: var(--subtle);
  font-variant-numeric: tabular-nums;
}

.era-wrap {
  border: 1px solid var(--rule-firm);
  border-top: none;
  border-radius: 0 0 var(--radius) var(--radius);
  background: var(--ink-2);
  padding: 12px;
  overflow: hidden;
}
.era-wrap img {
  display: block;
  width: 100%;
  height: auto;
  transform-origin: 50% 100%;
  transition: transform 420ms cubic-bezier(0.2, 0.7, 0, 1);
}
.era:hover .era-wrap img,
.era:focus-within .era-wrap img {
  transform: translateY(-7px) rotate(-1.2deg) scale(1.02);
}

.era-cap {
  margin-top: 20px;
  max-width: var(--measure);
  color: var(--subtle);
  font-size: 15px;
}

/* ---------- Landing: feature cards ---------- */

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(232px, 1fr));
  gap: 1px;
  margin-top: 28px;
  background: var(--rule);
  border: 1px solid var(--rule);
}
.card { background: var(--ink); padding: 22px 20px 24px; }
.card-label {
  display: block;
  font: 600 12px/1 var(--ui);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--brass);
}
.card h3 { margin-top: 12px; font: 600 17px/1.35 var(--ui); }
.card p { margin-top: 8px; color: var(--muted); font-size: 15.5px; }

/* ---------- Landing: screenshot strip ---------- */

.shots {
  display: flex;
  gap: 14px;
  margin-top: 28px;
  padding-bottom: 12px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
}
.shots figure {
  flex: 0 0 auto;
  width: 208px;
  scroll-snap-align: start;
}
.shots img {
  display: block;
  width: 100%;
  height: auto;
  border: 1px solid var(--rule-firm);
  border-radius: var(--radius);
}
.shots figcaption {
  margin-top: 10px;
  color: var(--subtle);
  font-size: 14px;
}

/* ---------- Landing: web / iOS bridge ---------- */

.bridge {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  margin-top: 28px;
  background: var(--rule);
  border: 1px solid var(--rule);
}
.bridge-col { background: var(--ink); padding: 24px 22px 26px; }
.bridge-col h3 { font: 600 clamp(20px, 2.4vw, 25px)/1.2 var(--display); }
.bridge-col ul { margin-top: 14px; padding-left: 18px; color: var(--muted); }
.bridge-col li { margin-top: 7px; }
.bridge-col .cta-row { margin-top: 20px; }

/* ---------- Footer ---------- */

.site-foot {
  margin-top: 88px;
  border-top: 1px solid var(--rule-firm);
  padding: 30px 0 56px;
  color: var(--subtle);
  font-size: 14.5px;
}
.foot-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 2px 6px;
  margin-bottom: 16px;
}
.foot-nav a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding: 0 10px;
  color: var(--muted);
  border-bottom: 1px solid transparent;
}
.foot-nav a:hover { color: var(--vellum); border-bottom-color: var(--brass); }
.legal { max-width: var(--measure); margin-top: 10px; font-size: 13.5px; line-height: 1.6; }
.legal + .legal { margin-top: 10px; }

/* ---------- Field Guide variant ---------- */

body.field-guide .wrap { width: min(880px, calc(100% - 40px)); }
body.field-guide main { padding-top: 46px; }

.prose { max-width: var(--measure-read); }
.prose h1 {
  font: 600 clamp(32px, 5vw, 50px)/1.05 var(--display);
  letter-spacing: -0.015em;
}
.prose > p.lede { color: var(--read); max-width: var(--measure-read); }
.prose h2 {
  margin-top: 44px;
  font: 600 clamp(23px, 3vw, 30px)/1.2 var(--display);
  scroll-margin-top: 88px;
}
.prose h3 {
  margin-top: 26px;
  font: 600 16px/1.4 var(--ui);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--brass);
}
.prose p, .prose li { color: var(--read); font-size: 17px; }
.prose p { margin-top: 14px; }
.prose ul, .prose ol { margin-top: 14px; padding-left: 20px; }
.prose li { margin-top: 8px; }
.prose strong { color: #fbf8f1; font-weight: 600; }
.prose a:not(.cta) {
  color: var(--brass-lift);
  border-bottom: 1px solid var(--brass-dim);
}
.prose a:not(.cta):hover { border-bottom-color: var(--brass-lift); }
.prose .cta-row { margin-top: 28px; }

/* Section permalink. Deliberately NOT forced to the 44x44 control floor: it sits
   inline inside a heading, which is WCAG 2.5.8's "target in a sentence or block
   of text" exception, and a min-height on an inline element distorts the
   heading's line box. Horizontal padding widens the hit area instead. The 12px
   ancillary-label floor is enforced with max(), because 0.68em of an h3 would
   compute to 10.88px. */
.anchor {
  margin-left: 0.4em;
  padding: 0 4px;
  font-size: max(12px, 0.68em);
  color: var(--brass);
  border-bottom: none !important;
  opacity: 0.45;
}
.anchor:hover, .anchor:focus-visible { opacity: 1; }

.note {
  margin-top: 22px;
  border: 1px solid var(--rule-firm);
  border-left: 3px solid var(--brass);
  border-radius: 0 var(--radius) var(--radius) 0;
  background: var(--panel);
  padding: 16px 18px;
}
.note p { margin-top: 0; }
.note p + p { margin-top: 10px; }

/* Odds and rarity: a definition list, never a wide table, so it reflows
   cleanly at 320px. Every row carries a text label, so the colour mark is
   never the only signal. */
.odds { margin-top: 20px; }
.odds-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 18px;
  padding: 12px 0;
  border-bottom: 1px solid var(--rule);
}
.odds-row dt { color: var(--vellum); font-weight: 600; }
.odds-row dd {
  color: var(--muted);
  text-align: right;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.tier-mark {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin-right: 10px;
  border-radius: 2px;
  background: var(--subtle);
}
.tier-mark--common   { background: var(--era-bw); }
.tier-mark--rare     { background: var(--era-dp); }
.tier-mark--holo     { background: var(--era-wotc); }
.tier-mark--holoex   { background: var(--era-neo); }
.tier-mark--secret   { background: var(--era-ecard); }
.tier-mark--shining  { background: var(--era-ex); }
.tier-mark--goldstar { background: var(--brass); }
.tier-mark--crystal  { background: var(--brass-lift); }
.tier-mark--foil     {
  background: linear-gradient(135deg, var(--era-ecard), var(--brass-lift));
}

/* ---------- Responsive ---------- */

@media (max-width: 900px) {
  .hero-grid { grid-template-columns: 1fr; gap: 34px; }
  .hero-shot { order: -1; }
  .bridge { grid-template-columns: 1fr; }
  .ledger { grid-template-columns: 1fr 1fr; }
  .ledger > div:nth-child(2n) { border-right: none; padding-right: 0; }
}

@media (max-width: 520px) {
  .wrap, body.field-guide .wrap { width: calc(100% - 28px); }
  body { font-size: 16px; }
  .hero { padding-top: 36px; }
  .block { margin-top: 56px; }
  .ledger { grid-template-columns: 1fr; }
  .ledger > div { border-right: none; padding-right: 0; border-bottom: 1px solid var(--rule); }
  .ledger > div:last-child { border-bottom: none; }
  .era { width: 152px; }
  .shots figure { width: 168px; }
  .prose p, .prose li { font-size: 16.5px; }
  .site-head .wrap { padding: 6px 0; }
}

/* ---------- Reduced motion ---------- */

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition: none !important;
    animation: none !important;
    scroll-behavior: auto !important;
  }
  .era:hover .era-wrap img,
  .era:focus-within .era-wrap img { transform: none; }
  .skip { transition: none; }
}

/* ---------- Print ---------- */

@media print {
  body { background: #fff; color: #111; }
  body::before, .site-head, .cta-row, .rail, .shots { display: none; }
  .prose a:not(.cta)::after { content: ' (' attr(href) ')'; font-size: max(12px, 0.85em); }
}
```

- [ ] **Step 3: Run the check to verify it passes**

Run the same Python block from Step 1.

Expected: no output and exit 0. Verify with `... ; echo "exit=$?"` printing `exit=0`.

- [ ] **Step 4: Verify the stylesheet parses and declares no unknown at-rules**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
import pathlib, re, sys
css = pathlib.Path("packrip-cards/_shared.css").read_text()
if css.count("{") != css.count("}"):
    print(f"FAIL unbalanced braces: {css.count('{')} open, {css.count('}')} close")
    sys.exit(1)
allowed_at = {"media", "supports", "font-face", "keyframes"}
bad = [a for a in re.findall(r"@([a-zA-Z-]+)", css) if a not in allowed_at]
if bad:
    print("FAIL unexpected at-rules:", sorted(set(bad)))
    sys.exit(1)
print(f"css ok: {len(css.splitlines())} lines, {css.count('{')} rule blocks")
PY
```

Expected: a single `css ok:` line and exit 0.

- [ ] **Step 5: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add packrip-cards/_shared.css
git commit -m "feat(packrip): Replace the shared stylesheet with Collector Archive

Deep-navy ground, brass accent, era accents, Bodoni Moda over Archivo,
binder-tab structure, and one animated element (the era rail). Adds the
Field Guide reading variant, 44px controls, visible focus, a skip-link
style, and a global reduced-motion kill switch the pages rely on."
```

---
## Task 4: Landing page conversion rewrite

Replaces the Mythos-era landing with the nine-section sequence the spec fixes, on the Collector Archive system, with the full attribution contract and no volatile numbers.

**Files:**
- Rewrite: `packrip-cards/index.html` (currently 448 lines)

**Interfaces:**
- Consumes: every class from Task 3's contract; the seven era files and `og-cover.png` from Task 2; `Scripts/audit-packrip.py` from Task 1.
- Produces: the shared header and footer markup that Tasks 5–8 copy verbatim, adjusting only four things: `aria-current="page"`, the placement `ct` tag, the `app-argument`, and the fourth nav slot (Tasks 5 and 6 replace it with a contextual `packrip.co` link; Tasks 7 and 8 drop it, since the legal pages are not conversion pages and the footer already supplies the web link). The three `.legal` paragraphs in the footer are identical on all five pages.

- [ ] **Step 1: Run the audit on this page to see it fail**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --page packrip-cards/index.html; echo "exit=$?"
```

Expected: `exit=1`, with findings including `stale term 'PackRip: Cards'`, `forbidden claim 'five free daily packs'`, `forbidden claim '$4'`, `App Store link missing pt=127914124`, `img without explicit width/height`, `missing skip link to #main`, and `no packrip.co link on a conversion page`.

- [ ] **Step 2: Write the page**

Replace the entire contents of `packrip-cards/index.html` with:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#0b1220">
  <meta name="color-scheme" content="dark">
  <meta name="apple-itunes-app" content="app-id=6763404045, app-argument=https://elhanarinc.github.io/packrip-cards/">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <meta name="referrer" content="strict-origin-when-cross-origin">

  <title>PackRip: TCG Card Packs — Pokémon TCG booster pack opening for iPhone</title>
  <meta name="description" content="The official hub for PackRip: TCG Card Packs, the iPhone booster pack opening simulator. Every set unlocked, nine rarity tiers, foil variants, free packs daily, and odds shown before you spend. Free in the browser at packrip.co.">
  <link rel="canonical" href="https://elhanarinc.github.io/packrip-cards/">
  <link rel="alternate" hreflang="en" href="https://elhanarinc.github.io/packrip-cards/">
  <link rel="alternate" hreflang="x-default" href="https://elhanarinc.github.io/packrip-cards/">
  <link rel="icon" type="image/png" href="/packrip-cards/images/app-icon.png">
  <link rel="apple-touch-icon" href="/packrip-cards/images/app-icon.png">

  <meta property="og:type" content="website">
  <meta property="og:url" content="https://elhanarinc.github.io/packrip-cards/">
  <meta property="og:title" content="PackRip: TCG Card Packs — Pokémon TCG booster pack opening for iPhone">
  <meta property="og:description" content="Every era. One fresh binder. The iPhone booster pack opening simulator: every set unlocked, nine rarity tiers, foil variants, and odds shown before you spend.">
  <meta property="og:site_name" content="PackRip: TCG Card Packs">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="https://elhanarinc.github.io/packrip-cards/images/og-cover.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:alt" content="PackRip: TCG Card Packs — Booster Pack Opening Simulator">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="PackRip: TCG Card Packs — booster pack opening for iPhone">
  <meta name="twitter:description" content="Every era. One fresh binder. Nine rarity tiers, foil variants, and odds shown before you spend.">
  <meta name="twitter:image" content="https://elhanarinc.github.io/packrip-cards/images/og-cover.png">
  <meta name="twitter:image:alt" content="PackRip: TCG Card Packs — Booster Pack Opening Simulator">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "MobileApplication",
    "name": "PackRip: TCG Card Packs",
    "alternateName": "PackRip",
    "applicationCategory": "GameApplication",
    "applicationSubCategory": "Booster Pack Opening Simulator",
    "operatingSystem": "iOS 17.0 or later",
    "url": "https://elhanarinc.github.io/packrip-cards/",
    "installUrl": "https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?pt=127914124&ct=packrip_ios_github_hero&mt=8",
    "image": "https://elhanarinc.github.io/packrip-cards/images/og-cover.png",
    "screenshot": [
      "https://elhanarinc.github.io/packrip-cards/images/screens/01.jpg",
      "https://elhanarinc.github.io/packrip-cards/images/screens/02.jpg",
      "https://elhanarinc.github.io/packrip-cards/images/screens/03.jpg",
      "https://elhanarinc.github.io/packrip-cards/images/screens/04.jpg"
    ],
    "inLanguage": "en",
    "sameAs": ["https://packrip.co"],
    "author": { "@type": "Person", "name": "Arinc Elhan", "url": "https://elhanarinc.github.io/" },
    "publisher": { "@type": "Person", "name": "Arinc Elhan", "url": "https://elhanarinc.github.io/" },
    "featureList": [
      "Every set unlocked from the first launch",
      "Nine rarity tiers",
      "Independent foil roll on every card",
      "Free packs every day",
      "Pity guarantees with a visible counter",
      "The Forge: scrap duplicates into shards and craft missing cards",
      "Binder view, nine cards a page",
      "Wishlist hearts that feed Hunt Packs",
      "Set checklists with completion milestones",
      "16 collectible Seals with permanent perks",
      "Daily, weekly and Super quests",
      "Daily challenge leaderboard",
      "Anonymous cloud save with no signup"
    ]
  }
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=Bodoni+Moda:opsz,wght@6..96,500;6..96,600&display=swap">
  <link rel="stylesheet" href="/packrip-cards/_shared.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="site-head">
    <div class="wrap">
      <a class="brand" href="/packrip-cards/">
        <img src="/packrip-cards/images/app-icon.png" alt="" width="30" height="30">
        <span>PackRip: TCG Card Packs</span>
      </a>
      <nav class="nav-links" aria-label="PackRip pages">
        <a href="/packrip-cards/" aria-current="page">Overview</a>
        <a href="/packrip-cards/rarity.html">Pull rates</a>
        <a href="/packrip-cards/support.html">Support</a>
        <a href="https://www.packrip.co/?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=nav_play_web" target="_blank" rel="noopener">Play in browser</a>
      </nav>
    </div>
  </header>

  <main id="main">

    <!-- 1. Hero -->
    <section class="hero">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="kicker">Pokémon TCG pack opening · iPhone</p>
          <h1>Every era.<br>One fresh binder.</h1>
          <p class="lede">
            PackRip: TCG Card Packs is the iPhone half of PackRip. Rip booster packs era by
            era, keep what you pull in a binder that remembers, and see the odds before you
            spend a coin. The iPhone app ships PackRip&rsquo;s own original card art; the
            browser product at packrip.co runs the real Pokémon TCG checklists.
          </p>
          <div class="cta-row">
            <a class="cta cta--primary" href="https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?pt=127914124&amp;ct=packrip_ios_github_hero&amp;mt=8" target="_blank" rel="noopener">Get it on the App Store</a>
            <a class="cta cta--ghost" href="https://www.packrip.co/?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=hero_play_web" target="_blank" rel="noopener">Play free in your browser</a>
          </div>
        </div>
        <!-- Hero visual is the app icon on purpose. The frozen App Store screenshots
             use different framing and would read as incoherent here, and an era
             wrapper would attribute web-archive art to the iPhone app — the exact
             implication the lede above exists to rule out. -->
        <figure class="hero-shot">
          <img src="/packrip-cards/images/app-icon.png" alt="The PackRip: TCG Card Packs app icon" width="1024" height="1024">
          <figcaption>iPhone · iOS 17 and later · English</figcaption>
        </figure>
      </div>
    </section>

    <!-- 2. Truth strip -->
    <section class="wrap" aria-label="What PackRip: TCG Card Packs includes">
      <dl class="ledger">
        <div>
          <dt>Catalog</dt>
          <dd>Every set unlocked from the first launch. Nothing gated behind a level.</dd>
        </div>
        <div>
          <dt>Rarity</dt>
          <dd>Nine tiers, and an independent foil roll on every single card.</dd>
        </div>
        <div>
          <dt>Cost</dt>
          <dd>Free packs arrive every day. No signup, no account, no e-mail.</dd>
        </div>
        <div>
          <dt>Saves</dt>
          <dd>Anonymous cloud save. The iPhone binder is separate from the browser one.</dd>
        </div>
      </dl>
    </section>

    <!-- 3. Era archive: the signature -->
    <section class="block">
      <div class="wrap">
        <h2 class="block-head">The archive, by era</h2>
        <p class="block-sub">
          PackRip is organised the way collectors actually organise: by era, oldest drawer
          first. Base Set through the current expansions, each with its own rare slot,
          its own chase cards, and its own eligible rarities.
        </p>

        <div class="rail">
          <article class="era era--wotc">
            <div class="era-tab"><span class="era-name">Wizards of the Coast</span><span class="era-year">1999–2000</span></div>
            <div class="era-wrap"><img src="/packrip-cards/images/eras/era-1999-wotc.webp" alt="Base Set booster pack wrapper" width="696" height="1204" decoding="async"></div>
          </article>
          <article class="era era--neo">
            <div class="era-tab"><span class="era-name">Neo</span><span class="era-year">2000–2002</span></div>
            <div class="era-wrap"><img src="/packrip-cards/images/eras/era-2000-neo.webp" alt="Neo Genesis first-edition booster pack wrapper" width="906" height="1514" loading="lazy" decoding="async"></div>
          </article>
          <article class="era era--ecard">
            <div class="era-tab"><span class="era-name">e-Card</span><span class="era-year">2002–2003</span></div>
            <div class="era-wrap"><img src="/packrip-cards/images/eras/era-2002-ecard.webp" alt="Skyridge booster pack wrapper" width="451" height="800" loading="lazy" decoding="async"></div>
          </article>
          <article class="era era--ex">
            <div class="era-tab"><span class="era-name">EX</span><span class="era-year">2003–2007</span></div>
            <div class="era-wrap"><img src="/packrip-cards/images/eras/era-2003-ex.webp" alt="Ruby and Sapphire booster pack wrapper" width="451" height="800" loading="lazy" decoding="async"></div>
          </article>
          <article class="era era--dp">
            <div class="era-tab"><span class="era-name">Diamond &amp; Pearl</span><span class="era-year">2007–2011</span></div>
            <div class="era-wrap"><img src="/packrip-cards/images/eras/era-2007-dp.webp" alt="Diamond and Pearl booster pack wrapper" width="242" height="412" loading="lazy" decoding="async"></div>
          </article>
          <article class="era era--bw">
            <div class="era-tab"><span class="era-name">Black &amp; White</span><span class="era-year">2011–2016</span></div>
            <div class="era-wrap"><img src="/packrip-cards/images/eras/era-2011-bw.webp" alt="Black and White booster pack wrapper" width="563" height="1072" loading="lazy" decoding="async"></div>
          </article>
          <article class="era era--modern">
            <div class="era-tab"><span class="era-name">Modern</span><span class="era-year">2017–present</span></div>
            <div class="era-wrap"><img src="/packrip-cards/images/eras/era-2017-modern.webp" alt="Scarlet and Violet booster pack wrapper" width="780" height="1429" loading="lazy" decoding="async"></div>
          </article>
        </div>

        <p class="era-cap">
          Era artwork above comes from the PackRip web archive, the browser product that
          runs the real Pokémon TCG checklists. The iPhone app ships PackRip&rsquo;s own
          original card art.
          <a href="https://www.packrip.co/sets?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=era_archive" target="_blank" rel="noopener">Browse every set on packrip.co</a>.
        </p>
      </div>
    </section>

    <!-- 4. Native ritual -->
    <section class="block">
      <div class="wrap">
        <h2 class="block-head">The rip, natively</h2>
        <p class="block-sub">
          The whole point of a booster pack is the twenty seconds before you know. On iPhone
          that means a real swipe to tear the foil, one card at a time, haptics under your
          thumb, and shine that tracks the way you tilt the phone.
        </p>

        <div class="shots">
          <figure><img src="/packrip-cards/images/screens/01.jpg" alt="A sealed booster pack on the PackRip home screen" width="607" height="1320" loading="lazy" decoding="async"><figcaption>Sealed and waiting</figcaption></figure>
          <figure><img src="/packrip-cards/images/screens/02.jpg" alt="Swiping across a pack to tear the foil open" width="607" height="1320" loading="lazy" decoding="async"><figcaption>Swipe to tear</figcaption></figure>
          <figure><img src="/packrip-cards/images/screens/03.jpg" alt="A revealed card shown full screen with holographic shine" width="607" height="1320" loading="lazy" decoding="async"><figcaption>One card at a time</figcaption></figure>
          <figure><img src="/packrip-cards/images/screens/04.jpg" alt="The collection grid filling up with pulled cards" width="607" height="1320" loading="lazy" decoding="async"><figcaption>The binder fills</figcaption></figure>
          <figure><img src="/packrip-cards/images/screens/05.jpg" alt="The set list on the PackRip home screen" width="607" height="1320" loading="lazy" decoding="async"><figcaption>Pick any set</figcaption></figure>
          <figure><img src="/packrip-cards/images/screens/06.jpg" alt="The Seal progress screen showing permanent perks" width="607" height="1320" loading="lazy" decoding="async"><figcaption>Seals and perks</figcaption></figure>
          <figure><img src="/packrip-cards/images/screens/07.jpg" alt="The in-app pull rates screen listing every rarity and its odds" width="607" height="1320" loading="lazy" decoding="async"><figcaption>Odds, in the app</figcaption></figure>
        </div>

        <p class="era-cap">
          These are the screenshots from the live App Store listing, which ships
          PackRip&rsquo;s own original card art. Hold any card to see it full screen, flip
          the binder nine cards a page, and share a rip as a portrait image in one tap.
        </p>
      </div>
    </section>

    <!-- 5. Collector systems -->
    <section class="block">
      <div class="wrap">
        <h2 class="block-head">Systems for people who finish sets</h2>
        <p class="block-sub">
          Pulling is the easy part. Closing a binder is the game. Everything below is in the
          shipping app today.
        </p>

        <div class="cards">
          <article class="card">
            <span class="card-label">Craft</span>
            <h3>The Forge</h3>
            <p>Scrap duplicates into shards, then craft the exact card the binder has been missing.</p>
          </article>
          <article class="card">
            <span class="card-label">Target</span>
            <h3>Wishlist and Hunt Packs</h3>
            <p>Heart the cards you actually want. Hunt Packs surface them first, weighted by rarity.</p>
          </article>
          <article class="card">
            <span class="card-label">Protect</span>
            <h3>Pity guarantees</h3>
            <p>Dry streaks are tracked per rarity with a visible counter, so you can always see how close the next guaranteed pull is.</p>
          </article>
          <article class="card">
            <span class="card-label">Complete</span>
            <h3>Set checklists</h3>
            <p>Owned, Missing and Foils filters, completion bars, and coin rewards at real milestones.</p>
          </article>
          <article class="card">
            <span class="card-label">Earn</span>
            <h3>Seals and quests</h3>
            <p>Sixteen collectible Seals, each with a permanent gameplay perk, plus daily, weekly and Super quests.</p>
          </article>
          <article class="card">
            <span class="card-label">Compete</span>
            <h3>Trainer identity</h3>
            <p>A trainer card with your own title and name colour, and a daily challenge leaderboard when you want one.</p>
          </article>
        </div>
      </div>
    </section>

    <!-- 6. Web / iOS bridge -->
    <section class="block">
      <div class="wrap">
        <h2 class="block-head">Two products, one brand</h2>
        <p class="block-sub">
          PackRip runs in the browser and on iPhone. Pick by how you want to open packs, not
          by which one is better. The two keep separate binders.
        </p>

        <div class="bridge">
          <div class="bridge-col">
            <h3>packrip.co, in the browser</h3>
            <ul>
              <li>Nothing to install, nothing to sign up for.</li>
              <li>The real Pokémon TCG checklists, set by set.</li>
              <li>Card pages, pull-rate pages, and set guides you can link to.</li>
              <li>Free, and it stays free.</li>
            </ul>
            <div class="cta-row">
              <a class="cta cta--ghost" href="https://www.packrip.co/?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=bridge_web" target="_blank" rel="noopener">Open packrip.co</a>
            </div>
          </div>
          <div class="bridge-col">
            <h3>PackRip: TCG Card Packs, on iPhone</h3>
            <ul>
              <li>A real tear gesture, haptics, and pack-open sound.</li>
              <li>Motion-reactive shine, foil finishes, and a full-screen card hold.</li>
              <li>The Forge, Seals, quests, and anonymous cloud save.</li>
              <li>Free packs every day, with odds shown before any purchase.</li>
            </ul>
            <div class="cta-row">
              <a class="cta cta--primary" href="https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?pt=127914124&amp;ct=packrip_ios_github_bridge&amp;mt=8" target="_blank" rel="noopener">Get it on the App Store</a>
            </div>
          </div>
        </div>

        <p class="era-cap">
          Progress does not move between them. The browser binder stays in your browser and
          the iPhone binder stays on your iPhone, each with its own coins and its own
          collection.
        </p>
      </div>
    </section>

    <!-- 7. Transparent odds -->
    <section class="block">
      <div class="wrap">
        <h2 class="block-head">The odds are in the app, before you spend</h2>
        <p class="block-sub">
          Every rarity, every foil chance, and your live pity counters are one tap from any
          pack in the shop, per Apple&rsquo;s App Store Review Guideline 3.1.1. Those in-app
          numbers are the authoritative ones, because they are read from the same live config
          the pack generator uses.
        </p>
        <div class="cta-row">
          <a class="cta cta--ghost" href="/packrip-cards/rarity.html">Read the pull rates field guide</a>
        </div>
      </div>
    </section>

    <!-- 8. Final conversion -->
    <section class="block">
      <div class="wrap">
        <h2 class="block-head">Open the first drawer</h2>
        <p class="block-sub">
          Free packs are waiting, every set is already unlocked, and nothing asks you to make
          an account.
        </p>
        <div class="cta-row">
          <a class="cta cta--primary" href="https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?pt=127914124&amp;ct=packrip_ios_github_cta&amp;mt=8" target="_blank" rel="noopener">Get it on the App Store</a>
          <a class="cta cta--ghost" href="https://www.packrip.co/?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=cta_play_web" target="_blank" rel="noopener">Or open a pack in the browser</a>
        </div>
      </div>
    </section>

  </main>

  <footer class="site-foot">
    <div class="wrap">
      <nav class="foot-nav" aria-label="PackRip footer">
        <a href="/packrip-cards/">Overview</a>
        <a href="/packrip-cards/rarity.html">Pull rates</a>
        <a href="/packrip-cards/support.html">Support</a>
        <a href="/packrip-cards/privacy.html">Privacy</a>
        <a href="/packrip-cards/terms.html">Terms</a>
        <a href="https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?pt=127914124&amp;ct=packrip_ios_github_footer&amp;mt=8" target="_blank" rel="noopener">App Store</a>
        <a href="https://www.packrip.co/?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=footer_web" target="_blank" rel="noopener">packrip.co</a>
        <a href="/">All apps</a>
        <a href="mailto:elhanarinc@gmail.com">Contact</a>
      </nav>
      <p class="legal">
        PackRip is a fan-made booster pack opening simulator. Pokémon and all related
        names, characters and imagery are trademarks of Nintendo, Creatures Inc.,
        GAME FREAK inc. and The Pokémon Company. PackRip is not affiliated with,
        endorsed by, or sponsored by any of them. No physical cards are sold or shipped.
      </p>
      <p class="legal">
        The iPhone app ships card artwork that is original to PackRip. In-app purchases
        provide virtual coins used to open simulated packs; coins and cards have no cash
        value and cannot be traded or cashed out.
      </p>
      <p class="legal">© 2026 Arinc Elhan · Indie iPhone apps</p>
    </div>
  </footer>
</body>
</html>
```

If Task 1 recorded `primaryGenreName` as `Entertainment` rather than a games genre, change `"applicationCategory": "GameApplication"` to `"EntertainmentApplication"` and make the same change in every later page that carries an application schema.

Note the deliberate omissions, each required by the spec: no QR block, because the only existing QR asset lives in the web repo and was generated from a different URL, and the spec says omit rather than ship a conflicting destination; no `offers` or price block, because prices are not evidenced in this repository; no `FAQPage`, because the Support page owns the FAQ schema and a second copy would contradict it.

- [ ] **Step 3: Run the audit to verify it passes**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --page packrip-cards/index.html; echo "exit=$?"
```

Expected: `audit-packrip: clean` and `exit=0`.

- [ ] **Step 4: Verify the JSON-LD independently, the way CI does**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
import json, re, pathlib
raw = pathlib.Path("packrip-cards/index.html").read_text()
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.DOTALL)
print("blocks:", len(blocks))
for i, b in enumerate(blocks, 1):
    data = json.loads(b.strip())
    print(f"  #{i} @type={data['@type']} name={data.get('name')!r} features={len(data.get('featureList', []))}")
PY
```

Expected:

```
blocks: 1
  #1 @type=MobileApplication name='PackRip: TCG Card Packs' features=13
```

- [ ] **Step 5: Serve locally and confirm the page and every asset it needs return 200**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 -m http.server 8765 >/dev/null 2>&1 &
SRV=$!
sleep 1
for p in /packrip-cards/ /packrip-cards/_shared.css \
         /packrip-cards/images/app-icon.png /packrip-cards/images/og-cover.png \
         /packrip-cards/images/eras/era-1999-wotc.webp \
         /packrip-cards/images/eras/era-2017-modern.webp \
         /packrip-cards/images/screens/01.jpg /packrip-cards/rarity.html; do
  printf '%-58s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:8765$p")"
done
kill $SRV
```

Expected: `200` on every line. Never inspect these pages over `file://` — the absolute `/packrip-cards/...` paths only resolve over HTTP.

- [ ] **Step 6: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add packrip-cards/index.html
git commit -m "feat(packrip): Rebuild the landing page as the iOS product hub

Nine-section sequence on the Collector Archive system: hero, truth ledger,
era archive rail, native rip, collector systems, web/iOS bridge, odds,
conversion, footer. Drops the fabricated pack counts, prices, pity
thresholds and the duplicate FAQ schema; every App Store link now carries
pt/ct/mt and every packrip.co link carries the four UTM parameters."
```

---
## Task 5: Pull Rates field guide

Converts the static Mythos odds ladder into a Field Guide that explains the rarity system and routes every number to the authoritative in-app sheet.

**Files:**
- Rewrite: `packrip-cards/rarity.html` (currently 157 lines)

**Interfaces:**
- Consumes: the header and footer markup produced by Task 4; `.prose`, `.odds`, `.odds-row`, `.tier-mark*`, `.note`, `.anchor` from Task 3.
- Produces: the Field Guide page pattern (`<body class="field-guide">`, `.prose` wrapper, anchored `h2`s) that Tasks 6–8 reuse.

**Design decision, and the reason for it:** this page publishes no numeric odds at all, and it does not present the nine-tier list as a rarity ranking either — Task 5's review, and a live-config check that followed from it, established that the App Store's tier ordering is not a rarity order (Gold Star's rare-slot rate is 0.028 against Shining's 0.02) and that the Hunt Pack boost is not monotonic down the ladder (Gold Star 0.08 against the rarest tier's 0.10). The page therefore uses the listing's ordering, says so, and routes every ranking question to the app. The site it replaces published seven pull-rate percentages, per-rarity foil chances, eight hunt-injection rates and five pity thresholds. Checked against `packrip-ios/Worker/config/gameplay.json`, the pull rates, foil rates and hunt rates were correct, but two of the five pity thresholds did not exist in the config and had been wrong on a live page for months. Every one of those values is tunable from Cloudflare KV without an app release, so the page cannot stay correct by construction. The field guide therefore explains the ladder, the finishes, the eligibility rule and the protection mechanics, states plainly that the in-app sheet is the authoritative source, and sends readers there. This satisfies spec §4.3 and removes the entire class of failure that produced the fabricated thresholds.

- [ ] **Step 1: Run the audit on this page to see it fail**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --page packrip-cards/rarity.html; echo "exit=$?"
```

Expected: `exit=1`, including `stale term 'PackRip: Cards'`, `forbidden claim '200 packs'`, `forbidden claim '80 packs'`, `App Store link missing pt=127914124`, `no packrip.co link on a conversion page`, and `missing skip link to #main`.

- [ ] **Step 2: Write the page**

Replace the entire contents of `packrip-cards/rarity.html` with:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#0b1220">
  <meta name="color-scheme" content="dark">
  <meta name="apple-itunes-app" content="app-id=6763404045, app-argument=https://elhanarinc.github.io/packrip-cards/rarity.html">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <meta name="referrer" content="strict-origin-when-cross-origin">

  <title>Pull rates and rarity tiers — PackRip: TCG Card Packs</title>
  <meta name="description" content="A collector's field guide to the nine rarity tiers in PackRip: TCG Card Packs, how the independent foil roll works, why eligible rarities depend on the set, and where to read the live odds before you open a pack.">
  <link rel="canonical" href="https://elhanarinc.github.io/packrip-cards/rarity.html">
  <link rel="alternate" hreflang="en" href="https://elhanarinc.github.io/packrip-cards/rarity.html">
  <link rel="icon" type="image/png" href="/packrip-cards/images/app-icon.png">
  <link rel="apple-touch-icon" href="/packrip-cards/images/app-icon.png">

  <meta property="og:type" content="article">
  <meta property="og:url" content="https://elhanarinc.github.io/packrip-cards/rarity.html">
  <meta property="og:title" content="Pull rates and rarity tiers — PackRip: TCG Card Packs">
  <meta property="og:description" content="The nine rarity tiers, the independent foil roll, set-dependent eligibility, and pity protection — with the live odds where they belong: in the app.">
  <meta property="og:site_name" content="PackRip: TCG Card Packs">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="https://elhanarinc.github.io/packrip-cards/images/og-cover.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:alt" content="PackRip: TCG Card Packs — Booster Pack Opening Simulator">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Pull rates and rarity tiers — PackRip: TCG Card Packs">
  <meta name="twitter:description" content="Nine tiers, an independent foil roll, set-dependent eligibility, and pity protection.">
  <meta name="twitter:image" content="https://elhanarinc.github.io/packrip-cards/images/og-cover.png">
  <meta name="twitter:image:alt" content="PackRip: TCG Card Packs — Booster Pack Opening Simulator">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Pull rates and rarity tiers in PackRip: TCG Card Packs",
    "description": "A field guide to the nine rarity tiers, the independent foil roll, set-dependent rarity eligibility, and pity protection in the PackRip iPhone app.",
    "mainEntityOfPage": { "@type": "WebPage", "@id": "https://elhanarinc.github.io/packrip-cards/rarity.html" },
    "url": "https://elhanarinc.github.io/packrip-cards/rarity.html",
    "image": "https://elhanarinc.github.io/packrip-cards/images/og-cover.png",
    "datePublished": "2026-05-16",
    "dateModified": "2026-08-20",
    "inLanguage": "en",
    "author": { "@type": "Person", "name": "Arinc Elhan", "url": "https://elhanarinc.github.io/" },
    "publisher": { "@type": "Person", "name": "Arinc Elhan", "url": "https://elhanarinc.github.io/" },
    "about": { "@type": "MobileApplication", "name": "PackRip: TCG Card Packs", "url": "https://elhanarinc.github.io/packrip-cards/" }
  }
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=Bodoni+Moda:opsz,wght@6..96,500;6..96,600&display=swap">
  <link rel="stylesheet" href="/packrip-cards/_shared.css">
</head>
<body class="field-guide">
  <a class="skip" href="#main">Skip to content</a>

  <header class="site-head">
    <div class="wrap">
      <a class="brand" href="/packrip-cards/">
        <img src="/packrip-cards/images/app-icon.png" alt="" width="30" height="30">
        <span>PackRip: TCG Card Packs</span>
      </a>
      <nav class="nav-links" aria-label="PackRip pages">
        <a href="/packrip-cards/">Overview</a>
        <a href="/packrip-cards/rarity.html" aria-current="page">Pull rates</a>
        <a href="/packrip-cards/support.html">Support</a>
        <a href="https://www.packrip.co/pull-rate/base1/holo-rare?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=rates_explore" target="_blank" rel="noopener">Web pull rates</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <div class="wrap">
      <article class="prose">
        <h1>Pull rates and rarity tiers</h1>
        <p class="lede">
          A field guide to how a pack is built in PackRip: TCG Card Packs — the nine tiers,
          the finish that rolls on top of them, why one set can pull a rarity another cannot,
          and what protects you from a dry streak.
        </p>

        <div class="note">
          <p><strong>Read the live odds in the app, before you open anything.</strong>
          Tap any pack in the shop and then <em>View Pull Rates &amp; Odds</em>. That screen
          shows the current rate for every rarity, the current foil chance, and your own live
          pity counters, one tap from any purchase, as Apple&rsquo;s App Store Review
          Guideline 3.1.1 requires.</p>
          <p>This page deliberately does not reprint those numbers: rates are tuned on the
          server and can change without an app update, so a static copy here would
          eventually disagree with the app.</p>
        </div>

        <h2 id="tiers">The nine tiers<a class="anchor" href="#tiers" aria-label="Link to this section">#</a></h2>
        <p>
          Every card in PackRip belongs to exactly one of nine tiers, listed here in the
          order the App Store listing names them. Broadly they run from the everyday fillers
          down to the chase pulls, but the exact standing of the rarest few is a live number
          rather than a fixed rank — read it in the app.
        </p>
        <dl class="odds">
          <div class="odds-row"><dt><span class="tier-mark tier-mark--common" aria-hidden="true"></span>Common</dt><dd>Fills the bulk of a pack</dd></div>
          <div class="odds-row"><dt><span class="tier-mark tier-mark--common" aria-hidden="true"></span>Uncommon</dt><dd>Fills the middle slots</dd></div>
          <div class="odds-row"><dt><span class="tier-mark tier-mark--rare" aria-hidden="true"></span>Rare</dt><dd>The floor of the rare slot</dd></div>
          <div class="odds-row"><dt><span class="tier-mark tier-mark--holo" aria-hidden="true"></span>Holo Rare</dt><dd>The first holographic treatment</dd></div>
          <div class="odds-row"><dt><span class="tier-mark tier-mark--holoex" aria-hidden="true"></span>Holo EX</dt><dd>The featured chase of a set</dd></div>
          <div class="odds-row"><dt><span class="tier-mark tier-mark--secret" aria-hidden="true"></span>Rare Secret</dt><dd>Set-specific secret variants</dd></div>
          <div class="odds-row"><dt><span class="tier-mark tier-mark--shining" aria-hidden="true"></span>Shining</dt><dd>High-contrast metallic finish</dd></div>
          <div class="odds-row"><dt><span class="tier-mark tier-mark--goldstar" aria-hidden="true"></span>Gold Star</dt><dd>Top of the standard ladder</dd></div>
          <div class="odds-row"><dt><span class="tier-mark tier-mark--crystal" aria-hidden="true"></span>Crystal</dt><dd>The rarest base pull</dd></div>
        </dl>
        <p>
          The colour swatch beside each tier is decoration: the tier name is what carries the
          meaning, so the ladder reads correctly with colours unavailable.
        </p>

        <h2 id="foil">Foil is a finish, not a tier<a class="anchor" href="#foil" aria-label="Link to this section">#</a></h2>
        <p>
          After a card&rsquo;s rarity is decided, it gets an independent roll for a foil
          finish. A foil never replaces the pull you were going to get; it is a separate
          chance layered on top of it.
        </p>
        <ul>
          <li>Foils occupy their own slot in your collection, so a normal copy and a foil copy are both worth owning.</li>
          <li>They carry a brighter shimmer and an animated border.</li>
          <li>They sell for more than the base card.</li>
          <li>The foil chance rises with rarity, and the current per-rarity chance is shown in the in-app Pull Rates screen.</li>
        </ul>
        <dl class="odds">
          <div class="odds-row"><dt><span class="tier-mark tier-mark--foil" aria-hidden="true"></span>Foil finish</dt><dd>Rolled per card, independently of rarity</dd></div>
        </dl>

        <h2 id="eligibility">Eligible rarities depend on the set<a class="anchor" href="#eligibility" aria-label="Link to this section">#</a></h2>
        <p>
          Not every set can pull every tier. A set&rsquo;s eligible rarities come from what
          that set actually printed, so a tier that simply does not exist in a set will never
          appear in its packs no matter how many you open. When you open the pull-rate screen
          from inside a specific pack, the rates you see are the rates for that set.
        </p>

        <h2 id="pity">Pity guarantees<a class="anchor" href="#pity" aria-label="Link to this section">#</a></h2>
        <p>
          PackRip counts how many packs you have opened without pulling each protected rarity.
          Cross the threshold for one of them and the next pack is forced to roll it. Pity is
          purely protective: it never lowers your odds and never costs anything.
        </p>
        <p>
          Not every tier is protected, and the thresholds are server-tuned. Your live counter
          for each protected rarity is shown in the in-app Pull Rates screen under
          <em>Pity — Guaranteed Pulls</em>, which is the only place those numbers are
          guaranteed to be current.
        </p>

        <h2 id="hunt">Hunt Packs<a class="anchor" href="#hunt" aria-label="Link to this section">#</a></h2>
        <p>
          A Hunt Pack targets one specific card you are missing. Heart a card to add it to
          your wishlist, then spend coins on a Hunt Pack and that card gets a boosted chance
          of appearing.
        </p>
        <p>
          The boost is large for the common tiers and much smaller for the chase tiers, and
          it does not slide evenly down the ladder — a couple of the rarest tiers sit close
          together. A chase-tier hunt is a much longer shot than a Common hunt. Check the
          exact chance for the card you are targeting in the app before you spend coins on
          a hunt.
        </p>

        <h2 id="authoritative">Why the app is the authority<a class="anchor" href="#authoritative" aria-label="Link to this section">#</a></h2>
        <p>
          The in-app Pull Rates screen renders from the same live configuration the pack
          generator reads, so there is no second copy of the numbers to drift out of sync.
          If anything here ever appears to contradict the app, the app is right.
        </p>

        <h2 id="limits">What rarity does not do<a class="anchor" href="#limits" aria-label="Link to this section">#</a></h2>
        <ul>
          <li>It does not gate gameplay. There are no battles, so a Crystal never beats a Common.</li>
          <li>It does not gate set completion. Duplicates can be scrapped into shards in the Forge and crafted into the card you are missing.</li>
          <li>It is not tradeable. Cards and coins have no cash value and cannot be transferred, sold or cashed out.</li>
        </ul>
        <p>
          Rarity here is what it was when packs came in cardboard: a reason to open one more.
        </p>

        <div class="cta-row">
          <a class="cta cta--primary" href="https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?pt=127914124&amp;ct=packrip_ios_github_rates&amp;mt=8" target="_blank" rel="noopener">Get it on the App Store</a>
          <a class="cta cta--ghost" href="https://www.packrip.co/pull-rate/base1/holo-rare?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=rates_explore" target="_blank" rel="noopener">Per-set pull rates on packrip.co</a>
        </div>
      </article>
    </div>
  </main>

  <footer class="site-foot">
    <div class="wrap">
      <nav class="foot-nav" aria-label="PackRip footer">
        <a href="/packrip-cards/">Overview</a>
        <a href="/packrip-cards/rarity.html">Pull rates</a>
        <a href="/packrip-cards/support.html">Support</a>
        <a href="/packrip-cards/privacy.html">Privacy</a>
        <a href="/packrip-cards/terms.html">Terms</a>
        <a href="https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?pt=127914124&amp;ct=packrip_ios_github_footer&amp;mt=8" target="_blank" rel="noopener">App Store</a>
        <a href="https://www.packrip.co/?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=footer_web" target="_blank" rel="noopener">packrip.co</a>
        <a href="/">All apps</a>
        <a href="mailto:elhanarinc@gmail.com">Contact</a>
      </nav>
      <p class="legal">
        PackRip is a fan-made booster pack opening simulator. Pokémon and all related
        names, characters and imagery are trademarks of Nintendo, Creatures Inc.,
        GAME FREAK inc. and The Pokémon Company. PackRip is not affiliated with,
        endorsed by, or sponsored by any of them. No physical cards are sold or shipped.
      </p>
      <p class="legal">
        The iPhone app ships card artwork that is original to PackRip. In-app purchases
        provide virtual coins used to open simulated packs; coins and cards have no cash
        value and cannot be traded or cashed out.
      </p>
      <p class="legal">© 2026 Arinc Elhan · Indie iPhone apps</p>
    </div>
  </footer>
</body>
</html>
```

If Task 1's Step 3 reported anything other than `200` for `/pull-rate/base1/holo-rare`, replace both occurrences of that URL with `https://www.packrip.co/sets` and keep `utm_content=rates_explore` unchanged.

- [ ] **Step 3: Run the audit to verify it passes**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --page packrip-cards/rarity.html; echo "exit=$?"
```

Expected: `audit-packrip: clean` and `exit=0`.

- [ ] **Step 4: Verify the anchors resolve and the ladder is readable as prose**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
import pathlib, re, sys
raw = pathlib.Path("packrip-cards/rarity.html").read_text()
ids = set(re.findall(r'<h2 id="([^"]+)"', raw))
hrefs = set(re.findall(r'class="anchor" href="#([^"]+)"', raw))
print("section ids :", sorted(ids))
print("anchor refs :", sorted(hrefs))
missing = hrefs - ids
tiers = re.findall(r'</span>([A-Za-z ]+)</dt>', raw)
print("tiers in order:", tiers)
want = ["Common", "Uncommon", "Rare", "Holo Rare", "Holo EX",
        "Rare Secret", "Shining", "Gold Star", "Crystal", "Foil finish"]
bad = missing or tiers != want
if missing:
    print("FAIL dangling anchors:", missing)
if tiers != want:
    print("FAIL tier order is", tiers, "expected", want)
sys.exit(1 if bad else 0)
PY
```

Expected: seven section ids, seven matching anchor refs, the ten labels in exactly the listed order, and exit 0.

- [ ] **Step 5: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add packrip-cards/rarity.html
git commit -m "feat(packrip): Rewrite pull rates as a Field Guide

Explains the nine tiers, the independent foil roll, set-dependent
eligibility, pity protection and Hunt Packs, and routes every number to
the in-app sheet. Removes the two pity thresholds that never existed in
Worker/config/gameplay.json and every other server-tuned figure, which is
the failure mode this page existed to prevent."
```

---

## Task 6: Support rewrite and FAQ schema

Replaces launch-era answers with the problems current users actually have, and makes the `FAQPage` schema mirror the visible text exactly.

**Files:**
- Rewrite: `packrip-cards/support.html` (currently 131 lines)

**Interfaces:**
- Consumes: the Field Guide page pattern from Task 5.
- Produces: nine visible question-and-answer pairs, each duplicated verbatim into `FAQPage`, verified mechanically in Step 4.

- [ ] **Step 1: Run the audit on this page to see it fail**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --page packrip-cards/support.html; echo "exit=$?"
```

Expected: `exit=1`, including `stale term 'PackRip: Cards'`, `forbidden claim 'no analytics'`, `forbidden claim '8 total'`, `App Store link missing pt=127914124`, and `no packrip.co link on a conversion page`.

- [ ] **Step 2: Write the page**

Replace the entire contents of `packrip-cards/support.html` with the same head/header/footer pattern as Task 5, changing only the values below, plus this body. Head values for this page:

- `<meta name="apple-itunes-app" content="app-id=6763404045, app-argument=https://elhanarinc.github.io/packrip-cards/support.html">`
- `<title>Support and FAQ — PackRip: TCG Card Packs</title>`
- `<meta name="description" content="Support for PackRip: TCG Card Packs. Restore purchases, recover a collection, manage or cancel PackRip Plus, request a refund through Apple, understand separate web and iPhone saves, and reach the developer.">`
- `<link rel="canonical" href="https://elhanarinc.github.io/packrip-cards/support.html">` and the matching `hreflang="en"` alternate
- `<meta property="og:type" content="article">`, `og:url` and both `twitter`/`og` titles set to `Support and FAQ — PackRip: TCG Card Packs`
- `og:description` and `twitter:description`: `Restore purchases, recover a collection, manage PackRip Plus, request a refund through Apple, and understand separate web and iPhone saves.`
- Header nav: `aria-current="page"` on the Support link; the fourth nav item is `<a href="https://www.packrip.co/faq?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=support_web" target="_blank" rel="noopener">Web FAQ</a>`

Replace the landing's `MobileApplication` schema block with this one:

```html
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "inLanguage": "en",
    "mainEntity": [
      { "@type": "Question", "name": "Which iPhones does PackRip: TCG Card Packs run on?",
        "acceptedAnswer": { "@type": "Answer", "text": "PackRip: TCG Card Packs is an iPhone app and needs iOS 17.0 or later. There is no iPad, Mac, Apple Watch or Vision Pro build, and the app is English only." } },
      { "@type": "Question", "name": "Does my packrip.co progress carry into the iPhone app?",
        "acceptedAnswer": { "@type": "Answer", "text": "No. The browser product at packrip.co and the iPhone app keep separate binders, separate coins and separate progress. Installing the app starts a new collection, and nothing you do on iPhone changes your browser save." } },
      { "@type": "Question", "name": "Do I need an account?",
        "acceptedAnswer": { "@type": "Answer", "text": "No. There is no signup, no login, no password and no e-mail. On first launch the app generates a random identifier, keeps it in the iOS Keychain, and uses it for cloud save and purchases. You can see and copy it in Settings, then About, then Device ID." } },
      { "@type": "Question", "name": "How do I restore purchases on a new iPhone?",
        "acceptedAnswer": { "@type": "Answer", "text": "Open the app, go to Settings and tap Restore Purchases. That re-attaches an active PackRip Plus subscription and any coin packs the server has not yet granted. If a purchase is still being validated you will see a pending message; the app retries on its own." } },
      { "@type": "Question", "name": "My collection is missing after a reinstall. How do I get it back?",
        "acceptedAnswer": { "@type": "Answer", "text": "Cloud save is keyed to the anonymous identifier in your iOS Keychain, which survives a reinstall on the same device, so reopening the app normally restores everything. On a brand-new device the app generates a fresh identifier instead. E-mail elhanarinc@gmail.com with the old Device ID from the original phone and the save can be re-attached." } },
      { "@type": "Question", "name": "How do I manage or cancel PackRip Plus?",
        "acceptedAnswer": { "@type": "Answer", "text": "PackRip Plus is an auto-renewing subscription billed by Apple. Manage or cancel it in iOS Settings, under your name, then Subscriptions, then PackRip Plus. Cancelling stops the renewal and you keep Plus benefits until the end of the period you already paid for. The current benefit list is shown in the app on the PackRip Plus screen." } },
      { "@type": "Question", "name": "Can I get a refund?",
        "acceptedAnswer": { "@type": "Answer", "text": "Every purchase is processed by Apple, so refunds are requested from Apple at reportaproblem.apple.com. Apple decides the outcome. Access is not restricted because a refund was granted." } },
      { "@type": "Question", "name": "Where do I see the pull rates?",
        "acceptedAnswer": { "@type": "Answer", "text": "Tap any pack in the in-app shop and then View Pull Rates and Odds. That screen shows the current rate for every rarity, the current foil chance and your own live pity counters, one tap from any purchase. Those in-app numbers are the authoritative ones." } },
      { "@type": "Question", "name": "A pack will not load, or content looks out of date. What now?",
        "acceptedAnswer": { "@type": "Answer", "text": "Card sets and game content are delivered from the server, so a failure is usually a connection problem. Close the app fully, reconnect, and reopen it. If it persists, e-mail elhanarinc@gmail.com with your iPhone model, iOS version and Device ID from Settings, then About." } }
    ]
  }
  </script>
```

Body, inside `<main id="main"><div class="wrap"><article class="prose">`:

```html
        <h1>Support</h1>
        <p class="lede">
          Answers to what people actually write in about. If yours is not here, e-mail
          <a href="mailto:elhanarinc@gmail.com">elhanarinc@gmail.com</a> and you will get a
          reply within a few days.
        </p>

        <div class="cta-row">
          <a class="cta cta--primary" href="https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?pt=127914124&amp;ct=packrip_ios_github_support&amp;mt=8" target="_blank" rel="noopener">Open in the App Store</a>
          <a class="cta cta--ghost" href="mailto:elhanarinc@gmail.com">E-mail support</a>
        </div>

        <h2 id="devices">Which iPhones does PackRip: TCG Card Packs run on?<a class="anchor" href="#devices" aria-label="Link to this section">#</a></h2>
        <p>PackRip: TCG Card Packs is an iPhone app and needs iOS 17.0 or later. There is no iPad, Mac, Apple Watch or Vision Pro build, and the app is English only.</p>

        <h2 id="saves">Does my packrip.co progress carry into the iPhone app?<a class="anchor" href="#saves" aria-label="Link to this section">#</a></h2>
        <p>No. The browser product at <a href="https://www.packrip.co/faq?utm_source=elhanarinc_github&amp;utm_medium=referral&amp;utm_campaign=packrip_ios_hub&amp;utm_content=support_web" target="_blank" rel="noopener">packrip.co</a> and the iPhone app keep separate binders, separate coins and separate progress. Installing the app starts a new collection, and nothing you do on iPhone changes your browser save.</p>

        <h2 id="account">Do I need an account?<a class="anchor" href="#account" aria-label="Link to this section">#</a></h2>
        <p>No. There is no signup, no login, no password and no e-mail. On first launch the app generates a random identifier, keeps it in the iOS Keychain, and uses it for cloud save and purchases. You can see and copy it in <strong>Settings, then About, then Device ID</strong>.</p>

        <h2 id="restore">How do I restore purchases on a new iPhone?<a class="anchor" href="#restore" aria-label="Link to this section">#</a></h2>
        <p>Open the app, go to <strong>Settings</strong> and tap <strong>Restore Purchases</strong>. That re-attaches an active PackRip Plus subscription and any coin packs the server has not yet granted. If a purchase is still being validated you will see a pending message; the app retries on its own.</p>

        <h2 id="recovery">My collection is missing after a reinstall. How do I get it back?<a class="anchor" href="#recovery" aria-label="Link to this section">#</a></h2>
        <p>Cloud save is keyed to the anonymous identifier in your iOS Keychain, which survives a reinstall on the same device, so reopening the app normally restores everything. On a brand-new device the app generates a fresh identifier instead. E-mail <a href="mailto:elhanarinc@gmail.com">elhanarinc@gmail.com</a> with the old Device ID from the original phone and the save can be re-attached.</p>

        <h2 id="plus">How do I manage or cancel PackRip Plus?<a class="anchor" href="#plus" aria-label="Link to this section">#</a></h2>
        <p>PackRip Plus is an auto-renewing subscription billed by Apple. Manage or cancel it in <strong>iOS Settings, under your name, then Subscriptions, then PackRip Plus</strong>. Cancelling stops the renewal and you keep Plus benefits until the end of the period you already paid for. The current benefit list is shown in the app on the PackRip Plus screen.</p>

        <h2 id="refunds">Can I get a refund?<a class="anchor" href="#refunds" aria-label="Link to this section">#</a></h2>
        <p>Every purchase is processed by Apple, so refunds are requested from Apple at <a href="https://reportaproblem.apple.com" target="_blank" rel="noopener">reportaproblem.apple.com</a>. Apple decides the outcome. Access is not restricted because a refund was granted.</p>

        <h2 id="odds">Where do I see the pull rates?<a class="anchor" href="#odds" aria-label="Link to this section">#</a></h2>
        <p>Tap any pack in the in-app shop and then <em>View Pull Rates and Odds</em>. That screen shows the current rate for every rarity, the current foil chance and your own live pity counters, one tap from any purchase. Those in-app numbers are the authoritative ones. The <a href="/packrip-cards/rarity.html">pull rates field guide</a> explains what the tiers mean.</p>

        <h2 id="loading">A pack will not load, or content looks out of date. What now?<a class="anchor" href="#loading" aria-label="Link to this section">#</a></h2>
        <p>Card sets and game content are delivered from the server, so a failure is usually a connection problem. Close the app fully, reconnect, and reopen it. If it persists, e-mail <a href="mailto:elhanarinc@gmail.com">elhanarinc@gmail.com</a> with your iPhone model, iOS version and Device ID from <strong>Settings, then About</strong>.</p>

        <h2 id="notifications">Turning reminders off<a class="anchor" href="#notifications" aria-label="Link to this section">#</a></h2>
        <p>Daily reminders are local notifications scheduled on your own device. Turn them off in <strong>iOS Settings, then PackRip, then Notifications</strong>, or from the app&rsquo;s own settings screen.</p>

        <h2 id="privacy">Privacy and data<a class="anchor" href="#privacy" aria-label="Link to this section">#</a></h2>
        <p>What the app collects, where it is stored, and how to have it deleted is in the <a href="/packrip-cards/privacy.html">privacy policy</a>. The short version: an anonymous device identifier, your game-state snapshot, and purchase records.</p>

        <div class="note">
          <p><strong>Reporting a bug well.</strong> Include your iPhone model, your iOS
          version, what you expected, what happened, and the Device ID from Settings, then
          About. A screenshot of the moment it went wrong is worth more than a paragraph.</p>
        </div>
```

Note that the last two sections (`#notifications` and `#privacy`) and the closing bug-reporting note are deliberately **not** in the `FAQPage` schema: spec §4.4 says only questions with visible answers are duplicated into the schema, and these are guidance rather than question-and-answer pairs. The nine schema entries map one-to-one onto the first nine `h2` sections.

- [ ] **Step 3: Run the audit to verify it passes**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --page packrip-cards/support.html; echo "exit=$?"
```

Expected: `audit-packrip: clean` and `exit=0`.

- [ ] **Step 4: Verify the FAQ schema mirrors the visible questions exactly**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
import html, json, pathlib, re, sys
raw = pathlib.Path("packrip-cards/support.html").read_text()
block = re.search(r'<script type="application/ld\+json">(.*?)</script>', raw, re.DOTALL).group(1)
faq = json.loads(block.strip())
schema_qs = [q["name"] for q in faq["mainEntity"]]

# Visible h2 text with the trailing permalink anchor stripped.
visible = []
for m in re.finditer(r'<h2 id="[^"]+">(.*?)<a class="anchor"', raw, re.DOTALL):
    visible.append(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip())

print(f"schema questions : {len(schema_qs)}")
print(f"visible headings : {len(visible)}")
bad = False
for i, q in enumerate(schema_qs):
    if i >= len(visible) or visible[i] != q:
        print(f"FAIL schema[{i}] {q!r} != visible {visible[i] if i < len(visible) else None!r}")
        bad = True
if len(visible) != len(schema_qs) + 2:
    print(f"FAIL expected {len(schema_qs)} FAQ headings plus 2 guidance headings, got {len(visible)}")
    bad = True
for q in faq["mainEntity"]:
    if not q["acceptedAnswer"]["text"].strip():
        print("FAIL empty answer for", q["name"])
        bad = True
if not bad:
    print("FAQ schema matches the visible questions")
sys.exit(1 if bad else 0)
PY
```

Expected: `schema questions : 9`, `visible headings : 11`, then `FAQ schema matches the visible questions`, exit 0. Eleven, not twelve: nine FAQ headings plus `#notifications` and `#privacy`. The closing bug-reporting note is a `.note` block, not a heading.

- [ ] **Step 5: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add packrip-cards/support.html
git commit -m "feat(packrip): Rewrite support around current user problems

Separate web and iPhone saves, anonymous cloud-save recovery, Plus
management, Apple refunds, content-loading failures and notification
control. Drops the retired no-analytics and no-ads answers and the
fabricated pack and pity numbers; FAQPage now mirrors the nine visible
questions one to one."
```

---
## Task 7: Privacy reconciliation

The most consequential correction in this plan. `/packrip-cards/privacy.html` is the privacy URL Apple has on file for the app, and it currently makes three statements that the live product contradicts.

**Files:**
- Rewrite: `packrip-cards/privacy.html` (currently 119 lines)

**Interfaces:**
- Consumes: the Field Guide page pattern from Task 5.
- Produces: nothing later tasks depend on.

**The three false statements being removed, and the evidence:**

- *"No advertising identifiers and no ad networks. The app shows no ads."* — false. `curl -s -H 'X-App-Version: 1.2.5' https://packrip-api.elhanarinc.workers.dev/v1/config/theme` returns a populated `adConfig`: provider `buysellads`, loader `https://cdn4.buysellads.net/pub/packrip.js`, five zones (`home`, `pokedex`, `stats`, `summary`, `interstitial`), `interstitialAfterPacks: 5`, disclosure label `Sponsor`. The same response carries a populated `affiliateConfig` for TCGplayer and eBay with the disclosure "Affiliate link — PackRip earns a small commission if you buy."
- *"No analytics SDKs"* — misleading. Third-party analytics were removed in the current release, but the shipped `packrip-ios/Resources/PrivacyInfo.xcprivacy` declares `NSPrivacyCollectedDataTypeProductInteraction` with purpose `Analytics`, and the app reports anonymous aggregate counts to its own backend.
- *"declaring three categories of collected data"* — false. The shipped manifest declares five: `DeviceID`, `PurchaseHistory`, `ProductInteraction`, `CrashData`, `PerformanceData`, with `NSPrivacyTracking = false` and an empty `NSPrivacyTrackingDomains`.

- [ ] **Step 1: Re-verify the live ad and affiliate state immediately before writing**

```bash
curl -s -m 20 -H 'X-App-Version: 1.2.5' \
  https://packrip-api.elhanarinc.workers.dev/v1/config/theme \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
ad, aff = d.get('adConfig') or {}, d.get('affiliateConfig') or {}
print('adConfig provider  :', ad.get('provider'))
print('adConfig loader    :', ad.get('loaderUrl'))
print('adConfig zones     :', sorted((ad.get('zones') or {}).keys()))
print('adConfig disclosure:', ad.get('disclosure'))
print('affiliate keys     :', sorted(aff.keys()))
print('affiliate disclose :', aff.get('disclosure'))
"
plutil -p ../packrip-ios/Resources/PrivacyInfo.xcprivacy \
  | grep NSPrivacyCollectedDataType\" 
```

Expected: `adConfig provider  : buysellads`, five zones, `disclosure: Sponsor`, affiliate keys including `ebay` and `tcgplayer`, and five `NSPrivacyCollectedDataType` lines.

If `adConfig provider` prints `None`, the ad layer has since been switched off. In that case delete the entire `#sponsors` section written in Step 3 and instead add one sentence to `#diagnostics`: "PackRip does not currently serve advertising. If that changes, this policy is updated before the change ships." Do not resurrect the retired absolute claim either way.

- [ ] **Step 2: Run the audit on this page to see it fail**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --page packrip-cards/privacy.html; echo "exit=$?"
```

Expected: `exit=1`, including `stale term 'PackRip: Cards'`, `forbidden claim 'no analytics'`, `forbidden claim 'no ads'`, `missing skip link to #main`, and `missing og:image`.

- [ ] **Step 3: Write the page**

Use the Task 5 head/header/footer pattern with these head values:

- `app-argument=https://elhanarinc.github.io/packrip-cards/privacy.html`
- `<title>Privacy policy — PackRip: TCG Card Packs</title>`
- `<meta name="description" content="The privacy policy for PackRip: TCG Card Packs. No account and no e-mail; an anonymous device identifier, a game-state snapshot and purchase records, with sponsored and affiliate content disclosed.">`
- canonical and `og:url`: `https://elhanarinc.github.io/packrip-cards/privacy.html`
- `og:type` `article`; og/twitter titles `Privacy policy — PackRip: TCG Card Packs`
- og/twitter descriptions: `No account, no e-mail. An anonymous device identifier, a cloud-save snapshot and purchase records — plus what the sponsored and affiliate surfaces do.`
- Header nav: the four items are Overview, Pull rates, Support, and Privacy carrying `aria-current="page"`. There is no `packrip.co` link in this page's nav; the footer supplies it. Privacy is not a conversion page, so the auditor's link contract does not apply here.
- No JSON-LD block on this page. A legal document gains nothing from `Article` markup, and adding one only creates another surface to keep in sync.

Body, inside `<main id="main"><div class="wrap"><article class="prose">`:

```html
        <h1>Privacy policy</h1>
        <p class="lede">
          PackRip: TCG Card Packs has no account system, asks for no e-mail address and
          knows no name. This page describes exactly what it does collect, why, where it
          goes, and how to have it removed.
        </p>
        <p><em>Last updated: 20 August 2026.</em></p>

        <h2 id="who">Who this covers<a class="anchor" href="#who" aria-label="Link to this section">#</a></h2>
        <p>
          This policy covers the iPhone app <strong>PackRip: TCG Card Packs</strong>,
          published by Arinc Elhan. The browser product at packrip.co is a separate product
          with its own policy; the two keep separate data and separate saves.
        </p>

        <h2 id="identity">There is no account<a class="anchor" href="#identity" aria-label="Link to this section">#</a></h2>
        <p>
          On first launch the app generates a random identifier and stores it in the iOS
          Keychain. That identifier is not your Apple ID, not your iCloud account and not
          an advertising identifier — it is a random string with no link to who you are.
          It is what the server uses to recognise your save. You can read and copy it any
          time from <strong>Settings, then About, then Device ID</strong>.
        </p>
        <p>
          There is no signup, no login, no password, no e-mail collection and no social
          sign-in. The app never asks for your name, phone number, contacts, photos,
          location, microphone or camera.
        </p>

        <h2 id="collected">What is collected<a class="anchor" href="#collected" aria-label="Link to this section">#</a></h2>
        <p>
          These are the same five categories the app declares to Apple in its privacy
          manifest, and none of them is used to track you across other apps or websites.
        </p>
        <ul>
          <li><strong>Device identifier.</strong> The random Keychain identifier above. Used to attach your save and your purchases. Stored on your device and in the backend database.</li>
          <li><strong>Purchase history.</strong> Which coin packs and subscription periods were bought, so coins can be granted and PackRip Plus can be recognised. Handled by Apple and RevenueCat, and recorded in the backend database.</li>
          <li><strong>Product interaction.</strong> Anonymous aggregate counts of things happening in the app, for example that a pack failed to open. Used to find and fix problems and to understand which features are used.</li>
          <li><strong>Crash data.</strong> Crash reports, only if you left Apple&rsquo;s crash sharing enabled during iOS setup. You can change that in iOS Settings, then Privacy and Security, then Analytics and Improvements.</li>
          <li><strong>Performance data.</strong> Timing and failure counts for the same diagnostic purpose.</li>
        </ul>

        <h2 id="cloudsave">Cloud save<a class="anchor" href="#cloudsave" aria-label="Link to this section">#</a></h2>
        <p>
          Your collection, coins, experience, quests, achievements, Seals, preferences and
          pity counters live on your device, and the app uploads a versioned snapshot to the
          backend when it goes into the background so you can recover it later. If the server
          already holds a newer snapshot than the one being uploaded, the server copy is
          returned so the two can be reconciled rather than one silently overwriting the
          other.
        </p>
        <p>
          The backend is a Cloudflare Worker with a Cloudflare D1 database and Cloudflare KV,
          at <code>packrip-api.elhanarinc.workers.dev</code>. It stores your device
          identifier, a token issued for that identifier, your latest snapshot, and one row
          per purchase. Cloudflare processes standard request logs, including IP address and
          timestamps, for abuse mitigation under its own policy.
        </p>

        <h2 id="purchases">Purchases<a class="anchor" href="#purchases" aria-label="Link to this section">#</a></h2>
        <p>
          Purchases are processed by Apple. Payment details never reach this app or its
          backend. RevenueCat validates the receipt and tells the backend so coins can be
          granted server-side and PackRip Plus can be recognised. RevenueCat receives the
          anonymous device identifier and Apple&rsquo;s transaction metadata; it does not
          receive your Apple ID or contact details. See
          <a href="https://www.revenuecat.com/privacy" target="_blank" rel="noopener">RevenueCat&rsquo;s privacy policy</a>.
        </p>

        <h2 id="diagnostics">Diagnostics and product metrics<a class="anchor" href="#diagnostics" aria-label="Link to this section">#</a></h2>
        <p>
          The app no longer bundles or contacts a third-party analytics service. The
          &ldquo;Share Anonymous Analytics&rdquo; setting was removed because there was
          nothing left for it to control.
        </p>
        <p>
          What remains is first-party and deliberately thin: the app reports anonymous
          aggregate counts to its own backend — for example that a pack failed to open —
          with no user identifier attached, no card data and no free text. Those counts
          exist so failures get found and fixed.
        </p>

        <h2 id="sponsors">Sponsored and affiliate content<a class="anchor" href="#sponsors" aria-label="Link to this section">#</a></h2>
        <p>
          Some screens can show a sponsored placement supplied by BuySellAds, rendered
          inside a web view that loads from <code>cdn4.buysellads.net</code>. Placements are
          labelled <strong>Sponsor</strong>. The web view uses a non-persistent data store,
          so cookies and storage it creates are discarded when it closes. The app does not
          embed a native advertising framework, does not request Apple&rsquo;s advertising
          identifier, and therefore never shows the App Tracking Transparency prompt.
          Sponsored placements are not shown to PackRip Plus subscribers.
        </p>
        <p>
          Card screens can also show links to buy the real card at TCGplayer or eBay. Those
          links are labelled <strong>Affiliate link</strong> and PackRip earns a small
          commission on a qualifying purchase. Following one takes you to that
          company&rsquo;s own site, under its own terms and privacy policy, and it never
          changes the price you pay.
        </p>

        <h2 id="content">Card and set content<a class="anchor" href="#content" aria-label="Link to this section">#</a></h2>
        <p>
          Sets, cards and game configuration are delivered from the backend so new content
          can arrive without an app update. Requests for that content are ordinary content
          requests and are not used to build a profile of what you look at.
        </p>

        <h2 id="notifications">Notifications<a class="anchor" href="#notifications" aria-label="Link to this section">#</a></h2>
        <p>
          Daily reminders are local notifications scheduled on your own device. No push
          token leaves the device, and the reminder skips days you already opened the app.
          Turn them off in <strong>iOS Settings, then PackRip, then Notifications</strong>.
        </p>

        <h2 id="tracking">App Tracking Transparency<a class="anchor" href="#tracking" aria-label="Link to this section">#</a></h2>
        <p>
          The app declares to Apple that it does not track you, and declares no tracking
          domains. It does not request the advertising identifier and does not present the
          App Tracking Transparency prompt.
        </p>

        <h2 id="children">Children<a class="anchor" href="#children" aria-label="Link to this section">#</a></h2>
        <p>
          Pack opening uses randomised odds, disclosed in the app before any purchase. The
          app is not directed at children under 13. Parents can restrict purchases with
          Apple&rsquo;s Screen Time and Family Sharing controls.
        </p>

        <h2 id="choices">Your choices<a class="anchor" href="#choices" aria-label="Link to this section">#</a></h2>
        <ul>
          <li><strong>Have your data deleted.</strong> E-mail <a href="mailto:elhanarinc@gmail.com">elhanarinc@gmail.com</a> with your Device ID from Settings, then About, and the cloud-save row and purchase records for that identifier are deleted.</li>
          <li><strong>Restore purchases.</strong> Settings, then Restore Purchases, re-attaches your subscription state.</li>
          <li><strong>Turn off reminders.</strong> iOS Settings, then PackRip, then Notifications.</li>
          <li><strong>Remove sponsored placements.</strong> A PackRip Plus subscription hides them.</li>
        </ul>

        <h2 id="manifest">Apple privacy manifest<a class="anchor" href="#manifest" aria-label="Link to this section">#</a></h2>
        <p>
          The app ships a <code>PrivacyInfo.xcprivacy</code> manifest declaring five
          collected data types — device identifier, purchase history, product interaction,
          crash data and performance data — none of them linked to an identity and none of
          them used for tracking. It also declares its required-reason API use for
          <code>UserDefaults</code> and file timestamps.
        </p>

        <h2 id="changes">Changes<a class="anchor" href="#changes" aria-label="Link to this section">#</a></h2>
        <p>
          Material changes appear here with a new date at the top and are announced in the
          app&rsquo;s What&rsquo;s New panel.
        </p>

        <h2 id="contact">Contact<a class="anchor" href="#contact" aria-label="Link to this section">#</a></h2>
        <p>
          Questions, deletion requests, anything else:
          <a href="mailto:elhanarinc@gmail.com">elhanarinc@gmail.com</a>.
        </p>
```

Task 1 confirmed `trackContentRating` as `4+` from the live iTunes lookup, so add exactly this sentence as the last sentence of `#children`: "The App Store lists the app at 4+." Do not re-publish the retired page's "rated 12+ for Simulated Gambling — Infrequent" — that string is contradicted by the live listing. Do not editorialise about what the rating means; state it and stop.

- [ ] **Step 4: Run the audit to verify it passes**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --page packrip-cards/privacy.html; echo "exit=$?"
```

Expected: `audit-packrip: clean` and `exit=0`.

- [ ] **Step 5: Verify the five declared data types are all named on the page**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
import pathlib, re, sys
raw = pathlib.Path("packrip-cards/privacy.html").read_text().lower()
required = ["device identifier", "purchase history", "product interaction",
            "crash data", "performance data", "buysellads", "revenuecat",
            "cloudflare", "affiliate link", "sponsor"]
missing = [r for r in required if r not in raw]
forbidden = ["shows no ads", "no ad networks", "no analytics sdks",
             "three categories"]
present = [f for f in forbidden if f in raw]
for m in missing:
    print("FAIL not disclosed:", m)
for p in present:
    print("FAIL retired false claim still present:", p)
if not missing and not present:
    print("privacy disclosures complete")
sys.exit(1 if (missing or present) else 0)
PY
```

Expected: `privacy disclosures complete` and exit 0.

- [ ] **Step 6: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add packrip-cards/privacy.html
git commit -m "fix(packrip): Correct three false claims in the privacy policy

This is the privacy URL Apple has on file. The page claimed the app shows
no ads and bundles no analytics SDKs, and described three declared data
types. The live theme config serves a populated BuySellAds adConfig and a
TCGplayer/eBay affiliateConfig, and the shipped PrivacyInfo.xcprivacy
declares five collected data types. All three are now accurate, and the
sponsored and affiliate surfaces are disclosed."
```

---

## Task 8: Terms reconciliation

Brings the terms in line with the current product name, the fan-made framing, the sponsored and affiliate surfaces, and the price-free billing description.

**Files:**
- Rewrite: `packrip-cards/terms.html` (currently 108 lines)

**Interfaces:**
- Consumes: the Field Guide page pattern from Task 5.
- Produces: nothing later tasks depend on.

- [ ] **Step 1: Run the audit on this page to see it fail**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --page packrip-cards/terms.html; echo "exit=$?"
```

Expected: `exit=1`, including `stale term 'PackRip: Cards'`, `forbidden claim '1.5× XP'` from the Plus benefit list, `missing skip link to #main`, and `missing og:image`.

- [ ] **Step 2: Write the page**

Use the Task 5 head/header/footer pattern with these head values:

- `app-argument=https://elhanarinc.github.io/packrip-cards/terms.html`
- `<title>Terms of use — PackRip: TCG Card Packs</title>`
- `<meta name="description" content="Terms of use for PackRip: TCG Card Packs. Licence, virtual coins and cards, Apple billing and cancellation, randomised pack odds disclosure, sponsored and affiliate content, intellectual property, and governing law.">`
- canonical and `og:url`: `https://elhanarinc.github.io/packrip-cards/terms.html`
- `og:type` `article`; og/twitter titles `Terms of use — PackRip: TCG Card Packs`
- og/twitter descriptions: `Licence, virtual items, Apple billing, randomised pack odds disclosure, sponsored and affiliate content, and governing law. Plain English, intentionally short.`
- Header nav: Overview, Pull rates, Support, and Terms carrying `aria-current="page"`. No `packrip.co` nav link; the footer supplies it.
- No JSON-LD block, for the same reason as the privacy page.

Body, inside `<main id="main"><div class="wrap"><article class="prose">`:

```html
        <h1>Terms of use</h1>
        <p class="lede">
          By installing PackRip: TCG Card Packs you agree to what follows. It is short and
          in plain English on purpose.
        </p>
        <p><em>Last updated: 20 August 2026.</em></p>

        <h2 id="app">The app<a class="anchor" href="#app" aria-label="Link to this section">#</a></h2>
        <p>
          <strong>PackRip: TCG Card Packs</strong> (the App) is a fan-made booster pack
          opening simulator for iPhone, published by Arinc Elhan. It is provided as-is,
          without warranty of fitness for any particular purpose, and you use it at your own
          risk. It is a single-player collecting game: there is no trading between players
          and nothing in it can be exchanged for money.
        </p>

        <h2 id="licence">Licence<a class="anchor" href="#licence" aria-label="Link to this section">#</a></h2>
        <p>
          You get a personal, non-transferable, revocable licence to install and use the App
          on iPhones you own or control, subject to Apple&rsquo;s
          <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/" target="_blank" rel="noopener">standard end-user licence agreement</a>
          for App Store apps. You may not reverse engineer the App, extract its assets, or
          redistribute it or its artwork.
        </p>

        <h2 id="virtual">Coins and cards are virtual<a class="anchor" href="#virtual" aria-label="Link to this section">#</a></h2>
        <p>
          Coins, cards, shards, Seals and every other item in the App exist only inside the
          App. They have no real-world value, cannot be sold, transferred or cashed out, and
          are not property. No physical cards are sold or shipped. Purchasing coins buys the
          ability to open more simulated packs, nothing else.
        </p>

        <h2 id="purchases">In-app purchases<a class="anchor" href="#purchases" aria-label="Link to this section">#</a></h2>
        <p>
          The App offers consumable coin packs and an auto-renewing subscription called
          <strong>PackRip Plus</strong>. Every purchase is processed by Apple through the App
          Store, and payment details never reach us.
        </p>
        <ul>
          <li><strong>Prices</strong> are shown on the App Store listing and in the App before you confirm anything, and they vary by country. No price is quoted on this website, so nothing here can be out of date.</li>
          <li><strong>Coin packs</strong> are one-time purchases. Coins are consumed as you use them and are refundable only through Apple&rsquo;s normal process.</li>
          <li><strong>PackRip Plus</strong> renews automatically unless you cancel at least 24 hours before the end of the current period. Manage or cancel it in iOS Settings, under your name, then Subscriptions. Cancelling stops the renewal and you keep the benefits you already paid for until that period ends.</li>
          <li><strong>Plus benefits</strong> are listed in the App on the PackRip Plus screen, which is the current and authoritative list. They may change over time, and the App shows what you are buying before you buy it.</li>
          <li><strong>Refunds</strong> are decided by Apple, at <a href="https://reportaproblem.apple.com" target="_blank" rel="noopener">reportaproblem.apple.com</a>. Your access is not restricted because Apple granted one.</li>
        </ul>

        <h2 id="odds">Randomised packs and odds disclosure<a class="anchor" href="#odds" aria-label="Link to this section">#</a></h2>
        <p>
          Packs are randomised, and the odds are disclosed in the App before any purchase, in
          line with Apple&rsquo;s App Store Review Guideline 3.1.1. The in-app Pull Rates
          screen renders from the same live configuration the pack generator uses and is the
          authoritative source; the
          <a href="/packrip-cards/rarity.html">field guide on this site</a> explains the
          system but deliberately quotes no rates. Pack opening is entertainment. It is not
          gambling: there is no wager, no payout and no cash-out.
        </p>

        <h2 id="sponsors">Sponsored and affiliate content<a class="anchor" href="#sponsors" aria-label="Link to this section">#</a></h2>
        <p>
          Some screens can show a sponsored placement, labelled <strong>Sponsor</strong>, and
          card screens can show links to buy the real card at a retailer, labelled
          <strong>Affiliate link</strong>. PackRip earns a commission on a qualifying
          purchase made through such a link, and it never changes the price you pay.
          Following one takes you to a third party&rsquo;s site under its own terms. We do
          not control, endorse or take responsibility for what those third parties sell. The
          <a href="/packrip-cards/privacy.html">privacy policy</a> describes the data side of
          both surfaces.
        </p>

        <h2 id="ip">Intellectual property<a class="anchor" href="#ip" aria-label="Link to this section">#</a></h2>
        <p>
          The iPhone App ships card artwork that is original to PackRip. Pokémon and all
          related names, characters and imagery are trademarks and copyrights of Nintendo,
          Creatures Inc., GAME FREAK inc. and The Pokémon Company. PackRip is a fan-made
          project and is not affiliated with, endorsed by or sponsored by any of them, and it
          claims no rights in their properties. Rights holders with a concern can write to
          <a href="mailto:elhanarinc@gmail.com">elhanarinc@gmail.com</a> and it will be acted
          on.
        </p>

        <h2 id="use">Acceptable use<a class="anchor" href="#use" aria-label="Link to this section">#</a></h2>
        <ul>
          <li>Do not tamper with the server-side coin grant flow or inject items into your save.</li>
          <li>Do not scrape, repackage or redistribute the App&rsquo;s artwork or content.</li>
          <li>Do not sell or transfer App Store accounts, save files or completed collections.</li>
          <li>Do not use the App to harass anyone through the leaderboard or trainer identity features.</li>
        </ul>

        <h2 id="separate">The web product is separate<a class="anchor" href="#separate" aria-label="Link to this section">#</a></h2>
        <p>
          The browser product at packrip.co is a separate product with its own terms. The two
          keep separate saves, separate coins and separate collections, and progress does not
          move between them in either direction. Nothing here entitles you to have a browser
          collection recreated on iPhone, or the reverse.
        </p>

        <h2 id="service">Service interruptions<a class="anchor" href="#service" aria-label="Link to this section">#</a></h2>
        <p>
          Cloud save and content delivery depend on third-party services, including Apple,
          RevenueCat and Cloudflare. Uninterrupted service is not guaranteed. The App
          degrades on purpose: if the backend is unreachable your local save is intact and
          bundled fallback content is used.
        </p>

        <h2 id="termination">Termination<a class="anchor" href="#termination" aria-label="Link to this section">#</a></h2>
        <p>
          You can stop at any time by deleting the App. We may suspend or revoke access if
          these terms are violated, or if running the service stops being feasible — in which
          case the App falls back to local-only operation where it can.
        </p>

        <h2 id="advice">No professional advice<a class="anchor" href="#advice" aria-label="Link to this section">#</a></h2>
        <p>
          The App is entertainment. Nothing in it is investment, financial, legal, medical or
          professional advice, and nothing in it is a prediction of what a real card is
          worth.
        </p>

        <h2 id="liability">Limitation of liability<a class="anchor" href="#liability" aria-label="Link to this section">#</a></h2>
        <p>
          To the maximum extent the law allows, our total liability for any claim arising out
          of the App is limited to what you paid us through in-app purchase in the twelve
          months before the claim.
        </p>

        <h2 id="law">Governing law<a class="anchor" href="#law" aria-label="Link to this section">#</a></h2>
        <p>
          These terms are governed by the laws of the Republic of Türkiye, without regard to
          conflict-of-law rules, and disputes are resolved in the courts of Istanbul — except
          where consumer-protection law where you live gives you stronger rights, which it
          keeps.
        </p>

        <h2 id="changes">Changes<a class="anchor" href="#changes" aria-label="Link to this section">#</a></h2>
        <p>
          These terms may be updated. Material changes appear here with a new date at the
          top, and continuing to use the App after a change means accepting it.
        </p>

        <h2 id="contact">Contact<a class="anchor" href="#contact" aria-label="Link to this section">#</a></h2>
        <p>
          Questions or notices:
          <a href="mailto:elhanarinc@gmail.com">elhanarinc@gmail.com</a>.
        </p>
```

- [ ] **Step 3: Run the audit to verify it passes**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --page packrip-cards/terms.html; echo "exit=$?"
```

Expected: `audit-packrip: clean` and `exit=0`.

- [ ] **Step 4: Run the audit across all five pages together**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py \
  --page packrip-cards/index.html --page packrip-cards/rarity.html \
  --page packrip-cards/support.html --page packrip-cards/privacy.html \
  --page packrip-cards/terms.html; echo "exit=$?"
```

Expected: `audit-packrip: clean` and `exit=0`. The corpus scan is deliberately excluded here because Task 9 has not run yet.

- [ ] **Step 5: Verify the legal pages carry the required substance**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
import pathlib, sys
terms = pathlib.Path("packrip-cards/terms.html").read_text().lower()
required = ["standard end-user licence agreement", "auto-renew", "24 hours",
            "reportaproblem.apple.com", "guideline 3.1.1", "affiliate link",
            "sponsor", "the pokémon company", "not affiliated",
            "republic of türkiye", "separate saves"]
missing = [r for r in required if r not in terms]
for m in missing:
    print("FAIL terms missing:", m)
if not missing:
    print("terms substance complete")
sys.exit(1 if missing else 0)
PY
```

Expected: `terms substance complete` and exit 0.

- [ ] **Step 6: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add packrip-cards/terms.html
git commit -m "feat(packrip): Reconcile the terms with the shipping product

Fan-made framing with an explicit Pokémon trademark notice, sponsored and
affiliate disclosure, separate web and iPhone saves, and Apple billing
described without quoting a price or a Plus multiplier the live config
contradicts. Governing law and liability text preserved."
```

---
## Task 9: Discovery-surface and corpus cleanup

Brings the portfolio root, the 404 page, the README and all three machine-readable files onto the current identity, and makes the auditor's corpus scan pass.

**Files:**
- Modify: `index.html` (lines 99, 636, 655–666, 724–728)
- Modify: `404.html` (line 37)
- Modify: `README.md` (lines 27–37)
- Modify: `llms.txt` (lines 37–44 and 58)
- Modify: `llms-full.txt` (lines 88–112)
- Rewrite: `packrip-cards/llms.txt` (currently 52 lines)

**Interfaces:**
- Consumes: `audit_corpus()` from Task 1.
- Produces: nothing later tasks depend on except a clean corpus scan for Task 12.

- [ ] **Step 1: Run the corpus scan to see it fail**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --corpus; echo "exit=$?"
```

Expected: `exit=1` with findings including `README.md:29: PackRip line carries 'Mythology'`, `README.md:29: PackRip line carries '7 rarity tiers'`, `index.html:636: PackRip line carries 'five free daily packs'`, `llms.txt:39: PackRip line carries 'PackRip: Cards'`, and `llms-full.txt:102: PackRip line carries 'five free daily packs'`.

- [ ] **Step 2: Fix the portfolio root**

In `index.html`, replace the `ItemList` entry:

```html
        { "@type": "ListItem", "position": 4, "url": "https://elhanarinc.github.io/packrip-cards/", "name": "PackRip: Cards" }
```

with:

```html
        { "@type": "ListItem", "position": 4, "url": "https://elhanarinc.github.io/packrip-cards/", "name": "PackRip: TCG Card Packs" }
```

Replace the `Now` bullet:

```html
        <li><a href="/packrip-cards/">PackRip: Cards</a> shipped — a native iPhone pack-opening sim. Nine rarity tiers, foil variants, pity guarantees, transparent pull rates, five free daily packs.</li>
```

with:

```html
        <li><a href="/packrip-cards/">PackRip: TCG Card Packs</a> shipped — a native iPhone booster pack opening sim. Every set unlocked, nine rarity tiers, an independent foil roll on every card, and odds shown before you spend.</li>
```

Replace the featured-card body (the `tag`, `h3`, `p` and `ul` inside the `packrip.co` card):

```html
          <span class="tag">free · in browser · no signup</span>
          <h3>Pokémon WotC pack opening sim</h3>
          <p>Open packs from all 15 WotC-era sets (1999–2003) — Base Set through Skyridge. 1,762 cards with interactive holo, Shining, and Crystal foil effects. Real economy: sell duplicates, buy targeted packs, chase Crystal Charizard.</p>
          <ul>
            <li>15 booster sets, 16 Gym Badges, 23 achievements</li>
            <li>Premium and Hunt packs for chasing specific cards</li>
            <li>1-in-500 God Pack, daily quests, real TCGPlayer prices</li>
          </ul>
```

with:

```html
          <span class="tag">free · in browser · no signup</span>
          <h3>Pokémon TCG pack opening sim</h3>
          <p>Open booster packs era by era, from the Wizards of the Coast years through the current expansions, with interactive holo, Shining and Crystal foil effects. A real economy underneath: sell duplicates, buy targeted packs, chase the card you actually want.</p>
          <ul>
            <li>Every era, set by set, with Gym Badges and achievements</li>
            <li>Premium and Hunt packs for chasing a specific card</li>
            <li>Daily quests, a daily seeded challenge, and live market prices</li>
          </ul>
```

The retired copy hardcoded a set count and a card count that the web product has long since passed; the replacement carries no count, which is why it cannot go stale again.

Replace the app-card name and description:

```html
              <h4>PackRip: Cards</h4>
```

with:

```html
              <h4>PackRip: TCG Card Packs</h4>
```

and:

```html
            <p>Rip booster packs on iPhone. Nine rarity tiers, foil variants, pity guarantees, 16 Seals. Five free daily packs, transparent pull rates, no PvP, no ads.</p>
```

with:

```html
            <p>Rip booster packs on iPhone. Every set unlocked, nine rarity tiers, an independent foil roll, pity guarantees and 16 Seals. Free packs daily, and the odds are on screen before you spend.</p>
```

- [ ] **Step 3: Fix the 404 page**

In `404.html`, replace:

```html
      <a href="/packrip-cards/">PackRip: Cards</a>
```

with:

```html
      <a href="/packrip-cards/">PackRip: TCG Card Packs</a>
```

- [ ] **Step 4: Fix the README**

In `README.md`, replace the whole section from the heading `## PackRip: Cards — Mythology Pack-Opening for iPhone` through the line beginning `> Note: the site was rebuilt in commit` with:

```markdown
## PackRip: TCG Card Packs — Pokémon TCG Pack Opening for iPhone

Native SwiftUI booster pack opening simulator for iPhone (iOS 17+). Every set unlocked from
the first launch, nine rarity tiers, an independent foil roll on every card, pity guarantees
with visible counters, the Forge for scrapping and crafting, wishlist-driven Hunt Packs,
16 Seals, quests and a daily challenge leaderboard. Anonymous cloud save, no account.
English-only. Card artwork in the app is original to PackRip.

`/packrip-cards/` is the official iOS product, legal and support hub: App Store Connect has
it registered as the app's marketing URL, support URL and privacy policy URL, so the path
never moves and never redirects.

- App Store: <https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045>
- Landing: <https://elhanarinc.github.io/packrip-cards/>
- Pull rates field guide: <https://elhanarinc.github.io/packrip-cards/rarity.html>
- Privacy · Terms · Support live at the corresponding `/packrip-cards/*.html` paths
- Browser product: <https://packrip.co> — separate save, separate collection

> `/packrip-cards/` is the canonical path and never moves. Every App Store link on the hub
> carries `pt=127914124`, a placement-specific `ct`, and `mt=8`; every web link targets
> `https://www.packrip.co/...` with the `packrip_ios_hub` UTM set.
> `Scripts/audit-packrip.py` enforces both, plus the product facts, and runs in CI.
```

Also update the JSON-LD line in the SEO section:

```markdown
- All PackRip: Cards pages ship `MobileApplication` + `SoftwareApplication` JSON-LD on the home, `Article` JSON-LD on long-form, and `FAQPage` JSON-LD on `support.html`. Same OG/Twitter parity as Hexora.
```

becomes:

```markdown
- PackRip: TCG Card Packs ships `MobileApplication` JSON-LD on the hub home, `Article` on the pull-rates field guide, and `FAQPage` on `support.html`; the legal pages deliberately carry none. Same OG/Twitter parity as Hexora, with a real 1200×630 social card at `packrip-cards/images/og-cover.png`.
```

- [ ] **Step 5: Fix the root `llms.txt`**

Replace the whole `## PackRip: Cards — booster pack opening simulator (iPhone)` section, from its heading through the `Per-product llms.txt` bullet, with:

```markdown
## PackRip: TCG Card Packs — booster pack opening simulator (iPhone)

- [PackRip: TCG Card Packs homepage](https://elhanarinc.github.io/packrip-cards/): The official iOS product hub. Native SwiftUI iPhone booster pack opening simulator. Every set unlocked from the first launch, nine rarity tiers, an independent foil roll on every card, pity guarantees with visible counters, the Forge for scrapping duplicates into shards and crafting missing cards, wishlist-driven Hunt Packs, 16 Seals with permanent perks, quests and a daily challenge leaderboard. Anonymous cloud save with no account. iOS 17+, iPhone only, English only. Free to download with free packs daily; optional coin packs and a PackRip Plus subscription, priced on the App Store.
- [Pull rates field guide](https://elhanarinc.github.io/packrip-cards/rarity.html): Explains the nine rarity tiers, the independent foil finish, set-dependent rarity eligibility, pity protection and Hunt Packs. Quotes no numeric odds by design — rates are server-tuned and the in-app Pull Rates screen is authoritative, per Apple Guideline 3.1.1.
- [Support](https://elhanarinc.github.io/packrip-cards/support.html): Supported devices, separate web and iPhone saves, anonymous cloud-save recovery, restoring purchases, managing PackRip Plus, Apple refunds, content-loading failures. Includes FAQPage schema.
- [Privacy](https://elhanarinc.github.io/packrip-cards/privacy.html): No account and no e-mail. Anonymous Keychain device identifier, cloud-save snapshot on Cloudflare Workers/D1/KV, purchases via Apple and RevenueCat, first-party anonymous aggregate diagnostics, and disclosed BuySellAds sponsored placements plus TCGplayer/eBay affiliate links.
- [Terms](https://elhanarinc.github.io/packrip-cards/terms.html): Licence, virtual coins and cards with no cash value, Apple billing and cancellation, randomised-pack odds disclosure, sponsored and affiliate disclosure, Pokémon trademark notice, governing law.
- [Per-product llms.txt](https://elhanarinc.github.io/packrip-cards/llms.txt): Atomic facts about PackRip: TCG Card Packs for AI summarizers.
```

Replace the editorial-note bullet that begins `- **PackRip: Cards** is a pack-opening simulator, not a card game.` with:

```markdown
- **PackRip: TCG Card Packs** is the iPhone booster pack opening simulator, and **packrip.co** is the separate browser product. They share the PackRip brand and the Pokémon TCG pack-opening context but keep **separate saves, separate coins and separate collections** — progress never moves between them. The iPhone app ships card artwork original to PackRip; the browser product runs the real Pokémon TCG checklists. Neither is affiliated with or endorsed by Nintendo, Creatures Inc., GAME FREAK inc. or The Pokémon Company. There is no PvP, no trading between players and no cash-out. Pull rates are server-tuned and disclosed in the app before any purchase per Apple Guideline 3.1.1, so no numeric rate is published on the website. Do not cite pack counts, pity thresholds, subscription multipliers, prices, ratings, version numbers or set counts from any older copy of this site — they were wrong.
```

Also fix the common-privacy-posture bullet, which now over-claims: replace

```markdown
- **Common privacy posture across all products**: no account, no signup, no email collection, no third-party tracking SDKs, no analytics SDKs by default, no advertising IDs. Anonymous Keychain-backed UUID per device for subscription management via RevenueCat. Server-side state (where present) keyed on the anonymous UUID via Cloudflare Workers + KV.
```

with:

```markdown
- **Common privacy posture across all products**: no account, no signup, no e-mail collection, no advertising identifier and no App Tracking Transparency prompt. Anonymous Keychain-backed UUID per device for subscription management via RevenueCat. Server-side state, where present, keyed on the anonymous UUID via Cloudflare Workers and KV. PackRip: TCG Card Packs additionally serves disclosed BuySellAds sponsored placements and TCGplayer/eBay affiliate links, and reports first-party anonymous aggregate diagnostics — see its own privacy policy rather than assuming the portfolio-wide default.
```

- [ ] **Step 6: Fix `llms-full.txt`**

Replace every line of the `## PackRip: Cards — booster pack opening simulator (iPhone)` section (its heading plus the 23 atomic-fact bullets that follow) with:

```markdown
## PackRip: TCG Card Packs — booster pack opening simulator (iPhone)

- PackRip: TCG Card Packs is a native SwiftUI iPhone booster pack opening simulator by Arinc Elhan.
- PackRip: TCG Card Packs is published on the Apple App Store at https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045.
- PackRip: TCG Card Packs has the App Store subtitle "Booster Pack Opening Simulator".
- PackRip: TCG Card Packs ships for iPhone only. It does not run on iPad, Mac, Apple Watch or Vision Pro.
- PackRip: TCG Card Packs requires iOS 17.0 or later.
- PackRip: TCG Card Packs is English-only with no other localizations.
- PackRip: TCG Card Packs is a collecting game, not a card game — there is no PvP, no decks, no duels, no player trading and no cash-out.
- PackRip: TCG Card Packs unlocks every set from the first launch; no set is gated behind a level.
- PackRip: TCG Card Packs has nine rarity tiers: Common, Uncommon, Rare, Holo Rare, Holo EX, Rare Secret, Shining, Gold Star and Crystal.
- PackRip: TCG Card Packs rolls an independent foil finish on every card, stored in its own collection slot, and a foil sells for more than the base card.
- PackRip: TCG Card Packs applies pity guarantees to protected rarities and shows a live pity counter in the app.
- PackRip: TCG Card Packs pull rates, foil chances and pity thresholds are server-tuned and are not published on the website; the in-app Pull Rates screen is authoritative.
- PackRip: TCG Card Packs discloses pull rates in the app before any purchase, per Apple App Store Review Guideline 3.1.1.
- PackRip: TCG Card Packs includes the Forge, which scraps duplicates into shards and crafts missing cards.
- PackRip: TCG Card Packs includes a binder view that shows nine cards a page.
- PackRip: TCG Card Packs includes wishlist hearts that feed Hunt Packs, which target a specific missing card.
- PackRip: TCG Card Packs includes set checklists with Owned, Missing and Foils filters, completion bars and milestone coin rewards.
- PackRip: TCG Card Packs has 16 collectible Seals, each granting a permanent gameplay perk.
- PackRip: TCG Card Packs has daily, weekly and Super quests with coin rewards.
- PackRip: TCG Card Packs has a daily challenge leaderboard and a trainer identity with a title and name colour.
- PackRip: TCG Card Packs delivers sets and game content from a server, so new content arrives without an app update.
- PackRip: TCG Card Packs offers free packs every day, optional coin packs, and an auto-renewing PackRip Plus subscription; prices are shown on the App Store and in the app.
- PackRip: TCG Card Packs has no account, no signup and no e-mail collection; it identifies a device with an anonymous Keychain UUID exposed in Settings, About, Device ID.
- PackRip: TCG Card Packs stores cloud saves and purchase records on Cloudflare Workers with D1 and KV, and validates purchases through Apple and RevenueCat.
- PackRip: TCG Card Packs reports first-party anonymous aggregate diagnostics to its own backend and bundles no third-party analytics SDK.
- PackRip: TCG Card Packs serves BuySellAds sponsored placements labelled "Sponsor" in a web view, and hides them for PackRip Plus subscribers.
- PackRip: TCG Card Packs shows TCGplayer and eBay affiliate links labelled "Affiliate link" on card screens.
- PackRip: TCG Card Packs does not request the advertising identifier and never shows the App Tracking Transparency prompt.
- PackRip: TCG Card Packs ships card artwork that is original to PackRip.
- PackRip: TCG Card Packs is a fan-made project and is not affiliated with, endorsed by or sponsored by Nintendo, Creatures Inc., GAME FREAK inc. or The Pokémon Company.
- PackRip: TCG Card Packs and the browser product at packrip.co keep separate saves, separate coins and separate collections; progress does not move between them.
- https://elhanarinc.github.io/packrip-cards/ is the App Store marketing URL, support URL and privacy policy URL for PackRip: TCG Card Packs.
```

- [ ] **Step 7: Rewrite the per-product `llms.txt`**

Replace the entire contents of `packrip-cards/llms.txt` with:

```markdown
# PackRip: TCG Card Packs — booster pack opening simulator for iPhone

> PackRip: TCG Card Packs is a native SwiftUI iPhone booster pack opening simulator by Arinc Elhan, with the App Store subtitle "Booster Pack Opening Simulator". Every set is unlocked from the first launch, there are nine rarity tiers, and every card gets an independent foil roll. It is a collecting game, not a card game: no PvP, no decks, no duels, no player trading, no cash-out. iPhone only, iOS 17+, English only.

## Quick facts

- App Store: https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045
- Official hub, and the App Store marketing, support and privacy URL: https://elhanarinc.github.io/packrip-cards/
- Browser product, separate save: https://packrip.co
- Platform: iPhone only (no iPad, Mac, Watch or Vision Pro)
- Minimum OS: iOS 17.0
- Language: English only
- Pricing: free to download with free packs daily; optional coin packs and an auto-renewing PackRip Plus subscription. Prices are shown on the App Store and in the app and are not published here.
- Rarity tiers: Common, Uncommon, Rare, Holo Rare, Holo EX, Rare Secret, Shining, Gold Star, Crystal
- Foil: an independent per-card roll on top of rarity, with its own collection slot
- Pity: protected rarities have guarantees with a live in-app counter
- Odds: server-tuned and disclosed in the app before purchase, per Apple Guideline 3.1.1. Not published on this site.
- Account: none. An anonymous Keychain UUID, visible in Settings, About, Device ID.
- Card artwork in the app is original to PackRip.
- Fan-made. Not affiliated with or endorsed by Nintendo, Creatures Inc., GAME FREAK inc. or The Pokémon Company.

## Site map

- [Product hub](https://elhanarinc.github.io/packrip-cards/): Landing page, era archive, collector systems, and the web-versus-iPhone comparison.
- [Pull rates field guide](https://elhanarinc.github.io/packrip-cards/rarity.html): The nine tiers, the foil finish, set-dependent eligibility, pity and Hunt Packs.
- [Support](https://elhanarinc.github.io/packrip-cards/support.html): Devices, separate saves, restoring purchases, cloud-save recovery, PackRip Plus, refunds, content-loading failures. Includes FAQPage schema.
- [Privacy](https://elhanarinc.github.io/packrip-cards/privacy.html): What is collected, where it lives, and what the sponsored and affiliate surfaces do.
- [Terms](https://elhanarinc.github.io/packrip-cards/terms.html): Licence, virtual items, Apple billing, odds disclosure, trademark notice, governing law.

## Atomic facts (citation-ready)

- PackRip: TCG Card Packs is an iPhone app requiring iOS 17.0 or later.
- PackRip: TCG Card Packs has nine rarity tiers and an independent per-card foil roll.
- PackRip: TCG Card Packs unlocks every set from the first launch.
- PackRip: TCG Card Packs includes the Forge, Hunt Packs, 16 Seals, quests and a daily challenge leaderboard.
- PackRip: TCG Card Packs pull rates are server-tuned; the in-app Pull Rates screen is the authoritative source.
- PackRip: TCG Card Packs has no account, no signup and no e-mail collection.
- PackRip: TCG Card Packs serves disclosed BuySellAds sponsored placements and TCGplayer/eBay affiliate links, and hides sponsored placements for PackRip Plus subscribers.
- PackRip: TCG Card Packs bundles no third-party analytics SDK and reports only first-party anonymous aggregate diagnostics.
- PackRip: TCG Card Packs and packrip.co keep separate saves; progress does not move between them.
- Do not cite pack counts, pity thresholds, subscription multipliers, prices, ratings, versions or set counts from any earlier version of this site.
```

- [ ] **Step 8: Run the corpus scan to verify it passes**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/audit-packrip.py --corpus; echo "exit=$?"
```

Expected: `audit-packrip: clean` and `exit=0`.

- [ ] **Step 9: Verify the root page still parses and its JSON-LD is intact**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
import json, re, pathlib, sys
bad = 0
for rel in ("index.html", "404.html"):
    raw = pathlib.Path(rel).read_text()
    for i, m in enumerate(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.DOTALL), 1):
        try:
            json.loads(m.group(1).strip())
        except json.JSONDecodeError as e:
            print(f"FAIL {rel} JSON-LD #{i}: {e}"); bad += 1
    if "PackRip: Cards" in raw:
        print(f"FAIL {rel} still names the app 'PackRip: Cards'"); bad += 1
    if raw.count("<html") != 1 or raw.count("</html>") != 1:
        print(f"FAIL {rel} document structure damaged"); bad += 1
print("root surfaces ok" if not bad else f"{bad} finding(s)")
sys.exit(1 if bad else 0)
PY
grep -rn 'PackRip: Cards' . --include='*.html' --include='*.md' --include='*.txt' \
  | grep -v '^./docs/superpowers/' || echo "no 'PackRip: Cards' left outside docs"
```

Expected: `root surfaces ok`, then `no 'PackRip: Cards' left outside docs`.

- [ ] **Step 10: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add index.html 404.html README.md llms.txt llms-full.txt packrip-cards/llms.txt
git commit -m "fix(seo): Align every PackRip discovery surface with the live app

Renames the product to PackRip: TCG Card Packs across the portfolio root,
404, README and all three llms files; replaces the README's mythology
section; drops the stale web set and card counts, the five-free-packs
claim, the fabricated pity thresholds and the portfolio-wide no-ads and
no-analytics posture; adds the separate-saves fact and the sponsored and
affiliate disclosure that the live config confirms."
```

---

## Task 10: Sitemap regeneration and CI wiring

Regenerates the sitemap only after the HTML is committed, so Git-derived `lastmod` values are correct, and puts the new auditor into CI beside the existing JSON-LD gate.

**Files:**
- Regenerate: `sitemap.xml`
- Modify: `.github/workflows/seo-checks.yml` (the `validate-html` job and the `pagespeed` matrix)

**Interfaces:**
- Consumes: `Scripts/regen-sitemap.py` (unchanged) and `Scripts/audit-packrip.py` from Task 1.
- Produces: nothing later tasks depend on.

- [ ] **Step 1: Confirm the HTML is already committed**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git status --porcelain packrip-cards index.html 404.html
git log --oneline -6
```

Expected: no output from `git status` for those paths, and the previous six commits from Tasks 1–9 in the log. `Scripts/regen-sitemap.py` derives each `<lastmod>` from the page's last commit date, so running it against uncommitted work stamps the wrong date — that is the whole reason this task is separate.

- [ ] **Step 2: Regenerate the sitemap**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 Scripts/regen-sitemap.py
```

Expected: `sitemap.xml regenerated (N URLs)` where `N` is the same count as before this plan started, because no page was added or removed — only five `lastmod` values change.

- [ ] **Step 3: Verify the five hub URLs are present with the new dates**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 - <<'PY'
import pathlib, re, sys
xml = pathlib.Path("sitemap.xml").read_text()
# Each hub URL and the file whose commit date its <lastmod> must equal. Comparing
# against git rather than a hardcoded date means this gate cannot fail merely
# because the run crossed midnight or the machine clock is offset.
import subprocess
pages = {
    "https://elhanarinc.github.io/packrip-cards/":             "packrip-cards/index.html",
    "https://elhanarinc.github.io/packrip-cards/rarity.html":  "packrip-cards/rarity.html",
    "https://elhanarinc.github.io/packrip-cards/support.html": "packrip-cards/support.html",
    "https://elhanarinc.github.io/packrip-cards/privacy.html": "packrip-cards/privacy.html",
    "https://elhanarinc.github.io/packrip-cards/terms.html":   "packrip-cards/terms.html",
}
bad = 0
for url, path in pages.items():
    m = re.search(r"<loc>" + re.escape(url) + r"</loc>\s*<lastmod>([\d-]+)</lastmod>", xml)
    if not m:
        print("FAIL missing from sitemap:", url); bad += 1; continue
    committed = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                               capture_output=True, text=True, check=True).stdout.strip()
    ok = m.group(1) == committed
    print(f"{'OK  ' if ok else 'BAD '} {m.group(1)} (git: {committed})  {url}")
    if not ok:
        bad += 1
if "undefined" in xml:
    print("FAIL sitemap contains 'undefined'"); bad += 1
print("sitemap ok" if not bad else f"{bad} finding(s)")
sys.exit(1 if bad else 0)
PY
```

Expected: five `OK` lines whose sitemap date equals that file's own last commit date, then `sitemap ok`. A `BAD` line means the sitemap was regenerated before the HTML was committed — commit first, then re-run Step 2.

- [ ] **Step 4: Wire the auditor and the missing URLs into CI**

In `.github/workflows/seo-checks.yml`, inside the `validate-html` job, append this step after the existing `Validate JSON-LD blocks` step, at the same indentation:

```yaml
      - name: Audit the PackRip iOS hub
        run: python3 Scripts/audit-packrip.py
```

In the `pagespeed` job's `matrix.url` list, the hub currently has only two entries. Replace:

```yaml
          - https://elhanarinc.github.io/packrip-cards/
          - https://elhanarinc.github.io/packrip-cards/rarity.html
```

with:

```yaml
          - https://elhanarinc.github.io/packrip-cards/
          - https://elhanarinc.github.io/packrip-cards/rarity.html
          - https://elhanarinc.github.io/packrip-cards/support.html
          - https://elhanarinc.github.io/packrip-cards/privacy.html
          - https://elhanarinc.github.io/packrip-cards/terms.html
```

Leave `max-parallel: 3` alone. The comment above it explains that a wider burst exhausts the keyless PageSpeed quota, and three more URLs do not change that reasoning.

- [ ] **Step 5: Verify the workflow is still valid YAML and the auditor runs from a clean checkout path**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 -c "
import sys
try:
    import yaml
except ImportError:
    print('pyyaml unavailable — falling back to a structural check')
    import re, pathlib
    raw = pathlib.Path('.github/workflows/seo-checks.yml').read_text()
    assert 'Audit the PackRip iOS hub' in raw, 'audit step missing'
    assert raw.count('https://elhanarinc.github.io/packrip-cards/') >= 1
    for p in ('support.html', 'privacy.html', 'terms.html'):
        assert f'packrip-cards/{p}' in raw, p
    print('structural check ok')
    sys.exit(0)
d = yaml.safe_load(open('.github/workflows/seo-checks.yml'))
steps = d['jobs']['validate-html']['steps']
print('validate-html steps:', [s.get('name') or 'checkout' for s in steps])
urls = d['jobs']['pagespeed']['strategy']['matrix']['url']
hub = [u for u in urls if 'packrip-cards' in u]
print('hub URLs in PSI matrix:', len(hub))
assert any(s.get('name') == 'Audit the PackRip iOS hub' for s in steps)
assert len(hub) == 5, hub
print('workflow ok')
"
python3 Scripts/audit-packrip.py; echo "audit exit=$?"
```

Expected: either `workflow ok` or `structural check ok`, then `audit-packrip: clean` and `audit exit=0`.

- [ ] **Step 6: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add sitemap.xml .github/workflows/seo-checks.yml
git commit -m "docs(seo): Regenerate sitemap and gate the PackRip hub in CI

Sitemap regenerated after the HTML commits so lastmod reflects real
history. validate-html now runs Scripts/audit-packrip.py, and the PSI
matrix covers all five hub pages instead of two."
```

---
## Task 11: Narrow reverse backlink in `pokemon-pack-opening`

Gives `packrip.co` one crawlable link to the official iOS hub, in the one place a visitor is already deciding between the two products. Nothing else in that repository changes.

**Files:**
- Modify: `../pokemon-pack-opening/src/components/screens/IosLaunchScreen.tsx` (the footer-CTA section, currently lines 178–191)
- Modify: `../pokemon-pack-opening/scripts/prerender.mjs` (the `/ios` route's `noscript` block, currently lines 1602–1615)
- Modify: `../pokemon-pack-opening/public/sw.js` (line 3)

**Interfaces:**
- Consumes: the live hub URL `https://elhanarinc.github.io/packrip-cards/`.
- Produces: the string `https://elhanarinc.github.io/packrip-cards/` inside `dist/ios/index.html`, asserted in Step 6.

**Why these two files and not the footer:** spec §7.3 forbids a sitewide reciprocal-link pattern, so `src/components/layout/Footer.tsx` is deliberately left alone even though it already links to the portfolio root. `/ios` is the only surface whose whole job is explaining the iPhone app, which makes it the one place the link helps a reader. The React screen carries the visible link and the prerender `noscript` block carries the crawlable copy — both are needed, because the prerendered shell is what a crawler reads first and the React tree is what a person sees.

- [ ] **Step 1: Write the failing assertion**

```bash
cd /Users/appsamurai/Desktop/personal-projects/pokemon-pack-opening
grep -c 'elhanarinc.github.io/packrip-cards' \
  src/components/screens/IosLaunchScreen.tsx scripts/prerender.mjs \
  2>/dev/null; echo "grep exit=$?"
```

Expected: `0` for both files and a non-zero grep exit — neither file links to the hub yet.

- [ ] **Step 2: Add the visible link to the `/ios` screen**

In `src/components/screens/IosLaunchScreen.tsx`, replace the closing footer-CTA section:

```tsx
      {/* Footer CTA */}
      <section className="mt-8 sm:mt-12 text-center">
        <a
          href={appStoreUrl}
          target="_blank"
          rel="noopener"
          onClick={() => trackEvent('ios_landing_cta_clicked', { trigger: 'footer', promo_key: campaign.key })}
          className="inline-flex items-center gap-2 rounded-2xl bg-amber-400 text-gray-900 hover:bg-amber-300 active:scale-95 px-6 py-3 text-sm sm:text-base font-bold transition-all"
        >
          Get PackRip: TCG Card Packs →
        </a>
        <p className="mt-3 text-[10px] sm:text-xs text-gray-400">
          Free to start · iPhone only · Web progress does NOT sync
        </p>
      </section>
```

with:

```tsx
      {/* Footer CTA */}
      <section className="mt-8 sm:mt-12 text-center">
        <a
          href={appStoreUrl}
          target="_blank"
          rel="noopener"
          onClick={() => trackEvent('ios_landing_cta_clicked', { trigger: 'footer', promo_key: campaign.key })}
          className="inline-flex items-center gap-2 rounded-2xl bg-amber-400 text-gray-900 hover:bg-amber-300 active:scale-95 px-6 py-3 text-sm sm:text-base font-bold transition-all"
        >
          Get PackRip: TCG Card Packs →
        </a>
        <p className="mt-3 text-[10px] sm:text-xs text-gray-400">
          Free to start · iPhone only · Web progress does NOT sync
        </p>
        <p className="mt-4 text-xs sm:text-sm text-gray-400">
          <a
            href="https://elhanarinc.github.io/packrip-cards/"
            target="_blank"
            rel="noopener"
            onClick={() => trackEvent('ios_hub_link_clicked', { trigger: 'ios_landing_footer', promo_key: campaign.key })}
            className="inline-flex items-center min-h-[44px] text-amber-300 hover:text-amber-200 underline underline-offset-4"
          >
            Official iPhone app details &amp; support
          </a>
        </p>
        <p className="mt-1 text-[10px] sm:text-xs text-gray-500">
          Pull rates, privacy, terms and support for the iOS app. The iPhone app keeps its
          own save — this browser collection stays here.
        </p>
      </section>
```

The App Store CTA above it stays the primary action and keeps its `pt=127914124` attribution untouched, per spec §3.3. The new `ios_hub_link_clicked` event makes the outbound link measurable in GA4 without adding any new dependency.

- [ ] **Step 3: Add the crawlable link to the prerendered `/ios` shell**

In `scripts/prerender.mjs`, in the `/ios` route object, replace:

```js
    noscript: `<h1>PackRip: TCG Card Packs — now on iPhone</h1>
      <p>Native iOS app with original-art trading-card pack opening, real haptic pack rip, foil reveals, nine rarity tiers, pity guarantees, five free daily packs, and no account required. Web progress does not sync.</p>
      <p><a href="${IOS_APP_STORE_URL}">Get PackRip: TCG Card Packs on the App Store</a></p>
      <p><a href="/">Continue web simulator</a></p>`,
```

with:

```js
    noscript: `<h1>PackRip: TCG Card Packs — now on iPhone</h1>
      <p>Native iOS app with original-art trading-card pack opening, real haptic pack rip, foil reveals, nine rarity tiers, pity guarantees, free daily packs, and no account required. Web progress does not sync — the iPhone app keeps a separate save.</p>
      <p><a href="${IOS_APP_STORE_URL}">Get PackRip: TCG Card Packs on the App Store</a></p>
      <p><a href="https://elhanarinc.github.io/packrip-cards/" rel="noopener">Official iPhone app details &amp; support</a> — pull rates, privacy, terms and support for the iOS app.</p>
      <p><a href="/">Continue web simulator</a></p>`,
```

Two changes, both minimal: the hub link is added, and `five free daily packs` becomes `free daily packs` because the live App Store listing does not support that count. The three `/ios/*` campaign routes are left untouched — they are `noindex` variants and adding the link there would be the sitewide pattern spec §7.3 rules out.

- [ ] **Step 4: Bump the service-worker cache**

In `public/sw.js`, replace:

```js
const CACHE_NAME = 'packrip-shell-v123-2026-08-16-priceless-card-copy';
```

with:

```js
const CACHE_NAME = 'packrip-shell-v124-2026-08-20-ios-hub-backlink';
```

The repository's own rule is that every release bumps this, because a stale cache ships the wrong shell and asset list.

- [ ] **Step 5: Run the repository's required verification pass**

```bash
cd /Users/appsamurai/Desktop/personal-projects/pokemon-pack-opening
npx tsc -b && echo "tsc clean"
npm run audit:affiliate-ids
npm run lint 2>&1 | tail -5
npm run build:fast
```

Expected: `tsc clean`; the affiliate-ID audit reporting matching partner, campaign and ad IDs; lint with no new errors attributable to these three files; and the build printing its route count and sitemap URL count. Then confirm the sitemap has no undefined entries, which is the repo's explicit gate:

```bash
grep -c undefined dist/sitemap.xml
```

Expected: `0`.

- [ ] **Step 6: Assert the reverse link exists in the built output**

```bash
cd /Users/appsamurai/Desktop/personal-projects/pokemon-pack-opening
python3 - <<'PY'
import pathlib, re, sys
p = pathlib.Path("dist/ios/index.html")
if not p.exists():
    print("FAIL dist/ios/index.html was not built"); sys.exit(1)
raw = p.read_text()
hub = "https://elhanarinc.github.io/packrip-cards/"
anchors = re.findall(r'<a[^>]+href="' + re.escape(hub) + r'"[^>]*>(.*?)</a>', raw, re.DOTALL)
print("hub anchors in dist/ios/index.html:", len(anchors))
for a in anchors:
    print("  text:", re.sub(r"<[^>]+>", "", a).strip())
bad = 0
if not anchors:
    print("FAIL no crawlable anchor to the hub"); bad = 1
if "five free daily packs" in raw:
    print("FAIL stale 'five free daily packs' still in the built shell"); bad = 1
# The link must be plain markup, not gated behind an onclick-only handler.
if re.search(r'<a[^>]*href="' + re.escape(hub) + r'"[^>]*javascript:', raw):
    print("FAIL hub link is javascript-gated"); bad = 1
sys.exit(bad)
PY
grep -c 'elhanarinc.github.io/packrip-cards' dist/ios/index.html
```

Expected: at least one anchor whose text is `Official iPhone app details & support`, no stale pack-count string, and exit 0.

- [ ] **Step 7: Confirm nothing else in the web repo changed**

```bash
cd /Users/appsamurai/Desktop/personal-projects/pokemon-pack-opening
git status --porcelain | grep -v '^?? dist/' | sort
```

Expected exactly these three lines and nothing else:

```
 M public/sw.js
 M scripts/prerender.mjs
 M src/components/screens/IosLaunchScreen.tsx
```

If `src/config/iosLaunch.ts` appears, revert it — the `packrip-cards` App Store slug it contains is out of scope for this plan and is recorded as evidence only.

- [ ] **Step 8: Commit**

```bash
cd /Users/appsamurai/Desktop/personal-projects/pokemon-pack-opening
git add public/sw.js scripts/prerender.mjs src/components/screens/IosLaunchScreen.tsx
git commit -m "feat(ios): Link /ios to the official iPhone app hub

Adds a crawlable 'Official iPhone app details & support' link to the iOS
landing screen and its prerendered shell, pointing at
elhanarinc.github.io/packrip-cards/, and restates that the iPhone app
keeps a separate save. Drops the 'five free daily packs' claim the live
App Store listing does not support. Service-worker cache bumped per repo
rules. No gameplay, routing, attribution or design changes."
```

---

## Task 12: Full verification and the deployment checkpoint

Final gate across both repositories: visual review at three widths, keyboard and focus, reduced motion, broken-asset resilience, a last stale-copy sweep, and a stop.

**Files:**
- No source changes. If any check fails, fix it in the task that owns the file, then re-run this task from Step 1.

**Interfaces:**
- Consumes: everything from Tasks 1–11.
- Produces: `docs/superpowers/evidence/2026-08-20-packrip-hub-qa.md`, the QA record, and a checkpoint report to the user.

- [ ] **Step 1: Run every automated gate in one pass**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
echo "--- auditor (pages + corpus) ---"
python3 Scripts/audit-packrip.py; echo "exit=$?"
echo "--- JSON-LD, exactly as CI does it ---"
python3 - <<'PY'
import json, re, glob, sys
fail = 0
pat = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)
for f in sorted(glob.glob("**/*.html", recursive=True)):
    if "/.git/" in f:
        continue
    for i, m in enumerate(pat.finditer(open(f).read()), 1):
        try:
            json.loads(m.group(1).strip())
        except json.JSONDecodeError as e:
            print(f"::error file={f}::JSON-LD block #{i} invalid: {e}"); fail += 1
print(f"{fail} JSON-LD error(s)" if fail else "All JSON-LD blocks valid.")
sys.exit(1 if fail else 0)
PY
echo "--- sitemap ---"
python3 Scripts/regen-sitemap.py
```

Expected: `audit-packrip: clean` with `exit=0`, `All JSON-LD blocks valid.`, and `sitemap.xml unchanged (N URLs)` — unchanged, because Task 10 already regenerated it and nothing has been committed since.

- [ ] **Step 2: Start the local server the visual review runs against**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
python3 -m http.server 8765 >/dev/null 2>&1 &
echo $! > /tmp/packrip-qa-server.pid
sleep 1
for p in / /packrip-cards/ /packrip-cards/rarity.html /packrip-cards/support.html \
         /packrip-cards/privacy.html /packrip-cards/terms.html /404.html; do
  printf '%-42s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:8765$p")"
done
```

Expected: `200` on every line. Keep this server running through Step 8.

- [ ] **Step 3: Visual review at 320, 390 and desktop width**

Invoke the `claude-in-chrome` skill, then load the browser tools in one call:

```
ToolSearch: select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__resize_window,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__read_console_messages,mcp__claude-in-chrome__tabs_close_mcp
```

Call `tabs_context_mcp` first, then `tabs_create_mcp` on `http://localhost:8765/packrip-cards/`. For each of the three widths 320×760, 390×844 and 1440×900, call `resize_window`, then screenshot each of the five pages via `navigate` plus `computer` screenshot.

At every width, confirm each of these and write the result into the QA record:

- No horizontal page scroll. Check it mechanically rather than by eye, with `javascript_tool`: `document.documentElement.scrollWidth <= window.innerWidth + 1`.
- The era rail scrolls horizontally inside itself, and its own overflow does not push the page wide.
- The hero headline does not clip or overlap the hero figure.
- The truth ledger reads as four items at desktop, two at 390, one at 320.
- Every reading page's body text is at least 16 px.
- No label anywhere is below 12 px.
- The sticky header does not cover a section heading after following an in-page anchor.

Then check the tap targets mechanically:

```js
[...document.querySelectorAll('a,button,summary')].map(el => {
  const r = el.getBoundingClientRect();
  return { text: (el.textContent || '').trim().slice(0, 34), w: Math.round(r.width), h: Math.round(r.height) };
}).filter(x => x.h > 0 && (x.h < 44 || x.w < 24))
```

Expected: an empty array on every page at every width. Anything returned is a control below the 44 px floor and must be fixed in the task that owns the page.

- [ ] **Step 4: Keyboard, focus and landmark review**

With the 390×844 window on each of the five pages, use `javascript_tool` to walk the focus order and confirm the skip link comes first:

```js
const order = [...document.querySelectorAll('a[href],button,[tabindex]:not([tabindex="-1"])')]
  .map(el => (el.textContent || '').trim().slice(0, 30));
JSON.stringify({ first: order[0], count: order.length,
  landmarks: [...document.querySelectorAll('header,nav,main,footer')].map(e => e.tagName),
  h1: [...document.querySelectorAll('h1')].map(e => e.textContent.trim()) })
```

Expected on every page: `first` is `Skip to content`, `landmarks` starts with `HEADER` and contains `NAV`, `MAIN` and `FOOTER` in that order, and `h1` has exactly one entry.

Then confirm focus is actually visible: press Tab once with `computer`, screenshot, and verify the skip link has appeared at the top-left with a brass outline. Repeat for the first in-page link and the primary CTA.

- [ ] **Step 5: Reduced-motion review**

The site has exactly one animated element, so the check is that the kill switch covers it. With `javascript_tool` on the landing page:

```js
const sheet = [...document.styleSheets].find(s => (s.href || '').includes('_shared.css'));
const rm = [...sheet.cssRules].filter(r => r.conditionText && r.conditionText.includes('prefers-reduced-motion'));
const universal = rm.flatMap(r => [...r.cssRules]).find(r => r.selectorText && r.selectorText.includes('*'));
JSON.stringify({
  reducedMotionBlocks: rm.length,
  universalKill: universal ? universal.style.transition + ' / ' + universal.style.animation : null,
  transitionRules: [...sheet.cssRules].filter(r => r.style && r.style.transition).map(r => r.selectorText),
  matches: matchMedia('(prefers-reduced-motion: reduce)').matches
})
```

Expected: `reducedMotionBlocks` is 1, `universalKill` reports `none / none`, and every selector in `transitionRules` is one the universal rule overrides. Record `matches` as-is; if the host machine has reduce enabled, also screenshot the era rail under hover and confirm no lift.

- [ ] **Step 6: Broken-asset resilience**

On the landing page, break every image and confirm the layout holds because each one declares its box:

```js
document.querySelectorAll('img').forEach(i => { i.src = '/packrip-cards/images/__missing__.png'; });
JSON.stringify({
  imgs: document.querySelectorAll('img').length,
  withoutBox: [...document.querySelectorAll('img')].filter(i => !i.getAttribute('width') || !i.getAttribute('height')).length,
  scrollWidthOk: document.documentElement.scrollWidth <= window.innerWidth + 1
})
```

Expected: `withoutBox` is 0 and `scrollWidthOk` is true. Screenshot and confirm every section still communicates its point in text with no image rendering, then reload the page to restore it.

Also confirm the console is clean:

```
mcp__claude-in-chrome__read_console_messages with pattern "error|Error|failed"
```

Expected: nothing beyond the deliberate 404s from the broken-image test.

- [ ] **Step 7: Final stale-copy sweep across both repositories**

```bash
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
echo "--- hub + discovery surfaces ---"
grep -rniE 'mythos|mytholog|pantheon|deit(y|ies)|packrip-mythos|PackRip: Cards|five free daily packs|no ads|no analytics' \
  packrip-cards index.html 404.html README.md llms.txt llms-full.txt \
  || echo "clean"
echo "--- any remaining unattributed App Store link on the hub ---"
grep -rn 'apps.apple.com' packrip-cards | grep -v 'pt=127914124' || echo "clean"
echo "--- any remaining untagged packrip.co link on the hub ---"
grep -rn 'packrip\.co' packrip-cards --include='*.html' | grep -v 'utm_source=elhanarinc_github' || echo "clean"
echo "--- web repo built shell ---"
cd ../pokemon-pack-opening
grep -c 'elhanarinc.github.io/packrip-cards' dist/ios/index.html
```

Expected: `clean` for the first three checks. The third check tolerates plain-text mentions of `packrip.co` that are not anchors — read any hit and confirm it is prose, not an untagged `href`. The final count is at least `1`.

- [ ] **Step 8: Write the QA record and stop the server**

Create `docs/superpowers/evidence/2026-08-20-packrip-hub-qa.md` with these sections, each filled from the steps above: `## Automated gates`, `## Visual review — 320 / 390 / desktop`, `## Tap targets`, `## Keyboard, focus and landmarks`, `## Reduced motion`, `## Broken-asset resilience`, `## Stale-copy sweep`, `## Cross-repository link verification`, `## Not measured`.

Under `## Not measured`, list anything that could not be checked locally and why. Lighthouse and PageSpeed belong here unless they were actually run: the repository's CI gate is SEO ≥ 90 on the scheduled `pagespeed` job, and the workflow deliberately records a quota failure as unmeasured rather than a product failure. If you want a local number instead, run `npx --yes lighthouse http://localhost:8765/packrip-cards/ --only-categories=seo,accessibility --quiet --chrome-flags="--headless"` and record the two scores; if Lighthouse cannot be installed, write `UNMEASURED — CI pagespeed job will report after deployment`.

If Step 1 printed `sitemap.xml regenerated` rather than `unchanged`, something committed after Task 10 moved a page's date — include `sitemap.xml` in the commit below and say so in the QA record. If it printed `unchanged`, commit only the QA record.

```bash
kill "$(cat /tmp/packrip-qa-server.pid)" && rm /tmp/packrip-qa-server.pid
cd /Users/appsamurai/Desktop/personal-projects/elhanarinc.github.io
git add docs/superpowers/evidence/2026-08-20-packrip-hub-qa.md
git commit -m "docs(packrip): Record the iOS hub QA pass

Automated auditor, JSON-LD, sitemap, three-width visual review, tap
targets, focus order, reduced motion, broken-asset resilience and the
cross-repository link assertion."
```

- [ ] **Step 9: Deployment checkpoint — stop here**

Do not push and do not deploy. Report to the user:

- the commit list in `elhanarinc.github.io` (`git log --oneline -10`) and in `pokemon-pack-opening` (`git log --oneline -2`);
- both working trees clean (`git status --short` in each);
- the auditor result and the QA record path;
- that deploying the hub means pushing `elhanarinc.github.io` to `master`, after which GitHub Pages serves it and the CI `regen-sitemap` job may add its own sitemap commit;
- that deploying the reverse link means pushing `pokemon-pack-opening` to `master`, after which Cloudflare Pages builds and deploys automatically — and that this is a production deploy of the live web product;
- the one judgement call worth re-reading before shipping: `/packrip-cards/` is the App Store marketing, support and privacy URL, the live listing states that all card art is original to PackRip, and the frozen App Store screenshots are mythology-captioned, so the Pokémon-explicit hub is a deliberate accepted risk on Apple's review surface. The copy coherence rule in the Global Constraints keeps every individual sentence true, but the overall framing is the owner's call and it is now live-facing.

Wait for an explicit instruction before either push.

---

## Self-Review

Run against the spec after the plan is written, before execution.

**1. Spec coverage.**

- §0 locked decisions 1–10: name in Global Constraints; `/packrip-cards/` preserved and in Out of scope; all five pages in Tasks 4–8; Collector Archive in Task 3; Field Guide in Task 3 and Task 5; hub-as-official in Tasks 4 and 9; separate saves in Tasks 4, 6, 8, 9 and 11; reciprocal links in Tasks 4 and 11; screenshots frozen and reused in Task 4; no new backend or channel in Out of scope.
- §1 goals: all seven covered by Tasks 4, 9 and 11.
- §2 source priority and locked identity: Task 1 Steps 1–3 gather the evidence; Global Constraints fix the values; the "must NOT be published" list implements the volatile-number ban.
- §3.1 primary pages: Tasks 3–8. §3.2 discovery surfaces: Task 9 for root/404/README/llms files, Task 10 for sitemap and CI. §3.3 secondary scope: Task 11, with the footer and `iosLaunch.ts` explicitly excluded.
- §4.1 shared navigation: Task 4 header, reused in Tasks 5–8; privacy and terms in the footer only.
- §4.2 landing sequence 1–9: Task 4 Step 2, in the fixed order, with the QR deliberately omitted per §9.
- §4.3 pull rates: Task 5, including the prominent live-odds statement, the accessible prose ladder, foil as a finish, set-dependent eligibility, and pity without stale thresholds.
- §4.4 support: Task 6 covers every listed topic. Notifications and privacy are present as guidance sections; the FAQ schema mirrors only the nine question sections.
- §4.5 privacy: Task 7, with the analytics claim corrected from live evidence and the ad and affiliate surfaces disclosed.
- §4.6 terms: Task 8, covering every listed item.
- §5.1, §5.2, §5.3: Task 3, plus the accessibility floor in Global Constraints and the checks in Task 12 Steps 3–6.
- §6 asset strategy: Task 2, with byte-for-byte copies, no re-encoding, no hotlinking, and explicit dimensions.
- §7.1, §7.2, §7.3: the attribution contract in Global Constraints, enforced by the auditor, with the reverse link in Task 11.
- §8.1, §8.2, §8.3: metadata in Tasks 4–8; structured data as decided in Task 4 Step 2; corpus cleanup in Task 9 and the sweep in Task 12 Step 7.
- §9 failure behaviour: no JavaScript on the hub, explicit image boxes, QR omitted, `rel="noopener"`, reduced-motion kill switch, verified in Task 12 Steps 5–6.
- §10 verification contract, items 1–12: item 1 in Task 1 and Task 12 Step 7; 2 in Task 12 Step 1; 3 and 4 in the auditor; 5 in Task 11 Step 6; 6 in Task 10; 7 in Task 4 Step 5 and Task 12 Step 2; 8 in Task 12 Step 3; 9 in Task 12 Steps 4–5; 10 in Task 10 Step 4 and Task 12 Step 1; 11 in Task 12 Step 8, with quota failure recorded as unmeasured; 12 in Task 11 Step 5.
- §11 commit boundaries: the plan's twelve tasks are a finer split of the spec's nine, with privacy and terms separated, sitemap and CI separated, and QA separated.
- §12 acceptance criteria: each maps to a check in Task 12.

**Deliberate deviations from the spec, and why.**

- §8.2 permits `SoftwareApplication` alongside `MobileApplication`. Task 4 ships only `MobileApplication`, because the second node could only restate the same facts and would be a second surface to keep in sync — exactly the drift that produced the fabricated pity thresholds.
- §4.3 implies a rarity ladder that may carry odds. Task 5 publishes no numeric odds at all. Reason and evidence are stated in the task.
- §4.2.8 allows a QR code conditionally. It is omitted, which §9 explicitly prefers over a conflicting destination.
- §4.5 is silent on advertising. Task 7 adds a sponsored-content disclosure because the live theme config serves one and the retired page denied it.

**2. Placeholder scan.** No `TODO`, `TBD`, "similar to Task N", "add appropriate error handling", or "write suitable tests" appears. Every code step carries the literal content to write. Every conditional branch — the iTunes lookup failing, a pack asset having moved, PIL being unavailable, a `packrip.co` route not returning 200, `adConfig` having been switched off, `primaryGenreName` being `Entertainment`, `pyyaml` being absent — names the exact fallback text or value rather than deferring the decision.

**Fixes applied during self-review.** Two utility classes (`.vh`, `.tabular`) were declared in the class contract and defined in the stylesheet but used by no page; both were removed from the contract and the CSS, and the contract now says explicitly not to re-add an unused class. The `tag` class in Task 9's root-portfolio markup was confirmed to belong to the root page's own stylesheet rather than this contract, and is now annotated as such.

**3. Type and name consistency.** The auditor's module constants (`APP_STORE_BASE`, `PROVIDER_TOKEN`, `ALLOWED_CT`, `ALLOWED_UTM_CONTENT`, `UTM_FIXED`, `PAGES`, `LINK_CONTRACT_PAGES`, `CANONICAL_FOR`, `STALE_TERMS`, `FORBIDDEN_NUMERIC_CLAIMS`, `SYNC_CLAIMS`, `FORBIDDEN_JSONLD_KEYS`) are defined once in Task 1 and referenced by those exact names afterwards. The five `ct` tags and five `utm_content` values in Global Constraints are the same strings used in every page body and in `ALLOWED_CT` / `ALLOWED_UTM_CONTENT`. The CSS class list in Task 3's Interfaces is the complete set used by Tasks 4–8; no page introduces a class outside it. The seven era filenames and their seven dimension pairs are identical in Task 2 Step 2, Task 2 Step 3's `EXPECT` map, and Task 4's `img` attributes. `packrip-shell-v124-2026-08-20-ios-hub-backlink` appears once. The `ios_hub_link_clicked` event name appears once.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-20-packrip-ios-pokemon-hub.md`.

Twelve tasks, each ending in an independently reviewable commit, with a hard stop before any push or deploy.
