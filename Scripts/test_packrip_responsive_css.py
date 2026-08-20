#!/usr/bin/env python3
"""Regression checks for the PackRip hub's narrow responsive contract."""

from pathlib import Path
import re
import unittest


CSS = (Path(__file__).resolve().parent.parent / "packrip-cards" / "_shared.css").read_text()


def media_body(max_width: int) -> str:
    match = re.search(rf"@media \(max-width: {max_width}px\) \{{(.*?)\n\}}", CSS, re.S)
    if not match:
        raise AssertionError(f"missing max-width: {max_width}px media block")
    return match.group(1)


class PackRipResponsiveCssTests(unittest.TestCase):
    def test_mobile_nav_is_a_contained_scroller_and_anchor_offset_matches_two_rows(self) -> None:
        mobile = media_body(520)
        self.assertRegex(
            mobile,
            r"\.nav-links\s*\{[^}]*width:\s*100%;[^}]*min-width:\s*0;",
        )
        self.assertRegex(
            mobile,
            r"\.prose h2\s*\{[^}]*scroll-margin-top:\s*132px;",
        )

    def test_long_odds_descriptions_stack_on_mobile(self) -> None:
        mobile = media_body(520)
        self.assertRegex(mobile, r"\.odds-row\s*\{[^}]*flex-direction:\s*column;")
        self.assertRegex(mobile, r"\.odds-row dd\s*\{[^}]*white-space:\s*normal;")

    def test_ledger_is_two_columns_at_390_and_one_column_at_320(self) -> None:
        mobile = media_body(520)
        narrow = media_body(359)
        self.assertNotRegex(mobile, r"\.ledger\s*\{[^}]*grid-template-columns:\s*1fr;")
        self.assertRegex(narrow, r"\.ledger\s*\{[^}]*grid-template-columns:\s*1fr;")


if __name__ == "__main__":
    unittest.main()
