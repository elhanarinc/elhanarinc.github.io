# PackRip iOS Pokémon Hub Design

**Date:** 2026-08-20  
**Status:** Approved in conversation  
**Primary repository:** `elhanarinc.github.io`  
**Secondary repository:** `../pokemon-pack-opening` (backlink-only scope)

## 0. Locked Decisions

The following decisions are approved and must not be reopened during implementation:

1. The product is presented everywhere as **PackRip: TCG Card Packs**, matching the live App Store listing.
2. The `/packrip-cards/` path stays in place. It already serves as the App Store Developer Website and Privacy Policy path, and GitHub Pages cannot provide a clean server-side 301 migration.
3. All five PackRip pages are converted end to end: landing, pull rates, support, privacy, and terms.
4. The approved visual direction is **Collector Archive**: deep navy, gold, premium collector typography, era-based set storytelling, and restrained foil effects.
5. Information-heavy pages use a lighter **Field Guide** expression of the same system without becoming a separate theme.
6. `elhanarinc.github.io/packrip-cards/` becomes the official iOS product, legal, and support hub.
7. `packrip.co` remains the playable browser product. The two products share the PackRip brand and Pokémon TCG pack-opening context but use separate saves.
8. Both sites link to each other contextually. The GitHub Pages redesign is broad; changes in `pokemon-pack-opening` are deliberately narrow and limited to the official iOS-hub backlink and factual alignment.
9. Existing App Store screenshots are frozen and are not redesigned. The site may reuse the current screenshots and repository-owned pack/set assets.
10. No new backend, account system, newsletter, paid acquisition, social channel, or web/iOS save synchronization is introduced.

## 1. Goal

Replace the obsolete Mythos-facing PackRip microsite with an authoritative, conversion-focused Pokémon TCG iPhone product hub that:

- immediately identifies PackRip as the iOS companion to `packrip.co`;
- accurately reflects the live App Store product and current features;
- sends qualified users to the App Store with measurable campaign attribution;
- sends browser-preferring users to relevant PackRip web experiences;
- gives `packrip.co` a clear official-details backlink to the iOS hub;
- removes contradictory Mythos-era copy from every discoverable surface;
- keeps the legal and support URLs already registered with Apple stable.

## 2. Product Truth and Source Priority

When facts conflict, implementation uses this priority order:

1. Live App Store listing for public product name, subtitle, platform, minimum OS, current IAP names/prices, and public description.
2. Current `packrip-ios` code/config and shipped release notes for feature behavior, cloud-save details, pull mechanics, and current theme behavior.
3. Current `pokemon-pack-opening` source for web-product behavior, cross-promo URLs, campaign tokens, and web/iOS separation language.
4. Existing GitHub Pages copy only when it agrees with all higher-priority evidence.

Locked identity facts:

- Public name: `PackRip: TCG Card Packs`
- App Store ID: `6763404045`
- Canonical App Store URL: `https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045`
- Provider token: `127914124`
- Platform: iPhone
- Minimum OS: iOS 17.0
- Language: English
- Web product: `https://packrip.co`
- Web and iOS progress do not synchronize.
- The in-app pre-purchase pull-rate view is authoritative for live odds.

Live ratings, rating counts, catalog/set counts, release version, and other fast-changing numbers must not be hardcoded into marketing copy or structured data.

## 3. Scope

### 3.1 Primary-site pages

The following pages are redesigned and rewritten:

- `packrip-cards/index.html`
- `packrip-cards/rarity.html`
- `packrip-cards/support.html`
- `packrip-cards/privacy.html`
- `packrip-cards/terms.html`
- `packrip-cards/_shared.css`
- PackRip-owned images under `packrip-cards/images/`

### 3.2 Primary-site discovery surfaces

The following files are reconciled with the new identity:

- root `index.html`
- root `404.html`
- root `README.md`
- root `llms.txt`
- root `llms-full.txt`
- `packrip-cards/llms.txt`
- `sitemap.xml` through `Scripts/regen-sitemap.py`
- `.github/workflows/seo-checks.yml` when the new validation commands need CI wiring

### 3.3 Secondary-site backlink scope

The `pokemon-pack-opening` repository receives only the smallest changes needed to establish and verify the reverse link:

- add an “Official iPhone app details & support” link to the appropriate `/ios`, footer, and/or about/contact product surfaces;
- point it to `https://elhanarinc.github.io/packrip-cards/`;
- preserve the existing direct App Store conversion CTAs and `pt=127914124` attribution system;
- state that the web and iOS saves are separate wherever the link’s context could imply synchronization;
- avoid unrelated design, gameplay, SEO-route, backend, or monetization changes.

## 4. Information Architecture

### 4.1 Shared navigation

Every PackRip page uses one compact header:

- Brand: `PackRip: TCG Card Packs`
- Product home: `/packrip-cards/`
- Pull Rates: `/packrip-cards/rarity.html`
- Support: `/packrip-cards/support.html`
- Browser CTA: `https://packrip.co` with contextual UTM parameters
- Primary CTA: attributed App Store URL

Privacy and Terms remain discoverable in the footer rather than competing in the primary navigation.

### 4.2 Landing sequence

The landing page follows this fixed order:

1. **Hero:** “Every era. One fresh binder.”, immediate Pokémon TCG/iPhone identification, primary App Store CTA, secondary “Play free on packrip.co” CTA, app icon/current iPhone visual.
2. **Truth strip:** every set unlocked, nine rarity tiers, daily free packs, no account/anonymous cloud save. Claims must be revalidated at implementation time.
3. **Era archive:** visual set families from WotC classics through current eras using repository-owned assets.
4. **Native ritual:** swipe-to-rip, card-by-card reveals, haptics, sound, foil motion, binder, and share flow.
5. **Collector systems:** Forge, wishlist/Hunt Packs, pity, completion, quests, Seals, trainer identity, and daily leaderboard. Copy distinguishes current capabilities from historical release notes.
6. **Web/iOS bridge:** a direct comparison framed as preference, not competition. Browser is immediate and free; iOS is native and tactile; saves are separate.
7. **Transparent odds:** link to Pull Rates and explain that live in-app odds shown before a purchase are authoritative.
8. **Final conversion block:** App Store CTA plus QR only if the current QR resolves to the attributed canonical URL.
9. **Footer:** browser product, support, pull rates, privacy, terms, portfolio, contact, and fan-made/original-art disclosure.

### 4.3 Pull Rates

The page becomes a collector field guide rather than a static Mythos ladder:

- explain the nine iOS rarity tiers using the current public App Store terminology;
- explain foil variants as an independent finish;
- explain pity guarantees without promising stale numeric thresholds;
- explain that eligible rarities depend on the selected set;
- explain Hunt Packs and any probability modifier only if current shipped behavior confirms it;
- place a prominent “Check live odds in app before opening” statement;
- retain an accessible prose version of any visual rarity ladder;
- link to the App Store and back to relevant web set/card exploration.

### 4.4 Support

Support answers current user problems, not launch-era Mythos questions:

- getting started and supported devices;
- web versus iOS and separate saves;
- anonymous device UUID/cloud save behavior;
- restore purchases and manage/cancel PackRip Plus;
- missing collection/content-loading recovery;
- pull rates, pity eligibility, foil variants, Forge, Hunt Packs, and daily challenge;
- refund path through Apple;
- notification controls;
- contact through `elhanarinc@gmail.com` unless live product evidence shows a newer address.

Only questions with visible answers are duplicated into `FAQPage` JSON-LD.

### 4.5 Privacy

Privacy copy is reconciled against the live App Store privacy disclosure and current implementation:

- anonymous identifiers and device UUID;
- purchase history and RevenueCat;
- Cloudflare Worker/D1/KV processing;
- cloud-save data and conflict handling at a user-readable level;
- analytics behavior based on current code, with no obsolete “no analytics” claim unless proven;
- retention/deletion/contact instructions grounded in actual backend capability;
- no account, email login, or payment-card collection claim;
- external processor links checked at implementation time.

### 4.6 Terms

Terms are updated without turning the page into marketing copy:

- current product name and fan-made collectible-card simulator framing;
- virtual packs only; no physical goods or cash-out;
- current coin consumables and PackRip Plus subscription;
- Apple billing, cancellation, and refund mechanics;
- original PackRip art/fan-made Pokémon-context disclosure consistent with the live listing;
- live odds are shown in the app before purchase;
- Apple Standard EULA link;
- governing-law and warranty text preserved unless contradictory.

## 5. Visual System

### 5.1 Collector Archive

The approved direction uses:

- deep navy/ink backgrounds derived from the current PackRip iOS/web palette;
- warm gold as the primary conversion and rarity accent;
- restrained blue, red, green, and violet era accents;
- a premium editorial serif for hero/display text paired with a highly legible sans serif for UI and legal copy;
- card, binder, archive-label, and foil-light motifs;
- generous negative space and one dominant action per viewport;
- motion that supports the pack/card material rather than generic neon-gacha spectacle.

The design must not imitate the Pokémon logo, official card frame, Poké Ball trade dress, or official site chrome. Pokémon context comes from truthful copy and product-owned/repository-owned gameplay assets.

### 5.2 Field Guide variant

Pull Rates, Support, Privacy, and Terms reuse the same tokens and header/footer but use:

- narrower reading width;
- higher text contrast;
- clear section anchors;
- compact callout cards;
- restrained decorative imagery;
- accessible lists instead of dense tables on narrow screens.

### 5.3 Responsive and accessible behavior

- Fully usable at 320 CSS px width.
- Primary controls are at least 44×44 CSS px.
- Body copy is at least 16 CSS px on reading pages and never below 12 CSS px for ancillary labels.
- Visible keyboard focus is required.
- Skip link and semantic landmarks are required.
- Decorative images use empty alt; informational images use specific alt.
- Content remains readable with images, CSS, or JavaScript unavailable.
- `prefers-reduced-motion: reduce` removes nonessential transforms, shimmer, parallax, and auto-animation.
- Color is never the only carrier of rarity or state.

## 6. Asset Strategy

Assets are selected in this order:

1. Current iOS App Store screenshots already stored in `packrip-cards/images/screens/`.
2. Current PackRip app icon.
3. Repository-owned pack/set assets from `pokemon-pack-opening/public/images/`.
4. Repository-owned iOS assets when they are already approved for public display.

Rules:

- Do not hotlink Pokémon TCG APIs, CDN scans, or third-party sites from GitHub Pages.
- Copy selected assets into `packrip-cards/images/` with descriptive, stable names.
- Do not edit generated output in `pokemon-pack-opening/dist/`.
- Produce WebP/AVIF variants only when browser fallbacks and repository tooling are clear; otherwise use optimized PNG/JPEG and explicit dimensions.
- Every above-the-fold image has width/height to prevent layout shift.
- The hero does not require a newly generated AI image.
- Existing App Store screenshots remain unchanged.

## 7. Cross-Site Linking and Attribution

### 7.1 GitHub Pages to App Store

All commercial App Store links use:

`https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?pt=127914124&ct=packrip_ios_github&mt=8`

If multiple GitHub Pages placements need separate attribution, use deterministic suffixes such as:

- `packrip_ios_github_hero`
- `packrip_ios_github_footer`
- `packrip_ios_github_support`
- `packrip_ios_github_rates`

Use placement-specific campaign tags. The surface has few links, and the added diagnostic value outweighs the small maintenance cost.

### 7.2 GitHub Pages to web

Contextual web links use HTTPS and UTM attribution:

- `utm_source=elhanarinc_github`
- `utm_medium=referral`
- `utm_campaign=packrip_ios_hub`
- `utm_content=<placement>`

Examples of `<placement>` are `hero_play_web`, `era_archive`, `rates_explore`, and `footer_web`.

### 7.3 Web to GitHub Pages

The reverse link uses plain crawlable `<a>` markup and descriptive text such as “Official iPhone app details & support.” It must not be hidden behind client-only interaction. The existing direct App Store links remain primary conversion actions.

No reciprocal-link sitewide spam pattern is introduced. Links appear only where they help a user understand or choose between the two PackRip products.

## 8. SEO and Machine-Readable Identity

### 8.1 Metadata

Every PackRip page receives unique:

- `<title>`;
- meta description;
- canonical URL;
- Open Graph title, description, type, URL, and image;
- Twitter card metadata;
- robots directive appropriate to the page;
- favicon/apple-touch icon;
- Smart App Banner with App Store ID `6763404045`.

### 8.2 Structured data

- Landing: `MobileApplication` plus `SoftwareApplication` only when both describe the same entity without contradictory duplicated facts.
- Support: `FAQPage` matching visible content exactly.
- Pull Rates: `Article` with accurate author/publisher/dateModified fields.
- Root portfolio: update `ItemList` and product card name/description.

Do not hardcode `aggregateRating`, current version, rating count, or volatile set count.

### 8.3 Corpus cleanup

The implementation includes repository-wide scans for stale terms and facts, including:

- `Mythos`, `mythology`, `pantheon`, and old fictional set names in PackRip surfaces;
- `PackRip: Cards` where it is not a historical quotation;
- retired App Store slug `packrip-mythos`;
- old App Store copy such as “five free daily packs” if current product evidence differs;
- obsolete “no analytics,” “no ads,” or platform statements;
- stale prices or Plus benefits;
- claims that imply the browser and iOS collection synchronize.

Historical changelog text in the separate web repository is not mass-rewritten unless it appears in a current marketing/discovery surface.

## 9. Failure Behavior

The site is static and must degrade cleanly:

- App Store links remain normal anchors and do not depend on JavaScript.
- If an image fails, explicit dimensions preserve layout and adjacent copy still communicates the feature.
- If decorative motion is unsupported or disabled, the design remains complete.
- If a QR code is stale or cannot be regenerated from the final attributed URL, omit it rather than ship a conflicting destination.
- External links open predictably, use `rel="noopener"` when opening a new tab, and do not force new tabs for internal/legal navigation.
- No runtime dependency on `packrip.co`, App Store APIs, Pokémon APIs, analytics APIs, or a build service is added.

## 10. Verification Contract

The implementation plan must include exact commands and expected results for:

1. Repository-wide stale-copy scans.
2. HTML/JSON-LD parsing for every changed page.
3. Internal-link and local-asset existence checks.
4. Canonical, OG URL, Smart App Banner, App Store ID, provider token, and campaign-tag assertions.
5. Validation that the reverse link exists in the built/prerendered `pokemon-pack-opening` output.
6. `python3 Scripts/regen-sitemap.py` after the HTML commit so Git-derived `<lastmod>` values are correct.
7. Local HTTP smoke tests rather than `file://` inspection.
8. Desktop and 320/390 px mobile visual review for all five pages.
9. Keyboard navigation, focus visibility, landmark order, alternative text, and reduced-motion review.
10. Existing GitHub Actions JSON-LD validation.
11. Lighthouse or PageSpeed checks with SEO ≥90; external PSI quota failure is recorded as unmeasured, not treated as a product failure.
12. In `pokemon-pack-opening`: TypeScript build, Vite build, prerender, link assertion, affiliate-ID audit, and service-worker cache bump if shipped source changes require it under repo rules.

## 11. Delivery and Commit Boundaries

Implementation is split into independently reviewable changes:

1. Evidence snapshot and automated identity/link assertions.
2. Shared Collector Archive visual system and asset set.
3. Landing page conversion rewrite.
4. Pull Rates field-guide rewrite.
5. Support rewrite and FAQ schema.
6. Privacy and Terms reconciliation.
7. Root portfolio, llms, README, 404, sitemap, and CI reconciliation.
8. Narrow `packrip.co` reverse-link change.
9. Full local visual, accessibility, SEO, and cross-repository verification.

The sitemap is regenerated only after the relevant HTML commit so `<lastmod>` reflects the correct Git history. No push or production deployment is part of plan creation; deployment requires the normal repository release flow.

## 12. Acceptance Criteria

The work is complete when:

- a first-time visitor identifies the page as the official PackRip Pokémon TCG iPhone app hub from the first viewport;
- all five PackRip pages use the Collector Archive/Field Guide system and contain no active Mythos positioning;
- every public product name matches `PackRip: TCG Card Packs`;
- every App Store CTA resolves to App ID `6763404045` with the approved provider/campaign parameters;
- GitHub Pages has contextual links to `packrip.co`, and the live web build has a crawlable link back to the iOS hub;
- landing/support/legal copy agrees with current App Store and repository evidence;
- no copy implies shared web/iOS progress;
- structured data parses and matches visible content;
- all local assets exist, have dimensions, and do not hotlink third-party card/CDN content;
- the five pages pass desktop/mobile visual review and keyboard/reduced-motion checks;
- required repository build and audit commands pass;
- sitemap and AI-crawler files contain the updated identity;
- no unrelated gameplay, backend, monetization, screenshot, or product changes are included.

## 13. References

- Live App Store listing: `https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045`
- PackRip web product: `https://packrip.co`
- Existing iOS hub: `https://elhanarinc.github.io/packrip-cards/`
- Google Search Central URL-move guidance: `https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes`
- Current cross-promo configuration: `../pokemon-pack-opening/src/config/iosLaunch.ts`
- Current iOS product implementation: `../packrip-ios/`
