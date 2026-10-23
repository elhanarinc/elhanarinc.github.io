#!/usr/bin/env python3
"""Generate captain-mittens/{tr,en}/ pages and patch captain-mittens/index.html (idempotent)."""
import json, pathlib, re, sys
from html import escape as E
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from captain_seo_content import L, APP_LIVE, STORE, BASE, MAIL, NAME

ROOT = pathlib.Path(__file__).resolve().parent.parent / "captain-mittens"
IMG = "/captain-mittens/images/"
SHOTS = ["shot_home.webp", "shot_board2.webp", "shot_board.webp", None]  # None = localized combo shot
APPLE = '<meta name="apple-itunes-app" content="app-id=6824941057">' if APP_LIVE else ''

def jld(o):
    return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "</script>"

def app_ld(lang, url):
    d = L[lang]
    return {"@context": "https://schema.org", "@type": ["MobileApplication", "VideoGame"], "name": NAME, "url": url,
            "description": d["desc"], "operatingSystem": "iOS", "applicationCategory": "GameApplication",
            "genre": "Puzzle", "inLanguage": ["tr", "en"], "image": BASE + IMG + "app-icon.png",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "TRY"},
            **({"downloadUrl": STORE, "installUrl": STORE} if APP_LIVE else {}),
            "publisher": {"@type": "Person", "name": "Arinc Elhan", "url": BASE + "/"}}

def faq_ld(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}

def faq_html(pairs):
    return "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>\n" for q, a in pairs)

def head(lang, title, desc, path, alts, img, ld):
    d = L[lang]; url = BASE + path
    al = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{v}">\n' for k, v in alts)
    return f'''<!doctype html>
<html lang="{lang}" class="dir-B">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#9fe0f4">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{APPLE}
<link rel="canonical" href="{url}">
{al}<link rel="icon" type="image/png" href="{IMG}app-icon.png">
<link rel="apple-touch-icon" href="{IMG}app-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="{d['locale']}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{BASE}{IMG}{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{BASE}{IMG}{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&display=swap">
<link rel="stylesheet" href="/captain-mittens/_style.css">
<link rel="stylesheet" href="/captain-mittens/_seo.css">
{ld}
</head>
'''

def chrome(lang, body, active=""):
    d = L[lang]; o = L[d["other"]]
    nav = "".join(f'<a href="{h}">{E(t)}</a>' for t, h in d["nav"])
    return f'''<body>
<a class="skip" href="#main">{"İçeriğe geç" if lang == "tr" else "Skip to content"}</a>
<header class="site"><div class="wrap in"><a class="brand" href="{d['path']}"><img src="{IMG}avatar_captain.webp" alt="" width="40" height="40"><span>Captain Mittens</span></a>
<nav aria-label="Main">{nav}<a class="lang" lang="{d['other']}" hreflang="{d['other']}" href="{o['path']}">{E(d['switch'])}</a></nav></div></header>
<main id="main">
{body}</main>
<footer class="site"><div class="wrap foot">
<div class="fb"><img src="{IMG}avatar_captain.webp" alt="" width="48" height="48" loading="lazy"><div><strong>{NAME}</strong></div></div>
<nav aria-label="Footer">{nav}<a href="mailto:{MAIL}">{MAIL}</a></nav>
<p class="fcopy">&copy; 2026 Arinc Elhan &middot; {E(d['foot'])}</p></div></footer>
</body></html>
'''

def cta(lang):
    if not APP_LIVE:
        return f'<span class="store" role="status">{E(L[lang]["cta"])}</span>'
    return f'<a class="store" href="{STORE}" rel="noopener"><span aria-hidden="true">&#63743;</span> {E(L[lang]["cta"])}</a>'

def shots(lang):
    d = L[lang]; out = []
    for i, s in enumerate(SHOTS):
        f = s or f"board_combo_{lang}.webp"
        eager = ' fetchpriority="high"' if i == 0 else ' loading="lazy" decoding="async"'
        out.append(f'<figure class="phone"><img src="{IMG}{f}" alt="{E(d["alts"][i])}" width="600" height="1304"{eager}></figure>')
    return "".join(out)

def landing(lang):
    d = L[lang]; o = L[d["other"]]
    feats = "".join(f"<li><h3>{E(t)}</h3><p>{E(p)}</p></li>" for t, p in d["feats"])
    body = f'''<section class="seo-hero"><div class="wrap seo-grid"><div>
<p class="eyebrow">{E(d['eyebrow'])}</p><h1>{NAME}</h1><p class="sub">{E(d['h1'])}</p>
<p class="lead">{E(d['pitch'])}</p><p>{cta(lang)}</p><p class="fine">{E(d['free'])}</p>
<p class="fine"><a href="{d['q']['file']}">{E(d['q']['h1'])}</a></p></div>
<div class="shots" aria-label="{E(d['shots_h'])}">{shots(lang)}</div></div></section>
<section class="seo-sec"><div class="wrap narrow"><h2>{E(d['feat_h'])}</h2><ul class="feats">{feats}</ul></div></section>
<section class="faq" id="faq"><div class="wrap narrow"><h2>{E(d['faq_h'])}</h2>
{faq_html(d['faq'])}</div></section>
<section class="seo-sec"><div class="wrap narrow"><p>{cta(lang)}</p></div></section>
'''
    alts = [(lang, d["path"]), (d["other"], o["path"]), ("x-default", "/captain-mittens/")]
    ld = jld(app_ld(lang, BASE + d["path"])) + "\n" + jld(faq_ld(d["faq"]))
    (ROOT / lang / "index.html").write_text(head(lang, d["title"], d["desc"], d["path"], alts, "shot_home.webp", ld) + chrome(lang, body))

def query(lang):
    d = L[lang]; q = d["q"]; o = L[d["other"]]
    path = d["path"] + q["file"]; opath = o["path"] + o["q"]["file"]
    paras = "".join(f"<p>{E(p)}</p>" for p in q["body"])
    body = f'''<section class="seo-hero"><div class="wrap seo-grid"><div>
<p class="eyebrow">{NAME}</p><h1>{E(q['h1'])}</h1>{paras}<p>{cta(lang)}</p>
<p class="fine"><a href="{d['path']}">{E(q['home'])}</a> &middot; <a href="{d['nav'][0][1]}">{E(d['nav'][0][0])}</a></p></div>
<div class="shots one"><figure class="phone"><img src="{IMG}shot_board2.webp" alt="{E(q['alt'])}" width="600" height="1304" fetchpriority="high"></figure></div></div></section>
'''
    alts = [(lang, path), (d["other"], opath)]
    ld = jld(app_ld(lang, BASE + path))
    (ROOT / lang / q["file"]).write_text(head(lang, q["title"], q["desc"], path, alts, "shot_board2.webp", ld) + chrome(lang, body))

def patch_index():
    p = ROOT / "index.html"; s = (pathlib.Path(__file__).resolve().parent / "captain_index_template.html").read_text()
    en = L["en"]; tr = L["tr"]
    desc = "Captain Mittens: Cat Match 3 is a free match-3 puzzle game for iPhone. Rescue kittens from cages, blast through boosters and rebuild a harbor town. Kedi eşleştirme oyunu, iPhone için ücretsiz."
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', s, 1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(desc)}">', s, 1)
    s = s.replace('<meta name="twitter:card" content="summary">', '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="%s%sshot_home.webp">' % (BASE, IMG))
    s = s.replace(f'<meta property="og:image" content="{BASE}{IMG}app-icon.png">', f'<meta property="og:image" content="{BASE}{IMG}shot_home.webp">')
    s = re.sub(r"\n?<!--seo-start-->.*?<!--seo-end-->", "", s, flags=re.S)
    blk = ("<!--seo-start-->\n" + (APPLE + "\n" if APPLE else "") + f'<link rel="alternate" hreflang="tr" href="{BASE}{tr["path"]}">\n<link rel="alternate" hreflang="en" href="{BASE}{en["path"]}">\n'
           f'<link rel="alternate" hreflang="x-default" href="{BASE}/captain-mittens/">\n' + jld(app_ld("en", BASE + "/captain-mittens/")) + "\n" + jld(faq_ld(en["faq"])) + "\n<!--seo-end-->")
    s = s.replace('<link rel="icon"', blk + '\n<link rel="icon"', 1)
    # "Coming soon" -> App Store button
    soon = re.compile(r'<span class="soon" role="status">.*?</span></span>', re.S)
    btn = f'<a class="store" href="{STORE}" rel="noopener"><span aria-hidden="true">&#63743;</span> <span class="en">{E(en["cta"])}</span><span class="tr" lang="tr">{E(tr["cta"])}</span></a>'
    if APP_LIVE:
        s = soon.sub(btn, s)
        s = s.replace("Coming soon to the App Store.", "Free on the App Store.").replace("Captain Mittens is coming soon to the App Store.", "Captain Mittens is free on the App Store.")
    if APP_LIVE:
        s = s.replace("Yavrular bekliyor. Captain Mittens çok yakında App Store'da.", "Yavrular bekliyor. Captain Mittens App Store'da ücretsiz.")
    items = "".join(f'<details><summary><span class="en">{E(eq)}</span><span class="tr" lang="tr">{E(tq)}</span></summary><p><span class="en">{E(ea)}</span><span class="tr" lang="tr">{E(ta)}</span></p></details>\n'
                    for (eq, ea), (tq, ta) in zip(en["faq"], tr["faq"]))
    faq = ('<section class="faq" id="faq">\n<div class="wrap narrow">\n <header class="sec-head"><p class="kicker">FAQ</p><h2><span class="en">Quick answers</span><span class="tr" lang="tr">Kısa cevaplar</span></h2></header>\n'
           + items + ' <p class="more"><a href="support.html"><span class="en">More on the support page</span><span class="tr" lang="tr">Destek sayfasında daha fazlası</span> &rarr;</a></p>\n</div>\n</section>')
    s = re.sub(r'<section class="faq" id="faq">.*?</section>', lambda m: faq, s, 1, flags=re.S)
    s = s.replace('<link rel="stylesheet" href="/captain-mittens/_style.css">', '<link rel="stylesheet" href="/captain-mittens/_style.css">\n<link rel="stylesheet" href="/captain-mittens/_seo.css">', 1) if "_seo.css" not in s else s
    p.write_text(s)

if __name__ == "__main__":
    for lg in L:
        (ROOT / lg).mkdir(exist_ok=True); landing(lg); query(lg)
    patch_index()
    print("ok")
