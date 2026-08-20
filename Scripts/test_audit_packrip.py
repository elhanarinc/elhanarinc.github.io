#!/usr/bin/env python3
"""Two-sided correctness tests for Scripts/audit-packrip.py.

Positive probe: one fully compliant synthetic page that exercises every
check family (A through Q) and must produce zero findings — proving the
auditor has no false positives on a page that does everything right.

Negative probes: one page per check family (A through Q), each carrying
exactly one deliberate violation, asserting the expected finding substring
appears — proving every check family actually fires, including C (sync
claims), K (target=_blank without noopener), and Q (inline motion), which
had never executed their failure branch before this test existed.

Probe files are written under packrip-cards/ as throwaway filenames
(prefixed with "_test_") and removed via unittest.TestCase.addCleanup, the
same pattern the brief's original Step 7 probe uses. No file under version
control — no real HTML page, no locked constant's on-disk value — is ever
modified; CANONICAL_FOR and LINK_CONTRACT_PAGES are extended in memory for
the duration of a single test only and are always restored, because
audit_page() has no other way to be told "this throwaway rel is a
canonical/conversion page" without touching a real page on disk.

Stdlib unittest only. No network calls.

Usage:
    python3 Scripts/test_audit_packrip.py
    python3 -m unittest Scripts.test_audit_packrip -v
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = REPO / "Scripts" / "audit-packrip.py"

_spec = importlib.util.spec_from_file_location("audit_packrip_under_test", SCRIPT)
aud = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aud)

PROBE_REL = "packrip-cards/_test_probe.html"
PROBE_PATH = REPO / PROBE_REL
ASSET_REL = "packrip-cards/_test_asset.png"
ASSET_PATH = REPO / ASSET_REL
ASSET_NAME = pathlib.Path(ASSET_REL).name  # "_test_asset.png", for relative hrefs

# Compliant defaults for every slot the template below fills in. A test
# overrides exactly the slot(s) needed to trip one check family.
DEFAULT_SLOTS = {
    "title": "PackRip: TCG Card Packs — Test Probe",
    "stale": "",
    "numeric_claim": "",
    "sync_claim": "",
    "product_name_mention": "PackRip: TCG Card Packs is a native iPhone app.",
    "canonical_href": f"{aud.SITE}{aud.HUB}_test_probe.html",
    "og_url": f"{aud.SITE}{aud.HUB}_test_probe.html",
    "meta_description": '<meta name="description" content="Test probe page for the PackRip audit suite.">',
    "og_type": '<meta property="og:type" content="website">',
    "og_title": '<meta property="og:title" content="PackRip: TCG Card Packs">',
    "og_description": '<meta property="og:description" content="Test probe page.">',
    "og_image": '<meta property="og:image" content="/packrip-cards/images/app-icon.png">',
    "og_site_name": f'<meta property="og:site_name" content="{aud.PRODUCT_NAME}">',
    "twitter_card": '<meta name="twitter:card" content="summary">',
    "twitter_title": '<meta name="twitter:title" content="PackRip: TCG Card Packs">',
    "twitter_description": '<meta name="twitter:description" content="Test probe page.">',
    "twitter_image": '<meta name="twitter:image" content="/packrip-cards/images/app-icon.png">',
    "robots": '<meta name="robots" content="index,follow">',
    "app_banner": f'<meta name="apple-itunes-app" content="app-id={aud.APP_ID}">',
    "icon_link": '<link rel="icon" href="/packrip-cards/images/app-icon.png">',
    "touch_icon_link": '<link rel="apple-touch-icon" href="/packrip-cards/images/app-icon.png">',
    "jsonld": ('<script type="application/ld+json">'
               '{"@context":"https://schema.org","@type":"SoftwareApplication",'
               '"name":"PackRip: TCG Card Packs"}</script>'),
    "store_href": f"{aud.APP_STORE_BASE}?pt={aud.PROVIDER_TOKEN}&ct=packrip_ios_github_hero&mt=8",
    "web_href": ("https://www.packrip.co/?utm_source=elhanarinc_github&"
                 "utm_medium=referral&utm_campaign=packrip_ios_hub&"
                 "utm_content=hero_play_web"),
    "blank_anchor": '<a href="https://example.com/external" target="_blank" rel="noopener">External reference</a>',
    "img_main": '<img src="/packrip-cards/images/app-icon.png" alt="PackRip app icon" width="64" height="64">',
    "img_relative": f'<img src="{ASSET_NAME}" alt="Relative test asset" width="32" height="32">',
    "internal_link": '<a href="rarity.html">See rarity odds</a>',
    "skip_link": '<a href="#main">Skip to content</a>',
    "header": "<header><nav>Nav</nav></header>",
    "footer": "<footer>Footer</footer>",
    "inline_style": "",
}

TEMPLATE = """<!doctype html><html lang="en"><head>
<title>{title}</title>
{meta_description}
{robots}
{app_banner}
{og_type}
{og_title}
{og_description}
{og_image}
{og_site_name}
<meta property="og:url" content="{og_url}">
{twitter_card}
{twitter_title}
{twitter_description}
{twitter_image}
<link rel="canonical" href="{canonical_href}">
{icon_link}
{touch_icon_link}
{jsonld}
</head><body>
{skip_link}
{header}
<main id="main">
<p>{product_name_mention}</p>
<p>{stale}</p>
<p>{numeric_claim}</p>
<p>{sync_claim}</p>
<div {inline_style}>Motion test</div>
{img_main}
{img_relative}
<a href="{store_href}">Download on the App Store</a>
<a href="{web_href}">Open the web simulator</a>
{internal_link}
{blank_anchor}
</main>
{footer}
</body></html>"""


def render(**overrides: str) -> str:
    slots = dict(DEFAULT_SLOTS)
    slots.update(overrides)
    return TEMPLATE.format(**slots)


class AuditPackripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # A real local asset the "relative path" checks (M) can resolve.
        ASSET_PATH.write_bytes(b"\x89PNG\r\n\x1a\n")

    @classmethod
    def tearDownClass(cls) -> None:
        ASSET_PATH.unlink(missing_ok=True)

    # -- helpers -----------------------------------------------------

    def run_probe(self, html: str) -> list[str]:
        PROBE_PATH.write_text(html, encoding="utf-8")
        self.addCleanup(lambda: PROBE_PATH.unlink(missing_ok=True))
        findings: list[str] = []
        aud.audit_page(PROBE_REL, findings)
        return findings

    def patch_canonical_for(self, value: str) -> None:
        """Temporarily register PROBE_REL in CANONICAL_FOR so check E's
        comparison branch actually executes. Restored in addCleanup — the
        on-disk auditor and its locked CANONICAL_FOR value are untouched
        once the test ends; this only mutates the in-memory dict object for
        the duration of one test."""
        had = PROBE_REL in aud.CANONICAL_FOR
        old = aud.CANONICAL_FOR.get(PROBE_REL)
        aud.CANONICAL_FOR[PROBE_REL] = value

        def _restore() -> None:
            if had:
                aud.CANONICAL_FOR[PROBE_REL] = old
            else:
                aud.CANONICAL_FOR.pop(PROBE_REL, None)

        self.addCleanup(_restore)

    def patch_link_contract_pages(self) -> None:
        """Temporarily register PROBE_REL as a conversion page so check J's
        branch executes. Restored in addCleanup."""
        had = PROBE_REL in aud.LINK_CONTRACT_PAGES
        aud.LINK_CONTRACT_PAGES.add(PROBE_REL)

        def _restore() -> None:
            if not had:
                aud.LINK_CONTRACT_PAGES.discard(PROBE_REL)

        self.addCleanup(_restore)

    def assert_finding(self, findings: list[str], substring: str) -> None:
        self.assertTrue(
            any(substring in f for f in findings),
            f"expected a finding containing {substring!r}, got: {findings!r}",
        )

    # -- positive probe: everything right, zero findings --------------

    def test_00_fully_compliant_page_has_zero_findings(self) -> None:
        want = f"{aud.SITE}{aud.HUB}_test_probe.html"
        self.patch_canonical_for(want)  # exercises E's match branch
        self.patch_link_contract_pages()  # exercises J's satisfied branch
        findings = self.run_probe(render())
        self.assertEqual(findings, [], f"compliant page should be clean: {findings!r}")

    # -- negative probes: one per check family A-Q --------------------

    def test_a_stale_term(self) -> None:
        findings = self.run_probe(render(stale="Mythos edition available now."))
        self.assert_finding(findings, "stale term")

    def test_b_forbidden_numeric_claim(self) -> None:
        # New copy phrased differently from the literal Mythos-era strings —
        # this exercises the general "\b\d+\s+packs?\b" pattern, not a
        # literal one.
        findings = self.run_probe(render(numeric_claim="5 packs are stacked in the vault this week."))
        self.assert_finding(findings, "forbidden claim '5 packs'")

    def test_c_sync_implying_copy(self) -> None:
        # Never fired before this test existed. New phrasing, not one of
        # the four original literal SYNC_CLAIMS strings.
        findings = self.run_probe(render(sync_claim="Your progress syncs across devices automatically."))
        self.assert_finding(findings, "sync-implying copy")

    def test_d_partial_product_name(self) -> None:
        findings = self.run_probe(render(product_name_mention="PackRip: Legends is now available."))
        self.assert_finding(findings, "partial product name")

    def test_e_canonical_mismatch(self) -> None:
        want = f"{aud.SITE}{aud.HUB}_test_probe.html"
        self.patch_canonical_for(want)
        findings = self.run_probe(render(canonical_href=f"{aud.SITE}{aud.HUB}wrong.html"))
        self.assert_finding(findings, "canonical is")

    def test_f_missing_required_metadata(self) -> None:
        findings = self.run_probe(render(meta_description=""))
        self.assert_finding(findings, "missing meta description")

    def test_g_og_site_name_not_full_product_name(self) -> None:
        findings = self.run_probe(render(og_site_name='<meta property="og:site_name" content="PackRip">'))
        self.assert_finding(findings, "og:site_name is not the full product name")

    def test_h_app_store_link_missing_attribution(self) -> None:
        bad_href = f"{aud.APP_STORE_BASE}?ct=packrip_ios_github_hero&mt=8"
        findings = self.run_probe(render(store_href=bad_href))
        self.assert_finding(findings, f"App Store link missing pt={aud.PROVIDER_TOKEN}")

    def test_i_packrip_link_missing_utm(self) -> None:
        bad_href = ("https://www.packrip.co/?utm_source=elhanarinc_github&"
                    "utm_medium=referral&utm_content=hero_play_web")
        findings = self.run_probe(render(web_href=bad_href))
        self.assert_finding(findings, "packrip.co link missing utm_campaign=packrip_ios_hub")

    def test_j_conversion_page_missing_ctas(self) -> None:
        self.patch_link_contract_pages()
        findings = self.run_probe(render(store_href="", web_href=""))
        self.assert_finding(findings, "no App Store CTA on a conversion page")
        self.assert_finding(findings, "no packrip.co link on a conversion page")

    def test_k_target_blank_without_noopener(self) -> None:
        # Never fired before this test existed.
        bad_anchor = '<a href="https://example.com/external" target="_blank">External reference</a>'
        findings = self.run_probe(render(blank_anchor=bad_anchor))
        self.assert_finding(findings, "target=_blank without rel=noopener")

    def test_l_image_missing_alt(self) -> None:
        bad_img = '<img src="/packrip-cards/images/app-icon.png" width="64" height="64">'
        findings = self.run_probe(render(img_main=bad_img))
        self.assert_finding(findings, "img without alt attribute")

    def test_m_local_asset_missing_relative_path(self) -> None:
        # Exercises the relative-path fix: a page-relative src that does
        # NOT start with /packrip-cards/ must still be checked.
        bad_img = '<img src="_missing_asset.png" alt="Missing asset" width="10" height="10">'
        findings = self.run_probe(render(img_relative=bad_img))
        self.assert_finding(findings, "local asset does not exist: _missing_asset.png")

    def test_n_internal_link_missing_relative_path(self) -> None:
        # Exercises the relative-path fix: a page-relative href that does
        # NOT start with /packrip-cards/ must still be checked.
        bad_link = '<a href="nonexistent-page.html">Broken link</a>'
        findings = self.run_probe(render(internal_link=bad_link))
        self.assert_finding(findings, "internal link target missing: nonexistent-page.html")

    def test_o_jsonld_forbidden_key(self) -> None:
        bad_jsonld = ('<script type="application/ld+json">'
                      '{"@context":"https://schema.org","@type":"SoftwareApplication",'
                      '"name":"PackRip: TCG Card Packs","price":"0"}</script>')
        findings = self.run_probe(render(jsonld=bad_jsonld))
        self.assert_finding(findings, "JSON-LD block #1 contains forbidden key 'price'")

    def test_p_missing_skip_link(self) -> None:
        findings = self.run_probe(render(skip_link=""))
        self.assert_finding(findings, "missing skip link to #main")

    def test_q_inline_motion_double_and_single_quotes(self) -> None:
        # Never fired before this test existed. Cover both quote styles —
        # the minor fix added single-quote support.
        findings_double = self.run_probe(render(inline_style='style="transition: opacity 0.2s;"'))
        self.assert_finding(findings_double, "inline transition/animation cannot be disabled by reduced-motion")

        findings_single = self.run_probe(render(inline_style="style='animation: fade 1s;'"))
        self.assert_finding(findings_single, "inline transition/animation cannot be disabled by reduced-motion")

    # -- corpus tests: portfolio-wide absolutes rule --------------------

    def test_r_portfolio_wide_absolute_without_carveout(self) -> None:
        """Portfolio-wide claim about ads/analytics/tracking without carving
        PackRip out must be flagged by the corpus scan."""
        # Create a temporary corpus file with the bad wording
        test_rel = "README.md"
        test_path = REPO / test_rel
        original_content = test_path.read_text(encoding="utf-8")

        # Inject a standalone portfolio-wide claim (without PackRip carve-out).
        # Note: must not mention PackRip, or the second pass will skip it.
        bad_line = "\nNo product on this site serves ads or ships an ad SDK."
        bad_content = original_content + bad_line
        test_path.write_text(bad_content, encoding="utf-8")
        self.addCleanup(lambda: test_path.write_text(original_content, encoding="utf-8"))

        findings: list[str] = []
        aud.audit_corpus(findings)
        self.assert_finding(findings, "portfolio-wide absolute about")

    def test_s_portfolio_wide_absolute_with_carveout(self) -> None:
        """Portfolio-wide claim about ads/analytics/tracking that names
        PackRip on the same line (carving it out) must NOT be flagged."""
        test_rel = "llms.txt"
        test_path = REPO / test_rel
        original_content = test_path.read_text(encoding="utf-8")

        # Create a portfolio-wide line that names PackRip (carve-out)
        test_line = "Common privacy posture across all products: no advertising identifier. PackRip: TCG Card Packs additionally serves disclosed placements."
        bad_content = original_content.replace(
            "Common privacy posture across all products",
            test_line.split(".")[0]
        )
        test_path.write_text(bad_content, encoding="utf-8")
        self.addCleanup(lambda: test_path.write_text(original_content, encoding="utf-8"))

        findings: list[str] = []
        aud.audit_corpus(findings)
        # Should NOT find the portfolio-wide absolute because it names PackRip
        bad_findings = [f for f in findings if "portfolio-wide absolute" in f and "advertising" in f]
        self.assertEqual(bad_findings, [], f"carve-out line should not trigger finding: {bad_findings!r}")


if __name__ == "__main__":
    sys.exit(unittest.main())
