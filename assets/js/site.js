// Progressive enhancement only: the page is complete without this file.
(function () {
  var root = document.documentElement;

  // Theme: Light / Dark / Auto (follows the system)
  var seg = document.querySelector('.seg');
  function sync() {
    var cur = root.dataset.theme || 'auto';
    seg.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.themeSet === cur)); });
  }
  if (seg) {
    seg.hidden = false;
    sync();
    seg.addEventListener('click', function (ev) {
      var b = ev.target.closest('button'); if (!b) return;
      var v = b.dataset.themeSet;
      if (v === 'auto') { delete root.dataset.theme; try { localStorage.removeItem('theme'); } catch (_) {} }
      else { root.dataset.theme = v; try { localStorage.setItem('theme', v); } catch (_) {} }
      sync();
    });
  }

  // Table of contents: mark the section being read
  var links = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (links.length && 'IntersectionObserver' in window) {
    var byId = {};
    links.forEach(function (a) { byId[a.hash.slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.removeAttribute('aria-current'); });
        var a = byId[en.target.id]; if (a) a.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    Object.keys(byId).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
  }

  // An earlier version of this site registered a service worker; remove it for returning visitors.
  if ('serviceWorker' in navigator && navigator.serviceWorker.getRegistrations) {
    navigator.serviceWorker.getRegistrations().then(function (rs) { rs.forEach(function (r) { r.unregister(); }); });
  }
})();
