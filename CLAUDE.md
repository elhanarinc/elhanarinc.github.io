# CLAUDE.md: elhanarinc.github.io

Static GitHub Pages site (no build, no Jekyll): owner's portfolio, the PackRip iOS hub (`packrip-cards/`) and `filmoire35/`. See README.md for layout and commands.

## Hard rules
- Never move, rename or delete `app-ads.txt` (root and `packrip-cards/`), `llms.txt`, `llms-full.txt`, `sitemap.xml`, `robots.txt`, `404.html`, the IndexNow key file, or any privacy/terms/support page: App Store Connect and AdMob link to them. `/packrip-cards/` never moves or redirects.
- The PackRip hub conforms to the frozen PackRip design system (source of truth: `../packrip-ios/CLAUDE.md` and `DesignTokens.swift`; tokens in `packrip-cards/_shared.css`). Inter body, Archivo display, no new palettes, fonts, serif or AI-slop.
- Hub App Store links keep `pt=127914124`, a `ct`, `mt=8`; web links keep the `packrip_ios_hub` UTM set (`Scripts/audit-packrip.py` enforces).
- `llms*.txt` are hand-maintained: mirror price/tier/OS changes in the same commit.
- Commit format `type(scope): Capital...` (no `chore`); regen the sitemap after committing HTML. Never commit secrets.

## Commands
```bash
python3 -m http.server 4000
python3 Scripts/regen-sitemap.py
python3 Scripts/audit-packrip.py
python3 -I Scripts/test_homepage.py   # + test_audit_packrip.py, test_packrip_responsive_css.py
```

Orchestrator mode per ../CLAUDE.md (dev/runner/scout/reviewer/sim-qa, explicit model, no fork).
