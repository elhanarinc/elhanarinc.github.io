"""Browser checks for the root homepage: responsive layout, dark mode and
the ⌘K command palette. Skips when Playwright for Python is not installed.

Spec: docs/superpowers/specs/2026-10-20-homepage-console-design.md (local only, gitignored)
"""
import functools
import http.server
import pathlib
import socketserver
import threading

import pytest

sync_api = pytest.importorskip("playwright.sync_api")

REPO = pathlib.Path(__file__).resolve().parent.parent
WIDTHS = [320, 360, 390, 768, 1024, 1280, 1440]


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="module")
def base_url():
    handler = functools.partial(_Quiet, directory=str(REPO))
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as httpd:
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()
        yield f"http://127.0.0.1:{httpd.server_address[1]}/"
        httpd.shutdown()


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as p:
        # Prefer the installed Chrome: the Playwright-managed build may not
        # match this Python package's version.
        try:
            b = p.chromium.launch(channel="chrome")
        except sync_api.Error:
            b = p.chromium.launch()
        yield b
        b.close()


def _page(browser, base_url, **ctx):
    context = browser.new_context(**ctx)
    page = context.new_page()
    page.goto(base_url, wait_until="load")
    return page


def _is_open(page):
    return page.evaluate("document.getElementById('cmdk').open")


def _visible_options(page):
    return page.locator("#cmdk-list [role=option]:visible")


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("width", WIDTHS)
def test_no_horizontal_scroll(browser, base_url, width, scheme):
    page = _page(browser, base_url, viewport={"width": width, "height": 900}, color_scheme=scheme)
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    page.context.close()


def test_palette_keyboard(browser, base_url):
    page = _page(browser, base_url, viewport={"width": 1280, "height": 900})
    trigger_focus = "document.activeElement && document.activeElement.id"

    page.keyboard.press("Meta+k")
    assert _is_open(page)
    assert page.evaluate(trigger_focus) == "cmdk-input"

    page.keyboard.type("film")
    opts = _visible_options(page)
    assert opts.count() == 1
    assert "Filmoire35" in opts.first.inner_text()

    page.keyboard.type("/")
    assert page.input_value("#cmdk-input").endswith("/")
    assert _is_open(page)

    page.fill("#cmdk-input", "")
    first = page.evaluate("[...document.querySelectorAll('#cmdk-list [role=option]')].findIndex(o => o.getAttribute('aria-selected') === 'true')")
    page.keyboard.press("ArrowDown")
    page.keyboard.press("ArrowDown")
    now = page.evaluate("[...document.querySelectorAll('#cmdk-list [role=option]')].findIndex(o => o.getAttribute('aria-selected') === 'true')")
    assert now == first + 2

    page.keyboard.press("Escape")
    assert not _is_open(page)
    assert page.evaluate(trigger_focus) == "cmdk-open"

    page.keyboard.press("Control+k")
    assert _is_open(page)
    page.keyboard.press("Escape")

    page.locator("body").click(position={"x": 5, "y": 300})
    page.keyboard.press("/")
    assert _is_open(page)
    assert page.input_value("#cmdk-input") == ""
    page.context.close()


def test_palette_enter_opens_active(browser, base_url):
    page = _page(browser, base_url, viewport={"width": 1280, "height": 900})
    page.keyboard.press("Meta+k")
    page.keyboard.type("filmoire")
    page.keyboard.press("Enter")
    page.wait_for_url("**/filmoire35/")
    page.context.close()


def test_palette_backdrop_click_closes(browser, base_url):
    page = _page(browser, base_url, viewport={"width": 1280, "height": 900})
    page.click("#cmdk-open")
    assert _is_open(page)
    page.mouse.click(10, 880)
    assert not _is_open(page)
    page.context.close()


def test_palette_opens_by_click_and_links_work(browser, base_url):
    page = _page(browser, base_url, viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    page.tap("#cmdk-open")
    assert _is_open(page)
    gh = page.locator("#cmdk-list [role=option] a", has_text="GitHub")
    assert gh.get_attribute("href") == "https://github.com/elhanarinc"
    size = page.evaluate("parseFloat(getComputedStyle(document.getElementById('cmdk-input')).fontSize)")
    assert size >= 16
    box = page.locator("#cmdk").bounding_box()
    assert box["x"] >= 0 and box["x"] + box["width"] <= 390
    page.context.close()


@pytest.mark.parametrize("scheme,bg", [("dark", "rgb(11, 13, 18)"), ("light", "rgb(246, 247, 249)")])
def test_dark_mode_tokens(browser, base_url, scheme, bg):
    page = _page(browser, base_url, color_scheme=scheme)
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == bg
    page.context.close()


def test_no_console_errors(browser, base_url):
    context = browser.new_context()
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: m.type == "error" and "fonts." not in (m.location or {}).get("url", "") and errors.append(m.text))
    page.goto(base_url, wait_until="load")
    page.click("#cmdk-open")
    page.keyboard.type("pack")
    page.keyboard.press("Escape")
    assert errors == []
    context.close()


def _selected_label(page):
    return page.evaluate("document.querySelector('#cmdk-list [aria-selected=true]').textContent")


def test_palette_tab_then_arrows_opens_highlighted(browser, base_url):
    page = _page(browser, base_url, viewport={"width": 1280, "height": 900})
    page.keyboard.press("Meta+k")
    page.keyboard.press("Tab")
    page.keyboard.press("ArrowDown")
    page.keyboard.press("ArrowDown")
    assert "Filmoire35" in _selected_label(page)
    page.keyboard.press("Enter")
    page.wait_for_url("**/filmoire35/")
    page.context.close()


def test_palette_activedescendant_follows_selection(browser, base_url):
    page = _page(browser, base_url, viewport={"width": 1280, "height": 900})
    page.keyboard.press("Meta+k")
    page.keyboard.press("ArrowDown")
    sel = page.evaluate("document.querySelector('#cmdk-list [aria-selected=true]').id")
    assert page.get_attribute("#cmdk-input", "aria-activedescendant") == sel
    page.context.close()


@pytest.mark.parametrize("mode", ["missing", "rejected"])
def test_copy_email_without_clipboard(browser, base_url, mode):
    context = browser.new_context()
    script = ("Object.defineProperty(navigator, 'clipboard', {value: undefined, configurable: true});"
              if mode == "missing" else
              "Object.defineProperty(navigator, 'clipboard', {value: {writeText: () => Promise.reject(new Error('denied'))}, configurable: true});")
    context.add_init_script(script)
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url, wait_until="load")
    page.click("#cmdk-open")
    page.click("[data-copy]")
    page.wait_for_timeout(200)
    assert errors == []
    assert "elhanarinc@gmail.com" in page.inner_text("#cmdk-status")
    context.close()


def test_copy_email_announces(browser, base_url):
    context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
    page = context.new_page()
    page.goto(base_url, wait_until="load")
    page.click("#cmdk-open")
    page.click("[data-copy]")
    page.wait_for_function("document.getElementById('cmdk-status').textContent.includes('Copied')")
    assert page.get_attribute("#cmdk-status", "aria-live") == "polite"
    context.close()


@pytest.mark.parametrize("width", [320, 360, 390, 768, 1024, 1440])
def test_layout_holds(browser, base_url, width):
    page = _page(browser, base_url, viewport={"width": width, "height": 900})
    assert page.evaluate("(() => { const h = document.querySelector('h1'); return h.scrollWidth <= h.clientWidth; })()")
    assert page.evaluate("""[...document.querySelectorAll('.svc')].every(row => {
        const r = row.getBoundingClientRect(), p = row.querySelector('.pill').getBoundingClientRect();
        return p.right <= r.right + 0.5 && p.left >= r.left && p.top >= r.top && p.bottom <= r.bottom;
    })""")
    page.context.close()


def test_mobile_trigger_shows_search_label(browser, base_url):
    page = _page(browser, base_url, viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    assert page.locator("#cmdk-open").inner_text().strip() == "Search"
    page.context.close()


def test_tap_result_navigates(browser, base_url):
    page = _page(browser, base_url, viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    page.tap("#cmdk-open")
    page.locator("#cmdk-list [role=option] a", has_text="Filmoire35").tap()
    page.wait_for_url("**/filmoire35/")
    page.context.close()


def test_dark_mode_text_colors(browser, base_url):
    page = _page(browser, base_url, color_scheme="dark")
    colors = page.evaluate("""['body', '.svc .desc', '.pill', '.card p'].map(s => getComputedStyle(document.querySelector(s)).color)""")
    assert colors == ["rgb(236, 238, 243)", "rgb(138, 146, 163)", "rgb(74, 222, 128)", "rgb(184, 191, 204)"]
    page.context.close()


def test_palette_expanded_reflects_results(browser, base_url):
    page = _page(browser, base_url, viewport={"width": 1280, "height": 900})
    page.keyboard.press("Meta+k")
    assert page.get_attribute("#cmdk-input", "aria-expanded") == "true"
    page.keyboard.type("zzzz")
    assert page.get_attribute("#cmdk-input", "aria-expanded") == "false"
    page.context.close()
