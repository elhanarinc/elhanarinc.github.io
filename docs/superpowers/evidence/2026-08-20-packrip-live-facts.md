# PackRip iOS hub — live facts snapshot (2026-08-20)

Frozen evidence the PackRip iOS hub copy (Tasks 2–12) is written against. All
values below were captured by running the commands in `## Command log` from
the repo root on 2026-08-20. This snapshot is not maintainable prose — it is
inputs to a contract. See `## Re-check trigger` for when it goes stale.

## Command log

```bash
mkdir -p docs/superpowers/evidence
curl -s 'https://itunes.apple.com/lookup?id=6763404045&country=us' \
  | python3 -c 'import json,sys; r=json.load(sys.stdin)["results"][0]; print(json.dumps({k:r.get(k) for k in ("trackName","trackViewUrl","sellerName","minimumOsVersion","trackContentRating","contentAdvisoryRating","primaryGenreName","genres","languageCodesISO2A","supportedDevices","currentVersionReleaseDate","formattedPrice","artistViewUrl")}, indent=2, ensure_ascii=False))'
```

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

```bash
for p in / /sets /faq /pull-rate/base1/holo-rare; do
  printf '%s -> ' "$p"
  curl -s -o /dev/null -w '%{http_code}\n' "https://packrip.co${p}"
done
```

Supplementary (not required by the plan, run to understand the non-200s):

```bash
for p in / /sets /faq /pull-rate/base1/holo-rare; do
  printf '%s -> ' "$p"
  curl -s -o /dev/null -w '%{http_code} -> ' "https://packrip.co${p}"
  curl -s -o /dev/null -w '%{redirect_url}\n' "https://packrip.co${p}"
done
for p in / /sets /faq /pull-rate/base1/holo-rare; do
  printf '%s -> ' "$p"
  curl -s -o /dev/null -w '%{http_code}\n' "https://www.packrip.co${p}"
done
```

```bash
cat ../packrip-ios/ASC/screenshot-captions.json
```

```bash
cat ../pokemon-pack-opening/src/config/iosLaunch.ts
```

## Live App Store listing

iTunes Lookup API (`https://itunes.apple.com/lookup?id=6763404045&country=us`)
returned `resultCount: 1`. Verbatim fields:

```json
{
  "trackName": "PackRip: TCG Card Packs",
  "trackViewUrl": "https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045?uo=4",
  "sellerName": "Arinc Elhan",
  "minimumOsVersion": "17.0",
  "trackContentRating": "4+",
  "contentAdvisoryRating": "4+",
  "primaryGenreName": "Games",
  "genres": [
    "Games",
    "Entertainment",
    "Simulation",
    "Card"
  ],
  "languageCodesISO2A": [
    "EN"
  ],
  "currentVersionReleaseDate": "2026-08-19T20:45:15Z",
  "formattedPrice": "Free",
  "artistViewUrl": "https://apps.apple.com/us/developer/arinc-elhan/id1822604589?uo=4"
}
```

(`supportedDevices` was returned but is omitted here as a very long device
list irrelevant to copy decisions — every iPhone from the 5s onward supports
this build.)

**`trackViewUrl` settles the slug question**: the live listing path is
`/us/app/packrip-tcg-card-packs/id6763404045`, i.e. the canonical slug is
`packrip-tcg-card-packs` — matching `Scripts/audit-packrip.py`'s
`APP_STORE_BASE` (`https://apps.apple.com/us/app/packrip-tcg-card-packs/id6763404045`)
and NOT the `packrip-cards` slug still hardcoded in the sibling web repo's
`iosLaunch.ts` (see `## Known conflicts` below).

- `minimumOsVersion`: `17.0`
- `trackContentRating`: `4+`
- `contentAdvisoryRating`: `4+`

## Live gameplay config

`../packrip-ios/Worker/config/gameplay.json`, read directly:

```
pity thresholds : {'holo': 20, 'holoEx': 50, 'shining': 150, 'goldStar': 150}
foil rates      : {'common': 0.01, 'uncommon': 0.01, 'rare': 0.015, 'holo': 0.02, 'holoEx': 0.03, 'rareSecret': 0.05, 'shining': 0.05, 'crystal': 0.05, 'goldStar': 0.05, 'illustration': 0.03}
foil multiplier : 5.0
pull rates      : {'godPack': 0.002, 'crystal': 0.01, 'shining': 0.02, 'goldStar': 0.028, 'rareSecret': 0.05, 'holoEx': 0.167, 'holo': 0.28, 'guaranteeHoloSecretChance': 0.05, 'illustration': 0.0}
hunt rates      : {'common': 0.6, 'uncommon': 0.6, 'rare': 0.6, 'holoRare': 0.5, 'rareSecret': 0.3, 'shining': 0.15, 'crystal': 0.1, 'holoEx': 0.4, 'goldStar': 0.08, 'energy': 0.6, 'illustration': 0.4}
plus perks      : {'xpMultiplier': 1.75, 'dailyPackBonus': 4, 'sellRateMultiplier': 1.5, 'streakCoinMultiplier': 2.5}
forge enabled   : True
setCompletion   : [{'pct': 25, 'rewardCoins': 50, 'rewardShards': 10}, {'pct': 50, 'rewardCoins': 150, 'rewardShards': 25}, {'pct': 100, 'rewardCoins': 500, 'rewardShards': 100}]
```

This matches the brief's expected output exactly, including the `pity
thresholds` and `plus perks` lines. Notably: `pity.thresholds` has no
`rareSecret` or `crystal` key (only `holo`, `holoEx`, `shining`, `goldStar`
are pity-guaranteed), and `plusPerks.xpMultiplier` is `1.75`, not `1.5`. Both
are why `FORBIDDEN_NUMERIC_CLAIMS` in the auditor bans `1.5× XP` and why the
copy must never publish a pity number for `rareSecret`/`crystal`.

## Frozen App Store screenshots

`../packrip-ios/ASC/screenshot-captions.json` captions the shipped `en-US`
screenshots (verbatim, line1 + line2 concatenated):

- `01_hero_apollo_card.png` → "Open Mythology Booster Packs"
- `05_home_sets.png` → "Greek, Norse, Egyptian & Beyond"

(Full caption set also includes "Tear Into Mythic Boosters", "Holographic &
Gold-Star Pulls", "Build Your Creature Collection", "16 Seals Permanent
Perks", "Pull Rate Transparency", "Subscribe Or Buy Coins", "Cancel
Anytime" — Mythos-era wording throughout.)

These screenshots are **frozen by owner decision** — they are not being
re-rendered for this plan. The hub therefore labels them generically as
iOS-app screenshots (e.g. "Screenshots from the App Store listing") and does
**not** repeat any of their Mythos-era captions in surrounding hub copy,
which is why `STALE_TERMS` in the auditor bans `Mythology`, `mytholog\w*`,
`mythic\w*`, `pantheon`, `deity/deities`, and the literal phrase
`Greek, Norse`.

## Web-product link targets

```
/ -> 301
/sets -> 301
/faq -> 301
/pull-rate/base1/holo-rare -> 301
```

None of the four `https://packrip.co<path>` targets returned `200`. All four
returned `301`, redirecting to the `www.` host (`https://www.packrip.co/`,
`/sets`, `/faq`, `/pull-rate/base1/holo-rare` respectively — confirmed with
`curl -w '%{redirect_url}'`); the `www.` versions independently return `200`
for all four paths. Per the plan's instruction, a non-200 for a bare
`packrip.co` path is a real finding to record, not a failure to retry
around — this snapshot leaves it exactly as measured (bare-domain path,
301) rather than substituting the `www.` result. Later tasks that place
outbound links to these targets should be aware the bare-domain path
redirects rather than resolving directly.

## Known conflicts carried into the copy

1. **Mythos screenshot captions vs. the Pokémon hub framing.** The shipped
   App Store screenshots are captioned "Open Mythology Booster Packs" and
   "Greek, Norse, Egyptian & Beyond" (see `## Frozen App Store screenshots`),
   but this plan reframes the iOS hub around the Pokémon-era pack-opening
   product. The screenshots are frozen and not re-rendered; the hub avoids
   the conflict by never repeating the Mythos captions and labeling the
   screenshots generically as "from the App Store listing."

2. **"All card art is original to PackRip" vs. the Pokémon era wrappers.**
   The live App Store listing describes the card art as original to
   PackRip, which sits in tension with the web product's Pokémon-era-themed
   pack wrappers. This is resolved by the Global Constraints' copy
   coherence rule: the hub copy must stay consistent with the listing's
   "original art" framing and must not claim or imply the app contains
   licensed Pokémon card art.

3. **`1.5×` vs. `1.75` XP disagreement.** Prior listing/marketing copy
   referenced a `1.5×` XP multiplier for the Plus perk, but the live
   `Worker/config/gameplay.json` (`## Live gameplay config` above) sets
   `plusPerks.xpMultiplier` to `1.75`. `Scripts/audit-packrip.py` forbids
   publishing `1.5× XP` (`FORBIDDEN_NUMERIC_CLAIMS`) specifically because of
   this disagreement; the hub does not publish either specific multiplier.

4. **`iosLaunch.ts` slug mismatch — deliberately left untouched.** The
   sibling web repo's `../pokemon-pack-opening/src/config/iosLaunch.ts`
   hardcodes `APP_STORE_BASE_URL` with the slug `packrip-cards`
   (`https://apps.apple.com/us/app/packrip-cards/id6763404045`), while the
   live `trackViewUrl` (`## Live App Store listing` above) and this plan's
   `APP_STORE_BASE` both use `packrip-tcg-card-packs`. Apple's redirect
   makes either slug resolve, so this is a latent inconsistency, not a
   broken link. `../pokemon-pack-opening` is a sibling repo on its own
   feature branch and is out of scope for this plan — it is recorded here
   as evidence and deliberately not fixed.

## Re-check trigger

This snapshot is void if the App Store listing name, subtitle, or
description changes, if `Worker/config/gameplay.json` pity or plusPerks
values change, or if the App Store screenshots are re-rendered.
