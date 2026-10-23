"""Static checks for the root homepage (index.html).

Spec: docs/superpowers/specs/2026-10-20-homepage-console-design.md (local only, gitignored)
"""
import hashlib
import json
import pathlib
import re
import subprocess

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
HTML = (REPO / "index.html").read_text(encoding="utf-8")

# Products removed from the site on 2026-10-20 must not come back here.
REMOVED_PRODUCTS = [
    "macos", "menu bar",
    "hexora", "roadshow", "warranty pad", "glance", "typesuggest",
    "wifi checker", "antrenman",
]

# Organisation names and wording that must never appear, stored as sha256 of
# the lowercased 1-3 word phrase, so the terms themselves stay out of this
# public repo. PAGE_HASHES is stricter than PUBLIC_HASHES because product
# facts in llms.txt legitimately say "available in English".
PUBLIC_HASHES = {
    "467b83c6d1797c2ed0d3eb20110321b2b36161042e33da3283bb3423c5deb9ff",
    "27ce19a3973be61262ea91799a234bd28ed738eaa73fec71c0af6b2e1d928249",
    "72d118b4e59bb2e49f6ab47569ba32d529c075922459303340f66c7fac439197",
    "a0b89699b2e6fd46c19bb33a69045d131fa8b46f2b2aa108d97e4ef614b03877",
    "45c849714eed79ed50fe3922aa4fe97b6debc59c784ffa1416b198d5d22275ea",
    "673405067fe9f7f6316d26be694a08ed256350c1c3fd90a362b956dc2a2b6a6f",
    "efa2707f1e97f3bc0e1d4362ab9ddc677f4d6a8e96aca04eb85f963960191cbe",
    "aea55a040c209ae000fe14bb3a496e15a4210e9e15fa65def8278765a7cace4e",
    "92d46204d8e9aeb3b37873c794348b3132ab9c9f33a89f2063c46180914c0104",
    "fb9d78cb1e099ccf5c7b06dca767a1f6b196d719961feb11e0d341049d609164",
    "926d3ba932dd9f384f13533029ed232e2ddd67e0a998a129b61802c7f4d94127",
}
PAGE_HASHES = {
    "467b83c6d1797c2ed0d3eb20110321b2b36161042e33da3283bb3423c5deb9ff",
    "ddd9818abacfde7afed60c93129175401439367a77e69ea93e0ddb3bb38e0bd9",
    "27ce19a3973be61262ea91799a234bd28ed738eaa73fec71c0af6b2e1d928249",
    "72d118b4e59bb2e49f6ab47569ba32d529c075922459303340f66c7fac439197",
    "bf90ace460be66498a913aaca0b7868806603cf0fef114305fcf81396c30b5ba",
    "b67edcdb95503aaeb8980b7017c4f7488871ce5908a5c945fb1b6334b808e960",
    "a0b89699b2e6fd46c19bb33a69045d131fa8b46f2b2aa108d97e4ef614b03877",
    "45c849714eed79ed50fe3922aa4fe97b6debc59c784ffa1416b198d5d22275ea",
    "673405067fe9f7f6316d26be694a08ed256350c1c3fd90a362b956dc2a2b6a6f",
    "b506f09dbc28a11fdcf8a84956b615bac5ba25da226073fabe827d8f5a3001bc",
    "efa2707f1e97f3bc0e1d4362ab9ddc677f4d6a8e96aca04eb85f963960191cbe",
    "aea55a040c209ae000fe14bb3a496e15a4210e9e15fa65def8278765a7cace4e",
    "92d46204d8e9aeb3b37873c794348b3132ab9c9f33a89f2063c46180914c0104",
    "fb9d78cb1e099ccf5c7b06dca767a1f6b196d719961feb11e0d341049d609164",
    "926d3ba932dd9f384f13533029ed232e2ddd67e0a998a129b61802c7f4d94127",
}


def phrases(text, longest=3):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {" ".join(words[i:i + n]) for n in range(1, longest + 1) for i in range(len(words) - n + 1)}


def banned_hits(text, hashes):
    return sorted(p for p in phrases(text) if hashlib.sha256(p.encode()).hexdigest() in hashes)


def test_no_banned_wording_on_page():
    assert banned_hits(HTML, PAGE_HASHES) == []


def jsonld_blocks():
    raw = re.findall(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S)
    return [json.loads(b) for b in raw]


def of_type(t):
    return [b for b in jsonld_blocks() if b.get("@type") == t]


@pytest.mark.parametrize("term", REMOVED_PRODUCTS)
def test_no_removed_products(term):
    assert not re.search(r"\b" + re.escape(term) + r"\b", HTML, re.I), term


def test_jsonld_profilepage():
    (page,) = of_type("ProfilePage")
    person = page["mainEntity"]
    assert person["@type"] == "Person"
    assert person["name"] == "Arınç Elhan"
    assert person["alternateName"] == "Arinc Elhan"
    assert "worksFor" not in person
    assert person["alumniOf"]["name"] == "Middle East Technical University"
    assert "https://www.packrip.co/" in person["sameAs"]

    (items,) = of_type("ItemList")
    urls = [i["url"] for i in items["itemListElement"]]
    assert urls == [
        "https://www.packrip.co/",
        "https://elhanarinc.github.io/packrip-cards/",
        "https://elhanarinc.github.io/filmoire35/",
        "https://elhanarinc.github.io/captain-mittens/",
    ]
    assert len(of_type("WebSite")) == 1


def test_head_meta():
    assert "<title>Arınç Elhan — Platform &amp; Backend Engineer, Ankara</title>" in HTML
    assert '<link rel="canonical" href="https://elhanarinc.github.io/">' in HTML
    assert re.search(r'<meta name="robots" content="index,follow[^"]*">', HTML)
    assert 'name="google-site-verification"' in HTML
    assert re.search(r'<meta name="viewport" content="[^"]*viewport-fit=cover', HTML)
    assert '<meta property="og:image" content="https://elhanarinc.github.io/og-cover.png">' in HTML


def test_copy():
    for s in ["I keep systems running.", "And build a few of my own.", "Things I run",
              "3 products", "What I do", "Stack", "Before"]:
        assert s in HTML, s
    body = HTML[HTML.index("<body"):]
    order = [body.index(s) for s in ["Adyen", "Picus Security", "Forto", "METU"]]
    assert order == sorted(order)


def test_images_have_dimensions():
    for tag in re.findall(r"<img\b[^>]*>", HTML):
        assert "width=" in tag and "height=" in tag, tag


@pytest.mark.parametrize("href", [
    "https://github.com/elhanarinc",
    "https://www.linkedin.com/in/elhanarinc/",
    "https://x.com/elhanarinc",
    "https://www.packrip.co/",
    "mailto:elhanarinc@gmail.com",
    "/packrip-cards/",
    "/filmoire35/",
])
def test_links_present(href):
    assert f'href="{href}"' in HTML, href


# Public files that describe the site or this work: the same two rules apply.
PUBLIC_TEXT = ["llms.txt", "llms-full.txt", "README.md", "robots.txt", "404.html"]


def test_working_docs_are_not_published():
    """Specs, plans and agent scratch stay local: GitHub Pages serves every
    tracked file, so docs/superpowers/ and .superpowers/ must be gitignored."""
    tracked = subprocess.run(["git", "ls-files", "docs/superpowers", ".superpowers"],
                             cwd=REPO, capture_output=True, text=True, check=True).stdout
    assert tracked == ""
    ignore = (REPO / ".gitignore").read_text(encoding="utf-8").split()
    assert "docs/superpowers/" in ignore and ".superpowers/" in ignore


@pytest.mark.parametrize("rel", PUBLIC_TEXT)
def test_public_text_has_no_banned_wording(rel):
    text = (REPO / rel).read_text(encoding="utf-8")
    assert banned_hits(text, PUBLIC_HASHES) == []


def test_llms_role_is_consistent():
    for rel in ["llms.txt", "llms-full.txt"]:
        head = (REPO / rel).read_text(encoding="utf-8").split("\n", 1)[0].lower()
        assert "platform and backend engineer" in head, rel


def test_meta_description_fits_snippet():
    desc = re.search(r'<meta name="description" content="([^"]+)">', HTML).group(1)
    assert len(desc) <= 150, len(desc)


def test_person_has_no_banner_as_portrait():
    (page,) = of_type("ProfilePage")
    assert "image" not in page["mainEntity"]


def test_palette_input_has_accessible_name():
    tag = re.search(r'<input id="cmdk-input"[^>]*>', HTML).group(0)
    assert 'aria-label="Search or jump to"' in tag


@pytest.mark.parametrize("rel", ["llms.txt", "llms-full.txt"])
def test_llms_carry_no_set_counts(rel):
    text = (REPO / rel).read_text(encoding="utf-8")
    assert not re.search(r"\b\d{2,}\s+(?:\w+\s+)?sets\b", text)
