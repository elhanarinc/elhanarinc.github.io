APP_LIVE = False  # flip to True at launch, re-run Scripts/build-captain-seo.py, update llms*.txt

"""Copy for the Captain Mittens SEO pages (TR first, EN adapted). Facts mirror the shipped build:
200 levels, 5 harbours (Liman, Tuzla, Bozcaada, Kaş, Amasra), no account, offline levels, weekly ranking, daily rewards."""
STORE = "https://apps.apple.com/app/id6824941057"
BASE = "https://elhanarinc.github.io"
MAIL = "elhanarinc@gmail.com"
NAME = "Captain Mittens: Cat Match 3"

L = {
"tr": {
 "locale": "tr_TR", "path": "/captain-mittens/tr/", "other": "en",
 "title": "Captain Mittens: Cat Match 3 | iPhone için ücretsiz kedi eşleştirme oyunu",
 "desc": "Captain Mittens: Cat Match 3, iPhone için ücretsiz match-3 bulmaca oyunu. Kafesteki yavru kedileri kurtar, fırtınada yıkılan liman kasabasını yeniden kur. Hesap gerekmez.",
 "h1": "Yavruları kurtar, kasabayı yeniden kur", "eyebrow": "Kedi eşleştirme oyunu",
 "pitch": "Fırtına limanı yıktı, yavru kediler kafeslere kapandı. Taşları eşleştir, kafesleri kır, limanı bir eşleşmeyle bir onar.",
 "cta": "App Store'dan indir", "free": "iPhone · Ücretsiz · Hesap gerekmez",
 "shots_h": "Oyundan görüntüler", "alts": ["Ana ekran: fırtınada yıkılmış liman ve görev düğmeleri", "Bölüm 64: eşleştirme tahtası ve dört güçlendirici", "Bölüm 11: yosun engelini tanıtan öğretici", "Roket ve yün bombası birleşip tahtada artı şeklinde patlıyor"],
 "feat_h": "Öne çıkanlar",
 "feats": [("Eşleştir ve patlat", "Üç ya da daha fazla taşı eşleştir; roket, yün bombası ve martı gibi özel taşlar yap, kombolar zinciri kur."),
  ("Limanı yeniden kur", "Yıldız topla, görevleri tamamla, fırtınada yıkılan Liman, Tuzla, Bozcaada, Kaş ve Amasra'yı adım adım onar."),
  ("200 bölüm", "200 bölüm ve beş liman var; fıçı, ip ve şamandıra gibi yeni engeller oyunu çeşitlendirir. Düzenli güncellemelerle yenileri gelecek."),
  ("Kurtarılacak kediler", "Her kafes bir yavru kedi; kurtardığın herkes tayfaya katılır."),
  ("Günlük ödüller ve haftalık sıralama", "Her gün ödül topla, haftalık sıralamada diğer oyuncularla yarış."),
  ("Hesapsız, internetsiz bölümler", "Üyelik yok. Bölümler internetsiz oynanır; sıralama, yedekleme ve ödüllü reklamlar için bağlantı gerekir.")],
 "faq_h": "Sık sorulan sorular",
 "faq": [("Captain Mittens ücretsiz mi?", "Evet, App Store'da ücretsiz indirilecek. İsteğe bağlı ödüllü reklamlar ve isteğe bağlı uygulama içi satın almalar vardır; oynamak için ödeme gerekmez."),
  ("İnternetsiz oynanır mı?", "Evet, bölümler internet olmadan oynanır. Haftalık sıralama, ilerleme yedeği ve ödüllü reklamlar için internet gerekir."),
  ("Kaç bölüm var?", "200 bölüm ve beş liman (Liman, Tuzla, Bozcaada, Kaş ve Amasra) var. Yenileri düzenli güncellemelerle eklenecek."),
  ("Hesap gerekiyor mu?", "Hayır. Üyelik ya da giriş yoktur. İlerlemen cihazında saklanır; rastgele bir Cihaz Kimliğiyle yedeklenir (Ayarlar → Hakkında → Cihaz Kimliği)."),
  ("Verilerimi nasıl sildiririm?", f"Cihaz Kimliğinle {MAIL} adresine yaz; verilerini sileriz. Ayrıntılar için Gizlilik Politikası'na ve Destek sayfasına bak.")],
 "nav": [("Destek", "/captain-mittens/support.html"), ("Gizlilik", "/captain-mittens/privacy.html"), ("Koşullar", "/captain-mittens/terms.html")],
 "switch": "English", "foot": "Apple ile bağlantılı değildir. App Store, Apple Inc. şirketinin hizmet markasıdır.",
 "q": {"file": "kedi-bulmaca-oyunu-iphone.html", "title": "iPhone için kedi bulmaca oyunu: Captain Mittens | Ücretsiz match-3",
  "desc": "iPhone'da kedili bir bulmaca oyunu mu arıyorsun? Captain Mittens ücretsiz bir match-3 oyunu: yavru kedileri kafesten kurtar, liman kasabasını yeniden kur.",
  "h1": "iPhone için kedi bulmaca oyunu", "alt": "Captain Mittens oyun içi görüntü",
  "body": ["Captain Mittens, iPhone için ücretsiz bir kedi temalı match-3 bulmaca oyunudur. Aynı renkteki taşları eşleştirirsin, kafeslere kapanmış yavru kedileri kurtarırsın ve fırtınada yıkılan liman kasabasını yeniden kurarsın.",
   "Kime göre? Kısa seanslarda rahatça oynamak isteyenlere. Bölümler internetsiz oynanır, hesap açmak gerekmez, reklamlar isteğe bağlıdır.",
   "Neye göre değil? 200 bölüm ve beş liman var; bu bir mobil oyun için sağlam bir başlangıç, sonsuz bir arşiv değil. Yenileri düzenli güncellemelerle gelecek.",
   "Nasıl işler: üç ya da daha fazla taşı eşleştir, dörtlü ve beşlilerle roket, yün bombası ya da martı yap, özel taşları birleştirip dev kombolar kur."],
  "links": "Daha fazlası", "home": "Oyun tanıtım sayfası"}},
"en": {
 "locale": "en_US", "path": "/captain-mittens/en/", "other": "tr",
 "title": "Captain Mittens: Cat Match 3 | Free cat match-3 puzzle game for iPhone",
 "desc": "Captain Mittens: Cat Match 3 is a free match-3 puzzle game for iPhone. Rescue caged kittens and rebuild a harbour town wrecked by a storm. No account needed.",
 "h1": "Rescue kittens, rebuild the town", "eyebrow": "Cat match-3 game",
 "pitch": "A storm wrecked the harbour and locked the kittens in cages. Match tiles, break the cages and bring the town back, one match at a time.",
 "cta": "Download on the App Store", "free": "iPhone · Free · No account needed",
 "shots_h": "Gameplay screenshots", "alts": ["Home screen: the storm-wrecked harbour with task buttons", "Level 64: the match-3 board with four boosters", "Level 11: the tutorial introducing seaweed blockers", "A rocket and a yarn bomb combining into a cross-shaped blast"],
 "feat_h": "Features",
 "feats": [("Match and blast", "Match three or more tiles, make specials like the rocket, yarn bomb and seagull, and chain combos."),
  ("Rebuild the harbour", "Earn stars, finish tasks and restore the storm-hit Liman harbour, Tuzla (the Salt Works), Bozcaada, Kaş and Amasra step by step."),
  ("200 levels", "200 levels and five harbours, with new obstacles like barrels, rope and buoys to keep things fresh. More arrive in regular updates."),
  ("Cats to rescue", "Every cage holds a kitten; every kitten you free joins the crew."),
  ("Daily rewards and weekly ranking", "Collect a reward every day and climb the weekly ranking."),
  ("No account, offline levels", "No sign-up. Levels play offline; the weekly ranking, progress backup and rewarded ads need a connection.")],
 "faq_h": "Frequently asked questions",
 "faq": [("Is Captain Mittens free?", "Yes, it will be free to download from the App Store. It has optional rewarded ads and optional in-app purchases; you never have to pay to play."),
  ("Can I play without internet?", "Yes, levels play offline. The weekly ranking, progress backup and rewarded ads need an internet connection."),
  ("How many levels are there?", "200 levels and five harbours (Liman, Tuzla, Bozcaada, Kaş and Amasra). More arrive in regular updates."),
  ("Do I need an account?", "No. There is no sign-up or login. Your progress is saved on your device and backed up under a random Device ID (Settings → About → Device ID)."),
  ("How do I delete my data?", f"Email {MAIL} with your Device ID and we will delete it. See the Privacy Policy and the Support page for details.")],
 "nav": [("Support", "/captain-mittens/support.html"), ("Privacy", "/captain-mittens/privacy.html"), ("Terms", "/captain-mittens/terms.html")],
 "switch": "Türkçe", "foot": "Not affiliated with Apple. App Store is a service mark of Apple Inc.",
 "q": {"file": "cat-match-3-game-iphone.html", "title": "Cat match 3 game for iPhone: Captain Mittens | Free puzzle game",
  "desc": "Looking for a cat match-3 game on iPhone? Captain Mittens is a free puzzle game: rescue caged kittens and rebuild a harbour town. No account needed.",
  "h1": "A cat match 3 game for iPhone", "alt": "Captain Mittens gameplay screenshot",
  "body": ["Captain Mittens is a free, cat-themed match-3 puzzle game for iPhone. You match tiles, rescue kittens locked in cages and rebuild a harbour town wrecked by a storm.",
   "Who it suits: short, relaxed sessions. Levels play offline, there is no account to create and ads are optional.",
   "Who it does not: 200 levels and five harbours is a solid start, not an endless library. It grows with regular updates.",
   "How it plays: match three or more, make a rocket, yarn bomb or seagull with bigger matches, then combine specials for huge combos."],
  "links": "More", "home": "Game page"}},
}

# Launch-date FAQ and CTA only while the app is not live yet.
_SOON = {"tr": ("Ne zaman çıkıyor?", "Çok yakında App Store'da."), "en": ("When does it launch?", "Coming soon to the App Store.")}
for _k in L:
    if not APP_LIVE:
        L[_k]["faq"] = L[_k]["faq"] + [_SOON[_k]]
        L[_k]["cta"] = {"tr": "Yakında App Store'da", "en": "Coming soon to the App Store"}[_k]
    else:
        L[_k]["faq"] = [(q, a.replace("indirilecek", "indirilir").replace("will be free", "is free")) for q, a in L[_k]["faq"]]
