# elhanarinc.github.io

Owner's portfolio on GitHub Pages: plain static HTML, no Jekyll (`.nojekyll` at root; never add `_config.yml`). Live: <https://elhanarinc.github.io/>

## Sections
- `/` portfolio (`index.html`), `404.html`, `llms.txt` / `llms-full.txt`, `sitemap.xml`, `robots.txt`.
- `/packrip-cards/` PackRip: TCG Card Packs iOS hub (landing, `rarity.html`, privacy, terms, support, `_shared.css`). App Store Connect uses it as marketing, support and privacy URL: the path never moves or redirects.
- `/filmoire35/` Filmoire35 landing (single page).
- `.well-known/` `security.txt` (expires 2027-04-30, rotate yearly), `indexnow-key.txt`; IndexNow key file `867d24559d40c4325caab092169a98e0.txt` at root.

## Hard rules
- `app-ads.txt` stays at the root AND in `packrip-cards/` (AdMob verifies it via the App Store developer website; no web `ads.txt`).
- Hub follows the frozen PackRip design system; the iOS app is the source of truth (`../packrip-ios/CLAUDE.md`, `DesignTokens.swift`). Tokens live in `packrip-cards/_shared.css`: Inter body, Archivo 125% width headings, dark only, no serif, no new palettes or fonts.
- Hub links: every App Store link carries `pt=127914124`, a placement-specific `ct`, and `mt=8`; every web link targets `https://www.packrip.co/...` with the `packrip_ios_hub` UTM set. `Scripts/audit-packrip.py` enforces this plus product facts (runs in CI).
- `llms.txt` and `llms-full.txt` are hand-maintained: mirror any price, tier or OS-version change in the same commit.
- Commit format: `(build|ci|docs|feat|fix|perf|refactor|style|test)(scope): Capital first letter`, subject under 74 chars; `chore` is rejected by the pre-commit hook.
- New product: `<product>/` with `index.html`, `privacy.html`, `terms.html`, `support.html`, `images/app-icon.*`; add to root `index.html`, `llms.txt`, `llms-full.txt`; regen sitemap.

## Commands
```bash
python3 -m http.server 4000                      # preview at http://localhost:4000
python3 Scripts/regen-sitemap.py                 # run AFTER committing HTML (lastmod = last commit date; needs full history)
Scripts/indexnow-ping.sh <url> [<url>...]        # Bing/Yandex IndexNow push
python3 Scripts/audit-packrip.py                 # hub audit (CI)
python3 -I Scripts/test_homepage.py              # also test_audit_packrip.py, test_packrip_responsive_css.py
python3 Scripts/test_homepage_browser.py         # needs Playwright; serves the repo itself
```
`Scripts/og-cover.html` is the source for `og-cover.png` (render at 1200x630 via a local server plus headless Chrome).

## Deploy
Push to `master`; Pages serves the repo root. `.github/workflows/seo-checks.yml` regenerates `sitemap.xml`, validates HTML/JSON-LD, runs the hub audit, and runs PageSpeed daily (a PSI HTTP 429 is a quota issue, not a regression; only a real score below 90 fails; optional `PSI_API_KEY` secret).

License: site code (c) 2026 Arinc Elhan.
