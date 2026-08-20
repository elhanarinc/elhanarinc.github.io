# PackRip iOS hub — QA pass (2026-08-20)

Task 12 of the `2026-08-20-packrip-ios-pokemon-hub` plan. Measurement-only pass across both
repositories: automated gates, three-width visual review, tap targets, focus order, reduced
motion, broken-asset resilience, and the final stale-copy sweep. No source files were changed.

Screenshots: `.superpowers/sdd/2026-08-20-packrip-ios-pokemon-hub/qa-shots/` (17 files).

**Testing environment note.** The browser sandbox used for this pass enforces a real OS
window-width floor of 500px and a viewport-height ceiling of ~709px (screen 1512×982
logical px). Neither 320/390px-wide windows nor a full 900px-tall viewport were directly
achievable via plain window resize. All narrow-width and full-page work therefore ran
through a same-origin `<iframe>` harness on a blank host page: the iframe's own
`width`/`height` are set directly in CSS and are **not** subject to the outer window's
floor or ceiling, so `iframe.contentWindow.innerWidth` reports the exact requested value
(320, 390, 1440) and all DOM measurements (overflow, tap targets, font sizes, focus order,
landmarks) were taken at the exact nominal widths and heights (320×760, 390×844, 1440×709 —
709 is the closest achievable stand-in for 900; width drives every breakpoint in this
stylesheet, so the shortfall does not affect any check). Screenshot *capture* is still
bounded by the outer window's ~709px viewport ceiling (via `computer` zoom, which crops a
viewport-relative region): first-viewport shots are therefore ~700px tall rather than the
full nominal device height, and the two full-page stitches (see below) were assembled from
multiple 700px slices with Python/PIL, cropped to the iframe's exact pixel width using the
zoom tool's own reported scale factor.

## Automated gates

```
audit-packrip: clean          exit=0
All JSON-LD blocks valid.     0 errors
sitemap.xml unchanged (161 URLs)
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
| rarity | **343 / 320 — FAIL** | 390 / 390 — OK | 1440 / 1440 — OK |
| support | 320 / 320 — OK | 390 / 390 — OK | 1440 / 1440 — OK |
| privacy | 320 / 320 — OK | 390 / 390 — OK | 1440 / 1440 — OK |
| terms | 320 / 320 — OK | 390 / 390 — OK | 1440 / 1440 — OK |

**Finding — rarity.html overflows by 23px at 320.** Using the diagnostic query from the
brief, the elements whose right edge exceeds the viewport are:

- `<a>` "Support" in `nav.nav-links` — right edge at 324px (4px over)
- `<a>` "Web pull rates" in `nav.nav-links` — right edge at 475px (155px over)
- `<dd>` "Rolled per card, independently of rarity" in `div.odds-row` — right edge at
  343px (matches the page's overall `scrollWidth`)

This reproduces only at 320px; both 390 and 1440 are clean on the same page. Route to
whichever task owns `packrip-cards/rarity.html` / `_shared.css`'s nav and `.odds-row`
rules.

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
| 390 | `362px` | 1 |
| 1440 | `270px 270px 270px 270px` | 4 |

**Finding — the ledger is 1-column at 390, not the 2-column layout the brief's Step 3
describes ("four items at desktop, two at 390, one at 320").** `_shared.css` has two rules:
`@media (max-width: 900px) { .ledger { grid-template-columns: 1fr 1fr; } }` (2 columns) and
a later `@media (max-width: 520px) { .ledger { grid-template-columns: 1fr; } }` (1 column).
Both match at 390px, and the later rule wins by source order, so 390 renders identically to
320 (1 column), not as 2. The 2-column layout only exists in the 521–900px band. This is a
measured discrepancy between the plan's stated expectation and the shipped CSS — not a
visual judgement call — and is worth a decision from whoever owns `_shared.css`'s
responsive block: either the breakpoint should move so 390 gets 2 columns, or the plan's
description was simply imprecise about where the 2-column band starts.

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
| 320 | 115px | 88px | **FAIL — 27px overlap** |
| 390 | 115px | 88px | **FAIL — 27px overlap** |
| 1440 | 65px | 88px | OK |

**Finding — the sticky header overlaps the jumped-to heading at 320 and 390.**
`_shared.css` sets a fixed `scroll-margin-top: 88px` on headings (line 475), which matches
the header's single-row desktop height. `.site-head .wrap` has `flex-wrap: wrap`, so at
320/390 the brand and nav links wrap to two rows and the sticky header grows to ~115px —
27px taller than the scroll-margin compensates for. Every section heading behind the sticky
header on every reading page is affected at these two widths. Route to whichever task owns
`_shared.css`'s header/anchor rules.

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
at 320×760: `iframe.contentWindow.focus()` → one `Tab` keypress →
`iframe.contentDocument.activeElement` reported `{tag: "A", class: "skip", text: "Skip to
content"}`. Screenshot (`index-320-tabbed.png`) confirms the brass-outlined skip link
rendered top-left. Repeating the sticky-header check above (jumping the first in-page link
and to the primary CTA) confirmed those controls receive real, visible focus in the same
way.

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
breaking the images (nothing beyond the browser's default silent handling of `<img>` 404s,
which does not log to console at all), and once broadly across the whole session (386
messages captured in total, every one of them a `MaxListenersExceededWarning` /
`ObjectMultiplex` warning from a locally-installed MetaMask browser extension
(`chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/...`), unrelated to any hub page).

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

Everything the brief asked for was measured, with two environment-driven caveats already
called out above: the outer browser window's 500px width floor and ~709px height ceiling
meant narrow-width and full-page testing ran through a same-origin iframe harness rather
than a literally-resized OS window, and 13 of the 15 per-page screenshots show
~700px-tall first viewports rather than the full nominal device height (320×760, 390×844,
1440×900) — only `index-320.png` and `index-390.png` were assembled as full-page stitches,
per the brief's own "capture the full page where the tool allows it" framing and its
stated reason (era rail + truth ledger below the fold on the *index* page specifically).

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
