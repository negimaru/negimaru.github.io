// Progressive enhancement only: the page is complete without this file.
(function () {
  var root = document.documentElement;
  var seg = document.querySelector('.seg');
  function stored() { try { return localStorage.getItem('theme'); } catch (_) { return null; } }
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
  // An earlier version of this site registered a service worker; remove it for returning visitors.
  if ('serviceWorker' in navigator && navigator.serviceWorker.getRegistrations) {
    navigator.serviceWorker.getRegistrations().then(function (rs) { rs.forEach(function (r) { r.unregister(); }); });
  }
})();
