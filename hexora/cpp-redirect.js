// Hexora CPP redirect — swaps the App Store CTA href to a theme-matched
// Custom Product Page. Page authors mark anchors with data-cpp="oracle"
// or "journal"; TR visitors are routed to the Fal & Burç CPP regardless of
// the page-level theme (it's the only TR-localized page).
//
// Source of truth: ASC/CPP-URLS.md in the hexora repo.
(function () {
  var BASE = "https://apps.apple.com/us/app/hexora-i-ching-oracle/id6764511696";
  var CPPS = {
    oracle:  "6dbdcdb3-f4f2-4914-9a74-3e6cc05158b9",
    journal: "09069b59-909c-4032-b45a-3a861d80d1b6",
    fal:     "74dd3bfe-65a9-40c1-9461-2ef92c3a3763"
  };
  var lang = (navigator.language || "en").toLowerCase();
  var isTR = lang.indexOf("tr") === 0;

  document.querySelectorAll("a[data-cpp]").forEach(function (a) {
    var theme = isTR ? "fal" : a.getAttribute("data-cpp");
    var ppid = CPPS[theme];
    if (!ppid) return; // keep fallback href
    a.href = BASE + "?ppid=" + ppid + "&mt=8";
  });
})();
