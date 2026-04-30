# elhanarinc.github.io

Static site hosting for my indie products. Each product lives in its own subdirectory and ships its own landing, support, terms, and privacy pages. The flagship is **Hexora**, a private I Ching oracle for iPhone.

Live: <https://elhanarinc.github.io/>

## Hexora — I Ching Oracle for iPhone

A private, beautifully crafted I Ching oracle for iPhone (iOS 18+). Cast a hexagram with an animated three-coin ritual, get a thoughtful AI-assisted interpretation grounded in the public-domain James Legge 1882 translation, and keep an on-device reflection journal. No account, no tracking SDKs, no social layer. Bilingual EN + TR.

- App Store: <https://apps.apple.com/us/app/hexora-i-ching-oracle/id6764511696>
- Landing (EN): <https://elhanarinc.github.io/hexora/>
- Landing (TR): <https://elhanarinc.github.io/hexora/tr/>
- Long-form (EN): <https://elhanarinc.github.io/hexora/oracle.html> · <https://elhanarinc.github.io/hexora/journal.html>
- Long-form (TR): <https://elhanarinc.github.io/hexora/tr/fal.html>
- 64 hexagrams — EN: <https://elhanarinc.github.io/hexora/hexagram/> · TR: <https://elhanarinc.github.io/hexora/tr/hexagram/>
- Privacy · Terms · Support pages live at the corresponding `/hexora/*.html` paths

## PackRip: Mythos — Mythology Pack-Opening for iPhone

A native SwiftUI collectible-card pack-opening simulator for iOS 17+. Painted creatures and deities from public-domain world mythology, generated offline via fal.ai Flux. Olympus and Asgard ship in the launch build; eight more pantheons (Kemet, Babel, Avalon, Slavica, Yokai, Cryptidae, Bestiarum, Draconis) unlock as you climb Trainer levels. 7 rarity tiers + God Pack, hunt packs, 16 Seals, no PvP, no ads. English-only.

- App Store: <https://apps.apple.com/us/app/packrip-mythos/id6763404045>
- Landing: <https://elhanarinc.github.io/packrip-mythos/>
- Long-form: <https://elhanarinc.github.io/packrip-mythos/pack-opening.html> · <https://elhanarinc.github.io/packrip-mythos/rarity.html>
- Pantheon hub: <https://elhanarinc.github.io/packrip-mythos/pantheons/> (Olympus, Asgard detail pages live)
- Privacy · Terms · Support pages live at the corresponding `/packrip-mythos/*.html` paths
- Browser companion: <https://packrip.co>

## Other products

| Product | Live | What it is |
|---|---|---|
| Filmoire 35 | [filmoire35/](https://elhanarinc.github.io/filmoire35/) | Vintage film camera for iPhone |
| Glance | [glance/](https://elhanarinc.github.io/glance/) | macOS menu-bar utility |
| WiFi Checker | [wifi-checker/](https://elhanarinc.github.io/wifi-checker/) | Network diagnostic |
| TypeSuggest | [typesuggest/](https://elhanarinc.github.io/typesuggest/) | AI writing helper |

## SEO / discovery

- `sitemap.xml` — full XML sitemap with hreflang annotations (160+ URLs across Hexora, PackRip: Mythos and the rest)
- `robots.txt` — references the sitemap, allows all
- `llms.txt` — AI crawler index (ChatGPT, Claude, Perplexity)
- IndexNow key file at root for Bing/Yandex push indexing
- 404.html for graceful errors
- All Hexora pages ship `MobileApplication`, `Article`, and `FAQPage` JSON-LD where applicable, plus `og:image:width/height/type`, `twitter:image`, hreflang, and `max-image-preview:large` robots hints.
- All PackRip: Mythos pages ship `MobileApplication` + `SoftwareApplication` JSON-LD on the home, `Article` JSON-LD on long-form (`pack-opening.html`, `rarity.html`, pantheon detail pages), and `FAQPage` JSON-LD on `support.html` and `pack-opening.html`. Same OG/Twitter parity as Hexora.

## License

Site code (CSS, HTML scaffolding) © 2026 Arinc Elhan. Hexora's I Ching content is paraphrased from the **public-domain James Legge 1882 translation** — never the still-copyrighted Wilhelm-Baynes 1950 Princeton translation.
