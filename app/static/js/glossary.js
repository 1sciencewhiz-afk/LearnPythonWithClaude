/* Client-side filter for the glossary page - no server round trip needed
   since the whole list is already on the page. */
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var input = document.getElementById("glossary-filter");
    var list = document.getElementById("glossary-list");
    var empty = document.getElementById("glossary-empty");
    var countLabel = document.getElementById("glossary-count");
    if (!input || !list) return;

    var entries = Array.prototype.slice.call(list.querySelectorAll(".glossary-entry"));

    function applyFilter() {
      var query = input.value.trim().toLowerCase();
      var visible = 0;
      entries.forEach(function (entry) {
        var term = entry.dataset.term || "";
        var text = entry.textContent.toLowerCase();
        var matches = !query || term.indexOf(query) !== -1 || text.indexOf(query) !== -1;
        entry.hidden = !matches;
        if (matches) visible += 1;
      });
      if (countLabel) countLabel.textContent = visible + (visible === 1 ? " term" : " terms");
      if (empty) empty.hidden = visible !== 0;
    }

    input.addEventListener("input", applyFilter);

    // Land-on-a-term links (from a lesson's "Key terms" box) arrive with a
    // #term-... hash; make sure that entry is not hidden by a stale filter.
    if (window.location.hash) {
      var target = document.getElementById(window.location.hash.slice(1));
      if (target) target.hidden = false;
    }

    applyFilter();
  });
})();
