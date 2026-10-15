/* Wii U on iOS compatibility site. Copyright (c) 2026 MuffinEMU Development Team (Void). SPDX-License-Identifier: GPL-3.0-only. */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };

  /* ---- game explorer: search, status filter, sort, surprise me ---- */
  var grid = $("#gcards");
  if (grid) {
    var cards = $$(".gcard", grid), q = $("#gsearch"), sortSel = $("#gsort"), empty = $("#gempty");
    var status = "all";
    function apply() {
      var v = (q.value || "").trim().toLowerCase(), n = 0;
      cards.forEach(function (c) {
        var ok = (status === "all" || c.dataset.status === status) && (!v || c.dataset.search.indexOf(v) > -1);
        c.hidden = !ok; if (ok) n++;
      });
      var list = cards.slice();
      var by = sortSel.value;
      list.sort(function (a, b) {
        if (by === "name") return a.dataset.name.localeCompare(b.dataset.name);
        if (by === "fps") return (+b.dataset.fps) - (+a.dataset.fps);
        return (+a.dataset.rank) - (+b.dataset.rank) || a.dataset.name.localeCompare(b.dataset.name);
      });
      list.forEach(function (c) { grid.appendChild(c); });
      empty.hidden = n > 0;
      var cnt = $("#gcount"); if (cnt) cnt.textContent = n + (n === 1 ? " game" : " games");
    }
    q.addEventListener("input", apply); sortSel.addEventListener("change", apply);
    $$(".fbtn[data-status]").forEach(function (b) {
      b.addEventListener("click", function () {
        status = b.dataset.status;
        $$(".fbtn[data-status]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        apply();
      });
    });
    var s = $("#gsurprise");
    if (s) s.addEventListener("click", function () {
      var vis = cards.filter(function (c) { return !c.hidden; });
      if (vis.length) vis[Math.floor(Math.random() * vis.length)].click();
    });
    apply();
  }

  /* ---- live test checklist: read issue #1 from GitHub ---- */
  var host = $("#checklist");
  if (host) {
    var api = "https://api.github.com/repos/MuffinEMU/wiiu-ios-compatibility/issues/1";
    fetch(api, { headers: { Accept: "application/vnd.github+json" } }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (issue) {
      var done = 0, total = 0, html = "", open = false;
      String(issue.body || "").split(/\r?\n/).forEach(function (line) {
        var h = line.match(/^##\s+(.*)/);
        if (h) { if (open) html += "</ul>"; html += '<h2 class="tier">' + esc(h[1]) + '</h2><ul class="tl">'; open = true; return; }
        var m = line.match(/^(\s*)- \[( |x|X)\]\s+(.*)/);
        if (m && open) {
          var sub = m[1].length > 0, on = m[2] !== " ";
          total++; if (on) done++;
          html += '<li class="' + (sub ? "sub " : "") + (on ? "done" : "") + '"><span class="box">' + (on ? "&#10003;" : "") + '</span><span class="t">' + esc(m[3].replace(/\*\*/g, "")) + "</span></li>";
          return;
        }
        var g = line.match(/^- \*\*(.*)\*\*\s*$/);
        if (g && open) html += '<li class="sub-head"><strong>' + esc(g[1]) + "</strong></li>";
      });
      if (open) html += "</ul>";
      host.innerHTML = html;
      var pct = total ? Math.round(done / total * 100) : 0;
      $("#pbar").style.width = pct + "%";
      $("#pnum").textContent = done + " of " + total + " tested";
      $("#ppct").textContent = pct + "%";
      var hp = $("#homeprog"); if (hp) { hp.textContent = done + " of " + total; }
    }).catch(function () {
      host.innerHTML = '<p class="empty">The live checklist could not be loaded. <a href="https://github.com/MuffinEMU/wiiu-ios-compatibility/issues/1">Open it on GitHub</a>.</p>';
    });
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
})();
