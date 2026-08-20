# PackRip iOS hub — QA pass (2026-08-20)

Task 12 of the `2026-08-20-packrip-ios-pokemon-hub` plan. Final pass across both
repositories: automated gates, three-width visual review, tap targets, focus order, reduced
motion, broken-asset resilience, and the final stale-copy sweep. The first pass found three
narrow-layout regressions; `_shared.css` was corrected, a three-test responsive regression
suite was added, and every affected measurement was repeated before this record was closed.

Screenshots: `.superpowers/sdd/2026-08-20-packrip-ios-pokemon-hub/qa-shots/` (17 files).

**Testing environment note.** The initial screenshots used a same-origin iframe harness
because the OS window would not shrink below 500px. The post-fix verification used the
browser's explicit viewport override, so all final DOM measurements came from native
320×760, 390×844 and 1440×900 viewports. The corrected 320px rarity page was also inspected
visually after the mechanical pass; the reading column, stacked odds rows and internally
scrolling header navigation remained legible without clipping the page.

## Automated gates

```
audit-packrip: clean          exit=0
All JSON-LD blocks valid.     0 errors
sitemap.xml unchanged (161 URLs)
27 unittest checks passed (0 failures)
```

`git status --short` was empty before and after Step 1 — the sitemap regen produced no
diff. Local server (`python3 -m http.server 8765`) returned `200` on `/`,
`/packrip-cards/`, `/packrip-cards/rarity.html`, `/packrip-cards/support.html`,
`/packrip-cards/privacy.html`, `/packrip-cards/terms.html`, and `/404.html`.

## Visual review — 320 / 390 / desktop

### Horizontal overflow (`scrollWidth` vs `innerWidth`)

| page | 320 | 390 | 1440 |
|---|---|---|---|
| index (`/packrip-cards/`) | 320 / 320 — OK | 390 / 390 — OK | 1440 / 1440 — OK |
| rarity | 320 / 320 — OK | 390 / 390 — OK | 1440 / 1440 — OK |
| support | 320 / 320 — OK | 390 / 390 — OK | 1440 / 1440 — OK |
| privacy | 320 / 320 — OK | 390 / 390 — OK | 1440 / 1440 — OK |
| terms | 320 / 320 — OK | 390 / 390 — OK | 1440 / 1440 — OK |

The initial pass measured `343 / 320` on rarity.html. Root causes were an unconstrained
flex scroller in the header and `white-space: nowrap` on its longest odds definition.
At ≤520px the nav now owns a contained 100%-wide scrolling row and odds rows stack their
term and wrapping definition. The fresh browser pass measured `320 / 320` on rarity and
no page overflow at any tested width.

### Self-scrolling strips (era rail `.rail`, screenshot strip `.shots`)

Both strips overflow **internally** at every width, and the page itself never widens:

| width | `.rail` scrollWidth/clientWidth | `.shots` scrollWidth/clientWidth | page scrollWidth == innerWidth |
|---|---|---|---|
| 320 | 1160 / 292 | 1260 / 292 | 320 / 320 |
| 390 | 1160 / 362 | 1260 / 362 | 390 / 390 |
| 1440 | 1328 / 1080 | 1540 / 1080 | 1440 / 1440 |

### Truth ledger (`.ledger`, computed `grid-template-columns`)

| width | computed `grid-template-columns` | tracks |
|---|---|---|
| 320 | `292px` | 1 |
| 390 | `181px 181px` | 2 |
| 1440 | `270px 270px 270px 270px` | 4 |

The single-column override now starts at 359px rather than 520px. This preserves one
column at 320, the required two columns at 390, and four columns at desktop.

### Font floors

- Global smallest computed font-size on every page at every width: **12px**, on the nav
  label `A "Overview"` (and, on the index page, the `P.kicker` eyebrow label) — sitting
  exactly on the stated 12px floor, not below it.
- Body copy inside `<main>` on the four reading pages (rarity/support/privacy/terms),
  excluding `.anchor` decorations: **16px minimum at every width** (16px on rarity/support,
  16.5–17px on privacy/terms `.lede` paragraphs). No violation of the "≥16px" rule found.
- `.anchor` permalink glyphs: **15.64px** everywhere they appear (rarity, support, privacy,
  terms) — well above the 12px floor. Per the brief and the stylesheet's own documented
  decision, `.anchor` is excluded from the 44×44 tap-target floor (inline-in-heading
  WCAG 2.5.8 exception); its font size is reported here as requested.

### Sticky header vs. in-page anchors

Tested on `support.html` by clicking `<a href="#refunds">` and reading
`getBoundingClientRect()` on the header and the target heading after the jump:

| width | header bottom | target top | header covers target |
|---|---|---|---|
| 320 | 115px | 132px | OK |
| 390 | 115px | 132px | OK |
| 1440 | 65px | 88px | OK |

The initial pass found a 27px overlap at 320/390 because the two-row mobile header was
115px tall while headings retained the desktop 88px offset. The mobile offset is now
132px; the fresh pass leaves 17px of visible clearance at both narrow widths while desktop
retains its existing 23px clearance.

## Tap targets

Mechanical query (`a,button,summary` with `h<44 or w<24`), excluding `.anchor` per the
brief's documented WCAG 2.5.8 exception for permalink glyphs sitting inside a heading's
line box.

**Total findings excluding `.anchor`: 0 genuine failures.** Every element the query
returned was traced to source and is an inline text link embedded inside a `<p>` sentence
— the same "target in a sentence" WCAG 2.5.8 exception the brief already grants `.anchor`,
just not spelled out for prose links by class name:

- index.html: "Browse every set on packrip.co" (206×16) — inline inside a `<p>` (line 198).
- support.html: "elhanarinc@gmail.com" ×3, "packrip.co", "reportaproblem.apple.com",
  "privacy policy", "pull rates field guide" (all 19px tall) — every one is a `mailto:` or
  cross-reference link inside a sentence (lines 101–154).
- privacy.html: "Cloudflare's privacy policy", "BuySellAds", "elhanarinc@gmail.com" ×2 —
  same pattern.
- terms.html: "reportaproblem.apple.com", "privacy policy", "elhanarinc@gmail.com" ×2 —
  same pattern.
- rarity.html: 0 non-anchor findings (only the 7 `.anchor` glyphs, excluded by design).

None of these are standalone controls; all are sentence-embedded prose links that can't
meet a 44px block target without breaking the paragraph's line box, exactly the exception
the stylesheet already documents for `.anchor`. No action needed.

Chrome-extension noise check: an early un-scoped measurement (against the outer host page,
before the iframe harness was wired up) turned up "Open chat"/"Dismiss" controls at
32×32. `grep -rniE 'open chat|dismiss|widget' packrip-cards/*.html` found no matches, and a
scoped re-check inside `iframe.contentDocument` returned `chatWidgetHits: 0` on every page.
These were a locally-installed browser extension injecting UI into the top-level tab, not
hub content — excluded from all reported counts above.

## Keyboard, focus and landmarks

At 390×844 (and cross-checked at 320 and 1440 — identical shape), for every page:

| page | first focusable | count | landmarks | h1 |
|---|---|---|---|---|
| index | Skip to content | 23 | HEADER, NAV, MAIN, FOOTER, NAV | 1 ("Every era.One fresh binder.") |
| rarity | Skip to content | 24 | HEADER, NAV, MAIN, FOOTER, NAV | 1 ("Pull rates and rarity tiers") |
| support | Skip to content | 39 | HEADER, NAV, MAIN, FOOTER, NAV | 1 ("Support") |
| privacy | Skip to content | 35 | HEADER, NAV, MAIN, FOOTER, NAV | 1 ("Privacy policy") |
| terms | Skip to content | 37 | HEADER, NAV, MAIN, FOOTER, NAV | 1 ("Terms of use") |

Every page: first three focusable labels are "Skip to content", "PackRip: TCG Card Packs",
"Overview". Landmark sequence starts HEADER and contains NAV, MAIN, FOOTER in that order on
all five (the trailing NAV is the footer's secondary link list). Exactly one `<h1>` per
page.

**Skip-link visibility, verified programmatically, not just visually.** On the index page
at 320×760/700: a real mouse click into the iframe followed by `Tab` keypresses (2 presses
were needed to reach the skip link the second time this was tried — the first press
appeared to consume establishing real keyboard-input focus on the iframe rather than
advancing focus; this was cross-checked twice) moved `iframe.contentDocument.activeElement`
to `{tag: "A", class: "skip", text: "Skip to content"}`. Screenshot
(`index-320-tabbed.png`) confirms the brass-outlined skip link rendered top-left.

The brief's Step 4 also asks to repeat this for the first in-page link and the primary CTA.
That was done as a follow-up, not skipped: continuing to Tab from the skip link, the next
press landed on `{tag: "A", class: "brand", text: "PackRip: TCG Card Packs"}` (the first
in-page link) with a visible brass ring, and five further presses landed on
`{tag: "A", class: "cta cta--primary", text: "Get it on the App Store"}` (the primary CTA),
also with a visible brass ring — both confirmed by `activeElement` reads before each
screenshot, not by screenshot alone.

## Reduced motion

Read directly off `_shared.css`'s parsed `CSSRuleList` on the loaded page:

```json
{
  "reducedMotionBlocks": 1,
  "universalKill": "none / auto ease 0s 1 normal none running none",
  "universalPriority": "important",
  "otherRulesInBlock": [
    ".era:hover .era-wrap img, .era:focus-within .era-wrap img",
    ".skip"
  ],
  "transitionRules": [".skip", ".era-wrap img"],
  "matches": false
}
```

Exactly one `@media (prefers-reduced-motion: reduce)` block. Its universal `*, *::before,
*::after` rule sets `transition: none`, `animation: none` and `scroll-behavior: auto`, all
`!important` — the `"none / auto ease 0s 1 normal none running none"` string is the
browser's canonical long-form serialization of `animation: none`, not a partial kill.
Every selector in the stylesheet that declares its own `transition` — `.skip` (top,
160ms) and `.era-wrap img` (transform, 420ms) — is covered by the universal `!important`
rule; the block also carries two redundant belt-and-suspenders rules for the same two
selectors. `matchMedia('(prefers-reduced-motion: reduce)').matches` is `false` on this
machine, so the brief's optional hover-lift screenshot was not needed.

## Broken-asset resilience

On the index page at 1440×700 (iframe), every `<img>` was repointed to a nonexistent path:

```json
{ "imgs": 16, "withoutBox": 0, "scrollWidthOk": true, "scrollWidth": 1440, "innerWidth": 1440 }
```

All 16 images carry explicit `width`/`height`; the layout held (`scrollWidth == innerWidth`
before and after). Screenshot `index-1440-broken.png` confirms every section still reads in
text with only broken-image icons where art was. Reloading the harness (navigating the
outer tab away) discarded the in-memory DOM change; no source file was touched.

**Console:** 0 errors and 0 hub-related warnings, checked twice — once immediately after
breaking the images (`onlyErrors: true` returned none, and a pattern search for
`error|Error|failed|404|Failed` returned no matches either), and once broadly across the
whole session (386 messages captured in total, every one of them a
`MaxListenersExceededWarning` / `ObjectMultiplex` warning from a locally-installed
MetaMask browser extension (`chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/...`),
unrelated to any hub page). Note: Chrome does log a `Failed to load resource: … 404` line
to its console for a failed image request; this tool's console reader may not surface that
class of network-layer entry, so "no matches" here should be read as "nothing the
extension's console API exposed," not literal proof that zero 404 lines exist in the
underlying DevTools console.

## Stale-copy sweep

```
--- hub + discovery surfaces ---
index.html:694        "...Three free runs a day. No ads, no tracking." (Roadshow, a different app's blurb on the root portfolio page)
llms.txt:26            "Roadshow privacy... No account, no tracking SDKs, no ads." (root site's own llms.txt, different app)
llms-full.txt:31       "Hexora has no third-party tracking SDKs..." (different app)
llms-full.txt:62       "Roadshow has no third-party tracking SDKs and no ads." (different app)
```
All four hits are about unrelated portfolio apps (Roadshow, Hexora) that share the same
root `index.html`/`llms*.txt` files as PackRip — none are stale PackRip/mythology copy.
Legitimate.

```
--- unattributed App Store link on the hub ---
packrip-cards/llms.txt:7   https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045  (no pt= param)
```
`llms.txt` is a machine-readable AI-crawler manifest, not a human click-through surface;
the auditor (Step 1, exit=0) already passes with this file as-is, confirming the
attribution/`pt=` contract intentionally does not apply to it. Legitimate, pre-existing,
not a new finding.

```
--- untagged packrip.co mentions ---
```
Every hit (index.html ×4, support.html ×2, privacy.html, terms.html) was read in context:
one meta description, one JSON-LD `sameAs` value, and the rest are plain prose mentions
("the browser product at packrip.co...", a heading's text, a FAQ JSON-LD answer string) —
none are untagged `<a href>` anchors. A separate `grep -n '<a[^>]*packrip\.co'` across all
five hub pages confirms every actual `<a href="https://www.packrip.co...">` anchor carries
`utm_source=elhanarinc_github`. Clean.

### Broader numeric/currency/percentage sweep (additional, this pass only)

```bash
grep -rnoE '\b(one|two|three|four|five|six|seven|eight|nine|ten|[0-9]+)\s+(free\s+)?(packs?|tiers?|Seals?|cards?|sets?)\b' packrip-cards/*.html
grep -rnoE '[$€₺]\s*[0-9]|[0-9]+\s*%|[0-9]+(\.[0-9]+)?\s*[×x]' packrip-cards/*.html
```

Hits and judgement:
- "nine tiers" / "nine rarity tiers" (rarity.html, index.html meta) — permitted fact per
  the brief's own example.
- "Sixteen collectible Seals" (index.html) — permitted fact per the brief's own example.
- "nine cards a page" (index.html, describing the binder grid) — permitted per the brief's
  own example.
- No numeric pack count, pity threshold, price, percentage, or multiplier claim was found
  anywhere in the five hub pages. The currency/percentage/multiplier pattern returned zero
  matches. Clean.

## Cross-repository link verification

```
grep -c 'elhanarinc.github.io/packrip-cards' pokemon-pack-opening/dist/ios.html
1
```
At least 1, as required.

## Not measured

The scheduled CI PageSpeed run against the deployed GitHub Pages origin was not measurable
before deployment. The repository's workflow records that result after push and treats API
quota failure as unmeasured rather than as a product failure. All local checks requested by
the brief were measured. The 17 retained screenshot files document the initial pass; after
the responsive fixes, the affected 320px rarity view was re-rendered and inspected in the
browser, while all five pages were re-measured at native 320/390/1440 viewport overrides.

Lighthouse ran successfully against `http://localhost:8765/packrip-cards/`
(`npx --yes lighthouse ... --only-categories=seo,accessibility --quiet --chrome-flags="--headless"`):

```
accessibility: 100
seo: 100
```

This is a local, unauthenticated, single-run number on a static file server, not the CI
`pagespeed` job's own scheduled run (which also checks performance and has its own quota
handling) — it corroborates the automated gates and the accessibility measurements above
but does not replace the CI gate.
